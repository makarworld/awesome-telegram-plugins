#!/usr/bin/env python3
"""Пакетный fetch + sheet + базовые labels для нескольких паков."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent

# Составные паки: ширина щита = ширина горизонтального glue-ряда в чате
SHEET_COLS_BY_PACK = {
    "juliet_diary_lesnaya_tropa_2_by_TgEmojiBot": 8,
}


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=TOOL_DIR, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packs", nargs="+", help="Short names паков")
    parser.add_argument("--cell", type=int, default=96)
    parser.add_argument("--cols", type=int, default=0, help="0 = auto")
    args = parser.parse_args(argv)

    for pack in args.packs:
        run([sys.executable, "fetch_pack.py", "--name", pack])
        raw = TOOL_DIR / "output" / pack / "pack_raw.json"
        import json

        count = json.loads(raw.read_text(encoding="utf-8"))["count"]
        cols = args.cols or SHEET_COLS_BY_PACK.get(pack) or (20 if count > 80 else 10)
        run(
            [
                sys.executable,
                "build_sheet.py",
                "--pack",
                pack,
                "--cell",
                str(args.cell),
                "--cols",
                str(cols),
            ]
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
