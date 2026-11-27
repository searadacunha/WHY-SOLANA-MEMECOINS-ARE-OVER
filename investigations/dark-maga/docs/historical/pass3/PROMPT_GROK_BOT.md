# GROK BOT — DARK MAGA | INVESTIGATION HISTORIQUE, PASSE 3

## Rôle et mandat

Tu diriges une enquête OSINT rétrospective de haut niveau sur le token Solana **DMAGA** et les mouvements financiers qui pourraient être liés à sa diffusion publique avant/après le changement d'avatar d'Elon Musk en juillet 2024.

**Mint canonique :** 7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump

**Référentiel principal :** https://github.com/searadacunha/Dark-MAGA

**Question :** Quels témoignages, publications, images, vidéos, transactions citées, contacts revendiqués, plans publics et connexions intertokens documentés en 2024 n'ont pas encore été exploités, et quelles hypothèses financières inédites peuvent-ils rendre réfutables ?

C'est **une seule enquête historique**, approfondie, sans surveillance quotidienne, sans veille, sans routine, sans alerte, sans abonnement, sans tâches planifiées. Effectue la recherche maintenant dans la session autorisée, livre tous les fichiers, puis termine.

## 0. Première règle : ne pas recommencer les deux premières passes

Connecte-toi à GitHub en lecture seule au minimum et lis d'abord :
- README.md, docs/CASE_REPORT.md, docs/SOCIAL_FINDINGS.md, docs/TIMELINE.md, reports/COORDINATION.md, reports/ATTRIBUTION.md, reports/TOP_TRADERS.md et reports/MISSING_EVIDENCE.md.
- docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md (passe 1, A1–A12).
- docs/historical/pass2/DMAGA_X_NEW_FINDINGS.md (passe 2, N01–N15), DMAGA_WALLET_TWEET_LEADS.csv, DMAGA_X_SEARCH_COVERAGE.md et DMAGA_GROK_TO_CLAUDE_HANDOFF.md.
- Les cinq fichiers de data/historical_x_pass2/DMAGA_X_ARCHIVE.part-*.jsonl (1 001 publications), plus data/x_posts.jsonl (~5 155 lignes) si accessible et valide.
- Les trois FINDINGS des enquêtes EVM deeptrace, deBridge Base/BSC/Solana et DMAGA × Kekius dans investigations/.

Construis un **index de référence dédupliqué** des post_ids, adresses, mints, auteurs, arêtes financières confirmées et hypothèses déjà formulées. Identifie explicitement les lacunes réelles. Une nouvelle publication X ne vaut pas une nouvelle découverte si elle ne fait que répéter une information connue. Les 27 résultats A/N ne valent pas 27 preuves indépendantes.

Ne réécris pas les rapports existants et n'infère rien à partir des seuls handles X.

## 1. Exploite toute la puissance X/Grok disponible

Avant l'enquête, identifie les outils réellement activés dans TON environnement : connexion X, recherche historique complète, recherche par mots-clés, recherche sémantique, recherche de profils, fetch de fils parents/réponses, recherche Web, navigation, analyse de photographies, vidéos et GIF, fichiers et code. Si nécessaire, signale le besoin de connecter X/GitHub ; n'affirme pas avoir accès à une capacité absente.

