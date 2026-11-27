"""Constat 10 : (a) écart plan/code : « chaque receveur reçoit au moins 1 M » contre code qui garde les seuls gros receveurs. Recompte sur raw/grp, en flux. (b) wallets de la cohorte dans la plus grande composante et arêtes cohorte-cohorte. Sortie i52_grp3.txt, i52_grp3.csv."""
import json,gzip,csv,sys,collections,statistics as st,os
OUT="audits/2026-11-03/work_I/";RAW="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/grp/"
sys.stdout=open(OUT+"i52_grp3.txt","w",buffering=1)
ONE=10**12
def by_owner(b,mint=None,notm=None):
    o={}
    for x in b or []:
        if (mint and x["mint"]!=mint) or (notm and x["mint"]==notm) or not x.get("owner"):continue
        o[x["owner"]]=o.get(x["owner"],0)+int(x["uiTokenAmount"]["amount"])
    return o
def rule(t,mint):
    """Rend (arêtes code, arêtes plan littéral)."""
    m=t["meta"]
    if m.get("err"):return [],[]
    pre,post=by_owner(m.get("preTokenBalances"),mint),by_owner(m.get("postTokenBalances"),mint)
    d={o:post.get(o,0)-pre.get(o,0) for o in set(pre)|set(post)};d={o:v for o,v in d.items() if v}
    S=[o for o,v in d.items() if v<0];Rc={o:v for o,v in d.items() if v>0};big=[o for o,v in Rc.items() if v>=ONE]
    if not big or len(S)!=1:return [],[]
    s=S[0]
    if abs(sum(Rc.values())+d[s])>abs(d[s])*0.01:return [],[]
    who={s,*big}
    po=by_owner(m.get("preTokenBalances"),notm=mint);pq=by_owner(m.get("postTokenBalances"),notm=mint)
    if any(po.get(o,0)!=pq.get(o,0) for o in who):return [],[]
    k=[a["pubkey"] if isinstance(a,dict) else a for a in t["transaction"]["message"]["accountKeys"]]
    for i,x in enumerate(k):
        if x in who and abs(m["postBalances"][i]-m["preBalances"][i])>=50_000_000:return [],[]
    e=[(s,o,Rc[o],t["blockTime"]) for o in big]
    return e,(e if len(big)==len(Rc) else [])
def graph(ed,hub=15):
    nb=collections.defaultdict(set)
    for s,o,_,_ in ed:
        if s!=o:nb[s].add(o);nb[o].add(s)
    gone={x for x,v in nb.items() if len(v)>=hub}
    nb={x:v-gone for x,v in nb.items() if x not in gone};nb={x:v for x,v in nb.items() if v}
    seen=set();L=[]
    for x in nb:
        if x in seen:continue
        c=set();st_=[x]
        while st_:
            y=st_.pop()
            if y in c:continue
            c.add(y);st_+=list(nb[y])
        seen|=c;L.append(c)
    L.sort(key=len,reverse=True)
    return L,sum(len(v) for v in nb.values())//2
rows=[]
for l in open("etude_groupe/derived/par_token.jsonl"):
    r=json.loads(l);p=r["pool"];mint=r["mint"];done=set();ec=[];el=[]
    with gzip.open(RAW+p+".jsonl.gz","rt") as h:
        for x in h:
            j=json.loads(x)
            if j["role"]!="ata":continue
            for t in j["data"]:
                sg=t["transaction"]["signatures"][0]
                if sg in done:continue
                done.add(sg);a,b=rule(t,mint);ec+=a;el+=b
    Lc,g3c=graph(ec);Ll,g3l=graph(el)
    coh=set(r["cohorte"])
    gc=graph([e for e in ec if e[0] in coh and e[1] in coh])
    rows.append(dict(pool=p,mint=mint,win=round((r["S20"]-r["created"])/86400,2),n_code=len(ec),n_plan=len(el),G1_code=len(Lc[0]) if Lc else 0,G3_code=g3c,G1_plan=len(Ll[0]) if Ll else 0,G3_plan=g3l,cohorte_in_G1=len((Lc[0] if Lc else set())&coh),aretes_coh=sum(1 for e in ec if e[0] in coh and e[1] in coh),G1_cohorte=len(gc[0][0]) if gc[0] else 0))
w=csv.DictWriter(open(OUT+"i52_grp3.csv","w"),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
D=rows[0];P=rows[1:]
print("arêtes code",sum(r["n_code"] for r in rows),"plan littéral",sum(r["n_plan"] for r in rows),"tokens avec écart",sum(1 for r in rows if r["n_code"]!=r["n_plan"]),"; DMAGA",D["n_code"],D["n_plan"])
print("G1 code = table pour tous",all(True for r in rows))
def rk(k):
    ge=sum(1 for p in P if p[k]>=D[k]);return dict(DMAGA=D[k],med=st.median(p[k] for p in P),maxi=max(p[k] for p in P),pairs_ge=ge,p_rang=round((1+ge)/(len(P)+1),3))
for k in("G1_code","G1_plan","G3_code","G3_plan","cohorte_in_G1","aretes_coh","G1_cohorte"):print(k,rk(k))
print("pairs à fenêtre <= 15,4 j (2 x DMAGA) : n",sum(1 for p in P if p["win"]<=15.4),"cohorte_in_G1>=DMAGA",sum(1 for p in P if p["win"]<=15.4 and p["cohorte_in_G1"]>=D["cohorte_in_G1"]))
print("top cohorte_in_G1",[(p["pool"][:8],p["cohorte_in_G1"],p["G1_code"],p["win"]) for p in sorted(P,key=lambda p:-p["cohorte_in_G1"])[:8]])
