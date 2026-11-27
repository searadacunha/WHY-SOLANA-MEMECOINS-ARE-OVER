"""pHash des images récupérées dans la Wayback contre l'avatar, V1, V2 et les images de @pmarca, plus planche. usage: python3.12 -I wbhash.py"""
import csv, glob, sys
from pathlib import Path
sys.path.insert(0, "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/pylib")
import imagehash
from PIL import Image, ImageDraw

W = Path(__file__).resolve().parent.parent
R = W.parent.parent.parent / "evidence/x_media"
refs = {"avatar": R / "profile_new_1815105297410666496.jpg", "V1": W / "evidence/x_media_new/1815054381823221968_GTBeVlkXsAAgbTW.jpg",
        "pmarca2007": R / "1814779160377602331_GS9WLZJbIAMcF-_.png", "pmarca0708": R / "1815004677160776126_GS_kcJJbMAIDyB8.png",
        "dmaga17_07": R / "1813683527575302497_GSt_gY7WUAAS6ue.jpg", "avatarV3": W / "evidence/x_media_new/1815062189763703119_GTBlcMpWkAABbvL.jpg",
        "V0": W / "evidence/x_media_new/1813310692243480937_GSosdsSWYAACOIC.jpg"}
H = {k: imagehash.phash(Image.open(p).convert("RGB")) for k, p in refs.items()}
files = sorted(glob.glob(str(W / "evidence/x_media_wb_new/*")))
rows = []
for p in files:
    im = Image.open(p).convert("RGB")
    h = imagehash.phash(im)
    rows.append({"file": Path(p).name, "w": im.width, "h": im.height, **{k: int(h - v) for k, v in H.items()}})
    print(Path(p).name[:15], im.size, {k: int(h - v) for k, v in H.items()})
with open(W / "derived/visual_wb.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
cols, s = 6, 170
sh = Image.new("RGB", (cols * s, ((len(files) + cols - 1) // cols) * (s + 13)), "white")
d = ImageDraw.Draw(sh)
for n, p in enumerate(files):
    im = Image.open(p).convert("RGB")
    im.thumbnail((s, s))
    x, y = (n % cols) * s, (n // cols) * (s + 13)
    sh.paste(im, (x, y + 13))
    d.text((x + 2, y), Path(p).name[:15], fill="black")
sh.save(W / "derived/sheet_wb_media.jpg", quality=80)
