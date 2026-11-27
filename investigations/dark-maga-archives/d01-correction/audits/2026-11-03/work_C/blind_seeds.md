# Auditeur C, phase aveugle : reconstruction des quatre graines

Fait sans lire `docs/`, `reports/`, `state/`, `JOURNAL_AGENTS.md`, `etude_final/results.md`, ni les parquets et JSON de groupes. Parseur : `c01_scan.py`, `c04_seeds.py` (mes scripts).

Sources : `raw/full_mint`, `raw/full_pool`, `raw/full_curve`, `raw/full_venue` (2 699 114 lignes, 1 842 450 tx uniques retenues, 118 tx en erreur écartées), `raw/flows/*/dmaga_all`, plus historique complet téléchargé de chaque graine (`getTransactionsForAddress`, `tokenAccounts: balanceChanged`, `status: succeeded`, voir `credits.csv`).

Chronologies signature par signature : `chrono_8YLEuU.csv`, `chrono_5QhJJc.csv`, `chrono_G41vRr.csv`, `chrono_9W9b3z.csv`. Bilan jetons : `seed_token_summary.csv`. Contreparties : `counterparties.csv`, `seeds_summary.txt`.

## Résultat par graine

### 8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR (créateur)

- 946 tx de solde, 13 signées. Financement 0,5 SOL par Coinbase 3 à 01:32:23Z, `5Ys6ggx4Fr3eYA4fdaDwowiuZg4HEbcRd6MYcPfspDX3g9KzLKMuKVh7ukUNVy3bpZwwhFT9ZLe2tQFMunHea4Dd`. Création et achat 7 105 960 jetons à 02:05:25Z, `fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6`.

- Ne vend rien pendant un an. Vide son solde SOL vers `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` le 26/01/2025 (0,593 SOL, reste 0,001288), `65aNPjoC8nb4yUu3oD5HGzSvyC9DLJZEK1LrkDD8hEXPzdv8Y4FJRgJEXZXXbDuHtYi8UNU7XYdmycKwNi2BS3g2`.

- 06/07/2025 02:18:38Z reçoit 0,032 SOL de `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd`, `Nfzx313VrsXHoEhpfXadwi16CXZyReEEjJA1hojZERATrdgRtz8TdNrveT4wTXPbyUFPySSzFPPXBtXB4LBSYM4`. Le solde avant était 0,001288 SOL, l'ouverture DCA suivante coûte 0,0091 SOL. 35 s plus tard, ordre Jupiter DCA vente de tous les jetons contre USDC, `2BUp8LXmhuhpiEtp1w4pNLHTuywq7Jf1hxpPHWx9jXmRA3kzwRDutXwfKne4nKVULvwsbCPyN5j57d1j7itbfT1k`. Les deux tx ont le même frais, 80 000 lamports.

- 13/07/2025 04:19:28Z rachat DCA avec 4 500 USDC, `3eNyvVpP5LnZVuSDzmjQFrTmptmLhjKDJ3sf4SitjUGQQTMea6BLWQmUMJS3MHEdwtwLbNtMTxuFnTD4mp2iHPVj`, puis transfert de 7 397 559 jetons vers `BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc`, `8cAyFE6ifX5anKxazY1AwJWszZoFLUvjGbjkkqeKC79FMR6kS8khJLNQ47fFhwWKFFNHB21Q4kmtTSXhmRA23A1`. Reste net nul.

- 843 lignes PumpSwap de 2026 où le wallet est en lecture seule, solde inchangé : compte cité, pas d'activité du wallet (exemple `4Y88M6PMk7`).

### 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd

- 403 tx, 82 signées. Financement 1,05 SOL par Coinbase 2 à 01:40:50Z (25 min avant le mint), `RpB7AKeKUJMiJ3rRKBtdxuuHsFvGrDN8gVKNxKFCaBQ64A5rxB2YuVVv5KnvWvw3asdg5ZGmq1KWob1wuhPPVdR`. Achat courbe 5 670 979 jetons à 02:10:11Z (4 min 46 s après le mint), `54xhLoJ4AKQviRt3PVSMTh1WUCwTFEWT7RYp5REhs3TGyvoBY8kpFauSuGRhyK9rPrK6Kf51HsEg6Lr8BR2k7e7z`.

- Achats AMM du 14 au 18/07/2024, DCA du 17 au 19/07. Bilan complet : `seed_token_summary.csv`.

- 18/07/2024 21:05:52Z envoie 18 M à `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu`, `2wxn47W59GaU8YcsTSVSJ1mufSe1g2xLjcAV3FJdu2RHx5zE6Sawncmw1W8A5PNw9u7qQpzZoxeiCGXYpC2zyTUB`, reçoit 23 SOL du même wallet 8 min 35 s après, `2t51AXk6zzRKFqd8xjuEeUzdVXxrjw1H5U19HxyB9xAFWmrY9C8gPS7KoSh1tphxwNY3fbWhzcNxzW8X9UtwHnKU`. Forme d'une vente de gré à gré, donc pas forcément le même opérateur.

- 29/09/2024 07:48-07:52Z reçoit de 8 wallets (26,23 M), puis 09:36-09:41Z envoie 10 M à chacun de 4 wallets avec 0,015 SOL de frais à 3 d'entre eux : `4FBWB1uhLov498H5tvSqfyHvhymxA9ASu1dDMyyr9CjZhy6wyvr9TT1RD9n82sDcCU8h4jCCGfoCmbrCQHWXBqUP`, `z1KXmmCxP3GyaLASd3YibNxDoSG56zuuVkRP9RqL3xDLo2YHHtZFcotYE9MWJW2doR2GH639ibAcTLUwBiXU9WU`. Vers 12:08-12:12Z ces mêmes wallets versent à 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL (35,94, 28,485, 6,68 SOL).

