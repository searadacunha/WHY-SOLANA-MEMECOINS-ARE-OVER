#!/usr/bin/env python3
"""Auditeur C, phase aveugle. Parseur propre : lit full_mint, full_pool, full_venue, full_curve en flux.

Ecrit trois tables plates (gz) dans audits_work/C :
 tx.csv.gz  : tid, sig, slot, txidx, bt, loc (dossier/page:ligne), payer, signers, programmes
 ta.csv.gz  : tid, token_account, owner_pre, owner_post, pre, post  (seulement si solde DMAGA change ou proprietaire change)
 ix.csv.gz  : tid, kind, src_ta, dst_ta, authority, amount, outer_prog, ordre  (instructions SPL touchant un compte DMAGA)
et seeds_local.jsonl.gz : lignes brutes des transactions ou une graine apparait.
Dedoublonne par empreinte 8 octets de la signature. Rien n'est agrege en memoire hors de cet ensemble.
"""
import csv
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
SEEDS = {"8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd",
         "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"}
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
RAW = EXT / "raw"
OUT = EXT / "audits_work" / "C"
TOKEN_KINDS = {"transfer", "transferChecked", "burn", "burnChecked", "mintTo", "mintToChecked", "setAuthority", "closeAccount"}


def pages():
    """(etiquette, chemin) pour chaque page, en excluant les fichiers ._ de macOS."""
    for top in ["full_mint", "full_pool", "full_curve", "full_venue"]:
        root = RAW / top
        for p in sorted(root.glob("p*.jsonl.gz")):
            if not p.name.startswith("._"):
                yield f"{top}/{p.stem[:-6] if False else p.stem}", p
        for d in sorted(x for x in root.iterdir() if x.is_dir() and not x.name.startswith("._")):
            for p in sorted(d.glob("p*.jsonl.gz")):
                if not p.name.startswith("._"):
                    yield f"{top}/{d.name}/{p.stem}", p


