#!/usr/bin/env python3
"""Imprime le detail d'une transaction d'une graine depuis le brut telecharge. usage: c14_tx.py <wallet> <prefixe_sig>"""
import gzip,json,sys
w,pre=sys.argv[1],sys.argv[2]
hits=[]
for l in gzip.open(f"/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/{w}.jsonl.gz","rt"):
    t=json.loads(l)
    if t['transaction']['signatures'][0].startswith(pre): hits.append(t)
assert len(hits)==1,len(hits)
t=hits[0]; m=t['transaction']['message']; me=t['meta']
print('sig',t['transaction']['signatures'][0]); print('slot',t['slot'],'idx',t.get('transactionIndex'),'bt',t['blockTime'],'fee',me['fee'],'err',me['err'],'version',t.get('version'))
keys=m['accountKeys']
for i,k in enumerate(keys):
    d=me['postBalances'][i]-me['preBalances'][i]
    print(f"  key[{i}] {k['pubkey']} signer={k['signer']} writable={k['writable']} delta={d/1e9:+.9f}")
print('ins:')
for i in m['instructions']:
    print('  ',i.get('program'),i.get('programId'),json.dumps(i.get('parsed') or {'accounts':len(i.get('accounts',[])),'data':(i.get('data') or '')[:40]})[:500])
for g in me.get('innerInstructions') or []:
    for i in g['instructions']:
        print('   inner',g['index'],i.get('program'),i.get('programId')[:12],json.dumps(i.get('parsed') or {})[:220])
print('log:',[x for x in (me.get('logMessages') or []) if 'Instruction' in x or 'Memo' in x][:20])
print('pre',[(keys[b['accountIndex']]['pubkey'],b['owner'],b['mint'][:8],b['uiTokenAmount']['amount']) for b in me.get('preTokenBalances') or []])
print('post',[(keys[b['accountIndex']]['pubkey'],b['owner'],b['mint'][:8],b['uiTokenAmount']['amount']) for b in me.get('postTokenBalances') or []])
