#!/usr/bin/env python3
"""Matrice de preuves par membre du groupe : ce qui les relie hors des transferts de jetons. Sortie member_evidence.csv et impression.
Preuves SOL lues depuis sol_edges.csv (historiques complets). Destinataires neufs : premiere tx a moins de 5 min avant la premiere reception de jetons."""
import csv, json, gzip, time, collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
NET='/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/'
g=json.load(open(REPO+'data/prevent_groups.json'))[0]; M=sorted(g['members']); MS=set(M); E=g['edges_top']
G41="G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E"; W9="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"; CR="8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
T0,TL=1720922725,1721588607
sol=list(csv.DictReader(open(ROOT+'sol_edges.csv')))
tab={r['wallet']:r for r in csv.DictReader(open(ROOT+'members_table.csv'))}
small=set(m for s in json.load(open(REPO+'data/group_split.json'))['ponts_faibles'] if s['M']==15.0 for m in s['members'])
deg=collections.Counter()
for e in E: deg[e['src']]+=1; deg[e['dst']]+=1
first_rcv={}
for e in sorted(E,key=lambda e:e['t']): first_rcv.setdefault(e['dst'],e['t'])
def ts(u): return int(time.mktime(time.strptime(u,'%Y-%m-%dT%H:%M:%SZ')))-time.timezone
w=csv.writer(open(ROOT+'member_evidence.csv','w',newline=''))
cols='wallet in29 held_Tlow_M token_edges g41_funded_avant_mint sol_from_group_n sol_to_group_n sol_group_total first_funder_in_group sends_9W9b_SOL n_tx neuf_avant_reception a_autre_preuve'.split()
w.writerow(cols)
res=[]
for m in M:
    g41=[x for x in sol if x['src']==G41 and x['dst']==m and T0-3600*2<=int(x['bt'])<=T0+3600]
    frm=[x for x in sol if x['dst']==m and x['src'] in MS and int(x['lamports'])>=1e7]
    to=[x for x in sol if x['src']==m and x['dst'] in MS and int(x['lamports'])>=1e7]
    tot=sum(int(x['lamports']) for x in frm+to)/1e9
    s9=sum(int(x['lamports']) for x in sol if x['src']==m and x['dst']==W9)/1e9
    ff=tab[m]['first_funder'] in MS or tab[m]['first_funder']==G41
    neuf=m in first_rcv and (first_rcv[m]-ts(tab[m]['first_tx']))<=300
    other=bool(g41 or frm or to or s9>0 or ff or neuf)
    row=[m,m not in small,round(float(tab[m]['held_Tlow']),3),deg[m],sum(int(x['lamports']) for x in g41)/1e9,len(frm),len(to),round(tot,3),ff,round(s9,3),tab[m]['n_tx'],neuf,other]
    w.writerow(row); res.append(row)
for r in sorted(res,key=lambda r:(r[12],r[2])): print(r[0][:9],'29' if r[1] else ' 4','held',r[2],'edges',r[3],'g41',r[4],'de',r[5],'vers',r[6],'SOL',r[7],'ff',r[8],'9W',r[9],'tx',r[10],'neuf',r[11],'AUTRE' if r[12] else 'SEULEMENT JETON')
only=[r for r in res if not r[12]]
print('sans autre preuve',len(only),'held',sum(r[2] for r in only),[r[0][:8] for r in only])
print('dans 29 sans autre preuve',len([r for r in only if r[1]]),sum(r[2] for r in only if r[1]))
print('G41 finance dans le groupe',[ (r[0][:6],r[4]) for r in res if r[4]])
print('9W9b dans le groupe',[ (r[0][:6],r[9]) for r in res if r[9]])
# liens de SOL entre les deux blocs du groupe (seuil strict) et avec le bloc de 4
strict=json.load(open(REPO+'data/group_split.json'))
