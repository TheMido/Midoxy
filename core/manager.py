import asyncio
import json
import time
import hashlib
import secrets
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque
from typing import Optional

from core.config import (
    DATA_DIR, DATA_FILE, REDIS_URL, REDIS_STATE_KEY,
    SECRET_KEY, ADMIN_PASSWORD, DEFAULT_REMARK, SESSION_TTL
)

logger = logging.getLogger("Midoxy")

LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()

SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

CONNECTIONS: dict = {}

STATS = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}

HOURLY_TRAFFIC: dict = defaultdict(int)
ACTIVITY_LOGS: deque = deque(maxlen=200)

SAVE_LOCK = asyncio.Lock()
_save_pending = False
_save_dirty_again = False
SAVE_DEBOUNCE_SECONDS = 3.0

redis_client = None
REDIS_CONNECTED = False


def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{SECRET_KEY}".encode()).hexdigest()


AUTH = {"password_hash": hash_password(ADMIN_PASSWORD)}


def log_activity(kind: str, message: str, level: str = "info"):
    ACTIVITY_LOGS.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })


def is_link_allowed(link: Optional[dict]) -> bool:
    if not link:
        return False
    if not link.get("active", True):
        return False
    limit = link.get("limit_bytes", 0)
    if limit > 0 and link.get("used_bytes", 0) >= limit:
        return False
    expires = link.get("expires_at")
    if expires:
        try:
            exp_dt = datetime.fromisoformat(expires)
            if datetime.now() > exp_dt:
                return False
        except Exception:
            pass
    return True


async def check_and_use(uid: str, nbytes: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if not link or not is_link_allowed(link):
            return False
        link["used_bytes"] = link.get("used_bytes", 0) + nbytes
        STATS["total_bytes"] += nbytes
        hour_key = datetime.now().strftime("%H:00")
        HOURLY_TRAFFIC[hour_key] += nbytes
    return True


def track_request():
    STATS["total_requests"] += 1


def track_error(msg: str):
    STATS["total_errors"] += 1
    log_activity("error", msg, "err")


async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token


async def is_valid_session(token: Optional[str]) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True


async def destroy_session(token: Optional[str]):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)


async def load_state():
    global LINKS, AUTH
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    loaded_data = None

    if REDIS_CONNECTED and redis_client:
        try:
            raw = await redis_client.get(REDIS_STATE_KEY)
            if raw:
                loaded_data = json.loads(raw)
        except Exception as e:
            logger.warning(f"Failed to read from Redis: {e}")

    if not loaded_data and DATA_FILE.exists():
        try:
            raw = DATA_FILE.read_text(encoding="utf-8")
            if raw:
                loaded_data = json.loads(raw)
        except Exception as e:
            logger.warning(f"Failed to read local state file: {e}")

    if loaded_data:
        async with LINKS_LOCK:
            LINKS.clear()
            LINKS.update(loaded_data.get("links", {}))
        if "password_hash" in loaded_data:
            AUTH["password_hash"] = loaded_data["password_hash"]
        logger.info(f"Loaded {len(LINKS)} configs from storage.")

    # Create default Midoxy config if none exists
    async with LINKS_LOCK:
        if not LINKS:
            default_uuid = secrets.token_hex(16)
            # format as 8-4-4-4-12 UUID
            formatted_uuid = f"{default_uuid[:8]}-{default_uuid[8:12]}-{default_uuid[12:16]}-{default_uuid[16:20]}-{default_uuid[20:]}"
            LINKS[formatted_uuid] = {
                "uuid": formatted_uuid,
                "label": DEFAULT_REMARK,
                "used_bytes": 0,
                "limit_bytes": 0,  # Unlimited by default
                "expires_at": None,
                "active": True,
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Created default Midoxy configuration: {formatted_uuid}")
            asyncio.create_task(save_state_debounced())


async def save_state():
    async with SAVE_LOCK:
        async with LINKS_LOCK:
            data = {
                "links": dict(LINKS),
                "password_hash": AUTH["password_hash"],
                "saved_at": datetime.now().isoformat(),
            }
        payload = json.dumps(data, ensure_ascii=False, indent=2)

        if REDIS_CONNECTED and redis_client:
            try:
                await redis_client.set(REDIS_STATE_KEY, payload)
            except Exception as e:
                logger.warning(f"Redis write error: {e}")

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            tmp = DATA_FILE.with_suffix(".tmp")
            tmp.write_text(payload, encoding="utf-8")
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")


async def save_state_debounced():
    global _save_pending, _save_dirty_again
    if _save_pending:
        _save_dirty_again = True
        return
    _save_pending = True
    try:
        while True:
            _save_dirty_again = False
            await asyncio.sleep(SAVE_DEBOUNCE_SECONDS)
            await save_state()
            if not _save_dirty_again:
                break
    finally:
        _save_pending = False

