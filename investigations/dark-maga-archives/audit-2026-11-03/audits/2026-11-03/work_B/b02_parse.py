"""Auditeur B, aveugle : parseur de swaps indépendant, en flux, par pool, depuis raw/ctrl_tx/<pool>/p*.jsonl.gz.
Écrit un parquet par token dans audits_work/B/tok/ et une ligne de comptes par token dans b02_stats.jsonl.
Reprise : un token dont le parquet existe est sauté.

Règles du plan appliquées :
 - swap = variations de sens opposés des deux vaults (mint et WSOL), lues dans pre/postTokenBalances ;
 - bénéficiaire = owner des jetons, agrégé par owner ; parts < 5 % de |dT| écartées et comptées ;
 - owner non signataire dont le jeton et un autre mint varient en sens opposés : écarté et compté ;
 - transactions réussies seulement ;
 - chaîne : pre(vault_sol, tx i+1) == post(vault_sol, tx i), dans l'ordre (slot, transactionIndex).
Choix (ambiguïtés du plan, voir notes) :
 - SOL d'une ligne = part × |dS| avec part = |delta owner| / |dT|, plafonnée, normalisée si la somme dépasse 1 ;
 - une ligne = (transaction, owner).
"""
import gzip, json, sys, time, os
from array import array
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
HERE = Path(__file__).parent
WSOL = "So11111111111111111111111111111111111111112"
OUTDIR = EXT / "audits_work/B/tok"
STATS = HERE / "b02_stats.jsonl"
MIN_SHARE = 0.05


def balances(lst, keys):
    """accountIndex -> (pubkey, mint, owner, amount int, decimals)"""
    out = {}
    for b in lst or []:
        i = b["accountIndex"]
        t = b["uiTokenAmount"]
        out[i] = (keys[i]["pubkey"], b["mint"], b.get("owner"), int(t["amount"]), t["decimals"])
    return out


def parse_tx(tx, mint, vault_sol, vault_tok, c):
    """Rend (chain, rows). chain = (pre, post, decimals_tok, res_tok_post) si le vault SOL figure dans les soldes, sinon None.
    rows = liste de (owner, side, lamports, tok_raw). side=+1 achat, -1 vente. Compteurs dans c."""
    m = tx["meta"]
    c["tx"] += 1
    if m.get("err") is not None:
        c["tx_err"] += 1
        return None, []
    keys = tx["transaction"]["message"]["accountKeys"]
    pre = balances(m.get("preTokenBalances"), keys)
    post = balances(m.get("postTokenBalances"), keys)
    pre_s = post_s = pre_t = post_t = None
    dec = None
    for d, is_post in ((pre, False), (post, True)):
        for i, (pk, mt, ow, am, de) in d.items():
            if pk == vault_sol:
                if is_post: post_s = am
                else: pre_s = am
            elif pk == vault_tok:
                dec = de
                if is_post: post_t = am
                else: pre_t = am
    if pre_s is None and post_s is None:
        c["tx_sans_vault_sol"] += 1
        return None, []
    pre_s = pre_s or 0; post_s = post_s or 0
    pre_t = pre_t or 0; post_t = post_t or 0
    chain = (pre_s, post_s, dec if dec is not None else -1, post_t, pre_t)
    dS = post_s - pre_s; dT = post_t - pre_t
    if dS == 0 or dT == 0 or (dS > 0) == (dT > 0):
        if dS != 0 or dT != 0:
            c["tx_vaults_meme_sens_ou_un_seul"] += 1
        return chain, []
    c["swap"] += 1
    side = 1 if dS > 0 else -1  # le vault reçoit du SOL : achat
    signers = {k["pubkey"] for k in keys if k.get("signer")}
    # delta par (owner, mint), hors comptes des vaults de ce pool
    delta = {}
    for d, sg in ((pre, -1), (post, 1)):
        for i, (pk, mt, ow, am, de) in d.items():
            if pk == vault_sol or pk == vault_tok:
                continue
            if ow is None:
                if mt == mint: c["owner_absent"] += 1
                continue
            key = (ow, mt)
            delta[key] = delta.get(key, 0) + sg * am
    # jetons : achat = owners qui gagnent ; vente = owners qui perdent
    cand = []
    absT = abs(dT)
    for (ow, mt), v in delta.items():
        if mt != mint or v == 0 or (v > 0) != (side > 0):
            continue
        share = abs(v) / absT
        if share < MIN_SHARE:
            c["part_sous_5pct"] += 1
            c["part_sous_5pct_sum"] += share
            continue
        if ow not in signers:
            opposite = any(mt2 != mint and v2 != 0 and (v2 > 0) != (v > 0) for (ow2, mt2), v2 in delta.items() if ow2 == ow)
            if opposite:
                c["nonsign_oppose"] += 1
                c["nonsign_oppose_part"] += share
                continue
        cand.append((ow, share))
    if not cand:
        c["swap_sans_beneficiaire"] += 1
        return chain, []
    tot = sum(s for _, s in cand)
    if tot > 1.0:
        c["swap_parts_sup_1"] += 1
        cand = [(o, s / tot) for o, s in cand]
    if len(cand) > 1:
        c["swap_multi_benef"] += 1
    rows = [(o, side, s * abs(dS), s * absT) for o, s in cand]
    return chain, rows


