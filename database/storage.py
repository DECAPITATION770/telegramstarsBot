import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import aiofiles

_default_data_dir = Path(__file__).resolve().parent.parent / "data"
_data_path = os.getenv("DATA_PATH", "")
if _data_path.endswith(".json"):
    DATA_FILE = Path(_data_path)
else:
    DATA_DIR = Path(_data_path) if _data_path else _default_data_dir
    DATA_FILE = DATA_DIR / "users.json"


class JsonStorage:
    def __init__(self, path: Path | None = None):
        self.path = path or DATA_FILE
        self._data: dict = {"users": {}}
        self._lock = asyncio.Lock()

    async def _load(self) -> None:
        if self.path.exists():
            async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
                content = await f.read()
                self._data = json.loads(content) if content.strip() else {"users": {}}
        else:
            self._data = {"users": {}}

    async def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(self.path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self._data, ensure_ascii=False, indent=2))

    async def init(self) -> None:
        async with self._lock:
            await self._load()

    async def get_or_create_user(self, user_id: int) -> dict:
        async with self._lock:
            await self._load()
            uid = str(user_id)
            if uid not in self._data["users"]:
                self._data["users"][uid] = {
                    "stars": 0,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                }
                await self._save()
            return self._data["users"][uid]

    async def deduct_stars(self, user_id: int, amount: int) -> bool:
        async with self._lock:
            await self._load()
            uid = str(user_id)
            if uid not in self._data["users"]:
                return False
            user = self._data["users"][uid]
            if user["stars"] < amount:
                return False
            user["stars"] -= amount
            await self._save()
            return True


storage = JsonStorage()
