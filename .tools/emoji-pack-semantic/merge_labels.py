#!/usr/bin/env python3
"""Склеивает labels_by_index.json с pack_raw.json → semantic_map.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from combo_schema import AGENT_RULES, SPACER_GUIDANCE, normalize_combos
from common import pack_dir, read_json, write_json
from export_agent_catalog import export_agent_catalog
from item_builder import build_by_tag


def merge_labels(pack_name: str, labels_path: Path | None = None) -> Path:
    base = pack_dir(pack_name)
    raw_path = base / "pack_raw.json"
    if not raw_path.exists():
        raise FileNotFoundError(f"Нет {raw_path}")

    labels_file = labels_path or (base / "labels_by_index.json")
    if not labels_file.exists():
        raise FileNotFoundError(
            f"Нет {labels_file}. Сохраните ответ vision-ИИ как labels_by_index.json"
        )

    pack_raw = read_json(raw_path)
    labels_data = read_json(labels_file)

    label_items = labels_data.get("items") or []
    by_index: dict[int, dict] = {}
    for item in label_items:
        idx = int(item["index"])
        by_index[idx] = item

    pack_type = labels_data.get("pack_type", "single")
    emojis = []
    missing = []
    for sticker in pack_raw["stickers"]:
        idx = int(sticker["index"])
        label = by_index.get(idx, {})
        if idx not in by_index:
            missing.append(idx)

        hint = label.get("hint_emoji") or label.get("description_emoji", "")
        entry = {
            "document_id": sticker.get("custom_emoji_id") or sticker.get("document_id"),
            "index": idx,
            "fallback_unicode": sticker.get("emoji", ""),
            "hint_emoji": hint,
            "tags": label.get("tags", []),
            "description": label.get("description", ""),
            "description_emoji": label.get("description_emoji", hint),
            "mood": label.get("mood", ""),
            "use_when": label.get("use_when", []),
        }
        for key in (
            "usage_mode",
            "item_type",
            "combo_group",
            "combo_role",
            "connects",
            "combo_with",
            "partial_combo",
        ):
            if key in label:
                entry[key] = label[key]
        emojis.append(entry)

    semantic = {
        "pack": pack_name,
        "title": pack_raw.get("title", ""),
        "pack_type": pack_type,
        "count": len(emojis),
        "emojis": emojis,
    }
    if labels_data.get("agent_rules"):
        semantic["agent_rules"] = labels_data["agent_rules"]
    elif pack_type == "composite":
        semantic["agent_rules"] = AGENT_RULES
    if labels_data.get("combos"):
        semantic["combos"] = normalize_combos(labels_data["combos"])
    if labels_data.get("scenes"):
        semantic["scenes"] = labels_data["scenes"]
    if labels_data.get("spacer_guide"):
        semantic["spacer_guide"] = labels_data["spacer_guide"]
    elif pack_type == "composite":
        semantic["spacer_guide"] = SPACER_GUIDANCE
    if labels_data.get("spacers"):
        semantic["spacers"] = []
        for sp in labels_data["spacers"]:
            idx = int(sp["index"])
            sticker = next(s for s in pack_raw["stickers"] if int(s["index"]) == idx)
            semantic["spacers"].append(
                {
                    **sp,
                    "document_id": sticker.get("custom_emoji_id") or sticker.get("document_id"),
                }
            )
    if missing:
        semantic["missing_labels"] = sorted(missing)
        print(f"  warn: нет меток для индексов: {missing}")

    combos = semantic.get("combos") or []
    semantic["by_tag"] = labels_data.get("by_tag") or build_by_tag(
        label_items, combos, pack_type=pack_type
    )

    out_path = base / "semantic_map.json"
    write_json(out_path, semantic)
    print(f"Карта: {out_path} ({len(emojis)} emoji)")
    export_agent_catalog(pack_name, out_path, out_dir=base)
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Собрать semantic_map.json")
    parser.add_argument("--pack", required=True, help="Short name пака")
    parser.add_argument(
        "--labels",
        type=Path,
        help="Путь к labels_by_index.json (по умолчанию output/<pack>/labels_by_index.json)",
    )
    args = parser.parse_args(argv)
    merge_labels(args.pack, args.labels)
    return 0


if __name__ == "__main__":
    sys.exit(main())