- 26/01/2025 16:14:34Z envoie 0,125 SOL à 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL, `1Ae21aJQzoAv6aa6pxkUVAXaCYHXXah5sUopKdEBJ1n5rgtDkfveDvxvdJHW6awLo1PjTJ7ERBWNhp3EEEsTMmi`.

### G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E

- 390 tx, 123 signées, de 12/2023 à 06/2025. Financé par MEXC 1 (5,95 SOL). Trader de memecoins : Raydium, Jupiter, comptes WSOL `7h4A6tLtzpaCsYCBG7UK2q5yyw2RN5325hWB2fuTocfX`. Pas de comportement de service : peu de contreparties réelles (la majorité des 65 entrantes sont de la poussière, dont des adresses imitant ses contreparties), pas de balayage, pas de rythme.

- 14/07/2024 entre 01:46:23Z et 02:03:38Z envoie exactement 0,5 SOL à 13 wallets (détail `g41v_recipients.csv`), le dernier 1 min 47 s avant le mint. Sur toute son histoire, 15 virements exacts de 0,5 SOL dont 13 ce jour-là. 5 destinataires achètent 422 à 1 036 s après le mint ; 6 reçoivent leurs premiers jetons une semaine plus tard ; 2 n'en ont jamais eu.

- Achat 3 079 165 jetons à 02:28:26Z, `5LiTyoCxVPNULBHtKvAY8LkLweP9XvHgFaAacjxj5n93ucsmxUWt4DV9RBBDhq13wTuuoXH1rApcwdoYc1vmh782`. Verse 8 SOL à 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL le 23/07/2024, `4e3Pg7TvkWucWVKUM5Mymc88jApjREYNsUGk9gSH9gqGWCSEBUQHPdaboYRoMTCP6hPEhw693BGh7iHnZsr3fgZN`, dans une série de 4 versements en 2 min 44 s.

### 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL

- 285 tx du 28/04/2024 au 26/08/2025. Aucun jeton, seul le programme système et ComputeBudget (2 tx cNFT reçues). Entrées 956,52 SOL, sorties 956,51 SOL : le solde revient à zéro à chaque cycle.

- 48 expéditeurs à 0,001 SOL ou plus (88 versements), 80 expéditeurs de poussière (172 versements). 59 sorties, toutes signées par le wallet lui-même, délai médian 126 s après la dernière entrée.

- 903,49 SOL (94,46 %) vers les 3 hot wallets publics de Coinbase. Le reste vers 6 adresses à très fort volume (1 000 signatures en quelques heures, `probe_dest9w.csv`).

- Frais de balayage de 155 000 lamports sur 39 sorties, identique au témoin : sur 41 adresses témoins à balayage pur tirées des hot wallets Coinbase (`ctrl_stats.csv`), 35 ont aussi 155 000 en frais principal ou secondaire. C'est la signature d'un balayeur de plate-forme, donc **compte de dépôt Coinbase**, pas un wallet personnel qui signe à la main.

- Taux de fond : 31 des 48 expéditeurs (64,6 %) ont un solde DMAGA qui bouge dans le brut. Sur 120 dépôts témoins, 8 de 1 452 expéditeurs (0,55 %). Mais le nombre d'expéditeurs n'est pas anormal : médiane témoin 2, percentile 90 de 36, maximum 131 (plafonné à 3 pages).

- 26/01/2025 : 15 versements en 2 rafales (16:11:24 à 16:15:09, 17:13:19 à 17:21:56), petits montants à 3 décimales, dont le créateur et 5QhJJc à 3 min 10 s d'écart. Balayés en un seul montant le 29/01.

## Graphe des transferts directs à 1 M ou plus

Règle : instruction SPL de DMAGA entre deux propriétaires différents (pré et post soldes), montant de 1 M ou plus, tx sans AMM ni agrégateur ni ordre, ou instruction de premier niveau signée par la source. Les transferts absents du brut mint/pool/venue (instruction `Transfer` qui ne cite pas le mint) sont repris des `flows/dmaga_all`, 237 tx retéléchargées.

Exclus par comportement : `C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN` (compte de mise en commun, 15 versements d'exactement 1 M de wallets variés en 4 jours, puis 14 M d'un coup vers un seul wallet : rejoint des wallets sans lien) et `u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w` (service étiqueté). Ordres Jupiter (`j1o2qRpj...`, 495 lignes) écartés : ce sont des escrows.

- Composante de 5QhJJc : **104 wallets, 187 transferts, 892,4 M de jetons déplacés** à 1 M, hub exclu ; 123 wallets hub inclus.

- Sensibilité (`sens_threshold.csv`) : 41 à 1,5 M et 2 M ; 36 à 3 M ; 22 à 5 M ; 20 à 7 M ; 6 à 10 M ; 2 à 15 M. Une composante à 1 M est donc fragile : la moitié des wallets ne tiennent que par un lien juste au seuil.

- Le créateur n'est **pas** dans cette composante (seul lien jeton : `BuHUkjUy...`). `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` non plus (seul lien : `2hNX9JoE...`). `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` n'a aucun jeton. Le lien entre ces graines passe uniquement par le SOL.

- Point d'articulation : retirer `NxtXcmEW...` fait perdre 37 wallets, `BteHCeVL...` 21, `AtZjv3Du...` 18 (`comp_5Q.txt`).

## Limites

- Un transfert `Transfer` entre deux wallets hors de `raw/flows` reste invisible. Mesuré par continuité des soldes (`c26_continuity.py`) : 345 écarts de 1 M ou plus sur 35 propriétaires avant reprise des `flows`, non résiduel à ce stade.

- `tx.parquet` ne contient que des tx réussies.
