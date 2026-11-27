import csv, json, os, re, time
from collections import defaultdict
from pathlib import Path
import duckdb
from dmaga.venues import load
os.environ["TZ"] = "UTC"; time.tzset()
A = Path("audits/2026-11-03"); B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2")
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H"})
con.execute("SET TimeZone='UTC'")
TR, AC, ED, ND = (f"read_parquet('{B}/{n}.parquet')" for n in ("trades", "accounts", "token_edges", "nodes"))
EV = {e["name"]: e["t"] for e in json.load(open(B / "events.json"))}
LOW, HI = EV["musk_borne_basse"], EV["musk_borne_haute"]; Z = HI + 86400
mem = json.load(open(B / "prevent_groups.json"))[0]["members"]; IN = ",".join(repr(x) for x in mem)
# destinataires des 34 transferts : vente plafonnée au reçu
d = con.execute(f"SELECT dst, min(block_time), sum(qty)*1e6 FROM {ED} WHERE block_time>={HI} AND block_time<{Z} AND src IN ({IN}) AND dst NOT IN ({IN}) AND dst<>'(multiple)' GROUP BY 1").fetchall()
att = 0.0; nv = 0
for dst, t, q in d:
    s = con.execute(f"SELECT coalesce(sum(-token_delta),0), coalesce(sum(sol_lamports),0) FROM {TR} WHERE owner='{dst}' AND kind='swap' AND token_delta<0 AND block_time>={t} AND block_time<{Z}").fetchone()
    if s[0]: att += s[1] * min(1.0, q / s[0]); nv += 1
mk = con.execute(f"SELECT sum(sol_lamports) FROM {TR} WHERE kind='swap' AND token_delta<0 AND block_time>={HI} AND block_time<{Z}").fetchone()[0]
gs = con.execute(f"SELECT sum(sol_lamports) FROM {TR} WHERE owner IN ({IN}) AND kind='swap' AND token_delta<0 AND block_time>={HI} AND block_time<{Z}").fetchone()[0]
print("destinataires vendeurs", nv, round(att / 1e9, 3), "part", round(100 * (gs + att) / mk, 3))
con.execute(f"CREATE TEMP TABLE bal AS SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {AC} WHERE block_time<{LOW} GROUP BY 1")
con.execute(f"CREATE TEMP TABLE seen AS SELECT DISTINCT signature s FROM {AC} WHERE block_time<{LOW}")
con.execute(f"CREATE TEMP TABLE hid AS SELECT src, qty*1e6 q FROM {ED} WHERE how='gtba' AND block_time<{LOW} AND dst<>'(multiple)' AND signature NOT IN (SELECT s FROM seen)")
con.execute("CREATE TEMP TABLE own AS WITH b AS (SELECT owner,sum(p) v FROM bal GROUP BY 1), o AS (SELECT src,sum(q) v FROM hid GROUP BY 1) SELECT b.owner, b.v-coalesce(o.v,0) v FROM b LEFT JOIN o ON o.src=b.owner")
ve = list(load()) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
VE = ",".join(repr(x) for x in ve)
con.execute(f"CREATE TEMP TABLE o AS SELECT owner a, v FROM own WHERE v>=1e12 AND owner NOT IN ({VE}) AND owner NOT IN ({IN}) AND owner NOT IN (SELECT address FROM {ND} WHERE kind<>'wallet')")
on, om = con.execute("SELECT count(*), sum(v)/1e12 FROM o").fetchone()
k = dict(con.execute(f"SELECT kind, sum(-token_delta)/1e12 FROM {TR} WHERE owner IN (SELECT a FROM o) AND token_delta<0 AND block_time>={HI} AND block_time<{Z} GROUP BY 1").fetchall())
oe = con.execute(f"SELECT coalesce(sum(qty),0)/1e6 FROM {ED} WHERE block_time>={HI} AND block_time<{Z} AND src IN (SELECT a FROM o) AND dst<>'(multiple)'").fetchone()[0]
oi = con.execute(f"SELECT coalesce(sum(qty),0)/1e6 FROM {ED} WHERE block_time>={HI} AND block_time<{Z} AND src IN (SELECT a FROM o) AND dst IN (SELECT a FROM o)").fetchone()[0]
print("autres", on, round(om, 2), {a: round(b, 2) for a, b in k.items()}, round(oe, 2), round(oi, 2), "swap %", round(100 * k.get("swap", 0) / om, 2), "bas", round(100 * (k.get("swap", 0) + k.get("transfer", 0) - oi) / om, 2), "haut", round(100 * (k.get("swap", 0) + oe) / om, 2))
print("G7", con.execute(f"SELECT src, dst, qty/1e6, strftime(to_timestamp(block_time),'%d/%m/%Y %H:%M:%S') FROM {ED} WHERE (src LIKE 'ERMtiLod%' AND dst LIKE 'HW5MqvM1%') OR (src LIKE 'GoPCTrS3%' AND dst LIKE 'HKzkNSH2%')").fetchall())
I = list(csv.DictReader(open(A / "work_G/g30_in.csv")))
hs = {x["sender"] for x in I if x["depot"].startswith("H9Xezqfd")}
print("H9X expéditeurs", len(hs), "touchent", con.execute(f"SELECT count(DISTINCT owner) FROM {AC} WHERE owner IN ({','.join(repr(x) for x in hs)})").fetchone())
print("26/01/2025 vers 9W9b", len([x for x in I if x["depot"].startswith("9W9b") and x["utc"].startswith("2025-01-26")]), [(x["utc"][11:19], x["sender"][:8]) for x in I if x["depot"].startswith("9W9b") and x["utc"].startswith("2025-01-26")][-3:])
FB = list(csv.DictReader(open(A / "work_G/flow_boundaries.csv")))
dd = defaultdict(float)
for r in FB:
    if r["perimetre_source"].startswith("P1"): dd[r["type_frontiere"].split(" [")[0]] += float(r["sol_eq"] or 0)
den = sum(v for a, v in dd.items() if not a.startswith(("interne", "pool ou route")))
print("P1", round(den, 1), {a: round(v, 1) for a, v in dd.items()})
for f, p in (("g31_ctrl_overlap.txt", r"7140|7 140|max"), ("g53.txt", r"1913|194[.,]85"), ("g22_all.txt", r"Caw4")):
    t = (A / "work_G" / f).read_text(errors="ignore"); print(f, [m.group(0)[:150] for m in re.finditer(rf".*(?:{p}).*", t)][:3])
for i, nom in ((1773893309028577383, "XHEILIGX"), (1815873841870299404, "twicrates"), (1815006501896872388, "kiki1250"), (1812984492157771825, "kanpai orig")):
    print(nom, time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(((i >> 22) + 1288834974657) // 1000)))
print("jours", (1720922725 - 1711764096) / 86400)
