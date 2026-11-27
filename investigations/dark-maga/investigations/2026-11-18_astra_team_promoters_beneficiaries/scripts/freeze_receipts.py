"""Freeze raw RPC receipts used by this investigation from raw/rpc_cache into evidence/ (gzip JSONL, one object per tx:
{"signature":..., "result": <getTransaction jsonParsed>}), plus individual JSON files for the key transactions."""
import json, glob, gzip, os, csv
here = os.path.join(os.path.dirname(__file__), '..')
cache = {}
for f in glob.glob(os.path.join(here, 'raw/rpc_cache/getTransaction_*.json')):
    d = json.load(open(f))
    if d.get('result'): cache[d['params'][0]] = d['result']
def dump(name, sigs):
    sigs = sorted(set(sigs))
    with gzip.open(os.path.join(here, 'evidence/receipts', name), 'wt', encoding='utf-8') as g:
        for s in sigs:
            if s in cache: g.write(json.dumps({'signature': s, 'result': cache[s]}, sort_keys=True) + '\n')
    return sum(1 for s in sigs if s in cache), len(sigs)
pp = [r['signature'] for r in csv.DictReader(open(os.path.join(here, 'data/pump_phase_txs.csv')))]
print('pump_phase', dump('pump_phase_0205_0216.jsonl.gz', pp))
cb = json.load(open(os.path.join(here, 'data/coinbase23_withdrawals_0120_mint.json')))
print('coinbase', dump('coinbase23_withdrawals_0120_mint.jsonl.gz', [o['signature'] for o in cb]))
fund = json.load(open(os.path.join(here, 'data/funding_before_first_buy.json')))
print('funding', dump('funding_transfers.jsonl.gz', [f['signature'] for r in fund for f in r['funders']]))
sib = json.load(open(os.path.join(here, 'data/coinbase3_batch_siblings_flows.json')))
print('siblings', dump('coinbase3_batch_siblings.jsonl.gz', [r['signature'] for v in sib.values() for r in v['rows']]))
sn = json.load(open(os.path.join(here, 'data/sniper_comparison_sample.json')))
print('sniper_first_buys', dump('sniper_sample_first_buys.jsonl.gz', [x['first_buy_sig'] for x in sn if x.get('first_buy_sig')]))
KEY = {'create_fePxr7ER': 'fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6',
       'g41v_failed_buy_1_5y7rbp2M': '5y7rbp2MPWukH3R1jSHCHvesrGAwyFbfT84RAH7wonyMUqCDoEu13Mi6DSb5pvoHhpzsnofGsrgijjK8avtPuTnG',
       'g41v_failed_buy_2_39nfmzR1': '39nfmzR12cVHaMd2EtoHvTmcNDCKFfKPkbmjXcnRXXLH6o5QmvtTnLJseeDTqegtN65MdttuP5B5qd4T8npEUXfG',
       'g41v_jupiter_buy_5LiTyoCx': '5LiTyoCxVPNULBHtKvAY8LkLweP9XvHgFaAacjxj5n93ucsmxUWt4DV9RBBDhq13wTuuoXH1rApcwdoYc1vmh782',
       'g41v_war_chest_sale_4DDtLbJF': '4DDtLbJF8T9LvrbCgpWrrXq6EHrd1H2dPdm92h9jwwj7NhSZSTpiRdwXS3vE2zBKbArW9GE1oaaAjs5NsLccMVYh'}
for o in cb:
    if abs(o['sol'] - 0.5) < 1e-9 and o['hot_wallet'] == 'Coinbase 3' and o['utc'] >= '2024-07-14T01:32' and o['utc'] <= '2024-07-14T01:34:59':
        KEY[f"coinbase3_0p5_{o['utc'][11:19].replace(':', '')}_{o['dst'][:8]}"] = o['signature']
os.makedirs(os.path.join(here, 'evidence/receipts/key'), exist_ok=True)
idx = {}
for k, s in KEY.items():
    t = cache.get(s)
    if t is None:
        import sys; sys.path.insert(0, os.path.dirname(__file__)); from rpc import tx; t = tx(s)
    json.dump({'signature': s, 'result': t}, open(os.path.join(here, 'evidence/receipts/key', k + '.json'), 'w'), indent=1, sort_keys=True)
    idx[k] = s
json.dump(idx, open(os.path.join(here, 'evidence/receipts/key/INDEX.json'), 'w'), indent=1)
print('key', len(idx))
