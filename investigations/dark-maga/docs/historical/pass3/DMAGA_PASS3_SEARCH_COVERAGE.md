# Passe 3 — couverture et limites, 6 novembre 2026 (Lisbonne)

## Bilan vérifiable

- **88 appels X** : 83 pages de recherche complète, 3 lectures directes groupées, 2 lectures de citations. 27 requêtes distinctes Q01–Q27, toutes paginées jusqu’à l’absence de next_token ; aucune continuation délibérément laissée ouverte. Les deux endpoints quotes retournent0, ce qui ne prouve pas qu’il n’existe aucune citation.
- Budget de planification communiqué : plafond~800 appels pour cette passe après~111 antérieurs. Arrêt à résultats documentaires raisonnablement épuisés des requêtes ciblées, pas épuisement artificiel du budget. Quota quotidien restant exact non exposé ici ; aucun429 observé. Appels publics seulement, pas lecture de messages privés ni get_users_me. Pas de coût estimé.
- 1171 objets-ID uniques vus, y compris includes et bruit ; 813 absents de l’index couvert, mais **316 posts nouveaux sélectionnés complets de 148 auteurs** réellement exportés. 128 objets incomplets tous périmètres confondus, exclus du DELTA. Ne pas confondre ces compteurs avec des découvertes indépendantes.
- 182 arêtes documentaires nouvelles, dont4 dérivées explicitement non financières. Aucun edge de transfert certifié. Certaines cibles sont connues ou non récupérées, donc volontairement absentes du DELTA.
- **19 médias originaux analysés** :18 images et1 vidéo ;5 frames dérivées lues pour la vidéo,24 lignes du CSV. Fichiers réels téléchargés, formats/dimensions et SHA256 calculés sur octets ; une somme de contrôle n’authentifie pas le contenu d’une capture.
- Sept résultats seulement : P3-01/02 nouvelles contraintes de grand livre ; P3-03 nouvelles sources sociales ; P3-04/05 correction/contrôle documentaire ; P3-06/07 nouveaux témoins comparatifs, pas nouvelles connexions DMAGA prouvées.

## Assimilation et déduplication

Tree SHA `65c681bbb48eecd96e4716f09490f5e2081a640d`, arborescence récursive non tronquée. Les 24 fichiers ci-dessous ont été téléchargés en lecture seule puis vérifiés contre les Git blob SHA annoncés ; ni pull vers une branche de travail, ni commit/PR, ni modification distante. Il s’agit d’un snapshot ciblé des textes et corpus demandés, non d’une lecture exhaustive de chaque fichier brut du dépôt.

`data/x_posts.jsonl`5155 lignes +pass2 1001 lignes−35IDs communs = **6121 IDs archivés uniques** ; l’index conservateur de tous les parents/citations/URLs donne **8116 IDs couverts**. Les deux ensembles sont exclus du DELTA. 1821 handles d’auteurs/mentions, 1577 candidats d’adresses/contrats, textes normalisés des posts et lignes d’hypothèses/contextes indexés ; présence d’une chaîne dans l’index n’est pas validation d’une adresse ni d’une hypothèse.

Index et reçus de travail persistants : `/workspace/dmaga_pass3_work/baseline_index.json`, `baseline_manifest.json`, `calls.json`, `raw/`, `index.json`. Ils ne sont pas ajoutés aux sept livrables : le DELTA inclut néanmoins variantes brutes, provenance/page/paramètres essentiels et hash du payload local. Les enveloppes d’outils et les JSON extraits restent distincts dans le ledger local.

| Chemin figé | Git blob SHA |
|---|---|
|`README.md`|`3df87a82ccce0c5e7746838c5320e987b8b9528b`|
|`data/historical_x_pass2/DMAGA_X_ARCHIVE.part-001.jsonl`|`7b10567ff024adb37a06532906cd5deddcec6ad7`|
|`data/historical_x_pass2/DMAGA_X_ARCHIVE.part-002.jsonl`|`242ef0254d72314b30eb69733ce685cc3c59cd14`|
|`data/historical_x_pass2/DMAGA_X_ARCHIVE.part-003.jsonl`|`d2d2acdde2b66f51df785c74adeaeb197ed99d92`|
|`data/historical_x_pass2/DMAGA_X_ARCHIVE.part-004.jsonl`|`2606d1095cf95bacbb65c9f11485c84f0360c270`|
|`data/historical_x_pass2/DMAGA_X_ARCHIVE.part-005.jsonl`|`92ceeb81d616477efcbc32977a2af2d6efe6251a`|
|`data/x_posts.jsonl`|`97e899b4185eac3bb001f599fd73b041bcc74788`|
|`docs/CASE_REPORT.md`|`050325755badbfcd9025ed4345c4ef18a00cde96`|
|`docs/SOCIAL_FINDINGS.md`|`5d769b1720cd0537d2c8124740c00253d57852e4`|
|`docs/TIMELINE.md`|`d14bd228cb70a66688bf195677de5d45e8ea631b`|
|`docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md`|`f313a259dd41c3f049acf627a110144a536f33d2`|
|`docs/historical/PROMPT_GROK_BOT.md`|`5b12d1b50a6f52e25b99bfed486c6291b95b98be`|
|`docs/historical/X_SOURCE_MANIFEST.json`|`9d51d59047c746af6ae6ea8dcdf3b0ef48adfea1`|
|`docs/historical/pass2/DMAGA_WALLET_TWEET_LEADS.csv`|`fec0fba28b96953228609fae3fb95973b3d82854`|
|`docs/historical/pass2/DMAGA_X_NEW_FINDINGS.md`|`1f9de9e687d09b5e75adf2aa463cfcd72934e400`|
|`docs/historical/pass2/DMAGA_X_SEARCH_COVERAGE.md`|`2f93b740ba8f4c50463037071814a7f0028f6ecb`|
|`docs/historical/pass2/README.md`|`3d998426e5c0c1e5a1cc72a88f75787cd74ad8af`|
|`investigations/2026-11-05_debridge_winners/RAPPORT_RESULTATS_NOUVEAUX.md`|`a3f90a8acd59c88f20f37cb45c40a85e4586d150`|
|`investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md`|`ea1ab49e855d8ae47f7301939e95f33f4c593cd6`|
|`investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md`|`fd1d5babbb1fe2af9ae25675644cffe1d55dd378`|
|`investigations/2026-11-06_dmaga_kekius_cross_token/FINDINGS.md`|`e4aea0057e45f5dc843a5f97d713ac733cbfd58c`|
|`investigations/2026-11-06_dmaga_kekius_cross_token/UNRESOLVED.md`|`2961c54294fd0d7245faf274ee0dcba772e29178`|
|`reports/EARLY_BUYERS.md`|`f285836ce34a66d025a07c6d9aefced76bdcac64`|
|`reports/TOP_TRADERS.md`|`e592c98b938ce9913dcd98d83da8fc673012474a`|

## Outils, paramètres et limitations

- Recherche réellement utilisée : `x.search_posts_all`, plus `get_posts_by_ids` et `get_posts_quoted_posts`. Aucun endpoint de recherche sémantique dédié dans le catalogue disponible ; pas de recherche sémantique prétendue. GitHub via outils de lecture uniquement. HTTP public pour les médias et WebSearch/WebFetch pour les archives, jamais pour appeler l’API X.
- Champs demandés : `created_at,author_id,conversation_id,referenced_tweets,note_tweet,entities,attachments`, expansions auteurs/références/médias, URL/type/dimensions des médias ; variants/preview pour les lectures vidéo. Certaines réponses n’hydratent pas tous ces champs, notamment conversation_id. Préserver null plutôt que l’inventer. Les usernames sont ceux observés lors de la lecture, pas une preuve de leur valeur historique.
- `max_results=100` demandé ; les pages observées contiennent au plus25posts, sans prétendre que c’est la limite théorique globale de X. Pages courtes avec next_token suivies normalement, y compris la page finale vide.
- Les réponses `200` avec errors[] fournissent des données utilisables ; les IDs en erreur sont marqués manquants et non reconstitués. Plusieurs références identiques peuvent apparaître en erreur dans différentes pages sans nouvelle tentative directe. Aucun401/403/429 fatal retourné par ces appels.
- Stratégies de repli effectivement mises en œuvre : auteurs et destinataires (Q16,Q20), adresses longues/courtes, auteur+date (Q22), lectures directes L01–L03, relations replied_to/quoted et recherche de citations C01/C02. L’échec conversation_id mentionné dans la passe antérieure n’a pas été “résolu” par une prétendue récupération exhaustive de tous les fils : reconstruction partielle à partir des données accessibles. Les reposts natifs sont exclus par -is:retweet dans les recherches pour réduire le bruit ; originaux et relations retrouvés par includes/lecture/archives. Cela réduit la couverture des cascades de reposts et doit rester explicite.
- Langues : anglais majoritaire ; chinois simplifié/traditionnel avec termes techniques(Q09), coréen/espagnol/français/portugais(Q15), filtres lang de ces quatre langues(Q23). Pas d’équivalence de rappel garantie entre langues. Pas de filtre minimal de likes/vues ni de sélection réservée aux comptes importants ; “petit compte” ne signifie pas faible audience mesurée en2024.
- Déduplication sur post_id, pas sur les compteurs. Les variantes API et occurrences restent dans raw_post_variants/provenance ; types reposted/retweeted normalisés seulement dans le graphe, type brut préservé dans le post. Le texte note_tweet est retenu quand fourni, sinon text ; les entities et edit_history restent dans les variantes brutes. Une seule version accessible ne certifie pas l’absence d’édition.
- Snowflakes : `(int(id)>>22)+1288834974657` millisecondes, converties UTC puis zoneinfo Europe/Lisbon. Zéro désaccord à la seconde sur les posts exportés. Le temps dérivé d’un ID ne date ni capture, ni transaction, ni changement d’avatar.