def _test():
    def C():
        import collections
        return collections.Counter()
    def bal(i, mint, owner, amt, dec=6):
        return {"accountIndex": i, "mint": mint, "owner": owner, "uiTokenAmount": {"amount": str(amt), "decimals": dec}}
    keys = [{"pubkey": "payer", "signer": True}, {"pubkey": "VS", "signer": False}, {"pubkey": "VT", "signer": False},
            {"pubkey": "ata", "signer": False}, {"pubkey": "fee", "signer": False}, {"pubkey": "venueT", "signer": False}, {"pubkey": "venueS", "signer": False}]
    def tx(pre, post, err=None):
        return {"meta": {"err": err, "preTokenBalances": pre, "postTokenBalances": post}, "transaction": {"message": {"accountKeys": keys}}}
    # achat simple, 2 % de frais à un collecteur : ligne unique, part 98 %
    t = tx([bal(1, WSOL, "A", 1000, 9), bal(2, "M", "A", 10000)], [bal(1, WSOL, "A", 1100, 9), bal(2, "M", "A", 9000), bal(3, "M", "payer", 980), bal(4, "M", "col", 20)])
    c = C(); ch, r = parse_tx(t, "M", "VS", "VT", c)
    assert ch[:2] == (1000, 1100) and len(r) == 1 and r[0][0] == "payer" and r[0][1] == 1 and abs(r[0][2] - 98) < 1e-9 and c["part_sous_5pct"] == 1
    # vente
    t = tx([bal(1, WSOL, "A", 1000, 9), bal(2, "M", "A", 9000), bal(3, "M", "payer", 500)], [bal(1, WSOL, "A", 900, 9), bal(2, "M", "A", 9500)])
    c = C(); ch, r = parse_tx(t, "M", "VS", "VT", c)
    assert r == [("payer", -1, 100.0, 500.0)]
    # routage : réserve d'une autre venue, non signataire, jeton et WSOL opposés : écartée
    t = tx([bal(1, WSOL, "A", 1000, 9), bal(2, "M", "A", 9000), bal(5, "M", "venue", 100), bal(6, WSOL, "venue", 5000, 9)],
           [bal(1, WSOL, "A", 1100, 9), bal(2, "M", "A", 8000), bal(5, "M", "venue", 1100), bal(6, WSOL, "venue", 4900, 9)])
    c = C(); ch, r = parse_tx(t, "M", "VS", "VT", c)
    assert r == [] and c["nonsign_oppose"] == 1 and c["swap_sans_beneficiaire"] == 1
    # les deux réserves montent (ajout de liquidité) : pas de swap
    t = tx([bal(1, WSOL, "A", 1000, 9), bal(2, "M", "A", 9000)], [bal(1, WSOL, "A", 1100, 9), bal(2, "M", "A", 9100)])
    c = C(); ch, r = parse_tx(t, "M", "VS", "VT", c)
    assert r == [] and c["swap"] == 0
    # échec : ignoré
    c = C(); ch, r = parse_tx(tx([], [], err={"x": 1}), "M", "VS", "VT", c)
    assert ch is None and c["tx_err"] == 1
_test()


def pool_info(pools):
    want = set(pools)
    out = {}
    for line in open(EXT / "data/controls/migrations.jsonl"):
        r = json.loads(line)
        if r["pool"] in want:
            out[r["pool"]] = r
    return out


