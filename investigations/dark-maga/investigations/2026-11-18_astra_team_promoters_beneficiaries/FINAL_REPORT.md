# FINAL_REPORT — réponses aux 8 questions (ASTRA, toutes heures UTC)

## 1. Qui a créé DMAGA ?

**Wallet**
- `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` (A). Il signe le create `fePxr7…` à 02:05:25 et fait l'achat dev de 0,201 SOL / 7,106 M.
- Il est financé par Coinbase 3 (0,5 SOL à 01:32:23) dans un lot de 11 retraits synchronisés vers des wallets qui consolident plus tard vers `9W9b3z…`. Niveau B pour le cluster coordonné, C pour un opérateur unique.

**Opérateur public**
- @DarkMagaCoin est relié au créateur au **niveau B** : sa pfp, téléversée à 01:51:10, est la même image que le token (ré-encodée, pHash 0), et il est le premier à publier le CA, à 02:26:35.
- Ce n'est pas une preuve de contrôle du wallet.

**Identité publique vérifiée : aucune.** La seule déclaration est celle de @Murray_Gothbard, « my friend developed the token » (C, sans nom).

## 2. Qui dirigeait le projet au lancement ?

| Compte | Rôle | Niveau | Fondement |
|---|---|---|---|
| @DarkMagaCoin | canal officiel | A | annonce du CA à 02:26:35, vidéo à 03:00:28 |
| @kikisknees | communication / artiste associé | B/C | RT du CA à 02:45:55 ; « pfp by me and @ChrisWinig » |
| @ChrisWinig | artiste | B | selon la déclaration de kiki |
| @Murray_Gothbard | artiste / promoteur précoce | rôle C | premier visuel à 02:31:29 |
| @kanpai | « lead » déclaré | C | déclaration postérieure au lancement |
| @Esoviz | « media team lead » | C | désigné par DMC le 13/08 ; aucune trace au lancement |

**Direction au lancement : non démontrée au-delà du canal DMC.**

## 3. Les dix premiers promoteurs

| # | Heure | Compte | Contenu |
|---|---|---|---|
| 1 | 02:26:35 | @DarkMagaCoin | « We are live Patriots! ca: 7D7B…pump » (supprimé ; Wayback + RT archivé) |
| 2 | 02:31:29 | @Murray_Gothbard (ex-@ChristienPhoto) | image « $DMAGA », post `1812313940841341353` |
| 3 | 02:33:53 | @adamjia7 | bot, CA |
| 4 | 02:44:08 | @Official67Token | RT de Murray |
| 5 | 02:45:49 | @SpecialBea99061 | RT + « $DMAGA » |
| 6 | 02:45:55 | @kikisknees | RT de DMC (Wayback) |
| 7 | 02:46:00 | @BoredNap66757 | RT |
| 8 | 02:46:16 | @Jacwin_n | RT |
| 9 | 02:46:33 | @eseleo | « @DarkMagaCoin $DMAGA💯 » |
| 10 | 02:48:08 | @CryptoOnlyCoims | vidéo « $DMAGA Time » |

Sources : X IDs et snowflakes dans `data/earliest_promoters.csv`. Niveau A pour chaque post.

Aucun post indexé avec le ticker ou le CA entre le 2024-07-13 00:00 et le 2024-07-14 02:20.

## 4. Les vingt premiers acheteurs

Détail complet (heures, Δslot, SOL, M, financement) : `FIRST_BUYERS.md` § 3.

- **0. Créateur** : 0,201 SOL.
- **1–10** :

| # | Wallet | Heure | SOL |
|---|---|---|---|
| 1 | EYykLf | 02:05:25 | 0,15 |
| 2 | Edq7kG | 02:05:28 | 0,19 |
| 3 | E1mh1W | 02:05:39 | 1,0 |
| 4 | Dj2a99 | 02:05:43 | 0,098 |
| 5 | BNHsrn | 02:05:46 | 1,96 |
| 6 | 8D2AGA | 02:05:50 | 0,214 |
| 7 | GySdM4 | 02:05:51 | 0,0001 (Coinbase 2) |
| 8 | DrKPLz | 02:05:54 | 2,02 |
| 9 | BE5S5w | 02:05:54 | 1,88 |
| 10 | gYVsQ5 | 02:05:56 | 1,14 |

- **11–20** :

