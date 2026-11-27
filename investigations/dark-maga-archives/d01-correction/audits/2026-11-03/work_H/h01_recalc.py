"""Recalcul indépendant, lecture seule, des chiffres du rapport sur data_v2. Requêtes réécrites, sans importer les scripts du dépôt."""
import csv, json, os, re, time
from pathlib import Path
import duckdb
os.environ["TZ"] = "UTC"; time.tzset()
B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2")
B0 = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data")
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
TR, WP, AC, RU, FE, ED, ND = (f"read_parquet('{B}/{n}.parquet')" for n in ("trades", "wallets", "accounts", "account_ruptures", "funding_edges", "token_edges", "nodes"))
EV = {e["name"]: e["t"] for e in json.load(open(B / "events.json"))}
T0, CRE, LOW, ENV, HIGH, WIN, BID = EV["creation_mint"], EV["migration_raydium"], EV["musk_borne_basse"], EV["musk_envoi_image"], EV["musk_borne_haute"], EV["winig_visuel"], EV["annonce_biden"]
S = 1721588400; Y0 = 1689292800
K1250 = 1721566245; F1600 = 1721577659  # @kikisknees 12:50:45, @FrancoAppr 16:00:59
out = {}
def one(q): return con.execute(q).fetchone()
def show(k, v): out[k] = v; print(k, "=", v, flush=True)
G = json.load(open(B / "prevent_groups.json"))[0]
mem = list(G["members"]); assert len(mem) == 33
coord = Path("reports/COORDINATION.md").read_text()
m_tab = re.findall(r"^\| `([1-9A-HJ-NP-Za-km-z]{32,44})` \| [\d,]+ \| [\d,]+ \| [\d, -]+ \| [\d,]+ \| [\d,]+ \| ", coord, re.M)
show("membres_table_coordination_egale_groupe", sorted(m_tab) == sorted(mem))
con.execute("CREATE TEMP TABLE g(a VARCHAR)"); con.executemany("INSERT INTO g VALUES (?)", [[a] for a in mem])
show("lignes_sigs", one(f"SELECT count(*), count(DISTINCT signature) FROM {TR}"))
show("doublons", one(f"SELECT coalesce(sum(n-1),0) FROM (SELECT count(*) n FROM {TR} GROUP BY signature,kind,owner,venue,token_delta,source HAVING count(*)>1)"))
show("doublons_sans_source", one(f"SELECT coalesce(sum(n-1),0) FROM (SELECT count(*) n FROM {TR} GROUP BY signature,kind,owner,venue,token_delta HAVING count(*)>1)"))
buy = "CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END"; sell = "CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END"
for nom, a, z in (("basse_envoi", LOW, ENV), ("envoi_haute", ENV, HIGH), ("haute_1h", HIGH, HIGH + 3600), ("biden_basse", BID, LOW), ("3h_envoi", ENV - 10800, ENV), ("3h_winig", WIN - 10800, WIN), ("24h", HIGH, HIGH + 86400), ("heure_S", S, S + 3600)):
    show("fen_" + nom, one(f"SELECT round(sum({buy})/1e9,3), round(sum({sell})/1e9,3), sum((token_delta>0)::int), sum((token_delta<0)::int) FROM {TR} WHERE kind='swap' AND block_time>={a} AND block_time<{z}"))
show("biden_h", round((LOW - BID) / 3600, 3))
show("butler_mint_s", T0 - 1720908660)
show("delta_fp_winig", WIN - F1600)
# groupe
W = "owner IN (SELECT a FROM g)"
h1 = one(f"SELECT count(DISTINCT owner), sum(token_delta)/1e12, sum(-sol_lamports)/1e9 FROM {TR} WHERE {W} AND kind='swap' AND token_delta>0 AND block_time<{T0 + 3600}")
show("groupe_1re_heure", h1)
show("groupe_achat_avant_low", one(f"SELECT sum(token_delta)/1e12, sum(-sol_lamports)/1e9, count(DISTINCT owner) FROM {TR} WHERE {W} AND kind='swap' AND token_delta>0 AND block_time<{LOW}"))
for nom, a, z in (("winig_haute", WIN, HIGH), ("k1250_winig", K1250, WIN), ("franco_winig", F1600, WIN), ("winig_low", WIN, LOW)):
    show("groupe_swaps_" + nom, one(f"SELECT count(*), coalesce(sum({buy}),0)/1e9, coalesce(sum({sell}),0)/1e9, count(DISTINCT owner) FROM {TR} WHERE {W} AND kind='swap' AND block_time>={a} AND block_time<{z}"))
    show("groupe_transferts_" + nom, one(f"SELECT count(*), coalesce(sum(qty),0) FROM {ED} WHERE block_time>={a} AND block_time<{z} AND dst<>'(multiple)' AND (src IN (SELECT a FROM g) OR dst IN (SELECT a FROM g))"))
