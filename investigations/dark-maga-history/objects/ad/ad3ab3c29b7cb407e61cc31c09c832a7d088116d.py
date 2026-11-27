#!/usr/bin/env python3
"""reports/COORDINATION.md et reports/ATTRIBUTION.md, depuis les données. Chaque signature et adresse vient d'une requête."""
import csv
import gzip
import json
from datetime import datetime, timezone
from pathlib import Path

from dmaga.config import BIG, DATA, RAW
from dmaga.db import connect
from dmaga.helius import Helius
from dmaga.labels import label

con = connect()
FLOWS = RAW / "flows"
EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
C = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
Q = "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
H3 = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"
GX = "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"
P9 = "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
NATIVE = "So11111111111111111111111111111111111111111"
MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
h = Helius(rps=4)


def ts(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m/%Y %H:%M:%S") if t else "n/d"


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(x) for x in r) + " |" for r in rows])


def lab(a):
    return label(a) or ""


wal = {r[0]: r[1:] for r in con.execute(f"""SELECT owner, realized_sol, net_sol_all, bought_sol, bought_qty, sold_sol, proceeds_usd, cost_usd, first_buy_time, n_buys, n_sells,
    transfer_in_qty, transfer_out_qty, residual_qty FROM read_parquet('{BIG}/wallets.parquet')""").fetchall()}
groups = json.loads((DATA / "prevent_groups.json").read_text())
G0 = groups[0]
tot_float = 938.0

tests = {}
p = Path("etude_final/tables/tests.json")
if p.exists():
    tests = json.loads(p.read_text())
verdict = json.loads(Path("etude_final/tables/verdict.json").read_text())["verdict"] if Path("etude_final/tables/verdict.json").exists() else "NON CALCULÉ"
fs = json.loads(Path("etude_final/tables/funder_share.json").read_text()) if Path("etude_final/tables/funder_share.json").exists() else None
counts = json.loads(Path("etude_final/derived/selection_counts.json").read_text()) if Path("etude_final/derived/selection_counts.json").exists() else {}

NAMES = {"M1": "Run-up 3 h", "M2": "Run-up 24 h", "M3": "Part des nouveaux wallets, 24 h", "M4": "Part des 5 premiers, 24 h", "M5": "Synchronisation, 24 h",
         "M6": "Détention des précoces à S", "M7": "Plus gros achat / réserve, 24 h"}
rows_t, r_var = [], ""
if tests.get("variants", {}).get("primary"):
    prim = tests["variants"]["primary"]
    for m, v in prim["mesures"].items():
        rows_t.append([m, NAMES[m], f"{v['dmaga']:.3f}", f"{v['median_ctrl']:.3f}", f"{v['p90_ctrl']:.3f}", f"{v['p']:.4f}", v["k"], v["indefinis"], "oui" if tests["holm_primary"].get(m) else "non"])
    for name, c in tests["variants"].items():
        if name != "primary":
            r_var += f"\n- **{name}**, k = {c['k']} : " + ", ".join(f"{m} p={v['p']:.3f}" for m, v in c["mesures"].items())
s1 = tests.get("S1", {})
rows_s1 = [[n, ts(r["E"]), f"{r['sol_achete']:,.1f}", f"{r['mediane_sol_passe']:,.1f}", f"{r['p_sol']:.3f}", r["nouveaux_wallets"], f"{r['mediane_new_passe']:.0f}", f"{r['p_new']:.3f}", r["n_fenetres_passees"]] for n, r in s1.items()]

# préparation et consolidation : virements de SOL avant le lancement, relus sur la chaîne
prep = []
# adresse vue tronquée à l'écran : résolue depuis les virements réels, jamais retapée
G41 = {x["fromUserAccount"] for x in h.call("getTransfersByAddress", ["AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5", {"direction": "in", "mint": NATIVE, "limit": 20, "sortOrder": "asc"}])["data"]
       if x["fromUserAccount"] and x["fromUserAccount"].startswith("G41vRrsHSh")}
