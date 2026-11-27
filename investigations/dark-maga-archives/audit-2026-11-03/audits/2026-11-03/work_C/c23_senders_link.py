#!/usr/bin/env python3
"""Population des expediteurs de 9W9b et des depots temoins : combien ont un solde DMAGA qui bouge dans le brut, combien de wallets temoin atteignent ce taux.
Ecrit senders_dmaga.csv et ctrl_senders_dmaga.csv."""
import csv, gzip, json, collections
import duckdb
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
NET=W+"/net"
ctrl=collections.defaultdict(set)
for line in gzip.open(f"{NET}/ctrl_deposits.jsonl.gz","rt"):
    j=json.loads(line); x=j['x']; tx=j['tx']
    seq=list(tx['transaction']['message']['instructions'])
    for g in tx['meta'].get('innerInstructions') or []: seq+=g['instructions']
    for i in seq:
        p=i.get('parsed')
        if i.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer' and p['info'].get('destination')==x and int(p['info']['lamports'])>=1_000_000:
            ctrl[x].add(p['info']['source'])
con=duckdb.connect()
con.execute(f"SET memory_limit='250MB'; SET threads=1; SET temp_directory='{W}/tmp';")
con.execute("CREATE TEMP TABLE s(x VARCHAR, sender VARCHAR)")
for x,ss in ctrl.items():
    con.executemany("INSERT INTO s VALUES (?,?)",[(x,y) for y in ss])
for r in csv.DictReader(open('audits/2026-11-03/work_C/9W9b3z_senders.csv')):
    con.execute("INSERT INTO s VALUES ('9W9b',?)",[r['sender']])
res=con.execute(f"""SELECT x, count(*) n, sum(CASE WHEN p.owner IS NOT NULL THEN 1 ELSE 0 END) nd
   FROM s LEFT JOIN '{W}/owner_profile.parquet' p ON p.owner=s.sender GROUP BY 1 ORDER BY n DESC""").fetchall()
w=csv.writer(open('audits/2026-11-03/work_C/ctrl_senders_dmaga.csv','w',newline='')); w.writerow(['x','n_senders','n_with_dmaga'])
for r in res: w.writerow(r)
tot=[r for r in res if r[0]!='9W9b']
print('9W9b',[r for r in res if r[0]=='9W9b'])
print('temoins: depots',len(tot),'expediteurs',sum(r[1] for r in tot),'avec solde DMAGA',sum(r[2] for r in tot),'part',sum(r[2] for r in tot)/max(1,sum(r[1] for r in tot)))
print('temoins avec >=1 expediteur DMAGA',sum(1 for r in tot if r[2]>0),'max',sorted([(r[2],r[1],r[0]) for r in tot],reverse=True)[:6])
rows=con.execute(f"""SELECT s.sender,p.n_tx,p.n_signed FROM s LEFT JOIN '{W}/owner_profile.parquet' p ON p.owner=s.sender WHERE x='9W9b' ORDER BY p.n_tx DESC NULLS LAST""").fetchall()
w=csv.writer(open('audits/2026-11-03/work_C/senders_dmaga.csv','w',newline='')); w.writerow(['sender','n_tx_dmaga','n_signed']); w.writerows(rows)
print('expediteurs sans solde DMAGA',[r[0] for r in rows if r[1] is None])
