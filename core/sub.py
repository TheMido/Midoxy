import base64
from urllib.parse import quote
from datetime import datetime
from core.config import WS_PATH_PREFIX, DEFAULT_REMARK
from core.manager import LINKS, LINKS_LOCK, is_link_allowed


def generate_vless_link(uuid: str, host: str, remark: str = DEFAULT_REMARK, path: str = None) -> str:
    if not path:
        path = f"{WS_PATH_PREFIX}/{uuid}"
    
    # Query parameters optimized for Iranian network bypass (TLS, Chrome fingerprint, HTTP/2 ALPN)
    params = {
        "encryption": "none",
        "security": "tls",
        "type": "ws",
        "host": host,
        "path": path,
        "sni": host,
        "fp": "chrome",
        "alpn": "h2",
    }
    query_str = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"vless://{uuid}@{host}:443?{query_str}#{quote(remark)}"


def build_sub_headers(label: str, used_bytes: int, limit_bytes: int, expires_at: str | None = None) -> dict:
    headers = {
        "profile-title": quote(label),
        "content-disposition": f'inline; filename="{quote(label)}"',
        "profile-update-interval": "24",
    }
    expire_ts = 0
    if expires_at:
        try:
            expire_ts = int(datetime.fromisoformat(expires_at).timestamp())
        except Exception:
            pass
    # Standard subscription-userinfo header recognized by modern proxy clients
    headers["subscription-userinfo"] = f"upload=0; download={used_bytes}; total={limit_bytes}; expire={expire_ts}"
    return headers


async def get_single_subscription(uuid: str, host: str) -> tuple[str, dict] | None:
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if not link or not is_link_allowed(link):
            return None
        label = link.get("label", DEFAULT_REMARK)
        used = link.get("used_bytes", 0)
        limit = link.get("limit_bytes", 0)
        expires = link.get("expires_at")

    vless_url = generate_vless_link(uuid, host, remark=f"Midoxy-{label}")
    b64_content = base64.b64encode((vless_url + "\n").encode("utf-8")).decode("utf-8")
    headers = build_sub_headers(label, used, limit, expires)
    return b64_content, headers


async def get_all_subscription(host: str) -> tuple[str, dict]:
    async with LINKS_LOCK:
        active_links = [l for l in LINKS.values() if is_link_allowed(l)]
        total_used = sum(l.get("used_bytes", 0) for l in active_links)
        total_limit = sum(l.get("limit_bytes", 0) for l in active_links)

    lines = [
        generate_vless_link(l["uuid"], host, remark=f"Midoxy-{l.get('label', DEFAULT_REMARK)}")
        for l in active_links
    ]
    raw_text = "\n".join(lines) + ("\n" if lines else "")
    b64_content = base64.b64encode(raw_text.encode("utf-8")).decode("utf-8")
    headers = build_sub_headers("Midoxy-All", total_used, total_limit)
    return b64_content, headers

