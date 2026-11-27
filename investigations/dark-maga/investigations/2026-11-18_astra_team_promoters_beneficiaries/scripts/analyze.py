"""Offline derivation of every table of the ASTRA addendum from frozen inputs (no network).
Inputs : evidence/receipts/*.jsonl.gz, data/repo_first1000_buyers_parsed.csv, data/repo_top_realised_parsed.csv,
         data/funding_before_first_buy.json, data/sniper_comparison_sample.json, data/focus_wallets.json.
Outputs: data/derived/*.csv|json. Usage: python3 scripts/analyze.py [--out DIR]"""
import csv, gzip, json, os, sys, datetime, statistics, argparse
sys.path.insert(0, os.path.dirname(__file__)); from pumpdecode import summarize
HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MINT = '7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump'
T0 = 1720922725; CREATE_SLOT = 277417695; MIGRATION = 1720923331
CREATOR = '8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR'; G41V = 'G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E'
CB3 = 'GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE'
def utc(ts): return datetime.datetime.fromtimestamp(ts, datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def load_gz(name):
    with gzip.open(os.path.join(HERE, 'evidence/receipts', name), 'rt', encoding='utf-8') as g:
        return [json.loads(l) for l in g]
def pump_phase():
    rows = []
    for o in load_gz('pump_phase_0205_0216.jsonl.gz'):
        x = summarize(o['result'], MINT)
        ev = x['events'][0] if x['events'] else None; ix = x['ix'][0] if x['ix'] else None
        rows.append({'signature': x['signature'], 'slot': x['slot'], 'utc': utc(x['blockTime']), 'delay_s': x['blockTime'] - T0,
                     'slot_delta': x['slot'] - CREATE_SLOT, 'signer': x['signer'], 'ok': x['ok'], 'error': x['error'], 'venue': x['venue'],
                     'kind': (('buy' if ev['is_buy'] else 'sell') if ev else (ix['kind'] if ix else 'other')),
                     'sol_amount': round(ev['sol_lamports'] / 1e9, 9) if ev else '', 'dmaga_amount': round(ev['token_raw'] / 1e6, 6) if ev else '',
                     'ix_token_amount': round(ix['token_amount_raw'] / 1e6, 6) if ix else '', 'ix_sol_limit': round(ix['sol_limit_lamports'] / 1e9, 9) if ix else ''})
    rows.sort(key=lambda r: (r['slot'], r['delay_s'], r['signature']))
    return rows
def windows(pp, repo):
    out = []
    for lab, s in (('60s', 60), ('5min', 300), ('15min', 900), ('1h', 3600), ('24h', 86400)):
        rec = {'window': lab, 'end_utc': utc(T0 + s)}
        if s <= 666:  # pump.fun curve phase fully covered by our own decode (migration 02:15:31 + 60 s)
            sub = [r for r in pp if r['delay_s'] <= s]
            okb = [r for r in sub if r['ok'] and r['kind'] == 'buy']
            rec.update(source='RPC decode (this addendum), mint-touching txs', tx=len(sub), failed=sum(not r['ok'] for r in sub), successful_buys=len(okb) + 1,
                       distinct_successful_buyers=len({r['signer'] for r in okb} | {CREATOR}), distinct_signers=len({r['signer'] for r in sub} | {CREATOR}),
                       sol_bought=round(sum(float(r['sol_amount']) for r in okb) + 0.201, 3))
        else:
            rec.update(source='repo reports/EARLY_BUYERS.md (first buy per wallet, all venues)', tx='', failed='', successful_buys='', distinct_signers='',
                       distinct_successful_buyers='', sol_bought='')
        sub = [r for r in repo if int(datetime.datetime.strptime(r['utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.UTC).timestamp()) - T0 <= s]
        rec.update(repo_new_buyers=len(sub), repo_first_buy_sol=round(sum(float(r['first_buy_sol']) for r in sub), 3),
                   repo_lifetime_bought_sol=round(sum(float(r['bought_sol_total']) for r in sub), 1), repo_lifetime_realised_sol=round(sum(float(r['realised_sol']) for r in sub), 1))
        out.append(rec)
    return out
def first_buyers(pp, repo, funding, focus, n=25):
    fund = {f['wallet']: f for f in funding}; roles = {f['wallet']: f['roles'] for f in focus}; rp = {r['wallet']: r for r in repo}
    first_attempt, first_ok = {}, {}
    for r in pp:
        first_attempt.setdefault(r['signer'], r)
        if r['ok'] and r['kind'] == 'buy': first_ok.setdefault(r['signer'], r)
    rows = [{'order': 1, 'wallet': CREATOR, 'first_attempt_utc': '2024-07-14T02:05:25Z', 'first_success_utc': '2024-07-14T02:05:25Z', 'slot_delta': 0,
             'sol_spent': 0.201, 'dmaga_M': 7.106, 'failed_before_success': 0}]
    for w, r in first_ok.items():
        fa = first_attempt[w]
        rows.append({'order': 0, 'wallet': w, 'first_attempt_utc': fa['utc'], 'first_success_utc': r['utc'], 'slot_delta': r['slot_delta'],
                     'sol_spent': round(float(r['sol_amount']), 6), 'dmaga_M': round(float(r['dmaga_amount']) / 1e6, 6),
                     'failed_before_success': sum(1 for x in pp if x['signer'] == w and not x['ok'] and x['slot'] <= r['slot'])})
    rows = rows[:n]
    for i, r in enumerate(rows):
        r['order'] = i + 1
        f = fund.get(r['wallet'], {}); last = (f.get('funders') or [None])[-1]
        r['last_funding_before_buy'] = f"{last['utc']} {last['label'] or last['source']} {last['sol']} SOL" if last else ('non observé (historique dense : ' + str(f.get('n_prior_sigs_seen')) + ' sigs, 8 dernières décodées)' if f else '')
        r['roles'] = roles.get(r['wallet'], '')
        x = rp.get(r['wallet'], {})
        r['repo_rank'] = x.get('rank', ''); r['repo_bought_sol_lifetime'] = x.get('bought_sol_total', ''); r['repo_realised_sol'] = x.get('realised_sol', ''); r['repo_residual_M'] = x.get('residual_M', '')
    return rows
def sniper_summary(sample, pp):
    fb = [x['first_buy_delay_s'] for x in sample if x['first_buy_delay_s'] is not None]
    fbs = [x['first_buy_slot_delta'] for x in sample if x.get('first_buy_slot_delta') is not None]
    tx60 = sorted(x['tx_within_60s'] for x in sample); f60 = sorted(x['failed_within_60s'] for x in sample)
    d_tx60 = sum(1 for r in pp if r['delay_s'] <= 60) + 1; d_f60 = sum(1 for r in pp if r['delay_s'] <= 60 and not r['ok'])
    seen = []
    for r in pp:
        if r['signer'] not in seen and r['signer'] != CREATOR: seen.append(r['signer'])
    g = [r for r in pp if r['signer'] == G41V]
    return {'n_tokens': len(sample), 'sampling': 'every 35th slot in [277409000, 277426500) (~±58 min around the DMAGA create slot); pump.fun Create instructions without error',
            'tokens_with_non_creator_buy_in_first_6_successful_txs': len(fb), 'first_buy_delay_s_median': statistics.median(fb),
            'first_buy_delay_s_p90': sorted(fb)[int(0.9 * (len(fb) - 1))], 'first_buy_slot_delta_median': statistics.median(fbs),
            'tx_within_60s_median': statistics.median(tx60), 'failed_within_60s_median': statistics.median(f60),
            'dmaga_tx_within_60s': d_tx60, 'dmaga_tx_within_60s_share_of_sample_below': round(sum(1 for v in tx60 if v < d_tx60) / len(tx60), 3),
            'dmaga_failed_within_60s': d_f60, 'dmaga_failed_within_60s_share_of_sample_below': round(sum(1 for v in f60 if v < d_f60) / len(f60), 3),
            'dmaga_first_non_creator_buy_delay_s': next(r['delay_s'] for r in pp if r['ok'] and r['kind'] == 'buy'),
            'g41v_attempts': [{'utc': r['utc'], 'delay_s': r['delay_s'], 'slot_delta': r['slot_delta'], 'error': r['error'], 'sol_limit': r['ix_sol_limit'],
                               'token_amount': r['ix_token_amount']} for r in g],
            'g41v_rank_among_distinct_non_creator_signers': seen.index(G41V) + 1, 'distinct_non_creator_signers_pump_phase': len(seen)}
HOT = {CB3: 'Coinbase 3', '2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm': 'Coinbase 2'}
def coinbase_batch():
    """All Coinbase 2/3 outgoing system transfers 01:20:00Z-mint, crossed with the repo's 9W9b sender list."""
    senders = {x['wallet'] for x in json.load(open(os.path.join(HERE, 'data/repo_collector_9w9b_senders.json')))['wallets']}
    rows = []
    for o in load_gz('coinbase23_withdrawals_0120_mint.jsonl.gz'):
        t = o['result']
        for ix in t['transaction']['message']['instructions']:
            p = ix.get('parsed')
            if isinstance(p, dict) and p.get('type') == 'transfer' and ix.get('program') == 'system' and p['info'].get('source') in HOT:
                rows.append({'hot_wallet': HOT[p['info']['source']], 'utc': utc(t['blockTime']), 'dst': p['info']['destination'],
                             'sol': int(p['info']['lamports']) / 1e9, 'signature': o['signature'], 'dst_later_sends_to_9W9b': p['info']['destination'] in senders})
    rows.sort(key=lambda r: (r['utc'], r['signature']))
    hits = [r for r in rows if r['dst_later_sends_to_9W9b']]
    by_amount = {}
    for a in (0.5, 1.0, 1.05):
        sub = [r for r in rows if abs(r['sol'] - a) < 1e-9]; by_amount[str(a)] = {'all': len(sub), 'to_9W9b_senders': sum(r['dst_later_sends_to_9W9b'] for r in sub)}
    return rows, hits, by_amount
def main(out):
    os.makedirs(out, exist_ok=True)
    repo = list(csv.DictReader(open(os.path.join(HERE, 'data/repo_first1000_buyers_parsed.csv'))))
    funding = json.load(open(os.path.join(HERE, 'data/funding_before_first_buy.json')))
    focus = json.load(open(os.path.join(HERE, 'data/focus_wallets.json')))['focus']
    sample = json.load(open(os.path.join(HERE, 'data/sniper_comparison_sample.json')))
    pp = pump_phase()
    def wcsv(name, rows):
        w = csv.DictWriter(open(os.path.join(out, name), 'w', newline=''), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    wcsv('pump_phase_txs.csv', pp)
    wcsv('windows_summary.csv', windows(pp, repo))
    wcsv('first_buyers_top25.csv', first_buyers(pp, repo, funding, focus))
    json.dump(sniper_summary(sample, pp), open(os.path.join(out, 'sniper_comparison_summary.json'), 'w'), indent=1)
    rows, hits, by_amount = coinbase_batch()
    json.dump({'n_transfers': len(rows), 'n_distinct_recipients': len({r['dst'] for r in rows}), 'by_round_amount': by_amount,
               'recipients_later_sending_to_9W9b': hits}, open(os.path.join(out, 'coinbase23_9w9b_summary.json'), 'w'), indent=1)
    print('ok', len(pp))
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(HERE, 'data/derived')); main(ap.parse_args().out)
