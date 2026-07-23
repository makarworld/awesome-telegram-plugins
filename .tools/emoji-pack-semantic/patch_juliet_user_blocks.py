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
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [[idx[91], idx[92], idx[93]], [idx[99], idx[100]], [idx[107], idx[108], idx[109]]],
        "weight": 4,
    },
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [[idx[137], idx[136], idx[139]], [idx[145], idx[146], idx[147], idx[148]]],
        "weight": 4,
    },
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [[idx[133], idx[134]], [idx[141], idx[142]], [idx[149], idx[150]]],
        "weight": 4,
    },
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [[idx[173], idx[174], idx[175]], [idx[181], idx[182], idx[183]]],
        "weight": 4,
    },
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [
            [idx[153], idx[154]],
            [idx[161], idx[162]],
            [idx[169], idx[170]],
            [idx[177], idx[178]],
        ],
        "weight": 4,
    },
    {"decoration": True, "ids": [idx[140]], "weight": 2},
    {"decoration": True, "ids": [idx[129], idx[130]], "weight": 2},
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [[idx[63], idx[64]], [idx[71], idx[72]]],
        "weight": 3,
    },
    {
        "decoration": True,
        "block_line": True,
        "layout": "grid",
        "rows": [[idx[57], idx[58]], [idx[65], idx[66]]],
        "weight": 3,
    },
]


def collect_ids(item):
    ids = set()
    if "ids" in item:
        ids.update(item["ids"])
    for row in item.get("rows") or []:
        ids.update(row)
    return ids


def strip_target_ids(item):
    item = dict(item)
    if "ids" in item:
        item["ids"] = [x for x in item["ids"] if x not in TARGET_IDS]
        if not item["ids"]:
            del item["ids"]
    if "rows" in item:
        rows = [[x for x in row if x not in TARGET_IDS] for row in item["rows"]]
        rows = [row for row in rows if row]
        if rows:
            item["rows"] = rows
        else:
            del item["rows"]
    return item


def fmt_item(item, indent=4):
    sp = " " * indent
    inner = sp + "    "
    simple = set(item) <= {"decoration", "ids", "weight", "replace", "nature", "mur", "block_line", "layout", "slots"}
    if simple and "rows" not in item and ("ids" not in item or len(item.get("ids", [])) <= 3):
        parts = []
        for k, v in item.items():
            if k == "ids":
                parts.append(f'"ids": [{", ".join(str(x) for x in v)}]')
            elif isinstance(v, str):
                parts.append(f'"{k}": {json.dumps(v)}')
            else:
                parts.append(f'"{k}": {v}')
        return f"{sp}{{{', '.join(parts)}}},"
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
        elif isinstance(v, str):
            lines.append(f'{inner}"{k}": {json.dumps(v)},')
        else:
            lines.append(f'{inner}"{k}": {v},')
    lines.append(f"{sp}}},")
    return "\n".join(lines)


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

out = []
savobod_idx = None
for n, item in enumerate(custom):
    if isinstance(item, str):
        if "Savobodattealovers" in item:
            savobod_idx = len(out)
        out.append(item)
        continue
    ids = collect_ids(item)
    overlap = ids & TARGET_IDS
    if overlap:
        if ids <= TARGET_IDS and item.get("decoration"):
            continue
        item = strip_target_ids(item)
        if not collect_ids(item) and "replace" not in item:
            continue
    out.append(item)

if savobod_idx is None:
    for n, item in enumerate(out):
        if isinstance(item, str) and "Savobodattealovers" in item:
            savobod_idx = n
            break

if savobod_idx is None:
    savobod_idx = len(out)

for ub in reversed(USER_BLOCKS):
    out.insert(savobod_idx, ub)

lines = ["CUSTOM_EMOJI = ["]
for item in out:
    if isinstance(item, str):
        lines.append("    " + item.strip())
    else:
        lines.append(fmt_item(item))
lines.append("]")
new_text = text[:start] + "\n".join(lines) + text[end:]
PLUGIN.write_text(new_text, encoding="utf-8")
print(f"patched: {len(custom)} -> {len(out)} items, inserted {len(USER_BLOCKS)} blocks at {savobod_idx}")