**Erreurs partielles** :82 occurrences, {'Not Found Error': 43, 'Authorization Error': 39} ; 66 ressources distinctes indiquées.

|Appel|ID manquant|Erreur|
|---|---|---|
|Q01.1|1815096055337496944|Not Found Error|
|Q02.1|1815187368485200317|Not Found Error|
|Q05.1|1809601942059946184|Authorization Error|
|Q05.1|1806012773324726527|Not Found Error|
|Q05.1|1787284537619173428|Authorization Error|
|Q04.2|1873980651164360876|Not Found Error|
|Q06.1|1815171057034121428|Authorization Error|
|Q06.1|1815152086264238555|Not Found Error|
|Q06.1|1815145588218024030|Not Found Error|
|Q08.1|1802917824991477830|Authorization Error|
|Q08.1|1791741360451850661|Authorization Error|
|Q09.1|1815902635620180119|Authorization Error|
|Q06.2|1815125869456724137|Not Found Error|
|Q06.2|1814831715983974617|Authorization Error|
|Q10.1|1815103769702793675|Authorization Error|
|Q12.1|1816149651193520215|Authorization Error|
|L01.1|1815054158367432804|Not Found Error|
|Q14.1|1815443939467686162|Not Found Error|
|Q16.1|1815372655513702612|Authorization Error|
|Q17.1|1815101355297587267|Authorization Error|
|Q17.1|1815091420060852699|Authorization Error|
|Q10.2|1815094761696723367|Not Found Error|
|Q10.2|1815096950800216222|Not Found Error|
|Q10.2|1815104100998250841|Authorization Error|
|Q12.2|1815562567378411764|Not Found Error|
|Q12.2|1815422915237589236|Not Found Error|
|Q13.2|1819801808954364066|Authorization Error|
|Q13.2|1819793811247182087|Authorization Error|
|Q13.2|1819795101956067401|Authorization Error|
|Q16.2|1815306202282164446|Authorization Error|
|Q17.2|1810977261887144165|Authorization Error|
|Q17.2|1815097306632655073|Not Found Error|
|Q12.3|1815341441616634079|Not Found Error|
|Q22.1|1825527888042774825|Not Found Error|
|Q10.4|1813714973031358820|Not Found Error|
|Q17.3|1814871197860893137|Authorization Error|
|Q17.3|1815094946179023356|Not Found Error|
|Q10.5|1815089091689750785|Authorization Error|
|Q23.3|1815286724618019243|Not Found Error|
|Q23.3|1815168955126005831|Not Found Error|
|Q23.3|1815192551286079816|Authorization Error|
|Q23.3|1815189782575681998|Authorization Error|
|Q23.4|1815037653709902321|Not Found Error|
|Q23.4|1814156240936747389|Authorization Error|
|Q23.4|1812539582539333912|Not Found Error|
|Q24.1|1786849426545246611|Not Found Error|
|Q17.6|1815075480401273327|Authorization Error|
|Q17.6|1815092339448136013|Authorization Error|
|Q17.6|1814836277281235345|Authorization Error|
|Q17.7|1814517429348815109|Authorization Error|
|Q17.8|1814748110100574250|Authorization Error|
|Q27.2|1815108708655149373|Authorization Error|
|Q27.2|1815108218856919386|Not Found Error|
|Q27.2|1815111685365235775|Not Found Error|
|Q27.2|1815109031373250961|Not Found Error|
|Q27.2|1815108867073671339|Not Found Error|
|Q27.4|1815100438439657713|Not Found Error|
|Q27.5|1815054000909168980|Not Found Error|
|Q27.5|1815089568045273223|Not Found Error|
|Q27.6|1815085684689870901|Authorization Error|
|Q27.6|1815081312635461770|Not Found Error|
|Q27.7|1814705804349743405|Not Found Error|
|Q27.7|1814991268054999268|Authorization Error|
|Q27.7|1815042704117842008|Authorization Error|
|Q27.8|1815046804565541258|Not Found Error|
|Q27.8|1815029358060355700|Not Found Error|

## Huit axes : ce qui a réellement été tenté et reste ouvert

|Axe|Requêtes principales|Résultat / manque|
|---|---|---|
|A avatar21juillet|Q01,Q06,Q10,Q17,Q20,Q27 ;L01,L02 ;19médias|Nouvelle couche de diffusion et contre-exemples ; pas de profil antérieur authentifié. Photos seules≠capture complète. Pas de date exacte du changement.|
|B Jeffro/cinqwallets|Q03,Q07,Q11,Q16,Q18 ;C01 ;deuxmédiasJeffro|Empreinte9Sxm nouvelle, pas signature190SOL/41.2M/20M/5/60/16SOL.|
|C Noah|Q02,Q03,Q09,Q14,Q16 ;C02 ;Viking|Capture6QFD antérieure ; pas source méthodologique/slot des quatre groupes ; relation≠propriété.|
|D comparateurs|Q05,Q08,Q12,Q21,Q24 ;MUDBONE|BARRON sources antérieures ; KLLARY non indépendant sans wallets ; ZOOMER/RETIREDI0 surtout contextes déjà connus. ContratsJOE/BILLY/WIF non résolus pour les swaps concernés, aucune jointure par ticker.|
|E équipe/origines|Q05,Q06,Q08,Q19,Q24 ;L01,L03 ;CTO2mai|Winig/BARRON contemporain ; pas preuve financière, concept/illustration/social/déploiement séparés ; parentkiki manquant.|
|F gagnants/sorties|Q13,Q18,Q25 ;L01 ;H3Qs|Source9Prm retrouvée avec clipWOLF ; H3Qs images sans signatures ; pas nouveau destinataireCoinbase/deBridge.|
|G petits comptes|Q09,Q14,Q15,Q23,Q27|Observations/contre-exemples publiés ; aucune nouvelle signature complète ; ne pas prendre l’audience actuelle pour celle de2024.|
|H Kekius|Q04,Q19,Q26|Nouveau témoinPERCY ; continuité créateur/programme≠continuitéDMAGA. Aucun nouveau fluxDMAGA/Kekius.|

Les axesD etH ne sont donc pas “résolus”. Les recherches d’adresses incluent plusieurs destinataires déjà connus du dépôt ; les résultats financiers connus ne sont pas réédités comme nouveaux.

## Requêtes exactes et pagination

Toutes les bornes since/until des requêtes sont UTC ; until est exclusif. Pourjuillet, ajouter1h pour Lisbonne ; décembre/janvier UTC=Lisbonne. Les compteurs ci-dessous sont des occurrences de résultats principaux, pas des posts distincts, et excluent includes.

### Q01

```text
(dmaga OR "dark maga" OR "laser eyes") since:2024-07-21_18:50:00_UTC until:2024-07-21_19:26:00_UTC -is:retweet
```

2 page(s), 18 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|18|`None`|`b26v89c19zqg8o3frqou3nwueigndyleve8e8wqzinmnx`|`64f50bf34a6d5ac4ae3fd46a95c1cdfd3cbb3549aae926d78296b45766e85e09`|
|2|0|`b26v89c19zqg8o3frqou3nwueigndyleve8e8wqzinmnx`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### C01

```text
QUOTES 1815291249102119198
```

1 page(s), 0 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|0|`None`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### C02

```text
QUOTES 1815372294426124565
```

