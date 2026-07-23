import json
import re
from pathlib import Path

raw = json.loads(
    Path(
        r"D:\Users\User\Projects\awesome-plugins\.tools\emoji-pack-semantic\output\juliet_diary_lesnaya_tropa_2_by_TgEmojiBot\pack_raw.json"
    ).read_text(encoding="utf-8")
)
idx = {s["index"]: s["document_id"] for s in raw["stickers"]}

blocks = [
    ("forest_greenery", [[91, 92, 93], [99, 100], [107, 108, 109]], True, 4),
    ("white_blossom_cluster", [[137, 136, 139], [145, 146, 147, 148]], True, 4),
    ("meadow_hanging", [[133, 134], [141, 142], [149, 150]], True, 4),
    ("apple_hearts_block", [[173, 174, 175], [181, 182, 183]], True, 4),
    ("dark_forest_trees", [[153, 154], [161, 162], [169, 170], [177, 178]], True, 4),
    ("solo_140", None, False, 2),
    ("fawn", [129, 130], False, 2),
    ("brown_mushrooms", [[63, 64], [71, 72]], True, 3),
    ("gnome_cap", [[57, 58], [65, 66]], True, 3),
]

solo_140 = idx[140]
fawn_ids = [idx[129], idx[130]]

all_block_ids = set()
lines = []
for name, spec, block_line, weight in blocks:
    if name == "solo_140":
        all_block_ids.add(solo_140)
        lines.append(f'    {{"decoration": True, "ids": [{solo_140}], "weight": {weight}}},')
        continue
    if isinstance(spec[0], int):
        ids = [idx[i] for i in spec]
        all_block_ids.update(ids)
        lines.append(f'    {{"decoration": True, "ids": [{", ".join(str(x) for x in ids)}], "weight": {weight}}},')
        continue
    rows = [[idx[i] for i in row] for row in spec]
    for row in rows:
        all_block_ids.update(row)
    rows_s = ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in rows)
    parts = ['"decoration": True', '"block_line": True', '"layout": "grid"', f'"rows": [{rows_s}]', f'"weight": {weight}']
    lines.append("    {")
    lines.append("        " + ",\n        ".join(parts) + ",")
    lines.append("    },")

out = Path(r"D:\Users\User\Projects\awesome-plugins\.tools\emoji-pack-semantic\juliet_user_blocks.txt")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")

plugin = Path(r"D:\Users\User\Projects\awesome-plugins\CuteMessages\cutemessagesenhanced.plugin")
text = plugin.read_text(encoding="utf-8")
ids_in_plugin = set(int(x) for x in re.findall(r"\b\d{16,20}\b", text))
overlap = sorted(all_block_ids & ids_in_plugin)
print("block ids count", len(all_block_ids))
print("overlap with plugin", len(overlap))
for i in sorted(set(sum(([r for r in b[1]] if isinstance(b[1], list) and isinstance(b[1][0], list) else [b[1]] if isinstance(b[1], list) and isinstance(b[1][0], int) else [140] if b[0]=='solo_140' else []), start=[])) for b in blocks):
    print(i, idx[i])
