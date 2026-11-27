"""Livrable : valeurs du commit 01ae5a4, de l'audit D (AUDIT_FINAL.md section 5 et CLAIM_VERIFICATION.csv) et finales sur data_v2. Lecture seule. Sortie : tableau Markdown, table_valeurs.md."""
import csv
import json
from pathlib import Path

DATA = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2")
A = json.loads((DATA / "audit_facts.json").read_text())
RT = json.loads((DATA / "roundtrip.json").read_text())
GS = json.loads((DATA / "group_split.json").read_text())
W = {r["window"]: r for r in csv.DictReader((DATA / "windows.csv").open())}
OLDW = {r["window"]: r for r in csv.DictReader(open("data/windows.csv"))}
L, V, P, R, F, S, AM, C, G, T = A["lignes"], A["ventes24"], A["perimetres"], A["ruptures"], A["fonds"], A["sorties"], A["angles_morts"], A["cohortes_tous"], A["groupe"], A["totaux"]
w = A["wallets"]
env = RT["fenetres"]["envoi_a_borne_haute"]
rows = []


def fmt(x, nd=2):
    if isinstance(x, str):
        return x
    return f"{x:,.{nd}f}".replace(",", " ").replace(".", ",")


EXPL = {
 "Lignes de `trades.parquet`": "K01. K03 change le type de certaines lignes, pas leur nombre : même total que D",
 "C15, marché 24 h (SOL)": "12 lignes `swap_other` redeviennent des ventes, +14,34 SOL sur le dédoublonné. D répartissait selon le sens du vault (5,52) ; le parseur suit le sens du wallet. 0,008 % du marché, négligeable",
 "C15, part du groupe (%)": "Négligeable",
 "C35, réalisés positifs entrés après Musk": "K01 et K03. Écart à l'estimation de D : 12, négligeable",
 "C35, wallets entrés après Musk": "K03 donne un premier achat à 67 wallets. Écart à l'estimation de D : 8, négligeable",
 "C35, à plus de 0,1 SOL": "Écart à l'estimation de D : 11, négligeable",
 "Réalisé du groupe de 33 (SOL)": "Estimation de D confirmée",
 "Réalisé cumulé, tous wallets": "K01 et K03. Écart à l'estimation de D : 115 SOL, 0,12 %",
 "Acheté, tous wallets": "K01 retire 3 151 SOL, K03 rend 1 418 SOL à des swaps sans valeur. La valeur de D ne contient que K01",
 "Vendu, tous wallets": "K01 retire 3 610 SOL, K03 rend 1 757 SOL. La valeur de D ne contient que K01",
 "Réalisé `DswkYbBh`": "Estimation de D confirmée",
 "C05, heure suivante (SOL)": "K03. Égal à la valeur au vault de A-17. D estimait +0,361, le parseur donne +0,18",
 "C50, part sans étiquette (%)": "L'ancien parquet datait d'avant les étiquettes des exécutants DCA : 7 sources passent de sans étiquette à Jupiter. Sans lien avec K07 et K08",
 "C50, part Jupiter (%)": "Même cause",
 "C50, premier financeur avant le mint, sans étiquette": "Même cause : 5 premiers financeurs changent de classe",
 "C50, premier financeur avant le mint, Jupiter": "Même cause",
 "B-06, stock à S hors M6 (M)": "D retirait une liste écrite à la main, sans le transfert caché de 0,267 M de `6t2dz4jm` : 69,09 M retirés et non 68,83 M",
 "A-04, part des allers-retours (%)": "K03 ajoute des achats au dénominateur. Valeur de A sur une autre règle",
 "C37, service non nommé (SOL éq.)": "Sélection : `4ToQp55m` (82 194) et `7dY2yLDb` (612) sortent des 40 gagnants tracés, `7uRDe43i` (1 146) et `BBcYhznj` (1) entrent. Sur les 63 wallets communs : 92 621 avant, 92 375 après. Écart important, à lire avec la liste",
 "C37, 6 échanges (SOL éq.)": "OKX 16 (446) disparaît : K12 arrête la trace sur un hot présumé, le 3e saut n'existe plus",
 "C37, wallets tronqués sur 65": "Même effet de sélection",
 "A-05, somme des résiduels (M)": "K04, plus les transferts vus par les seuls flux. Reste 88 M au-dessus de l'offre hors pools à la fin, 567,8 M : comptes non tracés jamais revus",
 "C34, déjà acheteurs avant le visuel": "K03 donne un acheteur de plus. A écrivait 184, D 183",
 "C12, cœur 29 wallets (M)": "Arrondi de l'ancien rapport",
 "C13, 4 wallets (M)": "Arrondi de l'ancien rapport",
}