1 page(s), 0 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|0|`None`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q02

```text
(from:Orkusx OR from:Pamp_It_ OR from:ogtraders_sol) (dmaga OR "dark maga" OR 6QFD OR 7GVC OR NxtX) since:2024-07-01 until:2024-10-01 -is:retweet
```

2 page(s), 6 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|6|`None`|`b26v89c19zqg8o3frqou3q19swtdi5ccflwr727ystbp9`|`c26fcbd91ab3fa5aff8ddca0a61f539656c60046c1870bd5205b926e8970f99f`|
|2|0|`b26v89c19zqg8o3frqou3q19swtdi5ccflwr727ystbp9`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q03

```text
("7GVC" OR "9Sxm" OR "A1UD" OR "6QFD" OR "H4mQ") since:2024-07-01 until:2024-11-01 -is:retweet
```

2 page(s), 2 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|2|`None`|`b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod`|`51a0b08785fd6a6434157831955733b4cfda0ab556848f1401e6e0fc8b86f561`|
|2|0|`b26v89c19zqg8o3frqou3s6ahjrz6s07jloj13mkeepod`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q04

```text
(DMAGA OR "dark maga") (KEKIUS OR "Kekius Maximus") since:2024-12-01 until:2025-02-01 -is:retweet
```

3 page(s), 36 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|20|`None`|`b26v89c19zqg8o3frr6sc54sz0ru2mwttlsgmjwbx9bwd`|`84b352515a7e919bc8ce078d48afdcb36c039f3cc198dcdb6924e278edabbbc8`|
|2|16|`b26v89c19zqg8o3frr6sc54sz0ru2mwttlsgmjwbx9bwd`|`b26v89c19zqg8o3frr6sbufz5ohxvi2sm7wburk1n04fx`|`bb22e065372f42c7c847c9c79adf4fce12dcc1955f0e0b5da0a00e0242bc91f8`|
|3|0|`b26v89c19zqg8o3frr6sbufz5ohxvi2sm7wburk1n04fx`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q05

```text
(from:sonder_crypto OR from:kikisknees OR from:Aristos_Revenge OR from:Barronsolana) (BARRON DMAGA OR wifejak OR "culture coins" OR developer) since:2024-05-01 until:2024-08-01 -is:retweet
```

2 page(s), 19 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|19|`None`|`b26v89c19zqg8o3fr5zembcgre4b5qgxb3kucqp8im1dp`|`5b1ca1b62c57a97b9ef78402e6594c3e7c15ed2d3ef136e0d5f431d7361e9af5`|
|2|0|`b26v89c19zqg8o3fr5zembcgre4b5qgxb3kucqp8im1dp`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q06

```text
(from:kikisknees OR from:ChrisWinig OR from:DarkMagaCoin) since:2024-07-21 until:2024-07-22 -is:retweet
```

3 page(s), 46 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|25|`None`|`b26v89c19zqg8o3frqou3pzrk5sn0xhtakghw59cxw9dp`|`58f052e3b88609ffe9c7ec8ea53c528049084e71a83e1bae7bcf6a54cbb4421c`|
|2|21|`b26v89c19zqg8o3frqou3pzrk5sn0xhtakghw59cxw9dp`|`b26v89c19zqg8o3frqotp1eqjhr5aehkv36oc8f3r7ji5`|`8450be7af86483a9d0095a855091fcb66563caea7dcf19e2446817732e43141e`|
|3|0|`b26v89c19zqg8o3frqotp1eqjhr5aehkv36oc8f3r7ji5`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q07

```text
(dmaga OR "dark maga") ("190" OR "41.2" OR "4120" OR "2000万" OR "60 SOL" OR "Jupiter") since:2024-07-13 until:2024-10-01 -is:retweet
```

2 page(s), 8 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|8|`None`|`b26v89c19zqg8o3frqou3q0ypuv83sm89dhuf9acna3y5`|`7af6ba307b14e1d694a0195768d2ff6b53cafa4f8eee822e6f06ba4fb6afef9a`|
|2|0|`b26v89c19zqg8o3frqou3q0ypuv83sm89dhuf9acna3y5`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q08

```text
(from:Barronsolana OR from:kikisknees) (contract OR "CA" OR takeover OR CTO OR developer OR launch OR deploy) since:2024-04-01 until:2024-07-23 -is:retweet
```

2 page(s), 11 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|11|`None`|`b26v89c19zqg8o3fr5zcxowp7q7fvw23ugq6yunps0vwd`|`7b15423c6ce74839c2d0494e1283e9a6dc88ee9319a7bc37adaa6bb06c3fede0`|
|2|0|`b26v89c19zqg8o3fr5zcxowp7q7fvw23ugq6yunps0vwd`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q09

```text
(dmaga OR "dark maga") (钱包 OR 地址 OR 捆绑 OR 老鼠仓 OR 内幕 OR 轉帳 OR 轉賬 OR "bundle" OR "redistributed") since:2024-07-13 until:2024-07-27 -is:retweet
```

4 page(s), 24 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|4|`None`|`b26v89c19zqg8o3frqou42sqa4h0x5cn2emzt6rx7epod`|`f0ca79de526fc25f3a83f405de8452cdf8a29f1e8e0e47ef9db8af90bda66646`|
|2|15|`b26v89c19zqg8o3frqou42sqa4h0x5cn2emzt6rx7epod`|`b26v89c19zqg8o3frqou3s4smfxqjwk0k0u8iti9zuyrh`|`6438525ae4babb1037c7d93871b41e90868b6406e1d0ea6c5f556be8c578121d`|
|3|5|`b26v89c19zqg8o3frqou3s4smfxqjwk0k0u8iti9zuyrh`|`b26v89c19zqg8o3frqou3q0ypuv83sm89dhuf9acna3y5`|`75db93b5215e35876da747017c549202bc74175833682c6fd6ec558d6b7d6c59`|
|4|0|`b26v89c19zqg8o3frqou3q0ypuv83sm89dhuf9acna3y5`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q10

```text
(elon OR musk) has:images since:2024-07-21_19:15:00_UTC until:2024-07-21_19:25:23_UTC -is:retweet
```

6 page(s), 90 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|25|`None`|`b26v89c19zqg8o3frqou3pyvefxiqwf64971bw2g6gygt`|`bee65e60dfcd9aa303f68a87cc36c9f6ff9df08d69b7c33989b17c30ab3b3b3c`|
|2|20|`b26v89c19zqg8o3frqou3pyvefxiqwf64971bw2g6gygt`|`b26v89c19zqg8o3frqou3pyvcydjmtzagk4t3qa8cg0ot`|`557e2d3b3c307927a79bd934db6a9d0fe37b21ce1144b429b30b7bb7e7379bb7`|
|3|15|`b26v89c19zqg8o3frqou3pyvcydjmtzagk4t3qa8cg0ot`|`b26v89c19zqg8o3frqou3pyvcx3ebwc6xfsajs0wsbdrx`|`c959677b7e4c72d55df3bbe5d11be8bf62a31fb07554c16488bac23c11360d58`|
|4|21|`b26v89c19zqg8o3frqou3pyvcx3ebwc6xfsajs0wsbdrx`|`b26v89c19zqg8o3frqou3pyvbfjd1wlg6xqhh4tekjfct`|`0d05ac199febd99f49750f624325c4d5b26a3da1c3255428fa431ad9dda074b1`|
|5|9|`b26v89c19zqg8o3frqou3pyvbfjd1wlg6xqhh4tekjfct`|`b26v89c19zqg8o3frqou3pyvbeh84xdqmvcpm1g8jjhq5`|`2c25053e51aad2014e04529766edd5e915c68780cdbe8447fb4589737aeba142`|
|6|0|`b26v89c19zqg8o3frqou3pyvbeh84xdqmvcpm1g8jjhq5`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q11

```text
("7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j" OR "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS" OR "A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J" OR "6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD" OR "H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y") since:2024-07-01 until:2024-11-01 -is:retweet
```

2 page(s), 6 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|6|`None`|`b26v89c19zqg8o3frqou3s6ahkuj7euw6lyza6b3vgb5p`|`1dfb9bb6075a67de5ff4c7df534cb65bdff8dde29f6654a6ef541a3bc8e30599`|
|2|0|`b26v89c19zqg8o3frqou3s6ahkuj7euw6lyza6b3vgb5p`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q12

```text
DMAGA BARRON since:2024-06-01 until:2024-08-01 -is:retweet
```

