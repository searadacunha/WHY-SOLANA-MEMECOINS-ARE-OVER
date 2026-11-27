#!/usr/bin/env python3
"""docs/CASE_REPORT.md : récit écrit à la main, chiffres injectés depuis les fichiers de résultats, textes d'audit repris mot pour mot.

etude_final/results.md n'est plus écrit ici : ce fichier appartient à l'étude gelée. Aucun réseau.
"""
import csv
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from dmaga.audit_txt import AUD, CLAIMS, INTERPRETATION, assertion, ligne_constat, niveau_et_texte, rendu, verifie
from dmaga.db import connect
from dmaga.paths import BIG, DATA

con = connect(mem="700MB")
W = f"read_parquet('{BIG}/wallets.parquet')"
tests = json.loads(Path("etude_final/tables/tests.json").read_text())
verdict = json.loads(Path("etude_final/tables/verdict.json").read_text())["verdict"]
assert verdict in INTERPRETATION
fs = json.loads(Path("etude_final/tables/funder_share.json").read_text())
vc = json.loads(Path("reports/data_checks/vault_chain.json").read_text())
vchain = list(csv.DictReader(open("reports/data_checks/venue_chain.csv")))
stats = json.loads((BIG / "trades_stats.json").read_text())
groups = json.loads((DATA / "prevent_groups.json").read_text())
G0 = groups[0]
GS = json.loads((DATA / "group_split.json").read_text())
COL = json.loads((DATA / "collector.json").read_text())
AF = json.loads((DATA / "audit_facts.json").read_text())
RT = json.loads((DATA / "roundtrip.json").read_text())
EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
win = {w["window"]: w for w in csv.DictReader((DATA / "windows.csv").open())}
SCEN = {r["scenario"]: r for r in csv.DictReader((AUD / "work_D/d11_scenarios.csv").open())}
prim = tests["variants"]["primary"]
PER, V24, RU, FO, SO, AM, LI = AF["perimetres"], AF["ventes24"], AF["ruptures"], AF["fonds"], AF["sorties"], AF["angles_morts"], AF["lignes"]
tot_float = AF["soldes"]["hors_pools_M"]
n_rows, n_sig = con.execute("SELECT count(*), count(DISTINCT signature) FROM trades").fetchone()
reg = subprocess.run(["python3", str(Path.home() / ".claude/skills/etude-gelee/scripts/registre.py"), "compter", "etude_final"], capture_output=True, text=True).stdout
m = re.search(r"au total \(balayages compris\) : (\d+)", reg)
n_cmp = int(m.group(1)) if m else None


def v(addr):
    return con.execute(f"SELECT realized_sol, proceeds_usd-cost_usd, cost_usd, bought_sol FROM {W} WHERE owner=?", [addr]).fetchone()


def pct(nom):
    return f"{float(SCEN[nom]['detection_pct']):.1f}"


H3, GX, P9, Q, C = ("H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq",
                    "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR")
vH, vG, vP, vQ = v(H3), v(GX), v(P9), v(Q)
n_w = con.execute(f"SELECT count(*) FROM {W}").fetchone()[0]
coh = AF["cohortes_tous"]
coh_r = AF["cohortes_rapports"]
cex_txt = " ; ".join(f"{k} : {v_:,.0f} SOL éq." for k, v_ in sorted(SO["echanges"].items(), key=lambda kv: -kv[1]) if v_ >= 1)
chain_DMAGA = [r for r in vchain if r["cote"] == "DMAGA"]
chain_WSOL = [r for r in vchain if r["cote"] == "WSOL"]
mrows = "\n".join(f"| {m_} | {x['dmaga']:.3f} | {x['median_ctrl']:.3f} | {x['p']:.3f} |" for m_, x in prim["mesures"].items())
best_p = min(x["p"] for x in prim["mesures"].values())
best_rank = round(best_p * (prim["k"] + 1))
s1 = tests["S1"]
bm, mh = win["biden_a_musk_borne_basse"], win["musk_plus_1h"]
butler_h = (EV["creation_mint"] - 1720908660) / 3600
fen = GS["achats_fenetre"]
g41 = GS["g41"]["address"]
n05 = sum(1 for x in GS["g41"]["avant_le_mint"] if x["sol"].startswith("0.5") and x["t"] < EV["creation_mint"])
n_never = sum(1 for x in GS["g41"]["avant_le_mint"] if x["sol"].startswith("0.5") and x["t"] < EV["creation_mint"] and not x["a_achete_sur_le_marche"])
t0_05 = [x["t"] for x in GS["g41"]["avant_le_mint"] if x["sol"].startswith("0.5") and x["t"] < EV["creation_mint"]]
s60 = GS["premieres_60s"]
RF = RT["fenetres"]
env = RF["envoi_a_borne_haute"]
net_env = env["achats_sol"] - env["allers_retours_sol"]
top3 = RT["top_acheteurs"][:3]
usdc = re.search(r"ordre d'achat de ([\d ]+) USDC", ligne_constat("C-10", "**Preuve.**")).group(1)
FP = FO["parts"]
FF = FO["premier_financeur"]
T_N, T_DEN, T_DEP = re.search(r"contre (\d+) expéditeurs sur ([\d ]+) dans (\d+) dépôts témoins", assertion("N03")).groups()
S_N, S_DUREE = re.search(r"(\d+) sur [\d ]+, tous dans (\d+) s", verifie("N01")).groups()
ADR = re.search(r"vers (\d+) adresses", verifie("C18")).group(1)
CHK = json.loads(Path("reports/data_checks/group_edges_check.json").read_text())
GAZ, ORDRE = CHK["gaz_vers_createur"], CHK["deplacement_createur"]
nul, moyen, fort = pct("nul"), pct("moyen du contrôle (6 wallets, 6 x lognormale, moitié slot)"), pct("fort du contrôle (18 wallets, 25 x lognormale, moitié slot)")