assert len(G41) == 1, G41
G41 = G41.pop()
for a, b in (("74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb", "6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M"),
             ("AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk", "6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M"),
             ("6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M", "8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh"),
             ("6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M", "99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb"),
             ("6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk"),
             (G41, "AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5"),
             (G41, "GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p")):
    try:
        r = h.call("getTransfersByAddress", [b, {"with": a, "direction": "in", "mint": NATIVE, "limit": 100, "sortOrder": "asc", "filters": {"blockTime": {"lt": 1720926325}, "amount": {"gte": 50_000_000}}}])["data"]
    except Exception as e:
        print("échec", a[:8], b[:8], repr(e))
        continue
    for x in r:
        if x["blockTime"] > 1720800000:
            prep.append([ts(x["blockTime"]), f"`{x['fromUserAccount']}`", f"`{x['toUserAccount']}`", x["uiAmount"], f"`{x['signature']}`"])
prep.sort(key=lambda r: r[0])

edges = [[ts(e["t"]), f"`{e['src']}`", f"`{e['dst']}`", f"{e['M']:,.3f}", f"`{e['sig']}`"] for e in G0["edges_top"]]
g_rows = [[i + 1, g["n"], g["edges"], f"{g['held_before_musk_M']:,.1f}", f"{100 * g['held_before_musk_M'] / tot_float:.1f} %", f"{g['bought_M']:,.1f}", f"{g['bought_sol']:,.1f}", f"{g['realized_sol']:,.0f}", f"{g['net_sol']:,.0f}", f"{g['proceeds_usd'] - g['cost_usd']:,.0f}"] for i, g in enumerate(groups[:12])]
members = [[f"`{m}`", f"{wal[m][2]:,.2f}" if m in wal else "n/d", f"{wal[m][3] / 1e6:,.2f}" if m in wal else "n/d", f"{wal[m][0]:,.1f}" if m in wal else "n/d", f"{wal[m][10] / 1e6:,.1f}" if m in wal else "n/d", f"{wal[m][11] / 1e6:,.1f}" if m in wal else "n/d", ts(wal[m][7]) if m in wal else "n/d"] for m in sorted(G0["members"], key=lambda m: wal[m][7] if m in wal and wal[m][7] else 9e12)]

fs_txt = "Non calculé."
if fs:
    fs_txt = (f"**Exploratoire, hors plan gelé.** Part des 50 premiers gros acheteurs qui partagent un financeur direct non service, dans les 72 h avant leur premier achat : "
              f"DMAGA {fs['dmaga']['part']:.2f} ({fs['dmaga']['n_financeurs_communs']} financeur(s) commun(s)), médiane des {fs['k']} comparateurs tirés au hasard {fs['mediane_comparateurs']:.2f}, p de rang {fs['p_rang']:.3f}. "
              "Ce test n'entre pas dans le verdict et n'a pas de correction.")

con.execute("CREATE TEMP TABLE g0(a VARCHAR)")
con.executemany("INSERT INTO g0 VALUES (?)", [[m] for m in G0["members"]])


def g_sum(a, b):
    return con.execute(f"""SELECT coalesce(sum(CASE WHEN token_delta>0 THEN -sol_lamports END),0)/1e9, coalesce(sum(CASE WHEN token_delta<0 THEN sol_lamports END),0)/1e9,
        coalesce(sum(CASE WHEN token_delta>0 THEN token_delta END),0)/1e12, count(*) FROM trades WHERE kind='swap' AND block_time>={a} AND block_time<{b} AND owner IN (SELECT a FROM g0)""").fetchone()


first_h = g_sum(EV["creation_mint"], EV["creation_mint"] + 3600)
quiet = g_sum(EV["winig_visuel"], EV["musk_borne_haute"] + 1)
after6 = g_sum(EV["musk_borne_haute"], EV["musk_borne_haute"] + 6 * 3600)
after24 = g_sum(EV["musk_borne_haute"] + 6 * 3600, EV["musk_borne_haute"] + 24 * 3600)
win_rows = {w["window"]: w for w in csv.DictReader((DATA / "windows.csv").open())}
bm = win_rows["biden_a_musk_borne_basse"]

