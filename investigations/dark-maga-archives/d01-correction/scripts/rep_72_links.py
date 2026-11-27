#!/usr/bin/env python3
"""reports/COORDINATION.md et reports/ATTRIBUTION.md, depuis les données. Chaque signature et adresse vient d'une requête ou d'une archive.

Aucun réseau : les réponses de getTransfersByAddress du 03/11 sont archivées dans reports/data_checks/rep72_reseau.json (code de collecte : historique git).
Textes d'audit repris mot pour mot par dmaga/audit_txt.py.
"""
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from dmaga.audit_txt import AUD, CLAIMS, INTERPRETATION, assertion, ligne_constat, niveau_et_texte, rendu, verifie
from dmaga.db import connect
from dmaga.paths import BIG, DATA

con = connect(mem="700MB")
EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
Q = "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
H3 = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"
GX = "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"
P9 = "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
AF = json.loads((DATA / "audit_facts.json").read_text())
RESEAU = json.loads(Path("reports/data_checks/rep72_reseau.json").read_text())


def ts(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m/%Y %H:%M:%S") if t else "n/d"


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(x) for x in r) + " |" for r in rows])


wal = {r[0]: r[1:] for r in con.execute(f"""SELECT owner, realized_sol, net_sol_all, bought_sol, bought_qty, sold_sol, proceeds_usd, cost_usd, first_buy_time, n_buys, n_sells,
    transfer_in_qty, transfer_out_qty, residual_qty FROM read_parquet('{BIG}/wallets.parquet')""").fetchall()}
groups = json.loads((DATA / "prevent_groups.json").read_text())
G0 = groups[0]
GS = json.loads((DATA / "group_split.json").read_text())
COL = json.loads((DATA / "collector.json").read_text())
PER = AF["perimetres"]
V24 = AF["ventes24"]
tot_float = AF["soldes"]["hors_pools_M"]

tests = json.loads(Path("etude_final/tables/tests.json").read_text())
verdict = json.loads(Path("etude_final/tables/verdict.json").read_text())["verdict"]
assert verdict in INTERPRETATION
fs = json.loads(Path("etude_final/tables/funder_share.json").read_text())
counts = json.loads(Path("etude_final/derived/selection_counts.json").read_text())
SCEN = {r["scenario"]: r for r in csv.DictReader((AUD / "work_D/d11_scenarios.csv").open())}

NAMES = {"M1": "Run-up 3 h", "M2": "Run-up 24 h", "M3": "Part des nouveaux wallets, 24 h", "M4": "Part des 5 premiers, 24 h", "M5": "Synchronisation, 24 h",
         "M6": "Détention des précoces à S", "M7": "Plus gros achat / réserve, 24 h"}
prim = tests["variants"]["primary"]
rows_t = [[m, NAMES[m], f"{v['dmaga']:.3f}", f"{v['median_ctrl']:.3f}", f"{v['p90_ctrl']:.3f}", f"{v['p']:.4f}", v["k"], v["indefinis"], "oui" if tests["holm_primary"].get(m) else "non"] for m, v in prim["mesures"].items()]
r_var = "".join(f"\n- **{name}**, k = {c['k']} : " + ", ".join(f"{m} p={v['p']:.3f}" for m, v in c["mesures"].items()) for name, c in tests["variants"].items() if name != "primary")
s1 = tests["S1"]
rows_s1 = [[n, ts(r["E"]), f"{r['sol_achete']:,.1f}", f"{r['mediane_sol_passe']:,.1f}", f"{r['p_sol']:.3f}", r["nouveaux_wallets"], f"{r['mediane_new_passe']:.0f}", f"{r['p_new']:.3f}", r["n_fenetres_passees"]] for n, r in s1.items()]
rows_scen = [[n, f"{float(r['detection_pct']):.1f} %"] for n, r in SCEN.items()]