4 page(s), 72 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|23|`None`|`b26v89c19zqg8o3frqou42txft4a1a6padpwnad7y9unx`|`7018fac2ea59a886c96209d7768db243f158cd794b5e2de883d9366f544bc36c`|
|2|25|`b26v89c19zqg8o3frqou42txft4a1a6padpwnad7y9unx`|`b26v89c19zqg8o3frqou3uaf3jlxlxmcxlskpyw91y54t`|`feadb7730b1e69c8bb2b61e8514476f633ab52813037f5f851b10cb7406c3793`|
|3|24|`b26v89c19zqg8o3frqou3uaf3jlxlxmcxlskpyw91y54t`|`b26v89c19zqg8o3frqosuq825qw31pkcfo1u1oyxfbz3x`|`36bc54bec499fd0a24196788a0d7a02132ab7274a85d60177a0f96e846cc1aa0`|
|4|0|`b26v89c19zqg8o3frqosuq825qw31pkcfo1u1oyxfbz3x`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q13

```text
("H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc" OR "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra" OR "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq" OR "Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V" OR "0xb29826d809aa04d2ead6f2310d8965a45b87fa67" OR "0xb947bf7f409e998b28f8e218802fc9575c3c8c57") since:2024-07-01 until:2025-02-01 -is:retweet
```

4 page(s), 54 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|22|`None`|`b26v89c19zqg8o3frqrrs0exgqstfn7f2y763u4fzjf5p`|`23baa5e3cf705fa9ecd14be5b54468a86168764bcfe399cae0b97f3157da2e14`|
|2|22|`b26v89c19zqg8o3frqrrs0exgqstfn7f2y763u4fzjf5p`|`b26v89c19zqg8o3frqouivkt3wtk1zh0qnxg6ld0h0nst`|`75a49b15266910e91cebee88c7ad717cea49da6f1cf0ebb8ac8b41c36558eeb2`|
|3|10|`b26v89c19zqg8o3frqouivkt3wtk1zh0qnxg6ld0h0nst`|`b26v89c19zqg8o3frqou3u8mg1gikxknqg8z8w7ombzwd`|`0d745cefce49c15978a49d6b69153f438c64a905b2ca25509414a7d209d9ba8b`|
|4|0|`b26v89c19zqg8o3frqou3u8mg1gikxknqg8z8w7ombzwd`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### L01

```text
LOOKUP 1815054158367432804,1815861833682534700,1816153818574491968,1835606491786805678,1825526180616827284,1786151405025116298,1786151406958694513,1786151408850362623,1786151414621700268,1815104731871867096,1815105034453213564
```

1 page(s), 10 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|10|`None`|`None`|`e285875a30e05698bf3f65dac927c5bb36dcd9d4193c03c3e76fabca8e67f080`|

### Q14

```text
DMAGA (insider OR sniper OR wallets OR holders OR bundled OR split OR funded) since:2024-07-13 until:2024-07-23 -is:retweet
```

3 page(s), 39 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|24|`None`|`b26v89c19zqg8o3frqou3s5ebw9evpfyqgij019307ofx`|`cbe51c9149e47128b89f484a5fe990ed7d74cd4560b7ffc201ef2c3c9e969d6a`|
|2|15|`b26v89c19zqg8o3frqou3s5ebw9evpfyqgij019307ofx`|`b26v89c19zqg8o3frqotokfbl9b9ok2sqdqoqi8pqnnul`|`fc8a891ffe1c3c7ae814215b61a0e76a3e8f6a18cde9f59d45b6ab6675dbf507`|
|3|0|`b26v89c19zqg8o3frqotokfbl9b9ok2sqdqoqi8pqnnul`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q15

```text
(DMAGA OR "dark maga") (지갑 OR 내부자 OR 고래 OR 지분 OR "cartera" OR "billetera" OR "carteira" OR "portefeuille" OR "initié") since:2024-07-13 until:2024-10-01 -is:retweet
```

1 page(s), 0 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|0|`None`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q16

```text
(from:JeffroBTC OR to:JeffroBTC OR from:Noah_nftn OR to:Noah_nftn) since:2024-07-20 until:2024-07-25 -is:retweet
```

4 page(s), 47 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|24|`None`|`b26v89c19zqg8o3frqou3u9in8vo4705257md9u1x57ct`|`3af6f7c19b19b12e7b5d6d58a41617aa1dbacb8a3336420bc27d9b58edcefeb2`|
|2|19|`b26v89c19zqg8o3frqou3u9in8vo4705257md9u1x57ct`|`b26v89c19zqg8o3frqotov15ocmcsrwshmxku5ciahdvh`|`dda14a9d6da495fc6428473e61e866ef56a8b0b6f58a5aaf939f3862ea00cad1`|
|3|4|`b26v89c19zqg8o3frqotov15ocmcsrwshmxku5ciahdvh`|`b26v89c19zqg8o3frqotosvtzoyhjjizv2fw549r51oxp`|`9aedf0be5aaae1dc39397672a3efe7cf80798ee85da65ae2c916ebf4523404b9`|
|4|0|`b26v89c19zqg8o3frqotosvtzoyhjjizv2fw549r51oxp`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q17

```text
(pfp OR avatar OR "profile picture" OR "photo de profil" OR "foto de perfil" OR 头像 OR 頭像) since:2024-07-21_19:15:00_UTC until:2024-07-21_19:25:23_UTC -is:retweet
```

9 page(s), 173 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|23|`None`|`b26v89c19zqg8o3frqou3pyvegs7s0d3gx2b6z70bbe65`|`7e58a0af0fbb427f6f8e860d06883904106b78dcb6e7d8ba771b54bbed21c50f`|
|2|20|`b26v89c19zqg8o3frqou3pyvegs7s0d3gx2b6z70bbe65`|`b26v89c19zqg8o3frqou3pyvefxjthf7bqpbj4w220xa5`|`f76216e07313fe75693f9710074b109647cc301d74220d0af37e4abc40bb882d`|
|3|22|`b26v89c19zqg8o3frqou3pyvefxjthf7bqpbj4w220xa5`|`b26v89c19zqg8o3frqou3pyvcyldjrnie3cp9f6soz7nh`|`65e918243903f10344f51150bc8cb874cabdfa1f1da70494c23a34b009d7eeac`|
|4|23|`b26v89c19zqg8o3frqou3pyvcyldjrnie3cp9f6soz7nh`|`b26v89c19zqg8o3frqou3pyvcxy7nhsobdtj9rylh08l9`|`43e8a2024f0d460b1169dfec32c2589527ebf0372e4799b0bb743ea3e1c39d12`|
|5|25|`b26v89c19zqg8o3frqou3pyvcxy7nhsobdtj9rylh08l9`|`b26v89c19zqg8o3frqou3pyvcxb882rynkbuovqz79tvh`|`5352146b2e40e734bb2928f991918795bbe861720c857da6f8c6d370254964ce`|
|6|20|`b26v89c19zqg8o3frqou3pyvcxb882rynkbuovqz79tvh`|`b26v89c19zqg8o3frqou3pyvbg6l2w5meskc0r4wp2rnh`|`0c73125bfd9d4ea3fc9acfe19b4b83b7f22b523593a9913ec4c55fc6c93bb9b4`|
|7|19|`b26v89c19zqg8o3frqou3pyvbg6l2w5meskc0r4wp2rnh`|`b26v89c19zqg8o3frqou3pyvbf49p7amvc2ciutncaph9`|`091b8642d115c3ae16b21486ecfab712b0cfbdc78ecd30e1ff386af184627809`|
|8|21|`b26v89c19zqg8o3frqou3pyvbf49p7amvc2ciutncaph9`|`b26v89c19zqg8o3frqou3pyvbeonzks00i90meiwgcnst`|`4ecf5990f7906a8dab6418100cfc817aa4432b75f48599c541b255469ed68001`|
|9|0|`b26v89c19zqg8o3frqou3pyvbeonzks00i90meiwgcnst`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q18

```text
DMAGA (url:solscan.io/tx OR signature OR "tx hash" OR "transaction hash" OR 交易哈希 OR 交易签名) since:2024-07-13 until:2024-11-01 -is:retweet
```

1 page(s), 0 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|0|`None`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q19

```text
(from:kikisknees OR from:Aristos_Revenge OR from:DarkMagaCoin OR from:ChrisWinig OR from:sonder_crypto) (kekius OR maximus OR $KM) since:2024-12-01 until:2025-02-01 -is:retweet
```

1 page(s), 0 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|0|`None`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q20

```text
to:elonmusk (DMAGA OR "dark maga") since:2024-07-21_15:00:00_UTC until:2024-07-21_19:25:23_UTC -is:retweet
```

