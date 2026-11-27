# Dark MAGA ($DMAGA) : rapport d'enquête

Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`, Solana. Enquête du 02 au 03/11/2026, Claude Code (Opus 5,5) pour Benjamin. Chiffres injectés par `scripts/rep_90_case.py`.

Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice ou hypothèse, **D** non vérifié ou contredit. Ce rapport ne présente personne comme l'auteur d'un délit. Un wallet ou un compte cité n'est accusé de rien.

## Version historique et périmètre

Cette synthèse conserve les calculs et formulations du 3 novembre 2026. Pour les conclusions retenues après relecture, lire le [README](../README.md), son [registre de preuves](README_REVIEW_2026-11-05.md), puis les [contrôles numériques H](https://github.com/searadacunha/Dark-MAGA/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_H/REAUDIT_CONCLUSIONS.md) et les [contrôles transactionnels I](https://github.com/searadacunha/Dark-MAGA/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_I/REFUTATION.md).

**Le créateur est extérieur à la composante de 33 wallets définie par les 40 transferts de DMAGA.** Les transferts de SOL et convergences vers des dépôts décrits au point 5 portent sur un autre périmètre, qui recoupe partiellement les 33. Ils ne démontrent ni l'appartenance du créateur aux 33, ni un contrôle commun dès le lancement. Les formulations historiques « autour du créateur » et « lien au créateur » ci-dessous ne doivent pas être interprétées comme ces démonstrations.

## L'essentiel
1. **Le token a été créé après Butler.** Mint créé le 14/07/2024 à 02:05:25 UTC, environ 3 h 54 après la tentative d'assassinat (A pour la création, heure de Butler non revérifiée dans un fichier). Le thread d'@Aristos_Revenge ne date pas le mint : il écrit que @kikisknees a lancé @DarkMagaCoin et les pfp deux jours avant Butler. Le compte X existe depuis le 11/06/2024.
2. **La hausse suit l'envoi de l'avatar de Musk.** Fenêtre documentée : 19:03:27 à 19:30:13 UTC le 21/07 (A), image envoyée à 19:23:20 UTC (B). Achats : 3,29 SOL de 19:03:27 à 19:23:20, 145,44 SOL de 19:23:20 à 19:30:13, 5 377,61 SOL dans l'heure suivante (A pour les flux, B pour la cause). Entre l'annonce de Biden et la borne basse (1,29 h) : 13,18 SOL d'achats, 84,94 de ventes. Sur les 3 h avant l'envoi, en revanche, 229,3 SOL contre une médiane de 6,2 dans le passé du token, p = 0,069, secondaire.
3. **Aucune preuve d'achat informé juste avant Musk.** Verdict du test gelé : **DMAGA NON DISTINGUABLE DE SES PAIRS** (211 comparateurs, meilleur p = 0,156, DMAGA au mieux 33e sur 212). Une absence d'anomalie ne prouve pas l'absence de connaissance : quelqu'un qui détient déjà n'a pas besoin d'acheter.
4. **Il existe un ensemble financier précoce, autour du créateur.** 33 wallets reliés par 40 transferts directs d'au moins 1 M, tous relus sur la chaîne (A ; règle descriptive, hors plan). Ils détiennent au plus 217 M avant Musk, 23 % des 938 M hors pools : c'est un plafond. Sous-ensemble le mieux relié : 29 wallets, 166,1 M, 17,7 % (B). 4 wallets, 50,9 M, ne tiennent que par une transaction (C). 15 des 33 achètent en première heure. Ventes par swap en 24 h après Musk : 4 525 SOL, soit **2,4 % des 190 551 SOL vendus sur le marché**. Aucun nom.
5. **Le wallet créateur est relié à cet ensemble.** `5QhJJc…`, le wallet de la capture de @ramonos (URL @0xRamonos), lui envoie 0 032 SOL 35 secondes avant qu'il ouvre un ordre de vente sur tous ses jetons, en juillet 2025. Et en janvier 2025, en 190 secondes, le créateur, `5QhJJc…` et un autre membre envoient du SOL à une même adresse, `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` (48 expéditeurs, 94,5 % de ses fonds repartent vers Coinbase). A pour les transactions, B pour une action concertée, C pour un acteur unique dès le lancement. Rien ne relie @ramonos à ce wallet au-delà de son post.
6. **Les autres gros gagnants signalés restent sans lien avec cet ensemble** par transfert direct : `H3QsBr…` (réalisé 5 491 SOL, 990 744 $ pour 1 087 $ de coût), `GXZvX…` (2 540 SOL) et `9PrmF8…` (1 748 SOL, fourni par la mission, source sociale non retrouvée). Leurs entrées précoces restent compatibles avec un pari spéculatif. Le contraire n'est pas exclu.
7. **Aucun lien documenté entre un wallet et @DarkMagaCoin, @kikisknees, @Aristos_Revenge ou @ChrisWinig.** Le DM à Musk reste revendiqué, non prouvé.

## Données et fiabilité
- **Collecte :** 796 883 transactions distinctes (919 783 lignes) dans `trades.parquet`. 2 699 114 lues sur tous les historiques (pool, courbe, mint, 77 venues), doublons compris, dont 1 181 780 sans flux DMAGA et 118 échouées. 71 706 wallets. Signatures listées : 9 875 478 sur le pool, 6 624 533 sur le mint.
- **Réconciliation :** chaîne de soldes des vaults Raydium : 0 rupture sur 681 308 transactions WSOL, 1 rupture sur 681 300 transactions DMAGA (0,39 jeton, poussière). Autres venues : 83 réserves, 215 309 transactions, 0 rupture.
- **Validation externe :** coût recalculé de `H3QsBr…` 1 087 $ contre 1 086 $ sur la capture DexScreener de 2024 ; capitalisation recalculée 844 k$ quand @kikisknees écrit « $850k » ; `GXZvX…` 48,5 SOL et 14,69 M comme le post de @ai_9684xtpa.
- **Trou détecté et comblé :** ce même contrôle a repéré 97 ruptures dues à un découpage trop court (23:36 à minuit le 23/07), comblées.
- **Limites du PnL :** coût moyen pondéré, frais de plateforme exclus. Un wallet qui reçoit ses jetons d'un autre a un réalisé surévalué : le classement des gagnants ne retient que les coûts connus (`reports/TOP_TRADERS.md`).

## Les 12 questions
**1. Qui a créé le token ?** Le wallet `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR`, signature `fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6` (A). Financé 33 minutes avant par Coinbase 3, 0,5 SOL : rupture de traçabilité. Il achète 7,1 M pour 0,2 SOL et ne vend rien pendant le pic. Aucun autre acheteur dans le slot de création (A) ; 17 acheteurs prennent 310,8 M pour 11,9 SOL dans les 60 premières secondes. @Aristos_Revenge écrit que @kikisknees a lancé @DarkMagaCoin (déclaration, C) ; aucun lien entre ce compte et ce wallet. Identité civile : impossible sans réquisition de l'échange. Wallets du lancement : `reports/COORDINATION.md`, dont 13 virements de 0,5 SOL de `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` entre 01:46 et 02:03 UTC, juste avant le mint (7 de ces wallets n'achètent jamais sur le marché), et 2 wallets financés 65 minutes avant (A pour les virements, finalité non établie).

**2. Qui a créé et publié le premier le visuel ?** Plus ancienne image identique archivée : @ChrisWinig, 21/07 16:02:29 UTC, pHash à distance 0 de l'avatar de Musk (A). @kikisknees revendique « pfp by me and @ChrisWinig » (A pour le post, C pour le contenu ; « made the first one » est une réponse du 22/07, objet non précisé). @DarkMagaCoin publie une capture iOS `IMG_5658` datée 06:17, fuseau inconnu, date modifiable (C). Une réponse de @kikisknees à Musk à 16:00:08 UTC a perdu son image : **on ne peut pas exclure qu'il ait publié le visuel 2 min 21 s plus tôt** (D). L'esthétique « Dark MAGA » existe depuis mars 2022.

**3. Qui a amplifié avant le changement de photo ?** @DarkMagaCoin, @kikisknees (réponses répétées à des comptes à forte audience, dont @pmarca à 12:50 UTC : « Is Elon mooning with us? », puis à Musk à 18:46:37 et 18:55:15 UTC, médias perdus), @koreanjewcrypto dès le 15/07, @kanpai dès le 16/07 (A pour les posts archivés). @pmarca publie des images rouges aux yeux laser sans mentionner DMAGA dans ses 2 posts archivés : il n'est pas compté comme amplificateur du token. Corpus partiel : pas de recherche X native. Graphe : `viz/index.html`, `data/social_links.parquet`.

**4. Quels wallets ont acheté avant chaque publication ?** `reports/EARLY_BUYERS.md` donne les 1 000 premiers acheteurs, les plus gros acheteurs des heures précédant le visuel et Musk, et les achats de la fenêtre indécidable de 27 minutes. Les deux cohortes sont distinctes (A).

**5. Profits réellement réalisés ?** `reports/TOP_TRADERS.md`. Tête au coût connu : `H3QsBr…` 5 491 SOL (990 744 $), `GXZvX…` 2 540 SOL (458 663 $), `9PrmF8…` 1 748 SOL (317 215 $). `5QhJJc…`, malgré « 1,8 M$ » sur la capture, a réalisé 74 SOL en propre : ses jetons sont sortis vers d'autres wallets (A). La valorisation maximale n'est jamais comptée. Sommet du prix : 631 364 SOL de capitalisation le 22/07/2024 09:00 UTC. Parmi les wallets entrés après Musk, 18 367 sur 53 893 ont un réalisé positif.

**6. D'où venaient les fonds ?** Surtout d'échanges et d'historiques de trading antérieurs : Coinbase, Binance, MEXC, OKX pour les wallets vérifiés (`data/funding_edges.parquet`). Un hot wallet coupe la trace. Dans le groupe, 11 des 32 wallets tracés ont leur premier financeur dans le groupe, 10 ont `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E`, hors du groupe (A pour les virements).

**7. Où sont allés les bénéfices ?** `data/exit_flows.parquet`, `data/exit_summary.json`. Échanges atteints à 3 sauts au plus, sur 65 wallets tracés, approximatif au-delà du premier saut : Bybit 2 : 8 523 SOL éq. ; Binance 1 : 8 051 SOL éq. ; Coinbase 3 : 3 285 SOL éq. ; Coinbase 1 : 2 589 SOL éq. ; Coinbase 2 : 2 039 SOL éq. ; OKX 16 : 446 SOL éq.. `9PrmF8…` passe par `H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi` puis Coinbase (A). Beaucoup de sorties s'arrêtent à des wallets non étiquetés ou à un service non nommé (limite). Aucune continuité n'est supposée à travers un échange.

**8. Clusters solides ?** En partie : voir le point 4. Le groupe de 33 est lui aussi exposé à l'effet de chaîne, d'où ses niveaux distincts. La composante plus large de `data/wallet_clusters.parquet` ne se lit pas comme un propriétaire unique.

**9. Liens wallets ↔ comptes X ?** Aucun lien de propriété documenté. Trois mentions de tiers, aucune adresse de wallet publiée par un compte du noyau (`reports/ATTRIBUTION.md`).

**10. Scénarios sans connaissance privilégiée ?** (a) Une équipe lance et accumule tôt, fait une campagne publique visant des comptes influents, Musk adopte l'image, un ensemble précoce vend dans le pic. Ce scénario est compatible avec les observations sans information sur Musk. Il suppose un lien entre l'équipe X et les wallets, **non établi**. (b) Des parieurs indépendants achètent un mème politique juste après Butler. (c) Le pré-mouvement du matin du 21/07 suit des posts publics.

**11. Preuves manquantes ?** La conversation d'origine, le fichier d'origine du visuel, une communication datée entre un wallet identifié et un proche de Musk, ou une attribution vérifiable d'un wallet à un compte. Voir `reports/MISSING_EVIDENCE.md`.

**12. Ce qui reste incertain ?** Le contenu de la réponse de 16:00:08 UTC ; le DM ; l'heure de la bascule à l'intérieur de 27 minutes ; un propriétaire unique ou non pour l'ensemble ; le sens des gestes du 21/07 avant le visuel (répartition 07:57-08:33 UTC, regroupement 14:22-14:25 UTC) ; la nature exacte de `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` ; l'identité de tous les wallets.

## Hypothèses
| Hypothèse | Conclusion | Niveau | Ce qui va contre |
|---|---|---|---|
| H0, hausse organique après adoption d'un mème | La hausse suit l'envoi de l'avatar. « Organique » est trop fort : une campagne existe | A pour la succession, B pour la cause | H1 |
| H1, campagne promotionnelle coordonnée | Soutenue : équipe déclarée, Telegram, outil de pfp, réponses à des comptes influents | A pour les posts, B pour la coordination | Une campagne publique n'a rien d'illicite en soi |
| H2, connaissance préalable de l'adoption | **Non établie.** Test gelé non significatif, le groupe ne trade pas entre le visuel et la bascule. DM non prouvé, reformulé ensuite par le compte (« We sent him the meme and he liked it ») | D pour une démonstration, C pour une possibilité | Gestes du groupe le 21/07 avant le visuel ; message « made for him » ; 229 SOL sur 3 h, inhabituel pour DMAGA ; test sans puissance sur un détenteur passif |
| H3, distribution anticipée, financement coordonné | Soutenue pour la distribution précoce : 29 wallets et 166 M (B), virements de SOL avant le mint (A, finalité non établie), lien au créateur (B). Volume artificiel non testé | B | Aucun autre acheteur au slot de création ; 0,2 SOL du créateur ; pas de propriétaire unique établi ; 2,4 % des ventes en 24 h seulement, et moins vendeur que les autres gros détenteurs (22,5 % contre 35,0 %, exploratoire) |
| H4, paris spéculatifs ordinaires | Compatible pour les gagnants hors de cet ensemble | C | Coïncidences non mesurées au niveau individuel |

Ces hypothèses coexistent. Le scénario le plus simple combine H1, H3 et un effet déclenché par Musk, sans nécessiter H2. Le lien entre l'équipe X (H1) et l'ensemble de wallets (H3) reste **non établi**.

## Test gelé
Plan gelé avant tout calcul des mesures (`etude_final/`). Comparateurs par règle sur 13 920 migrations Pump.fun du 15/06 au 31/08/2024. k = 211, 84 jours de pic.

| Mesure | DMAGA | Médiane des pairs | p de rang |
|---|---|---|---|
| M1 | 39,867 | 3,755 | 0,170 |
| M2 | 9,371 | 1,464 | 0,184 |
| M3 | 0,680 | 0,450 | 0,241 |
| M4 | 0,308 | 0,347 | 0,547 |
| M5 | 433,798 | 176,327 | 0,264 |
| M6 | 0,205 | 0,075 | 0,156 |
| M7 | 0,138 | 0,074 | 0,179 |

Verdict : **DMAGA NON DISTINGUABLE DE SES PAIRS**. Sur son propre passé, DMAGA est bien réveillé avant les événements : 402 SOL sur les 3 h avant le post de Winig contre une médiane de 6,1, p = 0,036 sur 27 fenêtres, et 229,3 SOL avant l'envoi de l'avatar, p = 0,069. Ce test secondaire ne pouvait pas passer Holm : 1/28 = 0 036 > 0,0125. Exploratoire, hors plan : financeur commun des 50 premiers gros acheteurs 0,08 contre une médiane de 0,00, p = 0,073, k = 40.

**Limites du test :** n = 1 pour la cible. À k = 211, une mesure ne passe Holm que si DMAGA dépasse tous les comparateurs (1/212 = 0,0047) ; il est au mieux 33e sur 212. Registre : 33 comparaisons réelles, seuil de Bonferroni 0,00152, inatteignable ici, sans effet sur le verdict. Les mesures ont été choisies après avoir vu DMAGA. Le pic compte des signatures échouées. R1 et R2 sont réduits par l'amendement 001, décidé par l'agent sans Benjamin (amendement 002). Le groupe de comparaison est conditionné au fait d'avoir explosé : la conclusion ne vaut que parmi les pics tardifs. Le groupe de wallets et les fenêtres sont des analyses descriptives hors plan.

**État des relectures :**
- Plan et code gelés avant le calcul des mesures ; audit des échecs silencieux **avant** le gel (5 bloquants, 8 majeurs, 8 mineurs, corrigés, corrections non re-auditées).
- Contrôles positifs (nul 5 %, effets synthétiques détectés à k = 150) et de bout en bout. Reproduction en copie neuve : `tests.json` et `verdict.json` identiques.
- Un audit indépendant des conclusions : **FAIL**, corrections intégrées ici sans nouvel audit.
- **Non lancés : les auditeurs à l'aveugle des fuites, des statistiques et du protocole.** `etude_final/audit/` n'existe pas : la porte d'audit de la méthode n'est pas ouverte. À décider par Benjamin.

## Contre-vérifications qui ont changé les conclusions en cours de route
Retirés avant livraison, parce que le contrôle a montré qu'ils étaient faux : financeur commun du créateur et de `9PrmF8…` (Coinbase) ; « destinataire commun » (réserve de pool) ; groupe de trois wallets signalés (comptes publiés par Jupiter) ; destinataire commun du créateur et de `5QhJJc…` (exécutant Jupiter DCA) ; « 28 h après Butler », faux : 3 h 54 ; premier registre d'étude contaminé par un bug de test (`etude/CONTAMINATION_E2E.md`).

## Ancien travail
Une seule session retrouvée, du 02/08/2026 (`docs/PRIOR_WORK.md`). Son constat « pas de snipe » tient au sens étroit : aucun autre acheteur au slot de création. Son « aucun lien ChangeNOW » reste un échantillon. Le récit d'une équipe et d'une adresse deBridge récurrente n'est documenté dans aucun fichier trouvé. Enquête secondaire Wifejak : désactivée, aucun contrat n'est donné par le thread.

## Livrables
`docs/TIMELINE.md`, `reports/TOP_TRADERS.md`, `reports/EARLY_BUYERS.md`, `reports/COORDINATION.md`, `reports/ATTRIBUTION.md`, `reports/MISSING_EVIDENCE.md`, `viz/index.html`, `data/x_posts.jsonl`, `data/social_links.parquet`, `data/wallet_clusters.parquet`, `evidence/MANIFEST.sha256`. Sur le disque USB `VERBATIM HD/Dark-MAGA-Investigation/data/` : `trades.parquet`, `wallets.parquet`, `funding_edges.parquet`, `exit_flows.parquet`, `link_edges.parquet`, reliés depuis `data/`. Brut : `raw/`, manifeste `evidence/RAW_MANIFEST.tsv`.