G41 = GS["g41"]["address"]
g41_rows = [[ts(x["t"]), f"`{x['dst']}`", x["sol"], "oui" if x["dans_le_groupe"] else "non", "oui" if x["a_achete_sur_le_marche"] else "non", f"`{x['sig']}`"] for x in GS["g41"]["avant_le_mint"]]
salve_rows = [[c["salve"], ts(c["t"]), f"`{c['wallet']}`", c["sol"], "créateur" if c["createur"] else "groupe" if c["groupe"] else "autre", "oui" if c["signe_par_expediteur"] else "non", f"`{c['signature']}`"] for c in COL["salves"]]
edges = [[ts(e["t"]), f"`{e['src']}`", f"`{e['dst']}`", f"{e['M']:,.3f}", f"`{e['sig']}`"] for e in G0["edges_top"]]
g_rows = [[i + 1, g["n"], g["edges"], f"{g['held_before_musk_M']:,.1f}", f"{100 * g['held_before_musk_M'] / tot_float:.1f} %", f"{g['bought_M']:,.1f}", f"{g['bought_sol']:,.1f}", f"{g['realized_sol']:,.0f}", f"{g['net_sol']:,.0f}", f"{g['proceeds_usd'] - g['cost_usd']:,.0f}"] for i, g in enumerate(groups[:12])]
members = [[f"`{m}`", f"{wal[m][2]:,.2f}" if m in wal else "n/d", f"{wal[m][3] / 1e6:,.2f}" if m in wal else "n/d", f"{wal[m][0]:,.1f}" if m in wal else "n/d", f"{wal[m][10] / 1e6:,.1f}" if m in wal else "n/d", f"{wal[m][11] / 1e6:,.1f}" if m in wal else "n/d", ts(wal[m][7]) if m in wal else "n/d"] for m in sorted(G0["members"], key=lambda m: wal[m][7] if m in wal and wal[m][7] else 9e12)]

