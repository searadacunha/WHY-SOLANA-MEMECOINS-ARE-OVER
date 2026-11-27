#!/usr/bin/env python3
"""Controles divers post-sceau : Habp5bnc, transferts sortants du groupe en 24 h et devenir, premier financeur du rapport, grappes du rapport, HQ2UUt, hubs, seuils bas. Sortie c50.out"""
import csv, json, duckdb, time, collections
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
B="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
ROOT=REPO+'audits/2026-11-03/work_C/'
TL,TH=1721588607,1721590213
M=set(json.load(open(REPO+'data/prevent_groups.json'))[0]['members'])
con=duckdb.connect(); con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/tmp'; SET preserve_insertion_order=false;")
con.execute("CREATE TEMP TABLE m(a VARCHAR)"); con.executemany("INSERT INTO m VALUES (?)",[(x,) for x in M])
H="Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96"
print('Habp nodes',con.execute(f"SELECT * FROM '{B}/nodes.parquet' WHERE address='{H}'").fetchall())
print('Habp wallets',con.execute(f"SELECT owner,n_buys,n_sells,n_transfers,bought_qty,sold_qty,realized_sol,transfer_in_qty,transfer_out_qty,residual_qty FROM '{B}/wallets.parquet' WHERE owner='{H}'").fetchall())
print('Habp tok',con.execute(f"SELECT signature,src,dst,qty,block_time,how FROM '{B}/token_edges.parquet' WHERE src='{H}' OR dst='{H}' ORDER BY qty DESC LIMIT 6").fetchall())
print('Habp ta',con.execute(f"SELECT count(*),sum(post-pre)/1e12 FROM '{W}/ta.parquet' WHERE owner_post='{H}' OR owner_pre='{H}'").fetchone())
print('edges cand Habp',[ (r['utc'],r['src'][:8],r['dst'][:8],int(r['amount'])/1e12,r['payer'][:8],r['sig']) for r in csv.DictReader(open(ROOT+'direct_edges_all.csv')) if H in (r['src'],r['dst'])])
# transferts sortants du groupe dans les 24 h et ce que font les destinataires
rows=con.execute(f"""SELECT src,dst,qty,block_time,signature FROM '{B}/token_edges.parquet' WHERE block_time>={TH} AND block_time<{TH+86400} AND src IN (SELECT a FROM m) AND dst NOT IN (SELECT a FROM m) AND dst<>'(multiple)' ORDER BY block_time""").fetchall()
print('transferts hors groupe 24 h',len(rows),sum(r[2] for r in rows)/1e6)
tot_sol=0;tot_q=0
for s,d,q,t,sig in rows:
    r=con.execute(f"SELECT coalesce(sum(sol_lamports),0)/1e9, coalesce(sum(-token_delta),0)/1e12 FROM '{B}/trades.parquet' WHERE owner=? AND kind='swap' AND token_delta<0 AND block_time>=? AND block_time<?",[d,t,TH+86400]).fetchone()
    r2=con.execute(f"SELECT n_tx,kind FROM '{B}/nodes.parquet' WHERE address=?",[d]).fetchone()
    print(time.strftime('%m-%d %H:%M:%S',time.gmtime(t)),s[:8],'>',d[:8],round(q/1e6,3),'dest vend 24h: M',round(r[1],2),'SOL',round(r[0],1),r2)
    tot_sol+=r[0]; tot_q+=r[1]
