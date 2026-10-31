import os
import secrets
from pathlib import Path

# Brand & Identity
BRAND_NAME = "Midoxy"
TELEGRAM_LINK = "https://t.me/OFFL1NE"
DEFAULT_REMARK = "Midoxy"

# Server configuration
PORT = int(os.environ.get("PORT", 8000))
DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
DATA_FILE = DATA_DIR / "midoxy_state.json"
SECRET_FILE = DATA_DIR / ".midoxy_secret"

# Persistence & Storage
REDIS_URL = os.environ.get("REDIS_URL", "").strip()
REDIS_STATE_KEY = "midoxy:state"

def get_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")
    if env_secret:
        return env_secret
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SECRET_FILE.exists():
            val = SECRET_FILE.read_text(encoding="utf-8").strip()
            if val:
                return val
        new_sec = secrets.token_urlsafe(32)
        SECRET_FILE.write_text(new_sec, encoding="utf-8")
        return new_sec
    except Exception:
        return secrets.token_urlsafe(32)

SECRET_KEY = get_or_create_secret()

# Admin Authentication
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "123456")
SESSION_COOKIE = "midoxy_session"
SESSION_TTL = 60 * 60 * 24 * 7  # 7 days

# Endpoints & Routes (Configurable)
WS_PATH_PREFIX = os.environ.get("WS_PATH_PREFIX", "/stream")
SUB_PATH_PREFIX = os.environ.get("SUB_PATH_PREFIX", "/feed")
PUBLIC_VIEW_PREFIX = os.environ.get("PUBLIC_VIEW_PREFIX", "/view")