def process(pool, info):
    import collections, numpy as np
    import pyarrow as pa, pyarrow.parquet as pq
    out = OUTDIR / f"{pool}.parquet"
    if out.exists():
        return False
    t0 = time.time()
    d = EXT / "raw/ctrl_tx" / pool
    files = sorted(x for x in os.listdir(d) if x.endswith(".jsonl.gz") and not x.startswith("._"))
    cur = json.loads((d / "cursor.json").read_text())
    mint, vs, vt = info["mint"], info["vault_sol"], info["vault_token"]
    c = collections.Counter()
    wid = {}
    # colonnes compactes
    r_slot, r_idx, r_time, r_side, r_w = array("q"), array("i"), array("q"), array("b"), array("i")
    r_sol, r_tok = array("d"), array("d")
    # chaîne : toutes les tx qui touchent le vault SOL
    t_slot, t_idx, t_time, t_pre, t_post, t_pret, t_postt = array("q"), array("i"), array("q"), array("q"), array("q"), array("q"), array("q")
    dec_seen = collections.Counter()
    lines = 0
    last = (-1, -1); non_mono = 0
    sigs_first = None
    for fn in files:
        with gzip.open(d / fn, "rt") as f:
            for line in f:
                lines += 1
                tx = json.loads(line)
                key = (tx["slot"], tx["transactionIndex"])
                if key < last: non_mono += 1
                last = key
                ch, rows = parse_tx(tx, mint, vs, vt, c)
                if ch is not None:
                    t_slot.append(key[0]); t_idx.append(key[1]); t_time.append(tx["blockTime"])
                    t_pre.append(ch[0]); t_post.append(ch[1]); t_pret.append(ch[4]); t_postt.append(ch[3])
                    dec_seen[ch[2]] += 1
                for ow, side, sol, tok in rows:
                    r_slot.append(key[0]); r_idx.append(key[1]); r_time.append(tx["blockTime"]); r_side.append(side)
                    r_w.append(wid.setdefault(ow, len(wid))); r_sol.append(sol); r_tok.append(tok)
    # chaîne de soldes
    ts = np.frombuffer(t_slot, dtype=np.int64); ti = np.frombuffer(t_idx, dtype=np.int32)
    order = np.lexsort((ti, ts))
    pre = np.frombuffer(t_pre, dtype=np.int64)[order]; post = np.frombuffer(t_post, dtype=np.int64)[order]
    breaks = int((pre[1:] != post[:-1]).sum()) if len(pre) > 1 else 0
    tm = np.frombuffer(t_time, dtype=np.int64)[order]
    pret = np.frombuffer(t_pret, dtype=np.int64)[order]; postt = np.frombuffer(t_postt, dtype=np.int64)[order]
    breaks_t = int((pret[1:] != postt[:-1]).sum()) if len(pret) > 1 else 0
    dup = int(((ts[order][1:] == ts[order][:-1]) & (ti[order][1:] == ti[order][:-1])).sum()) if len(order) > 1 else 0
    first_break = None
    if breaks:
        k = int(np.nonzero(pre[1:] != post[:-1])[0][0])
        first_break = {"t": int(tm[k + 1]), "attendu": int(post[k]), "lu": int(pre[k + 1])}
    # écrit lignes + réserves dans le même parquet, deux fichiers
    wallets = [None] * len(wid)
    for k, v in wid.items():
        wallets[v] = k
    tab = pa.table({"slot": np.frombuffer(r_slot, dtype=np.int64), "idx": np.frombuffer(r_idx, dtype=np.int32), "time": np.frombuffer(r_time, dtype=np.int64),
                    "side": np.frombuffer(r_side, dtype=np.int8), "w": np.frombuffer(r_w, dtype=np.int32), "sol": np.frombuffer(r_sol), "tok": np.frombuffer(r_tok)}) if len(r_slot) else pa.table({"slot": pa.array([], pa.int64()), "idx": pa.array([], pa.int32()), "time": pa.array([], pa.int64()), "side": pa.array([], pa.int8()), "w": pa.array([], pa.int32()), "sol": pa.array([], pa.float64()), "tok": pa.array([], pa.float64())})
    tmp = out.with_suffix(".tmp")
    pq.write_table(tab, tmp)
    res = pa.table({"slot": ts[order], "idx": ti[order], "time": tm, "pre_s": pre, "post_s": post, "pre_t": pret, "post_t": postt})
    resf = OUTDIR / f"{pool}.res.parquet"
    pq.write_table(res, resf)
    wf = OUTDIR / f"{pool}.wallets.txt"
    wf.write_text("\n".join(wallets))
    os.replace(tmp, out)
    st = {"pool": pool, "mint": mint, "created": info["created"], "lines": lines, "cursor_n": cur.get("n"), "cursor_complete": cur.get("complete"), "cursor_filter": cur.get("filters"),
          "non_mono": non_mono, "dups": dup, "chain_breaks": breaks, "chain_breaks_tok": breaks_t, "first_break": first_break, "decimals": {str(k): v for k, v in dec_seen.items()},
          "rows": len(r_slot), "wallets": len(wid), "counts": dict(c), "secs": round(time.time() - t0, 1)}
    with open(STATS, "a") as fs:
        fs.write(json.dumps(st) + "\n")
    print(pool[:10], lines, "tx", len(r_slot), "lignes", "ruptures", breaks, "s", st["secs"], flush=True)
    return True


if __name__ == "__main__":
    OUTDIR.mkdir(parents=True, exist_ok=True)
    root = EXT / "raw/ctrl_tx"
    pools = sorted(x for x in os.listdir(root) if not x.startswith("._"))
    if len(sys.argv) > 1 and sys.argv[1] == "rev":  # 2e processus : part de la fin, s'arrête au premier token déjà fait
        pools = pools[::-1]
    elif len(sys.argv) > 1 and sys.argv[1] != "all":
        pools = sys.argv[1:]
    info = pool_info(pools)
    done = 0
    for p in pools:
        if process(p, info[p]):
            done += 1
    print("fini", done, "sur", len(pools), flush=True)
