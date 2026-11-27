#!/usr/bin/env python3
"""Detail de la composante d'une graine et noeuds relais (points d'articulation)."""
import csv, collections, sys
from pathlib import Path
SEED=sys.argv[1]; EXC=set(Path(sys.argv[2]).read_text().split()) if len(sys.argv)>2 and Path(sys.argv[2]).exists() else set()
TH=float(sys.argv[3]) if len(sys.argv)>3 else 1e6
rows=[r for r in csv.DictReader(open('direct_edges_all.csv')) if int(r['amount'])>=TH*1e6 and r['src'] not in EXC and r['dst'] not in EXC]
adj=collections.defaultdict(set)
for r in rows: adj[r['src']].add(r['dst']);adj[r['dst']].add(r['src'])
seen={SEED};st=[SEED]
while st:
    x=st.pop()
    for y in adj[x]:
        if y not in seen: seen.add(y);st.append(y)
E=[r for r in rows if r['src'] in seen]
print('noeuds',len(seen),'transferts',len(E),'jetons (M)',sum(int(r['amount']) for r in E)/1e12)
for r in sorted(E,key=lambda r:(int(r['slot']),int(r['txidx'] or 0))):
    print(r['utc'],r['sig'][:10],r['src'][:8],'>',r['dst'][:8],f"{int(r['amount'])/1e12:,.2f}M",'pay:'+r['payer'][:6],'auth_ok' if r['authority']==r['src'] else 'AUTH:'+str(r['authority'])[:6],r['origin'][:3],r['kind'][-7:])
# points d'articulation
def comps_wo(v):
    s={SEED} if SEED!=v else set()
    st=list(s)
    while st:
        x=st.pop()
        for y in adj[x]:
            if y!=v and y not in s: s.add(y);st.append(y)
    return len(s)
art=[(v[:8],len(seen)-1-comps_wo(v)) for v in seen if v!=SEED and len(seen)-1-comps_wo(v)>0]
print('si on retire un noeud, nb de noeuds perdus:',sorted(art,key=lambda x:-x[1])[:20])
