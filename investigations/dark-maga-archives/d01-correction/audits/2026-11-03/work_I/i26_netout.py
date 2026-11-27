"""Virements purs sortants (BASIC seul) lus dans tout le net brut C et G, seuil 0,01 SOL ou 1 USD, ainsi que DMAGA transférés >= 1 000 jetons. Sortie audits_work/I/net_out.csv.gz."""
import gzip,json,os,csv,sys
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
W=R+"/audits_work/I/"
o=gzip.open(W+"net_out.csv.gz","wt");w=csv.writer(o);w.writerow("src dst asset amount bt sig".split())
seen=set();n=0;nf=0
for d in NETS:
    for f in sorted(os.listdir(d)):
        if f.startswith("._") or not f.endswith(".jsonl.gz") or f.startswith(("ctrl_deposits","absent_","probe_")): continue
        nf+=1
        with gzip.open(f"{d}/{f}","rt") as h:
            for l in h:
                t=json.loads(l)
                if not ok(t) or programs(t)-BASIC: continue
                sg=t["transaction"]["signatures"][0]
                if sg in seen: continue
                seen.add(sg)
                S=signers(t);sd=sol_delta(t);td,dec=tok_delta(t);fee=t["meta"]["fee"]
                for s in S:
                    v=-sd.get(s,0)-(fee if s==S[0] else 0)
                    if v>=1e7:
                        for k,x in sd.items():
                            if x>0 and k!=s:
                                w.writerow([s,k,"SOL",x/1e9,t["blockTime"],sg]);n+=1
                for (ow,m),x in td.items():
                    if x<0 and m in(USDC,USDT,DMAGA):
                        a=-x/10**dec[m]
                        if (m==DMAGA and a<1000) or (m!=DMAGA and a<1): continue
                        for (o2,m2),y in td.items():
                            if m2==m and y>0 and o2!=ow:
                                w.writerow([ow,o2,{USDC:"USDC",USDT:"USDT",DMAGA:"DMAGA"}[m],y/10**dec[m],t["blockTime"],sg]);n+=1
o.close();print("fichiers",nf,"lignes",n,"tx uniques pures",len(seen))