show("groupe_lignes_k1250_detail", con.execute(f"SELECT strftime(to_timestamp(block_time),'%H:%M:%S'), owner, kind, token_delta/1e12, sol_lamports/1e9 FROM {TR} WHERE {W} AND kind='swap' AND block_time>={K1250} AND block_time<{WIN} ORDER BY block_time LIMIT 25").fetchall())
gs = one(f"SELECT sum(sol_lamports)/1e9, sum(-token_delta)/1e12 FROM {TR} WHERE {W} AND kind='swap' AND token_delta<0 AND block_time>={HIGH} AND block_time<{HIGH + 86400}")
mk = one(f"SELECT sum(sol_lamports)/1e9 FROM {TR} WHERE kind='swap' AND token_delta<0 AND block_time>={HIGH} AND block_time<{HIGH + 86400}")[0]
show("ventes24", (gs[0], gs[1], mk, 100 * gs[0] / mk))
show("ventes6_18", one(f"SELECT sum(CASE WHEN block_time<{HIGH + 21600} THEN sol_lamports ELSE 0 END)/1e9, sum(CASE WHEN block_time>={HIGH + 21600} THEN sol_lamports ELSE 0 END)/1e9 FROM {TR} WHERE {W} AND kind='swap' AND token_delta<0 AND block_time>={HIGH} AND block_time<{HIGH + 86400}"))
show("groupe_wallets", one(f"SELECT count(*), sum(realized_sol), sum(net_sol_all), sum(proceeds_usd), sum(cost_usd), sum(proceeds_usd-cost_usd), sum(bought_qty)/1e6, sum(bought_sol) FROM {WP} WHERE {W}"))
# soldes à la borne basse
con.execute(f"CREATE TEMP TABLE bal AS SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {AC} WHERE block_time<{LOW} GROUP BY 1")
con.execute(f"CREATE TEMP TABLE seen AS SELECT DISTINCT signature s FROM {AC} WHERE block_time<{LOW}")
con.execute(f"CREATE TEMP TABLE hid AS SELECT src, qty*1e6 q FROM {ED} WHERE how='gtba' AND block_time<{LOW} AND dst<>'(multiple)' AND signature NOT IN (SELECT s FROM seen)")
con.execute("CREATE TEMP TABLE own AS WITH b AS (SELECT owner,sum(p) v FROM bal GROUP BY 1), o AS (SELECT src,sum(q) v FROM hid GROUP BY 1) SELECT b.owner, b.v-coalesce(o.v,0) v FROM b LEFT JOIN o ON o.src=b.owner")
ven = list(json.load(open("reports/data_checks/venues.json"))) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
con.execute("CREATE TEMP TABLE ve(a VARCHAR)"); con.executemany("INSERT INTO ve VALUES (?)", [[a] for a in ven])
tot, pools = one("SELECT sum(v)/1e12, sum(CASE WHEN owner IN (SELECT a FROM ve) THEN v ELSE 0 END)/1e12 FROM own")
hors = tot - pools
show("soldes_tot_pools_hors", (tot, pools, hors))
gm = one("SELECT sum(v)/1e12, count(*) FROM own WHERE owner IN (SELECT a FROM g)")
show("groupe_M_pct", (gm[0], gm[1], 100 * gm[0] / hors, 100 * gm[0] / 1000))
gs_ = json.load(open(B / "group_split.json"))
weak = next(x for x in gs_["ponts_faibles"] if any(m.startswith("Ei5yGz8") for m in x["members"]))
held = dict(con.execute("SELECT owner, v/1e12 FROM own WHERE owner IN (SELECT a FROM g)").fetchall())
core = [m for m in mem if m not in weak["members"]]
fa = ["9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP", "7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu"]
show("coeur", (len(core), sum(held.get(m, 0) for m in core), 100 * sum(held.get(m, 0) for m in core) / hors, sum(held.get(m, 0) for m in core if m not in fa), 100 * sum(held.get(m, 0) for m in core if m not in fa) / hors, len(weak["members"]), sum(held.get(m, 0) for m in weak["members"])))
ser = [r["dest"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
sen = [r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))]
un = set(mem) | set(ser) | set(sen)
for nom, L in (("serie", ser), ("exped", sen), ("union", un)):
    v = sum(x[0] for x in con.execute("SELECT v/1e12 FROM own WHERE owner IN (" + ",".join(repr(a) for a in L) + ")").fetchall())
    show("perim_" + nom, (len(set(L)), v, 100 * v / hors))