2 page(s), 5 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|5|`None`|`b26v89c19zqg8o3frqou3nvn5qfthk1sv4vhxiywlgnlp`|`10755ea5bb0725f3a3a54ff01465e750abce9152537156a8e159a8ed72c5719f`|
|2|0|`b26v89c19zqg8o3frqou3nvn5qfthk1sv4vhxiywlgnlp`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q21

```text
(BILLY OR WIF OR JOE) ("contract" OR "CA:") (from:dogwifcoin OR from:billyonsolana OR from:billysolcoin OR from:0xEnsp1re) since:2024-01-01 until:2024-08-01 -is:retweet
```

1 page(s), 0 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|0|`None`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q22

```text
from:cryptosymbiiote since:2024-08-19 until:2024-08-20 -is:retweet
```

2 page(s), 17 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|17|`None`|`b26v89c19zqg8o3frqrtvsf5g01rqihwk2axzy72q2agt`|`6927762203ac9b4fac4acc052dbff4ad9f989fd33fa29d3d437cd964b686118f`|
|2|0|`b26v89c19zqg8o3frqrtvsf5g01rqihwk2axzy72q2agt`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q23

```text
DMAGA (lang:ko OR lang:es OR lang:fr OR lang:pt) since:2024-07-13 until:2024-07-27 -is:retweet
```

6 page(s), 83 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|22|`None`|`b26v89c19zqg8o3frqou3ykgz2xd38r9ez1l63sg7gygt`|`7b62b54f91b239738d5cf2c82797201de02fa808b8319fd839207d8e77e57e07`|
|2|20|`b26v89c19zqg8o3frqou3ykgz2xd38r9ez1l63sg7gygt`|`b26v89c19zqg8o3frqou3u9tqa6wa4iw68sxy2bkbini5`|`d84a95fdac5c02df1e35ce005be78d1d64279f52ab965fdbb698da6e715287d4`|
|3|19|`b26v89c19zqg8o3frqou3u9tqa6wa4iw68sxy2bkbini5`|`b26v89c19zqg8o3frqou3q0yyz14az71nfgcqwy27u2d9`|`f71b2e0ed5fe2710032edec45ff08ea2d4a717acf83e70fc3b85907ceebbada2`|
|4|21|`b26v89c19zqg8o3frqou3q0yyz14az71nfgcqwy27u2d9`|`b26v89c19zqg8o3frqosujvdhsbwgird58bioz0z3o3nh`|`d5c813b18db2d08fbcad89b475cf7b178de61a545116efb8fe15f13da8e0791b`|
|5|1|`b26v89c19zqg8o3frqosujvdhsbwgird58bioz0z3o3nh`|`b26v89c19zqg8o3frqosudf3cq45dd89yv043enoxa1z1`|`259210e98bac52f5434c772a89e62728f95c75d975c3cfebe36e3357556411c4`|
|6|0|`b26v89c19zqg8o3frqosudf3cq45dd89yv043enoxa1z1`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### L02

```text
LOOKUP 1815370301128974544,1815158757942292949,1815191565121515817,1815355508959682732,1815409572686795158,1825526177957605756,1815407168700743950,1815105767600771266,1815105613107433608
```

1 page(s), 9 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|9|`None`|`None`|`b9b2456578c466a7b7d9db43d5d373f5c416d6b1b65458d4157edd55b2fdd6c0`|

### Q24

```text
(from:kikisknees OR from:Aristos_Revenge OR from:ChrisWinig) (wifejak OR barron OR prototype OR memecoin OR "pump.fun" OR launch) since:2024-04-01 until:2024-07-14 -is:retweet
```

2 page(s), 1 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|1|`None`|`b26v89c19zqg8o3fr5zemqag922j128o7wiv3cxnk15kt`|`9991ceee6544c25cc9a1b344d9e54b10e5c129a3d92662f90c314faa391d6d2d`|
|2|0|`b26v89c19zqg8o3fr5zemqag922j128o7wiv3cxnk15kt`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q25

```text
("0x86f99097c563e84dd5190f3e85f6a2988f1c47a5" OR "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b" OR "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL" OR "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E") since:2024-07-01 until:2025-02-01 -is:retweet
```

2 page(s), 3 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|3|`None`|`b26v89c19zqg8o3frqlvlf1ujro23ex38dgpiqgumhs3h`|`4b5c133c8203c13013d3dd8351b74137ebcc1e7c56ca0055fdb0bac855eb0c88`|
|2|0|`b26v89c19zqg8o3frqlvlf1ujro23ex38dgpiqgumhs3h`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q26

```text
("3oqARBNDr56L2oWQ9aR2QzS7FeTMEubd8J2v29wP5N58" OR "Go5rFkwKpTYGVck7emf4Uop81HBozmHHZfEhe2zJDY5u" OR "9dtGg97QAfxc2UF4LGaxLzYdB4MJpnNMK7Y2iUwGidoy") since:2024-12-01 until:2025-02-01 -is:retweet
```

2 page(s), 7 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|7|`None`|`b26v89c19zqg8o3frr6rwxccgpcfay0hvyxdrao2vogvx`|`6a289b2a178257d800233497f389226fe975f887c2f22d4156bfb6d09e41eb8e`|
|2|0|`b26v89c19zqg8o3frr6rwxccgpcfay0hvyxdrao2vogvx`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### Q27

```text
(DMAGA OR "dark maga") since:2024-07-21_15:00:00_UTC until:2024-07-21_20:00:00_UTC -is:retweet
```

9 page(s), 178 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|23|`None`|`b26v89c19zqg8o3frqou3pz62cxhke0qyot3p1ev5z7ul`|`887b711d153cdf5cd1e17b5f135d00e9dd9edeec4fd5f39165682e29875ab2a5`|
|2|25|`b26v89c19zqg8o3frqou3pz62cxhke0qyot3p1ev5z7ul`|`b26v89c19zqg8o3frqou3pz5zau4a16ujptu6a6v562kd`|`951149d76b45c9e940b680b7e45124afd54fe5f38e2098c311114b73bf224ab2`|
|3|21|`b26v89c19zqg8o3frqou3pz5zau4a16ujptu6a6v562kd`|`b26v89c19zqg8o3frqou3pyvkiugz5yybd3b0cfpp6dml`|`87ff7d171f8691b4c6c5d20304cd587f291dc8daf45390bf152dac799bd4321e`|
|4|23|`b26v89c19zqg8o3frqou3pyvkiugz5yybd3b0cfpp6dml`|`b26v89c19zqg8o3frqou3pyvhhtg6r8ltkk1fn4ziwygt`|`727c4bd8f723df10fc465c123f6e8efa5895ae99ac2ac32cc914b077e9d0e756`|
|5|22|`b26v89c19zqg8o3frqou3pyvhhtg6r8ltkk1fn4ziwygt`|`b26v89c19zqg8o3frqou3nwjp39ifq161a3ca2gh3b5od`|`c626c873ef3ee692f18893cdefce4d5667c56dce8621a3d95998937af8c21877`|
|6|24|`b26v89c19zqg8o3frqou3nwjp39ifq161a3ca2gh3b5od`|`b26v89c19zqg8o3frqou3nvndcemu0dfx2pdjl9x64vp9`|`2b33b2cf5b95f5b6ba17286ad3cd9383ab534b274b9d6579b7cc18e16528da29`|
|7|25|`b26v89c19zqg8o3frqou3nvndcemu0dfx2pdjl9x64vp9`|`b26v89c19zqg8o3frqou3nvckvqvf3o57wd6x7qbkbjwd`|`9a78a7fdc70a84794bc4011746374d03479785d4468c746be39200464f2ea66e`|
|8|15|`b26v89c19zqg8o3frqou3nvckvqvf3o57wd6x7qbkbjwd`|`b26v89c19zqg8o3frqou3nvc78cztaquujmlb84gh9uv1`|`9a575e3a7e3e189971da95e3d7c1d5790a733116a1420a043585db8eaddd0ae8`|
|9|0|`b26v89c19zqg8o3frqou3nvc78cztaquujmlb84gh9uv1`|`None`|`d2c052eab438f0669ddf856053cd0ae7d64d3f2cb419727531f076d8e5be2bcc`|

### L03

```text
LOOKUP 1786883817761820813,1808330517495836697,1808330515813929293,1875535395351314725,1875535213440192682
```

1 page(s), 5 résultats principaux au total ; dernière continuation : `None`.

|Page|Résultats|Token entrant|Token sortant|SHA256 payload extrait|
|---|---:|---|---|---|
|1|5|`None`|`None`|`ca7d65a6a9a368c6809b416ba28cb0ce1d845666bf321acbb6fd5bd261266054`|

