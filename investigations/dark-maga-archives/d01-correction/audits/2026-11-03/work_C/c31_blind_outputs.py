#!/usr/bin/env python3
"""Ecrit blind_graph.csv et blind_seeds.md depuis les chronologies et les aretes. Les signatures sont resolues par prefixe avec assertion d'unicite."""
import collections
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXC = set((ROOT / "excl_blind.txt").read_text().split())
HUB = "C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN"
S5 = "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
CR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
G4 = "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E"
W9 = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"

rows = list(csv.DictReader(open(ROOT / "direct_edges_all.csv")))
adj = collections.defaultdict(set)
for r in rows:
    if r["src"] in EXC or r["dst"] in EXC:
        continue
    adj[r["src"]].add(r["dst"])
    adj[r["dst"]].add(r["src"])
comp = {S5}
st = [S5]
while st:
    x = st.pop()
    for y in adj[x]:
        if y not in comp:
            comp.add(y)
            st.append(y)
assert len(comp) == 104, len(comp)
w = csv.writer(open(ROOT / "blind_graph.csv", "w", newline=""))
w.writerow("sig utc slot txidx src dst tokens authority payer origin kind excluded_hub in_component_5QhJJc_ge1M".split())
for r in sorted(rows, key=lambda r: (int(r["slot"]), int(r["txidx"] or 0))):
    exc = r["src"] in EXC or r["dst"] in EXC
    w.writerow([r["sig"], r["utc"], r["slot"], r["txidx"], r["src"], r["dst"], int(r["amount"]) / 1e6, r["authority"], r["payer"], r["origin"], r["kind"], exc,
                (not exc) and r["src"] in comp and r["dst"] in comp])


def sig(pref, seed):
    h = [r for r in csv.DictReader(open(ROOT / f"chrono_{seed[:6]}.csv")) if r["sig"].startswith(pref)]
    assert len(h) == 1, (pref, len(h))
    return h[0]["sig"]


