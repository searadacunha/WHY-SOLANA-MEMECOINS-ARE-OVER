# Attribution : liens vérifiables, hypothèses, niveaux

Généré par `scripts/rep_72_links.py`. **Audit du 03/11 : NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent.** Voir `audits/2026-11-03/`. Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice, **D** non vérifié ou contredit. Aucune identité civile n'est recherchée ni établie. Un wallet cité n'est accusé de rien.

## Conclusion courte
**Aucun lien documenté entre un wallet et un compte du noyau (@DarkMagaCoin, @kikisknees, @Aristos_Revenge, @ChrisWinig).** Aucun de ces comptes n'a publié d'adresse de wallet dans ce qui est archivé (le mint, lui, est publié). Le lien compte ↔ wallet reste une lacune, pas une absence prouvée. Le corpus X est partiel.

## Les quatre pistes
| Wallet | Source | Acheté SOL | Réalisé SOL | P&L USD | 1er achat UTC | Ach./Vte | Reçu transfert M | Sorti transfert M |
|---|---|---|---|---|---|---|---|---|
| `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` | fils de tiers d'août 2024 et @XHEILIGX, 30/03/2024, voir audits/2026-11-03/work_E/X_FOLLOWUP.md, partie 6 | 281,19 | 1 747,8 | 317 215 | 14/07/2024 02:28:56 | 26/39 | 0,00 | 0,16 |
| `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` | @ai_9684xtpa, id 1815243177475121253, adresse entière dans le lien | 48,50 | 2 540,1 | 458 663 | 14/07/2024 02:15:41 | 4/103 | 0,00 | 0,00 |
| `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | @ramonos (URL @0xRamonos), id 1815221876190294470, capture | 53,36 | 74,2 | 12 118 | 14/07/2024 02:10:11 | 208/13 | 37,79 | 76,26 |
| `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc` | @ashrobin (URL @ashrobinqt), id 1815233925662306427, capture | 7,27 | 5 490,9 | 990 744 | 14/07/2024 16:43:58 | 2/48 | 0,00 | 0,00 |

- **Les quatre désignent-ils une même entité ?** Non établi, et rien ne le soutient pour `H3QsBr…`, `GXZvX…` et `9PrmF8…` : après retrait des services, aucun transfert direct ne les relie entre eux ni au groupe, et aucun n'envoie vers `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL`. Une absence d'arête n'exclut pas un lien par échange : les quatre passent par des échanges (A pour le fait, C pour toute interprétation).
- **Rapprochement des captures :** `5QhJJc…HScd` et `H3QsBr…T6cc` sont uniques parmi les propriétaires de DMAGA pour ce préfixe et ce suffixe. Pour `H3QsBr…`, 1 087 $ recalculés contre 1 086 $ sur la capture et 16,82 M contre 16,8 M (A). Pour `5QhJJc…`, la capture dit 37 transactions et 28,4 M : l'écart avec les 208 achats totaux s'explique en partie par des ordres DCA Jupiter (keepers `DCAK…`) et des transferts (B). La date « 3 jours » du post correspond aux achats DCA du 17 au 19/07, alors que le wallet achetait dès le 14/07.

## Le périmètre du créateur : niveaux distincts
Niveaux scindés depuis l'audit du 03/11 (C19) :
- **A :** les transactions et leurs signataires.
- **B, même opérateur ou même compte de dépôt :** le créateur et 12 wallets de la série Coinbase du 14/07/2024.
- **B, type de compte :** `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` est un compte de dépôt Coinbase. Son titulaire n'est pas connu.
- **B, lien de 2025 :** `BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc` et ce compte, par un montant apparié. Sans valeur pour le lancement.
- **C :** les 33 wallets pris ensemble, avec des grappes antérieures au mint, et un même bénéficiaire derrière le dépôt.
- **Non établi :** qui. @ramonos a seulement commenté `5QhJJc…` : **rien ne le relie à lui ni à personne au-delà de sa publication.**

| UTC | De | Vers | Montant | Actif | Ce que c'est | Signature |
|---|---|---|---|---|---|---|
| 14/07/2024 01:32:23 | `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0,5 | SOL | Le créateur reçoit de Coinbase 3, premier mouvement du wallet | `5Ys6ggx4Fr3eYA4fdaDwowiuZg4HEbcRd6MYcPfspDX3g9KzLKMuKVh7ukUNVy3bpZwwhFT9ZLe2tQFMunHea4Dd` |
| 14/07/2024 01:40:50 | `2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm` | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 1,05 | SOL | `5QhJJc…` reçoit de Coinbase 2, 8 min 27 s plus tard, premier mouvement du wallet | `RpB7AKeKUJMiJ3rRKBtdxuuHsFvGrDN8gVKNxKFCaBQ64A5rxB2YuVVv5KnvWvw3asdg5ZGmq1KWob1wuhPPVdR` |
| 19/02/2025 22:04:04 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `sYBdq543ZX4iAXpNzhT4kTvKBaEDUGkiUo9jBFYdaNd` | 3561097,392281 | DMAGA | `5QhJJc…` avait ouvert un ordre DCA du même type, 4,5 mois plus tôt | `2WJCLkibEpkEbpYqPFfuUchKjqhEm3rkRN7ybmtvy7vxNgKFiDbWUzUMSE4U2VzWSttJBRoSgGWTDg1pJswhSosU` |
| 06/07/2025 02:18:38 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0,032 | SOL | **`5QhJJc…` signe seul un virement de SOL vers le créateur, 35 s avant la ligne suivante** | `Nfzx313VrsXHoEhpfXadwi16CXZyReEEjJA1hojZERATrdgRtz8TdNrveT4wTXPbyUFPySSzFPPXBtXB4LBSYM4` |
| 06/07/2025 02:19:13 | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | `AYymVrcAyPgcMcFkk5NqaEBLj7C4KH2NYvLognUGCEq5` | 7105960,2649 | DMAGA | Le créateur signe un ordre Jupiter DCA de vente sur tous ses jetons ; le destinataire est l'escrow de l'ordre | `2BUp8LXmhuhpiEtp1w4pNLHTuywq7Jf1hxpPHWx9jXmRA3kzwRDutXwfKne4nKVULvwsbCPyN5j57d1j7itbfT1k` |

