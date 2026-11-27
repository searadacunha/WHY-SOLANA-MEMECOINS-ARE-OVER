#!/usr/bin/env python3
"""Destinataires des virements de 0,5 SOL de G41vRr avant le mint : premiere activite DMAGA, volumes, et tout l'historique de ce type chez G41vRr."""
import csv, duckdb, time, collections
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
MINT_T=1720922725
rec=[]; all_05=[]
for r in csv.DictReader(open(ROOT+'chrono_G41vRr.csv')):
    for x in r['sys_out'].split(';'):
        if not x: continue
        a,v=x.split('(')[0].rsplit(':',1)
        if int(v)==500000000:
            all_05.append((r['utc'],a,r['sig']))
print('tous les virements exacts de 0,5 SOL de G41vRr',len(all_05),collections.Counter(u[:10] for u,_,_ in all_05))
pre=[(u,a,s) for u,a,s in all_05 if u<'2024-07-14T02:05:25Z' and u>='2024-07-14']
print('avant le mint le 14/07',len(pre))
con=duckdb.connect(); con.execute(f"SET memory_limit='250MB'; SET threads=1; SET TimeZone='UTC'; SET temp_directory='{W}/tmp';")
con.execute("CREATE TEMP TABLE r(u VARCHAR, a VARCHAR, s VARCHAR)")
con.executemany("INSERT INTO r VALUES (?,?,?)",pre)
out=con.execute(f"""WITH t AS (SELECT coalesce(nullif(owner_post,''),owner_pre) owner, tid, post-pre d FROM '{W}/ta.parquet' WHERE coalesce(nullif(owner_post,''),owner_pre) IN (SELECT a FROM r)),
 j AS (SELECT t.owner, t.tid, t.d, x.bt, x.sig, x.slot, x.txidx, x.programs FROM t JOIN '{W}/tx.parquet' x USING(tid))
 SELECT owner, count(*) n, min(bt) first_bt, sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e6 gross_in, sum(CASE WHEN d<0 THEN -d ELSE 0 END)/1e6 gross_out, arg_min(sig,bt) first_sig, arg_min(d,bt)/1e6 first_d FROM j GROUP BY 1""").fetchall()
d={o[0]:o for o in out}
w=csv.writer(open(ROOT+'g41v_recipients.csv','w',newline=''))
w.writerow('funded_utc recipient fund_sig n_tx first_dmaga_utc secs_after_mint gross_in_M gross_out_M first_delta_M first_sig'.split())
for u,a,s in pre:
    o=d.get(a)
    if o:
        w.writerow([u,a,s,o[1],time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(o[2])),o[2]-MINT_T,round(o[3]/1e6,3),round(o[4]/1e6,3),round(o[6]/1e6,3),o[5]])
        print(u,a[:8],'n',o[1],'premier',time.strftime('%H:%M:%S',time.gmtime(o[2])),'+',o[2]-MINT_T,'s in',round(o[3]/1e6,2),'M out',round(o[4]/1e6,2),'M d1',round(o[6]/1e6,2))
    else:
        w.writerow([u,a,s,0,'','','','','','']); print(u,a[:8],'AUCUN DMAGA')