L = []
L.append("# Auditeur C, phase aveugle : reconstruction des quatre graines\n")
L.append("Fait sans lire `docs/`, `reports/`, `state/`, `JOURNAL_AGENTS.md`, `etude_final/results.md`, ni les parquets et JSON de groupes. Parseur : `c01_scan.py`, `c04_seeds.py` (mes scripts).\n")
L.append("Sources : `raw/full_mint`, `raw/full_pool`, `raw/full_curve`, `raw/full_venue` (2 699 114 lignes, 1 842 450 tx uniques retenues, 118 tx en erreur écartées), `raw/flows/*/dmaga_all`, plus historique complet téléchargé de chaque graine (`getTransactionsForAddress`, `tokenAccounts: balanceChanged`, `status: succeeded`, voir `credits.csv`).\n")
L.append("Chronologies signature par signature : `chrono_8YLEuU.csv`, `chrono_5QhJJc.csv`, `chrono_G41vRr.csv`, `chrono_9W9b3z.csv`. Bilan jetons : `seed_token_summary.csv`. Contreparties : `counterparties.csv`, `seeds_summary.txt`.\n")
L.append("## Résultat par graine\n")
L.append(f"### {CR} (créateur)\n")
L.append(f"- 946 tx de solde, 13 signées. Financement 0,5 SOL par Coinbase 3 à 01:32:23Z, `{sig('5Ys6ggx4Fr', CR)}`. Création et achat 7 105 960 jetons à 02:05:25Z, `{sig('fePxr7ER3E', CR)}`.\n")
L.append(f"- Ne vend rien pendant un an. Vide son solde SOL vers `{W9}` le 26/01/2025 (0,593 SOL, reste 0,001288), `{sig('65aNPjoC8n', CR)}`.\n")
L.append(f"- 06/07/2025 02:18:38Z reçoit 0,032 SOL de `{S5}`, `{sig('Nfzx313Vrs', CR)}`. Le solde avant était 0,001288 SOL, l'ouverture DCA suivante coûte 0,0091 SOL. 35 s plus tard, ordre Jupiter DCA vente de tous les jetons contre USDC, `{sig('2BUp8LXmhu', CR)}`. Les deux tx ont le même frais, 80 000 lamports.\n")
L.append(f"- 13/07/2025 04:19:28Z rachat DCA avec 4 500 USDC, `{sig('3eNyvVpP5L', CR)}`, puis transfert de 7 397 559 jetons vers `BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc`, `{sig('8cAyFE6ifX', CR)}`. Reste net nul.\n")
L.append("- 843 lignes PumpSwap de 2026 où le wallet est en lecture seule, solde inchangé : compte cité, pas d'activité du wallet (exemple `4Y88M6PMk7`).\n")
L.append(f"### {S5}\n")
L.append(f"- 403 tx, 82 signées. Financement 1,05 SOL par Coinbase 2 à 01:40:50Z (25 min avant le mint), `{sig('RpB7AKeKUJ', S5)}`. Achat courbe 5 670 979 jetons à 02:10:11Z (4 min 46 s après le mint), `{sig('54xhLoJ4AK', S5)}`.\n")
L.append("- Achats AMM du 14 au 18/07/2024, DCA du 17 au 19/07. Bilan complet : `seed_token_summary.csv`.\n")
L.append(f"- 18/07/2024 21:05:52Z envoie 18 M à `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu`, `{sig('2wxn47W59G', S5)}`, reçoit 23 SOL du même wallet 8 min 35 s après, `{sig('2t51AXk6zz', S5)}`. Forme d'une vente de gré à gré, donc pas forcément le même opérateur.\n")
L.append(f"- 29/09/2024 07:48-07:52Z reçoit de 8 wallets (26,23 M), puis 09:36-09:41Z envoie 10 M à chacun de 4 wallets avec 0,015 SOL de frais à 3 d'entre eux : `{sig('4FBWB1uhLo', S5)}`, `{sig('z1KXmmCxP3', S5)}`. Vers 12:08-12:12Z ces mêmes wallets versent à {W9} (35,94, 28,485, 6,68 SOL).\n")
L.append(f"- 26/01/2025 16:14:34Z envoie 0,125 SOL à {W9}, `{sig('1Ae21aJQzo', S5)}`.\n")
L.append(f"### {G4}\n")
L.append("- 390 tx, 123 signées, de 12/2023 à 06/2025. Financé par MEXC 1 (5,95 SOL). Trader de memecoins : Raydium, Jupiter, comptes WSOL `7h4A6tLtzpaCsYCBG7UK2q5yyw2RN5325hWB2fuTocfX`. Pas de comportement de service : peu de contreparties réelles (la majorité des 65 entrantes sont de la poussière, dont des adresses imitant ses contreparties), pas de balayage, pas de rythme.\n")
L.append("- 14/07/2024 entre 01:46:23Z et 02:03:38Z envoie exactement 0,5 SOL à 13 wallets (détail `g41v_recipients.csv`), le dernier 1 min 47 s avant le mint. Sur toute son histoire, 15 virements exacts de 0,5 SOL dont 13 ce jour-là. 5 destinataires achètent 422 à 1 036 s après le mint ; 6 reçoivent leurs premiers jetons une semaine plus tard ; 2 n'en ont jamais eu.\n")
L.append(f"- Achat 3 079 165 jetons à 02:28:26Z, `{sig('5LiTyoCxVP', G4)}`. Verse 8 SOL à {W9} le 23/07/2024, `{sig('4e3Pg7TvkW', G4)}`, dans une série de 4 versements en 2 min 44 s.\n")
L.append(f"### {W9}\n")
L.append("- 285 tx du 28/04/2024 au 26/08/2025. Aucun jeton, seul le programme système et ComputeBudget (2 tx cNFT reçues). Entrées 956,52 SOL, sorties 956,51 SOL : le solde revient à zéro à chaque cycle.\n")
L.append("- 48 expéditeurs à 0,001 SOL ou plus (88 versements), 80 expéditeurs de poussière (172 versements). 59 sorties, toutes signées par le wallet lui-même, délai médian 126 s après la dernière entrée.\n")
L.append("- 903,49 SOL (94,46 %) vers les 3 hot wallets publics de Coinbase. Le reste vers 6 adresses à très fort volume (1 000 signatures en quelques heures, `probe_dest9w.csv`).\n")
L.append("- Frais de balayage de 155 000 lamports sur 39 sorties, identique au témoin : sur 41 adresses témoins à balayage pur tirées des hot wallets Coinbase (`ctrl_stats.csv`), 35 ont aussi 155 000 en frais principal ou secondaire. C'est la signature d'un balayeur de plate-forme, donc **compte de dépôt Coinbase**, pas un wallet personnel qui signe à la main.\n")
L.append("- Taux de fond : 31 des 48 expéditeurs (64,6 %) ont un solde DMAGA qui bouge dans le brut. Sur 120 dépôts témoins, 8 de 1 452 expéditeurs (0,55 %). Mais le nombre d'expéditeurs n'est pas anormal : médiane témoin 2, percentile 90 de 36, maximum 131 (plafonné à 3 pages).\n")
L.append("- 26/01/2025 : 15 versements en 2 rafales (16:11:24 à 16:15:09, 17:13:19 à 17:21:56), petits montants à 3 décimales, dont le créateur et 5QhJJc à 3 min 10 s d'écart. Balayés en un seul montant le 29/01.\n")
L.append("## Graphe des transferts directs à 1 M ou plus\n")
L.append("Règle : instruction SPL de DMAGA entre deux propriétaires différents (pré et post soldes), montant de 1 M ou plus, tx sans AMM ni agrégateur ni ordre, ou instruction de premier niveau signée par la source. Les transferts absents du brut mint/pool/venue (instruction `Transfer` qui ne cite pas le mint) sont repris des `flows/dmaga_all`, 237 tx retéléchargées.\n")
L.append(f"Exclus par comportement : `{HUB}` (compte de mise en commun, 15 versements d'exactement 1 M de wallets variés en 4 jours, puis 14 M d'un coup vers un seul wallet : rejoint des wallets sans lien) et `u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w` (service étiqueté). Ordres Jupiter (`j1o2qRpj...`, 495 lignes) écartés : ce sont des escrows.\n")
L.append(f"- Composante de 5QhJJc : **104 wallets, 187 transferts, 892,4 M de jetons déplacés** à 1 M, hub exclu ; 123 wallets hub inclus.\n")
L.append("- Sensibilité (`sens_threshold.csv`) : 41 à 1,5 M et 2 M ; 36 à 3 M ; 22 à 5 M ; 20 à 7 M ; 6 à 10 M ; 2 à 15 M. Une composante à 1 M est donc fragile : la moitié des wallets ne tiennent que par un lien juste au seuil.\n")
L.append(f"- Le créateur n'est **pas** dans cette composante (seul lien jeton : `BuHUkjUy...`). `{G4}` non plus (seul lien : `2hNX9JoE...`). `{W9}` n'a aucun jeton. Le lien entre ces graines passe uniquement par le SOL.\n")
L.append("- Point d'articulation : retirer `NxtXcmEW...` fait perdre 37 wallets, `BteHCeVL...` 21, `AtZjv3Du...` 18 (`comp_5Q.txt`).\n")
L.append("## Limites\n")
L.append("- Un transfert `Transfer` entre deux wallets hors de `raw/flows` reste invisible. Mesuré par continuité des soldes (`c26_continuity.py`) : 345 écarts de 1 M ou plus sur 35 propriétaires avant reprise des `flows`, non résiduel à ce stade.\n")
L.append("- `tx.parquet` ne contient que des tx réussies.\n")
(ROOT / "blind_seeds.md").write_text("\n".join(L))
print("ok", len(comp))
