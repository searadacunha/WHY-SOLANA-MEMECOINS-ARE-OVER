"""Derniers contrôles : dépôts de la salve contre exécutions DCA, 5NmoD59D, heures de média FrancoAppr/EeOo, premier post, compteurs à 02:45:55, concentration du pont sur 4 wallets, séries Coinbase hors 507 s. Sortie i73.txt."""
import csv,json,sys,collections,base64,datetime as dt,gzip
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/";sys.stdout=open(OUT+"i73.txt","w")
iso=lambda ms:dt.datetime.fromtimestamp(ms/1000,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
def key_ms(k):
    return snow(int.from_bytes(base64.urlsafe_b64decode(k[:11]+"="),"big"))
# 1
fills=collections.defaultdict(float)
for r in csv.DictReader(open(OUT+"i07_fills.csv")):
    if r["out_mint"]==USDC and "2024-07-21T19"<=r["utc"]<"2024-07-22T05:30":fills[r["wallet"]]+=float(r["out_amt"])
for r in csv.DictReader(open(OUT+"i01_moves.csv")):
    if r["depot"]=="Caw4" and r["side"]=="in" and r["asset"]=="USDC" and "2024-07-22T05:2"<=r["utc"]<"2024-07-22T05:3":
        print("salve",r["utc"],r["cp"],r["amount"],"exécutions USDC reçues avant",round(fills[r["cp"]],6),"écart",round(float(r["amount"])-fills[r["cp"]],6))
# 2
for r in csv.DictReader(open(OUT+"i01_moves.csv")):
    if r["cp"].startswith("5NmoD59D") and r["depot"]=="Caw4":print("5NmoD59D",r["utc"],r["amount"],r["signer"][:12],r["nprog"],r["sig"][:18])
for t in iter_tx("Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME"):
    td,dec=tok_delta(t)
    if ("5NmoD59DK5BvkCGsKVRq2xs9VN5s33TS4sr2sRazJsqg",USDC) in td:
        print(" programmes",sorted(programs(t)-BASIC),"signataires",[s[:10] for s in signers(t)]);break
# 3
for k,n in (("GTBeVcVXAAAVa3o","Franco"),("GTBeVlkXsAAgbTW","EeOo")):print(n,k,iso(key_ms(k)))
for i in ("1812312706826854843","1812317575411351639","1815105297410666496","1812303793645666304"):print(i,iso(snow(i)))
for p in ("evidence/x_wayback/1812317575411351639.raw",):
    j=json.load(open(p));print(p,j["data"]["created_at"],repr(j["data"]["text"])[:90])
    for u in j["includes"].get("users",[]):
        if u["username"]=="DarkMagaCoin":print(u["username"],u["created_at"],u["public_metrics"])
    for t in j["includes"].get("tweets",[]):print(" cite",t["id"],t["created_at"],repr(t["text"])[:90])
# 4
O=list(csv.DictReader(open(OUT+"i14_orders.csv")))
c=collections.Counter()
for r in O:c[r["maker"]]+=(int(r["give_amount"])+int(r["fee_pct"]))/1e6
tot=sum(c.values());top=c.most_common(4);print("4 makers",[(k[:8],round(v,2)) for k,v in top],"part",round(100*sum(v for _,v in top)/tot,2))
print("makers",len(c))