show("recouvrements", (len(set(mem) & set(ser)), len(set(mem) & set(sen)), len(set(ser) & set(sen))))
show("exped_touchent", one(f"SELECT count(DISTINCT owner) FROM {AC} WHERE owner IN (" + ",".join(repr(a) for a in sen) + ")"))
# ruptures
show("ruptures", one(f"SELECT count(*), count(DISTINCT account), sum(CASE WHEN gap>0 THEN gap ELSE 0 END)/1e12, sum(CASE WHEN gap<0 THEN -gap ELSE 0 END)/1e12 FROM {RU}"))
show("ruptures_avant", one(f"SELECT count(*), sum(abs(gap))/1e12, sum(CASE WHEN owner='AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk' OR prev_owner='AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk' THEN abs(gap) ELSE 0 END)/1e12 FROM {RU} WHERE block_time<{LOW}"))
show("ruptures_24h", one(f"SELECT count(*), sum(abs(gap))/1e12 FROM {RU} WHERE block_time>={HIGH} AND block_time<{HIGH + 86400}"))
# wallets, cohortes
show("wallets_n", one(f"SELECT count(*), sum(realized_sol), sum(bought_sol), sum(sold_sol) FROM {WP}"))
for n, a in (("H3", "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"), ("GX", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"), ("P9", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"), ("Q", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"), ("C", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR")):
    show("w_" + n, one(f"SELECT realized_sol, proceeds_usd-cost_usd, cost_usd, bought_sol, bought_qty/1e6 FROM {WP} WHERE owner='{a}'"))
show("cohorte_apres", one(f"SELECT count(*), sum((realized_sol>0)::int), sum((realized_sol>0.1)::int) FROM {WP} WHERE first_buy_time>={HIGH}"))
show("top5_realise_cout_connu", con.execute(f"SELECT owner, realized_sol FROM {WP} ORDER BY realized_sol DESC LIMIT 6").fetchall())
# sommet
con.execute(f"CREATE TEMP TABLE v AS SELECT * FROM read_parquet({[str(p) for p in (B / 'vault_shards').glob('*.parquet') if not p.name.startswith('._')]!r}) WHERE vault IN ('5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL','3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH')")
show("sommet", one("""WITH d AS (SELECT DISTINCT slot,tx_index,block_time,post FROM v WHERE vault='5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL' AND post>0), s AS (SELECT DISTINCT slot,tx_index,post FROM v WHERE vault='3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH')
    SELECT (s.post/1e9)/(d.post/1e6)*1e9, strftime(to_timestamp(d.block_time),'%d/%m %H:%M:%S') FROM d JOIN s USING(slot,tx_index) ORDER BY 1 DESC LIMIT 1"""))
# résiduels
show("residuel_somme", one(f"SELECT sum(residual_qty)/1e6, sum(residual_flux_qty)/1e6, sum(CASE WHEN owner IN (SELECT a FROM ve) THEN residual_qty ELSE 0 END)/1e6, min(residual_qty) FROM {WP}"))
con.execute(f"CREATE TEMP TABLE fin AS SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {AC} GROUP BY 1")
show("solde_fin_tout", one("SELECT sum(p)/1e12, sum(CASE WHEN owner IN (SELECT a FROM ve) THEN p ELSE 0 END)/1e12 FROM fin"))
# fonds
K = "CASE WHEN is_pool THEN 'pool' WHEN src_label IS NULL THEN 'sans' WHEN src_label LIKE 'Jupiter%' THEN 'jup' WHEN src_label LIKE 'Pont%' OR src_label LIKE 'Service%' THEN 'serv' ELSE 'ech' END"
r = con.execute(f"SELECT {K}, sum(sol) FROM {FE} WHERE level=0 AND query='in_before' AND block_time>={Y0} AND block_time<{T0} GROUP BY 1").fetchall()
t = sum(x[1] for x in r); show("fonds", (t, {x[0]: round(100 * x[1] / t, 3) for x in r}))
r2 = con.execute(f"SELECT {K}, sum(sol) FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} GROUP BY 1").fetchall()
t2 = sum(x[1] for x in r2); show("fonds_toutes_requetes", (t2, {x[0]: round(100 * x[1] / t2, 3) for x in r2}))
show("premier_financeur", con.execute(f"""WITH f AS (SELECT wallet, arg_min(src_label, block_time) l FROM {FE} WHERE level=0 AND NOT is_pool AND sol>=0.01 AND block_time<{T0} GROUP BY 1)
    SELECT CASE WHEN l IS NULL THEN 'sans' WHEN l LIKE 'Jupiter%' THEN 'jup' WHEN l LIKE 'Pont%' OR l LIKE 'Service%' THEN 'serv' ELSE 'ech' END, count(*) FROM f GROUP BY 1""").fetchall())