def add(nom, old, d, final, expl, nd=2):
    expl = EXPL.get(nom, expl)
    ecart = ""
    if isinstance(old, (int, float)) and isinstance(final, (int, float)):
        ecart = fmt(final - old, nd)
    rows.append(f"| {nom} | {fmt(old, nd)} | {d} | {fmt(final, nd)} | {ecart} | {expl} |")


add("Lignes de `trades.parquet`", L["avant"], "913 880 uniques", L["apres"], "K01 retire les doublons, K03 change quelques lignes", 0)
add("Lignes doublées retirées", L["doublees"], "5 903", L["avant"] - L["unique_avant"], "Recomptées sur l'ancien fichier, en lecture seule", 0)
add("Signatures distinctes", L["avant_sig"], "796 883", L["apres_sig"], "Le filtre K01 ne doit retirer aucune transaction", 0)
add("C15, marché 24 h (SOL)", 190551.17, "190 532,13 ; 190 537,65 avec A-02 (estimation)", V["marche_sol"], "Vraie valeur à la place de l'estimation")
add("C15, ventes du groupe (SOL)", 4524.91, "4 524,91", V["groupe_sol"], "")
add("C15, part du groupe (%)", 2.3746, "2,3749", V["part_pct"], "", 4)
add("C15, avec 3 destinataires (%)", "absent", "2,886", V["part_elargie_pct"], "", 3)
add("C35, réalisés positifs entrés après Musk", 18367, "18 309 ; 18 259 avec A-02 (estimation)", C["apres_musk_realise_pos"], "", 0)
add("C35, wallets entrés après Musk", 53893, "53 893 ; 53 968 avec A-02 (estimation)", C["apres_musk"], "", 0)
add("C35, à plus de 0,1 SOL", "absent", "9 885 ; 9 827 avec A-02", C["apres_musk_plus_01"], "", 0)
add("C35, heure du sommet", "09:00", "09:01:46", A["sommet"]["heure"], "")
add("C35, capitalisation au sommet (SOL)", 631364.0, "631,36 milliers", A["sommet"]["capitalisation_sol"], "", 0)
add("Réalisé du groupe de 33 (SOL)", G["realise_avant"], "5 471,7 ; 5 469,8 avec A-02", G["realise"], "", 1)
add("Réalisé cumulé, tous wallets", T["avant"]["realise"], "98 189,9 ; 97 278,3 avec A-02", T["realise"], "", 1)
add("Acheté, tous wallets", T["avant"]["achete"], "787 071,7, doublons seuls", T["achete"], "", 1)
add("Vendu, tous wallets", T["avant"]["vendu"], "782 244,1, doublons seuls", T["vendu"], "", 1)
for k, d_ in (("ET8ZG5zA", "203,63"), ("Akp46Dic", "268,70"), ("C7i9beNH", "378,01"), ("5FzhCSWL", "187,91"), ("DswkYbBh", "93,6 ; 4,4 avec A-02 (estimation)"),
              ("H3", "5 490,86"), ("GX", "2 540,10"), ("P9", "1 747,80"), ("Q", "74,17")):
    add(f"Réalisé `{k}`", w[k]["avant"], d_, w[k]["apres"], "")
