"""S6: sample pump.fun token creations in slots around the DMAGA mint and measure create->first attempt / first successful buy.
Only extracted fields are stored (full blocks are ~2.5 MB each)."""
import json, sys, time, urllib.request
sys.path.insert(0, 'scripts'); from rpc import sigs, tx
RPC = 'https://api.mainnet-beta.solana.com'
PUMP = '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'
START, END, STEP = 277409000, 277426500, 35   # ~ -58 min .. +58 min around slot 277417695
out = []
def getblock(slot):
    b = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getBlock", "params": [slot, {"encoding": "json", "maxSupportedTransactionVersion": 0, "transactionDetails": "full", "rewards": False}]}).encode()
    for k in range(6):
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request(RPC, data=b, headers={'Content-Type': 'application/json'}), timeout=90).read())
            if 'error' in d:
                if d['error'].get('code') in (-32007, -32009): return None
                time.sleep(3 + 2 * k); continue
            return d['result']
        except Exception: time.sleep(4 + 3 * k)
for slot in range(START, END, STEP):
    blk = getblock(slot)
    if not blk: continue
    for t in blk['transactions']:
        keys = t['transaction']['message']['accountKeys']
        logs = t['meta'].get('logMessages') or []
        if PUMP in keys and any('Instruction: Create' in l for l in logs) and t['meta']['err'] is None:
            mint = keys[1]
            out.append({'slot': slot, 'blockTime': blk['blockTime'], 'create_sig': t['transaction']['signatures'][0], 'creator': keys[0], 'mint': mint})
    time.sleep(0.4)
json.dump(out, open('raw/s6_sampled_creates.json', 'w'), indent=1)
print('creates', len(out), flush=True)
res = []
for c in out:
    s, complete = sigs(c['mint'], until=c['create_sig'], max_pages=6)
    s = sorted(s, key=lambda x: (x['slot'], x['blockTime']))
    rec = dict(c, n_sigs_after_create=len(s), complete=complete)
    first_fail = next((x for x in s if x['err'] is not None), None)
    rec['first_failed_delay_s'] = first_fail['blockTime'] - c['blockTime'] if first_fail else None
    rec['first_failed_slot_delta'] = first_fail['slot'] - c['slot'] if first_fail else None
    # first successful non-creator buy: decode earliest successful txs until a buyer != creator found (max 6 decodes)
    rec['first_buy_delay_s'] = None
    for x in [x for x in s if x['err'] is None][:6]:
        t = tx(x['signature'])
        if not t: continue
        signer = t['transaction']['message']['accountKeys'][0]['pubkey']
        logs = t['meta'].get('logMessages') or []
        if signer != c['creator'] and any('Instruction: Buy' in l for l in logs):
            rec['first_buy_delay_s'] = t['blockTime'] - c['blockTime']; rec['first_buy_slot_delta'] = t['slot'] - c['slot']
            rec['first_buy_signer'] = signer; rec['first_buy_sig'] = x['signature']; break
    # number of failed attempts within 60 s
    rec['failed_within_60s'] = sum(1 for x in s if x['err'] is not None and x['blockTime'] - c['blockTime'] <= 60)
    rec['tx_within_60s'] = sum(1 for x in s if x['blockTime'] - c['blockTime'] <= 60)
    res.append(rec); print(json.dumps(rec)[:300], flush=True)
    json.dump(res, open('data/sniper_comparison_sample.json', 'w'), indent=1)
