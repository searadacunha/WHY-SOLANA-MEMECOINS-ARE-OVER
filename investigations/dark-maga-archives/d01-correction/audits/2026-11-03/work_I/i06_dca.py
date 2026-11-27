"""G3. DCA refait sur le brut. Périmètre : wallets de g40_p1_wallets.csv (liste seule, reprise de G pour tester SES chiffres), plus expéditeurs de mes dépôts.
Ouverture = journal 'OpenDca' du programme DCA265. Jetons déposés = delta négatif du wallet dans la tx d'ouverture. Encaissement = entrée d'USDC/SOL/WSOL dans une tx portant le programme DCA, wallet receveur.
Sorties : i06_open.csv, i06_recv.csv, i06_dca.txt."""
import csv,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
DCA="DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M"
P1=[r["wallet"] if "wallet" in r else list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))]
SER=[r["dest"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))] if False else []
lg=open(OUT+"i06_dca.txt","w")
def P(*a): print(*a,file=lg)
op=csv.writer(open(OUT+"i06_open.csv","w")); op.writerow("wallet utc sig kind in_mint in_amt signer".split())
rc=csv.writer(open(OUT+"i06_recv.csv","w")); rc.writerow("wallet utc sig mint amt kind".split())
nw=0; miss=[]
K=collections.Counter()
for w in P1:
    ps=net_paths(w)
    if not ps: miss.append(w); continue
    nw+=1
    for t in iter_tx(w):
        if not ok(t): continue
        if DCA not in programs(t): continue
        logs=t["meta"].get("logMessages") or []
        ks=[l.split("Instruction: ")[1] for l in logs if "Program log: Instruction: " in l and any(x in l for x in ("Dca","Fill","Withdraw","Close","Deposit","Kickoff","Transfer"))]
        kind=next((k for k in ks if "OpenDca" in k),None)
        sg=t["transaction"]["signatures"][0]; td,dec=tok_delta(t); sd=sol_delta(t)
        u=dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        K[(tuple(sorted(set(ks))))]+=1
        if kind:
            neg=[(m,-v/10**dec[m]) for (o,m),v in td.items() if o==w and v<0]
            for m,a in neg or [("?",0)]:
                op.writerow([w,u,sg,kind,m,a,signers(t)[0]])
        else:
            for (o,m),v in td.items():
                if o==w and v>0: rc.writerow([w,u,sg,m,v/10**dec[m],"|".join(sorted(set(ks)))])
            if sd.get(w,0)>0: rc.writerow([w,u,sg,"SOL",sd[w]/1e9,"|".join(sorted(set(ks)))])
P("wallets P1",len(P1),"lus",nw,"absents",miss)
for k,v in K.most_common(20): P(v,k)
