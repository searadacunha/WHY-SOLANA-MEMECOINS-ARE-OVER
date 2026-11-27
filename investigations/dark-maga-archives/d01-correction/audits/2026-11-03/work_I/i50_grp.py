"""Constat 10 : recalcul indépendant de derived/table.csv depuis par_token.jsonl (graphe réécrit), puis structure des réseaux des pairs : PDA (hors courbe), étoile, montants répétés, tx multi-receveurs, durée. Variantes descriptives, sans valeur de verdict. Sorties i50_grp.txt, i50_structure.csv."""
import json,csv,sys,hashlib,collections,statistics as st
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i50_grp.txt","w")
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
ONE=10**12;SUP=10**15
def comp(nb):
    seen=set();best=set()
    for o in sorted(nb):
        if o in seen:continue
        c=set();s=[o]
        while s:
            x=s.pop()
            if x in c:continue
            c.add(x);s+=list(nb.get(x,()))
        seen|=c
        if len(c)>len(best):best=c
    return best
def measure(edges,bal,minraw=ONE,hub=15,drop=()):
    nb=collections.defaultdict(set)
    for e in edges:
        if e[2]>=minraw and e[0]!=e[1] and e[0] not in drop and e[1] not in drop:
            nb[e[0]].add(e[1]);nb[e[1]].add(e[0])
    gone={o for o,s in nb.items() if hub and len(s)>=hub}
    nb={o:s-gone for o,s in nb.items() if o not in gone}
    nb={o:s for o,s in nb.items() if s}
    b=comp(nb)
    return len(b),sum(bal.get(o,0) for o in b)/SUP,sum(len(s) for s in nb.values())//2,len(gone),b
T={r["pool"]:r for r in csv.DictReader(open("etude_groupe/derived/table.csv"))}
ok=0;bad=[]
R=[]
with open("etude_groupe/derived/par_token.jsonl") as h:
    for l in h:
        r=json.loads(l)
        e=r["aretes"];bal=r["soldes"]
        g1,g2,g3,svc,best=measure(e,bal)
        t=T[r["pool"]]
        same=int(t["principal_G1"])==g1 and abs(float(t["principal_G2"])-g2)<1e-9 and int(t["principal_G3"])==g3 and int(t["services_retires"])==svc
        ok+=same
        if not same:bad.append((r["pool"],g1,t["principal_G1"]))
        v1=measure(e,bal,minraw=5*ONE);v2=measure(e,bal,hub=None)
        same2=int(t["V1_5M_G1"])==v1[0] and int(t["V2_sans_retrait_G1"])==v2[0]
        if not same2:bad.append((r["pool"],"var",v1[0],t["V1_5M_G1"],v2[0],t["V2_sans_retrait_G1"]))
        # structure
        nodes={x for ed in e for x in ed[:2]}
        pda={x for x in nodes if not on_curve(x)}
        deg=collections.Counter();outd=collections.Counter();ind=collections.Counter();bysig=collections.Counter();amt=collections.Counter();pairs=set()
        for ed in e:
            if ed[2]>=ONE and ed[0]!=ed[1]:
                pairs.add(frozenset(ed[:2]));outd[ed[0]]+=1;ind[ed[1]]+=1;bysig[ed[4]]+=1;amt[ed[2]]+=1
        for p in pairs:
            for x in p:deg[x]+=1
        multi=sum(v for v in bysig.values() if v>=3)
        repeat=sum(v for v in amt.values() if v>=3)
        n=sum(outd.values()) or 1
        topout=outd.most_common(1)[0] if outd else ("",0)
        ts=[ed[3] for ed in e if ed[2]>=ONE]
        before=sum(1 for t_ in ts if t_<r["created"])
        nopda=measure(e,bal,drop=pda)
        hub5=measure(e,bal,hub=5)
        nomulti_e=[ed for ed in e if bysig[ed[4]]<3]
        nomulti=measure(nomulti_e,bal)
        R.append(dict(pool=r["pool"],mint=r["mint"],created=r["created"],S=r["S20"],G1=g1,G2=round(g2,4),G3=g3,svc=svc,n_edges=len(e),nodes=len(nodes),pda=len(pda),pda_in_best=len(best&pda),top_out=topout[1],top_out_share=round(topout[1]/n,3),max_deg=max(deg.values() or [0]),multi_recv_edges=multi,repeat_amount_edges=repeat,edges_before_created=before,edge_days=round((max(ts)-min(ts))/86400,2) if ts else 0,G1_noPDA=nopda[0],G2_noPDA=round(nopda[1],4),G1_hub5=hub5[0],G2_hub5=round(hub5[1],4),G1_nomulti=nomulti[0],ext_cap=r["extension_plafonnee"],curve_trunc=r["courbe_tronquee"],cov=r["couverture"],nouveaux=r["nouveaux"]))
print("lignes conformes",ok,"sur",len(T),"écarts",bad[:6])
w=csv.DictWriter(open(OUT+"i50_structure.csv","w"),fieldnames=list(R[0]));w.writeheader();w.writerows(R)
D_=R[0];assert D_["pool"].startswith("CRSwXnfF");peers=R[1:]
print("DMAGA",{k:D_[k] for k in("G1","G2","G3","svc","nodes","pda","pda_in_best","top_out","top_out_share","max_deg","multi_recv_edges","repeat_amount_edges","G1_noPDA","G2_noPDA","G1_hub5","G2_hub5","G1_nomulti")})
def rang(k,sens=1):
    v=D_[k];ge=sum(1 for p in peers if p[k]>=v);return dict(DMAGA=v,mediane=st.median(p[k] for p in peers),maxi=max(p[k] for p in peers),pairs_ge=ge,pct_rang=round(100*(1-ge/len(peers)),1),p_rang=round((1+ge)/(len(peers)+1),3))
for k in("G1","G2","G3","G1_noPDA","G2_noPDA","G1_hub5","G2_hub5","G1_nomulti"):print(k,rang(k))
print("pairs avec PDA dans le réseau",sum(1 for p in peers if p["pda"]),"médiane PDA",st.median(p["pda"] for p in peers),"; part médiane du plus gros expéditeur",st.median(p["top_out_share"] for p in peers),"DMAGA",D_["top_out_share"])
print("pairs à G1>=34 :")
for p in sorted(peers,key=lambda p:-p["G1"])[:10]:
    print(" ",p["pool"][:10],p["mint"],"G1",p["G1"],"G2",p["G2"],"G3",p["G3"],"svc",p["svc"],"nœuds",p["nodes"],"PDA",p["pda"],"topout",p["top_out"],p["top_out_share"],"multi",p["multi_recv_edges"],"rép",p["repeat_amount_edges"],"jours",p["edge_days"],"avant_created",p["edges_before_created"],"sansPDA",p["G1_noPDA"],"hub5",p["G1_hub5"],"sansmulti",p["G1_nomulti"],"ext",p["ext_cap"])