En plus de deux ans, le créateur n'a reçu que 3 virements d'au moins 0,003 SOL : 0,5 SOL de Coinbase 3 (14/07/2024), 0,57681998 SOL de Raydium AMM v4 authority (16/07/2024), 0,032 SOL de 5QhJJcFZ… (06/07/2025). Le virement de `5QhJJc…` arrive 35 secondes avant qu'il ouvre un ordre DCA de vente sur tous ses jetons. Le créateur n'y encaisse presque rien : il déplace sa position (voir plus bas).

**La série de retraits (N01) :** Le 14/07/2024, de 01:32:23 à 01:40:50 UTC, 13 des 2 201 destinataires de 3 hot wallets Coinbase sur 2 h reversent ensuite à 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL, dont le créateur et 5QhJJc. Aucun des 2 188 autres. 13 sur 2 201, tous dans 507 s ; CV des écarts 0,245, P 5e-05 ; témoin même matin, 44 wallets dans 4 fenêtres : au plus 3 sur une même destination par virement pur, contre 10 avec la même troncature, 13 sur l'historique complet.

**Le compte de dépôt (N02, N03) :** 100 % des sorties vers 3 hot wallets et 6 adresses qui balaient 53 dépôts témoins sur 120 ; 59 balayages signés par 9W9b ; 155 000 lamports en frais principal, comme 105 témoins sur 120. 31 des 48 expéditeurs de 9W9b touchent DMAGA, contre 8 expéditeurs sur 1 365 dans 120 dépôts témoins. 31 sur 48 ; 16 sur 33 hors série et hors groupe ; témoin 8 sur 1 365, 7 dépôts, au plus 2 par dépôt. Un trésorier ou un opérateur pour plusieurs personnes reste possible. La rafale de 9 ne sépare 9W9b que sous le filtre choisi après coup : sans filtre, 4 témoins sur 120 atteignent 9 et le maximum vaut 18. Salves : 16:11:24 à 16:14:34, 190 s ; en réalité 15 wallets en 2 rafales le 26/01/2025. Chaque virement est signé par son expéditeur (`data_v2/collector.json`, tableau dans `reports/COORDINATION.md`).

**Le lien de 2025 (N04), A pour les transactions, B pour le lien :** BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc reçoit 6,576337507 SOL d'un hot wallet de la même famille, 61,6 h après un dépôt de 6,576437507 SOL sur 9W9b, puis 7,4 M de jetons du créateur. écart exact 100 000 lamports ; placebo en temps inversé 0 ; témoin : 0 sur 3 237 dépôts à cet écart, 0 sur 1 951 dépôts d'au moins 1 SOL aux multiples de 100 000 ; 70 retraits sur 2 517 valent un rond moins exactement 100 000 lamports, frais standard ; 5g7yNH balayé par 16 dépôts témoins.

**Aller-retour de position (C-10) :** 7 105 960 jetons vendus en 2 exécutions à 63 s d'écart, `3MjSKVjP5RERFSnQwzvA3m9haFF9JDR1MyW3rzFBNbyyXtbtkzfm2D1AUEcXT33x8gKfCbJb363AU2cQGWs8BinG`, `Ayr9HoxiKrMNqh8JXTJBn35Y7JzaorXWJW9dHD2AAHyNUfv8vyQzXXRtU1sy43zWKArFEC3oH7dRF5MRTov2RJT`, pour 4 598,77 USDC. Le 13/07, ordre d'achat de 4 500 USDC, `3eNyvVpP5LnZVuSDzmjQFrTmptmLhjKDJ3sf4SitjUGQQTMea6BLWQmUMJS3MHEdwtwLbNtMTxuFnTD4mp2iHPVj`, soit 7 397 559 jetons, transférés le jour même. Reste 98,77 USDC. `Hx1UvdgM…` est bien l'escrow DCA : compte créé avec le propriétaire `DCA265Vj…`, log `OpenDcaV2`. Le 13/07/2025, ces 7 397 559 jetons reçus de `Hx1UvdgMqZBQRrSAKhSSfc7Hvcb2Mk4dFrcrQpYG6urT`, escrow d'un ordre DCA, passent à `BuHUkjUy…`.

**Ce qui va contre un seul acteur dès le lancement :** un hot wallet sert tout le monde, une clé peut changer de main, et rien n'empêche un tiers d'envoyer vers une adresse.

## Relations documentées (`social_links.parquet`)
Types distincts : `mention_tierce` (un compte commente un wallet), `declaration_publique` (ce qu'un compte affirme), `interaction_sociale` (réponses et mentions). Aucune arête `wallet_revendique` : zéro.
Déclarations de l'équipe, toutes à prendre pour ce qu'elles sont : « $DMAGA pfp by me and @ChrisWinig », « a wartime PFP that we made for him » (@kikisknees) ; « DMAGA team created Elon's pfp specifically for him » (@DarkMagaCoin).

## Hypothèses non retenues
- **« Musk ou ses proches ont organisé »** : D. Aucun élément ne relie un wallet à Musk ou à son entourage. Il a adopté une image publique.
- **« Ansem, deBridge, la Solana Foundation »** (récit de Benjamin du 02/08) : D. Rien dans ces données. Non testé en profondeur : aucune adresse fournie.
