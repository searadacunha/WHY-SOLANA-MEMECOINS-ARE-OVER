"""G8 : réextraction des 3 826 tx avec tous les propriétaires, DMAGA et WSOL, SOL du signataire et du trésor, pourboire Jito éventuel. Sortie audits_work/I/a16_full.jsonl.gz."""
import gzip,json,os,sys,time
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
SVC="3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk";O4="4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
TIP={"96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5","HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe","Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY","ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49","DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh","ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt","DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL","3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT"}
o=gzip.open(R+"/audits_work/I/a16_full.jsonl.gz","wt");seen=set();t0=time.time()
for base in ("raw/full_pool","raw/full_venue","raw/full_mint"):
    for root,ds,fs in os.walk(f"{R}/{base}"):
        for f in sorted(fs):
            if f.startswith("._") or not f.endswith(".gz"): continue
            try:
                with gzip.open(os.path.join(root,f),"rt") as h:
                    for l in h:
                        if SVC not in l: continue
                        x=json.loads(l)
                        items=x if isinstance(x,list) else x.get("data") or x.get("result",{}).get("data") if isinstance(x,dict) and ("data" in x or "result" in x) else [x]
                        for t in items:
                            if not isinstance(t,dict) or "transaction" not in t: continue
                            sg=t["transaction"]["signatures"][0]
                            if sg in seen or SVC not in programs(t): continue
                            seen.add(sg)
                            td,dec=tok_delta(t);sd=sol_delta(t);S=signers(t)
                            dm={k[0]:v for k,v in td.items() if k[1]==DMAGA};ws={k[0]:v for k,v in td.items() if k[1]==WSOL}
                            tip=sum(v for k,v in sd.items() if k in TIP and v>0)
                            json.dump(dict(s=sg,slot=t["slot"],i=t.get("transactionIndex"),bt=t["blockTime"],sg=S,fee=t["meta"]["fee"],dm=dm,ws=ws,sol={k:v for k,v in sd.items() if k in S or k==O4},tip=tip,err=t["meta"]["err"],pg=sorted(programs(t)-BASIC)),o);o.write("\n")
            except EOFError:
                pass
o.close();print("tx",len(seen),round(time.time()-t0))
