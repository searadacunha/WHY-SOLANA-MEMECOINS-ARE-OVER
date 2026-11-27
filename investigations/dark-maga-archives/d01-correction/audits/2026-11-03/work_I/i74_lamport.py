"""Candidat HFRc5Nmw : montants ronds + 1 lamport venus de 2 grappes en 192 s. Fréquence de ce motif dans tout raw/flows, sonde 10 crédits. Sortie i74.txt."""
import csv,gzip,json,sys,collections,time,os,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
from dmaga.helius import Helius
OUT="audits/2026-11-03/work_I/";sys.stdout=open(OUT+"i74.txt","w")
P1={list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))}
g33=set(json.load(open("data/prevent_groups.json"))[0]["members"])
tot=0;mot=0;src=collections.Counter();dstc=collections.defaultdict(set)
for r in csv.DictReader(gzip.open(R+"/audits_work/I/flows_out.csv.gz","rt")):
    if r["asset"]!="SOL":continue
    tot+=1;l=round(float(r["amount"])*1e9)
    if l%1000000==1:
        mot+=1;src[r["src"]]+=1;dstc[r["dst"]].add(r["src"])
print("lignes SOL",tot,"motif +1 lamport",mot,"wallets",len(src))
print("top expéditeurs",[(k[:8],v,"P1" if k in P1 else "33" if k in g33 else "") for k,v in src.most_common(10)])
print("P1 avec le motif",sum(1 for k in src if k in P1),"33 avec le motif",sum(1 for k in src if k in g33))
print("destinations à >=2 expéditeurs avec ce motif",[(k[:10],len(v),sorted(x[:6] for x in v)[:6]) for k,v in sorted(dstc.items(),key=lambda kv:-len(kv[1]))[:8] if len(v)>=2])
h=Helius(rps=3);A="HFRc5NmwpP83MambL2i7M7hhTe24qQxKwVtp4Yn6naVG"
r=h.txs_page(A,limit=100,sort="asc")
with gzip.open(R+f"/audits_work/I/net/{A}.jsonl.gz","wt") as f:
    for t in r.get("data") or []:f.write(json.dumps(t)+"\n")
open(OUT+"credits.csv","a").write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},gtfa_full,HFRc5Nmw,10\n")
L=r.get("data") or [];print("HFRc5Nmw tx",len(L),"suite",bool(r.get("paginationToken")))
for t in L[:16]:
    sd=sol_delta(t);td,dec=tok_delta(t);S=signers(t)
    print(" ",dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),"signe",S[0][:8],"SOL",round(sd.get(A,0)/1e9,4),"jetons",{m[:6]:round(v/10**dec[m],2) for (o,m),v in td.items() if o==A},"programmes",sorted(x[:8] for x in programs(t)-BASIC)[:3],"contre",[k[:8] for k,v in sd.items() if k!=A and v!=0][:3])
print("signées",sum(1 for t in L if A in signers(t)))
print(dict(h.stats))