show("cles_doublees", one(f"SELECT count(*) FROM (SELECT 1 FROM {FE} GROUP BY wallet,signature,src HAVING count(*)>1)"))
show("fonds_apres_mint_part", one(f"SELECT sum(CASE WHEN block_time>={T0} THEN sol ELSE 0 END)/sum(sol) FROM {FE} WHERE level=0 AND query='in_before'"))
# sorties
ex = json.load(open(B / "exit_summary.json"))
fr = {}; hotw = {}
for w, x in ex.items():
    for k, y in x["frontieres"].items():
        n = k.split(":", 1)[1]
        if "pool" not in n and "Jupiter" not in n:
            fr[n] = fr.get(n, 0) + y
        if n.startswith("hot"):
            hotw[w] = hotw.get(w, 0) + y
serv = sum(v for k, v in fr.items() if k.startswith("service")); hot = sum(v for k, v in fr.items() if k.startswith("hot")); cex = {k: round(v, 1) for k, v in fr.items() if not k.startswith(("service", "hot"))}
show("sorties", (len(ex), sum(1 for x in ex.values() if x["tronque"]), round(serv, 1), round(hot, 1), cex, round(sum(cex.values()), 1)))
show("hot_par_wallet_top3", sorted(hotw.items(), key=lambda kv: -kv[1])[:3])
# angles morts
SW = f"read_parquet('{B0}/controls/swaps/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k.parquet')"
con.execute(f"CREATE TEMP TABLE cb AS SELECT owner, sum(token_delta) b FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{CRE} GROUP BY 1")
con.execute(f"CREATE TEMP TABLE ea AS SELECT DISTINCT owner FROM {SW} WHERE qty>0 AND t<{CRE + 86400}")
con.execute(f"CREATE TEMP TABLE bs AS SELECT owner,sum(p) v FROM (SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {AC} WHERE block_time<{S} GROUP BY 1) GROUP BY 1")
hm = one("SELECT count(*), sum(c.b)/1e12, sum(coalesce(s.v,0))/1e12 FROM cb c LEFT JOIN bs s USING(owner) WHERE c.owner NOT IN (SELECT owner FROM ea)")
st = one(f"""SELECT coalesce(sum(e.qty),0)/1e6 FROM {ED} e WHERE e.how='gtba' AND e.block_time<{S} AND e.block_time<{LOW} AND e.dst<>'(multiple)' AND e.signature NOT IN (SELECT s FROM seen) AND e.src IN (SELECT owner FROM cb) AND e.src NOT IN (SELECT owner FROM ea)""")[0]
show("angles_morts", (hm, st, hm[2] - st))
con.execute(f"CREATE TEMP TABLE xf AS SELECT owner, token_delta d FROM {TR} WHERE kind='transfer' AND block_time>={S - 86400} AND block_time<{S}")
show("xf", (one("SELECT sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e12, count(DISTINCT CASE WHEN d>0 THEN owner END), sum(CASE WHEN d>0 AND owner IN (SELECT a FROM g) THEN d ELSE 0 END)/1e12 FROM xf"), one("SELECT sum(n)/1e12, count(*) FROM (SELECT owner, sum(d) n FROM xf GROUP BY 1) WHERE n>0")))
show("achats_heure_S_gel", one(f"SELECT sum(-sol)/1e9, count(*) FROM {SW} WHERE qty>0 AND t>={S} AND t<{S + 3600}"))
# étiquettes Dune
txt = Path("evidence/labels/dune_cex_solana_addresses.sql").read_text()
show("dune_lignes_adresses", len(set(re.findall(r"[1-9A-HJ-NP-Za-km-z]{32,44}", txt))))
Path("audits/2026-11-03/work_H/h01_recalc.json").write_text(json.dumps(out, indent=0, ensure_ascii=False, default=str))
