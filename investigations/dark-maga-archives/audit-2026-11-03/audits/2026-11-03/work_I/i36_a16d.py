"""G8 : un bloc de chaque forme en comptabilité complète (tous comptes, SOL et WSOL), et valeur des jetons gardés au prix du bloc. Cherche les 2 tx dans le dossier de pages qui les contient. Sortie i36_a16d.txt."""
import gzip,json,os,sys,collections
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/";W=R+"/audits_work/I/"
sys.stdout=open(OUT+"i36_a16d.txt","w")
TX=[json.loads(l) for l in gzip.open(W+"a16_full.jsonl.gz","rt")]
by=collections.defaultdict(list)
for t in TX:by[t["slot"]].append(t)
O4="4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
# valeur des jetons gardés : prix du bloc = WSOL du pool sur la jambe 1 / jetons
AMM="5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
val=0;n=0;tot=0;want={}
for sl,L in by.items():
    a,b=sorted(L,key=lambda t:t["i"])
    if a["dm"].get(O4,0)<0: 
        want.setdefault("vente",[a["s"],b["s"]]);continue
    S=a["sg"][0];q=a["dm"].get(S,0)
    kept=a["dm"].get(O4,0)+b["dm"].get(O4,0)
    w=a["ws"].get(AMM,0) or sum(v for k,v in a["ws"].items() if v>0)
    if q>0 and w>0:
        val+=kept/q*w/1e9;tot+=kept/1e6;n+=1
    want.setdefault("achat",[a["s"],b["s"]])
print("jetons gardés, valeur au prix de la jambe d'achat : blocs",n,"jetons M",round(tot/1e6,3),"SOL",round(val,2))
need={s for v in want.values() for s in v};found={}
for base in ("raw/full_pool",):
    for root,ds,fs in os.walk(f"{R}/{base}"):
        for f in sorted(fs):
            if f.startswith("._") or not f.endswith(".gz") or len(found)==len(need):continue
            with gzip.open(os.path.join(root,f),"rt") as h:
                for l in h:
                    if not any(s in l for s in need):continue
                    x=json.loads(l);items=x if isinstance(x,list) else x.get("data") or [x]
                    for t in items:
                        if isinstance(t,dict) and "transaction" in t and t["transaction"]["signatures"][0] in need:found[t["transaction"]["signatures"][0]]=t
for k,v in want.items():
    print("==",k)
    tot=collections.Counter()
    for s in v:
        t=found.get(s)
        if not t:print("non trouvé",s);continue
        print(" ",s,"slot",t["slot"],"idx",t["transactionIndex"],"frais",t["meta"]["fee"],"signe",signers(t))
        sd=sol_delta(t);td,dec=tok_delta(t)
        print("   SOL",{a:round(b/1e9,6) for a,b in sd.items()})
        print("   jetons",{(o,m[:6]):round(x/10**dec[m],6) for (o,m),x in td.items()})
        print("   logs",[l for l in t["meta"]["logMessages"] if "Program log:" in l and "Instruction" not in l][:6])
        for a,b in sd.items():tot[("SOL",a)]+=b/1e9
        for (o,m),x in td.items():tot[(m[:6],o)]+=x/10**dec[m]
    print("  NET",{k:round(x,6) for k,x in tot.items() if abs(x)>1e-9})
