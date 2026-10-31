import asyncio
import os
import time
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import (
    PORT, BRAND_NAME, DEFAULT_REMARK, SESSION_COOKIE,
    WS_PATH_PREFIX, SUB_PATH_PREFIX, PUBLIC_VIEW_PREFIX,
    REDIS_URL, REDIS_STATE_KEY
)
from core.manager import (
    LINKS, LINKS_LOCK, CONNECTIONS, STATS, AUTH,
    load_state, save_state_debounced, hash_password,
    create_session, is_valid_session, destroy_session,
    is_link_allowed
)
from core.sub import get_single_subscription, get_all_subscription, generate_vless_link
from core.tunnel import vless_ws_handler
from ui.portfolio import PORTFOLIO_HTML
from ui.login import LOGIN_HTML
from ui.dashboard import DASHBOARD_HTML
from ui.public_sub import PUBLIC_PAGE_HTML

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Midoxy")

app = FastAPI(title="Midoxy", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_request_host(request: Request) -> str:
    """Extract public domain cleanly from incoming request headers."""
    fwd_host = request.headers.get("x-forwarded-host")
    if fwd_host:
        return fwd_host.split(",")[0].strip()
    host_hdr = request.headers.get("host")
    if host_hdr:
        return host_hdr.split(":")[0].strip()
    return os.environ.get("PUBLIC_DOMAIN") or "localhost"


async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


def format_uptime() -> str:
    elapsed = int(time.time() - STATS["start_time"])
    days, rem = divmod(elapsed, 86400)
    hours, rem = divmod(rem, 3600)
    mins, _ = divmod(rem, 60)
    if days > 0:
        return f"{days}d {hours}h"
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


# ── Lifecycle ────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    await load_state()
    logger.info(f"Midoxy Node started on port {PORT}")


# ── Public Pages & Decoy ──────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index():
    """Decoy portfolio for root path."""
    return PORTFOLIO_HTML


@app.get("/health")
async def health():
    return {"status": "ok", "uptime": format_uptime(), "active": len(CONNECTIONS)}


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if await is_valid_session(token):
        return RedirectResponse(url="/dashboard")
    return LOGIN_HTML


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        return RedirectResponse(url="/login")
    return DASHBOARD_HTML


# ── Auth Endpoints ────────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    try:
        data = await request.json()
        password = data.get("password", "")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request")

    if hash_password(password) != AUTH["password_hash"]:
        return JSONResponse(status_code=401, content={"success": False, "message": "Invalid password"})

    token = await create_session()
    resp = JSONResponse(content={"success": True})
    resp.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite="lax",
    )
    return resp


