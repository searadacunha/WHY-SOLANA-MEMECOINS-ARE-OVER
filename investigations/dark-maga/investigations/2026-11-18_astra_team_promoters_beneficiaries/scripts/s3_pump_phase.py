"""S3: all transactions touching the DMAGA mint from creation to just after 02:28:26Z (pump.fun phase + migration)."""
import json, sys, time
sys.path.insert(0, 'scripts'); from rpc import sigs, tx, CALLS
MINT = '7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump'
CREATE = 'fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6'
BEFORE = '5LiTyoCxVPNULBHtKvAY8LkLweP9XvHgFaAacjxj5n93ucsmxUWt4DV9RBBDhq13wTuuoXH1rApcwdoYc1vmh782'
s, complete = sigs(MINT, before=BEFORE, until=CREATE, max_pages=20)
print('sigs', len(s), 'complete', complete, 'oldest', s[-1]['blockTime'] if s else None, flush=True)
json.dump({'mint': MINT, 'before': BEFORE, 'until': CREATE, 'complete': complete, 'signatures': s}, open('raw/s3_mint_sigs_create_to_0228.json', 'w'))
ok = 0
for i, x in enumerate(sorted(s, key=lambda x: (x['slot'], x['signature']))):
    if x['blockTime'] > 1720923331 + 60:  # stop decoding at migration 02:15:31 + 60 s
        continue
    t = tx(x['signature']); ok += 1
    if i % 100 == 0: print(i, CALLS['n'], flush=True)
    time.sleep(0.25)
print('decoded', ok, 'calls', CALLS['n'])
