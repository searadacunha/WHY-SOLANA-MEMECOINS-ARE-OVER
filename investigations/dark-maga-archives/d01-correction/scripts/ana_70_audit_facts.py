#!/usr/bin/env python3
"""Chiffres de l'audit du 03/11 recalculés sur le dérivé corrigé, pour les rapports. DESCRIPTIF, hors plan gelé, sans réseau. Sortie : DATA/audit_facts.json.

Règles reprises de l'audit D (work_D/d42, d43, d44, d45, d46, d48), appliquées à data_v2. Lit aussi en lecture seule : le dérivé du gel (comparaison avant et
après), les swaps gelés de DMAGA (mesure M6), work_C/cb_window.csv et work_D/d20_senders.csv (série et expéditeurs, sorties réseau complètes).
"""
import csv
import gzip
import json
from pathlib import Path

from dmaga.config import BIG as BIG0, RAW
from dmaga.db import connect
from dmaga.labels import load as load_labels
from dmaga.paths import BIG, DATA, SOURCES, exige_v2
from dmaga.venues import load as load_venues

exige_v2()
EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
T0, CRE, LOW, ENV, HIGH, WIN = EV["creation_mint"], EV["migration_raydium"], EV["musk_borne_basse"], EV["musk_envoi_image"], EV["musk_borne_haute"], EV["winig_visuel"]
S, TF, TZ = 1721588400, HIGH, HIGH + 86400
Y0 = 1689292800  # 14/07/2023
AUD = Path("audits/2026-11-03")
CR, Q, G41, COL = ("8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E",
                  "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL")
HX, HABP = "Hx1UvdgMqZBQRrSAKhSSfc7Hvcb2Mk4dFrcrQpYG6urT", "Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96"
FAIBLES_C06 = ["9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP", "7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu"]
NOMMES = {"H3": "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GX": "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "P9": "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "Q": Q, "C": CR}
AUTRES = {"ET8ZG5zA": "ET8ZG5zAcEA4n1bNN5B5MkeStCGw7T1f6ZJwwH7G3rMB", "Akp46Dic": "Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB", "C7i9beNH": "C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK",
          "5FzhCSWL": "5FzhCSWLT84QdgX9wYWWuWY1ZY3G9kMUu2fRifxLLhmx", "DswkYbBh": "DswkYbBhV9MKWhymaawezWEEZoWPV1az79wcm1J644na"}

con = connect(mem="700MB")
TR, ED, AC, RU, WP, ND = (f"read_parquet('{BIG}/{n}.parquet')" for n in ("trades", "token_edges", "accounts", "account_ruptures", "wallets", "nodes"))
TR0, WP0, ND0 = (f"read_parquet('{BIG0}/{n}.parquet')" for n in ("trades", "wallets", "nodes"))
SW = f"read_parquet('{BIG0}/controls/swaps/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k.parquet')"
FE = f"read_parquet('{BIG}/funding_edges.parquet')"


def one(sql):
    return con.execute(sql).fetchone()


def table(name, values):
    con.execute(f"CREATE OR REPLACE TEMP TABLE {name}(a VARCHAR)")
    con.executemany(f"INSERT INTO {name} VALUES (?)", [[a] for a in values])


