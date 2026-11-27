# Couverture X — DMAGA, passe 2

Collecte rétrospective unique, 6 novembre 2026, Europe/Lisbon. Aucun post, brouillon, like, repost, abonnement, DM, PR, ticket, modification GitHub ou routine créé. Les prompts importés qui proposent des corrections et une PR sont des documents de passation, pas des actions exécutées.

## Comptage vérifiable

- **89 appels X** : 81 recherches plein-archive, 8 lectures groupées d’ID. Les appels de découverte des outils, lectures GitHub, un GET Wayback et GET de médias publics ne sont pas comptés comme appels X.
- **1001 publications distinctes dans le JSONL**, dont 899 vues comme objets de premier niveau et 102 seulement comme originaux/citations développés. Toutes les lignes comptées ont un ID, une date UTC, un author_id et un handle récupérés ; aucun champ d’auteur n’est deviné.
- 1129 objets-ID au total dans les réponses, dont 128 références incomplètes non comptées comme publications archivées. Ces dernières restent dans les réponses brutes sur la box ; leurs IDs sont listés plus bas.
- 1000 objets de premier niveau selon la somme des result_count, avec doublons entre pages/requêtes/lectures. Ce n’est pas le nombre de sources indépendantes.
- 616 lignes ont au moins un tag de périmètre (DMAGA, comparateur, fil prioritaire ou candidat avatar) ; 385 sont contexte ou faux positif de recherche. Le JSONL les étiquette, il ne les transforme pas en preuves.
- 35 ID de l’archive figuraient dans les 5 155 posts du corpus chargé lors de la passe 1. Les autres IDs ne sont pas pour autant de nouveaux faits ou absents de tous les dossiers/branches.
- 29 requêtes distinctes ; **28 atteignent une réponse finale sans next_token**. Épuisement des pages de cette requête ≠ exhaustivité de X.
- Quinze résultats supplémentaires retenus dans le rapport, mais plusieurs partagent le même auteur ou relisent un média déjà connu : aucune équivalence entre 15 résultats et 15 témoins indépendants.

## Protocole et champs

Recherches `x.search_posts_all`, max_results=25, sort_order=recency ; continuation par le next_token exact en conservant requête et fenêtre. Opérateurs effectivement utilisés : from:, to:, conversation_id:, url:, OR, lang:, -is:retweet, since:/until:. Les champs sollicités couvrent dates, auteurs, langue, conversation, références, textes longs, entités et pièces jointes ; expansions author_id, referenced_tweets.id et attachments.media_keys. Certains appels de lecture demandent aussi variantes vidéo, public_metrics et edit_history ; ils ne constituent pas un audit complet des éditions.

Les limites ~30/min et 1 000/jour sont celles du brief, pas des quotas interrogés ni garantis par cette session. Aucun 429 n’a été observé ; aucun débit ou quota restant n’a été inféré de headers non disponibles.

### Angle mort démontré de conversation_id

`conversation_id:1815291249102119198` et `conversation_id:1815372294426124565` retournent zéro. Pourtant les lectures directes montrent des réponses authentifiées avec ces mêmes conversation_id : 1815291795787690478, 1815293200095138249, 1815492336123858975 ; côté Noah, 1815375121294725503 et les réponses visibles. La passe 1 avait donc manqué des commentaires réellement accessibles.

Récupération complémentaire par from:/to: sans filtre de vocabulaire, requêtes sur URLs, adresses exactes et lecture des referenced_tweets. Les pages de Q20/Q21 sont épuisées dans leur fenêtre, mais les réponses sans mention, comptes privés, posts supprimés et citations non indexées peuvent encore manquer. Le défaut conversation_id n’est pas attribué sans preuve à une cause technique précise.

### Citations, reposts, textes longs

Les citations sont suivies via URL et referenced_tweets puis hydratées par ID. Aucun endpoint spécialisé listant toutes les citations n’était exposé dans le catalogue interrogé ; aucun total exhaustif de quotes n’est revendiqué. Les reposts dupliquant Jeffro sont conservés mais ne sont pas considérés comme analyses indépendantes. Les variantes brutes sont sauvegardées par post pour éviter de fusionner un auteur original et un auteur de reprise.

Un texte long complet est préféré aux extraits de recherche lorsqu’il est disponible. `text_may_be_truncated` est un indicateur prudent, non un diagnostic certain : les variantes brutes permettent de vérifier. `is_original` signifie « non identifié comme repost », pas « message racine » ; consulter aussi post_type, conversation_id et les références. Une absence de référence dans un objet de recherche à hydratation partielle ne démontre pas une racine autonome. Pour N06, l’objet direct et son conversation_id propre ont été contrôlés.

## Référentiel consulté

Dépôt demandé uniquement, sans clone ni écriture : listing de docs/historical/, mémo complet, X_SOURCE_MANIFEST.json, RESEARCH_HANDOFF.md, PROMPT_CLAUDE_CODE.md, PROMPT_GROK_BOT.md, puis SOCIAL_FINDINGS.md et TIMELINE.md. Le mémo complet importé contient exactement le rapport local précédent (comparaison intégrale). Les documents des autres dossiers déjà étudiés en passe 1 ne sont pas réputés réaudités dans leur intégralité en passe 2.

L’absence d’un ID dans le corpus local initial est un contrôle de nouveauté documentaire, pas une recherche exhaustive de tous les reçus GitHub. Les mints identifiés socialement ne sont pas des wallets de personnes.

## Périmètres et requêtes exactes

### Q01 — épuisée au niveau API (sans next_token)

`conversation_id:1815291249102119198`

Pages : 1 ; result_count par page : [0].

### Q02 — épuisée au niveau API (sans next_token)

`conversation_id:1815372294426124565`

Pages : 1 ; result_count par page : [0].

### Q03 — épuisée au niveau API (sans next_token)

`from:JeffroBTC (DMAGA OR KLLARY OR 7GVC OR 9Sxm) since:2024-06-01 until:2024-11-01`

Pages : 2 ; result_count par page : [1, 0].

### Q04 — épuisée au niveau API (sans next_token)

`from:Noah_nftn (DMAGA OR DarkMaga OR 7GVC OR 9Sxm OR 5QhJJc) since:2024-06-01 until:2024-11-01`

Pages : 2 ; result_count par page : [1, 0].

### Q05 — épuisée au niveau API (sans next_token)

`(7GVC OR 9Sxm OR "190 SOL" OR "190SOL") (DMAGA OR KLLARY OR JeffroBTC) since:2024-06-01 until:2024-11-01`

Pages : 2 ; result_count par page : [18, 0].

### Q06 — épuisée au niveau API (sans next_token)

`(DMAGA OR DarkMagaCoin) (KLLARY OR RETIREDI0 OR RETARDIO OR JOE OR ZOOMER) since:2024-07-13 until:2024-07-27 -is:retweet`

Pages : 4 ; result_count par page : [24, 21, 14, 0].

