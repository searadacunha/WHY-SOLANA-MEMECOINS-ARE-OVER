#!/usr/bin/env python3
"""Composantes sur les transferts propres >= seuil, avec hubs affiches. Parametres: seuil en jetons, adresses a exclure (fichier)."""
import csv, collections, sys
from pathlib import Path
SEEDS=["8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR","5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd","G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E","9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"]
TH=float(sys.argv[1]) if len(sys.argv)>1 else 1e6
EXC=set(Path(sys.argv[2]).read_text().split()) if len(sys.argv)>2 else set()
rows=[r for r in csv.DictReader(open('direct_edges_all.csv')) if int(r['amount'])>=TH*1e6 and r['src'] not in EXC and r['dst'] not in EXC]
adj=collections.defaultdict(set)
ind=collections.defaultdict(set);out=collections.defaultdict(set)
for r in rows:
    adj[r['src']].add(r['dst']);adj[r['dst']].add(r['src']);out[r['src']].add(r['dst']);ind[r['dst']].add(r['src'])
seen={};comps=[]
for s in adj:
    if s in seen: continue
    st=[s];c=[];seen[s]=len(comps)
    while st:
        x=st.pop();c.append(x)
        for y in adj[x]:
            if y not in seen: seen[y]=len(comps);st.append(y)
    comps.append(c)
comps.sort(key=len,reverse=True)
print('transferts',len(rows),'noeuds',len(adj),'composantes',len(comps),'tailles',[len(c) for c in comps[:12]])
for s in SEEDS: print(s[:8],'dans graphe',s in adj,'degre',len(adj.get(s,())),'taille comp',next((len(c) for c in comps if s in c),0))
print('hubs',[(a[:8],len(ind[a]),len(out[a])) for a in sorted(adj,key=lambda a:-len(adj[a]))[:30]])
