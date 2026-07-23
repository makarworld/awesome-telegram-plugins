#!/usr/bin/env python3
"""Генерация labels/semantic_map из pack_profiles/*.json."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
PROFILES_DIR = TOOL_DIR / "pack_profiles"


def _role(idx: int, indices: list[int], layout: str) -> str:
    if layout == "solo" or len(indices) == 1:
        return "center"
    pos = indices.index(idx)
    if layout == "sandwich":
        return "left_wing" if pos == 0 else "right_wing"
    if pos == 0:
        return "left"
    if pos == len(indices) - 1:
        return "right"
    return f"segment_{pos + 1}"


def _connects(role: str, layout: str) -> list[str]:
    if role == "center":
        return []
    if layout == "sandwich":
        return ["right"] if role == "left_wing" else ["left"]
    if role == "left":
        return ["right"]
    if role == "right":
        return ["left"]
    return ["left", "right"]


def build_from_profile(profile: dict, count: int) -> dict:
    pack_type = profile.get("pack_type", "single")
    combos = profile.get("combos", [])
    item_overrides = {int(k): v for k, v in profile.get("item_overrides", {}).items()}
    default = profile.get("default_item", {})
    index_to_combo: dict[int, dict] = {}
    for combo in combos:
        for idx in combo["indices"]:
            if idx not in index_to_combo:
                index_to_combo[idx] = combo

    items = []
    for idx in range(1, count + 1):
        if idx in item_overrides:
            item = {"index": idx, **item_overrides[idx]}
            items.append(item)
            continue
        combo = index_to_combo.get(idx)
        if combo:
            indices = combo["indices"]
            layout = combo.get("layout", "horizontal")
            role = _role(idx, indices, layout)
            others = [i for i in indices if i != idx]
            mode = "solo" if layout == "solo" else "combo_required"
            items.append(
                {
                    "index": idx,
                    "tags": list(combo.get("tags", [])) + ([role] if role != "center" else []),
                    "description": combo.get("description", combo["name"])
                    + (
                        f" Фрагмент {role}; стыкуется с {', '.join(f'#{i:03d}' for i in others)}."
                        if others
                        else ""
                    ),
                    "description_emoji": combo.get("description_emoji", "✨"),
                    "mood": combo.get("mood", "neutral"),
                    "use_when": combo.get("use_when", ["декор"]),
                    "usage_mode": mode,
                    "combo_group": combo["id"],
                    "combo_role": role,
                    "connects": _connects(role, layout),
                    "combo_with": others,
                }
            )
        else:
            items.append(
                {
                    "index": idx,
                    "tags": default.get("tags", ["декор", "эмодзи"]),
                    "description": default.get(
                        "description", "Элемент пака — уточните по pack_sheet.png."
                    ),
                    "description_emoji": default.get("description_emoji", "✨"),
                    "mood": default.get("mood", "neutral"),
                    "use_when": default.get("use_when", ["декор сообщения"]),
                    **(
                        {"usage_mode": "solo"}
                        if pack_type == "single"
                        else {
                            "usage_mode": "combo_optional",
                            "combo_group": None,
                            "combo_role": "fragment",
                            "connects": ["left", "right"],
                            "combo_with": [i for i in (idx - 1, idx + 1) if 1 <= i <= count],
                        }
                    ),
                }
            )

    combos_out = []
    for combo in combos:
        c = dict(combo)
        c["order"] = combo["indices"]
        combos_out.append(c)

    data = {
        "pack": profile["pack"],
        "pack_type": pack_type,
        "items": items,
    }
    if pack_type == "composite":
        data["combos"] = combos_out
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", help="Short name или путь к profile json")
    parser.add_argument("--no-merge", action="store_true")
    args = parser.parse_args(argv)

    if args.pack.endswith(".json"):
        profile_path = Path(args.pack)
    else:
        profile_path = PROFILES_DIR / f"{args.pack}.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))

    raw_path = TOOL_DIR / "output" / profile["pack"] / "pack_raw.json"
    count = json.loads(raw_path.read_text(encoding="utf-8"))["count"]
    data = build_from_profile(profile, count)

    out = TOOL_DIR / "output" / profile["pack"] / "labels_by_index.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"labels: {out} ({len(data['items'])} items)")

    if not args.no_merge:
        subprocess.run(
            [sys.executable, "merge_labels.py", "--pack", profile["pack"]],
            cwd=TOOL_DIR,
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
