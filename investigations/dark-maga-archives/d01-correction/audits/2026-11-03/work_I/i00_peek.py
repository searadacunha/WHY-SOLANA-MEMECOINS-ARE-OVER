"""Forme brute d'un fichier net (C et G) et de raw/flows, sans rien agréger."""
import gzip, json, sys, os
R="/Volumes/VERBATIM HD/Dark-MAGA-Investigation"
def shape(o,d=0,maxd=3):
    if isinstance(o,dict):
        return {k:(shape(v,d+1,maxd) if d<maxd else type(v).__name__) for k,v in list(o.items())[:30]}
    if isinstance(o,list):
        return [len(o), shape(o[0],d+1,maxd) if o else None]
    return (str(o)[:60])
for f in ["audits_work/C/net/9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL.jsonl.gz","audits_work/G/net/Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME.jsonl.gz"]:
    p=os.path.join(R,f)
    print("==",f)
    with gzip.open(p,'rt') as h:
        n=0
        for l in h:
            n+=1
            if n==1:
                o=json.loads(l); print(json.dumps(shape(o),ensure_ascii=False)[:3500])
    print("lignes",n)
    print(open(p.replace('.jsonl.gz','.cursor.json')).read()[:200])
d=os.path.join(R,"raw/flows")
ws=[x for x in sorted(os.listdir(d)) if not x.startswith('._')][:1]
for w in ws:
    fs=[x for x in sorted(os.listdir(os.path.join(d,w))) if not x.startswith('._')]
    print("==flows",w,fs[:10])
    for x in fs[:1]:
        with gzip.open(os.path.join(d,w,x),'rt') as h:
            l=h.readline(); o=json.loads(l); print(json.dumps(shape(o),ensure_ascii=False)[:3000])
