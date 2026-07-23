#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
plugin = ROOT / "CuteMessages" / "cutemessagesenhanced.plugin"
frag = Path(__file__).resolve().parent / "plugin_emoji_batch_fragment.txt"

text = plugin.read_text(encoding="utf-8")
old_grid = """    {
        "nature": True,
        "layout": "grid",
        "rows": [
            [
                5422481775538501363,
                5425023077622768856,
                5422806887382940538,
                5415909492028105841,
                5413388947520780372,
                5422343967217839527,
                5422359678208210584,
                5424714157805038467,
                5422602794831999801,
            ],
            [5422656464743328682, 5422515984953015168, 5415582696556489435, 5413695238818525421],
        ],
        "block_line": True,
        "weight": 1,
    },
"""
if old_grid in text:
    text = text.replace(old_grid, "")
else:
    print("warn: tuwo nature grid not found, skip remove")

marker = "    # adapemoji @premiuss"
if marker not in text:
    raise SystemExit("marker not found")
batch = frag.read_text(encoding="utf-8")
if "# epicdepartmenthopeful" in text:
    raise SystemExit("batch already spliced?")
text = text.replace(marker, batch + "\n" + marker)
plugin.write_text(text, encoding="utf-8")
print(f"OK: {plugin} ({text.count(chr(10))} lines)")
