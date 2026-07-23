import ast
import json
from pathlib import Path

PLUGIN = Path(r"D:\Users\User\Projects\awesome-plugins\CuteMessages\cutemessagesenhanced.plugin")
RAW = Path(
    r"D:\Users\User\Projects\awesome-plugins\.tools\emoji-pack-semantic\output\juliet_diary_lesnaya_tropa_2_by_TgEmojiBot\pack_raw.json"
)
raw = json.loads(RAW.read_text(encoding="utf-8"))
idx = {s["index"]: s["document_id"] for s in raw["stickers"]}

TARGET_INDICES = {
    57, 58, 63, 64, 65, 66, 71, 72,
    91, 92, 93, 99, 100, 107, 108, 109,
    129, 130, 133, 134, 136, 137, 139, 140,
    141, 142, 145, 146, 147, 148, 149, 150,
    153, 154, 161, 162, 169, 170, 173, 174, 175,
    177, 178, 181, 182, 183,
}
TARGET_IDS = {idx[i] for i in TARGET_INDICES}

USER_BLOCKS = [
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[91], idx[92], idx[93]], [idx[99], idx[100]], [idx[107], idx[108], idx[109]]], "weight": 4},
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[137], idx[136], idx[139]], [idx[145], idx[146], idx[147], idx[148]]], "weight": 4},
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[133], idx[134]], [idx[141], idx[142]], [idx[149], idx[150]]], "weight": 4},
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[173], idx[174], idx[175]], [idx[181], idx[182], idx[183]]], "weight": 4},
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[153], idx[154]], [idx[161], idx[162]], [idx[169], idx[170]], [idx[177], idx[178]]], "weight": 4},
    {"decoration": True, "ids": [idx[140]], "weight": 2},
    {"decoration": True, "ids": [idx[129], idx[130]], "weight": 2},
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[63], idx[64]], [idx[71], idx[72]]], "weight": 3},
    {"decoration": True, "block_line": True, "layout": "grid", "rows": [[idx[57], idx[58]], [idx[65], idx[66]]], "weight": 3},
]

def collect_ids(item):
    ids = set()
    if isinstance(item, dict):
        ids.update(item.get("ids", []))
        for row in item.get("rows") or []:
            ids.update(row)
    return ids

def same_block(a, b):
    return collect_ids(a) == collect_ids(b) and a.get("layout") == b.get("layout")

text = PLUGIN.read_text(encoding="utf-8")
start = text.index("CUSTOM_EMOJI = [")
depth = 0
i = start + len("CUSTOM_EMOJI = ")
for j in range(i, len(text)):
    if text[j] == "[":
        depth += 1
    elif text[j] == "]":
        depth -= 1
        if depth == 0:
            end = j + 1
            break
custom = ast.literal_eval(text[start + len("CUSTOM_EMOJI = ") : end])

user_sigs = [collect_ids(b) for b in USER_BLOCKS]
out = []
removed = 0
for item in custom:
    ids = collect_ids(item)
    if ids and ids <= TARGET_IDS and item.get("decoration") and not any(same_block(item, ub) for ub in USER_BLOCKS):
        removed += 1
        continue
    if item.get("decoration") and ids == {idx[138]}:
        removed += 1
        continue
    if item.get("decoration") and len(item.get("rows", [[]])[0] if item.get("rows") else item.get("ids", [])) == 1 and item.get("block_line") and ids & TARGET_IDS:
        removed += 1
        continue
    out.append(item)

# ensure user blocks present once, before first savobod nature entry
SAVOBOD = 5282997962367075396
insert_at = next(i for i, x in enumerate(out) if collect_ids(x) == {SAVOBOD} or (isinstance(x, dict) and SAVOBOD in collect_ids(x)))
for ub in USER_BLOCKS:
    if not any(same_block(ub, x) for x in out if isinstance(x, dict)):
        out.insert(insert_at, ub)
        insert_at += 1

# dedupe exact user blocks at tail
seen = []
deduped = []
for item in out:
    if isinstance(item, dict) and item.get("decoration"):
        sig = (frozenset(collect_ids(item)), item.get("layout"), tuple(tuple(r) for r in item.get("rows") or ()))
        if sig in seen and collect_ids(item) <= TARGET_IDS | {idx[140]}:
            continue
        if collect_ids(item) <= TARGET_IDS | {idx[140]}:
            seen.append(sig)
    deduped.append(item)

print("removed", removed, "len", len(deduped))

# write back using repr for replace strings to keep emojis - actually use original slice for header
# reload from git for replace lines? use json only for changed part

def fmt_item(item, indent=4):
    sp = " " * indent
    inner = sp + "    "
    if set(item.keys()) <= {"decoration", "ids", "weight"}:
        return f'{sp}{{"decoration": True, "ids": [{", ".join(str(x) for x in item["ids"])}], "weight": {item["weight"]}}},'
    lines = [f"{sp}{{"]
    for k, v in item.items():
        if k == "rows":
            lines.append(f'{inner}"rows": [')
            for row in v:
                lines.append(inner + "    [" + ", ".join(str(x) for x in row) + "],")
            lines.append(f"{inner}],")
        elif k == "ids":
            if len(v) > 3:
                lines.append(f'{inner}"ids": [')
                for x in v:
                    lines.append(f"{inner}    {x},")
                lines.append(f"{inner}],")
            else:
                lines.append(f'{inner}"ids": [{", ".join(str(x) for x in v)}],')
        elif k == "replace":
            lines.append(f'{inner}"replace": {v!r},')
        elif isinstance(v, str):
            lines.append(f'{inner}"{k}": {v!r},')
        else:
            lines.append(f'{inner}"{k}": {v},')
    lines.append(f"{sp}}},")
    return "\n".join(lines)

lines = ["CUSTOM_EMOJI = ["]
for item in deduped:
    if isinstance(item, str):
        lines.append("    " + item)
    elif "replace" in item and len(item) == 2:
        lines.append(f'    {{"ids": [{item["ids"][0]}], "replace": {item["replace"]!r}}},')
    else:
        lines.append(fmt_item(item))
lines.append("]")
PLUGIN.write_text(text[:start] + "\n".join(lines) + text[end:], encoding="utf-8")