### Q07 — épuisée au niveau API (sans next_token)

`(url:1815291249102119198 OR url:1815372294426124565 OR to:JeffroBTC OR to:Noah_nftn) (DMAGA OR KLLARY OR wallet OR 钱包 OR 地址) since:2024-07-13 until:2024-11-01`

Pages : 3 ; result_count par page : [19, 8, 0].

### Q08 — épuisée au niveau API (sans next_token)

`(DMAGA OR "dark maga") (insider OR sniper OR wallet OR bundle OR "early buyers") since:2024-07-13 until:2024-07-27 -is:retweet`

Pages : 5 ; result_count par page : [24, 24, 22, 20, 0].

### Q09 — épuisée au niveau API (sans next_token)

`(DMAGA OR DarkMagaCoin) (钱包 OR 内幕 OR 老鼠仓 OR 狙击 OR 资金 OR 地址) since:2024-07-13 until:2024-07-27 -is:retweet`

Pages : 4 ; result_count par page : [7, 13, 16, 0].

### Q10 — épuisée au niveau API (sans next_token)

`(DMAGA OR DarkMagaCoin) (from:sonder_crypto OR from:0xEnsp1re OR from:kkashi_yt OR from:_deltaPG OR from:OnlyDeFiGuy) since:2024-07-13 until:2024-11-01`

Pages : 4 ; result_count par page : [25, 25, 15, 0].

### Q11 — épuisée au niveau API (sans next_token)

`from:JeffroBTC since:2024-07-21 until:2024-07-24`

Pages : 2 ; result_count par page : [10, 0].

### Q12 — épuisée au niveau API (sans next_token)

`from:Noah_nftn since:2024-07-21 until:2024-07-24`

Pages : 2 ; result_count par page : [6, 0].

### Q13 — épuisée au niveau API (sans next_token)

`(elon OR musk OR DMAGA) (pfp OR avatar OR profile OR laser) -is:retweet`

Pages : 3 ; result_count par page : [21, 11, 0].
Fenêtre explicite : start_time=2024-07-21T19:00:00Z ; end_time=2024-07-21T19:27:24Z (20:00:00–20:27:24 Lisbonne).

### Q14 — épuisée au niveau API (sans next_token)

`KLLARY (CA OR contract OR 合约 OR 地址 OR pump OR solscan) since:2024-07-01 until:2024-07-27 -is:retweet`

Pages : 2 ; result_count par page : [5, 0].

### Q15 — épuisée au niveau API (sans next_token)

`from:dissident42069 (RETIREDI0 OR RETARDI0 OR RETARDIO) since:2024-07-13 until:2024-07-23`

Pages : 2 ; result_count par page : [17, 0].

### Q16 — épuisée au niveau API (sans next_token)

`(DMAGA OR "dark maga") lang:ko since:2024-06-01 until:2024-11-01 -is:retweet`

Pages : 2 ; result_count par page : [15, 0].

### Q17 — épuisée au niveau API (sans next_token)

`(DMAGA OR "dark maga") lang:es since:2024-07-13 until:2024-07-27 -is:retweet`

Pages : 3 ; result_count par page : [22, 19, 0].

### Q18 — épuisée au niveau API (sans next_token)

`(DMAGA OR "dark maga") lang:fr since:2024-07-13 until:2024-07-27 -is:retweet`

Pages : 4 ; result_count par page : [22, 18, 3, 0].

### Q19 — épuisée au niveau API (sans next_token)

`(DMAGA OR "dark maga") lang:pt since:2024-07-13 until:2024-07-27 -is:retweet`

Pages : 2 ; result_count par page : [15, 0].

### Q20 — épuisée au niveau API (sans next_token)

`(from:JeffroBTC OR to:JeffroBTC) since:2024-07-22 until:2024-07-24`

Pages : 3 ; result_count par page : [20, 7, 0].

### Q21 — épuisée au niveau API (sans next_token)

`(from:Noah_nftn OR to:Noah_nftn) since:2024-07-22 until:2024-07-24`

Pages : 2 ; result_count par page : [9, 0].

### Q22 — épuisée au niveau API (sans next_token)

`from:DarkMagaCoin (DMed OR DM OR "sent him" OR "team member" OR spoke OR contact) since:2024-07-13 until:2024-11-01 -is:retweet`

Pages : 2 ; result_count par page : [5, 0].

### Q23 — PARTIELLE : next_token subsiste ; requête trop large mêlant sport/homonymes, abandonnée au profit de Q25/Q26

`(BARRON OR Barronsolana) (from:sonder_crypto OR from:DarkMagaCoin OR CA OR contract) since:2024-05-01 until:2024-07-24 -is:retweet`

Pages : 1 ; result_count par page : [24].

### Q24 — épuisée au niveau API (sans next_token)

`(DMAGA OR DarkMagaCoin) (HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv OR Hasten0x OR ClayBro883 OR RjL5pLQXzCjMHtT6nBSc9xiCsp2VJR1VWPjfudHrkSZ) since:2024-07-13 until:2024-11-01 -is:retweet`

Pages : 2 ; result_count par page : [9, 0].

### Q25 — épuisée au niveau API (sans next_token)

`(from:sonder_crypto OR from:DarkMagaCoin OR from:Barronsolana) (BARRON OR contract OR CA) since:2024-05-01 until:2024-07-24 -is:retweet`

Pages : 13 ; result_count par page : [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 0].
Extension ponctuelle à mai pour dater le contrat BARRON, antérieure au périmètre principal. Les résultats antérieurs à juillet ne prouvent pas que DMAGA existait déjà.

### Q26 — épuisée au niveau API (sans next_token)

`from:Barronsolana (CA OR contract OR pump OR dexscreener) since:2024-05-01 until:2024-07-27 -is:retweet`

Pages : 2 ; result_count par page : [10, 0].

### Q27 — épuisée au niveau API (sans next_token)

`(7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j OR 9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS OR A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J OR 6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD OR H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y) since:2024-06-01 until:2024-11-01 -is:retweet`

Pages : 2 ; result_count par page : [6, 0].

### Q28 — épuisée au niveau API (sans next_token)

`(EaoxyxgjUZvksR57aNy2jHWno3DCBNQU4dd4BWhgk66w OR APfA9dgxbnLGw4gexrJNDMU7XdS1juHP4fbATDi84sK OR AeiMit5PMUvdJSsa8jm2RpHJCdfJLFyW6dzkm65w1ybh OR "6.73%" OR "20.39%") (DMAGA OR Dmaga OR Noah_nftn) since:2024-06-01 until:2024-11-01 -is:retweet`

Pages : 2 ; result_count par page : [1, 0].

### Q29 — épuisée au niveau API (sans next_token)

`(H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc OR H3QsBr) (JOE OR ZOOMER) since:2024-06-01 until:2024-11-01 -is:retweet`

Pages : 2 ; result_count par page : [16, 0].

## Journal page par page : curseurs et preuves brutes