print('ventes des destinataires dans la fenetre (somme par ligne, peut compter deux fois un destinataire)',tot_q,tot_sol)
ds=sorted({r[1] for r in rows})
rr=con.execute(f"SELECT coalesce(sum(sol_lamports),0)/1e9, coalesce(sum(-token_delta),0)/1e12,count(DISTINCT owner) FROM '{B}/trades.parquet' WHERE owner IN ({','.join(repr(x) for x in ds)}) AND kind='swap' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400}").fetchone()
print('destinataires distincts',len(ds),'ventes 24 h SOL, M, wallets',rr)
print('premier swap du groupe apres la bascule',con.execute(f"SELECT min(block_time),arg_min(owner,block_time),arg_min(signature,block_time) FROM '{B}/trades.parquet' WHERE owner IN (SELECT a FROM m) AND kind='swap' AND block_time>={TH}").fetchone())
print('ventes groupe par tranche 1 h apres',con.execute(f"SELECT (block_time-{TH})//3600 h,round(sum(sol_lamports)/1e9,1),round(sum(-token_delta)/1e12,2),count(DISTINCT owner) FROM '{B}/trades.parquet' WHERE owner IN (SELECT a FROM m) AND kind='swap' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400} GROUP BY 1 ORDER BY 1 LIMIT 8").fetchall())
print('avant Musk swaps groupe ventes',con.execute(f"SELECT round(sum(sol_lamports)/1e9,1),round(sum(-token_delta)/1e12,2),count(*) FROM '{B}/trades.parquet' WHERE owner IN (SELECT a FROM m) AND kind='swap' AND token_delta<0 AND block_time<{TL}").fetchone())
# premier financeur du rapport
ff=dict(con.execute(f"SELECT wallet, arg_min(src, block_time) FROM '{B}/funding_edges.parquet' WHERE wallet IN (SELECT a FROM m) AND NOT is_pool GROUP BY 1").fetchall())
tab={r['wallet']:r for r in csv.DictReader(open(ROOT+'members_table.csv'))}
print('membres sans premier financeur rapport',[x[:8] for x in M if x not in ff])
print('ecarts premier financeur',[(x[:8],ff[x][:8],tab[x]['first_funder'][:8]) for x in ff if ff[x]!=tab[x]['first_funder']])
# grappes du rapport
print('clusters',con.execute(f"SELECT n_wallets,n_token_edges,n_sol_edges,round(dmaga_moved/1e6,1),strength FROM '{REPO}data/wallet_clusters.parquet' ORDER BY n_wallets DESC LIMIT 6").fetchall())
c0=con.execute(f"SELECT members FROM '{REPO}data/wallet_clusters.parquet' ORDER BY n_wallets DESC LIMIT 1").fetchone()[0].split(',')
print('grappe max contient',len(c0),'groupe de 33',len(M&set(c0)),'H3Qs','H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc' in c0,'9Prm','9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq' in c0,'GXZ','GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra' in c0,'C7qE','C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN' in c0)
# HQ2UUt
print('tx HQ2UUt',con.execute(f"SELECT count(*),count(DISTINCT payer),min(bt),max(bt) FROM '{W}/tx.parquet' WHERE contains(programs,'HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx')").fetchone())
print('payeurs HQ2UUt top',con.execute(f"SELECT payer,count(*) FROM '{W}/tx.parquet' WHERE contains(programs,'HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx') GROUP BY 1 ORDER BY 2 DESC LIMIT 8").fetchall())
print('membres avec HQ2UUt',con.execute(f"SELECT payer,count(*) FROM '{W}/tx.parquet' WHERE contains(programs,'HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx') AND payer IN (SELECT a FROM m) GROUP BY 1").fetchall())
# seuils bas : graphe propre avant Musk sous 1 M, depuis les ix
print('hubs nodes',con.execute(f"SELECT address,label,n_counterparts,n_tx FROM '{B}/nodes.parquet' WHERE kind='hub' ORDER BY n_counterparts DESC LIMIT 14").fetchall())
rows=con.execute(f"""SELECT x.src_o,x.dst_o,x.amount FROM '{W}/xfer.parquet' x JOIN (SELECT tid,bt FROM '{W}/tx.parquet' WHERE bt<{TL} AND NOT regexp_matches(programs,'675kPX9|JUP6|JUP4|DCA265|jupoNj|j1o2q|whirLb|LBUZKh|CAMMCz|CPMMoo|6EF8rr|Eo7WjK')) t USING(tid) WHERE x.amount>=10000000000 AND x.src_o IS NOT NULL AND x.dst_o IS NOT NULL""").fetchall()
S5="5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
abse=[r for r in csv.DictReader(open(ROOT+'direct_edges_all.csv')) if r['origin']=='net_absent']
def ts(u):
    import calendar
    return calendar.timegm(time.strptime(u,'%Y-%m-%dT%H:%M:%SZ'))
extra=[(r['src'],r['dst'],int(r['amount'])) for r in abse if ts(r['utc'])<TL]
SVC={"u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w",H}
for th in (0.01,0.05,0.1,0.25,0.5,0.75,1):
    adj=collections.defaultdict(set)
    for a,b,q in rows+extra:
        if q>=th*1e12 and a not in SVC and b not in SVC: adj[a].add(b);adj[b].add(a)
    s={S5};st=[S5]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y not in s: s.add(y);st.append(y)
    print('seuil',th,'M, taille composante 5QhJJc avant Musk',len(s),'noeuds max degre',sorted(((len(adj[x]),x[:8]) for x in s),reverse=True)[:5])
