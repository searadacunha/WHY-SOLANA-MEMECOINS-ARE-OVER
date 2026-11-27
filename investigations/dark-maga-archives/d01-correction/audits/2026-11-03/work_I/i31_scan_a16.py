"""G8 : extrait du brut raw/full_pool et raw/full_venue toutes les tx qui portent le programme 3GMsedVP et touchent DMAGA. Filtre en flux sur la chaîne de caractères avant de parser. Sortie audits_work/I/a16_tx.csv.gz."""
import gzip,json,os,csv,sys,time
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
SVC="3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"
W=R+"/audits_work/I/"
o=gzip.open(W+"a16_tx.csv.gz","wt");w=csv.writer(o);w.writerow("slot idx bt sig signer nsign owner dmaga sol wsol usdc progs err".split())
seen=set();nf=0;nl=0;t0=time.time()
for base in ("raw/full_pool","raw/full_venue","raw/full_mint"):
    for root,ds,fs in os.walk(f"{R}/{base}"):
        for f in sorted(fs):
            if f.startswith("._") or not f.endswith(".gz"): continue
            nf+=1
            try:
                h=gzip.open(os.path.join(root,f),"rt")
                for l in h:
                    nl+=1
                    if SVC not in l: continue
                    x=json.loads(l)
                    items=x if isinstance(x,list) else x.get("data") or x.get("result",{}).get("data") if isinstance(x,dict) and ("data" in x or "result" in x) else [x]
                    for t in items:
                        if not isinstance(t,dict) or "transaction" not in t: continue
                        sg=t["transaction"]["signatures"][0]
                        if sg in seen: continue
                        ps=programs(t)
                        if SVC not in ps: continue
                        seen.add(sg)
                        td,dec=tok_delta(t);sd=sol_delta(t);S=signers(t)
                        owners={k[0] for k in td if k[1]==DMAGA}
                        for ow in owners:
                            w.writerow([t["slot"],t.get("transactionIndex"),t["blockTime"],sg,S[0] if S else "",len(S),ow,td.get((ow,DMAGA),0),sd.get(ow,0),td.get((ow,WSOL),0),td.get((ow,USDC),0),"|".join(sorted(p for p in ps if p not in BASIC)),t["meta"]["err"]])
                h.close()
            except EOFError:
                print("gz tronqué",f)
            if nf%200==0:
                print(nf,"fichiers",nl,"lignes",len(seen),"tx",round(time.time()-t0),"s",flush=True)
o.close();print("fini",nf,nl,len(seen),round(time.time()-t0))