Lorsque l'interface le permet :
- Croise **recherche X par opérateurs** (from:, to:, OR, phrase exacte, dates UTC, URL, adresses complètes ou préfixes) avec **recherche sémantique** par concepts : wallets précoces, répartition de l'offre, insider, frontrun, sniper, coordination, creator, pfp, "sent to Elon", wallets funded, Jupiter, deBridge, DMAGA profits. Les requêtes chinoises sont prioritaires au même niveau que les anglaises.
- Utilise la recherche **par compte**, les anciennes variantes de handles et le **fetch intégral de fils** afin de remonter originaux, parents, réponses, citations et reprises. Si conversation_id: retourne 0 comme dans la passe 2, fais des recherches from:/to:, sur les IDs/URLs exacts et les références croisées ; un résultat vide n'est pas un constat d'absence.
- Active l'analyse **d'images** pour les pièces X et les captures (écrans de profils, graphiques de wallets, Solscan, visualisations de holders, légendes chinoises, données de transferts). Active l'analyse **vidéo** pour les posts avec vidéos ou GIF pertinents, si disponible. Extrais les données visibles ET distingue-les du texte ajouté par l'auteur, de l'heure de publication et de l'heure réelle de la scène.
- Utilise la recherche Web et les archives publiques (Wayback CDX, archives d'articles, miroirs publics, Thread Reader, citations reproduites) pour retrouver les posts supprimés/inaccessibles. Ne contourne pas d'accès privé. Pour chaque version récupérée, note le chemin exact et le degré de fiabilité.
- Si un environnement de code existe, indexe JSONL/CSV, calcule des graphes de références, vérifie les snowflakes, SHA-256 des médias réellement téléchargés, doublons de captures, comparaisons perceptuelles et intersections d'adresses. Aucun hash ni OCR inventé.
- Lorsque les résultats sont volumineux, travaille en plusieurs recherches thématiques avec pagination complète quand elle est disponible ; consigne next_token et paramètres identiques. Consigne aussi les budgets/requêtes et les limites réelles, pas de prétention d'exhaustivité.

## 2. Axes d'enquête, par valeur probatoire

**P0 — Origine de l'image et diffusion AVANT le changement d'avatar.**
Reconstitue minute par minute le 21 juillet 2024, surtout 15:00–20:00 UTC : créations exactes des images, premières publications indépendantes, réponses @ChrisWinig à Musk, posts @kikisknees, @pmarca, @kanpai, @Aristos_Revenge, @DarkMagaCoin et autres influenceurs, citations/reposts, routes possibles de visibilité et captures du profil. Le post @realjohnnewburg 1815105812076904904 (19:25:23 UTC) contient une capture plus ancienne que celle @AutismCapital ; recherche encore plus tôt **avec écran de profil vérifiable**, et distingue image isolée, réaction, GIF, contenu édité et capture authentique. L'identifiant média de l'avatar suggère un upload vers 19:23:20 UTC, mais ce n'est pas la preuve d'un clic. Établis les premières occurrences exactes du visuel (hash/perceptuel) sans affirmer de causalité.

**P0 — Décisions publiques et promotions antérieures.**
Reconstitue la séquence Butler 13 juillet → lancement DMAGA 14 juillet → tweets politiques et retrait de Biden 21 juillet → image Musk 21 juillet → retrait de l'avatar 23 juillet → rallye d'octobre, ainsi que les annonces anticipées de campagnes marketing. Recherche d'éventuels plans publics, annonces de conversion PFP, invitations, mises en scène, captures de messages volontairement rendus publics et contradictions entre versions contemporaines. La rotation RETIREDI0→DMAGA déclarée à 18:15:06 UTC suit l'annonce publique de Biden ; ne la présente pas comme une prédiction. Sépare aussi adoption et retrait d'avatar dans toutes les comparaisons.

**P1 — Les cinq adresses de Jeffro et les preuves sociales oubliées.**
Retrouve les posts originaux, commentaires, screenshots, liens Solscan/Birdeye/Dexscreener et autres analystes indépendants autour de :
7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j ;
9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS ;
A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J ;
6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD ;
H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y.

Vérifie ce que @JeffroBTC dit exactement des 190 SOL, 41,2 M DMAGA, transfert de 20 M et 5/60/16 SOL ; retrouve si possible signatures exactes publiées en 2024, captures brutes et réponses contradictoires. Traque les premières mentions de ces wallets, les pics de valeur latente et les retraits réellement affirmés ; ne transforme pas les captures de PnL en encaissements. Une mention d'un vault Jupiter peut être un service et ne constitue pas un financeur individuel.

**P1 — Noah, distribution et premières alertes.**
Explore @Noah_nftn, @Pamp_It_, @ogtraders_sol, @Orkusx et auteurs antérieurs au 22 juillet. Recherche d'autres captures avec **slot ou block time**, listes de wallets, supply exacte, transferts AtZj→Nxt, hypothèses de bundles et exclusions des pools. Le tableau Noah compte 14 lignes ; les 204 505 170 jetons affichés ne sont pas automatiquement le chiffre exact d'un cluster, ni une preuve de propriétaire unique. Une source commune peut expliquer des captures similaires.

**P1 — L'identité documentaire des projets comparateurs.**
Retrouve les comptes originaux, mints, promoteurs, anciens contrats, images de lancement et déclarations de créateur pour :
KLLARY : AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump
RETIREDI0 : DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo
BARRON : HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ
ZOOMER : 9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU

Vérifie la **déclaration du 22 juillet 2024 de @sonder_crypto** sur un possible "même dev" entre BARRON et DMAGA : "dev" peut désigner auteur du mème, animateur ou opérateur de mint. Enquête sur les allusions aux prototypes politiques, à Wifejak et aux expériences de culture coin d'@Aristos_Revenge sans réattribuer arbitrairement ces projets. Identifie JOE, BILLY et WIF seulement avec des sources contemporaines exactes et une désambiguïsation de chaîne/mint. Ne fabrique pas de lien token→wallet depuis un ticker.

**P1 — Origine des fonds et traceurs externes.**
Recherche des posts 2024 associant les quatorze first fundings Coinbase, le créateur, les deux dépôts 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL et Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME, les gagnants H3Qs/GXZvX et les destinations deBridge 0xb947bf7f409e998b28f8e218802fc9575c3c8c57 et 0xb29826d809aa04d2ead6f2310d8965a45b87fa67. Cherche les preuves PRIMAIRES de transactions mentionnées par des observateurs (signature, block, montant, lien explorer), pas de noms civils ou de dossiers privés. Distingue preuve de transfert et attribution d'une identité.

**P2 — Comparaisons et falsifications.**
Repère les premières réactions critiques, corrections d'analystes, exemples d'arbitrage atomique comme le wallet RjL5pLQXzCjMHtT6nBSc9xiCsp2VJR1VWPjfudHrkSZ au slot 279711913, cas de market making et traders multi-tokens. Cherche les explications publiques compatibles avec le timing : événements politiques, marketing, spéculation, arbitrage, bots, activité habituelle sur les autres memes. Compare les sources réelles, pas seulement l'accusation la plus virale.

**P2 — Kekius et les réutilisations ultérieures.**
Analyse seulement les documents publics datés décembre 2024–janvier 2025 qui pourraient tester un recoupement social entre DMAGA, Kekius Maximus et les comptes impliqués. L'enquête financière séparée ne démontre pas un opérateur commun. Aucun transfert ou contrôle commun ne se déduit d'un mème réutilisé ou d'une infrastructure DEX.

## 3. Recherche profonde des petits comptes, langues et données inaccessibles

Ne te limite pas aux gros influenceurs. Effectue un échantillonnage orienté signaux de comptes ayant très peu d'abonnés, tweets en chinois simplifié/traditionnel, anglais, portugais, français, coréen et espagnol. Multiplie les formulations historiques, slang et abréviations (sniper, cabal, bundler, LP, wallet, 老鼠仓, 内幕, 钱包, 狙击, 资金, 做市), ainsi que les adresses exactes et leurs préfixes/suffixes.

Pour les comptes supprimés/suspendus, essaie les sources PUBLIQUES indépendantes (archives, captures dans des réponses, citations presse, reposts déjà archivés). Ne reconstitue jamais un texte perdu à partir d'une accusation ultérieure. Ne fusionne pas un auteur de repost et l'auteur original. Identifie toute source circulaire : 10 comptes relayant une même capture = 1 pièce, pas 10 confirmations.

Priorise d'abord les requêtes qui ont une probabilité d'apporter un **nouvel identifiant transactionnel**, un **nouveau contrat authentifié**, une **nouvelle date primaire**, un **nouveau lien documentaire entre wallets** ou une **preuve directe de communication publiée**. N'empile pas 1 000 posts sans signal nouveau.

## 4. Standards obligatoires

Pour chaque découverte, archive :
- ID et URL X exacts, auteur + author_id, UTC précis, texte original et traduction fidèle, date de récupération, source du tweet/parent/quote, identifiant de média, hash vérifié si binaire disponible.
- Quel détail est **réellement nouveau par rapport à A1–A12/N01–N15** et au JSONL de 1 001 posts.
- Niveau : (A) post/média primaire vérifiable ; (B) témoignage corroboré indépendamment ; (C) déclaration seule ; (D) non vérifiable. La **véracité financière** est un champ séparé : vérifié sur la chaîne / allégation / réfuté / indécidable.
- Hypothèse, meilleure objection, mécanisme alternatif, date/slot/signature à vérifier, critère qui confirmerait et critère qui réfuterait.
- Métadonnées d'exécution : recherche, opérateurs, fenêtre UTC, pages lues, next_token, nombre de résultats, échecs et limites.

Ne prétends jamais à des DMs privés, données confidentielles, KYC, identités civiles ou capacités X illimitées. Ne déduis jamais de la même adresse de service un seul propriétaire. Ne conclus jamais qu'une personne a eu une information privilégiée par la seule antériorité d'un achat ou d'un tweet.

## 5. Livrables de la passe 3

Créer les fichiers de résultat complets :
1. **DMAGA_PASS3_FINDINGS.md** : jusqu'à 15 découvertes NETTES et additionnelles, classées par capacité à produire une vérification financière. Pas de remplissage si seuls 3 vrais nouveaux résultats existent.
2. **DMAGA_PASS3_DELTA.jsonl** : nouvelles publications seulement (absentes des archives A/N), objet original canonique et provenance; liste séparée des objets incomplets.
3. **DMAGA_PASS3_MEDIA.csv** : sources d'images/vidéos, captures de profils, médias vus/téléchargés, hashes, comparaisons, horodatages et limites.
4. **DMAGA_PASS3_SOURCE_GRAPH.csv** : arêtes original/repost/quote/reply, auteur réel, premières occurrences et dépendances entre témoignages.
5. **DMAGA_PASS3_WALLET_LEADS.csv** : wallet/mint/chaîne/source/post, montant allégué, signature si publiée, statut on-chain NON VÉRIFIÉ par défaut, lien direct vs service vs simple mention, piste pour Claude Code.
6. **DMAGA_PASS3_CLAUDE_HANDOFF.md** : 10 missions maximum, P0/P1/P2, avec données historiques, tests falsifiables, signatures recherchées, contrôles négatifs et coût/effort probable.
7. **DMAGA_PASS3_SEARCH_COVERAGE.md** : journal de requêtes, pagination, outils activés, lacunes, reprises et recherche non exhaustive.

Dans le rapport final, présente les **3 meilleures avancées inédites** et les liens vers les fichiers. Sépare les preuves publiques contemporaines, les observations rétrospectives et les hypothèses.

**Publication :** ne modifie ni README.md, ni les conclusions existantes, ni les études figées. Si tu disposes d'un connecteur GitHub autorisé en écriture, tu peux livrer UNIQUEMENT ces nouveaux fichiers sur une branche dédiée research/dmaga-x-pass3, ouvrir une pull request de recherche, et ne jamais fusionner sans validation. Sinon, fournis les 7 fichiers téléchargeables pour import par Claude Code. N'envoie aucun post, like, repost ou DM sur X.

**Fin de mission :** aucun monitoring continu et aucun rapport quotidien. Recherche historique une seule fois, fichiers livrés, mission terminée.
