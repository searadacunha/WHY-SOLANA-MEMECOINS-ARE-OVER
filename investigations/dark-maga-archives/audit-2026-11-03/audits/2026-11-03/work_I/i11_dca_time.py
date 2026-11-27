"""Calendrier de l'encaissement DCA, USDC et SOL natif, par rapport à 19:30:13 le 21/07/2024 (S). Vérifie « rien avant ». SOL natif < 0,01 écarté (rent, même règle que G). Sortie i11_dca_time.txt, i11_fills_sol.csv."""
import csv,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i11_dca_time.txt","w")
price={r["date"]:float(r["close"]) for r in csv.DictReader(open("audits/2026-11-03/work_G/sol_daily.csv"))}
ord_={r["order_pda"]:r for r in csv.DictReader(open(OUT+"i08_recon.csv"))}
series={r["dest"] if "dest" in r else list(r.values())[2] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
print("série lue depuis cb_series.csv",len(series))
byw=collections.defaultdict(set)
for o,r in ord_.items(): byw[r["wallet"]].add(o)
S0=int(dt.datetime(2024,7,21,19,30,13,tzinfo=dt.timezone.utc).timestamp())
T=collections.Counter();Ser=collections.Counter()
f=csv.writer(open(OUT+"i11_fills_sol.csv","w"));f.writerow("wallet utc sig sol_natif dmaga_sold order".split())
for w,os_ in byw.items():
    for t in iter_tx(w):
        if not ok(t): continue
        td,dec=tok_delta(t); logs=" ".join(t["meta"].get("logMessages") or [])
        hit={o for (o,m) in td}&os_
        if not hit or "OpenDca" in logs or "FulfillFlashFill" not in logs: continue
        ts=t["blockTime"]; d=dt.datetime.fromtimestamp(ts,dt.timezone.utc)
        px=price[d.strftime("%Y-%m-%d")]
        usd=td.get((w,USDC),0)/1e6; sol=sol_delta(t).get(w,0)/1e9
        sol=sol if sol>=0.01 else 0
        v=max(usd,0)/px+sol
        k="avant S" if ts<S0 else "24 h apres S" if ts<S0+86400 else "ensuite"
        T[k]+=v;T[k+" usdc"]+=max(usd,0)/px;T[k+" sol"]+=sol
        if w in series: Ser[k]+=v
        if sol: f.writerow([w,d.strftime("%Y-%m-%dT%H:%M:%SZ"),t["transaction"]["signatures"][0],round(sol,6),sum(-v2 for (x,m),v2 in td.items() if m==DMAGA and v2<0)/1e6,sorted(hit)[0]])
print({k:round(v,2) for k,v in sorted(T.items())})
print("série seule",{k:round(v,2) for k,v in Ser.items()})
print("total",round(sum(v for k,v in T.items() if k in("avant S","24 h apres S","ensuite")),2))
