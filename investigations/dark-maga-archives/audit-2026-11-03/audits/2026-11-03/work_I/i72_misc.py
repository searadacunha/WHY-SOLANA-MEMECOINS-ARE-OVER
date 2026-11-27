"""Vérifications courtes : séance du 26/01/2025, montant exact de 59L2oxym dans les témoins, signatures complètes de la jonction 7Gw3gL8m, retour de valeur G7, cours DMAGA du 26/01/2025. Sortie i72.txt."""
import csv,gzip,json,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i72.txt","w")
rows=[r for r in csv.DictReader(open(OUT+"i01_moves.csv")) if r["side"]=="in" and r["utc"].startswith("2025-01-26")]
print("26/01/2025 :",len(rows))
tot=collections.Counter()
for r in sorted(rows,key=lambda r:r["utc"]):
    if float(r["amount"])>=(0.001 if r["asset"]=="SOL" else 0.1):
        print(" ",r["utc"],r["depot"],r["asset"],round(float(r["amount"]),4),r["cp"]);tot[(r["depot"],r["asset"])]+=float(r["amount"])
print(dict(tot))
gas="59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h";c=collections.Counter();n=0
with gzip.open(R+"/audits_work/C/net/ctrl_deposits.jsonl.gz","rt") as h:
    for l in h:
        if gas not in l:continue
        j=json.loads(l);t=j["tx"];sd=sol_delta(t)
        if sd.get(j["x"],0)>0 and sd.get(gas,0)<0:
            c[sd[j["x"]]]+=1;n+=1
print("59L2oxym vers témoins : versements",n,"montants",c.most_common(10))
A=[]
for f in ("audits_work/I/flows_out.csv.gz","audits_work/I/net_out.csv.gz"):
    for r in csv.DictReader(gzip.open(R+"/"+f,"rt")):
        if r["dst"]=="7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx" and r["src"] in("EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy","DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT","6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM") or (r["dst"]=="7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx" and r["src"].startswith("9cfRU5RK") and float(r["amount"])==400):
            A.append((r["bt"],r["src"],r["asset"],r["amount"],r["sig"]))
for x in sorted(set(A)):print(dt.datetime.fromtimestamp(int(x[0]),dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),*x[1:])
# retour : 7Gw3gL8m -> EGtyQEgM 1 SOL
for l in gzip.open(R+"/audits_work/I/net/7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx.aout.jsonl.gz","rt"):
    t=json.loads(l);sd=sol_delta(t)
    if "EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy" in sd and sd["EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy"]>0:print("retour",t["transaction"]["signatures"][0],dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc),sd)
# G7 : retour de valeur des receveurs vers ERMtiLod et GoPCTrS3, tous actifs, toute date, net_out
pairs={("HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6","ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH"),("HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP","GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC")}
for f in ("audits_work/I/flows_out.csv.gz","audits_work/I/net_out.csv.gz"):
    for r in csv.DictReader(gzip.open(R+"/"+f,"rt")):
        if (r["src"],r["dst"]) in pairs:print("retour G7",f[-20:],r)
print("fin")