coord = f"""# Coordination : tests et liens financiers

Généré par `scripts/rep_72_links.py`. Une arête prouve qu'une transaction existe. Elle ne prouve ni un propriétaire unique ni une intention.

## 1. Test gelé : DMAGA contre les autres pics tardifs
Plan gelé le 02/11/2026 à 23:47 UTC avant tout calcul (`etude_final/analysis_plan.md`, `PROTOCOL.lock`). Amendement 001 : R1 et R2 réduits, sans effet sur le verdict.

**Verdict calculé par le code : {verdict}**

Comptage : {json.dumps({k: v for k, v in counts.items() if k != 'parse'}, ensure_ascii=False)}. Rejets du parseur : {json.dumps(counts.get('parse', {}), ensure_ascii=False)}.

{table(["Mesure", "Définition", "DMAGA", "Médiane pairs", "P90 pairs", "p de rang", "k", "Indéfinis", "Passe Holm"], rows_t) if rows_t else "Tests non calculés."}

Unité : le token. Fenêtres fixées par le pic S de chaque token (DMAGA : 21/07/2024 19:00 UTC). n effectif prudent : {tests.get('variants', {}).get('primary', {}).get('jours_de_pic_distincts', 'n/d')} jours de pic distincts. Le choix des mesures a pu être influencé par ce qui avait déjà été vu de DMAGA, jamais par les comparateurs. Variantes, jamais utilisées pour conclure :{r_var or ' non calculées.'}

### DMAGA contre son propre passé (secondaire, Holm séparé)
{table(["Événement", "Heure E (UTC)", "SOL acheté sur [E−3 h, E)", "Médiane du passé", "p", "Nouveaux acheteurs", "Médiane du passé", "p", "Fenêtres du passé"], rows_s1) if rows_s1 else "Non calculé."}

### Financeur commun
{fs_txt}

### Chiffres qui vont contre une ruée informée juste avant Musk
Voir `data/windows.csv` et `reports/EARLY_BUYERS.md`. Entre l'annonce de Biden et la borne basse du changement de photo ({bm['hours']} h) : {bm['buy_sol']} SOL d'achats contre {bm['sell_sol']} SOL de ventes, {bm['new_buyers']} nouveaux acheteurs. Le groupe ci-dessous fait {quiet[3]} swap(s) entre le visuel et la borne haute.

## 2. Groupes reliés par transferts directs de DMAGA avant Musk
Règle : transfert direct d'au moins 1 M de jetons avant le 21/07/2024 19:03:27 UTC, sans passer par un service. Liens de SOL exclus de ce tableau. Jetons détenus par tous les non-pools à cette heure : {tot_float:,.0f} M.

{table(["#", "Wallets", "Arêtes", "Détenu avant Musk M", "Part des jetons hors pools", "Acheté M", "SOL engagé", "Réalisé SOL", "Flux net SOL", "P&L USD"], g_rows)}

## 3. Le groupe n° 1 : {G0['n']} wallets, niveau B
- **{G0['held_before_musk_M']:,.1f} M de jetons avant Musk.** En première heure, le groupe achète {first_h[2]:,.1f} M de jetons pour {first_h[0]:,.1f} SOL.
- **{quiet[3]} swap entre le visuel de Winig et la borne haute du changement de photo.** Son geste du jour se fait avant : répartition le 21/07 entre 07:57 et 08:33 UTC.
- **Ventes :** {after6[1]:,.1f} SOL dans les 6 h après Musk, {after24[1]:,.1f} SOL dans les 18 h suivantes. Total sur la durée : {G0['proceeds_usd']:,.0f} $ reçus pour {G0['cost_usd']:,.0f} $ dépensés.
- Contient `5QhJJc…`, le wallet de la capture de @0xRamonos. Chacune des {G0['edges']} arêtes a été relue sur la chaîne : la source signe, sans programme d'échange (`reports/data_checks/group_edges_check.json`).
- **Explications alternatives :** un groupe de personnes qui se partagent des jetons, sans propriétaire unique ; des ventes de gré à gré ; un chemin qui rassemble des wallets sans rapport par une ou deux arêtes, notamment `5QhJJc → 7mdCAs8C` ou `NxtXcm → GFpqfj`. Aucun nom n'est établi.

### Préparation : virements de SOL autour du lancement
Création du mint : {ts(EV['creation_mint'])} UTC.

{table(["UTC", "De", "Vers", "SOL", "Signature"], prep)}

### Transferts directs de DMAGA du groupe, par date
{table(["UTC", "De", "Vers", "Jetons M", "Signature"], edges)}

### Membres
{table(["Wallet", "Acheté SOL", "Acheté M", "Réalisé SOL", "Reçu par transfert M", "Sorti par transfert M", "1er achat"], members)}

## 4. Faux liens écartés
| Lien apparent | Pourquoi il est écarté |
|---|---|
| Le créateur et `9PrmF8…` ont le même premier financeur `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` | Coinbase 3 selon Dune Spellbook. Rupture de traçabilité, pas un lien |
| `H3QsBr…` et `9PrmF8…` envoient des jetons à `9UsmwVmbV4VwEwv5q5iZh4y3THh6dn2cqjFpEUrGRzZJ` | Réserve d'un pool Raydium CLMM : ce sont des ventes |
| `3LoAYHuS…`, `HFqp6ErW…`, `GP8StUXN…`, `3CgvbiM3…`, `7iWnBRRh…` sont reliés à `5QhJJc…`, `9PrmF8…` et `H3QsBr…` | Comptes publiés par Jupiter (`jup-ag/docs`, DefiLlama), archivés dans `evidence/labels/`. Ce sont des jambes de routage |
| `Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` envoie du SOL à presque tous | Poussière de 0,0000001 SOL. Reste son arête de 8 M de DMAGA avec `5QhJJc…` |
| `5QhJJc…` et le créateur envoient des jetons vers `JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy` | Exécutant de Jupiter DCA : signataire, programme `DCA265Vj`, `InitiateFlashFill`. Ce sont deux ordres DCA, pas un destinataire commun |
| Le « créateur » DAS `TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM` commun avec Kekius | Autorité de mint de Pump.fun, présente sur tous ses tokens |
"""
Path("reports/COORDINATION.md").write_text(coord)

