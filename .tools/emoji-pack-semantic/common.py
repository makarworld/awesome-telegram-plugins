from __future__ import annotations

import json
import os
import re
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = TOOL_DIR / "output"


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or TOOL_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_bot_token() -> str:
    load_dotenv()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN не задан. Скопируйте .env.example → .env и вставьте токен бота."
        )
    return token


def pack_name_from_url(url: str) -> str:
    url = url.strip()
    patterns = (
        r"t\.me/addemoji/([A-Za-z0-9_]+)",
        r"tg://addemoji\?set=([A-Za-z0-9_]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_]+", url):
        return url
    raise ValueError(f"Не удалось извлечь имя пака из: {url}")


def pack_dir(pack_name: str) -> Path:
    return OUTPUT_DIR / pack_name


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
