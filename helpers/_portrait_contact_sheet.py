"""QA: build a contact sheet of scientist portraits composited on the card
background, to judge framing/consistency. Optionally pass specific stems.

  python helpers/_portrait_contact_sheet.py            # all portraits
  python helpers/_portrait_contact_sheet.py NAME ...   # only these stems
"""
import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw

SRC = Path("images/scientists-photos")
CARD_BG = (238, 242, 247, 255)
CELL_W, CELL_H = 148, 176
PAD = 8
COLS = 10


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        pngs = [SRC / f"{s}.png" for s in args]
    else:
        pngs = sorted(SRC.glob("*.png"))
    cols = min(COLS, len(pngs)) or 1
    rows = math.ceil(len(pngs) / cols)
    sw = cols * (CELL_W + PAD) + PAD
    sh = rows * (CELL_H + PAD) + PAD
    sheet = Image.new("RGB", (sw, sh), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(pngs):
        r, c = divmod(i, cols)
        x, y = PAD + c * (CELL_W + PAD), PAD + r * (CELL_H + PAD)
        cell = Image.new("RGBA", (CELL_W, CELL_H), CARD_BG)
        im = Image.open(p).convert("RGBA").resize((CELL_W, CELL_H), Image.LANCZOS)
        cell.alpha_composite(im)
        sheet.paste(cell.convert("RGB"), (x, y))
        draw.rectangle([x, y, x + CELL_W - 1, y + CELL_H - 1], outline=(200, 205, 212))
    out = Path(os.path.expandvars(r"%TEMP%")) / "daab_portrait_contact_sheet.png"
    sheet.save(out)
    print("wrote", out, sheet.size, "portraits:", len(pngs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
