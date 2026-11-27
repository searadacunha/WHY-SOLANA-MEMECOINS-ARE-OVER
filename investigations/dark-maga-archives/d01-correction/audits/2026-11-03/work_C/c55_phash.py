#!/usr/bin/env python3
"""pHash DCT recalcule (mon code) entre l'image de Winig et l'avatar de Musk, plus temoins ; et lecture de visual_matches ; recherche de la plus ancienne distance 0. Sortie c55.out"""
import csv, json
import numpy as np
from PIL import Image
R='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
def dct2(a):
    N=a.shape[0]
    C=np.array([[np.cos(np.pi*(2*x+1)*u/(2*N)) for x in range(N)] for u in range(N)])
    return C@a@C.T
def ph(p):
    im=Image.open(p).convert('L').resize((32,32),Image.LANCZOS)
    d=dct2(np.asarray(im,dtype=float))[:8,:8]
    med=np.median(d.flatten()[1:])
    return (d>med).flatten()
a=ph(R+'evidence/x_media/1815054750775173447_GTBerExWkAEFQuT.jpg')
b=ph(R+'evidence/x_media/profile_new_1815105297410666496.jpg')
c=ph(R+'evidence/x_media/profile_old_1780044485541699584.jpg')
d=ph(R+'evidence/x_media/profile_after_1815749056821346304.jpg')
print('Winig vs avatar laser',int((a!=b).sum()),'Winig vs ancien',int((a!=c).sum()),'Winig vs apres',int((a!=d).sum()),'laser vs ancien',int((b!=c).sum()))
rows=list(csv.DictReader(open(R+'data/visual_matches.csv')))
rows.sort(key=lambda r:r['created_utc'])
z=[r for r in rows if r['phash_dist'] not in('',None) and float(r['phash_dist'])<=4]
print('n',len(rows),'distance<=4',len(z))
for r in z[:10]: print(r['created_utc'],r['author'],r['phash_dist'],r['dhash_dist'],r['post_id'],(r['text'] or '')[:60].replace('\n',' '))
print('avant Winig, toute image <=10',[(r['created_utc'],r['author'],r['phash_dist']) for r in rows if r['created_utc']<'2024-07-21T16:02:29Z' and float(r['phash_dist'] or 99)<=10][:8])
rec=[json.loads(l) for l in open(R+'evidence/x_wayback/recovered.jsonl')]
for r in rec:
    t=r.get('text') or ''
    if r.get('account_in_url')=='kikisknees' and ('2024-07-21T12:' in r.get('snowflake','') or '2024-07-21T18:' in r.get('snowflake','')):
        print('kiki',r['snowflake'],t[:90].replace('\n',' '),[m for m in str(r.get('media'))[:60].split()][:1])
