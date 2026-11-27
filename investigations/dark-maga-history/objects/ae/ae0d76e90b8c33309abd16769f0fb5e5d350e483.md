# Dark MAGA ($DMAGA) : rapport d'enquête

Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`, Solana. Enquête du 02 au 03/11/2026, Claude Code (Opus 5.5) pour Benjamin. Chiffres injectés par `scripts/rep_90_case.py`.

Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice ou hypothèse, **D** non vérifié ou contredit. Ce rapport ne présente personne comme l'auteur d'un délit. Un wallet ou un compte cité n'est accusé de rien.

## L'essentiel
1. **Le token n'a pas été lancé avant Butler.** Mint créé le 14/07/2024 à 02:05:25 UTC, environ 28 h après la tentative d'assassinat, pas le 11/07 ni « deux jours avant » comme l'écrit le récit d'@Aristos_Revenge (A pour la création, la date de Butler étant une connaissance générale).
2. **L'explosion suit le changement de photo de Musk.** Fenêtre documentée : 19:03:27 à 19:30:13 UTC le 21/07, image envoyée à 19:23:20 UTC. Dans l'heure d'avant-bascule, presque rien : 13.18 SOL d'achats sur 1.29 h. Dans l'heure d'après : 5377.61 SOL (A).
3. **Aucune preuve d'achat informé juste avant Musk.** Verdict du test gelé : **DMAGA NON DISTINGUABLE DE SES PAIRS** (211 comparateurs, meilleur p = 0.156). Une absence d'anomalie ne prouve pas l'absence de connaissance : quelqu'un qui détient déjà n'a pas besoin d'acheter.
4. **Il existe bien un groupe tôt et concentré.** 33 wallets reliés par 40 transferts directs d'au moins 1 M de jetons, tous relus sur la chaîne, détiennent 217 M de jetons avant Musk, soit 23 % de ce qui est hors pools. Ils ont vendu dans le pic (B pour le groupe, aucun nom).
5. **Lien entre un wallet viral et le créateur.** `5QhJJc…`, le wallet de la capture de @0xRamonos, envoie 0,032 SOL au wallet créateur 35 secondes avant que celui-ci ouvre un ordre de vente sur tous ses jetons, en juillet 2025 (A pour la transaction, B pour une action concertée à cette date, C pour un acteur unique dès le lancement). Rien ne relie @0xRamonos à ce wallet au-delà de son post.
6. **Les trois autres pistes publiques restent sans lien avec ce groupe** sur les transferts directs : `H3QsBr…` (réalisé 5,491 SOL, 990,744 $ pour 1,087 $ de coût), `GXZvX…` (2,540 SOL), `9PrmF8…` (1,748 SOL). Leurs entrées précoces restent compatibles avec un pari spéculatif. Le contraire n'est pas exclu.
7. **Aucun lien documenté entre un wallet et @DarkMagaCoin, @kikisknees, @Aristos_Revenge ou @ChrisWinig.** Le DM à Musk reste revendiqué, non prouvé.

## Données et fiabilité
- **Collecte :** 2,699,114 transactions réussies normalisées (pool Raydium, courbe, mint, 77 venues), 71,706 wallets. Signatures listées : 9 875 478 sur le pool, dont une majorité échouée le 22/07, et 6 624 533 sur le mint.
- **Réconciliation :** chaîne de soldes des vaults Raydium : 0 rupture sur 681,308 transactions WSOL, 1 rupture sur 681,300 transactions DMAGA (0,39 jeton, poussière). Autres venues : 83 réserves, 215,309 transactions, 0 rupture.
- **Validation externe :** coût recalculé de `H3QsBr…` 1 087 $ contre 1 086 $ sur la capture DexScreener de 2024 ; capitalisation recalculée 844 k$ à l'instant où @kikisknees écrit « $850k » ; `GXZvX…` 48,5 SOL et 14,69 M comme le post de @ai_9684xtpa.
- **Trou détecté et comblé :** ce même contrôle a repéré 97 ruptures dues à un découpage trop court (23:36 à minuit le 23/07), comblées.
- **Limites du PnL :** coût moyen pondéré, frais de plateforme exclus. Un wallet qui reçoit ses jetons d'un autre a un réalisé surévalué : le classement des gagnants ne retient que les coûts connus (`reports/TOP_TRADERS.md`).

## Les 12 questions
**1. Qui a créé le token ?** Le wallet `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR`, signature `fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6` (A). Financé 33 minutes avant par Coinbase 3, 0,5 SOL : rupture de traçabilité. Il achète 7,1 M pour 0,2 SOL et ne vend rien pendant le pic. Pas de snipe de courbe (A). Identité civile : impossible à établir sans réquisition de l'échange. Wallets du lancement : voir `reports/COORDINATION.md`, dont le financement de wallets neufs 65 minutes avant le mint (A pour les virements).

**2. Qui a créé et publié le premier le visuel ?** Plus ancienne image identique archivée : @ChrisWinig, 21/07 16:02:29 UTC, pHash à distance 0 de l'avatar de Musk (A). @kikisknees revendique « pfp by me and @ChrisWinig » et « made the first one » (B, déclaration). @DarkMagaCoin publie une capture iOS `IMG_5658` datée 06:17, fuseau inconnu, date modifiable (C). Une réponse de @kikisknees à Musk à 16:00:08 UTC a perdu son image : **on ne peut pas exclure qu'il ait publié le visuel 2 min 21 s plus tôt** (D). Versions du fichier : l'esthétique rouge existe depuis mars 2022, et @pmarca publie une image rouge le 20/07, différente.

**3. Qui a amplifié avant le changement de photo ?** @DarkMagaCoin, @kikisknees (réponses répétées à des comptes à forte audience, dont @pmarca à 12:50 UTC : « Is Elon mooning with us? »), @koreanjewcrypto dès le 15/07, @kanpai dès le 16/07, @pmarca avec ses propres images rouges (A pour les posts archivés). Corpus partiel : pas de recherche X native. Graphe : `viz/index.html`, `data/social_links.parquet`.

**4. Quels wallets ont acheté avant chaque publication ?** `reports/EARLY_BUYERS.md` donne les 1 000 premiers acheteurs, les plus gros acheteurs des heures précédant le visuel et Musk, et les achats de la fenêtre indécidable de 27 minutes. Les deux cohortes sont distinctes (A).

**5. Profits réellement réalisés ?** `reports/TOP_TRADERS.md`. Tête au coût connu : `H3QsBr…` 5,491 SOL (990,744 $), `GXZvX…` 2,540 SOL (458,663 $), `9PrmF8…` 1,748 SOL (317,215 $). `5QhJJc…`, malgré « 1,8 M$ » sur la capture, a réalisé 74 SOL en propre : ses jetons sont sortis vers d'autres wallets (A). La valorisation maximale n'est jamais comptée. Parmi les 53,893 wallets entrés après Musk, 34 % ont un réalisé positif.

**6. D'où venaient les fonds ?** Surtout d'échanges et d'historiques de trading antérieurs : Coinbase, Binance, MEXC, OKX pour les wallets vérifiés (`data/funding_edges.parquet`). Un hot wallet coupe la trace. Hors échange, le groupe de lancement se finance entre lui (A pour les virements listés).

**7. Où sont allés les bénéfices ?** `data/exit_flows.parquet`, `data/exit_summary.json`. Échanges atteints dans la trace à 3 sauts, en SOL équivalents et de façon approximative au-delà du premier saut : Bybit 2 8,523, Binance 1 8,051, Coinbase 3 3,285, Coinbase 1 2,589, Coinbase 2 2,039, OKX 16 446. `9PrmF8…` passe par `H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi` puis Coinbase (A). Beaucoup de sorties s'arrêtent à des wallets non étiquetés ou à un service non nommé (limite). Aucune continuité n'est supposée à travers un échange.

**8. Clusters solides ?** Oui, un groupe de 33 wallets (B), et des groupes plus petits. Une composante plus large existe dans `data/wallet_clusters.parquet`, mais elle peut venir d'un effet de chaîne : ne pas la lire comme un propriétaire unique.

**9. Liens wallets ↔ comptes X ?** Aucun lien de propriété documenté. Trois mentions de tiers, aucune adresse revendiquée par un compte du noyau (`reports/ATTRIBUTION.md`).

**10. Scénarios sans connaissance privilégiée ?** (a) Une équipe lance et accumule tôt, fait une campagne publique visant des comptes influents, Musk adopte l'image comme d'autres, le groupe vend dans le pic. Ce scénario explique tout ce qui est observé sans aucune information sur Musk. (b) Des parieurs indépendants achètent un mème politique juste après Butler. (c) Le pré-mouvement du matin du 21/07 suit des posts publics, dont ceux de @pmarca.

**11. Preuves manquantes ?** La conversation d'origine, le fichier d'origine du visuel, une communication datée entre un wallet identifié et un proche de Musk, ou une attribution vérifiable d'un wallet à un compte. Voir `reports/MISSING_EVIDENCE.md`.

**12. Ce qui reste incertain ?** Le contenu de la réponse de 16:00:08 UTC ; le DM ; l'heure exacte de la bascule à l'intérieur de 27 minutes ; le propriétaire unique ou non du groupe ; le sens de la répartition du 21/07 à 08:00 UTC ; l'identité de tous les wallets.

## Hypothèses
| Hypothèse | Conclusion | Niveau | Ce qui va contre |
|---|---|---|---|
| H0, hausse organique après adoption d'un mème | L'adoption déclenche bien la hausse. « Organique » est trop fort, la campagne existe | A pour le déclenchement | H1 |
| H1, campagne promotionnelle coordonnée | Soutenue : équipe déclarée, Telegram, outil de pfp, réponses à des comptes influents | A pour les posts, B pour la coordination | Une campagne publique n'a rien d'illicite en soi |
| H2, connaissance préalable de l'adoption | **Non établie.** Test gelé non significatif, 13.18 SOL d'achats dans les 1.29 h avant, le groupe ne trade pas entre le visuel et la bascule. DM non prouvé, nuancé par le compte lui-même | D pour une démonstration, C pour une possibilité | Répartition du groupe à 08:00 UTC ; message « made for him » ; test sans puissance sur un détenteur passif |
| H3, contrôle de l'offre, financement coordonné | Soutenue pour la distribution précoce : 217 M détenus par le groupe, préparation avant le mint. Volume artificiel non testé | B | Pas de snipe au slot 0 ; 0,2 SOL du créateur ; aucun propriétaire unique établi |
| H4, paris spéculatifs ordinaires | Compatible pour la plupart des gagnants hors du groupe | C | Coïncidences non mesurées au niveau individuel |

Ces hypothèses coexistent. Le scénario le plus simple compatible avec les données combine H1, H3 et un effet H0 déclenché par Musk, sans nécessiter H2.

## Test gelé
Plan gelé avant tout calcul (`etude_final/`), audit des échecs silencieux avant le gel, contrôles positifs (nul 5 %, effets 100 %) et de bout en bout. Comparateurs par règle sur 13 920 migrations Pump.fun du 15/06 au 31/08/2024. k = 211, 84 jours de pic.

| Mesure | DMAGA | Médiane des pairs | p de rang |
|---|---|---|---|
| M1 | 39.867 | 3.755 | 0.170 |
| M2 | 9.371 | 1.464 | 0.184 |
| M3 | 0.680 | 0.450 | 0.241 |
| M4 | 0.308 | 0.347 | 0.547 |
| M5 | 433.798 | 176.327 | 0.264 |
| M6 | 0.205 | 0.075 | 0.156 |
| M7 | 0.138 | 0.074 | 0.179 |

Verdict : **DMAGA NON DISTINGUABLE DE SES PAIRS**. Sur son propre passé, DMAGA est bien réveillé avant les événements : 402 SOL sur les 3 h avant le post de Winig contre une médiane de 6.1, p = 0.036 sur 27 fenêtres (le plus petit p possible), sans passer Holm. Exploratoire, hors plan : financeur commun des 50 premiers gros acheteurs 0.08 contre une médiane de 0.00, p = 0.073, k = 40.

**Limites du test :** n = 1 pour la cible ; les mesures ont été choisies après avoir vu DMAGA ; le pic compte des signatures échouées ; R1 et R2 réduits par l'amendement 001 ; le groupe de comparaison est conditionné au fait d'avoir explosé : la conclusion ne vaut que parmi les pics tardifs. Audit complet par quatre auditeurs à l'aveugle non réalisé en entier, voir la fin de `reports/COORDINATION.md` si complété.

## Contre-vérifications qui ont changé les conclusions en cours de route
Retirés avant livraison, parce que le contrôle a montré qu'ils étaient faux : financeur commun du créateur et de `9PrmF8…` (Coinbase) ; « destinataire commun » (réserve de pool) ; groupe de trois wallets signalés (comptes publiés par Jupiter) ; second lien créateur ↔ `5QhJJc…` (exécutant Jupiter DCA) ; premier registre d'étude contaminé par un bug de test (`etude/CONTAMINATION_E2E.md`).

## Ancien travail
Une seule session retrouvée, du 02/08/2026 (`docs/PRIOR_WORK.md`). Son constat « pas de snipe » est confirmé. Son « aucun lien ChangeNOW » reste un échantillon. Le récit d'une équipe et d'une adresse deBridge récurrente n'est documenté dans aucun fichier trouvé. Enquête secondaire Wifejak : désactivée, aucun contrat n'est donné par le thread.

## Livrables
`docs/TIMELINE.md`, `reports/TOP_TRADERS.md`, `reports/EARLY_BUYERS.md`, `reports/COORDINATION.md`, `reports/ATTRIBUTION.md`, `reports/MISSING_EVIDENCE.md`, `viz/index.html`, `data/x_posts.jsonl`, `data/social_links.parquet`, `data/wallet_clusters.parquet`, `evidence/MANIFEST.sha256`. Sur le disque USB `VERBATIM HD/Dark-MAGA-Investigation/data/` : `trades.parquet`, `wallets.parquet`, `funding_edges.parquet`, `exit_flows.parquet`, `link_edges.parquet`, reliés depuis `data/`. Brut : `raw/`, manifeste `evidence/RAW_MANIFEST.tsv`.
