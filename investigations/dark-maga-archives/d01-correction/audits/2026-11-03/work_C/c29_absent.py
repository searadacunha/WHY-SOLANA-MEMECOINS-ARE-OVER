import csv,collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
rows=list(csv.DictReader(open(ROOT+'flows_absent_raw_1M.csv')))
c=collections.Counter(); 
for r in rows: c[(r['from_u'][:8],r['to_u'][:8])]+=1
print(len(rows),c.most_common(40))
print('to AtZj',[ (r['from_u'],int(r['amount'])/1e12,r['bt']) for r in rows if r['to_u'].startswith('AtZjv3Du')])
