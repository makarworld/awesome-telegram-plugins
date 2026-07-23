#!/usr/bin/env python3
"""Собирает PNG-сетку и HTML-галерею для vision-анализа emoji-пака."""

from __future__ import annotations

import argparse
import html
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import pack_dir, read_json, write_json

DEFAULT_CELL = 112
DEFAULT_COLS = 10
LABEL_HEIGHT = 36
PADDING = 8
BG_COLOR = (24, 24, 28)
CELL_BG = (40, 40, 48)
TEXT_COLOR = (230, 230, 235)
MUTED_COLOR = (160, 160, 170)


def load_font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def short_id(custom_emoji_id: int | None) -> str:
    if custom_emoji_id is None:
        return "—"
    text = str(custom_emoji_id)
    return text[-6:] if len(text) > 6 else text


def build_sheet(
    pack_name: str,
    cell_size: int = DEFAULT_CELL,
    cols: int = DEFAULT_COLS,
) -> tuple[Path, Path]:
    base = pack_dir(pack_name)
    raw_path = base / "pack_raw.json"
    if not raw_path.exists():
        raise FileNotFoundError(f"Нет {raw_path}. Сначала: python fetch_pack.py --name {pack_name}")

    pack_raw = read_json(raw_path)
    stickers = pack_raw["stickers"]
    assets = base / "assets"
    rows = math.ceil(len(stickers) / cols)

    label_h = LABEL_HEIGHT
    sheet_w = PADDING * 2 + cols * cell_size
    sheet_h = PADDING * 2 + rows * (cell_size + label_h)

    sheet = Image.new("RGB", (sheet_w, sheet_h), BG_COLOR)
    draw = ImageDraw.Draw(sheet)
    font_main = load_font(14)
    font_small = load_font(11)

    gallery_items: list[dict] = []

    for idx, sticker in enumerate(stickers):
        row = idx // cols
        col = idx % cols
        x0 = PADDING + col * cell_size
        y0 = PADDING + row * (cell_size + label_h)

        draw.rectangle(
            [x0, y0, x0 + cell_size - 1, y0 + cell_size - 1],
            fill=CELL_BG,
        )

        asset_path = assets / sticker["asset_file"]
        if asset_path.exists():
            try:
                img = Image.open(asset_path).convert("RGBA")
                img.thumbnail((cell_size - 16, cell_size - 16), Image.Resampling.LANCZOS)
                paste_x = x0 + (cell_size - img.width) // 2
                paste_y = y0 + (cell_size - img.height) // 2
                sheet.paste(img, (paste_x, paste_y), img)
            except OSError as exc:
                draw.text((x0 + 8, y0 + 8), "?", fill=TEXT_COLOR, font=font_main)
                print(f"  warn: {asset_path.name}: {exc}")
        else:
            draw.text((x0 + 8, y0 + 8), "?", fill=TEXT_COLOR, font=font_main)

        index = sticker["index"]
        cid = sticker.get("custom_emoji_id")
        label_y = y0 + cell_size + 4
        draw.text((x0 + 4, label_y), f"#{index:03d}", fill=TEXT_COLOR, font=font_main)
        draw.text(
            (x0 + 4, label_y + 16),
            f"id …{short_id(cid)}",
            fill=MUTED_COLOR,
            font=font_small,
        )

        gallery_items.append(
            {
                "index": index,
                "custom_emoji_id": cid,
                "emoji": sticker.get("emoji", ""),
                "asset_file": sticker["asset_file"],
            }
        )

    png_path = base / "pack_sheet.png"
    sheet.save(png_path, "PNG", optimize=True)

    html_path = base / "gallery.html"
    html_path.write_text(
        render_gallery_html(pack_raw, gallery_items, cell_size),
        encoding="utf-8",
    )

    meta = {
        "pack": pack_name,
        "title": pack_raw.get("title", ""),
        "count": len(stickers),
        "cols": cols,
        "cell_size": cell_size,
        "sheet": png_path.name,
        "gallery": html_path.name,
    }
    write_json(base / "sheet_meta.json", meta)

    print(f"Сетка: {png_path}")
    print(f"Галерея: {html_path}")
    return png_path, html_path


def render_gallery_html(pack_raw: dict, items: list[dict], cell_size: int) -> str:
    title = html.escape(pack_raw.get("title") or pack_raw.get("pack", "Emoji pack"))
    cards = []
    for item in items:
        idx = item["index"]
        cid = item["custom_emoji_id"]
        emoji = html.escape(item.get("emoji") or "")
        asset = html.escape(item["asset_file"])
        cards.append(
            f"""
        <div class="card">
          <img src="assets/{asset}" alt="#{idx:03d}" loading="lazy" />
          <div class="meta">
            <div class="idx">#{idx:03d}</div>
            <div class="id">id …{html.escape(short_id(cid))}</div>
            <div class="unicode">{emoji}</div>
            <div class="full-id">{cid or ""}</div>
          </div>
        </div>"""
        )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #18181c;
      --card: #282830;
      --text: #e6e6eb;
      --muted: #a0a0aa;
    }}
    body {{
      margin: 0;
      font-family: system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 16px;
    }}
    h1 {{ font-size: 1.25rem; margin: 0 0 4px; }}
    .sub {{ color: var(--muted); margin-bottom: 16px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax({cell_size + 24}px, 1fr));
      gap: 12px;
    }}
    .card {{
      background: var(--card);
      border-radius: 10px;
      padding: 10px;
      text-align: center;
    }}
    .card img {{
      width: {cell_size}px;
      height: {cell_size}px;
      object-fit: contain;
      image-rendering: auto;
    }}
    .idx {{ font-weight: 700; font-size: 1rem; }}
    .id, .unicode {{ color: var(--muted); font-size: 0.85rem; }}
    .full-id {{
      font-size: 0.7rem;
      color: #666;
      word-break: break-all;
      margin-top: 4px;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <div class="sub">{html.escape(pack_raw.get("pack", ""))} · {len(items)} emoji</div>
  <div class="grid">{"".join(cards)}
  </div>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Собрать PNG-сетку и HTML-галерею")
    parser.add_argument("--pack", required=True, help="Short name пака")
    parser.add_argument("--cell", type=int, default=DEFAULT_CELL, help="Размер ячейки (px)")
    parser.add_argument("--cols", type=int, default=DEFAULT_COLS, help="Колонок в сетке")
    args = parser.parse_args(argv)

    build_sheet(args.pack, cell_size=args.cell, cols=args.cols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
