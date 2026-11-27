"""Extrait les posts d'une page de recherche Warosu sauvegardée. usage: python3 -I warosu.py <fichier>"""
import html, re, sys

b = open(sys.argv[1], encoding="utf8").read()
# shortcut: découpage par blockquote, suffisant pour relire ; limite: la structure HTML peut changer d'une page à l'autre
parts = re.split(r'(?=<table[^>]*>|<div id="p\d+")', b)
n = 0
for p in parts:
    q = re.findall(r"<blockquote>(.*?)</blockquote>", p, flags=re.S)
    if not q:
        continue
    pid = re.findall(r'id="p(\d+)"|/biz/post/(\d+)|/biz/thread/(\d+)', p)
    ts = re.findall(r'data-timestamp="(\d+)"|title="(\d{10,})"', p)
    dt = re.findall(r"(\w{3}\s+\w{3}\s+\d+\s+\d\d:\d\d:\d\d\s+\d{4})|(\d\d/\d\d/\d\d\(\w+\)\d\d:\d\d(?::\d\d)?)", p)
    ids = [x for t in pid[:3] for x in t if x]
    txt = re.sub(r"<[^>]+>", " ", html.unescape(q[0]))
    txt = re.sub(r"\s+", " ", txt).strip()
    n += 1
    print(ids[:2], ts[:1], dt[:1], txt[:500])
print("n", n)