def amount_of(info):
    if "amount" in info:
        return int(info["amount"])
    return int(info["tokenAmount"]["amount"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    seen = set()
    ftx = gzip.open(OUT / "tx.csv.gz.tmp", "wt", compresslevel=3, newline="")
    fta = gzip.open(OUT / "ta.csv.gz.tmp", "wt", compresslevel=3, newline="")
    fix = gzip.open(OUT / "ix.csv.gz.tmp", "wt", compresslevel=3, newline="")
    fseed = gzip.open(OUT / "seeds_local.jsonl.gz.tmp", "wt", compresslevel=3)
    wtx, wta, wix = csv.writer(ftx), csv.writer(fta), csv.writer(fix)
    wtx.writerow("tid sig slot txidx bt loc payer signers programs fee".split())
    wta.writerow("tid token_account owner_pre owner_post pre post".split())
    wix.writerow("tid kind src_ta dst_ta authority amount outer_prog ord".split())
    n_lines = n_dupe = n_err = tid = n_nomint = 0
    t0 = time.time()
    for loc, p in pages():
        with gzip.open(p, "rt") as f:
            for ln, line in enumerate(f):
                n_lines += 1
                tx = json.loads(line)
                sig = tx["transaction"]["signatures"][0]
                h = int.from_bytes(hashlib.blake2b(sig.encode(), digest_size=8).digest(), "big")
                if h in seen:
                    n_dupe += 1
                    continue
                seen.add(h)
                meta = tx["meta"]
                if meta.get("err"):
                    n_err += 1
                    continue
                msg = tx["transaction"]["message"]
                akeys = msg["accountKeys"]
                keys = [k["pubkey"] for k in akeys]
                signers = [k["pubkey"] for k in akeys if k["signer"]]
                if SEEDS.intersection(keys):
                    fseed.write(line if line.endswith("\n") else line + "\n")
                pre = {b["accountIndex"]: b for b in meta.get("preTokenBalances") or [] if b["mint"] == MINT}
                post = {b["accountIndex"]: b for b in meta.get("postTokenBalances") or [] if b["mint"] == MINT}
                tid += 1
                progs = []
                for ins in msg["instructions"]:
                    if ins["programId"] not in progs:
                        progs.append(ins["programId"])
                inner = meta.get("innerInstructions") or []
                for grp in inner:
                    for ins in grp["instructions"]:
                        if ins["programId"] not in progs:
                            progs.append(ins["programId"])
                if not pre and not post:
                    n_nomint += 1
                wtx.writerow([tid, sig, tx["slot"], tx.get("transactionIndex"), tx["blockTime"], f"{loc}:{ln}", signers[0],
                              "|".join(signers), "|".join(progs), meta.get("fee")])
                ta_set = set()
                for i in set(pre) | set(post):
                    a, b = pre.get(i), post.get(i)
                    ta = keys[i]
                    ta_set.add(ta)
                    pa = int(a["uiTokenAmount"]["amount"]) if a else 0
                    pb = int(b["uiTokenAmount"]["amount"]) if b else 0
                    oa, ob = (a or {}).get("owner", ""), (b or {}).get("owner", "")
                    if pa != pb or (a and b and oa != ob):
                        wta.writerow([tid, ta, oa, ob, pa, pb])
                # instructions SPL, externes et internes, dans l'ordre d'execution approximatif (outer, inner)
                seq = [(i, -1, ins, ins.get("programId")) for i, ins in enumerate(msg["instructions"])]
                for grp in inner:
                    op = msg["instructions"][grp["index"]]["programId"]
                    for j, ins in enumerate(grp["instructions"]):
                        seq.append((grp["index"], j, ins, op))
                seq.sort(key=lambda r: (r[0], r[1]))
                for i, j, ins, op in seq:
                    if ins.get("program") not in ("spl-token",):
                        continue
                    parsed = ins.get("parsed")
                    if not isinstance(parsed, dict) or parsed.get("type") not in TOKEN_KINDS:
                        continue
                    info, kind = parsed["info"], parsed["type"]
                    if kind in ("transfer", "transferChecked"):
                        s, d = info["source"], info["destination"]
                        if s not in ta_set and d not in ta_set:
                            continue
                        wix.writerow([tid, kind, s, d, info.get("authority") or info.get("multisigAuthority") or "",
                                      amount_of(info), op, f"{i}.{j}"])
                    elif kind in ("burn", "burnChecked", "mintTo", "mintToChecked"):
                        acc = info.get("account")
                        if acc in ta_set:
                            wix.writerow([tid, kind, acc if kind.startswith("burn") else "", "" if kind.startswith("burn") else acc,
                                          info.get("authority") or info.get("mintAuthority") or "", amount_of(info), op, f"{i}.{j}"])
                    elif kind == "setAuthority":
                        acc = info.get("account")
                        if acc in ta_set:
                            wix.writerow([tid, "setAuthority:" + str(info.get("authorityType")), acc, info.get("newAuthority") or "",
                                          info.get("authority") or "", 0, op, f"{i}.{j}"])
                    elif kind == "closeAccount":
                        acc = info.get("account")
                        if acc in ta_set:
                            wix.writerow([tid, kind, acc, info.get("destination") or "", info.get("owner") or "", 0, op, f"{i}.{j}"])
                if n_lines % 100000 == 0:
                    print(f"{time.strftime('%H:%M:%S', time.gmtime())} lignes={n_lines} tid={tid} doublons={n_dupe} err={n_err} sansmint={n_nomint} loc={loc} {time.time()-t0:.0f}s", flush=True)
    for fh in (ftx, fta, fix, fseed):
        fh.close()
    for n in ("tx.csv.gz", "ta.csv.gz", "ix.csv.gz", "seeds_local.jsonl.gz"):
        (OUT / (n + ".tmp")).replace(OUT / n)
    print(f"FIN lignes={n_lines} tid={tid} doublons={n_dupe} err={n_err} sansmint={n_nomint} {time.time()-t0:.0f}s", flush=True)
    # auto-controle : chaque ligne vue est un doublon, une erreur ou une transaction retenue
    assert n_lines == tid + n_dupe + n_err, "lignes perdues"


if __name__ == "__main__":
    sys.exit(main())
