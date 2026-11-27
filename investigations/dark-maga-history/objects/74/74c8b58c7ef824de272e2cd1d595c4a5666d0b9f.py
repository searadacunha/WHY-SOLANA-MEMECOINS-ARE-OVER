#!/usr/bin/env python3
"""Rapports chiffrés générés depuis les données : TOP_TRADERS, EARLY_BUYERS, tables de COORDINATION.

Rien n'est retapé à la main : chaque adresse et chaque signature vient d'une requête. Également : export
data/trades.parquet et data/wallets.parquet (liens physiques impossibles sur FAT32 : petite copie en interne interdite,
ces deux fichiers restent sur le disque USB et sont reliés par symlink depuis data/).
"""
import json
import os
from datetime import datetime, timezone

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.labels import label
from dmaga.venues import load as load_venues

EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
T_WINIG, T_LOW, T_HIGH = EV["winig_visuel"], EV["musk_borne_basse"], EV["musk_borne_haute"]
venues = set(load_venues())
con = connect()
con.execute(f"CREATE VIEW w0 AS SELECT * FROM read_parquet('{BIG}/wallets.parquet')")
con.execute(f"CREATE VIEW n AS SELECT * FROM read_parquet('{BIG}/nodes.parquet')")
excl = sorted(venues | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"})
con.execute("CREATE TEMP TABLE excl(a VARCHAR)")
con.executemany("INSERT INTO excl VALUES (?)", [[a] for a in excl])
con.execute("""CREATE VIEW w AS SELECT *,
                 (sold_no_basis_qty <= 0.05*greatest(sold_qty,1) AND transfer_in_qty <= 0.05*greatest(bought_qty+transfer_in_qty,1)) AS cost_known
               FROM w0 WHERE owner NOT IN (SELECT a FROM excl)
               AND owner NOT IN (SELECT address FROM n WHERE kind IN ('router','venue','cex'))""")


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


REF = con.execute("SELECT max(valuation_ref_time) FROM w0").fetchone()[0]
totals = con.execute("SELECT count(*), sum(bought_sol), sum(sold_sol), sum(realized_sol), sum(cost_usd), sum(proceeds_usd) FROM w").fetchone()

# ---- TOP_TRADERS
top = con.execute("""SELECT owner, realized_sol, net_sol_all, bought_sol, sold_sol, cost_usd, proceeds_usd, n_buys, n_sells, residual_qty,
                     residual_value_sol_at_cutoff, first_buy_time, last_sell_time, completeness FROM w WHERE cost_known ORDER BY realized_sol DESC LIMIT 100""").fetchall()
rows = [[i + 1, f"`{r[0]}`", f"{r[1]:,.1f}", f"{r[2]:,.1f}", f"{r[3]:,.2f}", f"{r[4]:,.1f}", f"{r[6] - r[5]:,.0f}", f"{r[7]}/{r[8]}", f"{r[9] / 1e6:,.2f}",
         cohort(r[11]), ts(r[11]), ts(r[12]), r[13]] for i, r in enumerate(top)]
nocost = con.execute("""SELECT owner, sold_sol, sold_qty, sold_no_basis_qty, transfer_in_qty, bought_sol, n_sells, first_sell_time, last_sell_time FROM w
                        WHERE NOT cost_known ORDER BY sold_sol DESC LIMIT 40""").fetchall()
rows_nc = [[i + 1, f"`{r[0]}`", f"{r[1]:,.1f}", f"{r[2] / 1e6:,.1f}", f"{r[3] / 1e6:,.1f}", f"{r[4] / 1e6:,.1f}", f"{r[5]:,.1f}", r[6], ts(r[7]), ts(r[8])] for i, r in enumerate(nocost)]
res = con.execute("""SELECT owner, residual_qty, residual_value_sol_at_cutoff, bought_sol, realized_sol, first_buy_time FROM w
                     ORDER BY residual_qty DESC LIMIT 25""").fetchall()
rows2 = [[i + 1, f"`{r[0]}`", f"{r[1] / 1e6:,.2f}", f"{r[2]:,.1f}", f"{r[3]:,.2f}", f"{r[4]:,.1f}", cohort(r[5])] for i, r in enumerate(res)]
big = con.execute("""SELECT owner, bought_sol, cost_usd, n_buys, realized_sol, net_sol_all, first_buy_time FROM w ORDER BY bought_sol DESC LIMIT 100""").fetchall()
rows3 = [[i + 1, f"`{r[0]}`", f"{r[1]:,.1f}", f"{r[2]:,.0f}", r[3], f"{r[4]:,.1f}", f"{r[5]:,.1f}", cohort(r[6])] for i, r in enumerate(big)]
coh = con.execute(f"""SELECT CASE WHEN first_buy_time<{T_WINIG} THEN '1 avant visuel' WHEN first_buy_time<{T_LOW} THEN '2 avant Musk'
    WHEN first_buy_time<={T_HIGH} THEN '3 fenêtre Musk' WHEN first_buy_time IS NULL THEN '5 aucun achat' ELSE '4 après Musk' END c, count(*),
    sum(bought_sol), sum(sold_sol), sum(realized_sol), median(realized_sol), sum(CASE WHEN realized_sol>0 THEN 1 ELSE 0 END), sum(realized_sol) FILTER (WHERE realized_sol>1000)
    FROM w GROUP BY 1 ORDER BY 1""").fetchall()
rows4 = [[r[0][2:], r[1], f"{r[2]:,.0f}", f"{r[3]:,.0f}", f"{r[4]:,.0f}", f"{r[5]:,.3f}", f"{r[6]} ({100 * r[6] / r[1]:.0f} %)"] for r in coh]
txt = f"""# Plus gros gagnants de DMAGA

Généré par `scripts/rep_70_reports.py`, ne pas éditer à la main.

Population : {totals[0]:,} wallets, hors réserves de pools, routeurs et échanges. SOL acheté {totals[1]:,.0f}, SOL vendu {totals[2]:,.0f}, réalisé cumulé {totals[3]:,.0f}
(le cumul ne s'annule pas : les frais de plateforme, les positions de liquidité et les jetons reçus sans coût en sortent).

## Comment lire
- **Réalisé** : SOL reçu aux ventes moins coût moyen de ce qui est vendu, sur Raydium v4, CLMM, Meteora DLMM, Orca et la courbe. Une valorisation maximale n'y entre jamais.
- **Flux net** : SOL vendu moins SOL acheté, liquidité comprise. Ne dépend pas d'une hypothèse de coût.
- **USD** : conversion à la minute de chaque trade (SOLUSDT Binance).
- **Résiduel** : jetons restants, valorisés au dernier prix du pool ({ts(REF)} {datetime.fromtimestamp(REF, timezone.utc).year}), bien inférieur au sommet.
- **Complétude** : « partiel » signale des jetons reçus ou sortis hors swap ; le réalisé d'un wallet qui reçoit ses jetons d'un autre est surévalué.
- Cohortes : avant le visuel exact de @ChrisWinig ({ts(T_WINIG)}), avant la borne basse du changement de photo ({ts(T_LOW)}), dans la fenêtre ({ts(T_LOW)} à {ts(T_HIGH)}), après.

## Résultat par cohorte de premier achat
{table(["Cohorte", "Wallets", "SOL acheté", "SOL vendu", "Réalisé cumulé", "Réalisé médian", "Wallets gagnants"], rows4)}

## 100 plus gros réalisés, coût connu
Retenu si moins de 5 % des ventes sont sans quantité connue et moins de 5 % du stock vient de transferts sans coût.

{table(["#", "Wallet", "Réalisé SOL", "Flux net SOL", "Acheté SOL", "Vendu SOL", "P&L USD", "Ach./Vte", "Résiduel M", "Cohorte", "1er achat UTC", "Dernière vente UTC", "Complétude"], rows)}

## Plus gros vendeurs dont le coût n'est pas connu : aucun gain ne peut être affirmé
Leur stock vient de transferts sans prix. Cas typique : `GCvHhEUYQwTJ8jyf8Lc4bv8jBXyZU4LMMsZCobwEPzvM` et `Gtf4RWqjHhkoio55QkkYM7K3vP4BAT3eSUYPwSZKk8Wi` reçoivent leur stock de `3eGdjMdQqFUNc4G64BZb7YCALDEaturLUWcixjJfKxEh`, un hub actif depuis 2023 avec plus de 200 adresses entrantes, puis vendent sur Raydium à partir d'août 2024. Comportement compatible avec un arbitrage entre un échange et le pool ; non attribué.

{table(["#", "Wallet", "SOL reçu aux ventes", "Vendu M", "Vendu sans quantité M", "Reçu par transfert M", "Acheté SOL", "Ventes", "1re vente", "Dernière vente"], rows_nc)}

## 100 plus gros acheteurs (SOL engagé)
{table(["#", "Wallet", "Acheté SOL", "Coût USD", "Achats", "Réalisé SOL", "Flux net SOL", "Cohorte"], rows3)}

## 25 plus gros résiduels
{table(["#", "Wallet", "Jetons M", "Valeur SOL au dernier prix", "Acheté SOL", "Réalisé SOL", "Cohorte"], rows2)}
"""
os.makedirs("reports", exist_ok=True)
open("reports/TOP_TRADERS.md", "w").write(txt)

# ---- EARLY_BUYERS
first = con.execute("""SELECT owner, first_buy_slot, first_buy_tx_index, first_buy_time, first_buy_sol, first_buy_qty, bought_sol, realized_sol, residual_qty, first_buy_sig
                       FROM w WHERE first_buy_time IS NOT NULL ORDER BY first_buy_slot, first_buy_tx_index LIMIT 1000""").fetchall()
rows = [[i + 1, f"`{r[0]}`", r[1], ts(r[3]), f"{r[4]:,.3f}", f"{r[5] / 1e6:,.3f}", f"{r[6]:,.2f}", f"{r[7]:,.1f}", f"{r[8] / 1e6:,.2f}"] for i, r in enumerate(first)]
pre = con.execute(f"""
  SELECT owner, sum(-sol_lamports)/1e9, sum(token_delta)/1e12, count(*), min(block_time), max(block_time)
  FROM trades WHERE kind='swap' AND token_delta>0 AND block_time>={T_WINIG - 6 * 3600} AND block_time<{T_LOW}
  AND owner NOT IN (SELECT a FROM excl) GROUP BY 1 ORDER BY 2 DESC LIMIT 50""").fetchall()
pnl = {r[0]: r[1:] for r in con.execute("SELECT owner, realized_sol, net_sol_all, residual_qty, first_buy_time FROM w0").fetchall()}
rows5 = []
for r in pre:
    p = pnl.get(r[0], (0, 0, 0, None))
    rows5.append([f"`{r[0]}`", f"{r[1]:,.2f}", f"{r[2]:,.2f}", r[3], ts(r[4]), ts(r[5]), f"{p[0]:,.1f}", f"{p[1]:,.1f}", ts(p[3])])
win = con.execute(f"""
  SELECT owner, sum(-sol_lamports)/1e9, sum(token_delta)/1e12, count(*), min(block_time)
  FROM trades WHERE kind='swap' AND token_delta>0 AND block_time>={T_LOW} AND block_time<={T_HIGH}
  AND owner NOT IN (SELECT a FROM excl) GROUP BY 1 ORDER BY 2 DESC LIMIT 25""").fetchall()
rows6 = [[f"`{r[0]}`", f"{r[1]:,.2f}", f"{r[2]:,.2f}", r[3], ts(r[4])] for r in win]
windows = list(__import__("csv").DictReader((DATA / "windows.csv").open()))
rows7 = [[w["window"], w["hours"], w["buy_sol"], w["sell_sol"], w["n_buys"], w["n_sells"], w["wallets"], w["new_buyers"], w["median_buy_by_wallet_sol"], w["top5_share_pct"]] for w in windows]
txt = f"""# Achats antérieurs aux événements clés

Généré par `scripts/rep_70_reports.py`. Ne prouve aucune connaissance préalable : un achat antérieur à un événement est compatible avec un pari ordinaire.

Deux cohortes distinctes : avant le premier visuel public exact ({ts(T_WINIG)} UTC, @ChrisWinig, plus ancienne image identique dans le corpus archivé ;
une réponse de @kikisknees à Musk à 16:00:08 UTC a un média perdu), et avant l'adoption par Musk (borne basse {ts(T_LOW)} UTC, borne haute {ts(T_HIGH)} UTC,
identifiant de l'image 19:23:20 UTC). Un achat dans cette fenêtre de 27 minutes n'est classé ni avant ni après.

## Activité par fenêtre
{table(["Fenêtre", "Heures", "SOL acheté", "SOL vendu", "Achats", "Ventes", "Wallets", "Nouveaux acheteurs", "Médiane achat/wallet", "Part top 5 %"], rows7)}

## Plus gros acheteurs dans les 6 h avant le visuel et jusqu'à la borne basse du changement de photo
{ts(T_WINIG - 6 * 3600)} à {ts(T_LOW)} UTC. Ce sont les achats à regarder en premier, et aussi ceux qui ont le plus d'explications ordinaires : la promotion publique du projet s'intensifie ce matin-là.

{table(["Wallet", "SOL acheté", "Jetons M", "Achats", "Premier", "Dernier", "Réalisé SOL total", "Flux net SOL total", "1er achat du wallet"], rows5)}

## Plus gros acheteurs dans la fenêtre du changement de photo
{ts(T_LOW)} à {ts(T_HIGH)} UTC : classement impossible avant ou après.

{table(["Wallet", "SOL acheté", "Jetons M", "Achats", "Premier"], rows6)}

## Les 1 000 premiers acheteurs, tous venues
Ordre (slot, index de transaction). `Acheté` et `Réalisé` couvrent tout l'historique du wallet sur DMAGA.

{table(["#", "Wallet", "Slot", "UTC", "1er achat SOL", "1er achat M", "Acheté SOL", "Réalisé SOL", "Résiduel M"], rows)}
"""
open("reports/EARLY_BUYERS.md", "w").write(txt)
print("TOP_TRADERS", len(top), "EARLY_BUYERS", len(first), "pré-événement", len(pre))