def fmt(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m/%Y %H:%M UTC")


constats = [("N01", None), ("N02", None), ("N03", None), ("N04", None), ("N05", None),
            ("N06", ("niveau A pour les soldes, C pour un seul acteur", f"Périmètres à 19:03:27 UTC : {PER['groupe']['taille']} wallets {PER['groupe']['M']:,.2f} M, série de {PER['serie15']['taille']} {PER['serie15']['M']:,.2f} M, {PER['expediteurs48']['taille']} expéditeurs {PER['expediteurs48']['M']:,.2f} M, union de {PER['union']['taille']} adresses {PER['union']['M']:,.2f} M, {PER['union']['pct']:.1f} %")),
            ("N07", ("niveau A pour les flux, exploratoire", f"Ventes élargies : {V24['part_elargie_pct']:.2f} % du marché avec {V24['destinataires_vendeurs']} destinataires ; {V24['groupe_sortie_pct']:.1f} % contre {V24['autres_sortie_bas_pct']:.1f} à {V24['autres_sortie_haut_pct']:.1f} % de sortie sur base commune")),
            ("N08", None), ("N09", None),
            ("N10", ("niveau A", f"Allers-retours sous 10 s : {RT['part_pct']:.1f} % des achats selon la règle à 1 %, {env['part_pct']:.1f} % des achats de 19:23:20 à 19:30:13, rangs 1 à 3 des acheteurs")),
            ("N11", ("niveau A", f"{LI['doublees']:,} lignes doublées dans l'ancien `trades.parquet` ; réalisé du groupe {AF['groupe']['realise']:,.1f} SOL et non {AF['groupe']['realise_avant']:,.1f}, après retrait des doublons et correction de la réserve partagée ; top 100 à {100 - AF['top100']['communs']} lignes près, top 10 {'inchangé' if AF['top100']['top10_identique'] else 'modifié'}")),
            ("N12", ("niveau A", f"{RU['n']:,} ruptures sur {RU['comptes']:,} comptes, {RU['total_M']:,.0f} M de mouvements hors du brut, tous après la borne basse sauf {RU['avant_low_M']:,.1f} M déjà compensés")),
            ("N13", ("niveau A", f"Origine du SOL du 14/07/2023 au mint : sans étiquette {FP['sans_etiquette']['pct']:.1f} %, pools {FP['pool']['pct']:.1f} %, Jupiter {FP['jupiter']['pct']:.1f} %, échanges {FP['echange']['pct']:.1f} %")),
            ("N14", None), ("N15", None),
            ("N16", ("niveau A", f"Sorties à 3 sauts : {SO['service_non_nomme_sol']:,.0f} SOL éq. s'arrêtent sur un service non nommé, contre {SO['echanges_sol']:,.0f} sur les échanges cités")),
            ("N17", ("niveau A", f"Angles morts du test sur DMAGA, en stock et non en flux : {AM['stock_M']:,.2f} M détenus à S par {AM['acheteurs_hors_m6']} acheteurs de la courbe hors de M6 ; {AM['nets_M']:,.1f} M de transferts nets sur 24 h, dont {AM['recus_groupe_M']:,.1f} M reçus sur {AM['transferts_recus_M']:,.2f} M bruts par le groupe"))]
verb = {}
lignes_n = []
for cid, fait in constats:
    if fait:
        lignes_n.append(f"| {cid} | {fait[0]} | {fait[1]} |")
    else:
        niv, tx = niveau_et_texte(cid)
        verb[cid] = tx
        verb[cid + "N"] = niv
        lignes_n.append(f"| {cid} | @@{cid}N@@ | @@{cid}@@ |")
table_n = "\n".join(lignes_n)
verb.update(INTERPRETATION=INTERPRETATION, N01V=verifie("N01"), N02V=verifie("N02"), N03V=verifie("N03"), N04V=verifie("N04"), N14V=verifie("N14"), MAX_S1=re.search(r"au-dessus vaut ([\d,]+) SOL", verifie("C07")).group(1), C20V=verifie("C20"), C08V=verifie("C08").removeprefix("reproduit : "), C36V=verifie("C36").split("Sur 33 historiques complets : ")[1].rstrip("."),
            A08P=ligne_constat("A-08", "**Preuve :**").split("`a43_subset.py`. ")[1], A08E=ligne_constat("A-08", "**Effet :**").removeprefix("faible. "))
VERD = Counter(r["verdict"] for c, r in CLAIMS.items() if c.startswith("C"))
ENCADRE = "> **Audit du 03/11 : NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent.** Voir `audits/2026-11-03/` : `AUDIT_FINAL.md`, `CORRECTIONS.md`, `CLAIM_VERIFICATION.csv`, `work_F/CORRECTIONS_APPLIQUEES.md`."

txt = f"""# Dark MAGA ($DMAGA) : rapport d'enquête

{ENCADRE}

Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`, Solana. Enquête du 02 au 03/11/2026, Claude Code pour Benjamin. Chiffres injectés par `scripts/rep_90_case.py`, sur le dérivé corrigé `data_v2/`.

Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice ou hypothèse, **D** non vérifié ou contredit. Ce rapport ne présente personne comme l'auteur d'un délit. Un wallet ou un compte cité n'est accusé de rien. Aucune identité civile n'est présumée.

## L'essentiel
1. **Le token a été créé après Butler.** Mint créé le 14/07/2024 à 02:05:25 UTC, environ {int(butler_h)} h {round((butler_h % 1) * 60)} après la tentative d'assassinat (A pour la création, heure de Butler non revérifiée dans un fichier). Le thread d'@Aristos_Revenge ne date pas le mint : il écrit que @kikisknees a lancé @DarkMagaCoin et les pfp deux jours avant Butler. Le compte X existe depuis le 11/06/2024.
2. **La hausse suit l'envoi de l'avatar de Musk.** Fenêtre documentée : 19:03:27 à 19:30:13 UTC le 21/07 (A), image envoyée à 19:23:20 UTC (B). Achats : {fen['borne_basse_a_envoi']['sol']:.2f} SOL de 19:03:27 à 19:23:20, {fen['envoi_a_borne_haute']['sol']:.2f} SOL de 19:23:20 à 19:30:13, soit **{net_env:.2f} SOL hors allers-retours de moins de 10 s**, {float(mh['buy_sol']):,.2f} SOL dans l'heure suivante (A pour les flux, B pour la cause). Entre l'annonce de Biden et la borne basse ({bm['hours']} h) : {bm['buy_sol']} SOL d'achats, {bm['sell_sol']} de ventes. Sur les 3 h avant l'envoi : {s1['avatar']['sol_achete']:.1f} SOL contre une médiane de {s1['avatar']['mediane_sol_passe']:.1f} dans le passé du token, p = {s1['avatar']['p_sol']:.3f}, test secondaire et peu discriminant ({RF['3h_avant_envoi']['achats_sol']:.2f} SOL au vault, la seule fenêtre passée au-dessus appartient au même épisode que Winig).
3. **Connaissance préalable : ni établie ni écartée.** Verdict du test gelé : **{verdict}** ({prim['k']} comparateurs, meilleur p = {best_p:.3f}, DMAGA au mieux {best_rank}e sur {prim['k'] + 1}). @@INTERPRETATION@@ Un détenteur existant n'a d'ailleurs pas besoin d'acheter.
4. **Le groupe de {G0['n']}, relié par des transferts de jetons.** {G0['n']} wallets reliés par {G0['edges']} transferts directs d'au moins 1 M, tous relus sur la chaîne (A ; règle descriptive, hors plan). Ils détiennent au plus {PER['groupe']['M']:,.0f} M avant Musk, {PER['groupe']['pct']:.0f} % des {tot_float:,.0f} M hors pools : c'est un plafond. Sous-ensemble le mieux relié : {PER['coeur_n']} wallets, {PER['coeur_M']:,.1f} M, de {PER['coeur_sans_faibles_pct']:.1f} à {PER['coeur_pct']:.1f} % (B). {PER['faibles4_n']} wallets, {PER['faibles4_M']:,.1f} M, ne tiennent que par une transaction (C). {GS['acheteurs_premiere_heure']} des {G0['n']} achètent en première heure. Ventes par swap en 24 h après Musk : {V24['groupe_sol']:,.0f} SOL, soit **au moins {V24['part_pct']:.1f} % des {V24['marche_sol']:,.0f} SOL vendus sur le marché, {V24['part_elargie_pct']:.1f} % avec {V24['destinataires_vendeurs']} destinataires**. Le créateur n'est pas dans ce groupe et n'échange aucun jeton avec lui (A). Un seul propriétaire reste au niveau C, et des grappes antérieures au mint vont contre. Aucun nom.
5. **Le périmètre du créateur, relié par une série de retraits et un même compte de dépôt.** @@N01@@. A pour les transactions, **B pour le même opérateur ou le même compte de dépôt, sur le créateur et {int(S_N) - 1} wallets de la série**. `{COL['address']}` est un compte de dépôt Coinbase (B, le type ; titulaire inconnu) : {COL['part_coinbase_pct']:.1f} % de ses sorties, un plancher, vont vers 3 hot wallets étiquetés, 100 % avec {ADR} adresses présumées de la même famille. {AF['expediteurs']['touchent_dmaga']} de ses {COL['expediteurs']} expéditeurs touchent DMAGA, contre {T_N} sur {T_DEN} dans {T_DEP} dépôts témoins. Même bénéficiaire : C, un compte unique tenu pour plusieurs personnes reste possible, seule une réquisition de Coinbase trancherait. `5QhJJc…`, le wallet de la capture de @ramonos (URL @0xRamonos), envoie {GAZ['montant']} SOL au créateur {ORDRE['t'] - GAZ['t']} secondes avant qu'il ouvre un ordre DCA de vente sur ses jetons, en juillet 2025. Puis {usdc} USDC rachètent {AF['hx']['qty_jetons']:,.0f} jetons le 13/07 : le créateur déplace sa position plus qu'il n'encaisse. Le lien avec `BuHUkjUy…` par un montant apparié vaut B pour 2025, sans valeur pour le lancement. Rien ne relie @ramonos à ce wallet au-delà de son post.
6. **Les autres gros gagnants signalés restent sans lien avec ces périmètres** par transfert direct : `H3QsBr…` (réalisé {vH[0]:,.0f} SOL, {vH[1]:,.0f} $ pour {vH[2]:,.0f} $ de coût), `GXZvX…` ({vG[0]:,.0f} SOL) et `9PrmF8…` ({vP[0]:,.0f} SOL, fourni par la mission, source sociale non retrouvée). Leurs entrées précoces restent compatibles avec un pari spéculatif. Le contraire n'est pas exclu.
7. **Aucun lien documenté entre un wallet et @DarkMagaCoin, @kikisknees, @Aristos_Revenge ou @ChrisWinig.** Le DM à Musk reste revendiqué, non prouvé.

## Données et fiabilité
- **Collecte :** {n_sig:,} transactions distinctes ({n_rows:,} lignes) dans `trades.parquet`. {stats['tx']:,} lues sur tous les historiques (pool, courbe, mint, 77 venues), doublons compris, dont {stats['tx_no_dmaga_flow']:,} sans flux DMAGA. {n_w:,} wallets. @@N14@@ : @@N14V@@. Le pool et le mint sont collectés sur les seules réussies : les {stats['tx_failed']} échouées du compte ci-dessus viennent de la courbe.
- **Lignes doublées, corrigées :** {LI['doublees']:,} lignes de l'ancien `trades.parquet` ({LI['avant']:,} lignes) étaient en double : {LI['doublees_pool']:,} dans un chevauchement de tranches, {LI['doublees_venue']:,} entre deux historiques de venues. {LI['doublees_avant_musk']} avant la borne haute de Musk.
- **Réserve partagée, corrigée :** `GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL`, autorité Raydium CPMM, n'est plus comptée sur tous ses pools. Lignes `swap_other` : {LI['swap_other_avant']:,} avant, {LI['swap_other_apres']:,} après, doublons compris dans le premier compte.
- **Réconciliation :** chaîne de soldes des vaults Raydium : {vc['WSOL']['breaks']} rupture sur {vc['WSOL']['tx']:,} transactions WSOL, {vc['DMAGA']['breaks']} rupture sur {vc['DMAGA']['tx']:,} transactions DMAGA (0.39 jeton, poussière). Autres venues, côté DMAGA : {len(chain_DMAGA)} réserves, {sum(int(r['n_tx']) for r in chain_DMAGA):,} transactions, {sum(int(r['ruptures']) for r in chain_DMAGA)} rupture. Côté WSOL, contrôle ajouté après l'audit : {len(chain_WSOL)} réserves, {sum(int(r['n_tx']) for r in chain_WSOL):,} transactions, {sum(int(r['ruptures']) for r in chain_WSOL):,} ruptures, {sum(float(r['manquants']) for r in chain_WSOL):,.2f} SOL (`reports/data_checks/venue_chain.csv`). Une rupture de ce côté peut venir d'un versement direct à la réserve, elle n'est pas lue ici comme un swap manquant.
- **Validation externe :** coût recalculé de `H3QsBr…` 1 087 $ contre 1 086 $ sur la capture DexScreener de 2024 ; capitalisation recalculée 844 k$ quand @kikisknees écrit « $850k » ; `GXZvX…` 48,5 SOL et 14,69 M comme le post de @ai_9684xtpa.
- **Trou détecté et comblé :** ce même contrôle a repéré 97 ruptures dues à un découpage trop court (23:36 à minuit le 23/07), comblées. La tranche de comblement recouvrait 5 h 36 de la suivante : elle est coupée à minuit à la normalisation, le brut reste tel quel.
- **Mouvements hors du brut (N12) :** la chaîne des comptes de jetons compte {RU['n']:,} ruptures sur {RU['comptes']:,} comptes, {RU['total_M']:,.0f} M de jetons, des transferts SPL sans référence au mint. Avant la borne basse : {RU['avant_low_n']} ruptures, {RU['avant_low_M']:,.1f} M, déjà compensés par les flux tracés. Dans les 24 h après Musk : {RU['h24_n']} ruptures, {RU['h24_M']:,.2f} M. {RU['nommes']} sur les 3 gagnants, `5QhJJc…` et le créateur. Le groupe de {G0['n']}, les 217 M et les ventes de 24 h n'en dépendent pas. Les résiduels sont désormais lus sur les soldes des comptes, complétés par les flux tracés : {AF['residuels']['somme_soldes_M']:,.1f} M hors pools, contre {AF['residuels']['ancien_flux_M']:,.1f} M sur flux, pour {AF['residuels']['offre_hors_pools_fin_M']:,.1f} M d'offre hors pools à la fin. L'écart restant vient de comptes de wallets non tracés, jamais revus après un transfert hors du brut.
- **Allers-retours :** {RT['allers_retours_sol']:,.0f} SOL sur {RT['achats_sol']:,.0f} d'achats ({RT['part_pct']:.1f} %) reviennent en moins de 10 s. Les {RT['bots']['n']} wallets `bot_aller_retour` ({RT['bots']['sol']:,.0f} SOL) sortent des classements d'acheteurs (`scripts/ana_23_roundtrip.py`), dont `{top3[0]['owner']}`, `{top3[1]['owner']}` et `{top3[2]['owner']}`, rangs 1 à 3. Le programme `3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk` reste non identifié, aucune conclusion sur lui (A-16).
- **Limites du PnL :** coût moyen pondéré, frais de plateforme exclus. Un wallet qui reçoit ses jetons d'un autre a un réalisé surévalué : le classement des gagnants ne retient que les coûts connus (`reports/TOP_TRADERS.md`). Le flux `dmaga_all` reste tronqué pour {AF['residuels']['dmaga_all_tronques']} wallets (A-15), collecte non relancée.

## Les 12 questions
**1. Qui a créé le token ?** Le wallet `{C}`, signature `fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6` (A). Financé 33 minutes avant par Coinbase 3, 0.5 SOL. C'est le premier d'une série de {S_N} wallets en {S_DUREE} s qui reversent tous au même compte de dépôt (voir l'essentiel, point 5, et N01). Il achète 7.1 M pour 0.2 SOL et ne vend rien pendant le pic. Aucun autre acheteur dans le slot de création (A) ; {s60['acheteurs']} acheteurs prennent {s60['M']:,.1f} M pour {s60['sol']:.1f} SOL dans les 60 premières secondes. @Aristos_Revenge écrit que @kikisknees a lancé @DarkMagaCoin (déclaration, C) ; aucun lien entre ce compte et ce wallet. Identité civile : impossible sans réquisition de l'échange. Wallets du lancement : `reports/COORDINATION.md`, dont {n05} virements de 0.5 SOL de `{g41}` entre {fmt(min(t0_05))[11:16]} et {fmt(max(t0_05))[11:16]} UTC, juste avant le mint ({n_never} de ces wallets n'achètent jamais sur le marché), et 2 wallets financés 65 minutes avant (A pour les virements, finalité non établie).

**2. Qui a créé et publié le premier le visuel ?** Plus ancienne image identique archivée : @ChrisWinig, 21/07 16:02:29 UTC, pHash à distance 0 de l'avatar de Musk (A). @kikisknees revendique « pfp by me and @ChrisWinig » (A pour le post, C pour le contenu ; « made the first one » est une réponse du 22/07, objet non précisé). @DarkMagaCoin publie une capture iOS `IMG_5658` datée 06:17, fuseau inconnu, date modifiable (C). Une réponse de @kikisknees à Musk à 16:00:08 UTC a perdu son image : **on ne peut pas exclure qu'il ait publié le visuel 2 min 21 s plus tôt** (D). L'esthétique « Dark MAGA » existe depuis mars 2022.

**3. Qui a amplifié avant le changement de photo ?** @DarkMagaCoin, @kikisknees (réponses répétées à des comptes à forte audience, dont @pmarca à 12:50 UTC : « Is Elon mooning with us? », puis à Musk à 18:46:37 et 18:55:15 UTC, médias perdus), @koreanjewcrypto dès le 15/07, @kanpai dès le 16/07 (A pour les posts archivés). @pmarca publie des images rouges aux yeux laser sans mentionner DMAGA dans ses 2 posts archivés : il n'est pas compté comme amplificateur du token. Corpus partiel : pas de recherche X native. Graphe : `viz/index.html`, `data_v2/social_links.parquet`.

**4. Quels wallets ont acheté avant chaque publication ?** `reports/EARLY_BUYERS.md` donne les 1 000 premiers acheteurs, deux tableaux séparés pour les 6 h avant le visuel et pour le visuel jusqu'à Musk, et les achats de la fenêtre indécidable de 27 minutes. Ce sont des cohortes de premier achat, distinctes par définition seulement : {AF['deja_acheteurs']['deja']} des {AF['deja_acheteurs']['acheteurs']} acheteurs entre le visuel et la borne basse avaient déjà acheté, {AF['deja_acheteurs']['dans_6h']} dans les 6 h (A). Les `bot_aller_retour` sont retirés des classements.

**5. Profits réellement réalisés ?** `reports/TOP_TRADERS.md`. Tête au coût connu : `H3QsBr…` {vH[0]:,.0f} SOL ({vH[1]:,.0f} $), `GXZvX…` {vG[0]:,.0f} SOL ({vG[1]:,.0f} $), `9PrmF8…` {vP[0]:,.0f} SOL ({vP[1]:,.0f} $). `5QhJJc…`, malgré « 1,8 M$ » sur la capture, a réalisé {vQ[0]:,.0f} SOL en propre : ses jetons sont sortis vers d'autres wallets (A). La valorisation maximale n'est jamais comptée. Sommet du prix : {AF['sommet']['capitalisation_sol']:,.0f} SOL de capitalisation le 22/07/2024 à {AF['sommet']['heure']} UTC. Parmi les wallets entrés après Musk, {coh['apres_musk_realise_pos']:,} sur {coh['apres_musk']:,} ont un réalisé positif, {coh['apres_musk_plus_01']:,} à plus de 0.1 SOL. Population : {coh['wallets']:,} wallets ici, {coh_r['wallets']:,} dans `reports/TOP_TRADERS.md`, hors réserves, routeurs, échanges et services.

**6. D'où venaient les fonds ?** Le SOL reçu par les wallets tracés du 14/07/2023 au mint, {FO['total_sol']:,.0f} SOL : sans étiquette {FP['sans_etiquette']['pct']:.1f} %, pools {FP['pool']['pct']:.1f} %, Jupiter {FP['jupiter']['pct']:.1f} %, échanges étiquetés {FP['echange']['pct']:.1f} % (`funding_edges.parquet`, requête `in_before`, niveau 0). La part d'échange est une borne basse : le fichier Dune ne compte que 112 adresses et des hot wallets restent sans étiquette. Premier financeur reçu avant le mint : {FF['echange']} échange, {FF['sans_etiquette']} sans étiquette, {FF['jupiter']} Jupiter, {FF['service']} service. Un hot wallet ne coupe pas toute la trace : la série N01 et le montant apparié N04 le montrent. Dans le groupe, sur 33 historiques complets : @@C36V@@.

**7. Où sont allés les bénéfices ?** `exit_flows.parquet`, `exit_summary.json`. Échanges atteints à 3 sauts au plus, sur {SO['wallets']} wallets tracés, dont {SO['tronques']} tronqués, approximatif au-delà du premier saut : {cex_txt} Bien plus s'arrête sur un service non nommé : {SO['service_non_nomme_sol']:,.0f} SOL éq. contre {SO['echanges_sol']:,.0f} sur ces échanges. Ce chiffre dépend de la liste des 40 gagnants tracés : `{SO['sortis_de_la_liste'][0][0]}`, sorti de cette liste après la correction du PnL, portait à lui seul {SO['sortis_de_la_liste'][0][1]:,.0f} SOL éq. sur les {SO['service_avant_sol']:,.0f} de l'ancien calcul. Nature non établie (A-16). Hot wallets présumés de la famille Coinbase, liste séparée, non vérifiée : {SO['hot_presume_sol']:,.0f} SOL éq. `9PrmF8…` passe par `H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi` puis Coinbase (A). Aucune continuité n'est supposée à travers un échange.

**8. Clusters solides ?** En partie, et il y en a deux : le groupe de {G0['n']} relié par transferts, et le périmètre du créateur relié par la série et le dépôt. {PER['groupe_serie']} des {G0['n']} seulement sont dans la série, {PER['groupe_expediteurs']} expéditeurs du dépôt. Le créateur n'échange aucun jeton avec eux. Le groupe de {G0['n']} est exposé à l'effet de chaîne, d'où ses niveaux distincts : avant le mint, le SOL entre membres ne relie que 7 et 2 wallets. Le seuil de 1 M a été choisi après coup, et `Habp5bnc…` sort par sa poussière : {AF['habp']['wallets']} wallets et {AF['habp']['aretes']} arêtes avec la règle écrite, {PER['groupe']['M']:,.2f} M inchangé. La composante plus large de `wallet_clusters.parquet` ne se lit pas comme un propriétaire unique.

**9. Liens wallets ↔ comptes X ?** Aucun lien de propriété documenté. Trois mentions de tiers, aucune adresse de wallet publiée par un compte du noyau (`reports/ATTRIBUTION.md`).

**10. Scénarios sans connaissance privilégiée ?** (a) Une équipe lance et accumule tôt, fait une campagne publique visant des comptes influents, Musk adopte l'image, un ensemble précoce vend dans le pic. Ce scénario est compatible avec les observations sans information sur Musk. Il suppose un lien entre l'équipe X et les wallets, **non établi**. (b) Des parieurs indépendants achètent un mème politique juste après Butler. (c) Le pré-mouvement du matin du 21/07 suit des posts publics.

**11. Preuves manquantes ?** La conversation d'origine, le fichier d'origine du visuel, une communication datée entre un wallet identifié et un proche de Musk, une réquisition de Coinbase sur le compte de dépôt, ou une attribution vérifiable d'un wallet à un compte. Voir `reports/MISSING_EVIDENCE.md`.

**12. Ce qui reste incertain ?** Le contenu de la réponse de 16:00:08 UTC ; le DM ; l'heure de la bascule à l'intérieur de 27 minutes ; un propriétaire unique ou non pour le groupe de {G0['n']} ; le sens des gestes du 21/07 avant le visuel (répartition 07:57-08:33 UTC, regroupement 14:22-14:25 UTC) ; le titulaire du compte `{COL['address']}` et le nombre de bénéficiaires derrière lui ; l'identité de tous les wallets.

## Hypothèses
| Hypothèse | Conclusion | Niveau | Ce qui va contre |
|---|---|---|---|
| H0, hausse organique après adoption d'un mème | La hausse suit l'envoi de l'avatar. « Organique » est trop fort : une campagne existe | A pour la succession, B pour la cause | H1 |
| H1, campagne promotionnelle coordonnée | Soutenue : équipe déclarée, Telegram, outil de pfp, réponses à des comptes influents | A pour les posts, B pour la coordination | Une campagne publique n'a rien d'illicite en soi |
| H2, connaissance préalable de l'adoption | **Ni établie ni écartée.** Le test gelé ne départage pas. Le groupe ne trade pas entre le visuel et la bascule, mais un détenteur n'a pas besoin d'acheter. DM non prouvé, reformulé ensuite par le compte (« We sent him the meme and he liked it ») | D pour une démonstration, C pour une possibilité | Indices : gestes du groupe le 21/07 avant le visuel ; message « made for him » ; {s1['avatar']['sol_achete']:.0f} SOL sur 3 h, inhabituel pour DMAGA. Aucun ne démontre une connaissance préalable |
| H3, distribution anticipée, financement coordonné | Soutenue pour la distribution précoce : {PER['coeur_n']} wallets et {PER['coeur_M']:,.0f} M (B), virements de SOL avant le mint (A, finalité non établie), série du créateur (B pour le même opérateur ou compte, sur {S_N} wallets). Volume artificiel non testé | B | Aucun autre acheteur au slot de création ; 0.2 SOL du créateur ; pas de propriétaire unique établi, grappes antérieures au mint ; au moins {V24['part_pct']:.1f} % des ventes en 24 h, {V24['part_elargie_pct']:.1f} % avec {V24['destinataires_vendeurs']} destinataires. Swaps plus transferts : {V24['groupe_sortie_pct']:.1f} % contre {V24['autres_sortie_bas_pct']:.1f} à {V24['autres_sortie_haut_pct']:.1f} %, exploratoire |
| H4, paris spéculatifs ordinaires | Compatible pour les gagnants hors de ces périmètres | C | Coïncidences non mesurées au niveau individuel |

Ces hypothèses coexistent. Un jugement, pas un calcul : le scénario le plus simple combine H1, H3 et un effet déclenché par Musk, sans nécessiter H2. Le test gelé n'y contribue pas, il ne départage pas H2. Le lien entre l'équipe X (H1) et les wallets (H3) reste **non établi**.

## Test gelé
Plan et code gelés avant le calcul des mesures (`etude_final/`). Comparateurs par règle sur 13 920 migrations Pump.fun du 15/06 au 31/08/2024. k = {prim['k']}, {prim['jours_de_pic_distincts']} jours de pic.

| Mesure | DMAGA | Médiane des pairs | p de rang |
|---|---|---|---|
{mrows}

Verdict : **{verdict}**.

@@INTERPRETATION@@

**Reproduction par les audits :** @@C08V@@. Aucune trace d'une reproduction en copie vierge n'a été trouvée dans le dépôt : les valeurs sont retrouvées par trois voies, audits A, B et D.

**Sur son propre passé (secondaire) :** DMAGA est bien réveillé avant les événements : {s1['winig']['sol_achete']:,.0f} SOL selon la règle du plan, {RF['3h_avant_winig']['achats_sol']:,.0f} SOL au vault, sur les 3 h avant le post de Winig, contre une médiane de {s1['winig']['mediane_sol_passe']:,.1f}, p = {s1['winig']['p_sol']:.3f} sur {s1['winig']['n_fenetres_passees']} fenêtres, et {s1['avatar']['sol_achete']:,.1f} SOL avant l'envoi de l'avatar, p = {s1['avatar']['p_sol']:.3f}. Ce test secondaire ne pouvait pas passer Holm : 1/28 = 0.036 > 0.0125. Vault entier avant l'envoi : {RF['3h_avant_envoi']['achats_sol']:.2f} SOL. La seule fenêtre passée au-dessus vaut @@MAX_S1@@ SOL, même épisode que Winig.

**Exploratoire, hors plan :** financeur commun des 50 premiers gros acheteurs {fs['dmaga']['part']:.2f} contre une médiane de {fs['mediane_comparateurs']:.2f}, p = {fs['p_rang']:.3f}, k = {fs['k']}. Arithmétique juste, mesure non recalculable : les réponses réseau n'ont pas été gardées. C'est un jugement, pas une preuve.

**Limites du test :** n = 1 pour la cible. Le verdict ne bascule que si DMAGA dépasse tous les pairs sur au moins une mesure (1/{prim['k'] + 1} = {1 / (prim['k'] + 1):.4f}) ; il est au mieux {best_rank}e sur {prim['k'] + 1}. M3 et M4 ne peuvent pas ouvrir. Niveau réel {nul} %. Registre : {n_cmp} comparaisons réelles, seuil de Bonferroni {0.05 / n_cmp:.5f}, inatteignable ici, sans effet sur le verdict. Les mesures ont été choisies après avoir vu DMAGA. Le groupe de comparaison est conditionné au fait d'avoir explosé : la conclusion ne vaut que parmi les pics tardifs. Le groupe de wallets et les fenêtres sont des analyses descriptives hors plan.

**Puissance sur les vraies données (N08, exploratoire) :** {pct('nul')} % sans effet, {pct('1 R, 1 wallet, 3 h')} % pour une accumulation d'une fois la réserve, {pct('2 R, 1 wallet, 3 h')} % pour deux fois, {pct('5 R, 1 wallet, 3 h')} % pour cinq fois par M7 mécanique, {moyen} % pour l'effet moyen des contrôles, {fort} % pour le fort. Les contrôles positifs synthétiques sont un contrôle de la plomberie seulement.

**Angles morts sur DMAGA, en stock et non en flux (N17) :** {AM['stock_M']:,.2f} M détenus à S par {AM['acheteurs_hors_m6']} acheteurs de la courbe hors de M6. {AM['nets_M']:,.1f} M de transferts nets sur les 24 h avant S, dont {AM['recus_groupe_M']:,.1f} M reçus sur {AM['transferts_recus_M']:,.2f} M bruts par le groupe. {AM['achats_heure_S_sol']:,.0f} SOL d'achats dans l'heure de S, hors des mesures.

**Biais des pics d'échecs (A-08) :** @@A08P@@ @@A08E@@

**Variantes :** R1 et R2 sont réduits par l'amendement 001, décidé par l'agent sans Benjamin (amendement 002). Ce sont des variantes partielles, sans valeur de robustesse sur la bande. La décision sur l'amendement 001 et l'installation du projet d'amendement 003 sont en attente de Benjamin.

**Comparaisons des audits :** 121 comparaisons de l'audit B (B-20), et celles de l'audit D (`d11`, `d23`, `d30`), sont exploratoires et hors du registre gelé.

## État des relectures
- **Audit du 03/11 :** A (données), B (statistiques), C (attribution), D (confrontation), `audits/2026-11-03/AUDIT_FINAL.md`. Sur {sum(VERD.values())} assertions : {VERD['PASS']} PASS, {VERD['FAIL']} FAIL, {VERD['INCONCLUSIVE']} INCONCLUSIVE. Les corrections du présent rapport n'ont pas été auditées : un nouvel audit des conclusions manque, et le mot « validée » reste interdit.
- **Avant le gel :** audit des échecs silencieux (5 bloquants, 8 majeurs, 8 mineurs, corrigés, corrections non re-auditées). Contrôles positifs : plomberie seulement, voir ci-dessus.
- **Un premier audit des conclusions :** FAIL, corrections intégrées sans nouvel audit.
- **En attente de Benjamin :** amendement 001, projet d'amendement 003, nouvel audit des conclusions.

## Constats ajoutés par l'audit (N01 à N17)
Chiffres recalculés sur `data_v2/` pour N06, N07, N10 à N13, N16, N17, repris tels quels de `audits/2026-11-03/CLAIM_VERIFICATION.csv` pour les autres. Tous sont descriptifs.

| Id | Niveau | Constat |
|---|---|---|
{table_n}

## Contre-vérifications qui ont changé les conclusions en cours de route
Retirés avant livraison, parce que le contrôle a montré qu'ils étaient faux : financeur commun du créateur et de `9PrmF8…` (Coinbase) ; « destinataire commun » (réserve de pool) ; groupe de trois wallets signalés (comptes publiés par Jupiter) ; destinataire commun du créateur et de `5QhJJc…` (exécutant Jupiter DCA) ; « 28 h après Butler », faux : 3 h 54 ; premier registre d'étude contaminé par un bug de test (`etude/CONTAMINATION_E2E.md`).

Retirés après l'audit du 03/11 : le test gelé comme appui contre H2 ; « contrôles positifs corrects » comme garantie de détection ; un ensemble « autour du créateur » ; « surtout d'échanges et d'historiques antérieurs » ; « cohortes distinctes » ; « moins vendeur » sans base commune ; l'argument « 48 expéditeurs seulement ».

## Ancien travail
Une seule session retrouvée, du 02/08/2026 (`docs/PRIOR_WORK.md`). Son constat « pas de snipe » tient au sens étroit : aucun autre acheteur au slot de création. Son « aucun lien ChangeNOW » reste un échantillon. Le récit d'une équipe et d'une adresse deBridge récurrente n'est documenté dans aucun fichier trouvé. Enquête secondaire Wifejak : désactivée, aucun contrat n'est donné par le thread.

## Livrables
`docs/TIMELINE.md`, `reports/TOP_TRADERS.md`, `reports/EARLY_BUYERS.md`, `reports/COORDINATION.md`, `reports/ATTRIBUTION.md`, `reports/MISSING_EVIDENCE.md`, `viz/index.html`, `data/x_posts.jsonl`, `evidence/MANIFEST.sha256`. Dérivé corrigé sur le disque USB, `VERBATIM HD/Dark-MAGA-Investigation/data_v2/` : `trades.parquet`, `wallets.parquet`, `funding_edges.parquet`, `exit_flows.parquet`, `link_edges.parquet`, `accounts.parquet`, `account_ruptures.parquet`, `bots.parquet`, `audit_facts.json`, manifeste `evidence/DATA_V2_MANIFEST.tsv`. L'ancien dérivé reste dans `data/` et `VERBATIM HD/Dark-MAGA-Investigation/data/`, manifeste `evidence/RAW_MANIFEST.tsv`. Brut : `raw/`.
"""
Path("docs/CASE_REPORT.md").write_text(rendu(txt, **verb))
print("CASE_REPORT", len(txt), "; butler", round(butler_h, 2), "h ; comparaisons", n_cmp, "; n05", n05, "; rang", best_rank)
