"""Planche-contact des médias de work_E. usage: python3.12 -I sheet.py <sortie.jpg> <motif_id...>"""
import sys
from pathlib import Path
sys.path.insert(0, "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/pylib")
from PIL import Image, ImageDraw

W = Path(__file__).resolve().parent.parent
out, ids = sys.argv[1], sys.argv[2:]
files = [p for i in ids for p in sorted((W / "evidence/x_media_new").glob(i + "_*"))]
cols, s = 6, 200
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * s, rows * (s + 14)), "white")
d = ImageDraw.Draw(sheet)
for n, p in enumerate(files):
    im = Image.open(p).convert("RGB")
    im.thumbnail((s, s))
    x, y = (n % cols) * s, (n // cols) * (s + 14)
    sheet.paste(im, (x, y + 14))
    d.text((x + 2, y + 1), p.name.split("_")[0][-9:], fill="black")
sheet.save(W / out, quality=80)
print(len(files))
