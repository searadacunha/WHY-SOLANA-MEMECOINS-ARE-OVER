"""Constat 9 : réponses antérieures de @kikisknees portant le visuel ? Index de tous les médias des status lus (wb_status_recovered + x_wayback), images réellement présentes, pHash à V1 et à l'avatar, textes qui nomment Elon ou Musk avec un média avant 12:50:45 le 21/07. Puis alignement V1/avatar pour « même composition ». Sortie i41_kiki900.txt, i41_keys.csv."""
import json,glob,os,base64,sys,csv,datetime as dt,re
import numpy as np
from PIL import Image
OUT="audits/2026-11-03/work_I/";E="audits/2026-11-03/work_E/"
sys.stdout=open(OUT+"i41_kiki900.txt","w")
snow=lambda i:(int(i)>>22)+1288834974657
iso=lambda ms:dt.datetime.fromtimestamp(ms/1000,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
LIM=snow("1815006501896872388")
def dct(p):
    im=Image.open(p).convert("L").resize((32,32),Image.LANCZOS);a=np.asarray(im,dtype=float);N=32
    C=np.array([[np.cos(np.pi*(2*x+1)*u/(2*N)) for x in range(N)] for u in range(N)]);d=C@a@C.T;t=d[:8,:8];return (t>np.median(t)).flatten()
AV=dct("evidence/x_media/profile_new_1815105297410666496.jpg");V1=dct(E+"evidence/x_media_wb_new/GTAytGIW4AE9_93_20240723023716.png")
have={}
for p in glob.glob(E+"evidence/x_media_wb_new/*"):
    k=os.path.basename(p).split("_2024")[0];have[k]=p
rows=[];ids=set()
with open(E+"wb_status_recovered.jsonl") as h:
    for l in h:
        r=json.loads(l)
        if r.get("username")!="kikisknees" and r.get("account_in_url")!="kikisknees": continue
        pid=r["id"]
        if pid in ids: continue
        ids.add(pid)
        for m in r.get("media") or []:
            k=(m.get("url") or "").split("/")[-1].split(".")[0]
            rows.append((snow(pid),pid,k,m.get("width"),m.get("height"),m.get("type"),(r.get("text") or "")[:110],r.get("reply_to_user"),(r.get("refs") or [{}])[0].get("type") if r.get("refs") else ""))
# status dans evidence/x_wayback
for p in glob.glob("evidence/x_wayback/*.raw"):
    pid=os.path.basename(p)[:-4]
    if pid in ids: continue
    try: j=json.load(open(p))
    except Exception: continue
    d=j.get("data",{})
    if d.get("author_id")!="1474749663039401987": continue
    ids.add(pid)
    for m in j.get("includes",{}).get("media",[]) or []:
        k=(m.get("url") or "").split("/")[-1].split(".")[0]
        rows.append((snow(pid),pid,k,m.get("width"),m.get("height"),m.get("type"),(d.get("text") or "")[:110],d.get("in_reply_to_user_id"),(d.get("referenced_tweets") or [{}])[0].get("type")))
rows.sort()
w=csv.writer(open(OUT+"i41_keys.csv","w"));w.writerow("utc pid key w h type ref reply_to text present d_avatar d_V1".split())
print("status @kikisknees lus",len(ids),"médias",len(rows))
pre=[r for r in rows if r[0]<LIM and r[8]!="retweeted"]
print("médias de posts propres avant 12:50:45 le 21/07",len(pre),"dont 900x900",sum(1 for r in pre if r[3]==900 and r[4]==900),"images présentes",sum(1 for r in pre if r[2] in have))
for r in rows:
    d=(int((dct(have[r[2]])!=AV).sum()),int((dct(have[r[2]])!=V1).sum())) if r[2] in have else ("","")
    w.writerow([iso(r[0]),r[1],r[2],r[3],r[4],r[5],r[8],r[7],r[6].replace("\n"," "),int(r[2] in have),d[0],d[1]])
print("\nimages présentes, chronologie, distance à l'avatar et à V1")
for r in rows:
    if r[2] in have:
        print(" ",iso(r[0]),r[1],r[2],r[3],r[4],r[8],"av",int((dct(have[r[2]])!=AV).sum()),"V1",int((dct(have[r[2]])!=V1).sum()),repr(r[6][:70]))
print("\nposts avant 12:50:45 avec média, qui nomment Elon ou Musk, ou répondent à 44196397")
for r in pre:
    if re.search(r"elon|musk",r[6],re.I) or str(r[7]) in("44196397","elonmusk"):
        print(" ",iso(r[0]),r[1],r[2],r[3],r[4],"présent" if r[2] in have else "non lu",repr(r[6][:90]))
print("\nderniers médias 900x900 non lus avant 12:50:45")
L=[r for r in pre if r[3]==900 and r[4]==900 and r[2] not in have]
print("non lus",len(L))
for r in L[-25:]: print(" ",iso(r[0]),r[1],r[2],repr(r[6][:70]))
json.dump([r[2] for r in L],open("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/keys900.json","w"))
# même composition : alignement à l'œil par mesure
def G(p,box=None):
    im=Image.open(p).convert("RGB").resize((400,400),Image.LANCZOS);a=np.asarray(im,dtype=float)
    return a
av=G("evidence/x_media/profile_new_1815105297410666496.jpg");mask=np.zeros((400,400),bool);mask[20:400,110:300]=True
def edges(a):
    g=a.mean(axis=2);gx=np.abs(np.diff(g,axis=1))[:-1,:];gy=np.abs(np.diff(g,axis=0))[:,:-1];return gx+gy
ea=edges(av)
for name,p in [("V1 kiki",E+"evidence/x_media_wb_new/GTAytGIW4AE9_93_20240723023716.png"),("V3 kiki",E+"evidence/x_media_wb_new/GTCEEQ2WoAAm65s_20240723081618.png"),("V2 Franco",E+"evidence/x_media_new/1815054374982324401_GTBeVcVXAAAVa3o.jpg"),("V0 Franco",E+"evidence/x_media_new/1813310692243480937_GSosdsSWYAACOIC.jpg"),("Trump kiki",E+"evidence/x_media_wb_new/GTBeEjGXgAAbn4S_20240722211626.jpg"),("Winig",  "evidence/x_media/1815054750775173447_GTBerExWkAEFQuT.jpg")]:
    e=edges(G(p));best=(-1,0,0)
    for dx in range(-20,21,1):
        for dy in range(-20,21,1):
            a=ea[40:360,120:280];b=e[40+dy:360+dy,120+dx:280+dx]
            c=np.corrcoef(a.ravel(),b.ravel())[0,1]
            if c>best[0]:best=(c,dx,dy)
    print(f"corrélation des contours, zone visage et armure, meilleur décalage : {name}: r={best[0]:.3f} décalage {best[1]},{best[2]}")