## Web et archives : résultats réellement consultés

Trois WebSearch : `"DMAGA" "190" "2024"`, `"DMAGA" "BARRON" "developer" July 2024`, `"DMAGA" "wallet" "July 2024" insider`. Principalement bruit, reprisesGXZvX et pages explorateur/homonymes ; pas de nouvelle signature utilisable. Les résumés du moteur ne servent pas de preuve de transactions.

- ThreadReader : https://threadreaderapp.com/thread/1815291249102119198.html et https://threadreaderapp.com/thread/1825526155073700207.html : pages d’accueil/connexion, aucun fil récupéré. Aucun formulaire, unroll ou login soumis.
- WaybackCDX sur les URLs twitter.com etx.com exactes de `kikisknees/status/1815054158367432804` : résultat`[]`. Ce n’est pas une preuve d’absence sur toutes les archives, variantes d’URL ou captures. Le post répond NotFound viaX ; aucun texte/image reconstitué.
- Article contemporain https://www.chaincatcher.com/article/2134682 (22juillet2024) : contexte avatar/Biden déjà connu, pas nouvelle adresse ou signature. Heure de page20:01:24 sans fuseau explicite : laissée littérale, pas convertie arbitrairement.

## Chronologie minute par minute : couche d’observations, pas heure du changement

21juillet2024,16:00–21:00Lisbonne =15:00–20:00UTC. Q27 paginé jusqu’au bout fournit la couche générale “DMAGA/DarkMAGA” ; Q01/Q10/Q17/Q20 ajoutent les mots du profil et les messages àMusk. Le tableau suivant compte **uniquement les résultats principaux de Q27**, dédupliqués parID. `0` signifie aucun résultat de CETTE requête, non absence de publications surX. Une ligne ne prouve pas que son média a été vu ; seuls les fichiers du MEDIA.csv l’ont été. Un ID du corpus connu reste un repère, jamais une nouveauté.

