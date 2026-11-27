"""Première touche de DMAGA par rapport à S = 19:30:13 le 21/07/2024, par dépôt, depuis i60_touch.csv ; et jetons reçus par 9PrmF8 fin mars à mai 2024 (test $PEZI proposé par E). Sortie i61.txt."""
import csv,collections,sys,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i61.txt","w")
c=collections.defaultdict(collections.Counter)
for r in csv.DictReader(open(OUT+"i60_touch.csv")):
    d=c[r["depot"]];d["n"]+=1
    if r["touche"]=="1":
        d["touche"]+=1
        ft=r["first_touch"]
        if ft<"2024-07-21T19:30:13":d["avant Musk"]+=1
        elif ft<"2024-08-21":d["30 j après"]+=1
        elif ft<"2025-01-01":d["fin 2024"]+=1
        else:d["2025 et après"]+=1
for k,v in c.items():print(k,dict(v))
W="9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
n=0;t0=None;t1=None;seen=collections.Counter();ex={}
for t in iter_tx(W):
    n+=1;bt=t["blockTime"];t0=min(t0 or bt,bt);t1=max(t1 or bt,bt)
    if not(1711756800<=bt<1717200000):continue
    td,dec=tok_delta(t)
    for (o,m),v in td.items():
        if o==W and v>0 and not programs(t)-BASIC:
            seen[m]+=v/10**dec[m];ex[m]=(dt.datetime.fromtimestamp(bt,dt.timezone.utc).isoformat(),[x[0][:8] for x,y in td.items() if x[1]==m and y<0],t["transaction"]["signatures"][0][:18],signers(t)[0][:8])
print("9PrmF8 tx lues",n,dt.datetime.fromtimestamp(t0,dt.timezone.utc),dt.datetime.fromtimestamp(t1,dt.timezone.utc))
print("jetons reçus par transfert pur du 30/03 au 31/05/2024",len(seen))
for m,v in seen.most_common(30):print(" ",m,round(v,2),ex[m])
