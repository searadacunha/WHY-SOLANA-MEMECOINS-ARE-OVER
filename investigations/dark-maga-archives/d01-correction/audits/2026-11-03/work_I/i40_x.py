"""Constat 9 : contrôle des posts et images à partir des fichiers sauvegardés. Snowflake calculé ici. Clé média du post contre nom de fichier de l'image, sha256, pHash propre (DCT maison) et imagehash, dimensions. Sortie i40_x.txt."""
import json,hashlib,base64,struct,datetime as dt,sys,os,glob,re
import numpy as np
from PIL import Image
import imagehash
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i40_x.txt","w")
E="audits/2026-11-03/work_E/evidence/"
iso=lambda ms:dt.datetime.fromtimestamp(ms/1000,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
snow=lambda i:(int(i)>>22)+1288834974657
def key_ms(k):
    b=base64.urlsafe_b64decode(k[:11]+"=")
    return snow(int.from_bytes(b[:8],"big"))
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
def dct_phash(p):
    im=Image.open(p).convert("L").resize((32,32),Image.LANCZOS);a=np.asarray(im,dtype=float)
    N=32;C=np.array([[np.cos(np.pi*(2*x+1)*u/(2*N)) for x in range(N)] for u in range(N)])
    d=C@a@C.T;t=d[:8,:8];b=t>np.median(t);return b.flatten()
def ham(a,b): return int((a!=b).sum())
AV="evidence/x_media/profile_new_1815105297410666496.jpg"
WIN="evidence/x_media/1815054750775173447_GTBerExWkAEFQuT.jpg"
imgs={"avatar":AV,"Winig16:02":WIN,
"V1_kiki12:50":E+"x_media_wb_new/GTAytGIW4AE9_93_20240723023716.png",
"V2_Franco16:00:59":E+"x_media_new/1815054374982324401_GTBeVcVXAAAVa3o.jpg",
"V1_EeOo":E+"x_media_new/1815054381823221968_GTBeVlkXsAAgbTW.jpg",
"V1_GB15:58":E+"x_media_new/1815053713330876681_GTBdu7vXgAARcaz.jpg",
"V3_GB16:32":E+"x_media_new/1815062189763703119_GTBlcMpWkAABbvL.jpg",
"V3_kiki18:46":E+"x_media_wb_new/GTCEEQ2WoAAm65s_20240723081618.png",
"V0_Franco16/07":E+"x_media_new/1813310692243480937_GSosdsSWYAACOIC.jpg",
"V0_kiki18/07":E+"x_media_wb_new/GSzYuoTXgAA63zz_20240718222220.jpg",
"V0_kiki21/07":E+"x_media_wb_new/GS-D11oXEAAfsvX_20240722201641.jpg",
"Trump_kiki16:00:08":E+"x_media_wb_new/GTBeEjGXgAAbn4S_20240722211626.jpg",
"Trump_kiki20:07":E+"x_media_wb_new/GTCWqbzXUAAYsUP_20240723080042.jpg",
"Franco18:31":E+"x_media_new/1815092319244128645_GTCA2FyXcAAH6aD.jpg",
"Murray18:40":E+"x_media_new/1815094431152029711_GTCCxFyWMAA4Cy1.jpg",
"DMC_V1_16:12":E+"x_media_new/1815057307836842034_GTBg8wsXoAAouzI.png"}
print("== images")
H={}
for k,p in imgs.items():
    if not os.path.exists(p): print(k,"ABSENT",p);continue
    im=Image.open(p);H[k]=(dct_phash(p),imagehash.phash(im.convert("RGB")),imagehash.dhash(im.convert("RGB")))
    print(f"{k:22s} {im.size} {os.path.getsize(p)} sha256 {sha(p)}")
print("== distances (DCT maison / imagehash phash / dhash) à l'avatar")
for k in H: print(f"  {k:22s} {ham(H[k][0],H['avatar'][0]):3d} {H[k][1]-H['avatar'][1]:3d} {H[k][2]-H['avatar'][2]:3d}")
print("== distances à V1_kiki")
for k in H: print(f"  {k:22s} {ham(H[k][0],H['V1_kiki12:50'][0]):3d} {H[k][1]-H['V1_kiki12:50'][1]:3d}")
print("== distances à V0_Franco")
for k in H: print(f"  {k:22s} {ham(H[k][0],H['V0_Franco16/07'][0]):3d} {H[k][1]-H['V0_Franco16/07'][1]:3d}")
# posts
print("\n== posts")
def wb(pid):
    for base in ("evidence/x_wayback/",E+"wb_status/"):
        p=f"{base}{pid}.raw"
        if os.path.exists(p): return p
def show(pid):
    p=wb(pid)
    fx=f"{E}x_raw_new/{pid}.fx.json"
    print("--",pid,"snowflake",iso(snow(pid)))
    if p:
        raw=open(p,"rb").read();print("  fichier",p,"sha256",sha(p),"octets",len(raw))
        try:
            j=json.loads(raw)
        except Exception as e:
            print("  non JSON",raw[:200]);return
        d=j.get("data",{});inc=j.get("includes",{})
        print("  created_at",d.get("created_at"),"author_id",d.get("author_id"),"user",[u["username"] for u in inc.get("users",[]) if u["id"]==d.get("author_id")])
        print("  text",repr(d.get("text")))
        print("  media_keys",d.get("attachments",{}).get("media_keys"),"refs",d.get("referenced_tweets"),"in_reply_to_user",d.get("in_reply_to_user_id"))
        for m in inc.get("media",[]):
            k=m.get("url","").split("/")[-1].split(".")[0]
            print("  media",m.get("media_key"),m.get("url"),m.get("width"),m.get("height"),"clé->heure",iso(key_ms(k)) if k else "","id->heure",iso(snow(m["media_key"].split("_")[1])))
    if os.path.exists(fx):
        j=json.load(open(fx));t=j.get("tweet",j)
        print("  fx",fx,"sha256",sha(fx),"auteur",t.get("author",{}).get("screen_name"),"created",t.get("created_at"),"replying_to",t.get("replying_to"),"text",repr(t.get("text"))[:220])
        for m in (t.get("media",{}) or {}).get("all",[]) or []:
            print("  fx media",m.get("url"),m.get("width"),m.get("height"))
for pid in ["1815006501896872388","1815054374982324401","1815054158367432804","1814063148917256375","1815116385414209876","1813683527575302497","1814719737378607482","1813310692243480937","1815053713330876681","1815054381823221968"]:
    show(pid)
print("\n== sha256 Trump")
for pid,pat in (("1813683527575302497","*"),("1814719737378607482","*")):
    for p in glob.glob(f"evidence/x_media/{pid}_*")+glob.glob(f"{E}x_media_new/{pid}_*"):
        print(p,sha(p))
