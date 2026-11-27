#!/usr/bin/env python3
"""Sensibilite de la composante de 5QhJJc au seuil et a l'exclusion du hub de mise en commun. Sortie: sens_threshold.csv"""
import csv, collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
all_rows=list(csv.DictReader(open(ROOT+'direct_edges_all.csv')))
HUB="C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN"; SVC="u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w"
SEED="5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"; C="8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"; G="G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E"
w=csv.writer(open(ROOT+'sens_threshold.csv','w',newline='')); w.writerow('threshold_M hub_included n_nodes n_edges creator_in g41v_in'.split())
for th in (1,1.5,2,3,5,7,10,15,20):
  for hub in (False,True):
    exc={SVC}|(set() if hub else {HUB})
    adj=collections.defaultdict(set); E=[r for r in all_rows if int(r['amount'])>=th*1e12 and r['src'] not in exc and r['dst'] not in exc]
    for r in E: adj[r['src']].add(r['dst']);adj[r['dst']].add(r['src'])
    s={SEED};st=[SEED]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y not in s: s.add(y);st.append(y)
    n=sum(1 for r in E if r['src'] in s)
    w.writerow([th,hub,len(s),n,C in s,G in s]); print(th,hub,len(s),n,C in s,G in s)
