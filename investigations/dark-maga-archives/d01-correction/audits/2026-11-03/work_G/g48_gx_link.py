#!/usr/bin/env python3
"""Lien série Coinbase et dépôts de GXZvX : deux transferts de DMAGA vers HW5MqvM1 et HKzkNSH2. Contexte, paiement de retour, revente, ce que font les receveurs. Sortie g48.txt"""
import sys, time
sys.path.insert(0, "audits/2026-11-03/work_G")
import duckdb
from g_lib import history, parse
from dmaga.labels import label
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open("audits/2026-11-03/work_G/g48.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
HK = "HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP"; HW = "HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6"; ER = "ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH"; GO = "GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC"
print("== chronologie complète de HKzkNSH2")
for t in history(HK):
    x = parse(t)
    mv = [(a if a != "other" else m[:6], (s or "")[:8], (d or "")[:8], round(r / 10 ** (dc or 0), 3)) for k, a, m, s, d, r, dc in x["moves"] if (a == "SOL" and r >= 10_000_000) or a in ("DMAGA", "USDC", "USDT", "WSOL")]
    if mv: print(" ", iso(x["bt"]), x["sig"][:14], "signe" if HK in x["signers"] else "-", [p[:6] for p in x["progs"]][:3], mv[:5])
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1, "temp_directory": G + "duck"})
con.execute("SET TimeZone='UTC'")
A = f"read_parquet('{G}flows_all.parquet')"; DM = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
for a in (HW,):
    print("== raw/flows, DMAGA de", a[:8])
    for r in con.execute(f"SELECT DISTINCT bt,src,dst,raw,sig FROM {A} WHERE mint='{DM}' AND (src=? OR dst=?) ORDER BY bt LIMIT 30", [a, a]).fetchall(): print(" ", iso(r[0]), r[1][:8], "->", r[2][:8], r[3] / 1e6, r[4])
for a, b in ((ER, HW), (GO, HK)):
    print("== échanges entre", a[:8], "et", b[:8], ", toutes dates (net et raw/flows)")
    for r in con.execute(f"SELECT DISTINCT bt,src,dst,mint,raw,sig FROM {A} WHERE (src=? AND dst=?) OR (src=? AND dst=?) ORDER BY bt", [a, b, b, a]).fetchall(): print(" ", iso(r[0]), r[1][:8], "->", r[2][:8], r[3][:5], r[4], r[5])
    t0 = None
    for t in history(a):
        x = parse(t)
        for k, ass, m, s, d, rw, dc in x["moves"]:
            if s == a and d == b and ass == "DMAGA": t0 = x["bt"]; print("   transfert", iso(x["bt"]), rw / 1e6, x["sig"], "signataires", [q[:8] for q in x["signers"]], "pure", x["pure"])
    print("   SOL ou USD de", b[:8], "vers", a[:8], "dans 7 j :", con.execute(f"SELECT count(*),sum(raw) FROM (SELECT DISTINCT sig,raw FROM {A} WHERE src=? AND dst=? AND bt BETWEEN ? AND ? AND mint<>'{DM}')", [b, a, t0 or 0, (t0 or 0) + 7 * 86400]).fetchone())
    print("   solde de jetons de", a[:8], "dans les tx proches : ventes dans ±1 h")
    rr = con.execute(f"SELECT DISTINCT bt,src,dst,raw,sig FROM {A} WHERE mint='{DM}' AND (src=? OR dst=?) AND bt BETWEEN ? AND ? ORDER BY bt", [a, a, (t0 or 0) - 3600, (t0 or 0) + 3600]).fetchall()
    for r in rr[:10]: print("    ", iso(r[0]), r[1][:8], "->", r[2][:8], round(r[3] / 1e6), r[4][:12])
