#!/usr/bin/env python3
"""Компактный каталог для агента: agent_catalog.md + agent_index.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from combo_schema import _flat_indices
from common import pack_dir, read_json, write_json

COMBO_KEYS = (
    "id",
    "layout",
    "complete",
    "visual_short",
    "name",
    "rows",
    "order",
    "left_wing",
    "right_wing",
    "allows_text_between",
    "do_not_insert_text",
    "width_risk",
    "alone_on_line",
    "parent",
    "accent_only",
    "max_per_message",
)


def _doc_map(emojis: list[dict]) -> dict[int, dict]:
    return {int(e["index"]): e for e in emojis}


def _combo_doc_ids(combo: dict, docs: dict[int, dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for idx in _flat_indices(combo):
        e = docs.get(idx)
        if e and e.get("document_id") is not None:
            out[str(idx)] = int(e["document_id"])
    return out


def _compact_combo(combo: dict, docs: dict[int, dict]) -> dict:
    c: dict = {}
    for key in COMBO_KEYS:
        if key in combo:
            c[key] = combo[key]
    doc_ids = _combo_doc_ids(combo, docs)
    if doc_ids:
        c["document_ids"] = doc_ids
    if combo.get("layout") == "sandwich" and combo.get("allows_text_between"):
        c["insert_text_between"] = True
    return c


def build_agent_index(data: dict) -> dict:
    emojis = data.get("emojis") or []
    docs = _doc_map(emojis)
    pack_type = data.get("pack_type", "single")

    combos_raw = data.get("combos") or []
    combos = [_compact_combo(c, docs) for c in combos_raw if c.get("layout") != "spacer"]

    spacers = []
    for sp in data.get("spacers") or []:
        entry = {
            "id": sp.get("id", f"spacer_{sp.get('index')}"),
            "index": int(sp["index"]),
        }
        if sp.get("document_id") is not None:
            entry["document_id"] = int(sp["document_id"])
        spacers.append(entry)

    solo: dict[str, dict] = {}
    for e in emojis:
        if e.get("usage_mode") not in ("solo", "spacer"):
            continue
        idx = str(e["index"])
        solo[idx] = {
            "document_id": int(e["document_id"]),
            "hint_emoji": e.get("hint_emoji") or e.get("description_emoji", ""),
            "mood": e.get("mood", ""),
            "tags": e.get("tags", [])[:6],
        }
        if e.get("combo_group"):
            solo[idx]["combo_group"] = e["combo_group"]

    index = {
        "pack": data.get("pack", ""),
        "title": data.get("title", ""),
        "pack_type": pack_type,
        "count": data.get("count", len(emojis)),
        "by_tag": data.get("by_tag") or {},
        "scenes": data.get("scenes") or [],
        "combos": combos,
        "spacers": spacers,
    }
    if solo:
        index["solo_by_index"] = solo
    return index


def _fmt_indices(combo: dict) -> str:
    layout = combo.get("layout", "")
    if layout == "grid" and combo.get("rows"):
        return f"rows: {combo['rows']}"
    if layout == "sandwich":
        lw = combo.get("left_wing")
        rw = combo.get("right_wing")
        if lw is not None and rw is not None:
            return f"left #{lw:03d} · текст · right #{rw:03d}"
    order = combo.get("order") or combo.get("indices") or []
    if order:
        return "order: " + ", ".join(f"#{i:03d}" for i in order)
    return ""


def _md_combo_line(combo: dict) -> list[str]:
    cid = combo["id"]
    layout = combo.get("layout", "?")
    complete = combo.get("complete", True)
    if layout == "spacer" or complete is False:
        return []

    flags = [layout]
    if combo.get("allows_text_between"):
        flags.append("sandwich+text")
    if combo.get("do_not_insert_text"):
        flags.append("no_text")
    if combo.get("width_risk") == "high":
        flags.append("wide")
    if combo.get("accent_only"):
        flags.append("accent")

    lines = [f"### `{cid}` ({', '.join(flags)})"]
    if combo.get("visual_short"):
        lines.append(f"- **Визуал:** {combo['visual_short']}")
    elif combo.get("name"):
        lines.append(f"- **Имя:** {combo['name']}")
    idx_line = _fmt_indices(combo)
    if idx_line:
        lines.append(f"- **Индексы:** {idx_line}")
    tags = combo.get("tags") or []
    if tags:
        lines.append(f"- **Теги:** {', '.join(tags[:8])}")
    use = combo.get("use_when") or []
    if use:
        lines.append(f"- **Когда:** {use[0]}")
    return lines


def build_catalog_md(data: dict, index: dict) -> str:
    pack = data.get("pack", "")
    title = data.get("title", pack)
    pack_type = data.get("pack_type", "single")

    lines = [
        f"# Agent catalog: {title}",
        "",
        f"Пак: `{pack}` · тип: **{pack_type}** · emoji: **{index['count']}**",
        "",
        "Полные `document_id` — в **`agent_index.json`** (поле `document_ids` у combo, `solo_by_index`).",
        "Полный дамп — `semantic_map.json` (только по необходимости).",
        "",
    ]

    rules = data.get("agent_rules") or []
    if rules:
        lines.append("## Правила сборки")
        lines.append("")
        for i, rule in enumerate(rules, 1):
            lines.append(f"{i}. {rule}")
        lines.append("")

    scenes = index.get("scenes") or []
    if scenes:
        lines.append("## Scenes (готовые рецепты)")
        lines.append("")
        for scene in scenes:
            sid = scene.get("id", "?")
            lines.append(f"### `{sid}`")
            if scene.get("description"):
                lines.append(scene["description"])
            blocks = scene.get("blocks") or []
            sep = scene.get("between_blocks", "blank_line")
            lines.append(f"- **Блоки:** {' → '.join(f'`{b}`' for b in blocks)}")
            if sep == "blank_line":
                lines.append("- **Между блоками:** пустая строка")
            lines.append("")

    combos = [c for c in (data.get("combos") or []) if c.get("complete") is not False and c.get("layout") != "spacer"]
    if combos:
        lines.append("## Combos (готовые объекты)")
        lines.append("")
        for combo in combos:
            lines.extend(_md_combo_line(combo))
            lines.append("")

    if index.get("spacers"):
        lines.append("## Spacers")
        lines.append("")
        for sp in index["spacers"]:
            lines.append(f"- `{sp['id']}` — index #{sp['index']:03d}")
        lines.append("")

    by_tag = index.get("by_tag") or {}
    if by_tag:
        lines.append("## Поиск by_tag")
        lines.append("")
        lines.append("Полный индекс — в `agent_index.json` → `by_tag`. Примеры:")
        lines.append("")
        sample = list(by_tag.items())[:12]
        for tag, refs in sample:
            preview = ", ".join(f"`{r}`" for r in refs[:5])
            if len(refs) > 5:
                preview += f" (+{len(refs) - 5})"
            lines.append(f"- **{tag}** → {preview}")
        if len(by_tag) > 12:
            lines.append(f"- …ещё {len(by_tag) - 12} тегов в agent_index.json")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def export_agent_catalog(
    pack_name: str,
    map_path: Path | None = None,
    *,
    out_dir: Path | None = None,
) -> tuple[Path, Path]:
    base = out_dir or pack_dir(pack_name)
    semantic_path = map_path or (base / "semantic_map.json")
    if not semantic_path.exists():
        raise FileNotFoundError(f"Нет {semantic_path}")

    data = read_json(semantic_path)
    index = build_agent_index(data)

    index_path = base / "agent_index.json"
    md_path = base / "agent_catalog.md"

    write_json(index_path, index)
    md_path.write_text(build_catalog_md(data, index), encoding="utf-8")

    md_kb = md_path.stat().st_size // 1024
    idx_kb = index_path.stat().st_size // 1024
    sem_kb = semantic_path.stat().st_size // 1024
    print(f"Каталог: {md_path} ({md_kb} KB)")
    print(f"Индекс:  {index_path} ({idx_kb} KB)  [semantic_map {sem_kb} KB]")
    return md_path, index_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Экспорт agent_catalog.md + agent_index.json")
    parser.add_argument("--pack", required=True)
    parser.add_argument("--map", type=Path, help="Путь к semantic_map.json")
    args = parser.parse_args(argv)
    export_agent_catalog(args.pack, args.map)
    return 0


if __name__ == "__main__":
    sys.exit(main())