groups = json.loads((DATA / "prevent_groups.json").read_text())
G0 = groups[0]
members = set(G0["members"])
table("g", members)
ser = [r["dest"] for r in csv.DictReader((AUD / "work_C/cb_window.csv").open()) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
sen = [r["sender"] for r in csv.DictReader((AUD / "work_D/d20_senders.csv").open())]
assert len(ser) == 15 and len(sen) == 48
table("ser", ser)
table("sen", sen)
table("un", members | set(ser) | set(sen))
traced = [p.name for p in (RAW / "flows").iterdir() if p.is_dir() and not p.name.startswith("._")]
table("tr", traced)
RAY = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
table("ve", list(load_venues()) + [RAY, "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"])
F = {}

# 1. Lignes : ce que le dédoublonnage retire de l'ancien fichier, ce qui reste dans le nouveau
r = one(f"SELECT count(*), count(DISTINCT signature) FROM {TR0}")
d = one(f"""SELECT coalesce(sum(n-1),0), coalesce(sum(CASE WHEN source='pool' THEN n-1 END),0), coalesce(sum(CASE WHEN source='venue' THEN n-1 END),0)
            FROM (SELECT source, count(*) n FROM {TR0} GROUP BY signature, kind, owner, venue, token_delta, source HAVING count(*)>1)""")
n2 = one(f"SELECT count(*), count(DISTINCT signature) FROM {TR}")
pl = one(f"SELECT min(block_time), max(block_time) FROM (SELECT block_time FROM {TR0} WHERE source='pool' GROUP BY signature, kind, owner, venue, token_delta, block_time HAVING count(*)>1)")
F["lignes"] = {"avant": r[0], "avant_sig": r[1], "doublees": d[0], "doublees_pool": d[1], "doublees_venue": d[2], "unique_avant": r[0] - d[0], "apres": n2[0], "apres_sig": n2[1],
               "doublees_avant_musk": one(f"SELECT count(*) FROM (SELECT 1 FROM {TR0} WHERE block_time<={HIGH} GROUP BY signature, kind, owner, venue, token_delta, source HAVING count(*)>1)")[0],
               "swap_other_avant": one(f"SELECT count(*) FROM {TR0} WHERE kind='swap_other'")[0], "swap_other_apres": one(f"SELECT count(*) FROM {TR} WHERE kind='swap_other'")[0],
               "pool_doublon_de": pl[0], "pool_doublon_a": pl[1]}

# 2. Soldes à la borne basse : derniers soldes vus, moins les transferts vus par les seuls flux (d43)
con.execute(f"""CREATE TEMP TABLE bal_T AS SELECT account, arg_max(owner, (slot, tx_index)) owner, arg_max(post, (slot, tx_index)) bal FROM {AC} WHERE block_time<{LOW} GROUP BY 1""")
con.execute(f"CREATE TEMP TABLE seen AS SELECT DISTINCT signature s FROM {AC} WHERE block_time<{LOW}")
con.execute(f"CREATE TEMP TABLE hid AS SELECT src, dst, qty*1e6 q, block_time, signature FROM {ED} WHERE how='gtba' AND block_time<{LOW} AND dst<>'(multiple)' AND signature NOT IN (SELECT s FROM seen)")
con.execute("""CREATE TEMP TABLE own_T AS WITH b AS (SELECT owner, sum(bal) v FROM bal_T GROUP BY 1), o AS (SELECT src a, sum(q) v FROM hid GROUP BY 1)
               SELECT b.owner, b.v - coalesce(o.v, 0) v FROM b LEFT JOIN o ON o.a = b.owner""")
tot, pools, hors = one("SELECT sum(v)/1e12, sum(CASE WHEN owner IN (SELECT a FROM ve) THEN v ELSE 0 END)/1e12, sum(CASE WHEN owner IN (SELECT a FROM ve) THEN 0 ELSE v END)/1e12 FROM own_T")


def perimetre(tbl):
    n, m = one(f"SELECT count(*), sum(v)/1e12 FROM own_T WHERE owner IN (SELECT a FROM {tbl})")
    return {"avec_solde": n, "M": m, "pct": 100 * m / hors, "taille": one(f"SELECT count(*) FROM {tbl}")[0]}


held = dict(con.execute("SELECT owner, v/1e12 FROM own_T WHERE owner IN (SELECT a FROM g)").fetchall())
GS = json.loads((DATA / "group_split.json").read_text())
weak4 = next(x for x in GS["ponts_faibles"] if any(m.startswith("Ei5yGz8") for m in x["members"]))
core = [m for m in members if m not in weak4["members"]]
F["soldes"] = {"total_M": tot, "pools_M": pools, "hors_pools_M": hors, "hid_M": one("SELECT sum(q)/1e12 FROM hid")[0], "hid_n": one("SELECT count(*) FROM hid")[0]}
F["perimetres"] = {"groupe": perimetre("g"), "serie15": perimetre("ser"), "expediteurs48": perimetre("sen"), "union": perimetre("un"),
                   "groupe_serie": one("SELECT count(*) FROM g WHERE a IN (SELECT a FROM ser)")[0], "groupe_expediteurs": one("SELECT count(*) FROM g WHERE a IN (SELECT a FROM sen)")[0],
                   "serie_expediteurs": one("SELECT count(*) FROM ser WHERE a IN (SELECT a FROM sen)")[0], "createur_dans_groupe": CR in members,
                   "aretes_createur_groupe": one(f"SELECT count(*) FROM {ED} WHERE (src='{CR}' AND dst IN (SELECT a FROM g)) OR (dst='{CR}' AND src IN (SELECT a FROM g))")[0],
                   "coeur_n": len(core), "coeur_M": sum(held.get(m, 0) for m in core), "coeur_pct": 100 * sum(held.get(m, 0) for m in core) / hors,
                   "coeur_sans_faibles_M": sum(held.get(m, 0) for m in core if m not in FAIBLES_C06), "coeur_sans_faibles_pct": 100 * sum(held.get(m, 0) for m in core if m not in FAIBLES_C06) / hors,
                   "faibles4_n": len(weak4["members"]), "faibles4_M": sum(held.get(m, 0) for m in weak4["members"])}
assert all(m in members for m in FAIBLES_C06)
F["expediteurs"] = {"touchent_dmaga": one(f"SELECT count(DISTINCT owner) FROM {AC} WHERE owner IN (SELECT a FROM sen)")[0],
                    "hors_serie_groupe_touchent": one(f"SELECT count(DISTINCT owner) FROM {AC} WHERE owner IN (SELECT a FROM sen) AND owner NOT IN (SELECT a FROM ser) AND owner NOT IN (SELECT a FROM g)")[0],
                    "hors_serie_groupe": one("SELECT count(*) FROM sen WHERE a NOT IN (SELECT a FROM ser) AND a NOT IN (SELECT a FROM g)")[0]}

# 3. Ventes en 24 h : marché, groupe, destinataires, base commune (C-05, d43)
mk = one(f"SELECT sum(sol_lamports)/1e9 FROM {TR} WHERE kind='swap' AND token_delta<0 AND block_time>={TF} AND block_time<{TZ}")[0]
gs = one(f"SELECT coalesce(sum(sol_lamports),0)/1e9, coalesce(sum(-token_delta),0)/1e12 FROM {TR} WHERE owner IN (SELECT a FROM g) AND kind='swap' AND token_delta<0 AND block_time>={TF} AND block_time<{TZ}")
con.execute(f"CREATE TEMP TABLE gout AS SELECT src, dst, qty*1e6 q, block_time t FROM {ED} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM g) AND dst NOT IN (SELECT a FROM g) AND dst<>'(multiple)'")
go = one("SELECT count(*), sum(q)/1e12, count(DISTINCT dst) FROM gout")
att = tot_d = 0.0
n_vend = 0
for dst, t_, q_ in con.execute("SELECT dst, min(t), sum(q) FROM gout GROUP BY 1").fetchall():
    a24 = one(f"SELECT coalesce(sum(sol_lamports),0) FROM {TR} WHERE owner='{dst}' AND kind='swap' AND token_delta<0 AND block_time>={TF} AND block_time<{TZ}")[0]
    a2 = one(f"SELECT coalesce(sum(-token_delta),0), coalesce(sum(sol_lamports),0) FROM {TR} WHERE owner='{dst}' AND kind='swap' AND token_delta<0 AND block_time>={t_} AND block_time<{TZ}")
    tot_d += a24
    if a2[0]:
        att += a2[1] * min(1.0, q_ / a2[0])
        n_vend += 1
con.execute("CREATE TEMP TABLE o AS SELECT owner a, v FROM own_T WHERE v>=1e12 AND owner NOT IN (SELECT a FROM ve) AND owner NOT IN (SELECT a FROM g)")
con.execute(f"DELETE FROM o WHERE a IN (SELECT address FROM {ND} WHERE kind<>'wallet')")
on, om = one("SELECT count(*), sum(v)/1e12 FROM o")
ok = dict(con.execute(f"SELECT kind, sum(-token_delta)/1e12 FROM {TR} WHERE owner IN (SELECT a FROM o) AND token_delta<0 AND block_time>={TF} AND block_time<{TZ} GROUP BY 1").fetchall())
oe = one(f"SELECT coalesce(sum(qty),0)/1e6 FROM {ED} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM o) AND dst<>'(multiple)'")[0]
oi = one(f"SELECT coalesce(sum(qty),0)/1e6 FROM {ED} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM o) AND dst IN (SELECT a FROM o)")[0]
g_m = F["perimetres"]["groupe"]["M"]
F["ventes24"] = {"marche_sol": mk, "groupe_sol": gs[0], "groupe_M": gs[1], "part_pct": 100 * gs[0] / mk, "transferts_n": go[0], "transferts_M": go[1], "destinataires": go[2], "destinataires_vendeurs": n_vend,
                 "dest_vente_sol": tot_d / 1e9, "dest_plafonne_sol": att / 1e9, "part_elargie_pct": 100 * (gs[0] + att / 1e9) / mk,
                 "groupe_sortie_pct": 100 * (gs[1] + go[1]) / g_m, "groupe_swap_pct": 100 * gs[1] / g_m,
                 "autres_n": on, "autres_M": om, "autres_swap_M": ok.get("swap", 0), "autres_transfert_M": ok.get("transfer", 0), "autres_edges_M": oe, "autres_internes_M": oi,
                 "autres_swap_pct": 100 * ok.get("swap", 0) / om,
                 "autres_sortie_bas_pct": 100 * (ok.get("swap", 0) + ok.get("transfer", 0) - oi) / om, "autres_sortie_haut_pct": 100 * (ok.get("swap", 0) + oe) / om,
                 "cachees_autres": one(f"SELECT count(*) FROM {RU} WHERE block_time>={TF} AND block_time<{TZ} AND gap<0 AND coalesce(owner, prev_owner) IN (SELECT a FROM o)")[0],
                 "cachees_groupe": one(f"SELECT count(*) FROM {RU} WHERE block_time>={TF} AND block_time<{TZ} AND gap<0 AND coalesce(owner, prev_owner) IN (SELECT a FROM g)")[0]}

# 4. Angles morts du test sur DMAGA, en stock (B-06, d44)
con.execute(f"CREATE TEMP TABLE curvebuy AS SELECT owner, sum(token_delta) b FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{CRE} GROUP BY 1")
con.execute(f"CREATE TEMP TABLE early AS SELECT DISTINCT owner FROM {SW} WHERE qty>0 AND t<{CRE + 86400}")
con.execute(f"""CREATE TEMP TABLE bal_S AS SELECT owner, sum(bal) v FROM (SELECT account, arg_max(owner, (slot, tx_index)) owner, arg_max(post, (slot, tx_index)) bal FROM {AC} WHERE block_time<{S} GROUP BY 1) GROUP BY 1""")
hm = one("SELECT count(*), sum(c.b)/1e12, sum(coalesce(s.v,0))/1e12 FROM curvebuy c LEFT JOIN bal_S s USING (owner) WHERE c.owner NOT IN (SELECT owner FROM early)")
stale = one("SELECT coalesce(sum(q),0)/1e12 FROM hid WHERE block_time<1721588400 AND src IN (SELECT owner FROM curvebuy) AND src NOT IN (SELECT owner FROM early)")[0]
con.execute(f"CREATE TEMP TABLE xf AS SELECT owner, token_delta d FROM {TR} WHERE kind='transfer' AND block_time>={S - 86400} AND block_time<{S}")
xf = one("SELECT sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e12, count(DISTINCT CASE WHEN d>0 THEN owner END), sum(CASE WHEN d>0 AND owner IN (SELECT a FROM g) THEN d ELSE 0 END)/1e12 FROM xf")
xn = one("SELECT sum(n)/1e12, count(*) FROM (SELECT owner, sum(d) n FROM xf GROUP BY 1) WHERE n>0")
sh = one(f"SELECT sum(-sol)/1e9, count(*) FROM {SW} WHERE qty>0 AND t>={S} AND t<{S + 3600}")
F["angles_morts"] = {"acheteurs_hors_m6": hm[0], "achat_brut_M": hm[1], "solde_S_M": hm[2], "deja_sortis_M": stale, "stock_M": hm[2] - stale, "transferts_recus_M": xf[0], "wallets_recus": xf[1],
                     "recus_groupe_M": xf[2], "nets_M": xn[0], "nets_wallets": xn[1], "achats_heure_S_sol": sh[0], "achats_heure_S_n": sh[1]}

# 5. Mouvements hors du brut (A-05, d42)
con.execute(f"CREATE TEMP TABLE r2 AS SELECT *, coalesce(owner, prev_owner) o, prev_t iv0, block_time iv1 FROM {RU}")
ra = one("SELECT count(*), count(DISTINCT account), sum(CASE WHEN gap>0 THEN gap ELSE 0 END)/1e12, sum(CASE WHEN gap<0 THEN -gap ELSE 0 END)/1e12 FROM r2")
rb = one(f"SELECT count(*), sum(abs(gap))/1e12 FROM r2 WHERE iv1<{LOW}")
rc = one(f"SELECT count(*), sum(abs(gap))/1e12 FROM r2 WHERE coalesce(iv0,0)<{LOW} AND iv1>={LOW}")
rd = one(f"SELECT count(*), sum(abs(gap))/1e12, sum(CASE WHEN gap<0 THEN -gap ELSE 0 END)/1e12 FROM r2 WHERE iv1>={TF} AND iv1<{TZ}")
re_ = one(f"SELECT sum(abs(gap))/1e12 FROM r2 WHERE iv1>={TZ}")
rt = dict((str(k), v) for k, *v in con.execute("SELECT (o IN (SELECT a FROM tr)), count(*), count(DISTINCT o), sum(abs(gap))/1e12 FROM r2 GROUP BY 1").fetchall())
rn = dict((k, v) for k, *v in con.execute(f"SELECT CASE WHEN iv1<{LOW} THEN 'avant' WHEN iv1<{TZ} THEN '24h' ELSE 'apres' END, count(*), sum(abs(gap))/1e12 FROM r2 WHERE abs(gap)>=1e12 AND o NOT IN (SELECT a FROM tr) GROUP BY 1").fetchall())
F["ruptures"] = {"n": ra[0], "comptes": ra[1], "entrees_M": ra[2], "sorties_M": ra[3], "total_M": ra[2] + ra[3], "avant_low_n": rb[0], "avant_low_M": rb[1], "cheval_n": rc[0], "cheval_M": rc[1],
                 "h24_n": rd[0], "h24_M": rd[1], "h24_sorties_M": rd[2], "ensuite_M": re_[0], "traces": rt.get("True"), "non_traces": rt.get("False"), "non_traces_1M": rn,
                 "nommes": one("SELECT count(*) FROM r2 WHERE o IN ({})".format(",".join(repr(x) for x in NOMMES.values())))[0],
                 "compense_AtZjv3Du_M": one(f"SELECT sum(gap)/1e12 FROM r2 WHERE iv1<{LOW} AND o='AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk'")[0]}
F["residuels"] = {"somme_flux_M": one(f"SELECT sum(residual_flux_qty)/1e6 FROM {WP}")[0], "somme_soldes_M": one(f"SELECT sum(residual_qty)/1e6 FROM {WP}")[0],
                  "ancien_flux_M": one(f"SELECT sum(residual_qty)/1e6 FROM {WP0}")[0], "wallets_partiels_rupture": one(f"SELECT count(*) FROM {WP} WHERE completeness LIKE '%rupture%'")[0],
                  "wallets_avec_rupture": one(f"SELECT count(*) FROM {WP} WHERE n_ruptures>0")[0]}
for k, a in (("7gEQ6syD", "7gEQ6syDZmyPE4JdfJm4qatawnDqvqdh6i8jJjCXio6h"), ("HGs9NdwD", "HGs9NdwD2c4mYHb9fYdgp2Due5gbaSEdUV871wAiCkTd")):
    F["residuels"][k] = one(f"SELECT residual_flux_qty/1e6, residual_qty/1e6 FROM {WP} WHERE owner='{a}'")

d_ = RAW / "flows"
F["residuels"]["dmaga_all_tronques"] = sum(json.load(gzip.open(p / "dmaga_all.json.gz"))["truncated"] is True for p in d_.iterdir() if not p.name.startswith("._") and (p / "dmaga_all.json.gz").exists())
F["residuels"]["cas_6t2dz4jm"] = one(f"SELECT residual_flux_qty/1e6, residual_qty/1e6 FROM {WP} WHERE owner='6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M'")
pf = one(f"SELECT sum(CASE WHEN o IN (SELECT a FROM ve) THEN p ELSE 0 END)/1e12 FROM (SELECT account, arg_max(owner, (slot, tx_index)) o, arg_max(post, (slot, tx_index)) p FROM {AC} GROUP BY 1)")[0]
F["residuels"].update(pools_fin_M=pf, offre_hors_pools_fin_M=1000 - pf)  # offre totale : 1 000 M

# 6. Origine du SOL (A-03, d45), sur la bonne fenêtre, requête in_before, niveau 0
K = "CASE WHEN is_pool THEN 'pool' WHEN src_label IS NULL THEN 'sans_etiquette' WHEN src_label LIKE 'Jupiter%' THEN 'jupiter' WHEN src_label LIKE 'Pont%' OR src_label LIKE 'Service%' THEN 'service' ELSE 'echange' END"
fonds = con.execute(f"SELECT {K}, count(*), count(DISTINCT wallet), sum(sol) FROM {FE} WHERE level=0 AND query='in_before' AND block_time>={Y0} AND block_time<{T0} GROUP BY 1").fetchall()
tf = sum(r[3] for r in fonds)
ff = dict(con.execute(f"""WITH f AS (SELECT wallet, arg_min(src_label, block_time) l FROM {FE} WHERE level=0 AND NOT is_pool AND sol>=0.01 AND block_time<{T0} GROUP BY 1)
                          SELECT CASE WHEN l IS NULL THEN 'sans_etiquette' WHEN l LIKE 'Jupiter%' THEN 'jupiter' WHEN l LIKE 'Pont%' OR l LIKE 'Service%' THEN 'service' ELSE 'echange' END, count(*) FROM f GROUP BY 1""").fetchall())
dbl = one(f"SELECT count(*) FROM (SELECT 1 FROM {FE} GROUP BY wallet, signature, src HAVING count(*)>1)")[0]
F["fonds"] = {"parts": {r[0]: {"n": r[1], "wallets": r[2], "sol": r[3], "pct": 100 * r[3] / tf} for r in fonds}, "total_sol": tf, "premier_financeur": ff, "cles_doublees_apres_k08": dbl,
              "plus_de_100k_sol": one(f"SELECT count(*) FROM {FE} WHERE sol>=100000")[0], "sortie_plus_de_100k": one(f"SELECT count(*) FROM read_parquet('{BIG}/exit_flows.parquet') WHERE amount>=100000 AND asset='SOL'")[0]}

# 7. Sorties à 3 sauts (d48), étiquette vérifiée d'un côté, service et hot présumé de l'autre
ex = json.loads((DATA / "exit_summary.json").read_text())
fr_ = {}
for x in ex.values():
    for k, y in x["frontieres"].items():
        n = k.split(":", 1)[1]
        if "pool" not in n and "Jupiter" not in n:
            fr_[n] = fr_.get(n, 0) + y
serv = sum(v for k, v in fr_.items() if k.startswith("service"))
hot = sum(v for k, v in fr_.items() if k.startswith("hot"))
cex = {k: v for k, v in fr_.items() if not k.startswith(("service", "hot"))}
# la liste des 40 gagnants bouge avec le PnL corrigé : ce que chaque wallet sorti de la liste portait vers un service non nommé
ex0 = json.loads((SOURCES / "exit_summary.json").read_text())
serv_de = lambda x: sum(v for k, v in x["frontieres"].items() if "service non nommé" in k)
F["sorties"] = {"wallets": len(ex), "tronques": sum(1 for x in ex.values() if x["tronque"]), "service_non_nomme_sol": serv, "hot_presume_sol": hot, "echanges": cex, "echanges_sol": sum(cex.values()),
                "service_avant_sol": sum(serv_de(x) for x in ex0.values()), "sortis_de_la_liste": sorted(([a, serv_de(x)] for a, x in ex0.items() if a not in ex), key=lambda r: -r[1]),
                "entres_dans_la_liste": sorted(([a, serv_de(x)] for a, x in ex.items() if a not in ex0), key=lambda r: -r[1])}

# 8. Cohortes, PnL, sommet
excl = f"owner NOT IN (SELECT a FROM ve) AND owner NOT IN (SELECT address FROM {ND} WHERE kind IN ('router','venue','cex','service'))"
for nom, flt in (("tous", "1=1"), ("rapports", excl)):
    c = one(f"""SELECT count(*), sum(CASE WHEN first_buy_time>{HIGH} THEN 1 ELSE 0 END), sum(CASE WHEN first_buy_time>{HIGH} AND realized_sol>0 THEN 1 ELSE 0 END),
                sum(CASE WHEN first_buy_time>{HIGH} AND realized_sol>0.1 THEN 1 ELSE 0 END), sum(CASE WHEN first_buy_time>{HIGH} AND realized_sol>0 AND realized_sol<=0.001 THEN 1 ELSE 0 END),
                sum(CASE WHEN first_buy_time<{WIN} THEN 1 ELSE 0 END), sum(CASE WHEN first_buy_time>={WIN} AND first_buy_time<{LOW} THEN 1 ELSE 0 END), sum(CASE WHEN first_buy_time>={LOW} AND first_buy_time<={HIGH} THEN 1 ELSE 0 END)
                FROM {WP} WHERE {flt}""")
    F[f"cohortes_{nom}"] = dict(zip(("wallets", "apres_musk", "apres_musk_realise_pos", "apres_musk_plus_01", "apres_musk_poussiere", "avant_visuel", "avant_musk", "fenetre"), c))
da = one(f"""WITH a AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time>={WIN} AND block_time<{LOW}),
    b AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{WIN}), c AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time>={WIN - 21600} AND block_time<{WIN})
    SELECT (SELECT count(*) FROM a), (SELECT count(*) FROM a WHERE owner IN (SELECT owner FROM b)), (SELECT count(*) FROM a WHERE owner IN (SELECT owner FROM c))""")
vs = one(f"""WITH v AS (SELECT signature, sum(post-pre) vs FROM vault WHERE vault='3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH' GROUP BY 1)
             SELECT count(*), count(DISTINCT t.signature), coalesce(sum(abs(vs)),0)/1e9 FROM {TR} t JOIN v USING (signature) WHERE t.kind='swap_other' AND vs<>0""")
sg = one(f"""WITH v AS (SELECT signature, sum(post-pre) vs FROM vault WHERE vault='3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH' GROUP BY 1)
             SELECT count(*), coalesce(sum(abs(abs(sol_lamports)-abs(vs))),0)/1e9 FROM {TR} t JOIN v USING (signature) WHERE t.kind='swap' AND t.venue LIKE '%GpMZ%' AND t.n_owners=1""")
F["k03"] = {"swap_other_vault_mobile_n": vs[0], "swap_other_vault_mobile_tx": vs[1], "swap_other_vault_mobile_sol": vs[2], "swap_gpmz_n": sg[0], "swap_gpmz_ecart_sol": sg[1]}
F["deja_acheteurs"] = {"acheteurs": da[0], "deja": da[1], "dans_6h": da[2]}
VD, VS = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
pk = one(f"""WITH t AS (SELECT slot, tx_index, block_time, max(CASE WHEN vault='{VD}' THEN post END) tok, max(CASE WHEN vault='{VS}' THEN post END) sol FROM vault WHERE vault IN ('{VD}','{VS}') AND block_time>=1721606400 AND block_time<1721692800 GROUP BY 1,2,3)
             SELECT (sol/1e9)/(tok/1e6)*1e9, block_time, strftime(to_timestamp(block_time),'%H:%M:%S') FROM t WHERE tok IS NOT NULL AND sol IS NOT NULL ORDER BY sol*1.0/tok DESC LIMIT 1""")
F["sommet"] = {"capitalisation_sol": pk[0], "t": pk[1], "heure": pk[2]}
tt = one(f"SELECT count(*), sum(realized_sol), sum(bought_sol), sum(sold_sol) FROM {WP}")
t0 = one(f"SELECT count(*), sum(realized_sol), sum(bought_sol), sum(sold_sol) FROM {WP0}")
F["totaux"] = {"wallets": tt[0], "realise": tt[1], "achete": tt[2], "vendu": tt[3], "avant": {"wallets": t0[0], "realise": t0[1], "achete": t0[2], "vendu": t0[3]}}
F["groupe"] = {"realise": one(f"SELECT sum(realized_sol) FROM {WP} WHERE owner IN (SELECT a FROM g)")[0], "realise_avant": one(f"SELECT sum(realized_sol) FROM {WP0} WHERE owner IN (SELECT a FROM g)")[0],
               "achete_sol_avant_musk": one(f"SELECT coalesce(sum(-sol_lamports),0)/1e9 FROM {TR} WHERE owner IN (SELECT a FROM g) AND kind='swap' AND token_delta>0 AND block_time<{LOW}")[0],
               "achete_M_avant_musk": one(f"SELECT coalesce(sum(token_delta),0)/1e12 FROM {TR} WHERE owner IN (SELECT a FROM g) AND kind='swap' AND token_delta>0 AND block_time<{LOW}")[0]}
F["wallets"] = {k: {"apres": (one(f"SELECT realized_sol FROM {WP} WHERE owner='{a}'") or [None])[0], "avant": (one(f"SELECT realized_sol FROM {WP0} WHERE owner='{a}'") or [None])[0]} for k, a in {**NOMMES, **AUTRES}.items()}


def top(w, n):
    return [r[0] for r in con.execute(f"""SELECT owner FROM {w} WHERE sold_no_basis_qty <= 0.05*greatest(sold_qty,1) AND transfer_in_qty <= 0.05*greatest(bought_qty+transfer_in_qty,1)
        AND owner NOT IN (SELECT a FROM ve) AND owner NOT IN (SELECT address FROM {n} WHERE kind IN ('router','venue','cex','service')) ORDER BY realized_sol DESC LIMIT 100""").fetchall()]


ta, tb = top(WP0, ND0), top(WP, ND)
F["top100"] = {"communs": len(set(ta) & set(tb)), "top10_identique": ta[:10] == tb[:10], "entrants": [(a, tb.index(a) + 1) for a in tb if a not in ta], "sortants": [(a, ta.index(a) + 1) for a in ta if a not in tb]}

# 9. Petits faits
hb = one(f"SELECT count(*) FROM {ED} WHERE qty>=1000000 AND block_time<{LOW} AND dst<>'(multiple)' AND ((src='{HABP}' AND dst IN (SELECT a FROM g)) OR (dst='{HABP}' AND src IN (SELECT a FROM g)))")[0]
F["habp"] = {"aretes_avec_groupe": hb, "wallets": G0["n"] + (1 if hb else 0), "aretes": G0["edges"] + hb, "solde_T_M": (one(f"SELECT v/1e12 FROM own_T WHERE owner='{HABP}'") or [0])[0]}
F["hx"] = {"M_vers_createur": one(f"SELECT sum(qty)/1e6 FROM {ED} WHERE src='{HX}' AND dst='{CR}'")[0], "qty_jetons": one(f"SELECT sum(qty) FROM {ED} WHERE src='{HX}' AND dst='{CR}'")[0]}
F["labels"] = {"noeuds": dict(con.execute(f"SELECT kind, count(*) FROM {ND} GROUP BY 1").fetchall()), "noeuds_avant": dict(con.execute(f"SELECT kind, count(*) FROM {ND0} GROUP BY 1").fetchall()), "etiquettes": len(load_labels())}
F["groupe_inchange"] = {"membres_identiques": sorted(G0["members"]) == sorted(json.loads((Path("data") / "prevent_groups.json").read_text())[0]["members"]),
                        "aretes_identiques": sorted(e["sig"] for e in G0["edges_top"]) == sorted(e["sig"] for e in json.loads(Path("reports/data_checks/group_edges_check.json").read_text())["group"])}
(DATA / "audit_facts.json").write_text(json.dumps(F, indent=1, ensure_ascii=False, default=str))
print(json.dumps(F, indent=0, ensure_ascii=False, default=str)[:12000])
