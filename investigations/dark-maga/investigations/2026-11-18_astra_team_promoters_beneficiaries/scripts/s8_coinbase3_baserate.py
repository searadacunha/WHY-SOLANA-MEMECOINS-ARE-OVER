"""S8: base rate of Coinbase 3 (GJRs4F…) 0.5-SOL withdrawals around the creator's funding (01:32:23Z) and GoPCTrS3's (01:33:05Z).
Pages the hot wallet backwards from G41v's first pre-mint transfer (01:46:23Z), keeps 01:30:00–01:36:00Z, decodes each tx."""
import json, sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__)); from rpc import sigs, tx
here = os.path.join(os.path.dirname(__file__), '..')
CB3 = 'GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE'
REF = '2raMmNDhdkps29twoAGY8XwVuWDJX5rhnuyb444MKqKXcfRAzkdBqgGL7uoUqUVbiNjRpprutBj439VLhcvzoC4h'
lo = int(datetime.datetime(2024, 7, 14, 1, 30, tzinfo=datetime.UTC).timestamp()); hi = lo + 360
out = []; before = REF
s, _ = sigs(CB3, before=REF, max_pages=8)
win = [x for x in s if lo <= x['blockTime'] < hi and x['err'] is None]
print('sigs fetched', len(s), 'oldest', datetime.datetime.fromtimestamp(min(x['blockTime'] for x in s), datetime.UTC), 'in window', len(win), flush=True)
for x in win:
    t = tx(x['signature'])
    if not t: continue
    for ix in t['transaction']['message']['instructions']:
        p = ix.get('parsed')
        if isinstance(p, dict) and p.get('type') == 'transfer' and ix.get('program') == 'system' and p['info'].get('source') == CB3:
            out.append({'utc': datetime.datetime.fromtimestamp(t['blockTime'], datetime.UTC).strftime('%H:%M:%S'), 'dst': p['info']['destination'],
                        'sol': int(p['info']['lamports']) / 1e9, 'signature': x['signature']})
json.dump({'window_utc': ['2024-07-14T01:30:00Z', '2024-07-14T01:36:00Z'], 'n_sigs_window': len(win), 'transfers': out}, open(os.path.join(here, 'data/coinbase3_withdrawals_0130_0136.json'), 'w'), indent=1)
half = [o for o in out if abs(o['sol'] - 0.5) < 1e-9]
print('transfers', len(out), 'exactly 0.5 SOL', len(half), [(o['utc'], o['dst'][:6]) for o in half])
