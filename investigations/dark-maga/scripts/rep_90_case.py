#!/usr/bin/env python3
"""docs/CASE_REPORT.md et etude_final/results.md : récit écrit à la main, chiffres injectés depuis les fichiers de résultats."""
import csv
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.frfmt import fr


def hms(t):
    """Heure UTC d'un événement de data/events.json : aucune borne n'est écrite en dur dans le texte (issue #27)."""
    return __import__("datetime").datetime.fromtimestamp(t, __import__("datetime").timezone.utc).strftime("%H:%M:%S")


def duree(s):
    return f"{s // 60} min {s % 60} s"

con = connect()
W = f"read_parquet('{BIG}/wallets.parquet')"
tests = json.loads(Path("etude_final/tables/tests.json").read_text())
verdict = json.loads(Path("etude_final/tables/verdict.json").read_text())["verdict"]
fs = json.loads(Path("etude_final/tables/funder_share.json").read_text())
vc = json.loads(Path("reports/data_checks/vault_chain.json").read_text())
vchain = list(csv.DictReader(open("reports/data_checks/venue_chain.csv")))
stats = json.loads((BIG / "trades_stats.json").read_text())
groups = json.loads((DATA / "prevent_groups.json").read_text())
G0 = groups[0]
GS = json.loads((DATA / "group_split.json").read_text())
COL = json.loads((DATA / "collector.json").read_text())
ex = json.loads((DATA / "exit_summary.json").read_text())
EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
win = {w["window"]: w for w in csv.DictReader((DATA / "windows.csv").open())}
prim = tests["variants"]["primary"]
tot_float = 938.0
weak4 = next(x for x in GS["ponts_faibles"] if any(m.startswith("Ei5yGz8") for m in x["members"]))
core_n = G0["n"] - len(weak4["members"])
core_held = G0["held_before_musk_M"] - weak4["held_M"]
ath = con.execute(f"SELECT hour_utc, high_sol*1e9 FROM read_csv('{DATA}/price_hourly.csv') ORDER BY high_sol DESC LIMIT 1").fetchone()
n_rows, n_sig = con.execute("SELECT count(*), count(DISTINCT signature) FROM trades").fetchone()
reg = subprocess.run(["python3", str(Path.home() / ".claude/skills/etude-gelee/scripts/registre.py"), "compter", "etude_final"], capture_output=True, text=True).stdout
m = re.search(r"au total \(balayages compris\) : (\d+)", reg)
n_cmp = int(m.group(1)) if m else None


def v(addr):
    return con.execute(f"SELECT realized_sol, proceeds_usd-cost_usd, cost_usd, bought_sol FROM {W} WHERE owner=?", [addr]).fetchone()


H3, GX, P9, Q, C = ("H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq",
                    "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR")
vH, vG, vP, vQ = v(H3), v(GX), v(P9), v(Q)
n_w = con.execute(f"SELECT count(*) FROM {W}").fetchone()[0]
coh = con.execute(f"SELECT sum(CASE WHEN realized_sol>0 THEN 1 ELSE 0 END), count(*) FROM {W} WHERE first_buy_time>{EV['musk_borne_haute']}").fetchone()
cex = {}
for a, x in ex.items():
    for k, y in x["frontieres"].items():
        n = k.split(":", 1)[1]
        if not any(s in n for s in ("pool", "Jupiter", "service")):
            cex[n] = cex.get(n, 0) + y
