#!/usr/bin/env python3
"""Vérifications ciblées, sans réseau. (a) ordres inter-chaînes du programme src5qyZH : décodage Borsh des données d'instruction (b) 59L2oxym dans les dépôts témoins (c) expéditeurs d'ET7a91Ee (d) sortie d'Ej5Qv3UB et réception de 8SaiGW le 15/03/2025. Sortie g43.txt, g43_orders.csv."""
import csv, gzip, json, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse, NETC, NETG
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g43.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
AB = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58d(s):
    n = 0
    for c in s: n = n * 58 + AB.index(c)
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\0" * (len(s) - len(s.lstrip("1"))) + b
def b58e(b):
    n = int.from_bytes(b, "big"); s = ""
    while n: n, r = divmod(n, 58); s = AB[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + s
SRC = "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4"
# schéma lu : discriminant 8 octets, give_original_amount u64, offer {chain_id [32], token_address Vec<u8>, amount [32]}, receiver_dst Vec<u8>, external_call Option, give_patch_authority_src [32], allowed_cancel_beneficiary Option [32], order_authority_dst Vec<u8>...
# shortcut: schéma tiré de la structure publique d'un ordre DLN, vérifié seulement par la cohérence des champs (montants, longueurs), pas par un IDL gelé.
def decode(raw):
    p = 8
    give = int.from_bytes(raw[p:p + 8], "little"); p += 8
    chain = int.from_bytes(raw[p:p + 32], "big"); p += 32
    n = int.from_bytes(raw[p:p + 4], "little"); p += 4
    tok = raw[p:p + n]; p += n
    amt = int.from_bytes(raw[p:p + 32], "big"); p += 32
    n2 = int.from_bytes(raw[p:p + 4], "little"); p += 4
    rec = raw[p:p + n2]; p += n2
    return give, chain, tok.hex() if n in (20,) else b58e(tok), amt, ("0x" + rec.hex()) if n2 == 20 else b58e(rec)
T = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv"))}
want = collections.defaultdict(set)
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    if SRC in l["programs"] and l["err"] == "0": want[l["owner"]].add(l["sig"])
w = csv.writer(open(OUT + "g43_orders.csv", "w", newline="")); w.writerow("utc wallet signature instruction give_raw chain_id token_dst take_raw receiver_dst usd_sortis".split())
names = collections.Counter(); rec = collections.defaultdict(lambda: [0.0, set()]); done = set()
for a, S in sorted(want.items()):
    for t in history(a):
        s = t["transaction"]["signatures"][0]
        if s not in S or s in done: continue
        done.add(s)
        logs = [m[len("Program log: Instruction: "):] for m in (t["meta"].get("logMessages") or []) if m.startswith("Program log: Instruction: ")]
        nm = next((x for x in logs if x.startswith("CreateOrder")), None)
        names[nm or (logs[0] if logs else "?")] += 1
        if not nm: continue
        x = parse(t)
        who = x["signers"][0]  # le créateur de l'ordre, jamais le compte d'ordre dont on lit l'historique
        usd = sum(raw / 1e6 for k, asset, mint, src, d, raw, dec in x["moves"] if asset in ("USDC", "USDT") and src == who)
        sol = sum(raw / 1e9 for k, asset, mint, src, d, raw, dec in x["moves"] if asset in ("SOL", "WSOL") and src == who and raw > 2_000_000_0)
        for i in t["transaction"]["message"]["instructions"]:
            if i.get("programId") == SRC and i.get("data"):
                try:
                    g, ch, tok, amt, r = decode(b58d(i["data"]))
                except Exception as e:
                    print("décodage impossible", s, repr(e)[:80]); continue
                if ch > 10**9 or ch == 0: print("  champ chaîne incohérent, ignoré", s[:16], ch); continue
                w.writerow([iso(x["bt"]), who, s, nm, g, ch, tok, amt, r, round(usd, 2)])
                rec[(r, ch)][0] += g / 1e6; rec[(r, ch)][1].add(who)
                print(" ", iso(x["bt"]), who[:8], "donne", g, "USD lus", round(usd, 2), "SOL", round(sol, 3), "chaîne", ch, "jeton", tok[:44], "demande", amt, "receveur", r, s[:16])
print("instructions vues", names.most_common(8))
print("receveurs", [(k[0], k[1], round(v[0], 2), sorted(x[:8] for x in v[1])) for k, v in sorted(rec.items(), key=lambda kv: -kv[1][0])])
# (b) 59L2oxym dans les témoins
A59 = "59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h"; dep59 = collections.Counter(); amt59 = []; sen = collections.defaultdict(set)
for l in gzip.open(NETC + "ctrl_deposits.jsonl.gz", "rt"):
    j = json.loads(l); x = j["x"]; tt = j["tx"]
    seq = list(tt["transaction"]["message"]["instructions"])
    for g in tt["meta"].get("innerInstructions") or []: seq += g["instructions"]
    for i in seq:
        p = i.get("parsed")
        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["destination"] == x:
            if p["info"]["source"] == A59: dep59[x] += 1; amt59.append(int(p["info"]["lamports"]))
            sen[p["info"]["source"]].add(x)
print("59L2oxym : dépôts témoins alimentés", len(dep59), "versements", sum(dep59.values()), "montants lamports", sorted(amt59)[:6], sorted(amt59)[-3:])
print("adresses les plus communes parmi les expéditeurs des dépôts témoins", [(k, label(k), len(v)) for k, v in sorted(sen.items(), key=lambda kv: -len(kv[1]))[:8]])
for dep in ("Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME", "AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1", "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL", "H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi"):
    L = []
    for t in history(dep):
        x = parse(t)
        for k, asset, mint, s, d, raw, dc in x["moves"]:
            if s == A59 and d == dep: L.append((iso(x["bt"]), raw))
    print("  59L2oxym vers", dep[:8], L[:8])
# (c) ET7a91Ee
E = "ET7a91EepfVmKgFdHA6vrxgb1LZtjfKK13ZxCJFgQ98E"
T9 = {r["sender"] for r in csv.DictReader(open(OUT + "g30_in.csv".replace("g30_in", "g30_in")))} if False else set()
caw = set(); dep9 = set()
for r in csv.DictReader(open(OUT + "g30_in.csv")):
    if r["depot"].startswith("Caw4"): caw.add(r["sender"])
    if r["depot"].startswith("9W9b"): dep9.add(r["sender"])
snd = collections.Counter(); t21 = []
for t in history(E):
    x = parse(t)
    for k, asset, mint, s, d, raw, dc in x["moves"]:
        if asset == "SOL" and d == E and s != E and raw >= 1_000_000:
            snd[s] += raw
            if iso(x["bt"]).startswith("2025-08-21"): t21.append((iso(x["bt"])[11:], s[:8], raw / 1e9))
print("ET7a91Ee : expéditeurs >=0,001 SOL", len(snd), "dont 9W9b", len(set(snd) & dep9), "dont Caw4", len(set(snd) & caw), "dont l'un ou l'autre", len(set(snd) & (dep9 | caw)), "SOL", round(sum(snd.values()) / 1e9, 3))
print("  le 21/08/2025 : ", len(t21), t21[:6], t21[-3:])
# (d)
for A, pat in (("Ej5Qv3UBQYTuX1dnJ5Fvgx8H9JUSZ6zWgqyDhPzPCwgA", None), ):
    for t in history(A):
        x = parse(t)
        mv = [(asset if asset != "other" else mint[:6], (s or "")[:10], (d or "")[:10], round(raw / 10 ** (dc or 0), 3)) for k, asset, mint, s, d, raw, dc in x["moves"] if asset != "SOL" or raw > 1000000]
        if mv: print("  Ej5Qv3UB", iso(x["bt"]), x["sig"][:18], "signe", A in x["signers"], [p[:10] for p in x["progs"]], mv[:5])
for t in history("8SaiGWJnpcMNbnqa84op76MuRVkJPx4uZN77mZDb9g5F"):
    if iso(t["blockTime"]).startswith("2025-03-15 07:5"):
        x = parse(t)
        print("  8SaiGW", iso(x["bt"]), x["sig"], "signataires", [q[:8] for q in x["signers"]], [p[:10] for p in x["progs"]], [(asset if asset != "other" else mint[:6], (s or "")[:10], (d or "")[:10], round(raw / 10 ** (dc or 0), 3)) for k, asset, mint, s, d, raw, dc in x["moves"] if asset != "SOL" or raw > 1000000][:6])
