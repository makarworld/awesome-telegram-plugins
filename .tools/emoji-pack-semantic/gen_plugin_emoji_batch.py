#!/usr/bin/env python3
"""Генерация фрагмента CUSTOM_EMOJI для cutemessagesenhanced.plugin."""

from __future__ import annotations

import json
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "output"


def load_map(pack: str) -> dict[int, int]:
    raw = json.loads((OUTPUT / pack / "pack_raw.json").read_text(encoding="utf-8"))
    return {int(s["index"]): int(s["document_id"]) for s in raw["stickers"]}


def ids(m: dict[int, int], indices: list[int]) -> list[int]:
    return [m[i] for i in indices]


def band(m: dict[int, int], start: int, end: int, **kw) -> dict:
    n = end - start + 1
    entry = {"ids": ids(m, list(range(start, end + 1))), **kw}
    if "slots" not in entry:
        entry["slots"] = ["·"] * n
    return entry


def fmt_entry(e: dict) -> str:
    return json.dumps(e, ensure_ascii=False).replace("true", "True").replace("false", "False")


def solo(m: dict[int, int], index: int, **kw) -> dict:
    return {"ids": [m[index]], **kw}


def solos(m: dict[int, int], indices: list[int], **kw) -> list[dict]:
    return [solo(m, i, **kw) for i in indices]


def pairs(m: dict[int, int], pairs_list: list[tuple[int, int]], **kw) -> list[dict]:
    out = []
    for a, b in pairs_list:
        out.append({"ids": ids(m, [a, b]), **kw})
    return out


def emit(entries: list[dict], comment: str) -> str:
    lines = [f"    # {comment}"]
    for e in entries:
        lines.append("    " + fmt_entry(e) + ",")
    return "\n".join(lines)


def main() -> None:
    chunks: list[str] = []

    # epic — только #73
    m = load_map("epicdepartmenthopeful_by_fStikBot")
    chunks.append(emit([solo(m, 73, decoration=True, weight=2)], "epicdepartmenthopeful — solo #073"))

    # EsteticThngs — все solo decoration
    m = load_map("EsteticThngs")
    est = [solo(m, i, decoration=True, weight=1) for i in sorted(m)]
    chunks.append(emit(est, f"EsteticThngs — все {len(est)} solo"))

    # genadecorate — полосы
    m = load_map("genadecoratemoji")
    gena_bands = [
        band(m, 12, 17, decoration=True, block_line=True, weight=1),
        band(m, 23, 26, decoration=True, block_line=True, weight=1),
        band(m, 27, 30, decoration=True, block_line=True, weight=1),
        band(m, 40, 44, decoration=True, block_line=True, weight=1),
        band(m, 97, 99, decoration=True, block_line=True, weight=1),
        band(m, 100, 102, decoration=True, block_line=True, weight=1),
        band(m, 103, 105, decoration=True, block_line=True, weight=1),
        band(m, 112, 117, decoration=True, block_line=True, weight=1),
    ]
    chunks.append(emit(gena_bands, "genadecoratemoji — разделители"))

    # lostindiaries
    m = load_map("lostindiaries_by_fStikBot")
    lost_groups: list[dict] = [
        solo(m, 1, decoration=True, weight=2),
        solo(m, 2, decoration=True, weight=2),
        band(m, 3, 6, decoration=True, weight=2),
        band(m, 29, 32, decoration=True, weight=2),
        band(m, 91, 94, decoration=True, weight=2),
        band(m, 76, 77, decoration=True, weight=2),
        band(m, 157, 160, decoration=True, block_line=True, weight=1),
        band(m, 165, 166, decoration=True, weight=2),
        band(m, 194, 195, decoration=True, weight=2),
        band(m, 17, 19, decoration=True, weight=2),
        band(m, 113, 115, decoration=True, weight=2),
        solo(m, 86, decoration=True, weight=1),
        solo(m, 87, decoration=True, weight=1),
        solo(m, 88, decoration=True, weight=1),
        solo(m, 85, decoration=True, weight=1),
        band(m, 68, 69, decoration=True, weight=2),
        solo(m, 196, decoration=True, weight=1),
        solo(m, 164, decoration=True, weight=1),
        band(m, 161, 163, decoration=True, weight=2),
    ]
    chunks.append(emit(lost_groups, "lostindiaries"))

    # loveeemamaboss — перечисленные solo
    m = load_map("loveeemamaboss_by_TgEmodziBot")
    love_idx = [
        108, 114, 113, 74, 72, 17, 18, 19, 20, 21, 22, 23, 25, 26, 4, 5, 8, 10, 12,
        76, 77, 78, 81, 82, 44, 43, 47, 59, 56, 55, 51, 15, 35,
    ]
    chunks.append(emit(solos(m, love_idx, decoration=True, weight=1), "loveeemamaboss"))

    # sstamps — пары и диапазоны
    m = load_map("sstamps_by_TgEmodziBot")
    stamp_specs: list[tuple[int, int] | tuple[str, int, int]] = [
        (5, 6), (7, 8), (9, 10), (13, 14), (15, 16), (27, 28), (45, 46), (57, 58),
        ("range", 59, 69), (121, 122), (135, 136), (163, 164), (123, 124), (125, 126),
        (61, 62), (33, 34), (35, 36), (67, 68),
    ]
    stamp_entries: list[dict] = []
    for spec in stamp_specs:
        if spec[0] == "range":
            _, a, b = spec
            stamp_entries.append(band(m, a, b, decoration=True, weight=1))
        else:
            a, b = spec
            n = 2
            stamp_entries.append(
                {"ids": ids(m, [a, b]), "decoration": True, "weight": 1, "slots": ["·", "·"]}
            )
    chunks.append(emit(stamp_entries, "sstamps"))

    # tuwoqqqw — весь пак, каждый индекс solo
    m = load_map("tuwoqqqw_by_fStikBot")
    tuwo = [solo(m, i, decoration=True, weight=1) for i in sorted(m)]
    chunks.append(emit(tuwo, f"tuwoqqqw — все {len(tuwo)} solo"))

    out = Path(__file__).resolve().parent / "plugin_emoji_batch_fragment.txt"
    out.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
