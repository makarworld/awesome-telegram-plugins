#!/usr/bin/env python3
"""Валидация semantic_map.json — инварианты v2."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from combo_schema import _flat_indices
from common import pack_dir, read_json


def validate_map(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []

    count = data.get("count", 0)
    emojis = data.get("emojis") or []
    combos = data.get("combos") or []
    pack_type = data.get("pack_type", "single")

    covered: set[int] = set()
    for e in emojis:
        covered.add(int(e["index"]))

    for i in range(1, count + 1):
        if i not in covered:
            errors.append(f"Индекс #{i:03d} не покрыт в emojis")

    complete_indices: dict[int, str] = {}
    for combo in combos:
        if not combo.get("complete"):
            continue
        cid = combo.get("id", "?")
        for idx in _flat_indices(combo):
            if idx in complete_indices:
                errors.append(
                    f"#{idx:03d} в двух complete: {complete_indices[idx]} и {cid}"
                )
            else:
                complete_indices[idx] = cid

    for combo in combos:
        cid = combo.get("id", "?")
        layout = combo.get("layout", "")

        if layout == "sandwich":
            for key in ("left_wing", "right_wing", "allows_text_between"):
                if key not in combo:
                    errors.append(f"{cid}: sandwich без {key}")
            if not combo.get("allows_text_between"):
                errors.append(f"{cid}: sandwich без allows_text_between=true")

        if layout == "grid":
            rows = combo.get("rows") or []
            grid_ids = {i for row in rows for i in row}
            declared = set(_flat_indices(combo))
            if grid_ids != declared:
                errors.append(f"{cid}: rows не покрывают indices")

        if combo.get("width_risk") == "high" and not combo.get("alone_on_line"):
            warns.append(f"{cid}: width_risk=high без alone_on_line")

        if str(cid).startswith("sparkle_") and combo.get("complete") and not combo.get("accent_only"):
            warns.append(f"{cid}: sparkle complete без accent_only")

        if "flowers_165_178" in cid:
            errors.append(f"{cid}: устаревший id flowers_165_178")

        if "deep_forest" in cid and 165 in _flat_indices(combo):
            errors.append(f"{cid}: #165 не должен быть в deep_forest (это bonsai)")

    scenes = data.get("scenes") or []
    combo_ids = {c["id"] for c in combos}
    for scene in scenes:
        for block in scene.get("blocks") or []:
            if block not in combo_ids:
                warns.append(f"scene {scene.get('id')}: блок {block} не найден в combos")

    return errors, warns


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Проверить semantic_map.json")
    parser.add_argument("--pack", required=True)
    parser.add_argument("--map", type=Path, help="Путь к semantic_map.json")
    args = parser.parse_args(argv)

    path = args.map or (pack_dir(args.pack) / "semantic_map.json")
    if not path.exists():
        print(f"Нет файла: {path}", file=sys.stderr)
        return 1

    data = read_json(path)
    errors, warns = validate_map(data)

    for w in warns:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s)", file=sys.stderr)
        return 1
    print(f"OK: 0 errors, {len(warns)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