add("Top 100, communs avec l'ancien", 100, "97", A["top100"]["communs"], ", ".join(f"entre {a[:8]} rang {n}" for a, n in A["top100"]["entrants"]) + " ; " + ", ".join(f"sort {a[:8]} rang {n}" for a, n in A["top100"]["sortants"]), 0)
add("Top 10 identique", "oui", "oui", "oui" if A["top100"]["top10_identique"] else "non", "")
add("C05, 19:03:27 à 19:23:20 (SOL)", 3.29, "3,291", GS["achats_fenetre"]["borne_basse_a_envoi"]["sol"], "", 3)
add("C05, 19:23:20 à 19:30:13 (SOL)", 145.44, "145,440", GS["achats_fenetre"]["envoi_a_borne_haute"]["sol"], "", 3)
add("C05, hors allers-retours (SOL)", "absent", "100,78", env["achats_sol"] - env["allers_retours_sol"], "")
add("C05, heure suivante (SOL)", float(OLDW["musk_plus_1h"]["buy_sol"]), "5 377,608 ; +0,361 avec A-02", float(W["musk_plus_1h"]["buy_sol"]), "")
add("C06, achats Biden à borne basse (SOL)", float(OLDW["biden_a_musk_borne_basse"]["buy_sol"]), "13,177", float(W["biden_a_musk_borne_basse"]["buy_sol"]), "")
add("C06, ventes Biden à borne basse (SOL)", float(OLDW["biden_a_musk_borne_basse"]["sell_sol"]), "84,941", float(W["biden_a_musk_borne_basse"]["sell_sol"]), "")
add("C41, sortie du groupe, base commune (%)", 22.49, "37,3", V["groupe_sortie_pct"], "Ancienne valeur : swaps seuls", 1)
add("C41, autres, base commune, bas (%)", 34.96, "40,8", V["autres_sortie_bas_pct"], "Ancienne valeur : swaps seuls", 1)
add("C41, autres, base commune, haut (%)", 34.96, "43,7", V["autres_sortie_haut_pct"], "Ancienne valeur : swaps seuls", 1)
for k, n_, old, d_ in (("sans_etiquette", "sans étiquette", 67.8, "42,5"), ("pool", "pools", 14.8, "22,1"), ("jupiter", "Jupiter", 10.1, "20,5"), ("echange", "échanges", 7.3, "14,8")):
    add(f"C50, part {n_} (%)", old, d_, F["parts"][k]["pct"], "Ancienne valeur : table de A-03, à ne pas reprendre", 1)
for k, n_, d_ in (("echange", "échange", "189"), ("sans_etiquette", "sans étiquette", "189"), ("jupiter", "Jupiter", "109"), ("service", "service", "4")):
    add(f"C50, premier financeur avant le mint, {n_}", "absent", d_, F["premier_financeur"].get(k, 0), "", 0)
