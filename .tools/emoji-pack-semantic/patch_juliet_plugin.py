from pathlib import Path

plugin = Path(r"D:\Users\User\Projects\awesome-plugins\CuteMessages\cutemessagesenhanced.plugin")
block = Path(r"D:\Users\User\Projects\awesome-plugins\.tools\emoji-pack-semantic\juliet_decoration_block.txt")

text = plugin.read_text(encoding="utf-8")
new_block = block.read_text(encoding="utf-8").rstrip() + "\n"

start_marker = "    # Juliet — decoration"
end_marker = "    # Savobodattealovers @tttea_lovers свобода"

start = text.find(start_marker)
end = text.find(end_marker)
if start == -1 or end == -1 or end <= start:
    raise SystemExit(f"markers not found: start={start}, end={end}")

updated = text[:start] + new_block + text[end:]
plugin.write_text(updated, encoding="utf-8")
print("replaced juliet decoration block")