|Minute Lisbonne|Minute UTC|Posts Q27|IDs des observations de cette minute|
|---|---|---:|---|
|16:00|15:00|0|—|
|16:01|15:01|0|—|
|16:02|15:02|0|—|
|16:03|15:03|0|—|
|16:04|15:04|0|—|
|16:05|15:05|0|—|
|16:06|15:06|0|—|
|16:07|15:07|0|—|
|16:08|15:08|0|—|
|16:09|15:09|0|—|
|16:10|15:10|0|—|
|16:11|15:11|0|—|
|16:12|15:12|0|—|
|16:13|15:13|1|N:1815042353951891574|
|16:14|15:14|0|—|
|16:15|15:15|1|N:1815042820282908870|
|16:16|15:16|0|—|
|16:17|15:17|0|—|
|16:18|15:18|1|N:1815043617377144988|
|16:19|15:19|0|—|
|16:20|15:20|0|—|
|16:21|15:21|0|—|
|16:22|15:22|0|—|
|16:23|15:23|0|—|
|16:24|15:24|1|N:1815045232968245704|
|16:25|15:25|1|N:1815045447490396637|
|16:26|15:26|0|—|
|16:27|15:27|0|—|
|16:28|15:28|1|K:1815046174056837320|
|16:29|15:29|1|N:1815046522066661717|
|16:30|15:30|0|—|
|16:31|15:31|1|N:1815046916473782337|
|16:32|15:32|2|N:1815047189934059591 N:1815047244082446835|
|16:33|15:33|0|—|
|16:34|15:34|2|N:1815047649864601923 N:1815047700556959825|
|16:35|15:35|0|—|
|16:36|15:36|1|N:1815048171522757059|
|16:37|15:37|2|N:1815048355182936251 N:1815048472812216539|
|16:38|15:38|0|—|
|16:39|15:39|0|—|
|16:40|15:40|1|N:1815049127148851630|
|16:41|15:41|0|—|
|16:42|15:42|3|N:1815049622156378557 N:1815049693912588308 N:1815049756957085936|
|16:43|15:43|1|N:1815049993004142962|
|16:44|15:44|0|—|
|16:45|15:45|0|—|
|16:46|15:46|1|N:1815050639073808664|
|16:47|15:47|2|N:1815050898667712774 N:1815050931387383967|
|16:48|15:48|0|—|
|16:49|15:49|0|—|
|16:50|15:50|0|—|
|16:51|15:51|0|—|
|16:52|15:52|1|N:1815052136616702106|
|16:53|15:53|0|—|
|16:54|15:54|1|N:1815052783042679288|
|16:55|15:55|1|K:1815052979608653919|
|16:56|15:56|0|—|
|16:57|15:57|1|N:1815053521718321235|
|16:58|15:58|0|—|
|16:59|15:59|1|N:1815053909930709320|
|17:00|16:00|1|N:1815054374982324401|
|17:01|16:01|2|N:1815054381823221968 N:1815054496415813666|
|17:02|16:02|0|—|
|17:03|16:03|1|N:1815055055076159733|
|17:04|16:04|1|N:1815055334165360643|
|17:05|16:05|0|—|
|17:06|16:06|0|—|
|17:07|16:07|0|—|
|17:08|16:08|0|—|
|17:09|16:09|0|—|
|17:10|16:10|1|N:1815056683325890788|
|17:11|16:11|0|—|
|17:12|16:12|0|—|
|17:13|16:13|0|—|
|17:14|16:14|0|—|
|17:15|16:15|1|N:1815057957798735899|
|17:16|16:16|1|N:1815058155799212109|
|17:17|16:17|2|N:1815058630892572851 N:1815058631785615694|
|17:18|16:18|0|—|
|17:19|16:19|1|N:1815058914188402811|
|17:20|16:20|1|N:1815059189976183095|
|17:21|16:21|0|—|
|17:22|16:22|1|N:1815059780924272864|
|17:23|16:23|0|—|
|17:24|16:24|0|—|
|17:25|16:25|0|—|
|17:26|16:26|0|—|
|17:27|16:27|0|—|
|17:28|16:28|0|—|
|17:29|16:29|0|—|
|17:30|16:30|1|N:1815061835852185784|
|17:31|16:31|0|—|
|17:32|16:32|0|—|
|17:33|16:33|0|—|
|17:34|16:34|1|N:1815062796767244490|
|17:35|16:35|0|—|
|17:36|16:36|0|—|
|17:37|16:37|0|—|
|17:38|16:38|1|N:1815063915140645143|
|17:39|16:39|0|—|
|17:40|16:40|0|—|
|17:41|16:41|0|—|
|17:42|16:42|0|—|
|17:43|16:43|0|—|
|17:44|16:44|0|—|
|17:45|16:45|0|—|
|17:46|16:46|0|—|
|17:47|16:47|0|—|
|17:48|16:48|0|—|
|17:49|16:49|0|—|
|17:50|16:50|0|—|
|17:51|16:51|0|—|
|17:52|16:52|0|—|
|17:53|16:53|0|—|
|17:54|16:54|0|—|
|17:55|16:55|1|N:1815067977684832412|
|17:56|16:56|0|—|
|17:57|16:57|0|—|
|17:58|16:58|0|—|
|17:59|16:59|1|N:1815069094045168123|
|18:00|17:00|1|N:1815069292594864419|
|18:01|17:01|0|—|
|18:02|17:02|0|—|
|18:03|17:03|0|—|
|18:04|17:04|0|—|
|18:05|17:05|0|—|
|18:06|17:06|0|—|
|18:07|17:07|1|N:1815071063036055639|
|18:08|17:08|0|—|
|18:09|17:09|0|—|
|18:10|17:10|0|—|
|18:11|17:11|0|—|
|18:12|17:12|0|—|
|18:13|17:13|0|—|
|18:14|17:14|1|N:1815072845552046325|
|18:15|17:15|1|N:1815073076096258386|
|18:16|17:16|0|—|
|18:17|17:17|0|—|
|18:18|17:18|0|—|
|18:19|17:19|1|N:1815074257069547949|
|18:20|17:20|0|—|
|18:21|17:21|0|—|
|18:22|17:22|0|—|
|18:23|17:23|0|—|
|18:24|17:24|0|—|
|18:25|17:25|0|—|
|18:26|17:26|0|—|
|18:27|17:27|0|—|
|18:28|17:28|0|—|
|18:29|17:29|0|—|
|18:30|17:30|0|—|
|18:31|17:31|0|—|
|18:32|17:32|0|—|
|18:33|17:33|0|—|
|18:34|17:34|1|N:1815077860953948304|
|18:35|17:35|0|—|
|18:36|17:36|0|—|
|18:37|17:37|0|—|
|18:38|17:38|0|—|
|18:39|17:39|0|—|
|18:40|17:40|0|—|
|18:41|17:41|1|N:1815079714647642170|
|18:42|17:42|0|—|
|18:43|17:43|0|—|
|18:44|17:44|0|—|
|18:45|17:45|0|—|
|18:46|17:46|0|—|
|18:47|17:47|0|—|
|18:48|17:48|0|—|
|18:49|17:49|1|N:1815081735761154154|
|18:50|17:50|0|—|
|18:51|17:51|0|—|
|18:52|17:52|0|—|
|18:53|17:53|0|—|
|18:54|17:54|1|N:1815082897822634137|
|18:55|17:55|0|—|
|18:56|17:56|0|—|
|18:57|17:57|0|—|
|18:58|17:58|0|—|
|18:59|17:59|0|—|
|19:00|18:00|0|—|
|19:01|18:01|1|N:1815084709422191043|
|19:02|18:02|0|—|
|19:03|18:03|0|—|
|19:04|18:04|1|N:1815085535938908320|
|19:05|18:05|0|—|
|19:06|18:06|0|—|
|19:07|18:07|1|N:1815086175155048872|
|19:08|18:08|0|—|
|19:09|18:09|2|N:1815086710704980248 N:1815086713502667190|
|19:10|18:10|1|N:1815087028259725783|
|19:11|18:11|1|N:1815087260846743880|
|19:12|18:12|1|N:1815087429126066682|
|19:13|18:13|0|—|
|19:14|18:14|0|—|
|19:15|18:15|1|K:1815088124193579253|
|19:16|18:16|1|N:1815088433615995019|
|19:17|18:17|1|K:1815088727250858444|
|19:18|18:18|0|—|
|19:19|18:19|0|—|
|19:20|18:20|0|—|
|19:21|18:21|0|—|
|19:22|18:22|2|N:1815089890406658302 N:1815089901525966902|
|19:23|18:23|0|—|
|19:24|18:24|0|—|
|19:25|18:25|0|—|
|19:26|18:26|0|—|
|19:27|18:27|0|—|
|19:28|18:28|0|—|
|19:29|18:29|0|—|
|19:30|18:30|0|—|
|19:31|18:31|0|—|
|19:32|18:32|0|—|
|19:33|18:33|0|—|
|19:34|18:34|0|—|
|19:35|18:35|0|—|
|19:36|18:36|1|N:1815093629662220415|
|19:37|18:37|0|—|
|19:38|18:38|0|—|
|19:39|18:39|0|—|
|19:40|18:40|1|N:1815094431152029711|
|19:41|18:41|1|N:1815094810354860035|
|19:42|18:42|1|N:1815095033756029268|
|19:43|18:43|0|—|
|19:44|18:44|0|—|
|19:45|18:45|0|—|
|19:46|18:46|1|K:1815095993186328850|
|19:47|18:47|0|—|
|19:48|18:48|0|—|
|19:49|18:49|1|N:1815096750715138111|
|19:50|18:50|2|N:1815096959406842221 N:1815096998669795549|
|19:51|18:51|0|—|
|19:52|18:52|0|—|
|19:53|18:53|0|—|
|19:54|18:54|0|—|
|19:55|18:55|0|—|
|19:56|18:56|0|—|
|19:57|18:57|0|—|
|19:58|18:58|0|—|
|19:59|18:59|0|—|
|20:00|19:00|0|—|
|20:01|19:01|0|—|
|20:02|19:02|0|—|
|20:03|19:03|0|—|
|20:04|19:04|0|—|
|20:05|19:05|0|—|
|20:06|19:06|0|—|
|20:07|19:07|0|—|
|20:08|19:08|0|—|
|20:09|19:09|0|—|
|20:10|19:10|0|—|
|20:11|19:11|0|—|
|20:12|19:12|0|—|
|20:13|19:13|0|—|
|20:14|19:14|0|—|
|20:15|19:15|0|—|
|20:16|19:16|0|—|
|20:17|19:17|0|—|
|20:18|19:18|0|—|
|20:19|19:19|0|—|
|20:20|19:20|0|—|
|20:21|19:21|1|N:1815104731871867096|
|20:22|19:22|1|N:1815105034453213564|
|20:23|19:23|0|—|
|20:24|19:24|1|N:1815105518316527875|
|20:25|19:25|0|—|
|20:26|19:26|0|—|
|20:27|19:27|2|N:1815106256635564392 N:1815106365108433270|
|20:28|19:28|0|—|
|20:29|19:29|1|N:1815106770140029061|
|20:30|19:30|1|N:1815107027892334987|
|20:31|19:31|2|N:1815107230301086179 N:1815107380339965953|
|20:32|19:32|7|N:1815107516059308477 N:1815107549903135205 N:1815107560405704851 N:1815107570329416084 N:1815107641192120343 K:1815107681189015632 N:1815107702508634622|
|20:33|19:33|3|K:1815107751745601643 N:1815107889360433242 N:1815107973154513336|
|20:34|19:34|3|N:1815107993366900786 N:1815108106281714179 N:1815108148690055641|
|20:35|19:35|1|N:1815108354911490121|
|20:36|19:36|1|N:1815108690648727726|
|20:37|19:37|4|N:1815108761511707118 N:1815108898577363267 N:1815108933398536496 N:1815108969725141147|
|20:38|19:38|3|K:1815109035915444246 N:1815109052998770767 N:1815109130786607416|
|20:39|19:39|3|N:1815109362236411915 N:1815109386798260648 N:1815109401944183188|
|20:40|19:40|3|K:1815109519543771574 N:1815109521314091394 N:1815109711718429047|
|20:41|19:41|4|N:1815109744123609145 N:1815109784913232187 N:1815109849916592614 N:1815109959484371200|
|20:42|19:42|4|N:1815110081861861838 N:1815110098035028173 N:1815110121741246879 N:1815110216288968767|
|20:43|19:43|6|N:1815110297222332847 N:1815110327979364676 N:1815110341459644416 N:1815110369335279847 N:1815110418270245039 N:1815110495000547553|
|20:44|19:44|5|N:1815110496762351836 N:1815110540533895674 N:1815110543826624713 N:1815110563292414354 N:1815110576781046033|
|20:45|19:45|5|N:1815110873809043759 N:1815110878640943369 N:1815110941912203694 N:1815110958337102236 N:1815110976670162991|
|20:46|19:46|6|N:1815111016398623078 N:1815111098170786141 N:1815111171415961754 N:1815111200017125776 N:1815111208846176438 N:1815111242362523800|
|20:47|19:47|0|—|
|20:48|19:48|3|N:1815111547426930809 N:1815111584420618421 N:1815111694063898727|
|20:49|19:49|3|N:1815111907889619321 N:1815111941267841116 N:1815111998952415554|
|20:50|19:50|0|—|
|20:51|19:51|1|N:1815112263218426111|
|20:52|19:52|3|N:1815112653486149758 N:1815112676324094431 N:1815112713871192275|
|20:53|19:53|4|N:1815112797098836110 N:1815112883505967446 N:1815112901721510394 K:1815112990242619502|
|20:54|19:54|1|N:1815113082319880396|
|20:55|19:55|7|N:1815113277845786991 N:1815113367645802744 N:1815113383575998689 N:1815113404220154189 N:1815113468908851333 N:1815113496050512003 N:1815113513595269472|
|20:56|19:56|1|N:1815113584160157858|
|20:57|19:57|3|N:1815113826406396413 N:1815113871075533087 N:1815113988671250702|
|20:58|19:58|3|N:1815114074801238151 N:1815114106028085334 N:1815114221686009930|
|20:59|19:59|6|N:1815114289885434078 N:1815114343760932924 N:1815114350824501462 N:1815114437931696405 N:1815114443447300301 N:1815114444965663121|

K=ID déjà couvert, N=ID non couvert au départ (pas automatiquement une découverte). Table limitée au périmètre lexical, pas reconstitution complète du réseau social ni horodatage de l’upload média.

### Contrôle ancien, non réannoncé : les deux IDs RETIREDI0