| # | Wallet | Heure | SOL | Note |
|---|---|---|---|---|
| 11 | Hcnutb | 02:05:57 | 0,42 | |
| 12 | GS7aGE | 02:06:04 | 0,98 | |
| 13 | 6t2dz4 | 02:06:07 | 1,05 | groupe 33 |
| 14 | GZVLzg | 02:06:15 | 0,50 | |
| 15 | 2W83fC | 02:06:21 | 0,008 | |
| 16 | D9iUhx | 02:06:24 | 0,10 | |
| 17 | Ei1uVf | 02:06:26 | 0,98 | |
| 18 | 8YrEVP | 02:06:26 | 1,00 | groupe 33 |
| 19 | H4bVhV | 02:06:29 | 0,21 | |
| 20 | Hk74Yp | 02:06:38 | 0,50 | Coinbase 2, 0,689 SOL à 02:02:43 |

- **Ensuite** : GoPCTr à 02:06:53 (0,40 SOL, cluster CB/9W9b, tentative dès 02:06:13).
- Dans les 60 s : **17 acheteurs / 11,916 SOL ; 50 échecs**.

## 5. Quels promoteurs ont réellement gagné ?

**Aucun démontré : attribution non établie pour tous les comptes.**
- Aucune adresse revendiquée, aucune signature, aucune tx liée à une déclaration.
- « 1000x » (@koreanjewcrypto) et les mentions tierces de wallets (H3Qs, GXZvX, 5QhJJc) restent au niveau C.

## 6. Plus grands bénéficiaires

Profit réalisé, coût moyen, méthode du dépôt.

| Rang | Wallet | Réalisé SOL | Note |
|---|---|---|---|
| 1 | `H3QsBr…` | 5 490,9 | sortie vers un service non nommé et `8YSi5y…` |
| 2 | `GXZvXs…` | 2 540,1 | sortie vers `Co3zTr…` |
| 3 | FTKTNF | 2 046 | entré après Musk |
| 4 | `9PrmF8…` | 1 747,8 | sortie vers Coinbase 3/1/2 |
| 5 | F1DRDB | 1 709,5 | |
| 6 | 6Lomz4 | 1 466,6 | |
| 7 | CEzjbQ | 1 323 | |

Agrégats :
- Groupe 33 : 5 594 SOL au total.
- Cluster créateur CB/9W9b : 268 SOL.

**Aucune identité publique vérifiée. Aucun lien entre les grands bénéficiaires et l'équipe.**

## 7. L'équipe a-t-elle acheté avant la promotion publique ?

**Pour :**
- Le créateur fait l'achat dev à 02:05:25 (A).
- 7 autres wallets du cluster CB/9W9b, financés 25 à 33 min avant le mint, achètent entre 02:06:53 et 02:19:21. C'est **avant** le premier post DMC (02:26:35) : 5,9 SOL au total, avec le créateur, pour 33,25 M (≈ 3,3 % de l'offre).
- Les wallets G41v et groupe 33 financés avant le mint achètent entre 02:06 et 02:22.

**Contre :**
- Le token est public sur pump.fun dès le create : 182 signataires en 10 min, et des bots à 0 s.
- Les montants sont faibles (0,4–1 SOL par wallet).
- **Aucun de ces wallets n'est relié à un compte de l'équipe par une preuve admise.**
- Le lien au créateur est de niveau B (comportemental et CEX + collecteur), pas A.

**Verdict :**
- **Des wallets liés au créateur (B) ont acheté avant la promotion X (A pour les horodatages).**
- **Qu'il s'agisse de « membres de l'équipe » identifiés : non démontré.**
- Aucun jugement juridique.

## 8. Inconnues et preuves décisives

Voir `UNRESOLVED_IDENTITIES.md` (U1–U13). Les plus décisives :
- **U1 :** un message signé par `8YLEuU…`, publié par DMC.
- **U2 :** la revendication publique d'une adresse du cluster CB/9W9b.
- **U3 :** un transfert direct entre G41v et le cluster.
- **U7 :** les archives Wayback de kiki et Winig pour 01:00–02:45.
- **U11 :** une recherche TinEye ou Lens faite par un humain.

## Bilan

| Catégorie | Résultat |
|---|---|
| Identités civiles confirmées | **0** |
| Rôles confirmés | DMC = canal officiel (A) ; Murray = premier visuel tiers (A pour les posts) ; kiki = relais du CA (A) ; Winig = artiste (B) |
| Wallets attribués à un compte | **0**. Le créateur n'est relié à DMC qu'au niveau B. |
| Bénéficiaires liés à la promotion | **0** |
| Liens on-chain nouveaux | cluster CB/9W9b de 11 wallets incluant le créateur et 2 membres du groupe 33 (B) |

Prochaines vérifications :
1. Arêtes directes G41v ↔ cluster et cluster ↔ groupe 33 hors services (tous historiques).
2. Créateur de KLLARY ↔ créateur DMAGA.
3. Wayback ciblé kiki / Winig / Aristos de juillet 2024.
4. Recherche TinEye ou Lens par un humain.
5. Recherche d'adresses revendiquées dans les posts de 2024–2025 des comptes de l'équipe.
