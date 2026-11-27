"""Encaissement par ordre DCA DMAGA : tout ce que le wallet reçoit (hors DMAGA) dans une tx où le PDA de l'ordre bouge du DMAGA ou l'actif de sortie. Reprend i08_recon.csv pour les PDA. Contrôle du cours quotidien contre raw/solusd. Sortie i09_cash.txt."""
import csv,sys,collections,datetime as dt,zipfile,io
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i09_cash.txt","w")
price={}
for r in csv.DictReader(open("audits/2026-11-03/work_G/sol_daily.csv")): price[r["date"]]=float(r["close"])
ord_={r["order_pda"]:r for r in csv.DictReader(open(OUT+"i08_recon.csv"))}
byw=collections.defaultdict(set)
for o,r in ord_.items(): byw[r["wallet"]].add(o)
K=collections.Counter(); Kj=collections.Counter(); T=collections.defaultdict(float); seen=set(); by=collections.Counter(); perday=collections.Counter()
for w,os_ in byw.items():
    for t in iter_tx(w):
        if not ok(t): continue
        sg=t["transaction"]["signatures"][0]; td,dec=tok_delta(t)
        owners={o for (o,m) in td}
        hit=owners&os_
        if not hit: continue
        logs=" ".join(t["meta"].get("logMessages") or [])
        if "OpenDca" in logs: continue
        d=dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc).strftime("%Y-%m-%d")
        for (o,m),v in td.items():
            if o==w and v>0 and m!=DMAGA:
                a=v/10**dec[m]
                se=a/price[d] if m in(USDC,USDT) else a if m==WSOL else 0
                K[m]+=a; T["soleq"]+=se; by[w]+=se; perday[d]+=se
                Kj["fill" if "FulfillFlashFill" in logs else "close"]+=se
        sd=sol_delta(t).get(w,0)
        if sd>1e8: T["sol_natif_>0.1"]+=sd/1e9
print("encaissé par actif",{(k[:6]):round(v,3) for k,v in K.items()})
print("SOL éq total",round(T["soleq"],2),"dont exécution/clôture",{k:round(v,2) for k,v in Kj.items()},"SOL natif reçu >0,1 hors",round(T["sol_natif_>0.1"],3))
print("prix par M vendus",round(T["soleq"]/48.571,2))
print("top wallets",[(k[:8],round(v,1)) for k,v in by.most_common(8)])
# Cours : contrôle sur 3 jours
for ym,days in (("2024-07",["2024-07-21","2024-07-22"]),("2025-01",["2025-01-26"])):
    try:
        z=zipfile.ZipFile(f"{R}/raw/solusd/SOLUSDT-1m-{ym}.zip"); n=[x for x in z.namelist() if x.endswith(".csv")][0]
        with z.open(n) as h:
            last={}
            for l in io.TextIOWrapper(h):
                p=l.split(",")
                if not p[0].isdigit(): continue
                ms=int(p[0]); ms=ms/1000 if ms>1e14 else ms
                dd=dt.datetime.fromtimestamp(ms/1000,dt.timezone.utc).strftime("%Y-%m-%d")
                if dd in days: last[dd]=p[4]
        print("cours Binance dernier 1m",last,"sol_daily",{d:price[d] for d in days})
    except FileNotFoundError as e: print("absent",ym)
