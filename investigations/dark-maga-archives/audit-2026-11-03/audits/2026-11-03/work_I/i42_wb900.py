"""Constat 9 : tente de lire dans la Wayback les images 900x900 de @kikisknees juste avant 12:50:45 le 21/07, les plus proches d'abord, pour tester « V1 plus ancienne connue ». Arrêt après 6 échecs consécutifs ou 45 clés. Images dans audits_work/I/wb_media. Sortie i42_wb900.txt."""
import json,urllib.request,time,os,sys,hashlib,io
import numpy as np
from PIL import Image
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/";M=W+"wb_media/";os.makedirs(M,exist_ok=True)
OUT="audits/2026-11-03/work_I/";E="audits/2026-11-03/work_E/"
out=open(OUT+"i42_wb900.txt","w",buffering=1)
def dct(f):
    im=Image.open(f).convert("L").resize((32,32),Image.LANCZOS);a=np.asarray(im,dtype=float);N=32
    C=np.array([[np.cos(np.pi*(2*x+1)*u/(2*N)) for x in range(N)] for u in range(N)]);d=C@a@C.T;t=d[:8,:8];return (t>np.median(t)).flatten()
AV=dct("evidence/x_media/profile_new_1815105297410666496.jpg");V1=dct(E+"evidence/x_media_wb_new/GTAytGIW4AE9_93_20240723023716.png")
def get(u,to=45):
    r=urllib.request.Request(u,headers={"user-agent":"Mozilla/5.0"})
    with urllib.request.urlopen(r,timeout=to) as h: return h.read()
keys=json.load(open(W+"keys900.json"))[::-1][:45]
fails=0;ok=0;none=0
for k in keys:
    try:
        c=json.loads(get(f"https://web.archive.org/cdx/search/cdx?url=pbs.twimg.com/media/{k}*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&limit=4"))
        fails=0
    except Exception as e:
        fails+=1;print(k,"CDX échec",type(e).__name__,str(e)[:60],file=out)
        if fails>=6: print("arrêt : 6 échecs consécutifs",file=out);break
        time.sleep(8);continue
    if len(c)<2: none+=1;print(k,"aucune capture",file=out);time.sleep(1.5);continue
    ts,orig,_,mime=c[1]
    try:
        b=get(f"https://web.archive.org/web/{ts}im_/{orig}")
        p=f"{M}{k}_{ts}.img";open(p,"wb").write(b)
        im=Image.open(io.BytesIO(b));d=dct(io.BytesIO(b))
        print(k,ts,im.size,hashlib.sha256(b).hexdigest(),"av",int((d!=AV).sum()),"V1",int((d!=V1).sum()),file=out);ok+=1
    except Exception as e:
        print(k,"image échec",type(e).__name__,str(e)[:60],file=out)
    time.sleep(2)
print("lues",ok,"sans capture",none,file=out)
