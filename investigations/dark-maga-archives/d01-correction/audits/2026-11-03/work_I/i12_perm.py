"""G3 : test de permutation refait. Stat de G : nombre de wallets communs dont l'écart minimal entre un versement à 9W9b et un à Caw4 est <= W. Calendrier fixe, permutation des wallets. Fenêtres multiples, et sans le 26/01/2025. Puis test d'événements entre wallets DIFFÉRENTS (décalage circulaire), seul à parler d'une séance commune. Sortie i12_perm.txt."""
import csv,sys,collections,datetime as dt,random,bisect
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i12_perm.txt","w")
ep=lambda u:int(dt.datetime.strptime(u,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
rows=[r for r in csv.DictReader(open(OUT+"i01_moves.csv")) if r["side"]=="in" and r["depot"] in("9W9b","Caw4")]
amt=collections.Counter()
for r in rows: amt[(r["depot"],r["cp"],r["asset"])]+=float(r["amount"])
ok9={c for (d,c,a),v in amt.items() if d=="9W9b" and a=="SOL" and v>=0.01}
okC={c for (d,c,a),v in amt.items() if d=="Caw4" and ((a=="SOL" and v>=0.01) or (a!="SOL" and v>=1))}
com=sorted(ok9&okC)
A=collections.defaultdict(list);B=collections.defaultdict(list)
for r in rows:
    if r["depot"]=="9W9b" and r["cp"] in ok9 and float(r["amount"])>=0.001: A[r["cp"]].append(ep(r["utc"]))
    if r["depot"]=="Caw4" and r["cp"] in okC and (float(r["amount"])>=0.001 if r["asset"]=="SOL" else float(r["amount"])>=0.1): B[r["cp"]].append(ep(r["utc"]))
print("communs",len(com),"A",sum(len(A[c]) for c in com),"B",sum(len(B[c]) for c in com))
def gap(x,y):
    y=sorted(y);m=10**12
    for t in x:
        i=bisect.bisect(y,t)
        for j in (i-1,i):
            if 0<=j<len(y): m=min(m,abs(t-y[j]))
    return m
print("écart minimal par wallet commun, <= 1 jour")
det=[]
for c in com:
    g=gap(A[c],B[c])
    # jour de l'écart minimal
    best=None
    for t in A[c]:
        for u in B[c]:
            if abs(t-u)==g: best=t
    det.append((g,c,dt.datetime.fromtimestamp(best,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")))
for g,c,d in sorted(det):
    if g<=86400: print(f"  {g:>7} s {c} {d}")
days=collections.Counter(d[:10] for g,c,d in det if g<=900)
print("jours des écarts <= 15 min",sorted(days.items()))
def stat(pa,W): return sum(1 for a,b in pa if gap(a,b)<=W)
random.seed(20261103)
keysA=[A[c] for c in com];keysB=[B[c] for c in com]
N=5000
# précalcul de la matrice des écarts, permutation rapide
M=[[gap(a,b) for b in keysB] for a in keysA]
def run(M,W,N):
    n=len(M);obs=sum(1 for i in range(n) if M[i][i]<=W);idx=list(range(n));ge=0;tot=0
    for _ in range(N):
        random.shuffle(idx);s=sum(1 for i in range(n) if M[i][idx[i]]<=W);tot+=s;ge+=s>=obs
    return obs,round(tot/N,3),ge,round((ge+1)/(N+1),5)
for W in (60,180,300,600,900,1800,3600,7200,21600,86400):
    print("fenêtre",W,"s : obs, moyenne, tirages>=obs, P",run(M,W,N))
# Sans la séance du 26/01/2025
J0,J1=ep("2025-01-26T00:00:00Z"),ep("2025-01-27T00:00:00Z")
Af=[[t for t in a if not J0<=t<J1] for a in keysA];Bf=[[t for t in b if not J0<=t<J1] for b in keysB]
Mf=[[gap(a,b) if a and b else 10**12 for b in Bf] for a in Af]
print("sans le 26/01/2025, 900 s :",run(Mf,900,N))
# Le 26/01/2025 seul
Aj=[[t for t in a if J0<=t<J1] for a in keysA];Bj=[[t for t in b if J0<=t<J1] for b in keysB]
Mj=[[gap(a,b) if a and b else 10**12 for b in Bj] for a in Aj]
print("le 26/01/2025 seul, 900 s :",run(Mj,900,N),"wallets communs actifs des deux côtés ce jour",sum(1 for a,b in zip(Aj,Bj) if a and b))
print("ce jour, wallets vers 9W9b",sum(1 for a in Aj if a),"vers Caw4",sum(1 for b in Bj if b))
# Test entre wallets DIFFÉRENTS, tous expéditeurs >= seuil : paires (a,b), a de A, b de B, wallets différents, |t|<=W ; décalage circulaire de B sur toute la durée.
EA=[(t,c) for c in ok9 for t in A[c]];EB=[(t,c) for c in okC for t in B[c]]
tmin=min(t for t,_ in EA+EB);tmax=max(t for t,_ in EA+EB);L=tmax-tmin
def cross(EA,EB,W):
    tb=sorted(EB);ts=[t for t,_ in tb];n=0;same=0
    for t,c in EA:
        i=bisect.bisect_left(ts,t-W);j=bisect.bisect_right(ts,t+W)
        for k in range(i,j):
            if tb[k][1]!=c:n+=1
            else: same+=1
    return n,same
for W in (900,3600):
    o=cross(EA,EB,W)
    ge=0;tt=0;NN=2000
    for _ in range(NN):
        s=random.randint(3600*24,L-3600*24)
        sh=[(tmin+((t-tmin+s)%L),c) for t,c in EB]
        v=cross(EA,sh,W)[0];tt+=v;ge+=v>=o[0]
    print(f"événements, wallets différents, W={W}: obs {o[0]} (même wallet {o[1]}), décalage circulaire moyenne {tt/NN:.1f}, P {(ge+1)/(NN+1):.5f}")
    # sans le 26/01/2025
    ea=[e for e in EA if not J0<=e[0]<J1];eb=[e for e in EB if not J0<=e[0]<J1]
    o2=cross(ea,eb,W);ge=0;tt=0
    for _ in range(NN):
        s=random.randint(3600*24,L-3600*24);sh=[(tmin+((t-tmin+s)%L),c) for t,c in eb];v=cross(ea,sh,W)[0];tt+=v;ge+=v>=o2[0]
    print(f"   sans le 26/01/2025 : obs {o2[0]}, moyenne {tt/NN:.1f}, P {(ge+1)/(NN+1):.5f}")
