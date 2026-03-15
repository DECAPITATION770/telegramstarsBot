import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "")
ADMIN_IDS: set[int] = set()
WEB_SERVER_HOST: str = os.getenv("WEB_SERVER_HOST", "127.0.0.1")
WEB_SERVER_PORT: int = int(os.getenv("WEB_SERVER_PORT", "8080"))
WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")

_raw_admin_ids = os.getenv("ADMIN_IDS", "")
if _raw_admin_ids:
    for part in _raw_admin_ids.split(","):
        part = part.strip()
        if part.isdigit():
            ADMIN_IDS.add(int(part))


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