@app.post("/api/logout")
async def api_logout(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    await destroy_session(token)
    resp = JSONResponse(content={"success": True})
    resp.delete_cookie(SESSION_COOKIE)
    return resp


@app.post("/api/change-password")
async def api_change_password(request: Request, _auth=Depends(require_auth)):
    try:
        data = await request.json()
        old_pwd = data.get("old_password", "")
        new_pwd = data.get("new_password", "")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid data")

    if hash_password(old_pwd) != AUTH["password_hash"]:
        return JSONResponse(status_code=400, content={"success": False, "message": "Incorrect current password"})

    if len(new_pwd) < 6:
        return JSONResponse(status_code=400, content={"success": False, "message": "New password must be at least 6 characters"})

    AUTH["password_hash"] = hash_password(new_pwd)
    await save_state_debounced()
    return {"success": True}


# ── Stats & Configs API ───────────────────────────────────────────────────────
@app.get("/api/stats")
async def api_stats(request: Request, _auth=Depends(require_auth)):
    return {
        "active_connections": len(CONNECTIONS),
        "total_bytes": STATS["total_bytes"],
        "total_requests": STATS["total_requests"],
        "total_errors": STATS["total_errors"],
        "uptime": format_uptime(),
        "host": get_request_host(request),
    }


@app.get("/api/links")
async def api_get_links(_auth=Depends(require_auth)):
    async with LINKS_LOCK:
        return list(LINKS.values())


@app.post("/api/links")
async def api_create_link(request: Request, _auth=Depends(require_auth)):
    data = await request.json()
    label = data.get("label", DEFAULT_REMARK).strip() or DEFAULT_REMARK
    limit_gb = float(data.get("limit_gb", 0))
    limit_bytes = int(limit_gb * 1024 * 1024 * 1024) if limit_gb > 0 else 0
    days = int(data.get("expires_days", 0))
    expires_at = None
    if days > 0:
        expires_at = (datetime.now() + timedelta(days=days)).isoformat()

    new_uuid = secrets.token_hex(16)
    formatted_uuid = f"{new_uuid[:8]}-{new_uuid[8:12]}-{new_uuid[12:16]}-{new_uuid[16:20]}-{new_uuid[20:]}"

    async with LINKS_LOCK:
        LINKS[formatted_uuid] = {
            "uuid": formatted_uuid,
            "label": label,
            "used_bytes": 0,
            "limit_bytes": limit_bytes,
            "expires_at": expires_at,
            "active": True,
            "created_at": datetime.now().isoformat(),
        }

    asyncio.create_task(save_state_debounced())
    return {"success": True, "uuid": formatted_uuid}


@app.post("/api/links/{uuid}/toggle")
async def api_toggle_link(uuid: str, request: Request, _auth=Depends(require_auth)):
    data = await request.json()
    active = bool(data.get("active", True))
    async with LINKS_LOCK:
        if uuid in LINKS:
            LINKS[uuid]["active"] = active
            asyncio.create_task(save_state_debounced())
            return {"success": True}
    raise HTTPException(status_code=404, detail="Config not found")


@app.delete("/api/links/{uuid}")
async def api_delete_link(uuid: str, _auth=Depends(require_auth)):
    async with LINKS_LOCK:
        if uuid in LINKS:
            del LINKS[uuid]
            asyncio.create_task(save_state_debounced())
            return {"success": True}
    raise HTTPException(status_code=404, detail="Config not found")


# ── Subscriptions & Client Manifests ──────────────────────────────────────────
@app.get(f"{SUB_PATH_PREFIX}/{{uuid}}")
async def subscription_single(uuid: str, request: Request):
    host = get_request_host(request)
    sub = await get_single_subscription(uuid, host)
    if not sub:
        raise HTTPException(status_code=404, detail="Configuration not found or inactive")
    content, headers = sub
    return Response(content=content, media_type="text/plain; charset=utf-8", headers=headers)


@app.get("/manifest")
async def subscription_manifest(request: Request):
    host = get_request_host(request)
    content, headers = await get_all_subscription(host)
    return Response(content=content, media_type="text/plain; charset=utf-8", headers=headers)


@app.get(f"{PUBLIC_VIEW_PREFIX}/{{uuid}}", response_class=HTMLResponse)
async def public_config_view(uuid: str, request: Request):
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link:
        raise HTTPException(status_code=404, detail="Not found")

    host = get_request_host(request)
    vless_link = generate_vless_link(uuid, host, remark=f"Midoxy-{link.get('label', DEFAULT_REMARK)}")

    used = link.get("used_bytes", 0)
    limit = link.get("limit_bytes", 0)
    used_str = f"{round(used / (1024**3), 2)} GB"
    limit_str = f"{round(limit / (1024**3), 2)} GB" if limit > 0 else "Unlimited"

    exp_str = link.get("expires_at", "Never")
    if exp_str and exp_str != "Never":
        try:
            exp_str = exp_str.split("T")[0]
        except Exception:
            pass

    status_str = "Active" if is_link_allowed(link) else "Suspended / Quota Exceeded"

    html = (
        PUBLIC_PAGE_HTML
        .replace("{{label}}", link.get("label", DEFAULT_REMARK))
        .replace("{{status}}", status_str)
        .replace("{{used}}", used_str)
        .replace("{{limit}}", limit_str)
        .replace("{{expires}}", str(exp_str))
        .replace("{{vless_url}}", vless_link)
    )
    return html


# ── WebSocket Stream Routes ───────────────────────────────────────────────────
# Active stream endpoint
app.add_api_websocket_route(f"{WS_PATH_PREFIX}/{{uuid}}", vless_ws_handler)
# Backward-compatibility alias for clients configured with /ws/{uuid}
app.add_api_websocket_route("/ws/{uuid}", vless_ws_handler)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)