cex_txt = " ; ".join(f"{k} : {v_:,.0f} SOL éq." for k, v_ in sorted(cex.items(), key=lambda kv: -kv[1]) if v_ >= 1)
chain_tx = sum(int(r["n_tx"]) for r in vchain)
chain_br = sum(int(r["ruptures"]) for r in vchain)
mrows = "\n".join(f"| {m_} | {x['dmaga']:.3f} | {x['median_ctrl']:.3f} | {x['p']:.3f} |" for m_, x in prim["mesures"].items())
best_p = min(x["p"] for x in prim["mesures"].values())
best_rank = round(best_p * (prim["k"] + 1))
s1 = tests["S1"]
bm, mh, fm = win["biden_a_musk_borne_basse"], win["musk_plus_1h"], win["fenetre_musk"]
sell = GS["ventes_24h"]
butler_h = (EV["creation_mint"] - 1720908660) / 3600
fen = GS["achats_fenetre"]
ff = GS["premier_financeur"]
g41 = GS["g41"]["address"]
n05 = sum(1 for x in GS["g41"]["avant_le_mint"] if x["sol"].startswith("0.5") and x["t"] < EV["creation_mint"])
n_never = sum(1 for x in GS["g41"]["avant_le_mint"] if x["sol"].startswith("0.5") and x["t"] < EV["creation_mint"] and not x["a_achete_sur_le_marche"])
t0_05 = [x["t"] for x in GS["g41"]["avant_le_mint"] if x["sol"].startswith("0.5") and x["t"] < EV["creation_mint"]]
s60 = GS["premieres_60s"]
next_slot = next((r for r in GS["slot_creation_et_suivant"] if r[1] > 277417695), None)
audit = f"""- Plan et code gelés avant le calcul des mesures ; audit des échecs silencieux **avant** le gel (5 bloquants, 8 majeurs, 8 mineurs, corrigés, corrections non re-auditées).
- Contrôles positifs (nul 5 %, effets synthétiques détectés à k = 150) et de bout en bout. Reproduction en copie neuve : `tests.json` et `verdict.json` identiques.
- Un audit indépendant des conclusions : **FAIL**, corrections intégrées ici sans nouvel audit.
- **Non lancés : les auditeurs à l'aveugle des fuites, des statistiques et du protocole.** `etude_final/audit/` n'existe pas : la porte d'audit de la méthode n'est pas ouverte. À décider par Benjamin."""


