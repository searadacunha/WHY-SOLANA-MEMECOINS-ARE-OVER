"""9PrmF8 : première touche DMAGA, tous jetons reçus sans SOL sortant du 30/03 au 31/05/2024, quel que soit le programme. Sortie i62.txt."""
import sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i62.txt","w")
W="9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
L=sorted(iter_tx(W),key=lambda t:(t["slot"],t["transactionIndex"]))
print("tx",len(L))
f=None;c=collections.Counter();ex={}
for t in L:
    td,dec=tok_delta(t);sd=sol_delta(t).get(W,0)
    if (W,DMAGA) in td and f is None:
        f=t;print("première touche DMAGA",dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc),td[(W,DMAGA)]/1e6,sd/1e9,t["transaction"]["signatures"][0])
    if 1711756800<=t["blockTime"]<1717200000:
        for (o,m),v in td.items():
            if o==W and v>0 and sd>-5_000_000:
                c[m]+=v/10**dec[m];ex[m]=(dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc).strftime("%Y-%m-%d"),signers(t)[0][:8],sorted(x[:8] for x in programs(t)-BASIC)[:2])
print("jetons reçus sans dépense de SOL, 30/03 au 31/05/2024 :",len(c))
for m,v in c.most_common(25):print(" ",m,round(v,2),ex[m])
