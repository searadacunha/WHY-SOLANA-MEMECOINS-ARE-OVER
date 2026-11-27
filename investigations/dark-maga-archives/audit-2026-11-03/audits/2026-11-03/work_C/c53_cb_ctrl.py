#!/usr/bin/env python3
"""Temoin de la serie Coinbase : memes 2 h a d'autres dates. Mesure : max de retraits a montant rond (multiple de 0,05 SOL) sur une fenetre glissante de 510 s, puis pour la meilleure rafale,
combien de destinataires sont neufs (premiere tx = ce retrait). Sortie cb_series_ctrl.csv"""
import csv, time, json
from pathlib import Path
from dmaga.helius import Helius
ROOT=Path(__file__).resolve().parent
HOT=["H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS","2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm","GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"]
T0=1720922725
wins=[T0-14*86400,T0-7*86400,T0-2*86400,T0-86400,T0,T0+86400,T0+2*86400,T0+7*86400,T0+14*86400]
h=Helius(); pages=0
w=csv.writer(open(ROOT/'cb_series_ctrl.csv','w',newline='')); w.writerow('t0_offset_days n_withdrawals best_round_run_510s n_fresh_in_run run_start_utc amounts'.split())
for tt in wins:
    out=[]
    for hot in HOT:
        tok=None
        for _ in range(20):
            r=h.txs_page(hot,details="full",limit=100,sort="asc",token=tok,filters={"blockTime":{"gte":tt-3000,"lt":tt+60},"status":"succeeded"})
            pages+=1
            for tx in r["data"]:
                for i in tx["transaction"]["message"]["instructions"]:
                    p=i.get("parsed")
                    if i.get("program")=="system" and isinstance(p,dict) and p.get("type")=="transfer" and p["info"].get("source")==hot:
                        out.append((tx["blockTime"],p["info"]["destination"],int(p["info"]["lamports"])))
            tok=r.get("paginationToken")
            if not tok: break
    out.sort()
    rnd=[x for x in out if x[2]%50_000_000==0 and x[2]>=50_000_000]
    best=[]
    for i in range(len(rnd)):
        run=[x for x in rnd if rnd[i][0]<=x[0]<rnd[i][0]+510]
        if len(run)>len(best): best=run
    fresh=0
    for t,d,l in best:
        f=h.txs_page(d,details="signatures",limit=1,sort="asc"); pages+=1
        if f["data"] and f["data"][0].get("blockTime")==t: fresh+=1
    w.writerow([round((tt-T0)/86400,1),len(out),len(best),fresh,time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(best[0][0])) if best else '',[x[2]/1e9 for x in best]])
    print(round((tt-T0)/86400,1),len(out),len(best),fresh,[x[2]/1e9 for x in best],flush=True)
with open(ROOT/"credits.csv","a") as f:
    f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},gtfa_x{pages},coinbase_ctrl,{pages*10}\n")
print('pages',pages)
