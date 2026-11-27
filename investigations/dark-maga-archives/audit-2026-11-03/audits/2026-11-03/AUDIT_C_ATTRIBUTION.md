# Audit C : attribution des wallets et protocole

Auditeur C, 03/11/2026, commit de référence `01ae5a4`. Personne n'est accusé. Aucune identité civile n'est présumée. Un wallet cité n'est mis en cause en rien.

## Verdict global : PASS

Aucune transaction fausse, aucun faux lien, aucune double comptabilisation et un protocole conforme au gel, mais le rapport décrit mal le périmètre autour du créateur et laisse de côté la preuve la plus forte (constats C-01 à C-05, à corriger avant toute publication).

Le sens des corrections est important : aucune ne fait tomber un lien. Elles déplacent le centre du dossier et remontent un niveau de preuve.

## Ce qui a été fait

**À l'aveugle, scellé le 2026-11-03 à 08:58:56 UTC (`work_C/SEAL.txt`) :** parseur propre (`c01_scan.py`, 2 699 114 lignes, 1 842 450 transactions uniques, 118 en échec), chronologie signature par signature des 4 graines depuis leur historique complet téléchargé (`chrono_*.csv`), nature des contreparties, graphe des transferts directs d'au moins 1 M (`blind_graph.csv`, `blind_seeds.md`), témoin de 120 adresses de dépôt Coinbase.

Limite de cet aveugle : la consigne et l'index de ma mémoire citent déjà « 33 wallets », 40 transferts et 48 expéditeurs. Je n'ai lu aucun fichier interdit avant le sceau, mais je connaissais ces nombres. Mon résultat scellé ne les reproduit pas : sans coupure de date, ma composante compte 104 wallets.

**Recalculé après le sceau :** les 40 transferts, le groupe avec coupure à 19:03:27 UTC, les soldes à l'instant T depuis les post-soldes, la comptabilité avec et sans transferts internes, les premiers financeurs, le taux de fond des 48 expéditeurs, les salves, les retraits Coinbase du 14/07, les correspondances entre dépôt et retrait, les ventes en 24 h du groupe, les ventes brutes du pool Raydium, le pHash, les rangs et Holm du test gelé.

**Non recalculé :** les montants par échange de C37 ; le dénominateur « autres détenteurs » de C41 et le total 190 551 SOL de C15, lus dans `trades.parquet` et recoupés seulement par la sortie brute du vault Raydium ; les mesures M1 à M7 elles-mêmes (rangs recalculés depuis `metrics.csv`, mesures non recalculées depuis les swaps) ; le lien X vers wallet au-delà des preuves légères.

Réseau : 11 367 crédits comptés à 10 par page sur 20 000 (`work_C/credits.csv`), bruts dans `audits_work/C/net/`.

## Constats

### C-01, MAJEUR : la série de retraits Coinbase d'avant le mint n'est pas vue

**Preuve.** Le rapport cite le créateur (01:32:23) et `5QhJJc…` (01:40:50), « 8 min 27 s plus tard », et conclut : « un hot wallet sert tout le monde ». Entre ces deux instants, il y a 15 retraits Coinbase à 0,5, 1,0 ou 1,05 SOL, un toutes les 38 s en médiane (écarts [42, 25, 39, 6, 45, 40, 34, 43, 52, 32, 37, 40, 35, 37]) :

