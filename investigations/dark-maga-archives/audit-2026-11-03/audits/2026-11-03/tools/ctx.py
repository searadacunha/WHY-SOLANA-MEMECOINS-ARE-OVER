#!/usr/bin/env python3
"""Affiche le contexte d'une empreinte dans un fichier/objet git en masquant toute valeur UUID. usage: ctx.py <dépôt> <emp8> [...]"""
import re,subprocess,sys,hashlib
U=re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
repo,*fps=sys.argv[1:]; fps=set(fps)
chk=subprocess.run(["git","-C",repo,"cat-file","--batch-all-objects","--unordered","--batch-check=%(objectname) %(objecttype) %(objectsize)"],capture_output=True,text=True).stdout
done=set()
for l in chk.splitlines():
    s,t,z=l.split()
    if t!="blob" or int(z)>20<<20: continue
    d=subprocess.run(["git","-C",repo,"cat-file","blob",s],capture_output=True).stdout
    for m in U.finditer(d):
        f=hashlib.sha256(m.group()).hexdigest()[:8]
        if f in fps and f not in done:
            done.add(f)
            print(f, repr(U.sub(b"<UUID>",d[max(0,m.start()-90):m.end()+40]))[:260])
