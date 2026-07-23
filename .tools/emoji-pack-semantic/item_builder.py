"""Сборка items[] из combos[] для labels_by_index.json."""

from __future__ import annotations

from combo_schema import (
    _flat_indices,
    connects_for,
    grid_role,
    index_to_primary_combo,
    normalize_combos,
)


def _combo_with_list(combo: dict, idx: int) -> list[int]:
    return [i for i in _flat_indices(combo) if i != idx]


def _segment_description(combo: dict, idx: int, role: str) -> str:
    parent_id = combo.get("parent") or combo["id"]
    parent_name = combo.get("name", parent_id)
    indices = _flat_indices(combo)
    try:
        pos = indices.index(idx) + 1
    except ValueError:
        pos = 1
    total = len(indices)
    if role.startswith("r") and "c" in role:
        return f"Ячейка {role} объекта «{parent_name}»"
    return f"Кусок {pos}/{total} объекта «{parent_name}»"


def _is_segment(combo: dict, role: str) -> bool:
    if combo.get("complete") is False:
        return True
    return role.startswith("segment_") or (role.startswith("r") and "c" in role)


def build_items(
    count: int,
    combos_raw: list[dict],
    *,
    theme: str = "",
    pack_type: str = "composite",
    fallback_tags: list[str] | None = None,
) -> tuple[list[dict], list[dict]]:
    combos = normalize_combos(combos_raw)
    primary = index_to_primary_combo(combos)
    tags_base = fallback_tags or (["декор", theme] if theme else ["декор"])
    items: list[dict] = []

    for idx in range(1, count + 1):
        combo = primary.get(idx)
        if combo:
            layout = combo["layout"]
            if layout == "grid":
                role = grid_role(idx, combo["rows"])
            elif layout == "stack":
                role = f"stack_{combo['order'].index(idx) + 1}"
            elif layout == "sandwich":
                role = "left_wing" if combo["order"][0] == idx else "right_wing"
            elif layout == "spacer":
                role = "padding"
            elif layout == "solo":
                role = "center"
            elif combo["order"][0] == idx:
                role = "left"
            elif combo["order"][-1] == idx:
                role = "right"
            else:
                role = f"segment_{combo['order'].index(idx) + 1}"

            others = _combo_with_list(combo, idx)
            mode = "spacer" if layout == "spacer" else ("solo" if layout == "solo" else "combo_required")

            if _is_segment(combo, role):
                desc = _segment_description(combo, idx, role)
            elif layout == "grid" and combo.get("complete"):
                desc = combo.get("description", combo.get("name", ""))
                desc += f" Ячейка {role} в сетке."
            else:
                desc = combo.get("description", combo.get("name", ""))

            hint = combo.get("description_emoji", "✨")
            item = {
                "index": idx,
                "tags": list(combo.get("tags", [])) + ([role] if role not in ("center", "padding") else []),
                "description": desc,
                "description_emoji": hint,
                "hint_emoji": hint,
                "mood": combo.get("mood", "neutral"),
                "use_when": combo.get("use_when", ["декор"]),
                "usage_mode": mode,
                "combo_group": combo.get("parent") or combo["id"],
                "combo_role": role,
                "connects": connects_for(combo, idx),
                "combo_with": others,
            }
            if combo.get("item_type"):
                item["item_type"] = combo["item_type"]
            if combo.get("parent"):
                item["partial_combo"] = combo["id"]
        else:
            item = {
                "index": idx,
                "tags": tags_base + ["фрагмент", "неуверенно"],
                "description": f"Фрагмент пака{f' «{theme}»' if theme else ''}; не собирать сам — нужна доразметка combo.",
                "description_emoji": "🌿🍃✨",
                "hint_emoji": "🌿🍃✨",
                "mood": "neutral",
                "use_when": ["декор"],
                "usage_mode": "solo" if pack_type == "single" else "combo_optional",
                "combo_group": None,
                "combo_role": "solo" if pack_type == "single" else "fragment",
                "connects": [],
                "combo_with": [],
            }
        items.append(item)
    return items, combos


def build_by_tag(
    items: list[dict],
    combos: list[dict],
    *,
    pack_type: str,
) -> dict[str, list[str]]:
    by_tag: dict[str, list[str]] = {}

    def add(tag: str, ref: str) -> None:
        key = tag.strip().lower()
        if not key:
            return
        by_tag.setdefault(key, [])
        if ref not in by_tag[key]:
            by_tag[key].append(ref)

    if pack_type == "composite":
        for combo in combos:
            if combo.get("layout") == "spacer":
                continue
            ref = combo["id"]
            for tag in combo.get("tags") or []:
                add(tag, ref)
    else:
        for item in items:
            ref = str(item["index"])
            for tag in item.get("tags") or []:
                add(tag, ref)

    return dict(sorted(by_tag.items()))
