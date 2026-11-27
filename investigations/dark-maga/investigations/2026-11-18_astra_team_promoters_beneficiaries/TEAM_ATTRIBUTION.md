# TEAM_ATTRIBUTION — qui a créé et lancé $DMAGA ?

Addendum ASTRA, 2024-07-14, toutes heures en UTC. Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`.

Échelle de preuve :
- **A** : fait directement observable (tx, archive, post).
- **B** : convergence de plusieurs faits indépendants.
- **C** : déclaration ou indice isolé.
- **D** : hypothèse.

La colonne « origine » précise d'où vient le niveau :
- **RO** : rapport d'origine ou dépôt.
- **VI** : vérification indépendante de cet addendum.

> Aucune phrase de ce document n'attribue une identité civile. Les comptes X sont désignés par leur pseudonyme public. « Attribution non établie » veut dire qu'aucune preuve admise ne relie le compte au wallet. Cela n'innocente ni n'accuse personne.

## 1. Rôles retenus

| Compte | Rôle retenu | Niveau | Origine | Preuves pour | Preuves contre / limites |
|---|---|---|---|---|---|
| wallet `8YLEuU…` | **créateur technique** (signataire du create, achat dev 0,201 SOL / 7,106 M) | A | RO + VI (reçu figé `evidence/receipts/key/create_fePxr7ER.json`) | signature du create | opérateur humain inconnu |
| @DarkMagaCoin (DMC) | **communication officielle** ; premier à publier le CA (02:26:35, supprimé) | A (post) / B (même opérateur que le créateur) | RO (Wayback) + VI | voir le détail sous le tableau | image ré-encodée, donc pas une copie binaire ; un tiers rapide reste possible, mais improbable (0 abonné utile à 02:26) |
| @Murray_Gothbard (ex-@ChristienPhoto en juillet 2024) | **artiste / promoteur précoce** | A (posts) / C (rôle) | **VI (NOUVEAU)** | voir le détail sous le tableau | ne revendique ni création ni wallet ; aucun lien wallet |
| @kikisknees | **communication / artiste associé** ; relais du CA à 02:45:55 | A (RT) / C (rôle) | RO (Wayback) | RT du post « We are live » (archive) ; « pfp by me and @ChrisWinig » (C) | RT non retrouvé par l'API (Not Found) ; aucun wallet revendiqué ; recherche API 01:00–09:00 = 0 résultat |
| @ChrisWinig | **artiste** (pfp co-créé selon kiki) | B | RO | déclaration de kiki + mentions tierces | pas de post DMAGA du 14/07 avant 02:45 retrouvé |
| @CryptoOnlyCoims | **promoteur indépendant / sympathisant** (10e au classement, 02:48:08) | A (post) / C (rôle) | VI | vidéo $DMAGA en réponse à DMC ; slogan « Dark MAGA Has Begun » dès 00:41:12 (RT kiki) | pas de lien wallet |
| @kanpai | **admin communautaire / « lead » déclaré** | C | RO | déclaration « lead of the project » | déclaration seule, postérieure au lancement |
| @koreanjewcrypto | **promoteur indépendant** | C | RO | posts « 1000x » | pas de lien wallet ni de rôle déclaré |
| @Esoviz | **communication (après le lancement)** : DMC le nomme « media team lead » le 13/08 | C | RO ; VI : 0 post DMAGA trouvé de juin à août 2024 | déclaration de DMC | rien au lancement |
| @Aristos_Revenge | **sympathisant / non déterminé** | D | VI : compte **protégé** aujourd'hui (≈140 k abonnés), donc posts inaccessibles | — | l'absence de résultats vient de la protection du compte, pas de l'absence de posts |

Détail des preuves, lignes DMC et Murray :

**@DarkMagaCoin — preuves pour :**
- Le post « We are live Patriots! ca: 7D7B…pump » est archivé (Wayback). Son texte est corroboré par le RT archivé de kiki, `1812317575411351639`.
- La photo de profil DMC a été téléversée à **01:51:10** (snowflake de l'URL). C'est **la même image que le token** : distance pHash 0, mais pas identique au pixel (voir § 4).
- Le compte a été créé le 2024-06-11 et sa bio contient le CA.

**@Murray_Gothbard — preuves pour :**
- 02:31:29 : premier visuel « $DMAGA » de tiers connu. Le mot n'apparaît que dans l'image, ce qui explique que les recherches par mot-clé l'aient manqué.
- Ensuite 6 posts ou réponses $DMAGA la même nuit.
- Plus tard, il déclare « my friend developed the token » (C).

## 2. Opérateur du créateur et du cluster Coinbase/9W9b (NOUVEAU, B)

Entre **01:32:23 et 01:40:50**, donc 25 à 33 min avant le mint, les hot wallets Coinbase 2 et 3 envoient 11 retraits à **11 wallets qui enverront plus tard des SOL au même collecteur `9W9b3z…`**. Ce collecteur n'a que 48 expéditeurs sur toute sa vie, et 94,5 % de ses sorties partent vers Coinbase. Le créateur `8YLEuU…` fait partie de ces 11 wallets. Détail : `data/coinbase_to_9w9b_cluster.csv` ; contrôle : `tests/test_astra_offline.py::CoinbaseBatch`.

| UTC | Source | Wallet | SOL | 1re action DMAGA | Groupe 33 (repo) | Vers 9W9b (SOL, 1re date) | Réalisé DMAGA (repo) |
|---|---|---|---|---|---|---|---|
| 01:32:23 | CB3 | `8YLEuU…` créateur | 0,5 | create 02:05:25 | non | 0,593 (2025-01-26) | 0 |
| 01:33:05 | CB3 | `GoPCTr…` | 0,5 | échec 02:06:13, succès 02:06:53 | non | 0,97 (2025-05-28) | 0 |
| 01:33:30 | CB3 | `AFDkwJ…` | 0,5 | échec 02:07:24, achats Raydium 06:12–06:16 | non | 66,77 (2024-07-24) | 79,0 |
| 01:34:15 | CB3 | `EEpSRR…` | 0,5 | échecs 02:07:50 et 02:09:17, succès 02:09:29 | non | 8,02 (2024-09-22) | 25,2 |
| 01:35:40 | CB2 | `ERMtiL…` | 1,0 | 02:54:39 | non | 0,11 (2025-01-26) | 0 |
| 01:36:14 | CB2 | `HqwpWy…` | 1,0 | 02:36:47 | non | 0,28 (2025-01-26) | 0 |
| 01:37:49 | CB3 | `5s3ogz…` | 1,05 | 02:19:21 | non | 37,71 (2024-08-07) | 37,7 |
| 01:38:58 | CB3 | `7FGoCB…` | 1,05 | 02:17:56 | **oui** | 31,71 (2024-08-13) | 35,3 |
| 01:39:38 | CB3 | `Gmc1EG…` | 1,05 | échec 02:11:43, succès 02:12:02 | non | 40,77 (2024-08-13) | 8,9 |
| 01:40:13 | CB2 | `4pKFTQ…` | 1,05 | échec 02:10:44, succès 02:10:56 | non | 0,10 (2025-01-26) | 7,7 |
| 01:40:50 | CB2 | `5QhJJc…` | 1,05 | échec 02:10:02, succès 02:10:11 | **oui** | 0,13 (2025-01-26) | 74,2 |

Taux de base, pour tous les retraits CB2/CB3 de 01:20:00 au mint : 607 transferts vers 573 destinataires.

| Montant | Retraits | Vers des expéditeurs futurs de 9W9b |
|---|---|---|
| 1,05 SOL exactement | 5 | **les 5** |
| 0,5 SOL exactement | 7 | 4 |
| 1,0 SOL | 12 | 2 |

Le 2025-01-26, le créateur, `ERMtiL…`, `HqwpWy…`, `4pKFTQ…` et `5QhJJc…` font leur premier envoi vers 9W9b le même jour. Le dépôt avait déjà noté une salve ce jour-là.

**Interprétation, par ordre de parcimonie :**
1. Un même opérateur, ou un petit groupe partageant un compte Coinbase, prépare au moins 11 wallets frais avant le mint. Il les utilise pour acheter dans les 48 s à 50 min suivant le create, puis consolide vers une même adresse de type dépôt.
2. Plusieurs personnes distinctes coordonnées par un tiers (« équipe »).
3. Coïncidence. Elle est jugée très improbable, à cause de l'alignement simultané des montants ronds, de la fenêtre de 8,5 min et du collecteur rare.

**Niveau :**
- **A** pour les transferts.
- **B** pour « cluster coordonné lié au wallet créateur ».
- **C** pour « opérateur unique ».
- **Identité de l'opérateur : non établie.**

Coinbase seul n'est pas un lien (règle AGENTS.md). Le lien repose sur la conjonction de quatre éléments : montants et minutage, wallets frais, même token visé, même collecteur rare.

Ce cluster **fait le pont** entre le créateur et deux membres du groupe 33 (`7FGoCB…`, `5QhJJc…`). Cette jonction est nouvelle par rapport au dépôt, qui classait GoPCTr, AFDkwJ et EEpSRR en `groupe:false, createur:false`.

## 3. G41v et le groupe 33 (rappel et compléments)

- G41v (`G41vRr…`) finance avant le mint 13 wallets à 0,5 SOL (RO). 8 d'entre eux n'achètent jamais ; les autres achètent 0,49 SOL entre 02:12 et 02:22.
- Ses deux achats ratés sont décodés (VI, A) :
  - +29 s (slot +67) : limite 0,51005 SOL ;
  - +45 s (slot +100) : limite 0,40804 SOL ;
  - erreur 6002 `TooMuchSolRequired` dans les deux cas.
  - 0,5 et 0,4 SOL × 1,01 × 1,01 donnent exactement ces limites : saisie manuelle dans l'UI pump.fun (frais 1 % + slippage 1 %). C'est **compatible avec un humain qui surveille le flux**, pas avec un bot sniper (médiane des premiers acheteurs : 2 s ; cf. `FIRST_BUYERS.md`).
- Trésor de guerre de G41v : vente de son propre token `9MBzpy…` le 13/07 à 15:55:26 (+22,32 SOL, reçu figé).
- Lien G41v ↔ cluster Coinbase/9W9b : G41v envoie lui aussi 8 SOL à 9W9b (RO). Il n'apparaît **pas** dans les retraits Coinbase de 01:20–02:05. Niveau **C** pour « même opérateur que le créateur ».

## 4. Corrections apportées au rapport précédent

1. **Image du token et pfp DMC.** Elles ne sont **pas identiques au pixel près**. Distance pHash, dHash et aHash : 0, mais seulement 20,4 % de pixels identiques (écart moyen 1,88/255, maximum 81). Il s'agit de la même image ré-encodée : X recompresse les fichiers téléversés. La conclusion « même image » tient (B) ; la formulation « identique au pixel » est retirée.
2. **Heure de la pfp.** Le `Last-Modified` de pbs.twimg.com vaut systématiquement snowflake − 120 s, vérifié sur 3 cas. C'est un artefact du CDN. L'heure à retenir pour la pfp DMC est **01:51:10** (snowflake), pas 01:49:10.
3. **Premier visuel tiers.** C'est @Murray_Gothbard à **02:31:29**, avant @adamjia7 (02:33:53). Il ne s'agit pas de son post de 02:41:55 retenu par la passe 4.