Répertoire commun des réponses JSON reformatées : `/workspace/dmaga_pass2_work/raw/`. Le JSONL embarque les objets et leurs variantes/provenances ; ce répertoire supplémentaire et les binaires de médias restent sur la box et **ne sont pas inclus** dans le ZIP des cinq livrables. Les hashes ci-dessous portent sur les fichiers JSON reformatés, non sur des octets HTTP originaux. Dans le JSONL, raw_sha256 au niveau post porte sur l’objet canonisé ; les hashes de réponse figurent dans provenance.

| Appel | Résultats | Curseur entrant | Curseur sortant | Fichier brut / SHA-256 |
|---|---:|---|---|---|
| L01.1 | 4 | `—` | `—` | `L01_1.json` / `1d880d2cb86b4db3f953d375e91a20d2d4d059be90a84ad39a0c2caa7d01b3e4` |
| Q01.1 | 0 | `—` | `—` | `Q01_1.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q02.1 | 0 | `—` | `—` | `Q02_1.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q03.1 | 1 | `—` | `b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod` | `Q03_1.json` / `72ffd81e4578934b29db497c617eeed98e18d8970ef93dc00b76bd20a02e3c79` |
| Q04.1 | 1 | `—` | `b26v89c19zqg8o3frqou3uaf3jm5651ase8vg5b8y12f1` | `Q04_1.json` / `24278c861346ad97f9734ca4fd67f0e50f2ca6b8c573029f9949fbafdf820760` |
| Q05.1 | 18 | `—` | `b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod` | `Q05_1.json` / `593f5cb3c4c7352a7beaaf466e56847cf6cb4f9991f987363b7c9bac353977ae` |
| Q06.1 | 24 | `—` | `b26v89c19zqg8o3frqou40olu6hrgtdqiva7l9th7w3gd` | `Q06_1.json` / `a036740b6f9ded5cfe29ba66566e3c61cfa1c8ebafe89144432d516eed859e11` |
| Q03.2 | 0 | `b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod` | `—` | `Q03_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q04.2 | 0 | `b26v89c19zqg8o3frqou3uaf3jm5651ase8vg5b8y12f1` | `—` | `Q04_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q05.2 | 0 | `b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod` | `—` | `Q05_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q06.2 | 21 | `b26v89c19zqg8o3frqou40olu6hrgtdqiva7l9th7w3gd` | `b26v89c19zqg8o3frqou3s5zy84yduar423kh8mgdpvnh` | `Q06_2.json` / `0ae4ff9702913c07e6f7d211e69870fdacab15ec7f21638cc92deae645d6d8ae` |
| Q07.1 | 19 | `—` | `b26v89c19zqg8o3frqouy5ilumuk3f9g89kb5ighkeef1` | `Q07_1.json` / `24a8b3ca4d578a4b4e391fc717d714ba1ffee47546354f943fb47ea31d98b5ba` |
| Q08.1 | 24 | `—` | `b26v89c19zqg8o3frqou473divi6y2ja0ftsbj8grnipp` | `Q08_1.json` / `387a4b56c99480f97bf8f5e665c06003af7efe52f1303ec3e9d3e5c328c96930` |
| Q09.1 | 7 | `—` | `b26v89c19zqg8o3frqou42sqeo4p88dxsi2esly271myl` | `Q09_1.json` / `78f7c75fdfbc850168916f5695c8ec81434ecc8532c740a969cae09b97026b87` |
| Q06.3 | 14 | `b26v89c19zqg8o3frqou3s5zy84yduar423kh8mgdpvnh` | `b26v89c19zqg8o3frqot9phb78kmfogcs7ko2b0ugiid9` | `Q06_3.json` / `c796a77ee90fda44d54617e436357f595ca97e565a0d6332f1c236b28d8e4df6` |
| Q07.2 | 8 | `b26v89c19zqg8o3frqouy5ilumuk3f9g89kb5ighkeef1` | `b26v89c19zqg8o3frqot9eqzlvmlh0gposr9690eomcn1` | `Q07_2.json` / `297186a350b7d647dabcb116a307dcd0402b66d3c3be01920e488bfb933a7824` |
| Q08.2 | 24 | `b26v89c19zqg8o3frqou473divi6y2ja0ftsbj8grnipp` | `b26v89c19zqg8o3frqou40n3t0sqmb38d9yy6n9z702v1` | `Q08_2.json` / `95b2b40d71758e6aa47e45df14626852a6431783c0f98f4332692c033a9d17a8` |
| Q09.2 | 13 | `b26v89c19zqg8o3frqou42sqeo4p88dxsi2esly271myl` | `b26v89c19zqg8o3frqou3s6as6rtcuyhpnrzh2aosbdkt` | `Q09_2.json` / `8fdbfdadf55ea6b899aec41c8ef40a7997d488fe746bfd8f4f0a6af5656e4864` |
| Q10.1 | 25 | `—` | `b26v89c19zqg8o3frqou42t173af9c9dz8jamhs3fm9a5` | `Q10_1.json` / `4e7fb2a057085db74a32e21d131e21a85f99d0004f47f7057624e83a3e18f9a3` |
| L02.1 | 7 | `—` | `—` | `L02_1.json` / `517a31f69c479c82e218ebc51a7068f405427279503f035c4e8935b3f544cb13` |
| Q06.4 | 0 | `b26v89c19zqg8o3frqot9phb78kmfogcs7ko2b0ugiid9` | `—` | `Q06_4.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q07.3 | 0 | `b26v89c19zqg8o3frqot9eqzlvmlh0gposr9690eomcn1` | `—` | `Q07_3.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q08.3 | 22 | `b26v89c19zqg8o3frqou40n3t0sqmb38d9yy6n9z702v1` | `b26v89c19zqg8o3frqou3u97xtolbvttxlsd8ki1jdcot` | `Q08_3.json` / `580156a2c66849f332b6066246d8a808cb6a8fd197f4b3d5d6d50f0198a350cb` |
| Q09.3 | 16 | `b26v89c19zqg8o3frqou3s6as6rtcuyhpnrzh2aosbdkt` | `b26v89c19zqg8o3frqou3q0d516rfh4cdgo3gb3pnccjh` | `Q09_3.json` / `c6bb43b65f7d585cebbcda182d4b8a8e9157b595b94a28742e5b4f29dd2b5cf0` |
| Q10.2 | 25 | `b26v89c19zqg8o3frqou42t173af9c9dz8jamhs3fm9a5` | `b26v89c19zqg8o3frqou3wdy05oidqib5kw8e14mxyxdp` | `Q10_2.json` / `5353faf939234e4783b59a2358b0cec3b8ef9d8ae993fc80e411b668f9a1ac79` |
| Q11.1 | 10 | `—` | `b26v89c19zqg8o3frqotozalvzapv95l7zmt95f4hqcn1` | `Q11_1.json` / `1d30b2972fa1a898e3b9c0ddd5c694817b57613cddfce31c87ddf75a2816f1c2` |
| Q12.1 | 6 | `—` | `b26v89c19zqg8o3frqou3s5p7cvshfdird86auhk2g96l` | `Q12_1.json` / `628cd89e679580a7a8fe900ba74348d753bd9b86ee2684e9aaff366485e00105` |
| Q13.1 | 21 | `—` | `b26v89c19zqg8o3frqou3pyvegsfc2cqddeqseikqg0ot` | `Q13_1.json` / `71c2b0c2140731c6af2e0dfe45e1914125ba3a3ae2fdb5ef154ed60e7950fd5c` |
| Q13.2 | 11 | `b26v89c19zqg8o3frqou3pyvegsfc2cqddeqseikqg0ot` | `b26v89c19zqg8o3frqou3pyv6voc3gi7cshq9i42dnurh` | `Q13_2.json` / `f0dca82560ef683e53ef92c1fa701a104261d104f558daeb69050fe67c36a40f` |
| Q11.2 | 0 | `b26v89c19zqg8o3frqotozalvzapv95l7zmt95f4hqcn1` | `—` | `Q11_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q12.2 | 0 | `b26v89c19zqg8o3frqou3s5p7cvshfdird86auhk2g96l` | `—` | `Q12_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q09.4 | 0 | `b26v89c19zqg8o3frqou3q0d516rfh4cdgo3gb3pnccjh` | `—` | `Q09_4.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q08.4 | 20 | `b26v89c19zqg8o3frqou3u97xtolbvttxlsd8ki1jdcot` | `b26v89c19zqg8o3frqotoi93vfno2j6ednyb1va3ddojh` | `Q08_4.json` / `c6c690ecc65ea45128b57b5d543a5a8850de1aa7785f189fbfce4a1bfcd59f6d` |
| L03.1 | 7 | `—` | `—` | `L03_1.json` / `69070a44a02be5b1e9bddd903db2070353caea9a0fdbea303c0ea8bda51f54ce` |
| Q14.1 | 5 | `—` | `b26v89c19zqg8o3frqlv6fvw0v4r1w0332qmi7fu03919` | `Q14_1.json` / `190d38467c5456abeb0fff0bdb79ee62a0d62f478b7469dff543845c693e9c6b` |
| Q15.1 | 17 | `—` | `b26v89c19zqg8o3frqosfkliep4l6i62nt06hip7cqvel` | `Q15_1.json` / `988bd8df7afd0b6c85cfce925de2612e334d9cc2d484a0d89d086a5feb197bff` |
| Q13.3 | 0 | `b26v89c19zqg8o3frqou3pyv6voc3gi7cshq9i42dnurh` | `—` | `Q13_3.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q08.5 | 0 | `b26v89c19zqg8o3frqotoi93vfno2j6ednyb1va3ddojh` | `—` | `Q08_5.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q10.3 | 15 | `b26v89c19zqg8o3frqou3wdy05oidqib5kw8e14mxyxdp` | `b26v89c19zqg8o3frqou3s3wgrrz8wmealixrp9fihit9` | `Q10_3.json` / `225c4cb325f7e6b407cf30b84f370b20e38633ab3d4a10a5cac912e9f94fe9bb` |
| Q14.2 | 0 | `b26v89c19zqg8o3frqlv6fvw0v4r1w0332qmi7fu03919` | `—` | `Q14_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q15.2 | 0 | `b26v89c19zqg8o3frqosfkliep4l6i62nt06hip7cqvel` | `—` | `Q15_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q16.1 | 15 | `—` | `b26v89c19zqg8o3frqou3pzrt8omjt9rqs6mhyqxfstbx` | `Q16_1.json` / `6229b4f88aebff9ea4d5f1f2d4ebb4e1af4eec06132b61e11e92490201aaac70` |
| Q17.1 | 22 | `—` | `b26v89c19zqg8o3frqou3wdn97v2wza3u3l7mz6i8al4t` | `Q17_1.json` / `d81efe48ada796e6e7ee3ff94b3858f51dc59596b4b9b9a2ddd92c06af56e7e7` |
| Q18.1 | 22 | `—` | `b26v89c19zqg8o3frqou3u8xd14lydygttqeg2bk2p7y5` | `Q18_1.json` / `e61ef23f2def628c40d4fb427c670da70dee9792940c4c1e4cabd97cde987860` |
| Q19.1 | 15 | `—` | `b26v89c19zqg8o3frqosubbv722tyi448klf12x6fk6f1` | `Q19_1.json` / `e968885023e05c5ff217e60197465a551ff3c3e321cc03e3e155339309eb9d98` |
| Q10.4 | 0 | `b26v89c19zqg8o3frqou3s3wgrrz8wmealixrp9fihit9` | `—` | `Q10_4.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q16.2 | 0 | `b26v89c19zqg8o3frqou3pzrt8omjt9rqs6mhyqxfstbx` | `—` | `Q16_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q17.2 | 19 | `b26v89c19zqg8o3frqou3wdn97v2wza3u3l7mz6i8al4t` | `b26v89c19zqg8o3frqosubbkkq1nh0o0a7ddfldyp54zh` | `Q17_2.json` / `1588609a990d9f90028a73fee778b018fec9b4dcfef7a8527f680e97c706b827` |
| Q18.2 | 18 | `b26v89c19zqg8o3frqou3u8xd14lydygttqeg2bk2p7y5` | `b26v89c19zqg8o3frqotov2266m5xte7xjmgabv6tsosd` | `Q18_2.json` / `fc33f4bc2d97e2d6343f7dcef4c9e76551e68729cfd3f4f820e5d51e5f49c5f9` |
| Q19.2 | 0 | `b26v89c19zqg8o3frqosubbv722tyi448klf12x6fk6f1` | `—` | `Q19_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q20.1 | 20 | `—` | `b26v89c19zqg8o3frqou3s6aqnxubdmivkans4cjd4e4d` | `Q20_1.json` / `3bae49b24aa2eb3ae5303e68866badeeee223d6b6279de362e9ba4a5a3473462` |
| Q21.1 | 9 | `—` | `b26v89c19zqg8o3frqou3s5p7cvshfdird86auhk2g96l` | `Q21_1.json` / `0ca81c6ac9b5eeaea3ea792cfcacfa5b06a252903e9f141b1fe21ae309497e4e` |
| Q22.1 | 5 | `—` | `b26v89c19zqg8o3frqou3q19obvo7ivv86lztsx83781p` | `Q22_1.json` / `9446bacf70febe7b51818b102cf311fee5e70df5b33508cb159964c90be0f453` |
| L04.1 | 7 | `—` | `—` | `L04_1.json` / `2876f12bcc4f611e6d1113e1b4226adcfa2eb584f688195023f1c29ba86cb28e` |
| Q17.3 | 0 | `b26v89c19zqg8o3frqosubbkkq1nh0o0a7ddfldyp54zh` | `—` | `Q17_3.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q18.3 | 3 | `b26v89c19zqg8o3frqotov2266m5xte7xjmgabv6tsosd` | `b26v89c19zqg8o3frqosubbkg4wapk5paxs9jjxgd9s3h` | `Q18_3.json` / `8e9929945feb163922cb763f99fbff9b53b541bb16c5aff350c2327a2ba3d867` |
| Q20.2 | 7 | `b26v89c19zqg8o3frqou3s6aqnxubdmivkans4cjd4e4d` | `b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod` | `Q20_2.json` / `07ec17e54a74eec7d22df84e97cabbd5f6b9ed1956b3c2208c7ef58375d551c3` |
| Q21.2 | 0 | `b26v89c19zqg8o3frqou3s5p7cvshfdird86auhk2g96l` | `—` | `Q21_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q22.2 | 0 | `b26v89c19zqg8o3frqou3q19obvo7ivv86lztsx83781p` | `—` | `Q22_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q23.1 | 24 | `—` | `b26v89c19zqg8o3frqou42rj7g08znqouocjegbt61nct` | `Q23_1.json` / `83ed200c7e83415d28aaed72fb631ebbf9daa29d0fc154e12190761f2eecddb7` |
| Q24.1 | 9 | `—` | `b26v89c19zqg8o3frqou3weuez2g6px76svdlymqyk2nx` | `Q24_1.json` / `9f889ec6036b0eba317736f1bb273285352edd4f8a0ca745a483f2f50819409a` |
| Q18.4 | 0 | `b26v89c19zqg8o3frqosubbkg4wapk5paxs9jjxgd9s3h` | `—` | `Q18_4.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q20.3 | 0 | `b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod` | `—` | `Q20_3.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q24.2 | 0 | `b26v89c19zqg8o3frqou3weuez2g6px76svdlymqyk2nx` | `—` | `Q24_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q25.1 | 25 | `—` | `b26v89c19zqg8o3frqot9cn5kp787htrkaq8m4uqs4br1` | `Q25_1.json` / `73824e3e238cdd1a64c8e28e10998ad0ee63a6c1d4932ff3f0d0423e3edd3cc9` |
| L05.1 | 63 | `—` | `—` | `L05_1.json` / `341bbc851da9cc3569ba5d221225866a70f58fba24b2e86679f2e84cc1be673e` |
| Q25.2 | 25 | `b26v89c19zqg8o3frqot9cn5kp787htrkaq8m4uqs4br1` | `b26v89c19zqg8o3frqlvlf2r1maunkjskzqk6i3wmsc59` | `Q25_2.json` / `51d89ac4ed70f16fd388c2228ad26e333e8cc7f19721b8cd25235830f9cd222c` |
| Q26.1 | 10 | `—` | `b26v89c19zqg8o3fr62dkb1o48zjt7gsra2wkov32cqyl` | `Q26_1.json` / `e85129bde58acace7e08b089f6a52bd6b544e229610ac4c1a38ed3bf712ae78d` |
| Q27.1 | 6 | `—` | `b26v89c19zqg8o3frqou3s6ahkuj7euw6lyza6b3vgb5p` | `Q27_1.json` / `cba1a7db8fd9d5b0675860ab216256b2e598b42478262ee8f425fdc1b7237543` |
| Q28.1 | 1 | `—` | `b26v89c19zqg8o3frqou3uaf3jm5651ase8vg5b8y12f1` | `Q28_1.json` / `6b99383004893b842c365d7a4eca8681ae554226f58d3e3783c9de71babaa7b3` |
| Q25.3 | 25 | `b26v89c19zqg8o3frqlvlf2r1maunkjskzqk6i3wmsc59` | `b26v89c19zqg8o3frqlthzt3ofae7t7fywx08ukcipxfh` | `Q25_3.json` / `572696bd340582b435700a641d430249afd04fba014ae34c1b8fcb0e7ef472ce` |
| Q26.2 | 0 | `b26v89c19zqg8o3fr62dkb1o48zjt7gsra2wkov32cqyl` | `—` | `Q26_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q27.2 | 0 | `b26v89c19zqg8o3frqou3s6ahkuj7euw6lyza6b3vgb5p` | `—` | `Q27_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q28.2 | 0 | `b26v89c19zqg8o3frqou3uaf3jm5651ase8vg5b8y12f1` | `—` | `Q28_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| L06.1 | 9 | `—` | `—` | `L06_1.json` / `2c8c8142de6d48dc3d3f730f73efd277cb6815b473277afb1f7afe2698d7c32d` |
| Q25.4 | 25 | `b26v89c19zqg8o3frqlthzt3ofae7t7fywx08ukcipxfh` | `b26v89c19zqg8o3frqlt2s31bgkxyo1ynsoicrspgoqkd` | `Q25_4.json` / `04f3beda17b12eeb03ec892a64e140c5ac368f17b6290662b841a0195393b8ab` |
| L07.1 | 8 | `—` | `—` | `L07_1.json` / `ed2e06fcc011fdf5d39286cee6a681030a3774388307423a41e17569124ae830` |
| Q29.1 | 16 | `—` | `b26v89c19zqg8o3frqou3u8x2d2hfop2inlnlkvlny7p9` | `Q29_1.json` / `badb1d72cd366779832f46738aa2b6ce4639ca2b58bb40bb6f5cf51b34315bd7` |
| Q25.5 | 25 | `b26v89c19zqg8o3frqlt2s31bgkxyo1ynsoicrspgoqkd` | `b26v89c19zqg8o3frqls8ckhotbsvz5squrdx382udrb1` | `Q25_5.json` / `26533e8f94cde091d07f889fb085e84cb8dcfc5b158c850e3cde32f19be144a1` |
| Q29.2 | 0 | `b26v89c19zqg8o3frqou3u8x2d2hfop2inlnlkvlny7p9` | `—` | `Q29_2.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |
| Q25.6 | 25 | `b26v89c19zqg8o3frqls8ckhotbsvz5squrdx382udrb1` | `b26v89c19zqg8o3fr62f8tadt77nfokrh3c42hftvfdkt` | `Q25_6.json` / `68a9088058752710cb07a22ca003a81605b4078727648ad2b7bb31c921e7f23a` |
| Q25.7 | 25 | `b26v89c19zqg8o3fr62f8tadt77nfokrh3c42hftvfdkt` | `b26v89c19zqg8o3fr62eebmisiv10bn0yvh8hp4xdelx9` | `Q25_7.json` / `f5b33c8cec5ecee99d5833722defc2d18f1d2b6ed8e57bc0f6907d29fc108669` |
| Q25.8 | 25 | `b26v89c19zqg8o3fr62eebmisiv10bn0yvh8hp4xdelx9` | `b26v89c19zqg8o3fr62dkb1ys3n0v11urekoy2ost01h9` | `Q25_8.json` / `925d70d0063531b8aa6355dd464dbf7e03a1e0846d8a9fca0b884439c8d19884` |
| Q25.9 | 25 | `b26v89c19zqg8o3fr62dkb1ys3n0v11urekoy2ost01h9` | `b26v89c19zqg8o3fr62d4oe7rek6264rzxunzl45rbzi5` | `Q25_9.json` / `aa82b01400e06b80181f48e520c65a186d5e0619aecf3c2cb6582d292ffab3e9` |
| Q25.10 | 25 | `b26v89c19zqg8o3fr62d4oe7rek6264rzxunzl45rbzi5` | `b26v89c19zqg8o3fr62bvmi2hvduv1w8xvbhhgw5mmoot` | `Q25_10.json` / `f34bb71052f1a3bf515c0246bc59053925cbe2db8dac13bd65591376116bf36b` |
| Q25.11 | 25 | `b26v89c19zqg8o3fr62bvmi2hvduv1w8xvbhhgw5mmoot` | `b26v89c19zqg8o3fr5zf1pi7z6naeq51jhk0j91zvl0u5` | `Q25_11.json` / `8db2f343a7989a6b0aafb31f05717a37819b3a9fbc9c018f98d90b100caf98b5` |
| L08.1 | 7 | `—` | `—` | `L08_1.json` / `cd31720e48ac5e9754b34763d7e84cfb1517e9b185990c6cea6a161b430ca815` |
| Q25.12 | 25 | `b26v89c19zqg8o3fr5zf1pi7z6naeq51jhk0j91zvl0u5` | `b26v89c19zqg8o3fr5ze7gf28vjy0hm29n7jd4j7bq4ql` | `Q25_12.json` / `38490c07c22bbe815733737400d3d46297bb8e1f000dbad04474a4376f90e299` |
| Q25.13 | 0 | `b26v89c19zqg8o3fr5ze7gf28vjy0hm29n7jd4j7bq4ql` | `—` | `Q25_13.json` / `d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc` |

### Lots d’ID lus directement

- **L01** : `LOOKUP 1815088124193579253,1815088727250858444,1815291249102119198,1815372294426124565`
- **L02** : `LOOKUP 1815420495858114916,1816447409859518552,1816420955767624009,1816729265435562165,1815800630570516912,1815800633510727963,1815084272098697611`
- **L03** : `LOOKUP 1815291795787690478,1815293200095138249,1815302038282256628,1815375121294725503,1815389229758693508,1815479580838555682,1815850318758043898,1815492336123858975`
- **L04** : `LOOKUP 1815105565741470098,1815105605142761543,1815105638768464295,1815300464646443155,1815344994787397986,1813651418471100660,1810386941180883011`
- **L05** : `LOOKUP 1799443429035810971,1810308337021653216,1812258574049157405,1812482517993156754,1812923007775506580,1813024750341644560,1814290486519005427,1814305122131849630,1814652734366163174,1814653415202365445,1814655819457188001,1814680572444189084,1814819410739404800,1814964457098858705,1815091075431678146,1815094571497595108,1815098272849056151,1815105968381820966,1815112836386812271,1815117260123771210,1815154986663243909,1815178722309550194,1815186554345632039,1815223812905943406,1815233925662306427,1815240482026344565,1815241483466744145,1815280358906364119,1815330372143435778,1815398232052130269,1815408854873821205,1815412439959433432,1815458911467827506,1815484100482064631,1815506759055970611,1815547856838877340,1815581885885476978,1815590860064788556,1815631098380255296,1815660277893111925,1815736604519969254,1815761364842897696,1815762560550887518,1815767229440606580,1815767452707364922,1815770767755190547,1815777174495928647,1815806774542295366,1815824916169580789,1815833468968001765,1815874978568626290,1815920077461692647,1815955909991932266,1815968611384819977,1815998985598840940,1816277804448899146,1816439504380768331,1816810357018460659,1818296657483624508,1842690739609759804,1842704030080069791,1842711728679006479,1844112981656994058`
- **L06** : `LOOKUP 1820443412040171659,1817218497304567925,1816071057822056589,1815656329887010867,1815105812076904904,1795480077255209108,1798702410157973511,1814666414705274926,1815389229758693508`
- **L07** : `LOOKUP 1815656223121023203,1816070825877070009,1817218352278024318,1820443349163413780,1815609933611794890,1815886884972716329,1816729265435562165,1815850318758043898`
- **L08** : `LOOKUP 1814763940410499481,1814779160377602331,1813086353741230327,1813220461867573395,1812984492157771825,1813004360592552354,1815004677160776126`

## Erreurs, sources perdues et limites

- 35 réponses X contiennent errors[] partiels ; leurs objets data valides ont été utilisés et les objets refusés ignorés. Aucun contournement des contrôles d’accès. Les compteurs ci-dessous comptent les messages d’erreur, y compris répétitions de la même référence.
- Types : {"Not Found Error": 51, "Authorization Error": 26, "Field Hydration Error": 11}.
- Appels concernés : Q06.2, Q09.1, Q08.2, Q10.2, Q11.1, Q08.4, L03.1, Q15.1, Q10.3, Q16.1, Q17.1, Q18.1, Q19.1, Q17.2, Q18.2, Q20.1, Q21.1, Q22.1, Q18.3, Q24.1, Q25.1, L05.1, Q25.2, Q26.1, Q25.3, Q25.4, L07.1, Q25.5, Q25.6, Q25.7, Q25.8, Q25.9, Q25.11, L08.1, Q25.12.
- Champs d’hydratation parfois incomplets, en particulier referenced_tweets et in_reply_to_user_id. Les variantes sont conservées ; une absence de référence n’est pas une preuve universelle d’absence de réponse.

- Not Found Error — IDs distincts : 1783751408468324569, 1786122015876764085, 1786348192147141079, 1786849426545246611, 1793363257782346231, 1794066339088220581, 1794822048327639212, 1796318913384583619, 1799198915696198038, 1799597823165681775, 1801025288807088481, 1801565701326409961, 1802854018122686806, 1803110075600720291, 1803122195025240239, 1803525224807215472, 1806012773324726527, 1806385597033963666, 1806518096519454762, 1806790494099521773, 1811446971686625481, 1812136614845448429, 1812896481525014909, 1814713528281968818, 1814738306589917312, 1815037653709902321, 1815125720785391758, 1815168955126005831, 1815286724618019243, 1815312139323621834, 1815323562972238010, 1815367777970168303, 1815422915237589236, 1815428687656869893, 1815445657190015402, 1815479580838555682, 1816137027315982422, 1816480334961156279, 1825218625047035975, 1844189634252898564.
- Authorization Error — IDs distincts : 1785772879373602953, 1786861517285286340, 1789356744466194844, 1793830878210294134, 1794483980516888642, 1795554688655401339, 1795563627493109854, 1796702356073029723, 1798820560497152161, 1802917824991477830, 1810744618532884826, 1811735806765383814, 1814102155441123515, 1814156240936747389, 1814311053523841159, 1814349288131928566, 1815189782575681998, 1815192551286079816, 1815306202282164446, 1815372655513702612, 1815411879168061687, 1815902635620180119, 1843102987134361934.

- Parent Hasten0x 1815479580838555682 : non trouvé par X. Index Wayback exact ouvert pour `twitter.com/Hasten0x/status/1815479580838555682`, filtre HTTP 200/collapse digest : `[]`. URL : https://web.archive.org/cdx/search/cdx?url=twitter.com%2FHasten0x%2Fstatus%2F1815479580838555682&output=json&filter=statuscode%3A200&collapse=digest . Cela ne prouve ni la suppression, ni l’absence de toute archive, ni le contenu initial. L’hôte x.com et les miroirs tiers n’ont pas été explorés exhaustivement.
- Noah : le parent de sa réponse à takicalls, 1815372655513702612, est refusé. On peut lire sa propre réponse, pas inventer le texte du parent. Ni code ni règle exacte de clustering récupérés.
- Contacts Musk : les résultats du projet sont des déclarations d’une partie intéressée ; aucune communication privée authentifiée ni confirmation indépendante de juillet/octobre obtenue. Les anciennes revendications ne sont pas requalifiées en nouveaux faits.
- Langues : EN/ZH explorées par lexiques financiers, sources et adresses ; KO sur juin–octobre ; FR/ES/PT en recherches dédiées pendant le noyau juillet. Les tags lang retournent aussi des faux positifs et des textes multilingues ; ils ne constituent pas une garantie linguistique. Aucune nouvelle piste financière forte n’a été retenue uniquement pour remplir une langue.
- Temporalité : noyau 13–26 juillet ; élargissements explicites juin–octobre et mai pour BARRON. Pas d’export exhaustif de toutes les mentions de juin à octobre, ni de tous les historiques de comptes, ni de recherche rétrospective générale 2025–2026 dans cette passe.
- Médias : seulement les images utiles ont été récupérées/lues, et certaines miniatures de GIF. Le GIF books_empress est une réaction, pas un screenshot de Musk. Des GET urllib ont répondu 403 ; six médias publics utiles ont ensuite été récupérés normalement avec curl, d’autres avaient déjà été obtenus. Aucun accès authentifié ni contournement de session. Pas d’analyse forensique des appareils ou d’EXIF attestant la prise des captures.
- La borne basse Wayback de 19:03:27 UTC / 20:03:27 Lisbonne est reprise du dépôt, pas retéléchargée. La nouvelle borne haute est un post de screenshot, pas l’heure du clic ; la première réaction textuelle relevée à 19:24:24 UTC / 20:24:24 Lisbonne n’est pas transformée en capture.
- Les profils/public_metrics sont des lectures actuelles, pas des audiences de 2024. Les outils relisent les objets disponibles aujourd’hui : la totalité des éditions historiques n’est pas garantie.
- Pas de replay on-chain, pas de calcul de PnL net complet, pas de vérification des 190 SOL, des 5/60/16 SOL, de la supply Noah ou des achats KLLARY/RETIREDI0/BARRON/ZOOMER. Les signatures visibles mais ambiguës dans les images ne sont pas complétées au hasard.
- Le mint JOE reste inconnu ; le contrat BILLY effectivement visé reste à résoudre ; le mint ZOOMER du promoteur n’est pas encore lié transactionnellement à H3Qs. Les wallets de dissident42069 et de l’équipe ne sont pas attribués.

### Références partielles non comptées comme posts archivés

1785667859118497822, 1785896191454220500, 1786130805829325125, 1786222931296604387, 1786470360864395409, 1787223420201046123, 1787582149429760491, 1787900836514824456, 1787911168616534241, 1788348356680671623, 1788363913634914481, 1788377662232084743, 1789316538735951890, 1789657351123083366, 1790004032255176748, 1790152057833312395, 1790407808241770921, 1790410130842095625, 1790437542975664425, 1790505613052539022, 1790741479347921101, 1791142112391844342, 1791193254580695442, 1791546177139122506, 1791769130204635231, 1791921412653084677, 1792258712016662559, 1792450182141063278, 1792948215060320571, 1793010292919517391, 1793011138923237606, 1793024418983096614, 1793654641974288558, 1793807504947777732, 1793825829748867262, 1794034599124955495, 1794776545971806565, 1794810798772191736, 1794823314898391347, 1794825224103600330, 1794826572693966928, 1794857649366032571, 1794872939290284213, 1795106404728013133, 1795475193093128234, 1795561181798891936, 1795563353751830711, 1795886852618010997, 1796201708076597658, 1796207512410042500, 1796296401137123623, 1796303785888989552, 1796308209356988643, 1796345416293949862, 1796424737939456202, 1796575172369203605, 1796597273050362102, 1796604185343033461, 1796619113529245912, 1796673199163183439, 1797092389649027275, 1797377353590481338, 1797392841896804550, 1798077735488942139, 1798425785591640302, 1798778127805763873, 1798786695116279849, 1798832068446572702, 1799501773322797077, 1799511709595369565, 1799894461062795677, 1800555105131102395, 1800636123947082192, 1801004601644056598, 1801271098568298930, 1801678301125034098, 1801678608622141555, 1801992781373608228, 1802825492405669930, 1802839132084859242, 1802851140549169615, 1802854180043862291, 1802860407415009388, 1802876029842682105, 1802901401242099776, 1803093790111957119, 1803331506049523742, 1803397727482790008, 1803451823174340664, 1803515950055977143, 1803575252049601018, 1803584560099103008, 1803811644297957675, 1803826093599690958, 1805338792381104318, 1805343117396128135, 1806031821534273911, 1806153115403755768, 1806354008354812102, 1806358875966255479, 1806378029440188844, 1806765077254783268, 1811148085281837466, 1811181306438660375, 1811446491245924853, 1811695511889736171, 1811772584305762625, 1811812358508953803, 1812479518940012636, 1812556914833969334, 1812930050779717892, 1813362896321278131, 1813557558655046135, 1813776349229879767, 1814041726400753778, 1814060957745983715, 1814650918563991741, 1814685827076645115, 1815074326195879969, 1815093862748303795, 1815103916180422882, 1815108740913279457, 1815326886676840912, 1815376714001977643, 1815398333504016533, 1815425582663868559, 1816277331981242743, 1816809724626587985.

## Médias conservés et empreintes

Ces fichiers sont des copies binaires publiques, sauf montage0.jpg (planche dérivée, exclue ci-dessous). Les noms locaux .jpg peuvent contenir un PNG source : les octets téléchargés n’ont pas été réencodés. Empreinte ≠ preuve de l’heure de prise. Les URL et media_key sont dans le JSONL.

| Fichier local dans dmaga_pass2_work | SHA-256 |
|---|---|
| `1815105191966024005_0.jpg` | `e472635f23aec556a6869017db967b95346359a5a51c0c568d8e3907328791ab` |
| `1815105565741470098_0.jpg` | `53a1e04d7565c4f665fc2661b3e565737743ab4e9b51817ee28035167e013f87` |
| `1815105666505396719_0.jpg` | `93edce557172d6ed7f9a1311329f9b71c24a00c80507294e6582611633135218` |
| `1815105812076904904_0.jpg` | `93d239a02ca23f83aa3c158e6754786cdf037472f0a4467f3900ecc416cb0ce3` |
| `1815106023071334579_0.jpg` | `34582746519bb957f5a1bc0657102c3b9f6b919edeba58f061c50271b865e5c2` |
| `1815106032076734880_0.jpg` | `bc40a049c2a40aabd93e2aaa511b0588fd6dc9d5cece2c0b86bdd46eda73d792` |
| `1815106078142787931_0.jpg` | `bc40a049c2a40aabd93e2aaa511b0588fd6dc9d5cece2c0b86bdd46eda73d792` |
| `1815300464646443155_0.jpg` | `60e3b45f8ba77bd4b0f0b98236381d74caed5877d1989d326e95a4cc54d7a808` |
| `1815300464646443155_1.jpg` | `07f31d748fc6f753607e6482ce38107e4d59a385798a5750c9e2134fee0e79e2` |
| `1815300464646443155_2.jpg` | `68ccedcf5c2c8b98f25b5c70fd2ba669f2650665d6f0e41c1e916a9814b49ff1` |
| `1815300464646443155_3.jpg` | `6ba4c8d33a1901d7f84bfab2a8ab6e9909a58aab37b47343212456c5e7ab97e5` |
| `1815344994787397986_0.jpg` | `9111267027e10fb0a853d4f87661702162461cb7511c8c1783cf4eef111c9b80` |
| `1815344994787397986_1.jpg` | `1df9e1464dc91fb1ac9e7a076305d1f26bcfe325993e71cb7739007ff89fb661` |
| `1815850318758043898_0.jpg` | `062fd90a8e7cec83b3011f9333c40920ecc6ee4b43b55c13619581f932cf1a03` |
| `1815850318758043898_1.jpg` | `885942aedbcbdca1599354285e54060a020bdc0f6047a262f4bc00176109dd64` |
| `1816729265435562165_0.jpg` | `b5f38e7a32cfd275f15d45e90be65b4deec105570c73e9929af7f2c2e6f4f889` |
| `1816729265435562165_1.jpg` | `b14fe0f1b6b015f24134a2b412c947937daef5eb80cd2cb9bd69b6034aba60d4` |
| `dogeretweet.jpg` | `bc40a049c2a40aabd93e2aaa511b0588fd6dc9d5cece2c0b86bdd46eda73d792` |
| `jeffro-reply1.jpg` | `e00220b4b622a893f391abe789615d3f11ed5205368593e61b6a9f6ae0f6cf91` |
| `jeffro-reply2.jpg` | `26c86f33bc80024ca7fb73a8c7c983955cd1da2be04ff418368e1d8e1b6f9ab6` |
| `jeffro-vault.jpg` | `00e9dcd2bb2bb558197230fd4324ef394da5fd28d9388ac0174f47e01d7cf3df` |
| `jeffro1.jpg` | `a6babe9a07d06af957444cf49fe85c86fea23a70e3830a79b9d3e38f35e5c189` |
| `jeffro2.jpg` | `0320f7e945195a8b47b52fa148148ca9f4ca9fa4597287f577f57a1f22fcd3b3` |
| `noah1.jpg` | `8596d23a9c8a80aa2552891e726768f5a12bf70a70bbc436027b47dae8f9be48` |
| `noah2.png` | `a0e55bc810b0fba26b88c4e08e509b197c42ffb1411fc27acd75a87ba250ba5f` |
| `teslaboomermama.png` | `52b5c72a44d2418106d8d3189c986411dbade61cba01f650491878fb92d0273c` |

## Vérification finale / fermeture

Les fichiers livrés sont les cinq noms demandés. Le ZIP ne contient que ces cinq fichiers. Aucune Page n’a été créée. Les scripts locaux d’assemblage, index intermédiaires et réponses complètes restent sous `/workspace/dmaga_pass2_work/` pour audit ; ils ne modifient pas le dépôt et ne tournent pas en arrière-plan. La mission se termine avec cette livraison.

## Contrôles de qualité finaux et reprises

Les quinze résultats citent 43 posts distincts de 21 auteurs, tous présents dans le JSONL. Ce ne sont pas autant de confirmations indépendantes. Les pages de comparaison ont été collectées intégralement ; cela ne signifie pas que chaque promotion ou faux positif a été analysé manuellement comme une source pertinente.

L’API expose selon l’outil `includes.tweets` ou `includes.posts` ; les deux sont ingérés. Les types `retweeted` et `reposted` sont reconnus comme reprises, avec leur forme brute conservée. Quatre contrôles directs, rappelés ici pour l’audit et **non comptés comme nouveaux résultats A1**, séparent effectivement auteur original et compte de reprise :

| Reprise @DarkMagaCoin | Original et auteur | Date de l’original, Europe/Lisbon | Date de la reprise, Europe/Lisbon |
|---|---|---|---|
| [1814779160377602331](https://x.com/DarkMagaCoin/status/1814779160377602331) | [1814763940410499481](https://x.com/pmarca/status/1814763940410499481), @pmarca | 2024-07-20T21:46:54+01:00 Lisbonne | 2024-07-20T22:47:23+01:00 Lisbonne |
| [1813220461867573395](https://x.com/DarkMagaCoin/status/1813220461867573395) | [1813086353741230327](https://x.com/kanpai/status/1813086353741230327), @kanpai | 2024-07-16T06:40:46+01:00 Lisbonne | 2024-07-16T15:33:40+01:00 Lisbonne |
| [1813004360592552354](https://x.com/DarkMagaCoin/status/1813004360592552354) | [1812984492157771825](https://x.com/kanpai/status/1812984492157771825), @kanpai | 2024-07-15T23:56:01+01:00 Lisbonne | 2024-07-16T01:14:58+01:00 Lisbonne |
| [1815004677160776126](https://x.com/DarkMagaCoin/status/1815004677160776126) | [1814920352134537332](https://x.com/pmarca/status/1814920352134537332), @pmarca | 2024-07-21T08:08:26+01:00 Lisbonne | 2024-07-21T13:43:30+01:00 Lisbonne |

Ces contrôles ne datent pas un changement de profil de Musk. Tous les IDs de posts archivés concordent à la seconde avec leur horodatage Snowflake ; toutes les adresses complètes du CSV décodent en 32 octets Base58, contrôle de syntaxe et non preuve d’existence ou de propriété. Le corpus n’est pas rattaché à un commit Git immuable : les fichiers de référence ont été lus pendant cette session. Les sources, variantes et hashes sont conservés ; aucune écriture GitHub n’a été effectuée.