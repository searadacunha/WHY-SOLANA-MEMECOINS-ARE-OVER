"""S10: DMAGA and SOL flows of the wallets funded in the same Coinbase-3 batch as the creator (01:32:23–01:34:15Z),
from 2024-07-14 to 2024-08-31: buys, sells, token transfers and SOL transfers to named addresses. Decoded offline from cached RPC."""
import json, sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__)); from rpc import sigs, tx
here = os.path.join(os.path.dirname(__file__), '..')
MINT = '7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump'
W = ['GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC', 'AFDkwJXJPCkZUjGo4mrrRZY53xU1vMSvXsyQiKdEZN93', 'EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa']
lo, hi = 1720922725 - 3600, int(datetime.datetime(2024, 8, 31, tzinfo=datetime.UTC).timestamp())
out = {}
for w in W:
    s, complete = sigs(w, max_pages=6)
    win = sorted([x for x in s if lo <= x['blockTime'] <= hi], key=lambda x: x['slot'])
    rows = []
    for x in win[:120]:
        t = tx(x['signature'])
        if not t: continue
        m = t['meta']; keys = [k['pubkey'] for k in t['transaction']['message']['accountKeys']]
        pre = {(b['owner'], b['mint']): float(b['uiTokenAmount']['uiAmountString'] or 0) for b in m.get('preTokenBalances') or []}
        post = {(b['owner'], b['mint']): float(b['uiTokenAmount']['uiAmountString'] or 0) for b in m.get('postTokenBalances') or []}
        dtok = post.get((w, MINT), 0) - pre.get((w, MINT), 0)
        others = {o: post.get((o, MINT), 0) - pre.get((o, MINT), 0) for (o, mm) in set(pre) | set(post) if mm == MINT and o != w}
        i = keys.index(w) if w in keys else None
        dsol = (m['postBalances'][i] - m['preBalances'][i]) / 1e9 if i is not None else None
        ins = t['transaction']['message']['instructions'] + [ix for g in (m.get('innerInstructions') or []) for ix in g['instructions']]
        sol_tx = [(ix['parsed']['info'].get('source'), ix['parsed']['info'].get('destination'), int(ix['parsed']['info'].get('lamports', 0)) / 1e9)
                  for ix in ins if isinstance(ix.get('parsed'), dict) and ix.get('program') == 'system' and ix['parsed'].get('type') == 'transfer'
                  and w in (ix['parsed']['info'].get('source'), ix['parsed']['info'].get('destination')) and int(ix['parsed']['info'].get('lamports', 0)) >= 1_000_000]
        rows.append({'utc': datetime.datetime.fromtimestamp(t['blockTime'], datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'), 'signature': x['signature'],
                     'ok': m['err'] is None, 'signer': keys[0], 'dmaga_delta': dtok, 'sol_delta': dsol, 'dmaga_counterparties': {k: v for k, v in others.items() if abs(v) > 0},
                     'sol_transfers': sol_tx})
    out[w] = {'n_sigs_total_seen': len(s), 'history_complete': complete, 'n_in_window': len(win), 'decoded': len(rows), 'rows': rows}
    print(w[:8], len(s), complete, len(win), flush=True)
json.dump(out, open(os.path.join(here, 'data/coinbase3_batch_siblings_flows.json'), 'w'), indent=1)