gas = h.call("getTransfersByAddress", [C, {"with": Q, "limit": 100, "sortOrder": "asc"}])["data"]
moved = h.call("getTransfersByAddress", [C, {"mint": MINT, "direction": "out", "limit": 100, "sortOrder": "asc"}])["data"]
creator_in = h.call("getTransfersByAddress", [C, {"direction": "in", "mint": NATIVE, "limit": 100, "sortOrder": "asc", "filters": {"amount": {"gte": 3_000_000}}}])["data"]
q_first = h.call("getTransfersByAddress", [Q, {"direction": "in", "mint": NATIVE, "limit": 1, "sortOrder": "asc"}])["data"][0]
SY = "sYBdq543ZX4iAXpNzhT4kTvKBaEDUGkiUo9jBFYdaNd"
qs = h.call("getTransfersByAddress", [SY, {"with": Q, "mint": MINT, "limit": 20, "sortOrder": "asc"}])["data"]
link_rows = []
for x, why in [(creator_in[0], "Le créateur reçoit de Coinbase 3, premier mouvement du wallet"), (q_first, "`5QhJJc…` reçoit de Coinbase 2, 8 min 27 s plus tard, premier mouvement du wallet"),
               (gas[0], "**`5QhJJc…` signe seul un virement de SOL vers le créateur, 35 s avant la ligne suivante**"),
               (moved[0], "Le créateur signe un ordre Jupiter DCA de vente sur tous ses jetons ; le destinataire est l'escrow de l'ordre")] + [(x, "`5QhJJc…` avait ouvert un ordre DCA du même type, 4,5 mois plus tôt") for x in qs[:1]]:
    link_rows.append([ts(x["blockTime"]), f"`{x['fromUserAccount']}`", f"`{x['toUserAccount']}`", x["uiAmount"], "SOL" if x.get("mint") == NATIVE else "DMAGA", why, f"`{x['signature']}`"])
link_rows.sort(key=lambda r: datetime.strptime(r[0], "%d/%m/%Y %H:%M:%S"))
sources_in = ", ".join(f"{x['uiAmount']} SOL de {lab(x['fromUserAccount']) or x['fromUserAccount'][:8] + '…'} ({ts(x['blockTime'])[:10]})" for x in creator_in)

rep = []
for name, addr, src in (("9PrmF8", P9, "mission ; source sociale non retrouvée"), ("GXZvX", GX, "@ai_9684xtpa, id 1815243177475121253, adresse entière dans le lien"), ("5QhJJc", Q, "@0xRamonos, id 1815221876190294470, capture"), ("H3QsBr", H3, "@ashrobinqt, id 1815233925662306427, capture")):
    v = wal[addr]
    rep.append([f"`{addr}`", src, f"{v[2]:,.2f}", f"{v[0]:,.1f}", f"{v[5] - v[6]:,.0f}", ts(v[7]), f"{v[9]}/{v[8]}", f"{v[10] / 1e6:,.2f}", f"{v[11] / 1e6:,.2f}"])