add("B-06, solde vu à S hors M6 (M)", "845,72 (achat brut, B)", "158,88", AM["solde_S_M"], "")
add("B-06, stock à S hors M6 (M)", "absent", "90,05", AM["stock_M"], "")
add("B-06, transferts 24 h, reçus (M)", 114.96, "114,96", AM["transferts_recus_M"], "")
add("B-06, transferts 24 h, nets (M)", "absent", "76,3", AM["nets_M"], "", 1)
add("B-06, reçus par le groupe (M)", "absent", "110,2", AM["recus_groupe_M"], "", 1)
add("Achats de l'heure de S (SOL)", "absent", "2 762,2", AM["achats_heure_S_sol"], "", 1)
add("A-04, part des allers-retours (%)", "14,1 (A)", "13,52", RT["part_pct"], "K03 redonne une valeur à des swaps")
add("A-04, 19:23:20 à 19:30:13, allers-retours (SOL)", "absent", "44,66", env["allers_retours_sol"], "")
add("A-04, wallets à plus de 50 %, 100 SOL et plus", "absent", "103 ; 106 047,8 SOL", f"{RT['plus_de_50_cent_sol']['n']} ; {fmt(RT['plus_de_50_cent_sol']['sol'], 1)} SOL", "")
add("C37, service non nommé (SOL éq.)", "« beaucoup »", "175 427", S["service_non_nomme_sol"], "K12 sépare les hot présumés", 0)
add("C37, 6 échanges (SOL éq.)", 24933.0, "24 933", S["echanges_sol"], "", 0)
add("C37, wallets tronqués sur 65", "absent", "14", S["tronques"], "", 0)
add("A-05, ruptures", "absent", "27 196", R["n"], "", 0)
add("A-05, comptes touchés", "absent", "1 168", R["comptes"], "", 0)
add("A-05, entrées + sorties (M)", "absent", "2 845", R["total_M"], "", 0)
add("A-05, avant la borne basse (M)", "absent", "84,737", R["avant_low_M"], "", 3)
add("A-05, 24 h après Musk (M)", "absent", "3,98", R["h24_M"], "")
add("A-05, somme des résiduels (M)", A["residuels"]["ancien_flux_M"], "937,1 sur flux", A["residuels"]["somme_soldes_M"], "K04 : derniers soldes vus", 1)
add("C11, groupe à la borne basse (M)", 217.04, "217,037", P["groupe"]["M"], "", 3)
add("C12, cœur 29 wallets (M)", 166.1, "166,111", P["coeur_M"], "", 3)
add("C12, sans 2 liens faibles (%)", "absent", "16,0", P["coeur_sans_faibles_pct"], "", 1)
add("C13, 4 wallets (M)", 50.9, "50,926", P["faibles4_M"], "", 3)
add("N06, série de 15 (M)", "absent", "61,36", P["serie15"]["M"], "")
add("N06, 48 expéditeurs (M)", "absent", "92,08", P["expediteurs48"]["M"], "")
add("N06, union (M)", "260,4 élargis", "266,70", P["union"]["M"], "")
add("N03, expéditeurs touchant DMAGA", "absent", "31 sur 48", A["expediteurs"]["touchent_dmaga"], "", 0)
add("N03, hors série et hors groupe", "absent", "16 sur 33", f"{A['expediteurs']['hors_serie_groupe_touchent']} sur {A['expediteurs']['hors_serie_groupe']}", "")
add("C34, déjà acheteurs avant le visuel", "absent", "107 des 183 ; 51 en 6 h", f"{A['deja_acheteurs']['deja']} des {A['deja_acheteurs']['acheteurs']} ; {A['deja_acheteurs']['dans_6h']} en 6 h", "")
add("R17, avec Habp5bnc : wallets, arêtes", "33 ; 40", "34 ; 41 (C-07)", f"{A['habp']['wallets']} ; {A['habp']['aretes']}", "")
add("C-10, jetons rachetés le 13/07/2025", "7,40 M", "7 397 559 (C)", A["hx"]["qty_jetons"], "", 0)
add("`token_edges`, arêtes", 108057, "absent", 103394, "4 663 arêtes `gtba`, toutes avec un exécutant DCA : l'ancien parquet datait d'avant leur étiquette. 22 853 transferts au PnL des deux côtés, groupe de 33 identique", 0)
add("`funding_edges`, lignes", 216130, "une ligne par clé", 215178, "K08 : 0 clé doublée. Deux virements d'une même transaction s'additionnent au lieu de se perdre", 0)
add("Financements à 1 M de SOL ou plus", 1130, "décimales fausses", 0, "K07", 0)
add("Sorties SOL à 1 M de SOL ou plus", 5000, "décimales fausses", 0, "K07", 0)
add("`swap_other` avec un vault Raydium qui bouge", 1708, "1 708", A["k03"]["swap_other_vault_mobile_n"], "K03", 0)
add("Nœuds `cex`", 12, "10 à tort", A["labels"]["noeuds"]["cex"], "K11. 4 passent en `service`, 6 exécutants DCA sortent du graphe faute d'arête", 0)
out = "| Chiffre | Commit 01ae5a4 | Valeur D | Finale, data_v2 | Écart final moins commit | Explication |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
Path("audits/2026-11-03/work_F/table_valeurs.md").write_text(out)
print(out)
