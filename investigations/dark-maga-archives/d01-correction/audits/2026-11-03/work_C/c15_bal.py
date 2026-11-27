#!/usr/bin/env python3
"""Solde SOL du createur et de 5QhJJc autour du virement de 0,032 SOL (post soldes bruts)."""
import gzip,json
for w in ["8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR","5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"]:
    rows=[json.loads(l) for l in gzip.open(f"/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/{w}.jsonl.gz","rt")]
    rows.sort(key=lambda t:(t['slot'],t.get('transactionIndex') or 0))
    for t in rows:
        if 1751700000<=t['blockTime']<=1752500000 or (w[0]=='8' and 1737900000<=t['blockTime']<=1737908000):
            keys=[k['pubkey'] for k in t['transaction']['message']['accountKeys']]
            i=keys.index(w)
            pr=t['meta']['preBalances'][i]/1e9; po=t['meta']['postBalances'][i]/1e9
            ch={x.get('programId')[:6] for x in t['transaction']['message']['instructions']}
            if abs(po-pr)>1e-7 or t['transaction']['message']['accountKeys'][0]['pubkey']==w:
                print(w[:6],time if False else t['blockTime'],t['transaction']['signatures'][0][:12],f"{pr:.6f}->{po:.6f}",t['meta']['fee'],sorted(ch))