senders = {r["sender"] for r in csv.DictReader((AUD / "work_D/d20_senders.csv").open())}
serie = [r for r in csv.DictReader((AUD / "work_C/cb_window.csv").open()) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
serie_rows = [[r["utc"][11:19], r["hot"], f"`{r['dest']}`", r["sol"], "oui" if r["dest"] in senders else "non", "oui" if r["dest"] in G0["members"] else "non", f"`{r['sig']}`"] for r in sorted(serie, key=lambda r: r["utc"])]

fs_txt = (f"**Exploratoire, hors plan gelé.** Part des 50 premiers gros acheteurs qui partagent un financeur direct non service, dans les 72 h avant leur premier achat : "
          f"DMAGA {fs['dmaga']['part']:.2f} ({fs['dmaga']['n_financeurs_communs']} financeur(s) commun(s)), médiane des {fs['k']} comparateurs tirés au hasard {fs['mediane_comparateurs']:.2f}, p de rang {fs['p_rang']:.3f}. "
          "Ce test n'entre pas dans le verdict et n'a pas de correction. Arithmétique juste, mesure non recalculable : les réponses réseau n'ont pas été gardées (C46).")

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
VERD = Counter(r["verdict"] for c, r in CLAIMS.items() if c.startswith("C"))
ENCADRE = "**Audit du 03/11 : NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent.** Voir `audits/2026-11-03/`."

coord = f"""# Coordination : tests et liens financiers

Généré par `scripts/rep_72_links.py`. {ENCADRE} Une arête prouve qu'une transaction existe. Elle ne prouve ni un propriétaire unique ni une intention. Dérivé corrigé : `data_v2/`.

## 1. Test gelé : DMAGA contre les autres pics tardifs
Plan gelé le 02/11/2026 à 23:47 UTC avant le calcul des mesures (`etude_final/analysis_plan.md`, `PROTOCOL.lock`). Amendement 001 : R1 et R2 réduits, sans effet sur le verdict, décision de Benjamin en attente (amendement 002). L'installation du projet d'amendement 003 reste en attente aussi.

**Verdict calculé par le code : {verdict}**

@@INTERPRETATION@@

Comptage : {json.dumps({k: v for k, v in counts.items() if k != 'parse'}, ensure_ascii=False)}. Rejets du parseur : {json.dumps(counts.get('parse', {}), ensure_ascii=False)}.

{table(["Mesure", "Définition", "DMAGA", "Médiane pairs", "P90 pairs", "p de rang", "k", "Indéfinis", "Passe Holm"], rows_t)}

Unité : le token. Fenêtres fixées par le pic S de chaque token (DMAGA : 21/07/2024 19:00 UTC). n effectif prudent : {prim['jours_de_pic_distincts']} jours de pic distincts. Le choix des mesures a pu être influencé par ce qui avait déjà été vu de DMAGA, jamais par les comparateurs. Variantes partielles, sans valeur de robustesse sur la bande, jamais utilisées pour conclure :{r_var}

### Puissance sur les vraies données (exploratoire, hors registre)
Simulation de l'audit D, chaque token cible à son tour (`audits/2026-11-03/work_D/d11_scenarios.csv`). Le verdict ne bascule que si DMAGA dépasse tous les pairs sur au moins une mesure. M3 et M4 ne peuvent pas ouvrir. Niveau réel {float(SCEN['nul']['detection_pct']):.1f} %.

{table(["Scénario", "Détection"], rows_scen)}

### DMAGA contre son propre passé (secondaire, Holm séparé, peu discriminant)
{table(["Événement", "Heure E (UTC)", "SOL acheté sur [E−3 h, E)", "Médiane du passé", "p", "Nouveaux acheteurs", "Médiane du passé", "p", "Fenêtres du passé"], rows_s1)}

### Financeur commun
{fs_txt}

### Chiffres descriptifs juste avant Musk
Voir `windows.csv` et `reports/EARLY_BUYERS.md`. Entre l'annonce de Biden et la borne basse du changement de photo ({bm['hours']} h) : {bm['buy_sol']} SOL d'achats contre {bm['sell_sol']} SOL de ventes, {bm['new_buyers']} nouveaux acheteurs. Le groupe ci-dessous fait {quiet[3]} swap(s) entre le visuel et la borne haute. Ces chiffres ne départagent pas une connaissance préalable : un détenteur existant n'a pas besoin d'acheter.

## 2. Groupes reliés par transferts directs de DMAGA avant Musk
Règle : transfert direct d'au moins 1 M de jetons avant le 21/07/2024 19:03:27 UTC, sans passer par un service. Liens de SOL exclus de ce tableau. Jetons détenus par tous les non-pools à cette heure : {tot_float:,.0f} M. Les colonnes « toute la vie » couvrent tout l'historique des wallets, pas la période d'avant Musk.

{table(["#", "Wallets", "Arêtes", "Détenu avant Musk M", "Part des jetons hors pools", "Acheté M, toute la vie", "SOL engagé, toute la vie", "Réalisé SOL", "Flux net SOL", "P&L USD"], g_rows)}

## 3. Le premier groupe : {G0['n']} wallets, niveaux distincts
Descriptif, hors plan gelé : le seuil de 1 M a été choisi après avoir vu DMAGA. Le créateur n'en fait pas partie (voir plus bas).
- **A, les transferts :** {G0['edges']} transferts directs d'au moins 1 M, chacun relu sur la chaîne, la source signe sans programme d'échange (`reports/data_checks/group_edges_check.json`). Ces {G0['edges']} relectures datent du 03/11, elles n'ont pas été refaites : leurs signatures sont identiques à celles du dérivé corrigé.
- **Plafond, pas une mesure :** {PER['groupe']['M']:,.2f} M détenus avant Musk, {PER['groupe']['pct']:.1f} % des {tot_float:,.0f} M hors pools. Le groupe tient par une arête égale au seuil (`NxtXcmEW… → GFpqfj…`, 1.000 M). Au-dessus du seuil, il se coupe en {GS['seuil_strict_tailles'][0]} et {GS['seuil_strict_tailles'][1]} wallets. Achats réels avant 19:03:27 : {AF['groupe']['achete_M_avant_musk']:,.1f} M pour {AF['groupe']['achete_sol_avant_musk']:,.1f} SOL.
- **B, {PER['coeur_n']} wallets, {PER['coeur_M']:,.1f} M, de {PER['coeur_sans_faibles_pct']:.1f} à {PER['coeur_pct']:.1f} % :** plusieurs éléments indépendants concordent : les transferts ; le financement de 0,5 SOL avant le mint par `{G41}` ; une sortie commune en salves de moins de 3 minutes (ci-dessous). Ce niveau est une moyenne : `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` et `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` n'ont que des liens faibles, sans eux {PER['coeur_sans_faibles_M']:,.1f} M.
- **C, {PER['faibles4_n']} wallets, {PER['faibles4_M']:,.1f} M :** autour de `Ei5yGz8…`, reliés au reste par une seule transaction.
- **C, un seul propriétaire pour les {G0['n']} :** non établi. Avant le mint, le SOL entre membres ne relie que 7 et 2 wallets, en 2 composantes séparées, dès le 17/05 et le 10/04/2024.
- **`Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` :** il sort du groupe par la règle de service, à cause de ses envois de poussière. Avec la règle écrite, le groupe compte {AF['habp']['wallets']} wallets et {AF['habp']['aretes']} arêtes. Son solde à la borne basse vaut {AF['habp']['solde_T_M']:,.2f} M : les {PER['groupe']['M']:,.2f} M ne changent pas.
- **Tôt :** {GS['acheteurs_premiere_heure']} des {G0['n']} achètent en première heure, {first_h[2]:,.1f} M pour {first_h[0]:,.1f} SOL. Les autres entrent plus tard ou reçoivent leurs jetons.
- **{quiet[3]} swap entre le visuel de Winig et la borne haute du changement de photo.** Ses gestes du jour précèdent le visuel : répartition 07:57-08:33 UTC, transfert à 11:10, regroupement de 25,5 M à 14:22-14:25.
- **Ventes :** {after6[1]:,.1f} SOL dans les 6 h après Musk, {after24[1]:,.1f} SOL dans les 18 h suivantes. Ces {V24['groupe_sol']:,.0f} SOL en 24 h font **au moins {V24['part_pct']:.1f} % des {V24['marche_sol']:,.0f} SOL vendus sur le marché, {V24['part_elargie_pct']:.1f} % avec {V24['destinataires_vendeurs']} destinataires** de ses {V24['transferts_n']} transferts sortants ({V24['transferts_M']:,.1f} M vers {V24['destinataires']} wallets). Swaps plus transferts, base commune : {V24['groupe_sortie_pct']:.1f} % du détenu contre {V24['autres_sortie_bas_pct']:.1f} à {V24['autres_sortie_haut_pct']:.1f} % pour les {V24['autres_n']} autres détenteurs d'au moins 1 M (exploratoire). Sur les seuls swaps : {V24['groupe_swap_pct']:.1f} % contre {V24['autres_swap_pct']:.1f} %, une comparaison asymétrique à ne pas lire seule.
- **Total sur la durée :** {G0['proceeds_usd']:,.0f} $ reçus pour {G0['cost_usd']:,.0f} $ dépensés.
- Contient `5QhJJc…`, le wallet de la capture de @ramonos (URL @0xRamonos).
- **Explications alternatives :** un groupe de personnes qui se partagent des jetons, sans propriétaire unique ; des ventes de gré à gré ; un même service de gestion. Aucun nom n'est établi.

### Financement avant le mint : `{G41}`
Wallet actif depuis {ts(GS['g41']['first_tx'])[:10]}, financé par ses propres ventes et par des échanges de jetons. Mint créé le {ts(EV['creation_mint'])} UTC. Virements d'au moins 0,05 SOL de ce wallet, de 24 h avant le mint à 1 h après :

{table(["UTC", "Vers", "SOL", "Dans le groupe", "A acheté sur le marché", "Signature"], g41_rows)}

Virements de 0,5 SOL rapprochés avant le mint vers des wallets sans historique : A pour les virements, **finalité non établie**. Une partie reçoit ensuite des jetons de `GFpqfj…` le 21/07 à 08:00 UTC, sans acheter sur le marché. Premier financeur des membres, sur 33 historiques complets : @@C36@@.

### Autres virements de SOL avant le lancement
{table(["UTC", "De", "Vers", "SOL", "Signature"], RESEAU['prep'])}

## 4. Le périmètre du créateur : la série Coinbase et le compte de dépôt
Deux périmètres à ne pas confondre : le groupe de {G0['n']} relié par transferts de jetons, et le périmètre du créateur relié par la série et le dépôt. Le créateur n'est pas dans les {G0['n']} et n'échange aucun jeton avec eux : {PER['aretes_createur_groupe']} arête. {PER['groupe_serie']} des {G0['n']} sont dans la série, {PER['groupe_expediteurs']} sont expéditeurs de `{COL['address']}`.

### Série du 14/07/2024 (N01)
@@N01@@. @@N01V@@. Limite : témoin de 4 fenêtres, un seul matin. Le filtre sur les montants a été choisi après avoir vu le créateur, mais le résultat n'en dépend pas.

{table(["UTC", "Hot wallet", "Destinataire", "SOL", "Reverse ensuite à 9W9b", "Dans le groupe", "Signature"], serie_rows)}

Exploratoire. @@N15@@.

### `{COL['address']}` : un compte de dépôt Coinbase (N02, N03)
Sur tout son historique : {COL['n_in']} entrées de {COL['expediteurs']} expéditeurs, {COL['total_in_sol']:,.1f} SOL entrés, {COL['total_out_sol']:,.1f} SOL sortis, dont {COL['part_coinbase_pct']:.1f} % vers Coinbase 1, 2 et 3 : c'est un plancher, 100 % avec les 6 adresses présumées de la même famille (`data_v2/collector.json`, liste séparée `evidence/labels/hot_presume.tsv`, jamais une étiquette vérifiée). Délai médian entre une entrée et la sortie suivante : {COL['delai_median_s']} s.

- **B, le type de compte :** @@N02V@@.
- **B, un même compte de dépôt ; C, un même bénéficiaire :** @@N03@@. @@N03V@@.
- **Limite :** un compte unique tenu pour plusieurs personnes, par un trésorier ou un opérateur payé pour un lancement, reste possible. Seule une réquisition de Coinbase trancherait.

{table(["Salve", "UTC", "Expéditeur", "SOL", "Rôle", "Signe", "Signature"], salve_rows)}

### Deux périmètres, en jetons à la borne basse (N06)
{G0['n']} wallets : {PER['groupe']['M']:,.2f} M. Série de 15 : {PER['serie15']['M']:,.2f} M. {COL['expediteurs']} expéditeurs : {PER['expediteurs48']['M']:,.2f} M. Union de {PER['union']['taille']} adresses : {PER['union']['M']:,.2f} M, {PER['union']['pct']:.1f} %. A pour les soldes, C pour un seul acteur. L'union n'est pas un groupe : elle additionne des périmètres que rien ne relie à coup sûr.

### Transferts directs de DMAGA du groupe, par date
{table(["UTC", "De", "Vers", "Jetons M", "Signature"], edges)}

### Membres
{table(["Wallet", "Acheté SOL, toute la vie", "Acheté M, toute la vie", "Réalisé SOL", "Reçu par transfert M", "Sorti par transfert M", "1er achat"], members)}

## 5. État des relectures
- **Audit du 03/11 (A données, B statistiques, C attribution, D confrontation) :** `audits/2026-11-03/AUDIT_FINAL.md`. Sur {sum(VERD.values())} assertions : {VERD['PASS']} PASS, {VERD['FAIL']} FAIL, {VERD['INCONCLUSIVE']} INCONCLUSIVE. Ces corrections ne sont pas auditées : un nouvel audit des conclusions manque.
- **Reproduction :** les valeurs du test sont retrouvées par trois voies, audits A, B et D. Aucune trace d'une reproduction en copie vierge n'a été trouvée dans le dépôt.
- **Contrôles positifs :** contrôle de la plomberie seulement. Sur les vraies données, nul {float(SCEN['nul']['detection_pct']):.1f} %, effet moyen {float(SCEN['moyen du contrôle (6 wallets, 6 x lognormale, moitié slot)']['detection_pct']):.1f} %, effet fort {float(SCEN['fort du contrôle (18 wallets, 25 x lognormale, moitié slot)']['detection_pct']):.1f} %.
- **Fait avant l'audit :** audit des échecs silencieux avant le gel (5 bloquants, 8 majeurs, 8 mineurs, corrections appliquées, non re-auditées) ; un audit indépendant des conclusions, rendu FAIL.
- **En attente de Benjamin :** amendement 001, projet d'amendement 003, nouvel audit des conclusions.
- **Registre :** voir `python3 ~/.claude/skills/etude-gelee/scripts/registre.py compter etude_final`. Les comparaisons des audits sont exploratoires, hors registre gelé.

## 6. Faux liens écartés
| Lien apparent | Pourquoi il est écarté |
|---|---|
| Le créateur et `9PrmF8…` ont le même premier financeur `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` | Coinbase 3 selon Dune Spellbook. Un même hot wallet n'est pas un lien |
| `H3QsBr…` et `9PrmF8…` envoient des jetons à `9UsmwVmbV4VwEwv5q5iZh4y3THh6dn2cqjFpEUrGRzZJ` | Réserve d'un pool Raydium CLMM : ce sont des ventes |
| `3LoAYHuS…`, `HFqp6ErW…`, `GP8StUXN…`, `3CgvbiM3…`, `7iWnBRRh…` sont reliés à `5QhJJc…`, `9PrmF8…` et `H3QsBr…` | Comptes de pourboire et de frais publiés par Jupiter (`jup-ag/docs`, DefiLlama), archivés dans `evidence/labels/`, classe `service` |
| `Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` envoie du SOL à presque tous | Poussière de 0.0000001 SOL. Reste son arête de 8 M de DMAGA avec `5QhJJc…`, voir section 3 |
| `5QhJJc…` et le créateur envoient des jetons vers `JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy` | Exécutant de Jupiter DCA : signataire, programme `DCA265Vj`, `InitiateFlashFill`. Ce sont deux ordres DCA, pas un destinataire commun |
| Le « créateur » DAS `TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM` commun avec Kekius | Autorité de mint de Pump.fun, présente sur tous ses tokens |
"""
Path("reports/COORDINATION.md").write_text(rendu(coord, INTERPRETATION=INTERPRETATION, C36=verifie("C36").split("Sur 33 historiques complets : ")[1].rstrip("."), N01=assertion("N01"), N01V=verifie("N01"), N15=assertion("N15"),
                                                 N02V=verifie("N02"), N03=assertion("N03"), N03V=verifie("N03")))

rep = []
for name, addr, src in (("9PrmF8", P9, "fils de tiers d'août 2024 et @XHEILIGX, 30/03/2024, voir audits/2026-11-03/work_E/X_FOLLOWUP.md, partie 6"), ("GXZvX", GX, "@ai_9684xtpa, id 1815243177475121253, adresse entière dans le lien"), ("5QhJJc", Q, "@ramonos (URL @0xRamonos), id 1815221876190294470, capture"), ("H3QsBr", H3, "@ashrobin (URL @ashrobinqt), id 1815233925662306427, capture")):
    v = wal[addr]
    rep.append([f"`{addr}`", src, f"{v[2]:,.2f}", f"{v[0]:,.1f}", f"{v[5] - v[6]:,.0f}", ts(v[7]), f"{v[8]}/{v[9]}", f"{v[10] / 1e6:,.2f}", f"{v[11] / 1e6:,.2f}"])
attr = f"""# Attribution : liens vérifiables, hypothèses, niveaux

Généré par `scripts/rep_72_links.py`. {ENCADRE} Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice, **D** non vérifié ou contredit. Aucune identité civile n'est recherchée ni établie. Un wallet cité n'est accusé de rien.

## Conclusion courte
**Aucun lien documenté entre un wallet et un compte du noyau (@DarkMagaCoin, @kikisknees, @Aristos_Revenge, @ChrisWinig).** Aucun de ces comptes n'a publié d'adresse de wallet dans ce qui est archivé (le mint, lui, est publié). Le lien compte ↔ wallet reste une lacune, pas une absence prouvée. Le corpus X est partiel.

## Les quatre pistes
{table(["Wallet", "Source", "Acheté SOL", "Réalisé SOL", "P&L USD", "1er achat UTC", "Ach./Vte", "Reçu transfert M", "Sorti transfert M"], rep)}

- **Les quatre désignent-ils une même entité ?** Non établi, et rien ne le soutient pour `H3QsBr…`, `GXZvX…` et `9PrmF8…` : après retrait des services, aucun transfert direct ne les relie entre eux ni au groupe, et aucun n'envoie vers `{COL['address']}`. Une absence d'arête n'exclut pas un lien par échange : les quatre passent par des échanges (A pour le fait, C pour toute interprétation).
- **Rapprochement des captures :** `5QhJJc…HScd` et `H3QsBr…T6cc` sont uniques parmi les propriétaires de DMAGA pour ce préfixe et ce suffixe. Pour `H3QsBr…`, 1 087 $ recalculés contre 1 086 $ sur la capture et 16,82 M contre 16,8 M (A). Pour `5QhJJc…`, la capture dit 37 transactions et 28,4 M : l'écart avec les 208 achats totaux s'explique en partie par des ordres DCA Jupiter (keepers `DCAK…`) et des transferts (B). La date « 3 jours » du post correspond aux achats DCA du 17 au 19/07, alors que le wallet achetait dès le 14/07.

## Le périmètre du créateur : niveaux distincts
Niveaux scindés depuis l'audit du 03/11 (C19) :
- **A :** les transactions et leurs signataires.
- **B, même opérateur ou même compte de dépôt :** le créateur et {sum(1 for r in serie if r['dest'] in senders) - 1} wallets de la série Coinbase du 14/07/2024.
- **B, type de compte :** `{COL['address']}` est un compte de dépôt Coinbase. Son titulaire n'est pas connu.
- **B, lien de 2025 :** `BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc` et ce compte, par un montant apparié. Sans valeur pour le lancement.
- **C :** les {G0['n']} wallets pris ensemble, avec des grappes antérieures au mint, et un même bénéficiaire derrière le dépôt.
- **Non établi :** qui. @ramonos a seulement commenté `5QhJJc…` : **rien ne le relie à lui ni à personne au-delà de sa publication.**

{table(["UTC", "De", "Vers", "Montant", "Actif", "Ce que c'est", "Signature"], RESEAU['link_rows'])}

En plus de deux ans, le créateur n'a reçu que {RESEAU['creator_in_n']} virements d'au moins 0.003 SOL : @@SOURCES_IN@@. Le virement de `5QhJJc…` arrive 35 secondes avant qu'il ouvre un ordre DCA de vente sur tous ses jetons. Le créateur n'y encaisse presque rien : il déplace sa position (voir plus bas).

**La série de retraits (N01) :** @@N01@@. @@N01V@@.

**Le compte de dépôt (N02, N03) :** @@N02V@@. @@N03@@. @@N03V@@. Salves : @@C17V@@. Chaque virement est signé par son expéditeur (`data_v2/collector.json`, tableau dans `reports/COORDINATION.md`).

**Le lien de 2025 (N04), A pour les transactions, B pour le lien :** @@N04@@. @@N04V@@.

**Aller-retour de position (C-10) :** @@C10@@ Le 13/07/2025, ces {AF['hx']['qty_jetons']:,.0f} jetons reçus de `Hx1UvdgMqZBQRrSAKhSSfc7Hvcb2Mk4dFrcrQpYG6urT`, escrow d'un ordre DCA, passent à `BuHUkjUy…`.

**Ce qui va contre un seul acteur dès le lancement :** un hot wallet sert tout le monde, une clé peut changer de main, et rien n'empêche un tiers d'envoyer vers une adresse.

## Relations documentées (`social_links.parquet`)
Types distincts : `mention_tierce` (un compte commente un wallet), `declaration_publique` (ce qu'un compte affirme), `interaction_sociale` (réponses et mentions). Aucune arête `wallet_revendique` : zéro.
Déclarations de l'équipe, toutes à prendre pour ce qu'elles sont : « $DMAGA pfp by me and @ChrisWinig », « a wartime PFP that we made for him » (@kikisknees) ; « DMAGA team created Elon's pfp specifically for him » (@DarkMagaCoin).

## Hypothèses non retenues
- **« Musk ou ses proches ont organisé »** : D. Aucun élément ne relie un wallet à Musk ou à son entourage. Il a adopté une image publique.
- **« Ansem, deBridge, la Solana Foundation »** (récit de Benjamin du 02/08) : D. Rien dans ces données. Non testé en profondeur : aucune adresse fournie.
"""
Path("reports/ATTRIBUTION.md").write_text(rendu(attr, SOURCES_IN=RESEAU["sources_in"], N01=assertion("N01"), N01V=verifie("N01"), N02V=verifie("N02"), N03=assertion("N03"), N03V=verifie("N03"),
                                                N04=assertion("N04"), N04V=verifie("N04"), C17V=verifie("C17"), C10=ligne_constat("C-10", "**Preuve.**").replace(" Le « non vérifié » du rapport peut tomber.", "")))
print("COORDINATION et ATTRIBUTION écrits", len(RESEAU["prep"]), "virements de préparation,", len(RESEAU["link_rows"]), "lignes de lien")
