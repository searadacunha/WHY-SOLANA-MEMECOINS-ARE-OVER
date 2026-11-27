#!/usr/bin/env python3
"""Rapports chiffrés générés depuis les données : TOP_TRADERS, EARLY_BUYERS.

Rien n'est retapé à la main : chaque adresse et chaque signature vient d'une requête. Les fichiers viennent de BIG et DATA (dmaga/paths.py), donc data_v2 après l'audit du 03/11.
"""
import json
import os
from datetime import datetime, timezone

from dmaga.db import connect
from dmaga.frfmt import fr
from dmaga.paths import BIG, DATA
from dmaga.venues import load as load_venues

EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
T_WINIG, T_LOW, T_HIGH = EV["winig_visuel"], EV["musk_borne_basse"], EV["musk_borne_haute"]
AF = json.loads((DATA / "audit_facts.json").read_text())
RT = json.loads((DATA / "roundtrip.json").read_text())
S1_WIN = json.loads(open("etude_final/tables/tests.json").read())["S1"]["winig"]["sol_achete"]
venues = set(load_venues())
con = connect(mem="700MB")
con.execute(f"CREATE VIEW w0 AS SELECT * FROM read_parquet('{BIG}/wallets.parquet')")
con.execute(f"CREATE VIEW n AS SELECT * FROM read_parquet('{BIG}/nodes.parquet')")
con.execute(f"CREATE VIEW bots AS SELECT * FROM read_parquet('{BIG}/bots.parquet') WHERE bot_aller_retour")
excl = sorted(venues | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"})
con.execute("CREATE TEMP TABLE excl(a VARCHAR)")
con.executemany("INSERT INTO excl VALUES (?)", [[a] for a in excl])
con.execute("""CREATE VIEW w AS SELECT *,
                 (sold_no_basis_qty <= 0.05*greatest(sold_qty,1) AND transfer_in_qty <= 0.05*greatest(bought_qty+transfer_in_qty,1)) AS cost_known
               FROM w0 WHERE owner NOT IN (SELECT a FROM excl)
               AND owner NOT IN (SELECT address FROM n WHERE kind IN ('router','venue','cex','service'))""")
bots = {r[0] for r in con.execute("SELECT owner FROM bots").fetchall()}


def ts(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m %H:%M:%S") if t else "n/d"


def cohort(t):
    if t is None:
        return "aucun achat"
    if t < T_WINIG:
        return "avant visuel"
    if t < T_LOW:
        return "avant Musk"
    if t <= T_HIGH:
        return "fenêtre Musk"
    return "après Musk"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def wal(a):
    return f"`{a}` (bot_aller_retour)" if a in bots else f"`{a}`"


REF = con.execute("SELECT max(valuation_ref_time) FROM w0").fetchone()[0]
totals = con.execute("SELECT count(*), sum(bought_sol), sum(sold_sol), sum(realized_sol), sum(cost_usd), sum(proceeds_usd) FROM w").fetchone()
n_all = con.execute("SELECT count(*) FROM w0").fetchone()[0]
R = AF["ruptures"]
RES = AF["residuels"]

# ---- TOP_TRADERS
top = con.execute("""SELECT owner, realized_sol, net_sol_all, bought_sol, sold_sol, cost_usd, proceeds_usd, n_buys, n_sells, residual_qty,
                     residual_value_sol_at_cutoff, first_buy_time, last_sell_time, completeness FROM w WHERE cost_known ORDER BY realized_sol DESC LIMIT 100""").fetchall()
rows = [[i + 1, wal(r[0]), f"{r[1]:,.1f}", f"{r[2]:,.1f}", f"{r[3]:,.2f}", f"{r[4]:,.1f}", f"{r[6] - r[5]:,.0f}", f"{r[7]}/{r[8]}", f"{r[9] / 1e6:,.2f}",
         cohort(r[11]), ts(r[11]), ts(r[12]), r[13]] for i, r in enumerate(top)]
nocost = con.execute("""SELECT owner, sold_sol, sold_qty, sold_no_basis_qty, transfer_in_qty, bought_sol, n_sells, first_sell_time, last_sell_time FROM w
                        WHERE NOT cost_known ORDER BY sold_sol DESC LIMIT 40""").fetchall()
rows_nc = [[i + 1, wal(r[0]), f"{r[1]:,.1f}", f"{r[2] / 1e6:,.1f}", f"{r[3] / 1e6:,.1f}", f"{r[4] / 1e6:,.1f}", f"{r[5]:,.1f}", r[6], ts(r[7]), ts(r[8])] for i, r in enumerate(nocost)]
res = con.execute("""SELECT owner, residual_qty, residual_flux_qty, residual_value_sol_at_cutoff, bought_sol, realized_sol, first_buy_time, n_ruptures FROM w
                     ORDER BY residual_qty DESC LIMIT 25""").fetchall()
rows2 = [[i + 1, wal(r[0]), f"{r[1] / 1e6:,.2f}", f"{r[2] / 1e6:,.2f}", f"{r[3]:,.1f}", f"{r[4]:,.2f}", f"{r[5]:,.1f}", cohort(r[6]), r[7]] for i, r in enumerate(res)]
big = con.execute("""SELECT owner, bought_sol, cost_usd, n_buys, realized_sol, net_sol_all, first_buy_time FROM w WHERE owner NOT IN (SELECT owner FROM bots) ORDER BY bought_sol DESC LIMIT 100""").fetchall()
assert any(r[0].startswith("4ToQp55m") for r in big)
rows3 = [[i + 1, f"`{r[0]}`", f"{r[1]:,.1f}", f"{r[2]:,.0f}", r[3], f"{r[4]:,.1f}", f"{r[5]:,.1f}", cohort(r[6])] for i, r in enumerate(big)]
big_bots = con.execute("""SELECT w.owner, w.bought_sol, b.part_aller_retour, b.lignes_signataire, b.lignes, b.motif, b.programme FROM w JOIN bots b USING (owner) ORDER BY w.bought_sol DESC LIMIT 25""").fetchall()
rows_b = [[f"`{r[0]}`", f"{r[1]:,.1f}", f"{100 * r[2]:.1f} %", f"{r[3]}/{r[4]}", r[5], f"`{r[6]}`" if r[6] else ""] for r in big_bots]
coh = con.execute(f"""SELECT CASE WHEN first_buy_time<{T_WINIG} THEN '1 avant visuel' WHEN first_buy_time<{T_LOW} THEN '2 avant Musk'
    WHEN first_buy_time<={T_HIGH} THEN '3 fenêtre Musk' WHEN first_buy_time IS NULL THEN '5 aucun achat' ELSE '4 après Musk' END c, count(*),
    sum(bought_sol), sum(sold_sol), sum(realized_sol), median(realized_sol), sum(CASE WHEN realized_sol>0 THEN 1 ELSE 0 END), sum(realized_sol) FILTER (WHERE realized_sol>1000)
    FROM w GROUP BY 1 ORDER BY 1""").fetchall()
rows4 = [[r[0][2:], r[1], f"{r[2]:,.0f}", f"{r[3]:,.0f}", f"{r[4]:,.0f}", f"{r[5]:,.3f}", f"{r[6]} ({100 * r[6] / r[1]:.0f} %)"] for r in coh]
txt = f"""# Plus gros gagnants de DMAGA

Généré par `scripts/rep_70_reports.py`, ne pas éditer à la main. **Audit du 03/11 : NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent**, voir `audits/2026-11-03/`. Dérivé corrigé : `data_v2/`.

Population : {totals[0]:,} wallets sur {n_all:,}, hors réserves de pools, routeurs, échanges et services. `docs/CASE_REPORT.md` compte les {n_all:,} : les deux populations ne donnent donc pas tout à fait les mêmes comptes. SOL acheté {totals[1]:,.0f}, SOL vendu {totals[2]:,.0f}, réalisé cumulé {totals[3]:,.0f}
(le cumul ne s'annule pas : les frais de plateforme, les positions de liquidité et les jetons reçus sans coût en sortent).

## Comment lire
- **Réalisé** : SOL reçu aux ventes moins coût moyen de ce qui est vendu, sur Raydium v4, CLMM, Meteora DLMM, Orca et la courbe. Une valorisation maximale n'y entre jamais.
- **Flux net** : SOL vendu moins SOL acheté, liquidité comprise. Ne dépend pas d'une hypothèse de coût.
- **USD** : conversion à la minute de chaque trade (SOLUSDT Binance).
- **Résiduel** : somme des derniers soldes vus des comptes du wallet, plus les transferts vus par les seuls flux après ce solde, valorisée au dernier prix du pool ({ts(REF)} {datetime.fromtimestamp(REF, timezone.utc).year}), bien inférieur au sommet. L'ancienne mesure sur flux sommait à {RES['ancien_flux_M']:,.1f} M, la nouvelle à {RES['somme_soldes_M']:,.1f} M, pour {RES['offre_hors_pools_fin_M']:,.1f} M d'offre hors pools à la fin. Le compte d'un wallet non tracé qui bouge plus tard hors du brut garde un solde périmé : le résiduel surestime encore.
- **Complétude** : « partiel » signale des jetons reçus ou sortis hors swap, ou un compte dont la chaîne de soldes a une rupture ; le réalisé d'un wallet qui reçoit ses jetons d'un autre est surévalué.
- **Mouvements hors du brut** : {R['n']:,} ruptures sur {R['comptes']:,} comptes, {R['total_M']:,.0f} M de jetons, presque tout après Musk (`docs/CASE_REPORT.md`, N12).
- **bot_aller_retour** : au moins 100 SOL achetés et plus de 50 % d'allers-retours sous 10 s, ou jamais signataire avec un programme propre (`scripts/ana_23_roundtrip.py`). Étiquette de lecture, pas une identité. {RT['bots']['n']} wallets, {RT['bots']['sol']:,.0f} SOL d'achats, retirés des classements d'acheteurs.
- Cohortes de premier achat : avant le visuel exact de @ChrisWinig ({ts(T_WINIG)}), avant la borne basse du changement de photo ({ts(T_LOW)}), dans la fenêtre ({ts(T_LOW)} à {ts(T_HIGH)}), après. Un wallet n'est classé que par son premier achat.

## Résultat par cohorte de premier achat
{table(["Cohorte", "Wallets", "SOL acheté", "SOL vendu", "Réalisé cumulé", "Réalisé médian", "Wallets gagnants"], rows4)}

## 100 plus gros réalisés, coût connu
Retenu si moins de 5 % des ventes sont sans quantité connue et moins de 5 % du stock vient de transferts sans coût.

{table(["#", "Wallet", "Réalisé SOL", "Flux net SOL", "Acheté SOL", "Vendu SOL", "P&L USD", "Ach./Vte", "Résiduel M", "Cohorte", "1er achat UTC", "Dernière vente UTC", "Complétude"], rows)}

## Plus gros vendeurs dont le coût n'est pas connu : aucun gain ne peut être affirmé
Leur stock vient de transferts sans prix. Cas typique : `GCvHhEUYQwTJ8jyf8Lc4bv8jBXyZU4LMMsZCobwEPzvM` et `Gtf4RWqjHhkoio55QkkYM7K3vP4BAT3eSUYPwSZKk8Wi` reçoivent leur stock de `3eGdjMdQqFUNc4G64BZb7YCALDEaturLUWcixjJfKxEh`, un hub actif depuis 2023 avec plus de 200 adresses entrantes, puis vendent sur Raydium à partir d'août 2024. Comportement compatible avec un arbitrage entre un échange et le pool ; non attribué.

{table(["#", "Wallet", "SOL reçu aux ventes", "Vendu M", "Vendu sans quantité M", "Reçu par transfert M", "Acheté SOL", "Ventes", "1re vente", "Dernière vente"], rows_nc)}

## 100 plus gros acheteurs (SOL engagé), sans les bot_aller_retour
{table(["#", "Wallet", "Acheté SOL", "Coût USD", "Achats", "Réalisé SOL", "Flux net SOL", "Cohorte"], rows3)}

`4ToQp55m…` reste classé : 45 signataires y versent, par le programme `3GMsedVP…`, non identifié (A-16). Aucune conclusion tant que ce programme ne l'est pas.

## Écartés des classements d'acheteurs : plus gros bot_aller_retour
{table(["Wallet", "Acheté SOL", "Part d'allers-retours", "Lignes signataire/total", "Motif", "Programme"], rows_b)}

## 25 plus gros résiduels
{table(["#", "Wallet", "Dernier solde vu M", "Ancienne mesure sur flux M", "Valeur SOL au dernier prix", "Acheté SOL", "Réalisé SOL", "Cohorte", "Ruptures"], rows2)}
"""
os.makedirs("reports", exist_ok=True)
open("reports/TOP_TRADERS.md", "w").write(fr(txt))

# ---- EARLY_BUYERS
first = con.execute("""SELECT owner, first_buy_slot, first_buy_tx_index, first_buy_time, first_buy_sol, first_buy_qty, bought_sol, realized_sol, residual_qty, first_buy_sig
                       FROM w WHERE first_buy_time IS NOT NULL ORDER BY first_buy_slot, first_buy_tx_index LIMIT 1000""").fetchall()
rows = [[i + 1, wal(r[0]), r[1], ts(r[3]), f"{r[4]:,.3f}", f"{r[5] / 1e6:,.3f}", f"{r[6]:,.2f}", f"{r[7]:,.1f}", f"{r[8] / 1e6:,.2f}"] for i, r in enumerate(first)]
pnl = {r[0]: r[1:] for r in con.execute("SELECT owner, realized_sol, net_sol_all, residual_qty, first_buy_time FROM w0").fetchall()}


def acheteurs(a, b, limit=25):
    """Plus gros acheteurs de [a, b), sans les bot_aller_retour."""
    res = con.execute(f"""
      SELECT owner, sum(-sol_lamports)/1e9, sum(token_delta)/1e12, count(*), min(block_time), max(block_time)
      FROM trades WHERE kind='swap' AND token_delta>0 AND block_time>={a} AND block_time<{b}
      AND owner NOT IN (SELECT a FROM excl) AND owner NOT IN (SELECT owner FROM bots) GROUP BY 1 ORDER BY 2 DESC LIMIT {limit}""").fetchall()
    out = []
    for r in res:
        p = pnl.get(r[0], (0, 0, 0, None))
        out.append([f"`{r[0]}`", f"{r[1]:,.2f}", f"{r[2]:,.2f}", r[3], ts(r[4]), ts(r[5]), f"{p[0]:,.1f}", f"{p[1]:,.1f}", ts(p[3])])
    return out


rows_avant_visuel = acheteurs(T_WINIG - 6 * 3600, T_WINIG)
rows_visuel_musk = acheteurs(T_WINIG, T_LOW)
win = con.execute(f"""
  SELECT owner, sum(-sol_lamports)/1e9, sum(token_delta)/1e12, count(*), min(block_time), owner IN (SELECT owner FROM bots)
  FROM trades WHERE kind='swap' AND token_delta>0 AND block_time>={T_LOW} AND block_time<={T_HIGH}
  AND owner NOT IN (SELECT a FROM excl) GROUP BY 1 ORDER BY 2 DESC LIMIT 25""").fetchall()
rows6 = [[wal(r[0]), f"{r[1]:,.2f}", f"{r[2]:,.2f}", r[3], ts(r[4])] for r in win]
windows = list(__import__("csv").DictReader((DATA / "windows.csv").open()))
rows7 = [[w["window"], w["hours"], w["buy_sol"], w["sell_sol"], w["n_buys"], w["n_sells"], w["wallets"], w["new_buyers"], w["median_buy_by_wallet_sol"], w["top5_share_pct"]] for w in windows]
NOMS_FEN = {"fenetre_musk": "Fenêtre de Musk, 19:03:27 à 19:30:13", "envoi_a_borne_haute": "Envoi à borne haute, 19:23:20 à 19:30:13", "24h_apres_musk": "24 h après Musk",
            "3h_avant_envoi": "3 h avant l'envoi", "3h_avant_winig": "3 h avant le visuel de Winig", "24h_avant_pic": "24 h avant le pic gelé"}
rows_rt = [[NOMS_FEN[k], f"{v['achats_sol']:,.2f}", f"{v['allers_retours_sol']:,.2f}", f"{v['achats_sol'] - v['allers_retours_sol']:,.2f}", f"{v['part_pct']:.1f} %"] for k, v in RT["fenetres"].items()]
DA = AF["deja_acheteurs"]
txt = f"""# Achats antérieurs aux événements clés

Généré par `scripts/rep_70_reports.py`. **Audit du 03/11 : NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent**, voir `audits/2026-11-03/`. Ne prouve aucune connaissance préalable : un achat antérieur à un événement est compatible avec un pari ordinaire.

**Cohortes de premier achat.** Elles ne sont distinctes que par définition : un wallet n'est classé que par son premier achat. Sur les {DA['acheteurs']} acheteurs entre le visuel et la borne basse, {DA['deja']} avaient déjà acheté avant le visuel, dont {DA['dans_6h']} dans les 6 h précédentes. Repères : premier visuel public exact ({ts(T_WINIG)} UTC, @ChrisWinig, plus ancienne image identique dans le corpus archivé ;
une réponse de @kikisknees à Musk à 16:00:08 UTC a un média perdu), et adoption par Musk (borne basse {ts(T_LOW)} UTC, borne haute {ts(T_HIGH)} UTC,
identifiant de l'image 19:23:20 UTC). Un achat dans cette fenêtre de 27 minutes n'est classé ni avant ni après.

## Activité par fenêtre
Compté au vault, allers-retours compris. Le test gelé applique une autre règle (non-signataires à deux côtés écartés) : {S1_WIN:,.0f} SOL au lieu de {RT['fenetres']['3h_avant_winig']['achats_sol']:,.0f} sur les 3 h avant Winig, voir `docs/CASE_REPORT.md`.

{table(["Fenêtre", "Heures", "SOL acheté", "SOL vendu", "Achats", "Ventes", "Wallets", "Nouveaux acheteurs", "Médiane achat/wallet", "Part top 5 %"], rows7)}

## Part des allers-retours sous 10 s, par fenêtre
Un aller-retour : achat suivi d'une vente de même quantité à 1 % près sous 10 s, par le même propriétaire. Sur toute l'histoire : {RT['allers_retours_sol']:,.0f} SOL sur {RT['achats_sol']:,.0f}, {RT['part_pct']:.1f} %.

{table(["Fenêtre", "SOL acheté", "Allers-retours", "Hors allers-retours", "Part"], rows_rt)}

## Plus gros acheteurs dans les 6 h avant le visuel
{ts(T_WINIG - 6 * 3600)} à {ts(T_WINIG)} UTC, sans les bot_aller_retour. La promotion publique du projet s'intensifie ce matin-là : ces achats ont beaucoup d'explications ordinaires.

{table(["Wallet", "SOL acheté", "Jetons M", "Achats", "Premier", "Dernier", "Réalisé SOL total", "Flux net SOL total", "1er achat du wallet"], rows_avant_visuel)}

## Plus gros acheteurs entre le visuel et la borne basse du changement de photo
{ts(T_WINIG)} à {ts(T_LOW)} UTC, sans les bot_aller_retour.

{table(["Wallet", "SOL acheté", "Jetons M", "Achats", "Premier", "Dernier", "Réalisé SOL total", "Flux net SOL total", "1er achat du wallet"], rows_visuel_musk)}

## Plus gros acheteurs dans la fenêtre du changement de photo
{ts(T_LOW)} à {ts(T_HIGH)} UTC : classement impossible avant ou après. Les bot_aller_retour restent ici, marqués : cette table décrit la fenêtre, elle ne classe pas des acheteurs.

{table(["Wallet", "SOL acheté", "Jetons M", "Achats", "Premier"], rows6)}

## Les 1 000 premiers acheteurs, tous venues
Ordre (slot, index de transaction). `Acheté` et `Réalisé` couvrent tout l'historique du wallet sur DMAGA.

{table(["#", "Wallet", "Slot", "UTC", "1er achat SOL", "1er achat M", "Acheté SOL", "Réalisé SOL", "Résiduel M"], rows)}
"""
open("reports/EARLY_BUYERS.md", "w").write(fr(txt))
print("TOP_TRADERS", len(top), "EARLY_BUYERS", len(first), "6 h avant visuel", len(rows_avant_visuel), "visuel à Musk", len(rows_visuel_musk))
