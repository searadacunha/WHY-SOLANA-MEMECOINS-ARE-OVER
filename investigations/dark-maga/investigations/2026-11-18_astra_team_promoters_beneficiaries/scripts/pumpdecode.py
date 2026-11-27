"""Offline decoders for pump.fun (program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P, July 2024 layout).
- Buy/Sell instruction args: 8-byte discriminator + amount (u64, token base units, 6 decimals) + max_sol_cost / min_sol_output (u64 lamports).
- TradeEvent ('Program data:' log): disc(8) mint(32) sol_amount(u64) token_amount(u64) is_buy(u8) user(32) timestamp(i64) vsol(u64) vtok(u64).
No network access."""
import base64, struct, hashlib
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58decode(s):
    n = 0
    for c in s: n = n * 58 + B58.index(c)
    full = n.to_bytes((n.bit_length() + 7) // 8, 'big') if n else b''
    pad = len(s) - len(s.lstrip('1'))
    return b'\x00' * pad + full
def b58encode(b):
    n = int.from_bytes(b, 'big'); out = ''
    while n: n, r = divmod(n, 58); out = B58[r] + out
    return '1' * (len(b) - len(b.lstrip(b'\x00'))) + out
PUMP = '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'
DISC_BUY = hashlib.sha256(b'global:buy').digest()[:8]
DISC_SELL = hashlib.sha256(b'global:sell').digest()[:8]
DISC_TRADE_EVENT = hashlib.sha256(b'event:TradeEvent').digest()[:8]
def decode_ix(data_b58):
    raw = b58decode(data_b58)
    if len(raw) >= 24 and raw[:8] in (DISC_BUY, DISC_SELL):
        amount, lim = struct.unpack('<QQ', raw[8:24])
        return {'kind': 'buy' if raw[:8] == DISC_BUY else 'sell', 'token_amount_raw': amount, 'sol_limit_lamports': lim}
    return None
def decode_trade_events(logs):
    out = []
    for l in logs or []:
        if l.startswith('Program data: '):
            try: raw = base64.b64decode(l[len('Program data: '):])
            except Exception: continue
            if raw[:8] == DISC_TRADE_EVENT and len(raw) >= 8 + 32 + 8 + 8 + 1 + 32 + 8:
                o = 8; mint = b58encode(raw[o:o + 32]); o += 32
                sol, tok = struct.unpack('<QQ', raw[o:o + 16]); o += 16
                is_buy = raw[o] == 1; o += 1
                user = b58encode(raw[o:o + 32]); o += 32
                ts, = struct.unpack('<q', raw[o:o + 8])
                out.append({'mint': mint, 'sol_lamports': sol, 'token_raw': tok, 'is_buy': is_buy, 'user': user, 'ts': ts})
    return out
def summarize(t, mint):
    """Summarise one jsonParsed transaction for a given mint."""
    msg = t['transaction']['message']; keys = [k['pubkey'] for k in msg['accountKeys']]
    signer = keys[0]; meta = t['meta']
    ixs = [ix for ix in msg['instructions'] if ix.get('programId') == PUMP]
    inner = [ix for g in (meta.get('innerInstructions') or []) for ix in g['instructions'] if ix.get('programId') == PUMP]
    dec = [d for d in (decode_ix(ix['data']) for ix in ixs + inner if 'data' in ix) if d]
    logs = meta.get('logMessages') or []
    err_name = next((l.split('Error Code: ')[1].split('.')[0] for l in logs if 'Error Code: ' in l), None)
    ev = [e for e in decode_trade_events(logs) if e['mint'] == mint]
    i = keys.index(signer)
    pre = {(b['owner'], b['mint']): float(b['uiTokenAmount']['uiAmountString'] or 0) for b in meta.get('preTokenBalances') or []}
    post = {(b['owner'], b['mint']): float(b['uiTokenAmount']['uiAmountString'] or 0) for b in meta.get('postTokenBalances') or []}
    tok_delta = post.get((signer, mint), 0) - pre.get((signer, mint), 0)
    venue = 'pump' if ixs or inner else ('jupiter' if any('JUP' in k for k in keys) else ('raydium' if '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8' in keys else 'other'))
    is_create = any('Instruction: Create' in l for l in logs) and PUMP in keys
    return {'signature': t['transaction']['signatures'][0], 'slot': t['slot'], 'blockTime': t['blockTime'], 'signer': signer,
            'ok': meta['err'] is None, 'error': err_name or (str(meta['err']) if meta['err'] else None), 'venue': venue, 'is_create': is_create,
            'ix': dec, 'events': ev, 'signer_sol_delta': (meta['postBalances'][i] - meta['preBalances'][i]) / 1e9,
            'signer_dmaga_delta': tok_delta, 'fee_sol': meta['fee'] / 1e9}