| UTC | Hot wallet | Destinataire | SOL | 1re tx du wallet | Dans les 33 | Versé à 9W9b, SOL | Tenu à 19:03:27, M | Signature |
|---|---|---|---|---|---|---|---|---|
| 01:32:23 | Coinbase3 | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0.5 | oui | non | 0.593 | 7.11 | `5Ys6ggx4Fr3eYA4fdaDwowiuZg4HEbcRd6MYcPfspDX3g9KzLKMuKVh7ukUNVy3bpZwwhFT9ZLe2tQFMunHea4Dd` |
| 01:33:05 | Coinbase3 | `GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC` | 0.5 | oui | non | 0.969 | 5.26 | `4QxgQHNQtkWzir3nr5qZr6CfaWJf7ZUzw3wMoksBUUjLS8nofh9jGT3yDxSrDdMLt3fpUirEPehcHjkA13PKGYky` |
| 01:33:30 | Coinbase3 | `AFDkwJXJPCkZUjGo4mrrRZY53xU1vMSvXsyQiKdEZN93` | 0.5 | oui | non | 66.767 | 1.74 | `67gZiXkLDwerix8bnJCoPfY73SRAqK5DzyRALZjdWaz47zWTAoNd2HN7SN9rnNpELpZTaBjEaCG4W3kzGDqAd3PG` |
| 01:34:09 | Coinbase3 | `A52fNskQkLPD6oBdXFwznrmrT52jNdgvh2MCRWGqaiCW` | 1.0 | non | non | 0.000 | 0.00 | `4Nmd3bncho3u7aLQXcqFqbSTmRZ2fgd8qHWZZjogyo3ENdCLbgJxkRuRxg4YDQhexJp3hkvdQYq4gaCbeS9uStup` |
| 01:34:15 | Coinbase3 | `EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa` | 0.5 | oui | non | 8.022 | 2.46 | `4918LwRUfs95omfpgBKMToNq7DYi98Fh1sVMWgo8zLVxTusHRoVZyoQhA65f7aRxwjowKnmSrDNGwLwSpSG4GaWh` |
| 01:35:00 | Coinbase1 | `6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM` | 0.5 | oui | non | 29.411 | 5.04 | `21RBuWf1mKgUFfhUKBmtfKqi6nEGJeSqmM7FNGm8CBgASAy1S48ot45h6uQKypq3udmMoNSd8QvkmVAKUxEXpUoq` |
| 01:35:40 | Coinbase2 | `ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH` | 1.0 | oui | non | 0.109 | 0.25 | `5NUDHAsyv7tMN8wi6Tb4AvCHDo1uUhjeQbxB2v5E6zML8YizAVdPNxBxSVv49ZQbDPV9s6ASSurMszxPkZXvNWYF` |
| 01:36:14 | Coinbase2 | `HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ` | 1.0 | oui | non | 0.276 | 1.32 | `gUQjZXYWfo5paEpR8ep2zCk9EEeGuftqUL8cEyv1VkQrsrMYzPFjCZo7yWM4JLZfH18fPWzo729TMXyqC3CtKg1` |
| 01:36:57 | Coinbase1 | `6ZMaqHjPYpPdYor9qNGJP7bmunaFCuWcDVjDkR5H3b1J` | 1.0 | oui | non | 95.601 | 1.22 | `a8LwZn4nQUUA7j51Sc8pCCk4y2AZeH8GCMkaFHJqha8SePJxeSRi5Ttx2sy1gYCa9wUmguiKoThzt7vEAG74PE7` |
| 01:37:49 | Coinbase3 | `5s3ogzsq8cvwHtS1B6MhwUUp9CyzugJ6y3WqLPM9Ee3C` | 1.05 | oui | non | 37.710 | 1.32 | `3xgsew5Ua5zxFwZ7HcVLhDAvzBoGrSmha9dZQV9GzXe4Tpqw5bkAUP3CaKisGWghBf9drGJhFApgUyFBLsPTKpUY` |
| 01:38:21 | Coinbase1 | `Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt` | 1.05 | oui | non | 0.000 | 1.46 | `3qnLH9qL4aUj6JLaP3vw8BetmFMYa9sowoivhRTJ2e64X4XPrAFLMJAmk1tQTttNSfUz7rhpvLvfVc8Mbwr9hn4j` |
| 01:38:58 | Coinbase3 | `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 1.05 | oui | oui | 31.710 | 6.75 | `2sPrsWKLgo452VgDLu7QJWFAF3VRHw2jmGJpB6ZLLsxHe9oyisyUkJ6H8WaLLWaR9UCJLFcdYu1zJ84rejJgDiKz` |
| 01:39:38 | Coinbase3 | `Gmc1EGGV4TQfS3Hs8qvNV6u9MMWoS6AJ6f6WLHS9VRjd` | 1.05 | oui | non | 40.765 | 0.00 | `4VdpfqKkCBzeEMF7LXibn4j7UydVsrpiCDLGDpS896HYMHHbXLwX9ENV61PZXPGmmudqMhdnLXbHa4pXJefyTkXg` |
| 01:40:13 | Coinbase2 | `4pKFTQxsc69nzioRwPuAwUm49MRP4KzBmvrfjRCpEe5g` | 1.05 | oui | non | 0.100 | 8.15 | `2r6gBypSxfzq8yT3Y7qQ5SNpqT3XiYs175BEthroK5ZtKnoGTewwaQhDqZeK12YzoBZhE7vzCHfApNuXKvEraNoG` |
| 01:40:50 | Coinbase2 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 1.05 | oui | oui | 0.125 | 19.27 | `RpB7AKeKUJMiJ3rRKBtdxuuHsFvGrDN8gVKNxKFCaBQ64A5rxB2YuVVv5KnvWvw3asdg5ZGmq1KWob1wuhPPVdR` |

- 14 des 15 sont la toute première transaction du wallet. 14 touchent ensuite DMAGA, **13 reversent ensuite au même dépôt `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL`**. Taux de fond sur 2 h (`cb_window.csv`) : 119 des 2 201 destinataires touchent DMAGA, 5,4 %.
- Les 6 retraits exacts de 1,05 SOL des 2 h sont tous dans la série. Sur 13 retraits exacts de 0,5 SOL, les 5 de la série touchent DMAGA, les 8 autres jamais.
- Fenêtres témoins (`cb_series_ctrl.csv`, 8 fenêtres de −14 à +14 jours) : des montants ronds, il y en a partout, 14 à 23 sur 510 s dont 5 à 13 wallets neufs, contre 28 dont 22 ce matin-là. La rondeur seule ne prouve donc rien. Ce qui sépare la série, c'est le retour vers le même dépôt : 13 sur 15, contre un taux de fond de 0,55 % (C-03).
- Rythme proche des salves de sortie du 26/01/2025 (écarts de 33 à 69 s pour l'essentiel) : une main qui clique, wallet après wallet.
- Chronologie de préparation, jamais mise bout à bout dans le rapport : 00:52:29 `74qFhHyp…` vers `6t2dz4jm…` ; 00:59 et 01:00 vers `8YrEVPQq…`, `99Xrt5uu…` ; 01:32:23 à 01:40:50 série Coinbase ; 01:46:23 à 02:03:38 virements de `G41vRrsH…` ; 01:57:02 création de la chaîne Telegram (`docs/SOCIAL_FINDINGS.md`) ; 02:05:25 mint.

**Limite.** La fenêtre a été choisie après avoir vu les deux premiers retraits (recherche a posteriori) : le chiffre fort est le retour à 9W9b, pas la fenêtre. Un retrait Coinbase ne donne pas le titulaire du compte.

**Impact.** « Un hot wallet coupe la trace » est trop court ici. Pour le créateur et ces wallets, un même client Coinbase dès avant le mint devient l'explication la plus simple. Le niveau C d'« un acteur unique dès le lancement » est sous-évalué pour ce périmètre.

**Correctif proposé.** Ajouter la série à `reports/ATTRIBUTION.md` et `docs/CASE_REPORT.md`, B pour « même client Coinbase » sur ces wallets, C maintenu pour le groupe de 33 dans son ensemble.

### C-02, MAJEUR : « un ensemble financier précoce, autour du créateur » décrit mal le groupe de 33

**Preuve.** Le créateur n'est pas dans les 33 et n'a aucun transfert de jetons vers eux (son seul transfert va à `BuHUkjUy…`). Seuls 2 des 33 (`5QhJJc…`, `7FGoCB63…`) sont dans sa série de financement. 4 des 33 versent à 9W9b (`member_evidence.csv`).

Le graphe de SOL (`sol_edges.csv`, `c44.out`) montre des grappes antérieures au token : `74qFhHyp`, `AtZjv3Du`, `35nAuv6j`, `C7i9beNH`, `6t2dz4jm` liés depuis le 17/05/2024 ; `G41vRrsH`, `NxtXcmEW`, `GFpqfjEQ` liés depuis le 10/04/2024 ; le bloc `Ei5yGz8d`. Le jour du mint, ces grappes sont soudées par quelques transactions (41 M `AtZjv3Du` vers `NxtXcmEW`, 1 M `NxtXcmEW` vers `GFpqfjEQ`).

**Impact.** Le périmètre le mieux relié au créateur n'est pas celui du rapport. Périmètres mesurés à 19:03:27 UTC, sur 938,0 M : 33 wallets 217,04 M (23,1 %) ; série Coinbase 61,36 M dont 35,34 M hors des 33 ; 48 expéditeurs 92,08 M dont 48,20 M hors des 33 ; union de 79 wallets **266,7 M, 28,4 %**, à comparer aux 260,4 M « élargis » du rapport, niveau C. L'existence de grappes antérieures au token va contre un propriétaire unique des 33.

**Correctif proposé.** Présenter deux périmètres distincts : le groupe de 33, relié par transferts, et le périmètre créateur, relié par la série et le dépôt. Retirer « autour du créateur » pour les 33.

### C-03, MAJEUR : la nature de 9W9b peut être tranchée, et « 94,5 % » n'est qu'un plancher

**Preuve.** Le rapport écrit « adresse de dépôt ou relais personnel : non tranché » et « 48 expéditeurs seulement : pas un service de masse ». Témoin : 120 adresses tirées au hasard des transactions des 3 hot wallets Coinbase, juin à octobre 2024 (`c12_ctrl_deposits.py`, `ctrl_stats.csv`, 41 relais purs).

| Mesure | 9W9b | Témoin |
|---|---|---|
| Frais de balayage | 155 000 lamports sur 39 des 59 sorties | 155 000 lamports parmi les 3 frais les plus fréquents de 35 des 41 relais purs |
| Délai médian entrée à sortie | 126 s | 81 s |
| Signataire des sorties | le wallet, 59 sur 59 | le wallet |
| Nombre d'expéditeurs | 48 | médiane 2, P90 36, P95 98, maximum 131 (plafonné à 3 pages) |
| Expéditeurs ayant un solde DMAGA | **31 sur 48, 64,6 %** | **8 sur 1 452, 0,55 %** ; 7 dépôts sur 120 en ont au moins un, jamais plus de 2 |
| Montants à 3 décimales | 87,5 % | médiane 57,6 % |
| Expéditeur vidé sous 0,02 SOL | 71,6 % | médiane 25,6 % |
| Plus longue rafale ronde et vidée sur 10 min | **9 wallets** | **maximum 3 sur 120** |

Les 6 destinations hors des 3 étiquettes reçoivent aussi les balayages de 53 des 120 témoins : `FpwQQh` 39, `D89hHJ` 35, `DPqsob` 29, `9obNtb` 28, `4NyK1A` 20, `8JUEoH` 5 (`c56.out`). Ce sont des hot wallets de la même famille, absents de la liste Dune.

**Ce que signifie 94,5 %.** Rien sur l'expéditeur : c'est le balayage automatique d'un compte de dépôt vers les hot wallets de la plate-forme, et la vraie part est proche de 100 %. Ce n'est pas un wallet qui « envoie à Coinbase ».

**Ce que signifient 48 expéditeurs.** Le nombre seul ne distingue rien : le raisonnement du rapport ne tient pas, 10 % des relais témoins atteignent au moins 36 expéditeurs. Ce qui distingue, c'est leur population.

**Test client ou service partagé.** Quatre tests sur la chaîne, tous en faveur d'un compte de dépôt tenu pour un même bénéficiaire : (1) taux de fond sur une population indépendante, 64,6 % contre 0,55 % ; (2) empreinte de vidage à la main, 9 contre 3 au plus ; (3) retraits de la même plate-forme vers les mêmes wallets, 13 sur 15 (C-01) ; (4) correspondance exacte entre un dépôt et un retrait (C-04). Le test décisif reste hors chaîne : une réquisition de Coinbase. Rien n'exclut un compte tenu pour plusieurs personnes par un trésorier.

**Impact.** B pour « compte de dépôt Coinbase », B pour « même bénéficiaire pour les rafales ». **Correctif proposé.** Remplacer « non tranché » et retirer l'argument des « 48 expéditeurs seulement ».

### C-04, MAJEUR : le transfert du créateur vers BuHUkjUy est un lien, laissé « non interprété »

**Preuve.** Le 10/07/2025 à 03:05:01, `4dYxmSbn…` verse **6,576437507 SOL** à 9W9b, `SJmX4rVPRXUm8cUqkRFKAJz2RX5Fc3EQE2Z82p72bqyqM2ceP4T6Uk5zmH6aEK4LoX7JxQfWYXXoJNsL4nXviCw`. Le 12/07 à 16:43:59, première transaction de `BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc` : **6,576337507 SOL**, soit le même montant à exactement 100 000 lamports près, depuis `5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs`, `2hUi9BhncmfYeBkFKLthvde1zKa5Xy3iHnBusNarf22YtsCpqCqWx6HaMaNCuGURMWLz4vtjCxHQDCp9Kr2DW4a1`. C'est la seule correspondance sur 11 dépôts non ronds (`deposit_withdraw_match.csv`). 71 s plus tard, le même wallet reçoit 10 000 USDC de `9obNtb5G…`, une des destinations de balayage de 9W9b. Le lendemain, le créateur lui envoie 7 397 559 jetons, `8cAyFE6ifX5anKxazY1AwJWszZoFLUvjGbjkkqeKC79FMR6kS8khJLNQ47fFhwWKFFNHB21Q4kmtTSXhmRA23A1`.

`5g7yNH…` n'a pas d'étiquette publique. Il émet 1 000 signatures en 5 h et reçoit des balayages du dépôt `H9Xezqfd…` (`c62.out`) : il appartient à la même famille de hot wallets.

**Impact.** Troisième élément indépendant, en plus du gaz et de la salve : les jetons du créateur finissent chez un wallet financé par le compte derrière 9W9b. **Correctif proposé.** Le sortir de « autre fait, non interprété », niveau B pour le lien de 2025.

### C-05, MAJEUR : 2,4 % et « moins vendeur » reposent sur les seuls swaps des 33

**Preuve.** La mesure elle-même est juste (C15, C41 en PASS). Mais dans les 24 h, 32,1 M sortent du groupe par transfert. 3 destinataires, surtout `FZLmLkf93NPU44zwCTcrRwYfFfx4orZN2cqdUSufft8i`, vendent 4,88 M pour **973,3 SOL** dans la même fenêtre (`c50.out`). 25,7 M vont à 8 wallets entre 17:17 et 17:28 le 22/07, dont 5 sont regroupés le 26/07 sur `GZXKYzwZ…` (`comp_5Q.txt`).

- Ventes avec ces destinataires : 5 498 SOL, **2,9 %** au lieu de 2,4 % des 190 551 SOL.
- Sur la même base, swaps et transferts sortants : groupe (48,80 + 32,10) / 217,04 = **37,3 %**, autres détenteurs (224,95 + 43,99) / 643,6 = **41,8 %**, au lieu de 22,5 % contre 35,0 %.

**Impact.** La lecture modeste reste vraie en ordre de grandeur. L'écart de vente se réduit de 12,5 à 4,5 points. **Correctif proposé.** Écrire « au moins 2,4 % », donner 2,9 % et les 37,3 % contre 41,8 %.

### C-06, MINEUR : le niveau B des 29 wallets est une moyenne

**Preuve.** `member_evidence.csv` : 31 des 33 ont un lien de SOL, un financeur commun ou un versement à 9W9b en plus des jetons. Deux sont faibles : `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` (2,5 M, seul un transfert) et `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` (13,9 M). Ce dernier reçoit 18 M, `2wxn47W59GaU8YcsTSVSJ1mufSe1g2xLjcAV3FJdu2RHx5zE6Sawncmw1W8A5PNw9u7qQpzZoxeiCGXYpC2zyTUB`, et paie 23 SOL 8 min 35 s plus tard, `2t51AXk6zzRKFqd8xjuEeUzdVXxrjw1H5U19HxyB9xAFWmrY9C8gPS7KoSh1tphxwNY3fbWhzcNxzW8X9UtwHnKU` : forme d'une vente de gré à gré, à 45 % du prix que `5QhJJc…` paie sur le marché 7 min plus tard. Nuance : il finance `HBsgbps…`, un expéditeur de 9W9b, 8 jours après, `H6G5ZxxcdvWhQicWKcLb2yQxmmFqyqTcD1wxFzcANqEkgWmVW2ZWBL9rpE6gMu9vUgCwVNhfmZEpveFMBenhjih`.

**Impact.** Sans eux : 149,7 M, 16,0 %. **Correctif proposé.** Citer la fourchette 16,0 à 17,7 %.

### C-07, MINEUR : le wallet Habp5bnc sort du groupe à cause de sa poussière

**Preuve.** `NxtXcmEW…` envoie 8 M à `5QhJJc…` à 01:14:34 le 15/07, `2o4UXdGtAFqxWc9kGkLxfTFEyVX8vJDuebnk6eG7Umicp74VqVUpGwzZWXBeJeXds5SP52N6NRMYyxtEZbi6xd57`, et `5QhJJc…` les renvoie à `Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` 112 s plus tard, `4gzzHCqB8ZTLPNSs8fgyskcBsLpAn9UjYwqFFiqryxBqdApxBKMvzy8j7RULnJ3xCCkaC1ScepCC1PiUJdruZFS4`. Avec la règle écrite, le groupe compte 34 wallets et 41 arêtes. Il en sort parce qu'il est vu par au moins 15 wallets tracés à cause de ses envois de poussière (`ana_60_clusters.py`, table `svc`). Le rapport cite l'arête au § 5 sans dire qu'elle change le compte. Il vend les 8 M le 21/07 à 03:47:21 : solde nul à l'instant T, 217,04 M inchangé.

**Correctif proposé.** Le dire, et ne pas compter comme service une adresse exclue par sa seule poussière.

### C-08, MINEUR : C36 sous-compte G41vRrsH d'un wallet

**Preuve.** `CZsBW8yC…` manque de `funding_edges` ; son premier financeur est `G41vRrsH…`. Résultat sur 33 wallets : 11 dans le groupe, 11 G41vRrsH. Trois premiers financeurs diffèrent selon la définition, sans changer les comptes (`c50.out`). **Correctif proposé.** Écrire 11 sur 33 et 11 sur 33.

### C-09, MINEUR : « Acheté 426,2 M, 831,9 SOL » n'est pas « avant Musk »

**Preuve.** Ces colonnes couvrent toute la vie des wallets, à côté d'une colonne « détenu avant Musk ». `7mdCAs8C…` y compte pour 338 SOL achetés après le 23/07. Achats réels avant 19:03:27 : 359,79 M. **Correctif proposé.** Renommer les colonnes.

### C-10, MINEUR : « ordre de vente » cache un aller-retour

**Preuve.** 7 105 960 jetons vendus en 2 exécutions à 63 s d'écart, `3MjSKVjP5RERFSnQwzvA3m9haFF9JDR1MyW3rzFBNbyyXtbtkzfm2D1AUEcXT33x8gKfCbJb363AU2cQGWs8BinG`, `Ayr9HoxiKrMNqh8JXTJBn35Y7JzaorXWJW9dHD2AAHyNUfv8vyQzXXRtU1sy43zWKArFEC3oH7dRF5MRTov2RJT`, pour 4 598,77 USDC. Le 13/07, ordre d'achat de 4 500 USDC, `3eNyvVpP5LnZVuSDzmjQFrTmptmLhjKDJ3sf4SitjUGQQTMea6BLWQmUMJS3MHEdwtwLbNtMTxuFnTD4mp2iHPVj`, soit 7 397 559 jetons, transférés le jour même. Reste 98,77 USDC. `Hx1UvdgM…` est bien l'escrow DCA : compte créé avec le propriétaire `DCA265Vj…`, log `OpenDcaV2`. Le « non vérifié » du rapport peut tomber.

**Impact.** Le créateur n'encaisse presque rien : il déplace sa position. **Correctif proposé.** Le dire au point 5 de l'essentiel.

### C-11, MINEUR : deux écarts de tenue dans l'étude gelée

**Preuve.** Le plan veut que `tronque_sans_S20` soit compté. Les 5 tokens concernés sont passés en `reporte_budget`, statut écarté avant le compteur : la clé est absente de `selection_counts.json`. `selection.jsonl` (modifié le 03/11 à 03:24:24 UTC) reste hors du verrou, et le statut `reporte_budget` n'est pas produit par le code gelé. Effet nul sur le verdict : les 213 tokens principaux sont tous `retenu_superset` (`c33_protocol.out`). **Correctif proposé.** Publier le compte de 5 et faire valider l'amendement 001 par Benjamin, ce qui reste à faire.

### C-12, INFO : le dénominateur de 938 M inclut 33,3 M sur 11 adresses classées hub

Hors tous services : 904,7 M, part du groupe 24,0 % au lieu de 23,1 %. Pas une erreur : « hors pools » est écrit.

### C-13, INFO : le brut mint, pool et venues ne voit pas tout

Une instruction `Transfer` ne cite pas le mint : 237 transactions d'au moins 1 M manquent du brut, dont les 5 transferts vers `AtZjv3Du…` (84,5 M). Le rapport les compense. Sans compensation, la somme de `ta` donne 301,6 M pour le groupe. Après correction, la somme de tous les soldes à T vaut 1 000 M à 0,005 M près : avant Musk, il ne manque rien. Après, il reste 345 écarts d'au moins 1 M sur 35 propriétaires, surtout `D5jx4wmx…`, `GCvHhEUY…`, `Bya5eBy9…` (`continuity_gaps_1M.csv`). Toute lecture de soldes après Musk hors de `flows` doit le savoir.

### C-14, INFO : un compte de mise en commun rejoint des wallets sans lien

`C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN` reçoit 13 versements d'un million par 11 wallets du 16 au 20/11/2024, plus un versement fractionné (`hP2AfR5s5kuCa7HyJz7Q1Lg3PEj9nyW6RQ8jzNBZLQvSrS26aLS2PAPcWgogZXfwwbj3oezKbp4uyw1YWpxQ3Rm`, premier versement), 14,0005 M au total, puis envoie tout d'un coup. Il fait passer ma composante de 104 à 123 wallets. Il est dans la grappe de 345 du rapport, qui ne la lit pas comme un propriétaire unique (C38). Il verse lui-même 7,417 SOL à 9W9b.

### C-15, INFO : pistes testées et écartées

- **Programme `HQ2UUt…` commun à 4 membres :** 25 006 tx, 2 302 payeurs, pas une empreinte.
- **Bots de snipe vendus en service :** des achats de la première heure paient des comptes de frais de terminaux (`F4hJ3Ee3…`, 7 tx, 4 wallets ; `AVUCZyuT…` ; `9yMwSPk9…`). Cela ne relie personne, et aucun lien du rapport ne passe par là.
- **Poussière et adresses imitées :** `9W5J3orC…BxpL` imite `9W9b…BxpL`, `AmroX3cQ…JAF1` imite `AQVgyg8P…JAF1`. Ce sont des envois d'un lamport ou presque : aucun n'est compté comme lien.
- **Comptes de jetons temporaires :** `6SRNoR8P…` et `7h4A6tLt…`, très fréquentés, sont les comptes WSOL de `5QhJJc…` et `G41vRrsH…`, pas des contreparties.

### C-16, INFO : sensibilité au seuil

Groupe avant Musk, sans Habp5bnc : 33 à 1 M, 19 au-dessus, 18 à 3 M, 17 à 4 M, 16 à 5 M, 14 à 7 M, 2 à 10 M (`prevent_sens.csv`). Vers le bas : 34 à 0,25 M, 40 à 0,1 M, avec `Gmc1EGGV…`, membre de la série Coinbase. Toutes dates : 104 à 1 M, 41 à 1,5 M, 36 à 3 M, 22 à 5 M, 6 à 10 M (`sens_threshold.csv`). Le rapport signale la coupure en 19 et 14, pas le reste.

## Tableau des liens

Preuve d'une transaction, d'une coordination, d'un contrôle commun : trois questions séparées.

| Lien | Transaction | Coordination | Contrôle commun | Explication alternative | Preuve |
|---|---|---|---|---|---|
| 5QhJJc vers créateur, 0,032 SOL, 06/07/2025 | A, signé par 5QhJJc seul, programmes System et ComputeBudget | B : solde du créateur 0,001288 SOL, l'ordre coûte 0,0091 SOL, ordre 35 s après, 5QhJJc donne 93 % de son solde | Pas établi par ce seul lien | Frais d'un service, ordre : **écartés**, aucun programme. Service de gaz : écarté. Un ami qui dépanne : **possible**, c'est encore une concertation | `Nfzx313VrsXHoEhpfXadwi16CXZyReEEjJA1hojZERATrdgRtz8TdNrveT4wTXPbyUFPySSzFPPXBtXB4LBSYM4`, `2BUp8LXmhuhpiEtp1w4pNLHTuywq7Jf1hxpPHWx9jXmRA3kzwRDutXwfKne4nKVULvwsbCPyN5j57d1j7itbfT1k`, `c15_bal.py` |
| Salve vers 9W9b, 26/01/2025, 15 wallets dont créateur et 5QhJJc | A, chacun signe | B | B : 15 clés en 2 rafales, 33 à 69 s entre deux wallets pour l'essentiel, 3 décimales, résidu sous 0,012 SOL | Dépôt partagé : **écarté** pour cette salve, rafale de 9 contre 3 au plus. Trésorier d'un groupe : possible | `65aNPjoC8nb4yUu3oD5HGzSvyC9DLJZEK1LrkDD8hEXPzdv8Y4FJRgJEXZXXbDuHtYi8UNU7XYdmycKwNi2BS3g2`, `1Ae21aJQzoAv6aa6pxkUVAXaCYHXXah5sUopKdEBJ1n5rgtDkfveDvxvdJHW6awLo1PjTJ7ERBWNhp3EEEsTMmi`, `bursts_9W9b.csv`, `c48.out` |
| Série Coinbase, 14/07/2024, 15 retraits | A | B : 13 sur 15 reviennent à 9W9b | B pour « même client Coinbase », pas pour une personne | Hot wallet commun : **écarté comme seule cause**, 0,55 % de fond. Hasard des montants : les montants ronds sont courants, ce n'est pas l'argument | `cb_series.csv`, `c52.out`, `c53.out` |
| Salve vers 9W9b, 23/07/2024, G41vRrsH, C73Yv9iH, AtZjv3Du, EGtyQEgM | A | B : 8 SOL chacun ou presque, 164 s | C : soldes non vidés, résidu médian 64 % | Coïncidence sur un dépôt partagé : peu probable, balayés ensemble, 31,9 SOL | `bursts_9W9b.csv`, `chrono_9W9b3z.csv` |
| 9W9b vers BuHUkjUy par Coinbase, créateur vers BuHUkjUy, 07/2025 | A | B : montant identique à 100 000 lamports près, 7,4 M le lendemain | B pour « même client » | Hasard sur 10 chiffres significatifs : **écarté** | `SJmX4rVPRXUm8cUqkRFKAJz2RX5Fc3EQE2Z82p72bqyqM2ceP4T6Uk5zmH6aEK4LoX7JxQfWYXXoJNsL4nXviCw`, `2hUi9BhncmfYeBkFKLthvde1zKa5Xy3iHnBusNarf22YtsCpqCqWx6HaMaNCuGURMWLz4vtjCxHQDCp9Kr2DW4a1`, `8cAyFE6ifX5anKxazY1AwJWszZoFLUvjGbjkkqeKC79FMR6kS8khJLNQ47fFhwWKFFNHB21Q4kmtTSXhmRA23A1` |
| G41vRrsH vers 13 wallets, 0,5 SOL, avant le mint | A | B : 13 sur 15 de ses virements exacts de 0,5 SOL, en 17 min, fini 1 min 47 s avant le mint | B pour les 7 sans achat qui ne servent qu'au transit ; finalité non établie | Service : **écarté**, trader ordinaire, 390 tx, pas de balayage. Bot : écarté. Connaissance du mint : compatible, non démontrée | `g41v_recipients.csv`, `chrono_G41vRr.csv` |
| GFpqfjEQ vers 10 wallets, 11 transferts, 07:57-08:32, puis regroupement 14:22-14:25, 21/07 | A | B | B : wallets de transit, 6 à 8 tx pour FjuV7m, HkrGvx, HKXb8L, 8xjM4f, qui renvoient tout 6 h après | Gré à gré : écarté, aucun paiement de retour | `edges40_replay.csv`, `c42.out` |
| 6t2dz4jm, 8YrEVPQq, 99Xrt5uu, AW63YBXX vers AtZjv3Du, 84,5 M, 14/07 | A | B | B : SOL entre eux depuis 06/2024, gaz d'avant le mint | Service : écarté. Absents du brut mint, revus par `flows` | `sol_edges.csv`, `c44.out` |
| AtZjv3Du vers NxtXcmEW, 41 M | A | C+ | C : relie deux grappes antérieures | Gré à gré : aucun retour de SOL mesuré, reste possible en un autre actif | `dLnMuAksDjjA1ioFbB4SPDNPLFURnrp6bxwYjwBLFYvYLTRBEDUN8eFpQ2zwySyXdHu34UijFYN1Bcnv17ivDnM` |
| NxtXcmEW vers GFpqfjEQ, 1,0 M, arête au seuil | A | B : SOL dans les 2 sens depuis le 10/04/2024, 0,9 SOL 5 min après le mint | C+ | Le rapport note 2 virements, sa fenêtre commençant le 13/06, j'en lis 6 avant le 14/07 | `2epM63ZTNSNSmXDo87Xn7qrJKkRXLD1znE9awNj2u2QZkdS4VNNeAsBnkaBfJ1UK6YLh8UT9gQiStAHrZ6RcYa1R`, `c44.out` |
| NxtXcmEW vers 5QhJJc, 8 M, puis 5QhJJc vers Habp5bnc | A | C | C | Transit, cadeau : **retenus comme possibles**. Seul lien de jetons de 5QhJJc avec les grappes | `2o4UXdGtAFqxWc9kGkLxfTFEyVX8vJDuebnk6eG7Umicp74VqVUpGwzZWXBeJeXds5SP52N6NRMYyxtEZbi6xd57`, `4gzzHCqB8ZTLPNSs8fgyskcBsLpAn9UjYwqFFiqryxBqdApxBKMvzy8j7RULnJ3xCCkaC1ScepCC1PiUJdruZFS4` |
| 4wComYHQ vers 74qFhHyp, 15 M, bloc de 4 | A | C | C | Le rapport a raison, aucun lien de SOL avec le reste | `1X9w8xLDu39Ti9TjHsJud4AMzcfFjso5KBo1WRrLoKep1PwZfQnrRuUL7hnR2QPn3SfngjKuLeqK3pKCP2o273G`, `c44.out` |
| 5QhJJc vers 7mdCAs8C, 18 M, contre 23 SOL | A | C | Non établi | Vente de gré à gré : **retenue comme possible**, prix à 45 % de celui du marché 7 min plus tard | `2wxn47W59GaU8YcsTSVSJ1mufSe1g2xLjcAV3FJdu2RHx5zE6Sawncmw1W8A5PNw9u7qQpzZoxeiCGXYpC2zyTUB`, `2t51AXk6zzRKFqd8xjuEeUzdVXxrjw1H5U19HxyB9xAFWmrY9C8gPS7KoSh1tphxwNY3fbWhzcNxzW8X9UtwHnKU`, `H6G5ZxxcdvWhQicWKcLb2yQxmmFqyqTcD1wxFzcANqEkgWmVW2ZWBL9rpE6gMu9vUgCwVNhfmZEpveFMBenhjih` |
| 5QhJJc vers 9u5JKgWd, 2,5 M | A | D | Non établi | Cadeau, vente : **retenus**, aucune autre preuve | `member_evidence.csv` |
| Autres feuilles reçues par des wallets neufs (HGBiExZR, Gcyg2jeL, Akp46Dic, GPMYCuus, BuBXTWEC, 4wComYHQ) | A | B | B : wallet créé au plus 47 s avant la première réception, financé par le groupe | Écartée | `c42.out`, `sol_edges.csv` |
| H3QsBr, GXZvX, 9PrmF8 avec les 33 | Aucune | Aucune | Aucun | 9PrmF8 sort vers un autre dépôt, `H9Xezqfd…`. Absence d'arête, pas preuve d'absence | `c47.out`, `c62.out` |

**Le mot « concertée » est justifié.** Le virement de gaz seul le soutient déjà, sans dire si c'est une personne ou deux. Le niveau B d'une action concertée est mérité. Il est même prudent, au vu de C-01 et C-04.

## Double comptabilisation

**Résultat : aucune dans les chiffres publiés.** Soldes recalculés depuis les post-soldes bruts de chaque historique (`members_table.csv`, `accounting_Tlow.csv`, `c58.out`), à 2024-07-21 19:03:27 UTC.

| Poste, M de jetons, 33 wallets | Valeur |
|---|---|
| Achats avant T (swaps) | 359,789 |
| Ventes avant T | −134,052 |
| Reçus par transferts internes | +392,917 |
| Envoyés par transferts internes | −392,917 |
| Reçus de l'extérieur | 0 |
| Envoyés à l'extérieur (dont 8 M vers Habp5bnc) | −8,700 |
| **Net, égal à la somme des post-soldes** | **217,0365** |
| Somme naïve achats et reçus internes, à ne pas utiliser | 752,706 |

| Chiffre publié | Recalcul | Double compte ? |
|---|---|---|
| 217 M | 217,0365 M | Non, les transferts internes s'annulent exactement |
| 166,1 M et 50,9 M | 166,111 et 50,926, somme 217,037 | Non, partition exacte |
| 19 et 14 wallets | 145,27 et 71,77 M, somme 217,04 | Non |
| 23 % et 17,7 % | 23,14 % et 17,71 % | Non. 16,0 % sans les 2 liens faibles |
| 938 M hors pools | 1 000 M moins 62,00 M Raydium. Somme brute des soldes 1 084,53 M avant de corriger les 5 transferts absents du brut (84,54 M), soit 1 000,00 M | Non, le rapport a bien corrigé |
| 4 525 SOL | 48,80 M vendus ; 4 408,7 SOL plus 18 935 USDC, environ 4 515 SOL | Non. Écart de 0,2 %, frais et conversion |
| 2,4 % de 190 551 SOL | 2,37 à 2,41 % ; 1 seule tx de vente sur 23 000 a plusieurs lignes (38 SOL) ; brut Raydium sens vente 187 715 SOL, arbitrages compris | Non. Plancher, voir C-05 |
| Réalisé des gagnants | H3QsBr 5 498,1 SOL reçus moins 7,27 payés, 5 490,9 ; aucun transfert | Non |
| Réalisé du groupe 5 594 SOL | Flux net 5 437 SOL | Pas de double compte, mais surévaluation de 157 SOL au niveau du groupe et bien plus par wallet : `C73Yv9iH` 1 686 SOL pour 5,5 SOL achetés et 23,6 M reçus. Le rapport l'annonce (C27) |

Le recalcul donne aussi les 33 soldes à T : `members_table.csv`, colonne `held_Tlow`.

## Protocole

**Passe 1, le code seul.** Population : migrations Pump.fun vers Raydium v4, filtre par pic (signatures par heure au moins 20 fois la médiane des 72 h, plancher 5, au moins 500, de création + 96 h à création + 60 j), capitalisation à S − 1 h entre 100 000 $ et 10 M$, au moins 20 swaps sur 96 h. Swaps du seul pool Raydium v4. Sept mesures calculées sur t < S. Rang unilatéral, p = (1 + nombre de comparateurs ≥ cible) / (k + 1). Holm à 0,05. Verdict par code, INCONCLUSIF sous k = 139. S1 sur fenêtres de 3 h de DMAGA, Holm séparé, hors verdict.

**Passe 2, comparaison au plan.**

| Point | Plan | Code ou fichier | Résultat |
|---|---|---|---|
| Période | 15/06 inclus au 01/09 exclu, 13 920 | `T_FROM`, `T_TO` ; 13 920 lues, du 15/06 00:02:43 au 31/08 23:49:56 | Conforme |
| Pic | 20 fois, plancher 5, au moins 500 | `spike_hour` | Conforme |
| Capitalisation | 100 k$ à 10 M$, S − 1 h, 200 tx | `fdv_at`, `BAND` | Conforme, 0 hors bande |
| Au moins 20 swaps sur 96 h | oui | `ana_10_table` | Conforme, 1 exclu |
| M1 à M7 | définitions du plan | `metrics.compute` | Conforme, ligne à ligne |
| M6 | transferts ignorés | seuls les swaps | Conforme, limite annoncée |
| Tests et Holm | rang, Holm 0,05 | `rank_p`, `holm` | Conforme. Recalcul : rangs 36, 39, 51, 116, 56, 33, 38 ; meilleur p 0,1557 ; seuil 0,00714 |
| S1 | 4 comparaisons, Holm séparé | `self_history` | Conforme, 27 et 28 fenêtres |
| Verdict | texte fixé | `verdict` | Conforme, identique |
| Variantes | R1, R2, R3 | k 212, 240, 210 | Conforme après amendement 001, à valider par Benjamin |
| `tronque_sans_S20` | compté | clé absente | **Écart mineur, C-11** |
| Comparaisons | 32 déclarées | 33 au registre, 1 exploratoire venue de code non gelé | Écart annoncé par le rapport |

**Le gel a-t-il précédé tout calcul ?** Oui, sur tout ce qui est vérifiable. `gel.py verifier` : 17 fichiers conformes au gel du 2026-11-02 23:47:06 UTC. Commit `26cf5c7` à 23:47:50, hash du plan dans ce commit identique au verrou (`15d6964c…`). Aucune différence depuis sur `etude_final/code`, le plan, `controles`, `collect`, `helius`, `config`, `col_40`. Registre : avant le gel, seulement les contrôles synthétiques ; `primary_*` à 03:25:36. `metrics.csv` à 03:25, après le gel, ajouté au verrou avant les tests à 03:25:30. `etude/` contient bien des pools synthétiques `pool0000x…`, donc aucune donnée réelle. Amendement 001 écrit à 02:46:05, avant `metrics.csv`, cohérent avec `resultats_vus: non`.

**Limite que le plan dit lui-même :** l'auteur connaissait déjà la courbe de DMAGA, ses gagnants et l'existence de transferts entre wallets. Rien dans les fichiers ne permet de prouver qu'aucun calcul n'a eu lieu hors registre, seulement que rien ne le contredit.

**Analyses hors plan.** Bien étiquetées : le groupe (« règle descriptive, hors plan »), le seuil choisi après avoir vu DMAGA (dans `COORDINATION.md`, pas dans `CASE_REPORT.md`), le financeur commun, la comparaison de ventes. Le mot « inhabituel » du tableau H2 s'appuie sur S1 à p = 0,069, secondaire qui ne passe pas Holm : acceptable car placé dans « ce qui va contre » et chiffré.

## Assertions Cnn

Voir `work_C/claims_C.csv`. 23 PASS, 1 FAIL (C19, troisième niveau seulement), 2 INCONCLUSIVE (C37, C39).

## Fichiers

`work_C/SEAL.txt`, `blind_graph.csv`, `blind_seeds.md`, `blind_seeds_v2.md`, `claims_C.csv`, `cb_series.csv`, `member_evidence.csv`, `edges40_replay.csv`, `accounting_Tlow.csv`, scripts `c01` à `c64`.