attr = f"""# Attribution : liens vérifiables, hypothèses, niveaux

Généré par `scripts/rep_72_links.py`. Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice, **D** non vérifié ou contredit. Aucune identité civile n'est recherchée ni établie. Un wallet cité n'est accusé de rien.

## Conclusion courte
**Aucun lien documenté entre un wallet et un compte du noyau (@DarkMagaCoin, @kikisknees, @Aristos_Revenge, @ChrisWinig).** Aucun de ces comptes n'a publié d'adresse dans ce qui est archivé. Le lien compte ↔ wallet reste une lacune, pas une absence prouvée. Le corpus X est partiel.

## Les quatre pistes publiques
{table(["Wallet", "Source", "Acheté SOL", "Réalisé SOL", "P&L USD", "1er achat UTC", "Ach./Vte", "Reçu transfert M", "Sorti transfert M"], rep)}

- **Les quatre désignent-ils une même entité ?** Non établi, et rien ne le soutient pour `H3QsBr…`, `GXZvX…` et `9PrmF8…` : après retrait des services, aucun chemin direct ne les relie entre eux ni au groupe de lancement (`H3QsBr…` n'a aucune arête directe, `GXZvX…` une seule voisine, `9PrmF8…` une petite composante de 9 wallets). Une absence d'arête n'exclut pas un lien par échange : les quatre passent par des échanges (A pour le fait, C pour toute interprétation).
- **Rapprochement des captures :** `5QhJJc…HScd` et `H3QsBr…T6cc` sont uniques parmi les propriétaires de DMAGA pour ce préfixe et ce suffixe. Pour `H3QsBr…`, 1 087 $ recalculés contre 1 086 $ sur la capture et 16,82 M contre 16,8 M (A). Pour `5QhJJc…`, la capture dit 37 transactions et 28,4 M : l'écart avec les 208 achats totaux s'explique en partie par des ordres DCA Jupiter (keepers `DCAK…`) et des transferts (B). La date « 3 jours » du post correspond aux achats DCA du 17 au 19/07, alors que le wallet achetait dès le 14/07.

## Lien entre le créateur et `5QhJJc…` : A pour la transaction, B pour une action concertée en 2025, C pour un acteur unique au lancement
{table(["UTC", "De", "Vers", "Montant", "Actif", "Ce que c'est", "Signature"], link_rows)}

En plus de deux ans, le créateur n'a reçu que {len(creator_in)} virements d'au moins 0,003 SOL : {sources_in}. Le virement de `5QhJJc…` arrive 35 secondes avant qu'il vide sa position.
- **Vérifié (A) :** ces transactions et leurs signataires (`reports/data_checks/group_edges_check.json`).
- **Fortement corroboré (B) :** en juillet 2025, celui qui contrôle `5QhJJc…` et celui qui contrôle le wallet créateur agissent ensemble, ou sont la même personne.
- **Indice seulement (C) :** qu'ils étaient déjà le même acteur au lancement. Les deux financements Coinbase à 8 minutes d'écart, 33 et 25 minutes avant la création, vont dans ce sens, mais un hot wallet sert tout le monde. Une clé peut aussi changer de main en un an. L'usage commun de Jupiter DCA ne vaut rien seul : l'outil est répandu.
- **Ce qui n'est pas établi :** qui. @0xRamonos a seulement commenté ce wallet : **rien ne le relie à lui ni à personne au-delà de sa publication.**

## Relations documentées (`data/social_links.parquet`)
Types distincts : `mention_tierce` (un compte commente un wallet), `declaration_publique` (ce qu'un compte affirme), `interaction_sociale` (réponses et mentions). Aucune arête `wallet_revendique` : zéro.
Déclarations de l'équipe, toutes à prendre pour ce qu'elles sont : « $DMAGA pfp by me and @ChrisWinig », « a wartime PFP that we made for him » (@kikisknees) ; « DMAGA team created Elon's pfp specifically for him » (@DarkMagaCoin).

## Hypothèses non retenues
- **« Musk ou ses proches ont organisé »** : D. Aucun élément ne relie un wallet à Musk ou à son entourage. Il a adopté une image publique.
- **« Ansem, deBridge, la Solana Foundation »** (récit de Benjamin du 02/08) : D. Rien dans ces données. Non testé en profondeur : aucune adresse fournie.
"""
Path("reports/ATTRIBUTION.md").write_text(attr)
print("COORDINATION et ATTRIBUTION écrits", len(prep), "virements de préparation,", len(link_rows), "lignes de lien")
