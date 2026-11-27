"""7Gw3gL8m : que lit-on dans le net brut ? Signe-t-il, balaye-t-il, quels programmes, quels flux ? Et 9cfRU5RK vu depuis raw/flows. Sortie i28_7gw.txt."""
import sys,collections,datetime as dt,gzip,json
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i28_7gw.txt","w")
A="7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx"
print(net_paths(A))
n=0;sig=0;P=collections.Counter();I=collections.Counter();O=collections.Counter();times=[]
for t in iter_tx(A):
    n+=1;times.append(t["blockTime"])
    S=signers(t)
    if A in S:
        sig+=1
        for p in programs(t):P[p]+=1
    sd=sol_delta(t).get(A,0)
    k=[x for x,v in sol_delta(t).items() if (v<0)==(sd>0) and x!=A]
    if programs(t)<=BASIC:
        if sd>0:I[(k[0] if k else "?")]+=sd/1e9
        if sd<0:O[(k[0] if k else "?")]+=-sd/1e9
print("tx",n,"signées",sig,"de",dt.datetime.fromtimestamp(min(times),dt.timezone.utc),"à",dt.datetime.fromtimestamp(max(times),dt.timezone.utc))
print("programmes signés",P.most_common(12))
print("entrées pures",[(a[:10],round(v,3)) for a,v in I.most_common(12)])
print("sorties pures",[(a[:10],round(v,3)) for a,v in O.most_common(12)])
print(open(R+"/audits_work/G/net/"+A+".cursor.json").read())
W="9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw"
print("== 9cfRU5RK")
for f in ("first_in","in_before","sol_out_after","usdc_out_after","dmaga_all"):
    o=json.load(gzip.open(f"{R}/raw/flows/{W}/{f}.json.gz","rt"))
    rows=o["rows"];print(f,"lignes",len(rows),"tronqué",o.get("truncated"),o.get("cfg",{}).get("filters"))
    if f in("first_in","in_before"):
        c=collections.Counter()
        for r in rows:c[r["fromUserAccount"]]+=int(r["amount"])/1e9
        print("  sources",[(a[:10],round(v,2)) for a,v in c.most_common(10)]);
        if rows: print("  premier",rows[0]["fromUserAccount"],int(rows[0]["amount"])/1e9,dt.datetime.fromtimestamp(rows[0]["blockTime"],dt.timezone.utc))
    if "out" in f:
        c=collections.Counter()
        for r in rows:c[r["toUserAccount"]]+=int(r["amount"])/(1e9 if f.startswith("sol") else 1e6)
        print("  dest",[(a[:10],round(v,2)) for a,v in c.most_common(12)])
