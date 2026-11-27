#!/usr/bin/env python3
"""Test de compte de dépôt, adresse par adresse, depuis son historique. Mêmes grandeurs que C et D : destinations des sorties, signataire, frais, délai, solde après sortie,
expéditeurs réels (au moins 0,001 SOL ou 1 USD stable), part de ces expéditeurs touchant DMAGA (brut relu par D : d01_own) contre témoin 8 sur 1 365.
usage : g22_deposit.py <fichier sortie csv> addr... ; une fiche sur stdout, une ligne par expéditeur dans le csv."""
import csv, json, os, sys, time, statistics as st, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
import duckdb
from g_lib import history, parse, CB, FAM, NETC, NETG
from dmaga.labels import label
iso = lambda t: time.strftime("%Y-%m-%d %H:%M", time.gmtime(t))
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 1, "temp_directory": G + "duck"})
own_cols = [c[0] for c in con.execute(f"DESCRIBE SELECT * FROM '{D}d01_own.parquet'").fetchall()]
roles = {r["wallet"]: r["roles"] for r in csv.DictReader(open("audits/2026-11-03/work_G/targets.csv"))}
def touches(ads):
    if not ads: return set()
    con.execute("CREATE OR REPLACE TEMP TABLE q(a VARCHAR)"); con.executemany("INSERT INTO q VALUES (?)", [[a] for a in ads])
    return {r[0] for r in con.execute(f"SELECT DISTINCT owner FROM '{D}d01_own.parquet' WHERE owner IN (SELECT a FROM q)").fetchall()}
w = csv.writer(open(sys.argv[1], "w", newline="")); w.writerow("depot sender sol usdc usdt dmaga n first last touche_dmaga roles".split())
def lab(x): return CB.get(x) or ("famille CB présumée" if x in FAM else (label(x) or ""))
for A in sys.argv[2:]:
    comp = None
    for d in (NETG, NETC):
        p = d + A + ".cursor.json"
        if os.path.exists(p): comp = json.load(open(p)); break
    sen = collections.defaultdict(lambda: collections.Counter()); dates = {}
    outs = collections.Counter(); outu = collections.Counter(); out_tx = 0; out_self = 0; fees = collections.Counter(); after = []; delays = []; lastin = None; n = 0; first = last = None; prog = collections.Counter(); swaps = 0; outD = collections.Counter(); signers_out = collections.Counter()
    for t in history(A):
        x = parse(t); n += 1; first = first or x["bt"]; last = x["bt"]
        if x["err"]: continue
        for p in x["progs"]: prog[p] += 1
        got_out = False; got_in = False
        for k, asset, mint, s, d_, raw, dec in x["moves"]:
            if d_ == A and s != A:
                if (asset == "SOL" and raw >= 1_000_000) or (asset in ("USDC", "USDT") and raw >= 1_000_000) or (asset == "DMAGA" and raw >= 1_000_000) or asset == "WSOL":
                    sen[s][asset] += raw; sen[s]["n"] += 1; dates.setdefault(s, [x["bt"], x["bt"]])[1] = x["bt"]; got_in = True
            if s == A and d_ != A:
                if asset == "SOL": outs[d_] += raw
                elif asset in ("USDC", "USDT"): outu[d_] += raw
                elif asset == "DMAGA": outD[d_] += raw
                got_out = True
        if got_in: lastin = x["bt"]
        if got_out:
            out_tx += 1; signers_out[";".join(x["signers"])[:44]] += 1
            if A in x["signers"]: out_self += 1; fees[x["fee"]] += 1
            after.append(x["post"].get(A, 0))
            if lastin: delays.append(x["bt"] - lastin)
    ts, tu = sum(outs.values()), sum(outu.values())
    t = touches(list(sen))
    print(f"== {A} lab={lab(A)} tx={n} complet={comp.get('complete') if comp else '?'} {iso(first) if first else ''} -> {iso(last) if last else ''}")
    print(f"   expéditeurs réels {len(sen)} ; touchent DMAGA {len(t)} ; SOL sorti {ts/1e9:.2f} : CB {sum(v for k,v in outs.items() if k in CB)/max(ts,1):.3f} famille {sum(v for k,v in outs.items() if k in FAM)/max(ts,1):.3f} ; USD sorti {tu/1e6:.2f} : CB {sum(v for k,v in outu.items() if k in CB)/max(tu,1):.3f} famille {sum(v for k,v in outu.items() if k in FAM)/max(tu,1):.3f}")
    print(f"   sorties {out_tx} signées par l'adresse {out_self} ; frais {fees.most_common(3)} ; solde après sortie médian {int(st.median(after)) if after else ''} ; délai médian entrée à sortie {int(st.median(delays)) if delays else ''} s ; programmes {[(p[:8],c) for p,c in prog.most_common(4)]}")
    print("   sorties SOL", [(k, lab(k)[:14], round(v/1e9, 2)) for k, v in outs.most_common(6)])
    if outu: print("   sorties USD", [(k, lab(k)[:14], round(v/1e6, 2)) for k, v in outu.most_common(5)])
    if outD: print("   sorties DMAGA", [(k, lab(k)[:14], round(v/1e6, 2)) for k, v in outD.most_common(5)])
    rows = sorted(sen.items(), key=lambda kv: -(kv[1]["SOL"] / 1e9 + (kv[1]["USDC"] + kv[1]["USDT"]) / 1e6 / 170))
    rc = collections.Counter()
    for s, c in rows:
        rr = roles.get(s, "")
        for x_ in rr.split("|"):
            if x_: rc[x_] += 1
        w.writerow([A, s, c["SOL"] / 1e9, c["USDC"] / 1e6, c["USDT"] / 1e6, c["DMAGA"] / 1e6, c["n"], iso(dates[s][0]), iso(dates[s][1]), s in t, rr])
    print("   rôles des expéditeurs", dict(rc))
    for s, c in rows[:int(os.environ.get("TOPN", "10"))]:
        print("     ", s, lab(s)[:16], "SOL", round(c["SOL"] / 1e9, 3), "USD", round((c["USDC"] + c["USDT"]) / 1e6, 2), "D" if s in t else "-", roles.get(s, ""), iso(dates[s][0])[:10], iso(dates[s][1])[:10])
