# FIRST_BUYERS — premiers achats depuis le mint (2024-07-14 02:05:25 UTC, slot 277417695)

## 1. Méthode et couverture

**Phase pump.fun (create → migration 02:15:31, plus 60 s)**
- Rejeu indépendant de **toutes** les tx qui touchent le mint jusqu'à 02:16:31 : 436 tx, 0 manquante. Les signatures viennent de `getSignaturesForAddress(mint)` entre le create et `5LiTyo…` (02:28:26) ; les données sont décodées hors ligne.
- Décodage :
  - instruction `buy` : `amount`, `max_sol_cost` ;
  - événement `TradeEvent` : SOL et jetons réels ;
  - erreurs Anchor.
- Reçus figés : `evidence/receipts/pump_phase_0205_0216.jsonl.gz`. Table reconstruite : `data/derived/pump_phase_txs.csv` (test `PumpPhaseRebuild`).

**Fenêtres 15 min, 1 h et 24 h (tous lieux d'échange)**
- On reprend la table du dépôt `reports/EARLY_BUYERS.md` (1 000 premiers acheteurs ; 1er achat par wallet ; Raydium, CLMM, Meteora, Orca et courbe), parsée dans `data/repo_first1000_buyers_parsed.csv`.
- Le rang 1000 date du 15/07 à 16:59, donc la fenêtre de 24 h est **intégralement couverte** pour les *nouveaux* acheteurs. Les achats répétés ne sont comptés que dans les totaux de vie.
- Concordance : les 25 premiers wallets du rejeu sont **les mêmes et dans le même ordre** que dans le dépôt. Seul écart possible : des égalités dans un même slot (test `test_first_buyers_order_matches_repo_table`).

## 2. Fenêtres

| Fenêtre (fin UTC) | Tx sur le mint | Échecs | Achats réussis | Acheteurs distincts | SOL achetés | Nouveaux acheteurs (dépôt) | SOL 1er achat (dépôt) | SOL achetés sur la vie | Réalisé sur la vie (dépôt) |
|---|---|---|---|---|---|---|---|---|---|
| 60 s (02:06:25) | 74 | 50 | 17 | 17 | 11,92 | 17 | 11,92 | 45,7 | 40,6 |
| 5 min (02:10:25) | 188 | 87 | 74 | 69 | 76,98 | 69 | 70,51 | 1 256,0 | 4 132,6 |
| 15 min (02:20:25) | — | — | — | — | — | 283 | 248,51 | 29 209,0 | 8 451,6 |
| 1 h (03:05:25) | — | — | — | — | — | 606 | 471,73 | 33 498,5 | 14 842,5 |
| 24 h (15/07 02:05:25) | — | — | — | — | — | 731 | 542,68 | 38 962,3 | 24 876,9 |

Notes sur le tableau :
- Les colonnes « Tx sur le mint » à « SOL achetés » ne sont renseignées que pour la phase courbe ; le dépôt ne les fournit pas pour 15 min, 1 h et 24 h.
- Les chiffres « vie » couvrent tous les achats et ventes ultérieurs des wallets entrés dans la fenêtre. Ils sont très supérieurs aux montants de lancement, à cause des acheteurs entrés en début de cycle et revenus plus tard.
- Le create (achat dev de 0,201 SOL) est compté dans les fenêtres.

## 3. Les 20 premiers acheteurs (+ le créateur)

Source : `data/derived/first_buyers_top25.csv`. Le financement est le dernier transfert SOL entrant (≥ 0,001) avant le 1er achat, sur les 8 dernières tx décodées. « Dense » veut dire que l'historique est trop chargé pour conclure dans cette fenêtre.

| # | Wallet | 1re tentative | 1er succès (Δslot) | SOL | M DMAGA | Financement direct observé | Rôle / remarque | Réalisé (dépôt) |
|---|---|---|---|---|---|---|---|---|
| 0 | `8YLEuU…` | 02:05:25 | create | 0,201 | 7,106 | **Coinbase 3, 0,5 SOL à 01:32:23** | créateur ; cluster Coinbase/9W9b | 0 |
| 1 | `EYykLf…` | 02:05:25 | 02:05:25 (+1) | 0,150 | 5,268 | dense | bot (vend 37 slots plus tard) | — |
| 2 | `Edq7kG…` | 02:05:28 | 02:05:28 (+5) | 0,190 | 6,592 | dense | bot | — |
| 3 | `E1mh1W…` | 02:05:39 | (+33) | 1,000 | 33,419 | dense | — | — |
| 4 | `Dj2a99…` | 02:05:43 | (+42) | 0,098 | 3,223 | non observé | — | — |
| 5 | `BNHsrn…` | 02:05:46 | (+48) | 1,960 | 60,710 | non observé | — | — |
| 6 | `8D2AGA…` | 02:05:50 | (+57) | 0,214 | 6,194 | non observé | — | — |
| 7 | `GySdM4…` | 02:05:51 | (+59) | 0,0001 | 0,002 | Coinbase 2, 0,0135 SOL à 01:54:59 | micro-achat | — |
| 8 | `DrKPLz…` | 02:05:54 | (+65) | 2,025 | 54,923 | non observé | — | — |
| 9 | `BE5S5w…` | 02:05:54 | (+67) | 1,876 | 45,583 | non observé | — | — |
| 10 | `gYVsQ5…` | 02:05:56 | (+69) | 1,142 | 25,578 | dense | 9 échecs `IllegalOwner` avant | — |
| 11 | `Hcnutb…` | 02:05:57 | (+73) | 0,425 | 9,132 | dense | — | — |
| 12 | `GS7aGE…` | 02:06:04 | (+85) | 0,980 | 20,321 | dense | — | — |
| 13 | `6t2dz4…` | 02:06:07 | (+94) | 1,051 | 20,701 | 74qF…, avant le mint (dépôt) | **groupe 33** | — |
| 14 | `GZVLzg…` | 02:06:15 | (+110) | 0,496 | 9,483 | non observé | — | — |
| 15 | `2W83fC…` | 02:06:04 | 02:06:21 (+125) | 0,008 | 0,189 | non observé | 1 échec avant | — |
| 16 | `D9iUhx…` | 02:06:24 | (+133) | 0,100 | 2,401 | dense | — | — |
| 17 | `Ei1uVf…` | 02:06:26 | (+138) | 0,980 | 21,668 | dense | même slot que n° 18 | — |
| 18 | `8YrEVP…` | 02:06:26 | (+138) | 1,005 | 23,409 | 6t2dz4 à 00:59:41 (dépôt) | **groupe 33** | — |
| 19 | `H4bVhV…` | 02:06:29 | (+144) | 0,206 | 4,203 | non observé | — | — |
| 20 | `Hk74Yp…` | 02:06:38 | (+163) | 0,500 | 10,015 | Coinbase 2, 0,689 SOL à 02:02:43 | — | — |

Suivants notables :
- `543jAT…` (02:06:46, 2,81 SOL).
- `GoPCTr…` : 1re tentative à 02:06:13, **succès à 02:06:53, 0,40 SOL / 7,256 M**. Cluster Coinbase/9W9b.
- `CEzjbQ…` : tentative à 02:06:11, succès à 02:06:58 pour 0,88 SOL. Financé par DQ5JWb… (2,853 SOL à 00:01:26). Réalisé 1 323 SOL.
- `6Lomz4…` : 02:07:06, 1,256 SOL, financé par Binance 2. Réalisé 1 466,6 SOL.

Les colonnes « réalisé » des rangs 1 à 20 sont reprises du dépôt quand le wallet y figure (`repo_realised_sol` dans le CSV).

## 4. Wallets suivis

| Wallet / groupe | 1re tentative | 1er succès | SOL / M | Financement | Sorties et PnL (dépôt, coût moyen) | Coordination |
|---|---|---|---|---|---|---|
| `8YLEuU…` créateur | create 02:05:25 | idem | 0,201 / 7,106 | CB3 0,5 à 01:32:23 | achats de vie 28 SOL, réalisé 0 ; 0,593 SOL vers 9W9b le 2025-01-26 | **cluster CB/9W9b (B)** |
| `G41vRr…` | 02:05:54 (échec), 02:06:10 (échec) | 02:28:26 via Raydium/Jupiter, 4 SOL | 4 / — | MEXC à l'origine ; +22,32 SOL de la vente du token 9MBzpy le 13/07 | réalisé 30,3 ; 8 SOL vers 9W9b | finance 13 wallets à 0,5 SOL + 5 SOL à GFpqfj à 02:06:57 (A) |
| 13 destinataires G41v à 0,5 SOL | — | 5 achètent 0,38–0,49 SOL entre 02:12 et 02:22 ; 8 n'achètent jamais | — | G41v, 01:46–02:03 | EZXUvi 92,6 ; CZsBW8 23,9 ; 2mW45k 21,4 | B (dépôt) |
| `GFpqfj…` | 02:07:26 | idem | 4,411 | G41v 5 SOL à 02:06:57 (**après** le mint) | réalisé 148,5 | B |
| groupe 33 | 6t2dz4 02:06:07 ; 8YrE 02:06:26 ; 5QhJJc 02:10:11 ; 7FGoCB 02:17:56 ; … | | | arêtes avant le mint, 74qF → 6t2dz4 → 8YrE/99Xr/AtZj (dépôt) | cf. `FINANCIAL_BENEFICIARIES.md` | B (dépôt) ; **7FGoCB et 5QhJJc appartiennent aussi au cluster CB/9W9b** |
| GoPCTr / AFDkwJ / EEpSRR | 02:06:13 / 02:07:24 / 02:07:50 | 02:06:53 / 06:12:56 / 02:09:29 | 0,40 / 0,05 / 0,44 | CB3 0,5 SOL chacun, 01:33–01:34 | voir le détail sous le tableau | **cluster CB/9W9b (B)** |
| 9 adresses Choupette hors groupe | BteHCe 02:08:33 (5 SOL) ; 6b29tK 02:09:38 ; 4JrabS 02:46:19 ; EEdq9 06:48:34 ; Douvv 11:14:31 ; 9cfRU5 12:59:49 ; B252 21:48:19 ; DfJHv 15/07 15:30 ; HMVYeT (hors table des 1 000) | | | BteHCe : wallet frais, BKscDV 10 SOL à 01:23 ; 9cfRU5 : 7Gw3gL 4 SOL à 02:18 ; 6b29tK : Coinbase 1 (2022) | EEdq9 618,8 ; 9cfRU5 729,2 (sort 1 471 SOL vers son propre financeur 7Gw3gL) ; DfJHv 478,5 ; 4JrabS 247,2 | B252 et HMVYeT envoient vers 9W9b, mais B252 dès le 2024-06-28 : le collecteur existait déjà |
| `H3QsBr…` | — | 14/07 16:43:58 | 3,03 | Coinbase 1, 0,834 SOL (2024-03-12) | **5 490,9 réalisé** ; sorties : service non nommé 11 637,6 ; 8YSi5y… 2 840 | aucune liaison |
| `GXZvXs…` | — | 02:15:41 | 2,5 | non résolu (19 tx antérieures) | **2 540,1** ; Co3zTr… 1 530,3 | aucune liaison |
| `9PrmF8…` | — | 02:28:56 | 4,197 | Coinbase 3, 5,56 SOL (2024-01-30) | **1 747,8** ; vers Coinbase 3/1/2 | aucune liaison (même financeur CEX que le créateur, donc **pas** un lien) |

Sorties du trio GoPCTr / AFDkwJ / EEpSRR (`data/coinbase3_batch_siblings_flows.json`, reçus figés) :
- **GoPCTr** distribue ses 7,256 M en 4 transferts de jetons (2 / 0,5 / 1 / 2 M, du 16/07 au 10/08). Aucune vente.
- **AFDkwJ** vend les 22/07 et 23/08 puis envoie **9,73 + 25,36 + 8,94 + 22,74 SOL vers 9W9b**.
- **EEpSRR** déplace ses jetons vers 98UuAv… puis les récupère.

## 5. Bot ou préparation ? Comparateur sniper (VI, NOUVEAU)

**Échantillon :** 54 tokens pump.fun créés à ±58 min du DMAGA, sélection systématique d'un slot sur 35 (`data/sniper_comparison_sample.json`, `data/derived/sniper_comparison_summary.json`).

| Mesure | Échantillon | DMAGA |
|---|---|---|
| Délai médian du 1er achat non créateur | **2 s** (p90 4 s ; Δslot médian 3) | 0 s (slot +1, bot `EYykLf…`) |
| Tx sur le mint dans les 60 s (médiane) | 22 | **74** (au-dessus de 94 % de l'échantillon) |
| Échecs dans les 60 s (médiane) | 13 | **50** (au-dessus de 96 % de l'échantillon) |
| G41v | — | +29 s / +67 slots puis +45 s / +100 slots, limites arrondies à l'UI ; 13e signataire distinct sur 182 |

Lecture :
- G41v, le cluster CB/9W9b (GoPCTr à +48 s) et le groupe 33 (6t2dz4 à +42 s) sont **plus lents que les bots**. Leurs montants arrondis (0,4–1,05 SOL) collent à une saisie manuelle.
- La demande initiale pour DMAGA est atypiquement forte. Elle s'explique par le contexte de l'actualité (tentative d'assassinat, 13/07 à 22:11) et ne démontre aucun accès privilégié.
- Le timing **ne prouve ni n'exclut** une connaissance préalable. La preuve de préparation repose sur les **financements avant le mint**, pas sur la vitesse.