def fmt(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m/%Y %H:%M UTC")


txt = f"""# Dark MAGA ($DMAGA) : rapport d'enquête

Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`, Solana. Enquête du 02 au 03/11/2026, Claude Code (Opus 5.5) pour Benjamin. Chiffres injectés par `scripts/rep_90_case.py`.

Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice ou hypothèse, **D** non vérifié ou contredit. Ce rapport ne présente personne comme l'auteur d'un délit. Un wallet ou un compte cité n'est accusé de rien.

## Version historique et périmètre

Cette synthèse conserve les calculs et formulations du 3 novembre 2026. Pour les conclusions retenues après relecture, lire le [README](../README.md), son [registre de preuves](README_REVIEW_2026-11-05.md), puis les [contrôles numériques H](https://github.com/searadacunha/Dark-MAGA/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_H/REAUDIT_CONCLUSIONS.md) et les [contrôles transactionnels I](https://github.com/searadacunha/Dark-MAGA/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_I/REFUTATION.md).

**Le créateur est extérieur à la composante de 33 wallets définie par les 40 transferts de DMAGA.** Les transferts de SOL et convergences vers des dépôts décrits au point 5 portent sur un autre périmètre, qui recoupe partiellement les 33. Ils ne démontrent ni l'appartenance du créateur aux 33, ni un contrôle commun dès le lancement. Les formulations historiques « autour du créateur » et « lien au créateur » ci-dessous ne doivent pas être interprétées comme ces démonstrations.

**Correctif du 10 novembre 2026 :** le segment « envoi de l’image → première capture » incluait à tort les achats à la seconde exacte de la borne haute, également comptés dans l’heure suivante. Les deux achats publiés totalisent 0,277882029 SOL : 17,838882029 − 0,277882029 = **17,561 SOL**, soit **17,56 SOL** au lieu de 17,84. Le total de la fenêtre documentaire reste **20,851551083 SOL**, soit **20,85 SOL** dans le README. Le générateur utilise désormais des intervalles `[début, fin)` ; les tableaux historiques et leur compteur de wallets restent conservés jusqu’au rejeu complet. Voir l’[audit du 10 novembre](AUDIT_2026-11-10.md).

## L'essentiel
1. **Le token a été créé après Butler.** Mint créé le 14/07/2024 à 02:05:25 UTC, environ {int(butler_h)} h {round((butler_h % 1) * 60)} après la tentative d'assassinat (A pour la création, heure de Butler non revérifiée dans un fichier). Le thread d'@Aristos_Revenge ne date pas le mint : il écrit que @kikisknees a lancé @DarkMagaCoin et les pfp deux jours avant Butler. Le compte X existe depuis le 11/06/2024.
2. **La hausse suit l'envoi de l'avatar de Musk.** Fenêtre documentée : {hms(EV['musk_borne_basse'])} à {hms(EV['musk_borne_haute'])} UTC le 21/07 (A), image envoyée à {hms(EV['musk_envoi_image'])} UTC (B). Achats : {fen['borne_basse_a_envoi']['sol']:.2f} SOL de {hms(EV['musk_borne_basse'])} à {hms(EV['musk_envoi_image'])}, {fen['envoi_a_borne_haute']['sol']:.2f} SOL de {hms(EV['musk_envoi_image'])} à {hms(EV['musk_borne_haute'])}, {float(mh['buy_sol']):,.2f} SOL dans l'heure suivante (A pour les flux, B pour la cause). Entre l'annonce de Biden et la borne basse ({bm['hours']} h) : {bm['buy_sol']} SOL d'achats, {bm['sell_sol']} de ventes. Sur les 3 h avant l'envoi, en revanche, {s1['avatar']['sol_achete']:.1f} SOL contre une médiane de {s1['avatar']['mediane_sol_passe']:.1f} dans le passé du token, p = {s1['avatar']['p_sol']:.3f}, secondaire.
3. **Aucune preuve d'achat informé juste avant Musk.** Verdict du test gelé : **{verdict}** ({prim['k']} comparateurs, meilleur p = {best_p:.3f}, DMAGA au mieux {best_rank}e sur {prim['k'] + 1}). Une absence d'anomalie ne prouve pas l'absence de connaissance : quelqu'un qui détient déjà n'a pas besoin d'acheter.
4. **Il existe un ensemble financier précoce, autour du créateur.** {G0['n']} wallets reliés par {G0['edges']} transferts directs d'au moins 1 M, tous relus sur la chaîne (A ; règle descriptive, hors plan). Ils détiennent au plus {G0['held_before_musk_M']:,.0f} M avant Musk, {100 * G0['held_before_musk_M'] / tot_float:.0f} % des {tot_float:,.0f} M hors pools : c'est un plafond. Sous-ensemble le mieux relié : {core_n} wallets, {core_held:,.1f} M, {100 * core_held / tot_float:.1f} % (B). {len(weak4['members'])} wallets, {weak4['held_M']:,.1f} M, ne tiennent que par une transaction (C). {GS['acheteurs_premiere_heure']} des {G0['n']} achètent en première heure. Ventes par swap en 24 h après Musk : {sell['groupe_sol']:,.0f} SOL, soit **{sell['part_pct']:.1f} % des {sell['marche_sol']:,.0f} SOL vendus sur le marché**. Aucun nom.
5. **Le wallet créateur est relié à cet ensemble.** `5QhJJc…`, le wallet de la capture de @ramonos (URL @0xRamonos), lui envoie 0,032 SOL 35 secondes avant qu'il ouvre un ordre de vente sur tous ses jetons, en juillet 2025. Et en janvier 2025, en 190 secondes, le créateur, `5QhJJc…` et un autre membre envoient du SOL à une même adresse, `{COL['address']}` ({COL['expediteurs']} expéditeurs, {COL['part_coinbase_pct']:.1f} % de ses fonds repartent vers Coinbase). A pour les transactions, B pour une action concertée, C pour un acteur unique dès le lancement. Rien ne relie @ramonos à ce wallet au-delà de son post.
6. **Les autres gros gagnants signalés restent sans lien avec cet ensemble** par transfert direct : `H3QsBr…` (réalisé {vH[0]:,.0f} SOL, {vH[1]:,.0f} $ pour {vH[2]:,.0f} $ de coût), `GXZvX…` ({vG[0]:,.0f} SOL) et `9PrmF8…` ({vP[0]:,.0f} SOL, fourni par la mission, source sociale non retrouvée). Leurs entrées précoces restent compatibles avec un pari spéculatif. Le contraire n'est pas exclu.
7. **Aucun lien documenté entre un wallet et @DarkMagaCoin, @kikisknees, @Aristos_Revenge ou @ChrisWinig.** Le DM à Musk reste revendiqué, non prouvé.

## Données et fiabilité
- **Collecte :** {n_sig:,} transactions distinctes ({n_rows:,} lignes) dans `trades.parquet`. {stats['tx']:,} lues sur tous les historiques (pool, courbe, mint, 77 venues), doublons compris, dont {stats['tx_no_dmaga_flow']:,} sans flux DMAGA et {stats['tx_failed']} échouées. {n_w:,} wallets. Signatures listées : 9 875 478 sur le pool, 6 624 533 sur le mint.
- **Réconciliation :** chaîne de soldes des vaults Raydium : {vc['WSOL']['breaks']} rupture sur {vc['WSOL']['tx']:,} transactions WSOL, {vc['DMAGA']['breaks']} rupture sur {vc['DMAGA']['tx']:,} transactions DMAGA (0,39 jeton, poussière). Autres venues : {len(vchain)} réserves, {chain_tx:,} transactions, {chain_br} rupture.
- **Validation externe :** coût recalculé de `H3QsBr…` 1 087 $ contre 1 086 $ sur la capture DexScreener de 2024 ; capitalisation recalculée 844 k$ quand @kikisknees écrit « $850k » ; `GXZvX…` 48,5 SOL et 14,69 M comme le post de @ai_9684xtpa.
- **Trou détecté et comblé :** ce même contrôle a repéré 97 ruptures dues à un découpage trop court (23:36 à minuit le 23/07), comblées.
- **Limites du PnL :** coût moyen pondéré, frais de plateforme exclus. Un wallet qui reçoit ses jetons d'un autre a un réalisé surévalué : le classement des gagnants ne retient que les coûts connus (`reports/TOP_TRADERS.md`).

## Les 12 questions
**1. Qui a créé le token ?** Le wallet `{C}`, signature `fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6` (A). Financé 33 minutes avant par Coinbase 3, 0,5 SOL : rupture de traçabilité. Il achète 7,1 M pour 0,2 SOL et ne vend rien pendant le pic. Aucun autre acheteur dans le slot de création (A) ; {s60['acheteurs']} acheteurs prennent {s60['M']:,.1f} M pour {s60['sol']:.1f} SOL dans les 60 premières secondes. @Aristos_Revenge écrit que @kikisknees a lancé @DarkMagaCoin (déclaration, C) ; aucun lien entre ce compte et ce wallet. Identité civile : impossible sans réquisition de l'échange. Wallets du lancement : `reports/COORDINATION.md`, dont {n05} virements de 0,5 SOL de `{g41}` entre {fmt(min(t0_05))[11:16]} et {fmt(max(t0_05))[11:16]} UTC, juste avant le mint ({n_never} de ces wallets n'achètent jamais sur le marché), et 2 wallets financés 65 minutes avant (A pour les virements, finalité non établie).

**2. Qui a créé et publié le premier le visuel ?** Plus ancienne image identique archivée : @ChrisWinig, 21/07 16:02:29 UTC, pHash à distance 0 de l'avatar de Musk (A). @kikisknees revendique « pfp by me and @ChrisWinig » (A pour le post, C pour le contenu ; « made the first one » est une réponse du 22/07, objet non précisé). @DarkMagaCoin publie une capture iOS `IMG_5658` datée 06:17, fuseau inconnu, date modifiable (C). Une réponse de @kikisknees à Musk à 16:00:08 UTC a perdu son image : **on ne peut pas exclure qu'il ait publié le visuel 2 min 21 s plus tôt** (D). L'esthétique « Dark MAGA » existe depuis mars 2022.

**3. Qui a amplifié avant le changement de photo ?** @DarkMagaCoin, @kikisknees (réponses répétées à des comptes à forte audience, dont @pmarca à 12:50 UTC : « Is Elon mooning with us? », puis à Musk à 18:46:37 et 18:55:15 UTC, médias perdus), @koreanjewcrypto dès le 15/07, @kanpai dès le 16/07 (A pour les posts archivés). @pmarca publie des images rouges aux yeux laser sans mentionner DMAGA dans ses 2 posts archivés : il n'est pas compté comme amplificateur du token. Corpus partiel : pas de recherche X native. Graphe : `viz/index.html`, `data/social_links.parquet`.

**4. Quels wallets ont acheté avant chaque publication ?** `reports/EARLY_BUYERS.md` donne les 1 000 premiers acheteurs, les plus gros acheteurs des heures précédant le visuel et Musk, et les achats de la fenêtre indécidable de {duree(EV['musk_borne_haute'] - EV['musk_borne_basse'])}. Les deux cohortes sont distinctes (A).

**5. Profits réellement réalisés ?** `reports/TOP_TRADERS.md`. Tête au coût connu : `H3QsBr…` {vH[0]:,.0f} SOL ({vH[1]:,.0f} $), `GXZvX…` {vG[0]:,.0f} SOL ({vG[1]:,.0f} $), `9PrmF8…` {vP[0]:,.0f} SOL ({vP[1]:,.0f} $). `5QhJJc…`, malgré « 1,8 M$ » sur la capture, a réalisé {vQ[0]:,.0f} SOL en propre : ses jetons sont sortis vers d'autres wallets (A). La valorisation maximale n'est jamais comptée. Sommet du prix : {ath[1]:,.0f} SOL de capitalisation le {fmt(ath[0])}. Parmi les wallets entrés après Musk, {coh[0]:,} sur {coh[1]:,} ont un réalisé positif.

**6. D'où venaient les fonds ?** Surtout d'échanges et d'historiques de trading antérieurs : Coinbase, Binance, MEXC, OKX pour les wallets vérifiés (`data/funding_edges.parquet`). Un hot wallet coupe la trace. Dans le groupe, {ff['dans_le_groupe']} des {ff['n']} wallets tracés ont leur premier financeur dans le groupe, {ff['g41']} ont `{g41}`, hors du groupe (A pour les virements).

**7. Où sont allés les bénéfices ?** `data/exit_flows.parquet`, `data/exit_summary.json`. Échanges atteints à 3 sauts au plus, sur {len(ex)} wallets tracés, approximatif au-delà du premier saut : {cex_txt}. `9PrmF8…` passe par `H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi` puis Coinbase (A). Beaucoup de sorties s'arrêtent à des wallets non étiquetés ou à un service non nommé (limite). Aucune continuité n'est supposée à travers un échange.

**8. Clusters solides ?** En partie : voir le point 4. Le groupe de {G0['n']} est lui aussi exposé à l'effet de chaîne, d'où ses niveaux distincts. La composante plus large de `data/wallet_clusters.parquet` ne se lit pas comme un propriétaire unique.

**9. Liens wallets ↔ comptes X ?** Aucun lien de propriété documenté. Trois mentions de tiers, aucune adresse de wallet publiée par un compte du noyau (`reports/ATTRIBUTION.md`).

**10. Scénarios sans connaissance privilégiée ?** (a) Une équipe lance et accumule tôt, fait une campagne publique visant des comptes influents, Musk adopte l'image, un ensemble précoce vend dans le pic. Ce scénario est compatible avec les observations sans information sur Musk. Il suppose un lien entre l'équipe X et les wallets, **non établi**. (b) Des parieurs indépendants achètent un mème politique juste après Butler. (c) Le pré-mouvement du matin du 21/07 suit des posts publics.

**11. Preuves manquantes ?** La conversation d'origine, le fichier d'origine du visuel, une communication datée entre un wallet identifié et un proche de Musk, ou une attribution vérifiable d'un wallet à un compte. Voir `reports/MISSING_EVIDENCE.md`.

**12. Ce qui reste incertain ?** Le contenu de la réponse de 16:00:08 UTC ; le DM ; l'heure de la bascule à l'intérieur de ces {duree(EV['musk_borne_haute'] - EV['musk_borne_basse'])} ({hms(EV['musk_borne_basse'])} à {hms(EV['musk_borne_haute'])} UTC, bornes documentaires) ; un propriétaire unique ou non pour l'ensemble ; le sens des gestes du 21/07 avant le visuel (répartition 07:57-08:33 UTC, regroupement 14:22-14:25 UTC) ; la nature exacte de `{COL['address']}` ; l'identité de tous les wallets.

## Hypothèses
| Hypothèse | Conclusion | Niveau | Ce qui va contre |
|---|---|---|---|
| H0, hausse organique après adoption d'un mème | La hausse suit l'envoi de l'avatar. « Organique » est trop fort : une campagne existe | A pour la succession, B pour la cause | H1 |
| H1, campagne promotionnelle coordonnée | Soutenue : équipe déclarée, Telegram, outil de pfp, réponses à des comptes influents | A pour les posts, B pour la coordination | Une campagne publique n'a rien d'illicite en soi |
| H2, connaissance préalable de l'adoption | **Non établie.** Test gelé non significatif, le groupe ne trade pas entre le visuel et la bascule. DM non prouvé, reformulé ensuite par le compte (« We sent him the meme and he liked it ») | D pour une démonstration, C pour une possibilité | Gestes du groupe le 21/07 avant le visuel ; message « made for him » ; {s1['avatar']['sol_achete']:.0f} SOL sur 3 h, inhabituel pour DMAGA ; test sans puissance sur un détenteur passif |
| H3, distribution anticipée, financement coordonné | Soutenue pour la distribution précoce : {core_n} wallets et {core_held:,.0f} M (B), virements de SOL avant le mint (A, finalité non établie), lien au créateur (B). Volume artificiel non testé | B | Aucun autre acheteur au slot de création ; 0,2 SOL du créateur ; pas de propriétaire unique établi ; {sell['part_pct']:.1f} % des ventes en 24 h seulement, et moins vendeur que les autres gros détenteurs ({sell['part_du_detenu_pct']:.1f} % contre {sell['autres_part_pct']:.1f} %, exploratoire) |
| H4, paris spéculatifs ordinaires | Compatible pour les gagnants hors de cet ensemble | C | Coïncidences non mesurées au niveau individuel |

Ces hypothèses coexistent. Le scénario le plus simple combine H1, H3 et un effet déclenché par Musk, sans nécessiter H2. Le lien entre l'équipe X (H1) et l'ensemble de wallets (H3) reste **non établi**.

## Test gelé
Plan gelé avant tout calcul des mesures (`etude_final/`). Comparateurs par règle sur 13 920 migrations Pump.fun du 15/06 au 31/08/2024. k = {prim['k']}, {prim['jours_de_pic_distincts']} jours de pic.

| Mesure | DMAGA | Médiane des pairs | p de rang |
|---|---|---|---|
{mrows}

Verdict : **{verdict}**. Sur son propre passé, DMAGA est bien réveillé avant les événements : {s1['winig']['sol_achete']:,.0f} SOL sur les 3 h avant le post de Winig contre une médiane de {s1['winig']['mediane_sol_passe']:,.1f}, p = {s1['winig']['p_sol']:.3f} sur {s1['winig']['n_fenetres_passees']} fenêtres, et {s1['avatar']['sol_achete']:,.1f} SOL avant l'envoi de l'avatar, p = {s1['avatar']['p_sol']:.3f}. Ce test secondaire ne pouvait pas passer Holm : 1/28 = 0,036 > 0,0125. Exploratoire, hors plan : financeur commun des 50 premiers gros acheteurs {fs['dmaga']['part']:.2f} contre une médiane de {fs['mediane_comparateurs']:.2f}, p = {fs['p_rang']:.3f}, k = {fs['k']}.

**Limites du test :** n = 1 pour la cible. À k = {prim['k']}, la première étape de Holm sur sept mesures exige que la plus petite p-value corresponde au rang 1/{prim['k'] + 1} ({1 / (prim['k'] + 1):.4f}). Les seuils suivants augmentent seulement si les étapes précédentes sont franchies ; le meilleur rang observé est {best_rank}/{prim['k'] + 1}, donc aucune étape ne passe. Cette précision rédactionnelle est documentée dans l’[amendement 003](../etude_final/amendements/003-2026-11-10.md). Registre : {n_cmp} comparaisons réelles, seuil de Bonferroni {0.05 / n_cmp:.5f}, inatteignable ici, sans effet sur le verdict. Les mesures ont été choisies après avoir vu DMAGA. Le pic compte des signatures échouées. R1 et R2 sont réduits par l'amendement 001, décidé par l'agent sans Benjamin (amendement 002). Le groupe de comparaison est conditionné au fait d'avoir explosé : la conclusion ne vaut que parmi les pics tardifs. Le groupe de wallets et les fenêtres sont des analyses descriptives hors plan.

**État des relectures :**
{audit}

## Contre-vérifications qui ont changé les conclusions en cours de route
Retirés avant livraison, parce que le contrôle a montré qu'ils étaient faux : financeur commun du créateur et de `9PrmF8…` (Coinbase) ; « destinataire commun » (réserve de pool) ; groupe de trois wallets signalés (comptes publiés par Jupiter) ; destinataire commun du créateur et de `5QhJJc…` (exécutant Jupiter DCA) ; « 28 h après Butler », faux : 3 h 54 ; premier registre d'étude contaminé par un bug de test (`etude/CONTAMINATION_E2E.md`).

## Ancien travail
Une seule session retrouvée, du 02/08/2026 (`docs/PRIOR_WORK.md`). Son constat « pas de snipe » tient au sens étroit : aucun autre acheteur au slot de création. Son « aucun lien ChangeNOW » reste un échantillon. Le récit d'une équipe et d'une adresse deBridge récurrente n'est documenté dans aucun fichier trouvé. Enquête secondaire Wifejak : désactivée, aucun contrat n'est donné par le thread.

## Livrables
`docs/TIMELINE.md`, `reports/TOP_TRADERS.md`, `reports/EARLY_BUYERS.md`, `reports/COORDINATION.md`, `reports/ATTRIBUTION.md`, `reports/MISSING_EVIDENCE.md`, `viz/index.html`, `data/x_posts.jsonl`, `data/social_links.parquet`, `data/wallet_clusters.parquet`, `evidence/MANIFEST.sha256`. Sur le disque USB `VERBATIM HD/Dark-MAGA-Investigation/data/` : `trades.parquet`, `wallets.parquet`, `funding_edges.parquet`, `exit_flows.parquet`, `link_edges.parquet`, reliés depuis `data/`. Brut : `raw/`, manifeste `evidence/RAW_MANIFEST.tsv`.
"""
Path("docs/CASE_REPORT.md").write_text(fr(txt))
res = f"""# Résultats de l'étude gelée

Plan : `analysis_plan.md`. Verdict calculé par `code/ana_90_verdict.py` : **{verdict}**.

Comptages : `derived/selection_counts.json`. Sortie complète : `tables/tests.json`. k = {prim['k']}, {prim['jours_de_pic_distincts']} jours de pic distincts, cible n = 1.

| Mesure | DMAGA | Médiane des pairs | p de rang |
|---|---|---|---|
{mrows}

Holm sur 7 mesures : aucune ne passe. La première étape exigeait que la plus petite p-value corresponde à un dépassement de tous les comparateurs ; les seuils suivants ne sont examinés que si les étapes précédentes sont franchies. Voir la clarification rédactionnelle dans `amendements/003-2026-11-10.md`. Secondaire S1, Holm séparé : aucune. Registre : {n_cmp} comparaisons réelles.

## Deviations and data notes
- Amendement 001 : R1 et R2 limités aux comparateurs collectés, décidé par l'agent, sans Benjamin, à valider (amendement 002).
- `selection.jsonl` réordonné pour traiter d'abord les tokens principaux, sans changement de contenu.
- Le gel de la table a été ajouté après son calcul par le code gelé, avant les tests.
- Exploratoire hors plan : `tables/funder_share.json`.
- Audit à l'aveugle (fuites, statistiques, protocole) non réalisé : la porte d'audit n'est pas ouverte.
"""
Path("etude_final/results.md").write_text(fr(res))
print("CASE_REPORT", len(txt), "; butler", round(butler_h, 2), "h ; comparaisons", n_cmp, "; n05", n05, "; rang", best_rank)
