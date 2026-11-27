"""S4: observable direct SOL funding before each wallet's first successful DMAGA buy.
Method: page getSignaturesForAddress backwards from a reference signature just after the first buy (foreign 'before' signatures
are accepted by the RPC), keep txs strictly before the first-buy time, decode the 8 most recent successful ones and the oldest
fetched one; record parsed System transfers whose destination is the wallet. Hubs (CEX, routers) are labelled, never merged."""
import json, csv, sys, os, datetime, bisect
sys.path.insert(0, os.path.dirname(__file__)); from rpc import rpc, sigs, tx
here = os.path.join(os.path.dirname(__file__), '..')
ref = json.load(open(os.path.join(here, 'raw/reference_signatures_repo.json')))
ref += [['5LiTyoCxVPNULBHtKvAY8LkLweP9XvHgFaAacjxj5n93ucsmxUWt4DV9RBBDhq13wTuuoXH1rApcwdoYc1vmh782', 1720924106]]
ref.sort(key=lambda x: x[1]); rts = [r[1] for r in ref]
pp = list(csv.DictReader(open(os.path.join(here, 'data/pump_phase_txs.csv'))))
first_ok = {}
for r in pp:
    if r['ok'] == 'True' and r['kind'] == 'buy' and r['signer'] not in first_ok: first_ok[r['signer']] = int(r['delay_s']) + 1720922725
repo = {r['wallet']: r for r in csv.DictReader(open(os.path.join(here, 'data/repo_first1000_buyers_parsed.csv')))}
focus = json.load(open(os.path.join(here, 'data/focus_wallets.json')))['focus']
order = sorted(first_ok.items(), key=lambda x: x[1])[:25]
wallets = {w: t for w, t in order}
for f in focus:
    w = f['wallet']
    if w in wallets: continue
    if w in first_ok: wallets[w] = first_ok[w]
    elif f['first_buy_utc']:
        wallets[w] = int(datetime.datetime.strptime(f['first_buy_utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.UTC).timestamp())
    else: wallets[w] = None  # never bought in the first-1000 table: funding before mint+24h
LABELS = {'GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE': 'Coinbase 3', 'H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS': 'Coinbase 1',
          '2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm': 'Coinbase 2', '5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9': 'Binance 2',
          '9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM': 'Binance 1', 'AC5RDfQFmDS1deWZos921JfqscXdByf8BKHs5ACWjtW2': 'Bybit',
          'ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ': 'MEXC', '5VCwKtCXgCJ6kit5FybXjvriW3xELsFDhYrPSqtJNmcD': 'OKX',
          'FWznbcNXWQuHTawe9RxvQ2LdCENssh12dsznf4RiouN5': 'Kraken', 'BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6': 'Kucoin'}
out = []
for w, T in wallets.items():
    Tq = T if T else 1720922725 + 86400
    i = bisect.bisect_left(rts, Tq + 1)
    before = ref[i][0] if i < len(ref) else None
    s, complete = sigs(w, before=before, max_pages=3)
    prior = sorted([x for x in s if x['blockTime'] < Tq], key=lambda x: (x['slot'], x['blockTime']))
    rec = {'wallet': w, 'first_buy_ts': T, 'first_buy_utc': datetime.datetime.fromtimestamp(T, datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ') if T else None,
           'n_prior_sigs_seen': len(prior), 'history_complete': complete, 'oldest_seen_utc': None, 'funders': []}
    if prior: rec['oldest_seen_utc'] = datetime.datetime.fromtimestamp(prior[0]['blockTime'], datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    pick = [x for x in prior if x['err'] is None][-8:]
    if prior and prior[0] not in pick: pick = [prior[0]] + pick
    for x in pick:
        t = tx(x['signature'])
        if not t: continue
        ins = t['transaction']['message']['instructions'] + [ix for g in (t['meta'].get('innerInstructions') or []) for ix in g['instructions']]
        for ix in ins:
            p = ix.get('parsed')
            if isinstance(p, dict) and p.get('type') in ('transfer', 'transferWithSeed', 'createAccount') and ix.get('program') == 'system':
                info = p['info']; dst = info.get('destination') or info.get('newAccount'); src = info.get('source')
                lam = int(info.get('lamports', 0))
                if dst == w and lam >= 1_000_000:  # >= 0.001 SOL: dust/poisoning excluded
                    rec['funders'].append({'utc': datetime.datetime.fromtimestamp(t['blockTime'], datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'), 'source': src,
                                           'label': LABELS.get(src), 'sol': lam / 1e9, 'signature': x['signature']})
    out.append(rec); print(w[:8], rec['first_buy_utc'], len(prior), complete, [(f['utc'][11:], f['source'][:6], f['label'], f['sol']) for f in rec['funders']][-4:], flush=True)
    json.dump(out, open(os.path.join(here, 'data/funding_before_first_buy.json'), 'w'), indent=1)
