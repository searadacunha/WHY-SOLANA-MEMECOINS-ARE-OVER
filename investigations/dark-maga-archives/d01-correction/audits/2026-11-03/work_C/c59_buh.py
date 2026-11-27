#!/usr/bin/env python3
"""BuHUkjUy : premiers virements, exacts. 9PrmF8 -> H9Xezqfd. Hx1Uvdg : proprietaire. Sortie c59.out"""
import gzip, json, time, csv
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
def rows(a):
    L=[json.loads(l) for l in gzip.open(NET+a+'.jsonl.gz','rt')]; L.sort(key=lambda t:(t['slot'],t.get('transactionIndex') or 0)); return L
B="BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc"
L=rows(B); print('n',len(L))
for t in L[:6]:
    m=t['transaction']['message']; ks=[k['pubkey'] for k in m['accountKeys']]
    seq=list(m['instructions'])
    for g in t['meta'].get('innerInstructions') or []: seq+=g['instructions']
    tr=[(i['parsed']['info'].get('source'),i['parsed']['info'].get('destination'),i['parsed']['info'].get('lamports') or i['parsed']['info'].get('amount')) for i in seq if isinstance(i.get('parsed'),dict) and i['parsed'].get('type') in('transfer','transferChecked') and i.get('program') in('system',) ]
    print(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t['blockTime'])),t['transaction']['signatures'][0][:14],'payeur',ks[0],tr[:3])
L=rows("8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR")
for t in L:
    if t['transaction']['signatures'][0].startswith('3eNyvVpP5L'):
        for g in t['meta']['innerInstructions']:
            for i in g['instructions']:
                p=i.get('parsed')
                if isinstance(p,dict) and p.get('type')=='createAccount' and p['info'].get('newAccount','').startswith('Hx1Uvdg'):
                    print('Hx1Uvdg proprietaire',p['info']['owner'])
        print([x for x in t['meta']['logMessages'] if 'Instruction' in x][:8])
    if t['transaction']['signatures'][0].startswith('23n9iu1G2R'):
        for i in t['transaction']['message']['instructions']:
            if isinstance(i.get('parsed'),dict): print('98,77 USDC',i['parsed'].get('type'),json.dumps(i['parsed'].get('info'))[:260])
P="9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
L=rows(P); tot={}
for t in L:
    seq=list(t['transaction']['message']['instructions'])
    for g in t['meta'].get('innerInstructions') or []: seq+=g['instructions']
    for i in seq:
        p=i.get('parsed')
        if i.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer' and p['info']['source']==P:
            d=p['info']['destination']; tot[d]=tot.get(d,0)+int(p['info']['lamports'])
print('9PrmF8 dernier',time.strftime('%Y-%m-%d',time.gmtime(L[-1]['blockTime'])),'top sorties',[(k,round(v/1e9,2)) for k,v in sorted(tot.items(),key=lambda x:-x[1])[:5]])
