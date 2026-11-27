"""Constat 10, suite. (a) Égalités de composante : pourquoi 2 lignes diffèrent. (b) Fenêtre : S - created par token, corrélation avec G1, G1 et G3 à fenêtre fixe = celle de DMAGA, sans retirer d'observation. (c) Étiquettes (dmaga/labels) dans les graphes : le code ne les retire pas des arêtes. (d) Détail des 3 pairs les plus hauts sur G1. Sorties i51_grp2.txt, i51_fixed.csv."""
import json,csv,sys,collections,statistics as st,gzip,hashlib,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from dmaga.labels import load as load_labels
import importlib.util
spec=importlib.util.spec_from_file_location("grp","audits/2026-11-03/work_I/i50_grp.py")
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i51_grp2.txt","w")
ALPHA="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
P=2**255-19;D=(-121665*pow(121666,P-2,P))%P
def b58d(s):
    n=0
    for c in s:n=n*58+ALPHA.index(c)
    return b"\0"*(len(s)-len(s.lstrip("1")))+n.to_bytes((n.bit_length()+7)//8,"big")
def on_curve(a):
    b=b58d(a)
    if len(b)!=32:return False
    y=(int.from_bytes(b,"little")&((1<<255)-1))%P;u=(y*y-1)%P;v=(D*y*y+1)%P;x2=u*pow(v,P-2,P)%P
    return pow(x2,(P-1)//2,P) in(0,1)
ONE=10**12
def comps(edges,hub=15,drop=frozenset()):
    nb=collections.defaultdict(set)
    for e in edges:
        if e[2]>=ONE and e[0]!=e[1] and e[0] not in drop and e[1] not in drop:
            nb[e[0]].add(e[1]);nb[e[1]].add(e[0])
    gone={o for o,s in nb.items() if hub and len(s)>=hub}
    nb={o:s-gone for o,s in nb.items() if o not in gone}
    nb={o:s for o,s in nb.items() if s}
    seen=set();L=[]
    for o in nb:
        if o in seen:continue
        c=set();s=[o]
        while s:
            x=s.pop()
            if x in c:continue
            c.add(x);s+=list(nb[x])
        seen|=c;L.append(c)
    L.sort(key=len,reverse=True)
    return L,sum(len(s) for s in nb.values())//2,gone
labels=set(load_labels())
R=[]
with open("etude_groupe/derived/par_token.jsonl") as h:
    for l in h:
        r=json.loads(l);R.append({k:r[k] for k in("pool","mint","created","S20","aretes","soldes","extension_plafonnee","courbe_tronquee","nouveaux","cohorte")})
d0=R[0];W=d0["S20"]-d0["created"]
print("DMAGA fenêtre created->S en jours",round(W/86400,3))
rows=[]
for r in R:
    win=r["S20"]-r["created"]
    L,g3,gone=comps(r["aretes"])
    # G1 sur [début, created+W) : arêtes avant created comprises, comme dans la mesure gelée.
    e2=[e for e in r["aretes"] if e[3]<r["created"]+W]
    L2,g32,_=comps(e2)
    lab=[x for e in r["aretes"] for x in e[:2] if x in labels]
    L3,g33_,_=comps(r["aretes"],drop=frozenset(labels))
    tie=len(L)>1 and len(L[0])==len(L[1])
    rows.append(dict(pool=r["pool"],mint=r["mint"],win_j=round(win/86400,2),G1=len(L[0]) if L else 0,G3=g3,G1_fix=len(L2[0]) if L2 else 0,G3_fix=g32,labels_in=len(set(lab)),G1_sans_etiq=len(L3[0]) if L3 else 0,tie=tie,ext=r["extension_plafonnee"]))
w=csv.DictWriter(open(OUT+"i51_fixed.csv","w"),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print("(a) égalités de plus grande composante",[(x["pool"][:8],x["G1"]) for x in rows if x["tie"]])
D0=rows[0];peers=rows[1:]
def rk(k):
    ge=sum(1 for p in peers if p[k]>=D0[k]);return dict(DMAGA=D0[k],med=st.median(p[k] for p in peers),maxi=max(p[k] for p in peers),pairs_ge=ge,p_rang=round((1+ge)/(len(peers)+1),3))
print("(b) fenêtre pairs : médiane",st.median(p["win_j"] for p in peers),"min",min(p["win_j"] for p in peers),"max",max(p["win_j"] for p in peers),"; pairs à fenêtre plus courte que DMAGA",sum(1 for p in peers if p["win_j"]<D0["win_j"]))
def spearman(a,b):
    def ranks(v):
        s=sorted(range(len(v)),key=lambda i:v[i]);r=[0.0]*len(v);i=0
        while i<len(v):
            j=i
            while j+1<len(v) and v[s[j+1]]==v[s[i]]:j+=1
            for k in range(i,j+1):r[s[k]]=(i+j)/2
            i=j+1
        return r
    x,y=ranks(a),ranks(b);mx,my=st.mean(x),st.mean(y)
    return sum((p-mx)*(q-my) for p,q in zip(x,y))/((sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))**.5)
print("Spearman fenêtre et G1, pairs",round(spearman([p["win_j"] for p in peers],[p["G1"] for p in peers]),3),"; fenêtre et G3",round(spearman([p["win_j"] for p in peers],[p["G3"] for p in peers]),3))
print("G1",rk("G1"));print("G3",rk("G3"));print("G1 fenêtre fixe",rk("G1_fix"));print("G3 fenêtre fixe",rk("G3_fix"))
print("pairs >= DMAGA en G1 fenêtre fixe",[(p["pool"][:8],p["G1_fix"],p["G3_fix"],p["win_j"],p["ext"]) for p in peers if p["G1_fix"]>=D0["G1_fix"]])
print("pairs >= DMAGA en G3 fenêtre fixe",[(p["pool"][:8],p["G1_fix"],p["G3_fix"],p["win_j"],p["ext"]) for p in peers if p["G3_fix"]>=D0["G3_fix"]])
print("pairs de fenêtre <= 2 x DMAGA : n",sum(1 for p in peers if p["win_j"]<=2*D0["win_j"]),"G1>=34 parmi eux",sum(1 for p in peers if p["win_j"]<=2*D0["win_j"] and p["G1"]>=34))
print("(c) étiquettes dans les arêtes : pairs concernés",sum(1 for p in peers if p["labels_in"]),"DMAGA",D0["labels_in"],"; G1 sans étiquettes",rk("G1_sans_etiq"))
# (d) détail
top=sorted(R[1:],key=lambda r:-(len(comps(r["aretes"])[0][0]) if comps(r["aretes"])[0] else 0))[:3]
def ata(owner,mint):
    TP=b58d("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA");AP=b58d("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
    seeds=b58d(owner)+TP+b58d(mint)
    def e(b):
        n=int.from_bytes(b,"big");o=""
        while n:n,x=divmod(n,58);o=ALPHA[x]+o
        return "1"*(len(b)-len(b.lstrip(b"\0")))+o
    for bump in range(255,-1,-1):
        h=hashlib.sha256(seeds+bytes([bump])+AP+b"ProgramDerivedAddress").digest()
        y=(int.from_bytes(h,"little")&((1<<255)-1))%P;u=(y*y-1)%P;v=(D*y*y+1)%P;x2=u*pow(v,P-2,P)%P
        if pow(x2,(P-1)//2,P) not in(0,1):return e(h)
RAW="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/grp/"
iso=lambda t:dt.datetime.fromtimestamp(t,dt.timezone.utc).strftime("%m-%dT%H:%M")
for r in top+[R[0]]:
    L,g3,gone=comps(r["aretes"])
    best=L[0]
    print(f"\n(d) {r['pool']} mint {r['mint']} created {iso(r['created'])} S {iso(r['S20'])} fenêtre {round((r['S20']-r['created'])/86400,1)} j G1 {len(best)} G3 {g3} retirés {[x for x in gone]} cohorte dans composante {len(best&set(r['cohorte']))}")
    # activité ATA par propriétaire
    a2o={}
    for x in {y for e in r["aretes"] for y in e[:2]}|set(r["cohorte"]):
        a2o[ata(x,r["mint"])]=x
    cnt=collections.Counter();progs=collections.defaultdict(collections.Counter);signs=collections.defaultdict(collections.Counter)
    with gzip.open(RAW+r["pool"]+".jsonl.gz","rt") as h:
        for l in h:
            j=json.loads(l)
            if j["role"]!="ata":continue
            o=a2o.get(j["addr"])
            if not o:continue
            for t in j["data"]:
                cnt[o]+=1
                msg=t["transaction"]["message"]
                for i in msg["instructions"]:progs[o][i.get("programId")]+=1
                S=[a["pubkey"] for a in msg["accountKeys"] if a.get("signer")]
                if S:signs[o][S[0]]+=1
    deg=collections.Counter();od=collections.Counter();id_=collections.Counter();vol=collections.Counter();times=collections.defaultdict(list);amts=collections.Counter()
    for e in r["aretes"]:
        if e[2]>=ONE and e[0]!=e[1]:
            od[e[0]]+=1;id_[e[1]]+=1;vol[e[0]]+=e[2]/1e6;times[e[0]].append(e[3]);amts[round(e[2]/1e12,3)]+=1
    for x in sorted(best,key=lambda x:-(od[x]+id_[x]))[:10]:
        print("  ",x,"sort",od[x],"entre",id_[x],"M envoyés",round(vol[x]/1e6,2),"tx ATA",cnt[x],"cohorte" if x in r["cohorte"] else "","PDA" if not on_curve(x) else "","label" if x in labels else "","signé par soi",signs[x][x],"période",iso(min(times[x])) if times[x] else "",iso(max(times[x])) if times[x] else "")
    print("   montants les plus répétés (M) :",amts.most_common(8))
    print("   arêtes avant created",sum(1 for e in r["aretes"] if e[3]<r["created"] and e[2]>=ONE),"sur",sum(1 for e in r["aretes"] if e[2]>=ONE),"; par semaine depuis created",sorted(collections.Counter((e[3]-r["created"])//(7*86400) for e in r["aretes"] if e[2]>=ONE).items())[:10])
    print("   tx ATA des 30 de la cohorte, médiane",st.median(cnt[x] for x in r["cohorte"]),"; wallets avec 400+ tx ATA",sum(1 for x,v in cnt.items() if v>=400))
