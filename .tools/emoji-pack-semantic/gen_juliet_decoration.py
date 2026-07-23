import json
from pathlib import Path

raw = json.loads(
    Path(
        r"D:\Users\User\Projects\awesome-plugins\.tools\emoji-pack-semantic\output\juliet_diary_lesnaya_tropa_2_by_TgEmojiBot\pack_raw.json"
    ).read_text(encoding="utf-8")
)
idx = {s["index"]: s["document_id"] for s in raw["stickers"]}


def doc(*nums):
    return [idx[n] for n in nums]


def doc_rows(rows):
    return [[idx[n] for n in row] for row in rows]


combos = [
    ("vine_border_top", {"ids": doc(1, 2, 3, 4, 5, 6, 7, 8), "block_line": True, "weight": 5}),
    ("forest_floor_22_26", {"ids": doc(22, 23, 24, 25, 26), "block_line": True, "weight": 4}),
    ("curly_vines", {"ids": doc(27, 28, 29, 30), "block_line": True, "weight": 4}),
    ("flowers_65_72", {"ids": doc(65, 66, 67, 68, 69, 70, 71, 72), "block_line": True, "weight": 4}),
    ("flowers_83_95", {"ids": doc(*range(83, 96)), "block_line": True, "weight": 5}),
    (
        "forest_table_scene",
        {"layout": "grid", "rows": doc_rows([[105, 106], [107, 108], [109, 110]]), "block_line": True, "weight": 5},
    ),
    ("flowers_123_131", {"ids": doc(*range(123, 132)), "block_line": True, "weight": 5}),
    ("bonsai", {"layout": "grid", "rows": doc_rows([[157, 158], [165]]), "block_line": True, "weight": 5}),
    (
        "deep_forest_panorama",
        {
            "layout": "grid",
            "rows": doc_rows([list(range(166, 175)), list(range(175, 179))]),
            "block_line": True,
            "weight": 5,
        },
    ),
    ("clover_full", {"layout": "grid", "rows": doc_rows([[179, 180], [187, 188]]), "block_line": True, "weight": 4}),
    ("thorn_border", {"ids": doc(194, 195, 196, 197, 198), "block_line": True, "weight": 4}),
    ("mushroom_house_2x2", {"layout": "grid", "rows": doc_rows([[10, 11], [18, 19]]), "block_line": True, "weight": 4}),
    ("pink_flower_2x2", {"layout": "grid", "rows": doc_rows([[12, 13], [20, 21]]), "block_line": True, "weight": 4}),
    ("tree_2x2", {"layout": "grid", "rows": doc_rows([[25, 26], [33, 34]]), "block_line": True, "weight": 3}),
    ("anthurium_2x2", {"layout": "grid", "rows": doc_rows([[38, 39], [46, 47]]), "block_line": True, "weight": 3}),
    (
        "floral_branch_4x2",
        {"layout": "grid", "rows": doc_rows([[51, 52, 53, 54], [59, 60, 61, 62]]), "block_line": True, "weight": 4},
    ),
    ("brown_mushrooms_2x2", {"layout": "grid", "rows": doc_rows([[63, 64], [71, 72]]), "block_line": True, "weight": 3}),
    ("yellow_flower_2x2", {"layout": "grid", "rows": doc_rows([[73, 74], [81, 82]]), "block_line": True, "weight": 3}),
    ("green_plant_2x2", {"layout": "grid", "rows": doc_rows([[91, 92], [99, 100]]), "block_line": True, "weight": 3}),
    ("pink_peony_2x2", {"layout": "grid", "rows": doc_rows([[137, 138], [145, 146]]), "block_line": True, "weight": 3}),
    ("hanging_strands_2x2", {"layout": "grid", "rows": doc_rows([[141, 142], [149, 150]]), "block_line": True, "weight": 3}),
    ("dark_tree_2x2", {"layout": "grid", "rows": doc_rows([[153, 154], [161, 162]]), "block_line": True, "weight": 3}),
    ("fairy_dress_2x2", {"layout": "grid", "rows": doc_rows([[163, 164], [171, 172]]), "block_line": True, "weight": 3}),
    ("thick_trunk_2x2", {"layout": "grid", "rows": doc_rows([[169, 170], [177, 178]]), "block_line": True, "weight": 3}),
    ("apple_hearts_2x2", {"layout": "grid", "rows": doc_rows([[173, 174], [181, 182]]), "block_line": True, "weight": 3}),
    ("green_leaves_31_34", {"ids": doc(31, 32, 33, 34), "weight": 3}),
    ("floral_40_42", {"ids": doc(40, 41, 42), "weight": 2}),
    ("spring_buds_117_120", {"ids": doc(117, 118, 119, 120), "weight": 3}),
    ("meadow_133_136", {"ids": doc(133, 134, 135, 136), "weight": 3}),
    ("flowering_143_148", {"ids": doc(143, 144, 145, 146, 147, 148), "weight": 3}),
    ("forest_buds_151_154", {"ids": doc(151, 152, 153, 154), "weight": 3}),
    ("fairy_seated", {"layout": "grid", "rows": doc_rows([[9], [17]]), "weight": 3}),
    ("fairy_statue", {"layout": "grid", "rows": doc_rows([[14, 15], [22, 23]]), "weight": 3}),
    ("teapot", {"ids": doc(36, 37), "weight": 2}),
    ("moth_white", {"ids": doc(49, 50), "weight": 2}),
    ("butterfly_55_56", {"ids": doc(55, 56), "weight": 2}),
    ("mushroom_cap", {"ids": doc(57, 58), "weight": 2}),
    ("gnome_mushroom", {"ids": doc(65, 66), "weight": 2}),
    ("fawn", {"ids": doc(129, 130), "weight": 2}),
    ("moth_pink", {"ids": doc(183, 184), "weight": 2}),
    ("daisy_bouquet", {"ids": doc(16), "weight": 2}),
    ("fairy_statue_top", {"ids": doc(14, 15), "weight": 2}),
    ("pink_flower_pair", {"ids": doc(12, 13), "weight": 2}),
    ("peach_poppy", {"ids": doc(20, 21), "weight": 2}),
    ("yellow_flower_pair", {"ids": doc(61, 62), "weight": 2}),
    ("pink_blossom_101_102", {"ids": doc(101, 102), "weight": 2}),
    ("fairy_flower_hat", {"ids": doc(155, 156), "weight": 2}),
    ("heart_apple_row", {"ids": doc(181, 182, 183), "weight": 3}),
    ("butterfly_189_190", {"ids": doc(189, 190), "weight": 2}),
    ("butterfly_73_74", {"ids": doc(73, 74), "weight": 2}),
    ("mushroom_pair_43_44", {"ids": doc(43, 44), "weight": 2}),
]

lines = ["    # Juliet — decoration (все составные блоки пака)"]
for _name, spec in combos:
    parts = ['"decoration": True']
    if spec.get("block_line"):
        parts.append('"block_line": True')
    if "layout" in spec:
        parts.append(f'"layout": "{spec["layout"]}"')
    if "rows" in spec:
        rows_s = ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in spec["rows"])
        parts.append(f'"rows": [{rows_s}]')
    if "ids" in spec:
        ids_s = ", ".join(str(x) for x in spec["ids"])
        parts.append(f'"ids": [{ids_s}]')
    parts.append(f'"weight": {spec["weight"]}')
    if "rows" in spec or len(spec.get("ids", [])) > 3 or spec.get("block_line"):
        lines.append("    {")
        lines.append("        " + ",\n        ".join(parts) + ",")
        lines.append("    },")
    else:
        lines.append("    {" + ", ".join(parts) + "},")

out = Path(r"D:\Users\User\Projects\awesome-plugins\.tools\emoji-pack-semantic\juliet_decoration_block.txt")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("written", len(combos), "entries to", out)