[1815088124193579253](https://x.com/dissident42069/status/1815088124193579253) est le post de **@dissident42069 à19:15:06Lisbonne/18:15:06UTC**, « sold80% of our RETIREDI0 and rotated into$dmaga ». [1815088727250858444](https://x.com/dissident42069/status/1815088727250858444) est **une autre publication du même auteur, réponse à19:17:29Lisbonne/18:17:29UTC**, parent1815084272098697611, « Time to rotate… ». Ni mêmeID ni repost de l’un par l’autre. La réponse ne doit pas être datée19:15:06. Cette résolution était déjà présente dans la passe2 : les deux IDs sont exclus du DELTA ; Q27 les confirme sans créer un huitième résultat.

### Bornes image/profil

20:21:05Lisbonne FrankButcher81 : portraitMusk isolé ;20:22:17 onthepickle :Trump ;20:24:35FlipCrypt : portrait400×400 ;20:25:12MonetizedLiving : portraitcirculaire. Aucun n’est une capture complète du profil. La borne de comparaison connue reste **20:25:23Lisbonne/19:25:23UTC**, realjohnnewburg1815105812076904904, pas une première mondiale prouvée ni l’heure exacte du changement. Le parentkiki de17:00:08Lisbonne/16:00:08UTC reste indisponible. Aucune “communication privée” extrapolée.

## Limites principales et arrêt

1. Exhaustivité deX impossible à garantir : index de recherche, posts supprimés/privés, includes tronqués, champs absents, exclusions de reposts et choix lexicaux. Fin de token signifie fin de résultats accessibles pour une requête précise, pas fin de toutes les sources.
2. Sept résultats ne sont pas sept preuves financières. Les nouveaux posts peuvent être reprises de rumeurs ; les bots ne sont pas nécessairement deux témoins indépendants. Le graphe sépare relations natives et annotations dérivées.
3. Les captures de trackers n’établissent pas de signatures ni de montants natifs exacts. Certaines dates sont relatives ou sans fuseau ; les adresses tronquées restent telles quelles dans les observations, avec résolution canonique ancienne explicitement signalée.
4. Aucun RPC/explorateur on-chain nouveau ni source de prix historique vérifiée dans cette passe. Le handoff décrit les tests à exécuter séparément, pas des résultats obtenus.
5. La vidéo a été échantillonnée en5frames, pas lue image par image. Les autres médias des posts archivés sont listés parURL mais n’ont pas tous été téléchargés. JOE/BILLY/WIF et certaines chaînesEVM restent non résolus : aucune invention de contrat.
6. Aucun contact de compte, post/brouillon, PR/commit, donnée privée, identification civile ou routine. Mission arrêtée après fichiers et vérifications locales.

## Inventaire de livraison et intégrité

Six autres livrables et24fichiers média ci-dessous. Ce fichier de couverture est exclu de son propre inventaire pour éviter un hash autoréférent. Le checksum du ZIP est externe : `/workspace/dmaga_pass3.zip.sha256`.

|Chemin relatif|Octets|SHA256|
|---|---:|---|
|`DMAGA_PASS3_CLAUDE_HANDOFF.md`|12512|`83bf2e9b7698ab85d07a77376e5e127d6d4af47e417e55d482000ec152423def`|
|`DMAGA_PASS3_DELTA.jsonl`|721968|`00a92ab53939bda2a225caec3997fb0481aae1eb493e14e282bf1948a391742f`|
|`DMAGA_PASS3_FINDINGS.md`|24724|`ddb0cae1741610221181d55da08002b07dfdf422c652dea5e10f7df4b7a5e11e`|
|`DMAGA_PASS3_MEDIA.csv`|15372|`fb624ba575add381ed133a28e7cb1f2d0bc99db7708e7795ed09ad91ef2edf95`|
|`DMAGA_PASS3_SOURCE_GRAPH.csv`|53073|`2b3d49ebf9e87524329474c21b32926e52fe1cc70d7f3fb45d341e4d91512460`|
|`DMAGA_PASS3_WALLET_LEADS.csv`|4818|`638b046af5bd61624ccb1ec5a57848f77fb061d0979e7acf9b73854d62a56146`|
|`media/1786151408850362623_3-1786150063548342272.jpg`|84551|`c3aab48f0e5e5576e27aa7da124d07d36b68eed9a772240fc7399bfd560618a5`|
|`media/1786151408850362623_3-1786150104988012545.jpg`|3587943|`1e01bb75cce9d62a59527abeae74ec96fd828a56c7eb13180f4b5141fdc99b9c`|
|`media/1786151408850362623_3-1786150138043404288.jpg`|546120|`3858a6e84bba8a67e19cdebff9d0fada170b24f778442e16a240a78e91989633`|
|`media/1786151408850362623_3-1786150354763075584.jpg`|105353|`038cbc8621bcd8b5984db4cd9a12d799eb0c35808f3510504f7846751f01a4ce`|
|`media/1815088433615995019_3-1815088429795016704.jpg`|98919|`9891d69095cf7ee8f246940887c5a4d6b07f9fea171091f65b21454e073681a4`|
|`media/1815094810354860035_3-1815094675495157760.jpg`|111030|`c1a2088f12a8c91437da53acfbabb8cfdef4f64b3645810a257c8d925842ff3e`|
|`media/1815094810354860035_3-1815094675507699712.jpg`|89712|`e0cee79437976fdec1ce34ce76d2fe1111e4e8e0babdf0c56e1034b75802ab8e`|
|`media/1815104731871867096_3-1815104727970914304.jpg`|64170|`d2baea648503e8ffc759531307fce00424fd8ca62f6affb46e34185d8b949b6c`|
|`media/1815105034453213564_3-1815105031143653376.jpg`|105387|`60fb616e309c8cfe9359e692b564c58c8d471f7e7a0e554677009b455e84cc6f`|
|`media/1815105613107433608_3-1815105479699279872.jpg`|289154|`52b5c72a44d2418106d8d3189c986411dbade61cba01f650491878fb92d0273c`|
|`media/1815105767600771266_3-1815105763842392064.jpg`|65415|`0c871de183df40a5908a4aa456f8c2e681f4dee34845ece0720b48e49f732693`|
|`media/1815291249102119198_3-1815288876430426112.jpg`|105385|`ee270a37efe721310e43db3bbf1864d6ce94b521ecd05137f12c36fe46093b5a`|
|`media/1815291249102119198_3-1815288959033020416.jpg`|126498|`58a1990807e006c008cb09acf2a86c7eee312a4ef375d48e21f0ad65acde079e`|
|`media/1815370301128974544_3-1815370118731280385.jpg`|406266|`8eace954222fc20badc6c4e3d71bfa31853f3cfd236a96435014292b0a87b01c`|
|`media/1815407168700743950_3-1815406599332126720.jpg`|182795|`fe7c51436bfa220596876c6df0fa8901ba3b61ffe72a4082e2052a79f2410280`|
|`media/1815494781390262663_3-1815494360919584768.jpg`|101942|`8a226d56eb11d4a53feb40d6ba951cd99850431d9b8253d51828ea4296152cf8`|
|`media/1825526180616827284_7-1825525900378550272.mp4`|1397394|`14254f1d509d6b8a27a79fbe7916b9d71d22f9b2a05dc0f4c30d92351ab5c78d`|
|`media/1825526180616827284_frame_00.png`|481806|`5e919da32e304a76b3d1746be7d08d9c4ee1ba7c638fc7bb705d3244f8b8e52d`|
|`media/1825526180616827284_frame_05.png`|501734|`42ec8d0323a0b8b1145fe1550ed9370c2bbbf901c3ad3b66027e992e689af59f`|
|`media/1825526180616827284_frame_10.png`|495463|`65ee30d57ecf119c6509917183fabb696d12d4af655d832210e3ac54aa5b4628`|
|`media/1825526180616827284_frame_15.png`|503444|`1d8bcb7f612323d5c8c8278f2849f7b449df93079b8cbed46b451dc48fa6497d`|
|`media/1825526180616827284_frame_19.png`|509309|`538768a6a575d2447b6a09d042c1cf65eb798ec467da030e8dd637db64088720`|
|`media/1835606491786805678_3-1835606480973877248.jpg`|138766|`61d79855ee8f4c52f1078d6306db2529342377b7a170115a53b58e149a19d27b`|
|`media/1835606491786805678_3-1835606480978132993.jpg`|148018|`585594c4e84bc23db64868663c68c33b432f266898900caa24158c10aa0c00ee`|

Contrôles exécutés : JSONL analysable316IDs uniques, disjoints des6121IDs archivés et8116couverts ; metadata et auteurID/handle présents ; zéro discordance Snowflake à la seconde ;9adresses complètes Base58/hex syntaxiquement valides, sans signature inventée ;19originaux+5frames hachés et vus ; sept fichiers à la racine. Le ZIP est testéCRC puis extrait dans un répertoire temporaire et comparé octet pour octet aux31fichiers de livraison. Le checksum final du ZIP est fourni séparément.
