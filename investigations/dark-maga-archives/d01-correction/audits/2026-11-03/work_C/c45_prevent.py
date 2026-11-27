#!/usr/bin/env python3
"""Groupe d'avant Musk reconstruit depuis mes aretes propres : comparaison au groupe de 33 et sensibilite au seuil. Sortie prevent_sens.csv, prevent_membership.txt"""
import csv, json, collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
g=json.load(open(REPO+'data/prevent_groups.json'))[0]; M=set(g['members']); S5="5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
TL=1721588607
tab={r['wallet']:r for r in csv.DictReader(open(ROOT+'members_table.csv'))}
def ts(u):
    import calendar,time
    return calendar.timegm(time.strptime(u,'%Y-%m-%dT%H:%M:%SZ'))
rows=[r for r in csv.DictReader(open(ROOT+'direct_edges_all.csv')) if ts(r['utc'])<TL]
SVC={"u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w"}
def comp(th,seed=S5,exc=frozenset(),cut=None):
    adj=collections.defaultdict(set); E=[r for r in rows if int(r['amount'])>=th*1e12 and r['src'] not in SVC and r['dst'] not in SVC and r['src'] not in exc and r['dst'] not in exc and (cut is None or r['sig'] not in cut)]
    for r in E: adj[r['src']].add(r['dst']);adj[r['dst']].add(r['src'])
    s={seed};st=[seed]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y not in s: s.add(y);st.append(y)
    return s,[r for r in E if r['src'] in s]
c,e=comp(1)
print('mon groupe avant Musk a 1 M',len(c),'aretes',len(e),'identique au 33 ?',c==M,'en plus',[x[:8] for x in c-M],'en moins',[x[:8] for x in M-c])
w=csv.writer(open(ROOT+'prevent_sens.csv','w',newline='')); w.writerow('threshold_M n_wallets n_edges held_Tlow_M_known'.split())
for th in (0.5,0.75,1,1.0001,1.25,1.5,2,2.5,3,4,5,7,10,15,20):
    c2,e2=comp(th)
    held=sum(float(tab[x]['held_Tlow']) for x in c2 if x in tab)
    w.writerow([th,len(c2),len(e2),round(held,2)]); print(th,len(c2),len(e2),round(held,2), 'hors table',[x[:6] for x in c2 if x not in tab][:8])
# seul le seuil 1 M tient les deux blocs ?
for x in ('NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7',):
    pass
# chaque membre : combien d'aretes le retiennent et quelle part du groupe tombe si on retire chacun
adj=collections.defaultdict(set)
for r in e: adj[r['src']].add(r['dst']);adj[r['dst']].add(r['src'])
def size_wo(v):
    s={S5} if v!=S5 else set(); st=list(s)
    while st:
        x=st.pop()
        for y in adj[x]:
            if y!=v and y not in s: s.add(y);st.append(y)
    return len(s)
print('retirer un noeud (restent autour de 5QhJJc):',sorted([(size_wo(v),v[:8]) for v in c if size_wo(v)<len(c)-1])[:10])
print('feuilles (degre 1)',sum(1 for v in c if len(adj[v])==1))
# composantes 2 M et plus
c5,_=comp(2); print('a 2 M autour de 5QhJJc',sorted(x[:8] for x in c5))
adj2=collections.defaultdict(set)
for r in rows:
    if int(r['amount'])>=1.0001e12 and r['src'] in M and r['dst'] in M: adj2[r['src']].add(r['dst']);adj2[r['dst']].add(r['src'])
