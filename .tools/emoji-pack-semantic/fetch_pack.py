#!/usr/bin/env python3
"""Скачивает custom emoji pack через Telegram Bot API."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

from common import get_bot_token, pack_dir, pack_name_from_url, write_json

API_BASE = "https://api.telegram.org/bot{token}/{method}"


def api_call(token: str, method: str, **params):
    url = API_BASE.format(token=token, method=method)
    response = requests.get(url, params=params, timeout=120)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"{method} failed: {data.get('description', data)}")
    return data["result"]


def download_file(token: str, file_id: str, dest: Path) -> Path:
    file_info = api_call(token, "getFile", file_id=file_id)
    file_path = file_info["file_path"]
    ext = Path(file_path).suffix or ".bin"
    dest = dest.with_suffix(ext)
    dest.parent.mkdir(parents=True, exist_ok=True)

    file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    with requests.get(file_url, timeout=180, stream=True) as resp:
        resp.raise_for_status()
        dest.write_bytes(resp.content)
    return dest


def pick_preview_file_id(sticker: dict) -> str:
    thumb = sticker.get("thumbnail") or sticker.get("thumb")
    if thumb and thumb.get("file_id"):
        return thumb["file_id"]
    return sticker["file_id"]


def normalize_sticker(sticker: dict, index: int) -> dict:
    custom_id = sticker.get("custom_emoji_id")
    if custom_id is not None:
        custom_id = int(custom_id)
    return {
        "index": index,
        "custom_emoji_id": custom_id,
        "document_id": custom_id,
        "emoji": sticker.get("emoji", ""),
        "file_id": sticker.get("file_id", ""),
        "file_unique_id": sticker.get("file_unique_id", ""),
        "is_animated": bool(sticker.get("is_animated")),
        "is_video": bool(sticker.get("is_video")),
        "type": sticker.get("type", ""),
        "width": sticker.get("width"),
        "height": sticker.get("height"),
        "preview_file_id": pick_preview_file_id(sticker),
    }


def fetch_pack(token: str, pack_name: str) -> Path:
    result = api_call(token, "getStickerSet", name=pack_name)
    stickers = result.get("stickers") or []
    if not stickers:
        raise RuntimeError(f"Пак '{pack_name}' пуст или недоступен.")

    out = pack_dir(pack_name)
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    items = []
    for i, sticker in enumerate(stickers, start=1):
        item = normalize_sticker(sticker, i)
        asset_name = f"{i:03d}"
        if item["custom_emoji_id"] is not None:
            asset_name += f"_{item['custom_emoji_id']}"
        dest = assets / asset_name
        saved = download_file(token, item["preview_file_id"], dest)
        item["asset_file"] = saved.name
        items.append(item)
        print(f"  [{i}/{len(stickers)}] {saved.name}")

    pack_raw = {
        "pack": pack_name,
        "title": result.get("title", ""),
        "name": result.get("name", pack_name),
        "sticker_type": result.get("sticker_type", ""),
        "is_animated": bool(result.get("is_animated")),
        "is_video": bool(result.get("is_video")),
        "count": len(items),
        "stickers": items,
    }
    raw_path = out / "pack_raw.json"
    write_json(raw_path, pack_raw)
    print(f"Сохранено: {raw_path} ({len(items)} emoji)")
    return raw_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Скачать custom emoji pack через Bot API")
    parser.add_argument(
        "--name",
        help="Short name пака (например epicdepartmenthopeful_by_fStikBot)",
    )
    parser.add_argument(
        "--url",
        help="URL t.me/addemoji/... (альтернатива --name)",
    )
    args = parser.parse_args(argv)

    if not args.name and not args.url:
        parser.error("Укажите --name или --url")

    pack_name = args.name or pack_name_from_url(args.url)
    token = get_bot_token()

    print(f"Загрузка пака: {pack_name}")
    fetch_pack(token, pack_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
