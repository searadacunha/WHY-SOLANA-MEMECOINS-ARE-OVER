"""S9: every outgoing SOL transfer from Coinbase hot wallets 2 and 3 between 01:20:00Z and 02:05:25Z (mint) on 2024-07-14,
joined with DMAGA pump-phase signers and the repo's first-1000-buyers table. Purpose: base rate for 'CEX-funded fresh wallet' patterns.
Coinbase is an intermediary: a shared withdrawal source never proves common ownership on its own."""
import json, sys, os, datetime, csv
sys.path.insert(0, os.path.dirname(__file__)); from rpc import sigs, tx
here = os.path.join(os.path.dirname(__file__), '..')
HOT = {'GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE': 'Coinbase 3', '2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm': 'Coinbase 2'}
REF = 'fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6'
lo = int(datetime.datetime(2024, 7, 14, 1, 20, tzinfo=datetime.UTC).timestamp()); hi = 1720922725
R = {r['wallet']: r for r in csv.DictReader(open(os.path.join(here, 'data/repo_first1000_buyers_parsed.csv')))}
P = {}
for r in csv.DictReader(open(os.path.join(here, 'data/pump_phase_txs.csv'))): P.setdefault(r['signer'], r)
out = []
for hw, label in HOT.items():
    s, _ = sigs(hw, before=REF, max_pages=12)
    win = [x for x in s if lo <= x['blockTime'] < hi and x['err'] is None]
    print(label, 'sigs', len(s), 'oldest', datetime.datetime.fromtimestamp(min(x['blockTime'] for x in s), datetime.UTC), 'window', len(win), flush=True)
    for x in win:
        t = tx(x['signature'])
        if not t: continue
        for ix in t['transaction']['message']['instructions']:
            p = ix.get('parsed')
            if isinstance(p, dict) and p.get('type') == 'transfer' and ix.get('program') == 'system' and p['info'].get('source') == hw:
                d = p['info']['destination']
                out.append({'hot_wallet': label, 'utc': datetime.datetime.fromtimestamp(t['blockTime'], datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                            'dst': d, 'sol': int(p['info']['lamports']) / 1e9, 'signature': x['signature'],
                            'dmaga_pump_first_tx_utc': P.get(d, {}).get('utc'), 'dmaga_pump_first_tx_ok': P.get(d, {}).get('ok'),
                            'repo_first_buy_rank': R.get(d, {}).get('rank'), 'repo_first_buy_utc': R.get(d, {}).get('utc')})
    json.dump(out, open(os.path.join(here, 'data/coinbase23_withdrawals_0120_mint.json'), 'w'), indent=1)
w = csv.DictWriter(open(os.path.join(here, 'data/coinbase23_withdrawals_0120_mint.csv'), 'w', newline=''), fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
hit = [o for o in out if o['dmaga_pump_first_tx_utc'] or o['repo_first_buy_rank']]
print('transfers', len(out), 'recipients touching DMAGA', len(hit))
for o in hit: print(o['hot_wallet'], o['utc'][11:], o['dst'], o['sol'], o['dmaga_pump_first_tx_utc'], o['dmaga_pump_first_tx_ok'], o['repo_first_buy_rank'])
