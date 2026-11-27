#!/usr/bin/env python3
"""Detail d'une transaction du lot absent, ou liste des tx mediees non j1o2. usage: c30_abs_tx.py <prefixe sig> | list"""
import gzip,json,sys,csv,collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
if sys.argv[1]=='list':
    c=collections.Counter()
    for r in csv.DictReader(open(ROOT+'mediated_edges.csv')):
        ps=[p for p in r['programs'].split('|') if p not in('ComputeBudget111111111111111111111111111111','TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA','ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL','11111111111111111111111111111111')]
        c[','.join(ps)]+=1
        if 'j1o2' not in r['programs']:
            print(r['utc'],r['sig'][:10],r['src'][:8],'>',r['dst'][:8],int(r['amount'])/1e12,'|',','.join(p[:10] for p in ps),r['origin'][:3],'auth',(r['authority'] or '')[:8],'pay',r['payer'][:8])
    print(c.most_common(20)); sys.exit()
for l in gzip.open("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/absent_1M.jsonl.gz","rt"):
    t=json.loads(l)
    if t['transaction']['signatures'][0].startswith(sys.argv[1]):
        m=t['transaction']['message']; me=t['meta']
        print(t['transaction']['signatures'][0],t['blockTime'],me['fee'])
        print([ (k['pubkey'],k['signer']) for k in m['accountKeys']][:12])
        for i in m['instructions']: print(' ',i.get('program'),i.get('programId'),json.dumps(i.get('parsed') or {'n_accounts':len(i.get('accounts',[])),'accounts':i.get('accounts',[])[:6],'data':(i.get('data') or '')[:30]})[:400])
        for g in me.get('innerInstructions') or []:
            for i in g['instructions']: print('  inner',g['index'],i.get('program'),i.get('programId')[:10],json.dumps(i.get('parsed') or {})[:200])
        print([x for x in (me.get('logMessages') or [])][:14])
