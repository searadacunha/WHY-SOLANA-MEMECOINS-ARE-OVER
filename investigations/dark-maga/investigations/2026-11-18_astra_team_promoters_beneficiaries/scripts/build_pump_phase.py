"""Build data/pump_phase_txs.csv: every transaction touching the DMAGA mint from creation (02:05:25Z) to 02:16:31Z
(migration 02:15:31Z + 60 s), successful and failed, decoded offline from cached raw RPC responses."""
import json, csv, sys, os, glob, datetime
sys.path.insert(0, os.path.dirname(__file__)); from pumpdecode import summarize
MINT = '7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump'; T0 = 1720922725
here = os.path.join(os.path.dirname(__file__), '..')
sigs = json.load(open(os.path.join(here, 'raw/s3_mint_sigs_create_to_0228.json')))['signatures']
cache = {}
for f in glob.glob(os.path.join(here, 'raw/rpc_cache/getTransaction_*.json')):
    d = json.load(open(f))
    if d.get('result'): cache[d['params'][0]] = d['result']
rows = []
for s in sigs:
    if s['blockTime'] > T0 + 666: continue
    t = cache.get(s['signature'])
    if not t: rows.append({'signature': s['signature'], 'slot': s['slot'], 'missing': True}); continue
    x = summarize(t, MINT)
    ev = x['events'][0] if x['events'] else None
    ix = x['ix'][0] if x['ix'] else None
    rows.append({'signature': x['signature'], 'slot': x['slot'], 'utc': datetime.datetime.fromtimestamp(x['blockTime'], datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                 'delay_s': x['blockTime'] - T0, 'slot_delta': x['slot'] - 277417695, 'signer': x['signer'], 'ok': x['ok'], 'error': x['error'], 'venue': x['venue'],
                 'is_create': x['is_create'], 'kind': (('buy' if ev['is_buy'] else 'sell') if ev else (ix['kind'] if ix else 'other')),
                 'sol_amount': ev['sol_lamports'] / 1e9 if ev else None, 'dmaga_amount': ev['token_raw'] / 1e6 if ev else None,
                 'ix_token_amount': ix['token_amount_raw'] / 1e6 if ix else None, 'ix_sol_limit': ix['sol_limit_lamports'] / 1e9 if ix else None,
                 'signer_sol_delta': x['signer_sol_delta'], 'signer_dmaga_delta': x['signer_dmaga_delta'], 'missing': False})
rows.sort(key=lambda r: (r['slot'], r.get('delay_s') or 0))
keys = list(rows[0].keys())
w = csv.DictWriter(open(os.path.join(here, 'data/pump_phase_txs.csv'), 'w', newline=''), fieldnames=keys); w.writeheader(); w.writerows(rows)
print(len(rows), 'missing', sum(1 for r in rows if r.get('missing')))
