# DMAGA — Passe 2 : nouvelles précisions historiques

**Quinze résultats supplémentaires**, de granularité différente : nouvelles sources primaires, contrats comparateurs, corrections et analyses de médias déjà connus. **Aucun transfert ni propriétaire de wallet n’est certifié on-chain par cette collecte.**

Référentiel : https://github.com/searadacunha/Dark-MAGA — mint officiel Solana : `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Mission unique du 6 novembre 2026 (Lisbonne), dépôt strictement en lecture seule ; aucune publication, brouillon, interaction X ou routine.

## Ce qui constitue réellement la nouveauté

Les douze résultats A1–A12 du dossier `docs/historical/`, le manifeste, la passation, les deux prompts, SOCIAL_FINDINGS et TIMELINE ont été consultés. Le mémo importé a aussi été comparé intégralement au rapport local précédent : son corps est identique. Les adresses 7GVC, 9Sxm, 5Qh, Nxt, AtZj, H3Qs et GXZvX ne sont **pas** annoncées comme de nouveaux wallets.

Chaque résultat précise son delta. N08/N09 relisent le média du post Noah déjà connu ; N06 corrige A7 ; N07 apporte une autre capture plus ancienne. Les nouveaux ID sont comparés au corpus initial de 5 155 posts, pas à chaque reçu, branche ou fichier GitHub. « Absent du corpus » ne signifie jamais « inconnu de tout le dépôt ».

Les originaux, réponses et citations sont séparés dans le JSONL ; les reposts ne constituent pas des corroborations indépendantes. Les heures machine sont UTC dans les champs `created_at_utc` ; les heures locales associées sont Europe/Lisbon (UTC+1 en juillet 2024). Les chiffres financiers ci-dessous sont des déclarations historiques, non des PnL recalculés.

## Résultats retenus

### N01 — Les trois satellites de Jeffro sont enfin nommés intégralement (P1)

**Sources originales** :

- [1815291795787690478](https://x.com/JeffroBTC/status/1815291795787690478) — @JeffroBTC (author_id `1536322421158211585`), 2024-07-22T07:44:25.000Z ; 2024-07-22T08:44:25+01:00 **Lisbonne**

**Extrait pertinent / traduction** : « 文中涉及的完整地址如下，以出现的先后顺序排列 » — « Voici les adresses complètes, dans leur ordre d’apparition. »

**Nouveauté exacte** : La passe 1 et la passation ne disposaient que de A1UD…vQ8J, 6QFD…5jqD et H4mQ…JU5y. Ce commentaire original, absent des 5 155 posts du corpus de référence, fournit les trois chaînes exactes sans résolution conjecturale.

**Observation** : A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J ; 6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD ; H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y. Les financements respectifs 5/60/16 SOL restent ceux allégués dans le parent déjà connu, pas des transferts nouvellement certifiés. Les wallets peuvent déjà figurer dans d’autres fichiers du dépôt : nouveauté de provenance sociale, pas certificat d’inédit global.

**Arguments favorables à la piste** : Un commentaire directement rattaché au parent relie explicitement chaque abréviation à une adresse.

**Objections / alternative non incriminante** : Il ne fournit ni signature ni preuve de propriété commune ; un transfert SOL peut rémunérer un tiers ou traverser un service.

**Données manquantes** : Instructions System/SPL, sens des arêtes, dates et soldes antérieurs.

**Test falsifiable** : Rejouer les cinq adresses du commentaire du 14 au 22 juillet ; rechercher 5/60/16 SOL et les achats du mint officiel. Confirmer seulement les montants et chemins observés ; réfuter chaque arête absente ou passant uniquement par un service.

### N02 — Jeffro explique sa méthode : flux d’ordres, RPC et API Birdeye (P1)

**Sources originales** :

- [1815609933611794890](https://x.com/JeffroBTC/status/1815609933611794890) — @JeffroBTC (author_id `1536322421158211585`), 2024-07-23T04:48:35.000Z ; 2024-07-23T05:48:35+01:00 **Lisbonne**
- [1815886884972716329](https://x.com/JeffroBTC/status/1815886884972716329) — @JeffroBTC (author_id `1536322421158211585`), 2024-07-23T23:09:05.000Z ; 2024-07-24T00:09:05+01:00 **Lisbonne**
- [1815601378548728093](https://x.com/alexin091/status/1815601378548728093) — @alexin091 (author_id `1230685846983954433`), 2024-07-23T04:14:35.000Z ; 2024-07-23T05:14:35+01:00 **Lisbonne**

**Extrait pertinent / traduction** : « 我是把订单流拉下来配合rpc用程序初步分析 » — « Je récupère le flux d’ordres et fais une première analyse par programme avec le RPC. » Puis : « birdeye有api » — « Birdeye a une API. »

**Nouveauté exacte** : Ces réponses méthodologiques n’étaient pas dans le rapport initial. Elles précisent comment reproduire l’analyste, sans prétendre avoir retrouvé son code.

**Observation** : À la question « les smart wallets viennent-ils du classement top traders Dexscreener ? », Jeffro répond que cet outil peut aider mais n’est pas assez temps réel, puis décrit son pipeline. Le dernier message survient le 24 juillet à 00:09:05 Lisbonne (23 juillet 23:09:05 UTC).

**Arguments favorables à la piste** : La description vient de l’auteur de l’analyse et se rattache au même fil.

**Objections / alternative non incriminante** : Elle ne décrit pas son critère de clustering, ses seuils, son instantané ni ses requêtes exactes ; ce n’est pas une validation de ses chiffres.

**Données manquantes** : Code, fenêtre, règles de sélection et signatures.

**Test falsifiable** : Construire un registre RPC exhaustif et comparer au flux historique disponible ; calculer achats cumulés, position maximale, transferts et PnL réalisé séparément. Un désaccord ne doit pas être masqué en prenant le prix terminal de 0,0547 USD.

### N03 — La suite Jeffro ajoute BILLY et suscite immédiatement une objection Jupiter (P1)

**Sources originales** :

- [1815293200095138249](https://x.com/JeffroBTC/status/1815293200095138249) — @JeffroBTC (author_id `1536322421158211585`), 2024-07-22T07:50:00.000Z ; 2024-07-22T08:50:00+01:00 **Lisbonne**
- [1815302038282256628](https://x.com/apebtc8/status/1815302038282256628) — @apebtc8 (author_id `1577940363569860608`), 2024-07-22T08:25:07.000Z ; 2024-07-22T09:25:07+01:00 **Lisbonne**
- [1815294467232158058](https://x.com/DanaChai/status/1815294467232158058) — @DanaChai (author_id `3591408194`), 2024-07-22T07:55:02.000Z ; 2024-07-22T08:55:02+01:00 **Lisbonne**

**Extrait pertinent / traduction** : « 还发现相关钱包有参与 $BILLY 的做市痕迹 » — « J’ai aussi trouvé des traces de tenue de marché sur BILLY dans les wallets liés. » Un lecteur demande ensuite ce qu’est cette adresse Jupiter et doute de son interprétation.

**Nouveauté exacte** : BILLY et la discussion contradictoire sont absents des douze résultats. Le fait déjà connu qu’un service Jupiter ne désigne pas un financeur personnel n’est pas redécouvert.

**Observation** : Jeffro écrit que les sources et destinations finales passent par « Jupiter Labs Perpetuals Vault Authority » et suggère une dissimulation. Son image GTE27S5aUAAXfB5.jpg montre un compte étiqueté Jupiter et isOnCurve=False ; cette image ne documente aucun propriétaire humain. @DanaChai ajoute « semble aussi avoir vu WIF », sans adresse ni contrat : simple piste, pas relation financière retenue.

**Arguments favorables à la piste** : Le commentaire primaire identifie un nouveau comparateur d’activité, susceptible d’être testé sur les cinq adresses désormais exactes.

**Objections / alternative non incriminante** : Ni contrat BILLY, ni wallet précis, ni ordre prouvant une activité de market maker. Un PDA/service partagé suffit à créer de faux regroupements ; l’intention de cacher des fonds n’est pas établie.

**Données manquantes** : Mints effectivement échangés, instructions perpétuelles et flux nets propres à chaque utilisateur.

**Test falsifiable** : Identifier BILLY depuis les transactions des cinq wallets, puis tester inventory aller-retour, frais et contreparties. Séparer activité d’arbitrage/tenue de marché et retrait de position perpétuelle ; ne pas regrouper tous les clients du vault.

**Médias liés** :
- https://pbs.twimg.com/media/GTE27S5aUAAXfB5.jpg

### N04 — KLLARY : le contrat Solana est identifié par une source officielle datée (P1)

**Sources originales** :

- [1810386941180883011](https://x.com/KILLARYonSOL/status/1810386941180883011) — @KILLARYonSOL (author_id `1800752995090468864`), 2024-07-08T18:54:16.000Z ; 2024-07-08T19:54:16+01:00 **Lisbonne**
- [1815492336123858975](https://x.com/JeffroBTC/status/1815492336123858975) — @JeffroBTC (author_id `1536322421158211585`), 2024-07-22T21:01:17.000Z ; 2024-07-22T22:01:17+01:00 **Lisbonne**
- [1815449734162653410](https://x.com/dissident42069/status/1815449734162653410) — @dissident42069 (author_id `1270407614808162309`), 2024-07-22T18:12:00.000Z ; 2024-07-22T19:12:00+01:00 **Lisbonne**

**Extrait pertinent / traduction** : « Contract Address: AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump ».

**Nouveauté exacte** : Le blocage « ticker KLLARY sans contrat » de la passe 1 est levé documentair​ement. Le post officiel du 8 juillet précède DMAGA et les analyses de Jeffro.

**Observation** : Mint candidat authentifié socialement : AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump, Solana, compte @KILLARYonSOL. Le soir du 22 juillet, Jeffro répond à son propre fil avec une capture « The Clinton Kill List », KLLARY/SOL sur Raydium : cohérence de nom et de chaîne, mais aucun mint lisible dans cette capture. Un autre post de dissident42069 affiche le même mint et ce même compte.

**Arguments favorables à la piste** : Deux publications contemporaines écrivent l’adresse ; le visuel de Jeffro précise quel nom commercial il regarde.

**Objections / alternative non incriminante** : L’image seule ne verrouille pas le contrat précis traité par Jeffro ; aucun swap des wallets DMAGA vers ce mint n’est certifié ici.

**Données manquantes** : Transactions de lancement du mint, historiques des cinq wallets et eventuels homonymes.

**Test falsifiable** : Interroger exclusivement ce mint candidat et les cinq adresses N01. Confirmer le recoupement seulement par des instructions SPL/swaps ; si Jeffro visait un autre contrat, séparer les deux au lieu de forcer le résultat.

**Médias liés** :
- https://pbs.twimg.com/ext_tw_video_thumb/1810386797320613889/pu/img/LE-86TDi5gA8iytT.jpg
- https://pbs.twimg.com/media/GTHsqHLbMAAVk7m.jpg
- https://pbs.twimg.com/media/GTHsqHOakAAsTFo.jpg

### N05 — RETIREDI0 n’est pas un simple RETARDIO mal orthographié (P1)

**Sources originales** :

- [1813651418471100660](https://x.com/dissident42069/status/1813651418471100660) — @dissident42069 (author_id `1270407614808162309`), 2024-07-17T19:06:08.000Z ; 2024-07-17T20:06:08+01:00 **Lisbonne**
- [1813886694199820366](https://x.com/dissident42069/status/1813886694199820366) — @dissident42069 (author_id `1270407614808162309`), 2024-07-18T10:41:02.000Z ; 2024-07-18T11:41:02+01:00 **Lisbonne**
- [1814667184246751544](https://x.com/dissident42069/status/1814667184246751544) — @dissident42069 (author_id `1270407614808162309`), 2024-07-20T14:22:26.000Z ; 2024-07-20T15:22:26+01:00 **Lisbonne**

**Extrait pertinent / traduction** : « Retiredi0 is back in play. CA: DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo ».

**Nouveauté exacte** : La passe 1 conservait volontairement RETIREDI0 sans contrat. Le même auteur publie maintenant une adresse complète plusieurs jours avant sa déclaration de rotation.

**Observation** : Le 17 juillet, @dissident42069 donne DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo. Le 18 il promeut encore RETIREDI0 ; le 20 il écrit « Retardi0 x retiredi0 », distinguant lui-même les deux noms. Ce mint est une cible documentaire Solana, pas un wallet revendiqué par l’auteur.

**Arguments favorables à la piste** : Continuité de compte et de ticker avant le post de rotation ; aucun remplacement typographique n’est nécessaire.

**Objections / alternative non incriminante** : Une déclaration de vente de 80 % ne prouve pas une vente, et ne donne toujours aucun wallet.

**Données manquantes** : Swaps identifiables, contrats réellement échangés et éventuelle preuve publique de contrôle d’un wallet.

**Test falsifiable** : Chercher les comptes qui vendent ce mint et achètent DMAGA dans la fenêtre de rotation publique, avec témoins politiques. Même un match de pourcentage ne permet pas d’attribuer le compte X à un wallet.

**Médias liés** :
- https://pbs.twimg.com/media/GStiWpoXMAAiEmi.jpg
- https://pbs.twimg.com/media/GSw4VeZWsAEjtrT.jpg
- https://pbs.twimg.com/media/GSw4VegXcAAoYde.jpg
- https://pbs.twimg.com/media/GS7-MBhXsAAjkYv.jpg

### N06 — Le paradoxe 1815088124 / 1815088727 est résolu : deux posts distincts (P0)

**Sources originales** :

- [1815088124193579253](https://x.com/dissident42069/status/1815088124193579253) — @dissident42069 (author_id `1270407614808162309`), 2024-07-21T18:15:06.000Z ; 2024-07-21T19:15:06+01:00 **Lisbonne**
- [1815088727250858444](https://x.com/dissident42069/status/1815088727250858444) — @dissident42069 (author_id `1270407614808162309`), 2024-07-21T18:17:29.000Z ; 2024-07-21T19:17:29+01:00 **Lisbonne**
- [1815084272098697611](https://x.com/DegenerateNews/status/1815084272098697611) — @DegenerateNews (author_id `1505874016761831430`), 2024-07-21T17:59:47.000Z ; 2024-07-21T18:59:47+01:00 **Lisbonne**

**Extrait pertinent / traduction** : Premier : « We have sold 80% of our RETIREDI0 and rotated into $dmaga. » Second : « @DegenerateNews @JoeBiden @boden4pres […] Time to rotate into @DarkMagaCoin, bros. »

**Nouveauté exacte** : Correction précise demandée par le nouveau dossier ; on ne republie pas la simple découverte de rotation A7.

**Observation** : L’objet 1815088124193579253 est une publication autonome à 18:15:06 UTC / 19:15:06 Lisbonne, sans referenced_tweets, conversation_id égal à son propre ID. L’objet 1815088727250858444 est une réponse à 1815084272098697611 (@DegenerateNews), à 18:17:29 UTC / 19:17:29 Lisbonne. Le vrai parent annonce le retrait de Biden à 17:59:47 UTC / 18:59:47 Lisbonne. Aucun des deux posts dissident n’est une réponse à l’autre ; écart de 143 secondes. La narration antérieure avait confondu la relation contextuelle, pas les dates des objets.

**Arguments favorables à la piste** : Dates, author_id et referenced_tweets des trois objets sont maintenant disponibles ; les snowflakes sont compatibles.

**Objections / alternative non incriminante** : Cela ne vérifie pas la rotation ni l’heure des trades. Le premier post précède l’avatar, mais suit déjà une annonce publique du retrait de Biden.

**Données manquantes** : Transactions et contrats effectivement vendus/achetés.

**Test falsifiable** : Ajouter un test de graphe : parent(1815088727250858444)=1815084272098697611 ; aucun arc de réponse entre les deux dissident. Étudier les swaps après la nouvelle publique, pas comme une prédiction de cette nouvelle.

**Médias liés** :
- https://pbs.twimg.com/media/GTB9B85W0AAbGlq.jpg
- https://pbs.twimg.com/media/GTB9lCBWoAE67ip.jpg
- https://pbs.twimg.com/media/GTB48aLWMAAKRoX.png
- https://pbs.twimg.com/media/GTB5YLLWEAAU6UZ.jpg

### N07 — Une capture du profil de Musk précède AutismCapital de deux minutes (P0)

**Sources originales** :

- [1815105812076904904](https://x.com/realjohnnewburg/status/1815105812076904904) — @realjohnnewburg (author_id `3115697491`), 2024-07-21T19:25:23.000Z ; 2024-07-21T20:25:23+01:00 **Lisbonne**
- [1815105565741470098](https://x.com/books_empress/status/1815105565741470098) — @books_empress (author_id `1709946001916882944`), 2024-07-21T19:24:24.000Z ; 2024-07-21T20:24:24+01:00 **Lisbonne**
- [1815105605142761543](https://x.com/DogeRetweet/status/1815105605142761543) — @DogeRetweet (author_id `1340082622211510272`), 2024-07-21T19:24:33.000Z ; 2024-07-21T20:24:33+01:00 **Lisbonne**

**Extrait pertinent / traduction** : @realjohnnewburg : « Elon Musk just changed his profile pic ».

**Nouveauté exacte** : Le screenshot de @AutismCapital était déjà A2 ; le nouveau résultat est le post antérieur de @realjohnnewburg et son média, pas la même capture renommée.

**Observation** : À 19:25:23 UTC / 20:25:23 Lisbonne le 21 juillet, le média https://pbs.twimg.com/media/GTCNAerXYAA-ajC.png montre le profil @elonmusk, bandeau de nuit et avatar rouge/laser. Fichier visuellement vérifié : 1815105812076904904_0.jpg. En conservant la borne basse du dépôt (non retéléchargée pendant cette passe), nouvelle fenêtre documentaire prudente : [19:03:27 ; 19:25:23] UTC, soit [20:03:27 ; 20:25:23] Lisbonne, durée 21 min 56 s. Un message texte de @books_empress à 19:24:24 UTC dit déjà que la photo a changé, mais son GIF est une réaction sans profil ; ce n’est pas une capture d’écran de Musk.

**Arguments favorables à la piste** : Image du profil réellement lue, distincte des nombreux portraits isolés et GIF de réaction de la même minute.

**Objections / alternative non incriminante** : Le timestamp du post n’est ni celui de la capture ni celui du clic. L’identité parfaite du fichier doit être comparée par hash/pHash au matériau du dépôt ; aucun déplacement automatique de fenêtre de trades n’a été fait.

**Données manquantes** : Horodatage de capture, comparaison perceptuelle et ledgers autour de la nouvelle borne.

**Test falsifiable** : Comparer le portrait de ce profil à Winig et aux avatars archivés, puis recalculer la sensibilité des cohortes 19:25:23–19:27:24 et 19:27:24–19:30:13 UTC. Ne pas traiter une image isolée comme un écran de profil.

**Médias liés** :
- https://pbs.twimg.com/media/GTCNAerXYAA-ajC.png
- https://pbs.twimg.com/tweet_video_thumb/GTCM48kXkAARNOI.jpg
- https://pbs.twimg.com/media/GTCM7UJXsAAK7Lg.jpg

### N08 — Le tableau Noah permet de quantifier un effet de troncature des pourcentages (P1)

**Sources originales** :

- [1815372294426124565](https://x.com/Noah_nftn/status/1815372294426124565) — @Noah_nftn (author_id `1343419848936673286`), 2024-07-22T13:04:17.000Z ; 2024-07-22T14:04:17+01:00 **Lisbonne**

**Extrait pertinent / traduction** : Tableau joint : total « 204505170 » et « 20.39% » ; groupe 2 annoncé « 6.73% ».

**Nouveauté exacte** : Le texte et les quatre listes A4 sont connus. La nouveauté est la transcription des quatorze montants de l’image GTF0A7xbQAA_FKW.jpg et son contrôle arithmétique, pas une nouvelle analyse indépendante.

**Observation** : Les 14 quantités transcrites totalisent 204 505 170 unités, soit 20,450517 % d’une offre supposée de 1 milliard. Les pourcentages individuels affichés (tronqués à deux décimales) s’additionnent à 20,39 %. Pour le groupe 2, 26 230 000 + 19 274 396 + 6 747 095 + 13 900 000 + 1 359 843 = 67 511 334, soit 6,7511334 %, alors que 2,62+1,92+0,67+1,39+0,13=6,73. Ce petit écart ne modifie pas la conclusion de concentration et n’est pas une preuve de manipulation.

**Arguments favorables à la piste** : Les différences sont reproductibles depuis les chiffres de l’image et expliquées par l’agrégation de pourcentages tronqués.

**Objections / alternative non incriminante** : Le dénominateur exact et le slot ne sont pas fournis ; l’offre affichée peut légèrement différer de 1 milliard. Les quantités de l’image ne sont pas des soldes RPC vérifiés.

**Données manquantes** : Slot de l’instantané, supply exacte et transcription indépendante des nombres.

**Test falsifiable** : Répéter la saisie à deux lecteurs ; calculer les parts à partir des unités entières et d’un unique supply à un slot fixé, puis distinguer troncature et changement réel de balance. Aucun recalcul du groupe des 33 avant Musk ne peut utiliser cet instantané comme s’il était contemporain de cette période.

**Médias liés** :
- https://pbs.twimg.com/media/GTF0A7xbQAA_FKW.jpg
- https://pbs.twimg.com/media/GTF7HGtasAAkxbd.png

### N09 — 6QFD est un pont entre Jeffro et une ligne non groupée du tableau Noah (P1)

**Sources originales** :

- [1815291795787690478](https://x.com/JeffroBTC/status/1815291795787690478) — @JeffroBTC (author_id `1536322421158211585`), 2024-07-22T07:44:25.000Z ; 2024-07-22T08:44:25+01:00 **Lisbonne**
- [1815372294426124565](https://x.com/Noah_nftn/status/1815372294426124565) — @Noah_nftn (author_id `1343419848936673286`), 2024-07-22T13:04:17.000Z ; 2024-07-22T14:04:17+01:00 **Lisbonne**

**Extrait pertinent / traduction** : Jeffro nomme « 6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD » ; la même adresse apparaît dans le tableau Noah avec « 15392092 » et « 1.53% ».

**Nouveauté exacte** : La passe 1 ne disposait ni du satellite résolu ni de la lecture détaillée de cette ligne. Il ne s’agit pas de réénumérer les quatre groupes connus.

**Observation** : Le tableau place 6QFD sur une ligne blanche, hors des quatre aplats de couleur « même entité ». Jeffro le relie par un financement allégué de 60 SOL aux wallets 7GVC/9Sxm. Si cette arête est réelle et pertinente, le tableau de groupes ne capture pas nécessairement tout le réseau financier. Une ligne hors couleur n’affirme cependant pas explicitement « indépendant ».

**Arguments favorables à la piste** : Adresse identique, deux représentations contemporaines et montant d’inventaire lisible.

**Objections / alternative non incriminante** : Jeffro et Noah peuvent utiliser les mêmes services ou données ; ce n’est pas une preuve de même propriétaire. Le versement peut être économiquement banal.

**Données manquantes** : Signature des 60 SOL, expéditeur précis, utilisation et contre-flux.

**Test falsifiable** : Tester 6QFD dans et hors du groupe 4 ; retirer les arêtes de service et mesurer la stabilité du regroupement. Confirmer uniquement une relation transactionnelle justifiée, ou réfuter l’idée d’un périmètre de propriétaire élargi.

**Médias liés** :
- https://pbs.twimg.com/media/GTF0A7xbQAA_FKW.jpg
- https://pbs.twimg.com/media/GTF7HGtasAAkxbd.png

### N10 — Deux comptes publient des observations de distribution avant Noah (P1)

**Sources originales** :

- [1815300464646443155](https://x.com/Pamp_It_/status/1815300464646443155) — @Pamp_It_ (author_id `1234519912409858048`), 2024-07-22T08:18:52.000Z ; 2024-07-22T09:18:52+01:00 **Lisbonne**
- [1815344994787397986](https://x.com/ogtraders_sol/status/1815344994787397986) — @ogtraders_sol (author_id `1787963712067809280`), 2024-07-22T11:15:48.000Z ; 2024-07-22T12:15:48+01:00 **Lisbonne**

**Extrait pertinent / traduction** : @Pamp_It_ : « Wallet with 7% of supply split to 10 wallets […] There are 4 other wallet bundles with 3 - 4% supply ». @ogtraders_sol nomme NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7.

**Nouveauté exacte** : Deux originaux absents du corpus antérieur, pas de nouveaux wallets. Le dépôt connaissait les transferts AtZj/Nxt et les 33 comptes ; le résultat nouveau est la provenance contemporaine antérieure à Noah.

**Observation** : Pamp publie le 22 juillet à 08:18:52 UTC / 09:18:52 Lisbonne ; ogtraders à 11:15:48 UTC / 12:15:48 Lisbonne, avant Noah à 13:04:17 UTC / 14:04:17 Lisbonne. Une capture Pamp montre AtZj → Nxt, 41 000 000 DMAGA, slot 277423092, horodatage affiché 14 juillet 02:46:05 UTC / 03:46:05 Lisbonne ; une autre montre des distributions de Nxt. Ogtraders annonce 290 USD engagés puis 1,8 M USD sur une adresse : coût consolidé non démontré.

**Arguments favorables à la piste** : Les observations ne peuvent pas avoir copié le post Noah ultérieur ; elles fournissent des pièces comparables au graphe connu.

**Objections / alternative non incriminante** : Une source commune antérieure ou un même tableau reste possible. « 7 % sur 10 wallets » ne signifie pas le groupe exact des 33 ; la valorisation de 1,8 M n’est pas un encaissement.

**Données manquantes** : Provenance des captures, signatures et coût des jetons reçus.

**Test falsifiable** : Comparer les arêtes et le slot aux reçus déjà présents, sans les compter comme transferts découverts en 2026. Reconstituer le coût porté par AtZj/Nxt ; ne pas rapprocher des entités par seul pourcentage.

**Médias liés** :
- https://pbs.twimg.com/media/GTE9UHgaEAAZ5N9.png
- https://pbs.twimg.com/media/GTE9Ui7bQAAogfA.png
- https://pbs.twimg.com/media/GTE9tqKa0AA3ZcT.jpg
- https://pbs.twimg.com/media/GTE9wD1bwAAvQsd.jpg
- https://pbs.twimg.com/media/GTFmpjzWYAAUndd.jpg
- https://pbs.twimg.com/media/GTFmpj4XIAAsWI3.jpg

### N11 — Une allégation de développeur commun DMAGA/BARRON devient testable sur un mint précis (P1)

**Sources originales** :

- [1815389229758693508](https://x.com/sonder_crypto/status/1815389229758693508) — @sonder_crypto (author_id `1539044217858560000`), 2024-07-22T14:11:35.000Z ; 2024-07-22T15:11:35+01:00 **Lisbonne**
- [1798702410157973511](https://x.com/Barronsolana/status/1798702410157973511) — @Barronsolana (author_id `1781292925470863361`), 2024-06-06T13:04:07.000Z ; 2024-06-06T14:04:07+01:00 **Lisbonne**
- [1795480077255209108](https://x.com/Barronsolana/status/1795480077255209108) — @Barronsolana (author_id `1781292925470863361`), 2024-05-28T15:39:43.000Z ; 2024-05-28T16:39:43+01:00 **Lisbonne**
- [1815420495858114916](https://x.com/sonder_crypto/status/1815420495858114916) — @sonder_crypto (author_id `1539044217858560000`), 2024-07-22T16:15:49.000Z ; 2024-07-22T17:15:49+01:00 **Lisbonne**

**Extrait pertinent / traduction** : @sonder_crypto : « The $DMAGA dev is also behind $BARRON ». @Barronsolana : « Our contract address: HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ ».

**Nouveauté exacte** : Nouvelle déclaration inter-projets et nouveau contrat comparateur dans les sources chargées. Le prototype politique non nommé du thread Aristos n’est pas identifié automatiquement comme BARRON.

**Observation** : La revendication est datée du 22 juillet. Le compte @Barronsolana publie le mint Solana HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ dès le 28 mai, puis le répète le 6 juin. Le même sonder crédite Kiki du travail sur DMAGA et dit avoir reçu plusieurs appels à y regarder ; cette déclaration sociale n’identifie pas le signataire du mint DMAGA. D’autres BARRON Ethereum et nouveaux pump.fun sont des homonymes, expressément exclus.

**Arguments favorables à la piste** : Le comparateur a une adresse contemporaine issue de son propre compte et une allégation explicite de développeur commun.

**Objections / alternative non incriminante** : Sonder est promoteur/holder déclaré, non témoin indépendant de contrôle cryptographique ; « dev » peut désigner un créateur de contenu plutôt que le wallet créateur. Aucune identité civile n’est recherchée.

**Données manquantes** : Création du mint, signataires, financement, trésorerie et droits résiduels des deux tokens.

**Test falsifiable** : Comparer create-mint, fee payers, autorités, premiers financements et transferts directs hors CEX/services. Un même style graphique, un like ou un routeur commun ne confirme pas le même opérateur ; absence de pont on-chain laisse l’allégation sociale non confirmée.

**Médias liés** :
- https://pbs.twimg.com/media/GTGO3GLWIAA9Niu.jpg

### N12 — Un autre petit compte fournit un cas d’arbitrage atomique, pas d’anticipation (P1)

**Sources originales** :

- [1816729265435562165](https://x.com/OnlyDeFiGuy/status/1816729265435562165) — @OnlyDeFiGuy (author_id `1611183515021746176`), 2024-07-26T06:56:24.000Z ; 2024-07-26T07:56:24+01:00 **Lisbonne**

**Extrait pertinent / traduction** : « Wallet: RjL5pLQXzCjMHtT6nBSc9xiCsp2VJR1VWPjfudHrkSZ […] 8.8 SOL in > 214,341 DMAGA > 9.61906666 SOL out […] 1 atomic TX ».

**Nouveauté exacte** : Adresse et source absentes du corpus X antérieur ; aucun certificat d’absence du wallet dans tous les reçus du dépôt. Ce mécanisme n’était pas documenté dans les douze résultats.

**Observation** : La capture Solscan montre le slot 279711913, 26 juillet 04:00:23 UTC / 05:00:23 Lisbonne, un swap WSOL → DMAGA sur Raydium Liquidity Pool V4 puis DMAGA → WSOL sur Raydium Concentrated Liquidity, agrégés par Jupiter v6. Différence brute alléguée : 0,81906666 SOL ; frais affichés 0,000007177 SOL. La signature visible n’est pas transcrite de façon hasardeuse : slot, wallet et média suffisent à la retrouver.

**Arguments favorables à la piste** : Une image d’instructions et de montants accompagne l’affirmation ; scénario vérifiable sans supposer une position conservée.

**Objections / alternative non incriminante** : Capture ≠ reçu RPC ; le mint exact et le calcul net (tips/ATA/fees) doivent être vérifiés. Le post ne démontre pas que tout trading bénéficiaire est de l’arbitrage.

**Données manquantes** : Transaction brute, mint de chaque compte, balances avant/après et frais complets.

**Test falsifiable** : Retrouver le swap du signataire au slot donné et tester l’inventaire DMAGA intra-transaction puis nul. S’il est confirmé, classer cet échantillon comme arbitrage de pools, non achat informé ; s’il existe une position antérieure, la compter séparément.

**Médias liés** :
- https://pbs.twimg.com/tweet_video_thumb/GTZRoMRagAQzFix.jpg
- https://pbs.twimg.com/media/GTZQ9n3a8AAc51I.jpg

### N13 — Une contestation contemporaine sépare bilan affiché et ventes prétendues (P1)

**Sources originales** :

- [1815850318758043898](https://x.com/ClayBro883/status/1815850318758043898) — @ClayBro883 (author_id `1392193787796000769`), 2024-07-23T20:43:47.000Z ; 2024-07-23T21:43:47+01:00 **Lisbonne**
- [1815849566807146776](https://x.com/ClayBro883/status/1815849566807146776) — @ClayBro883 (author_id `1392193787796000769`), 2024-07-23T20:40:48.000Z ; 2024-07-23T21:40:48+01:00 **Lisbonne**
- [1815568958847959332](https://x.com/cheatbandit_/status/1815568958847959332) — @cheatbandit_ (author_id `1500711502973902849`), 2024-07-23T02:05:46.000Z ; 2024-07-23T03:05:46+01:00 **Lisbonne**
- [1815544758086844687](https://x.com/cexypanda/status/1815544758086844687) — @cexypanda (author_id `3513408197`), 2024-07-23T00:29:36.000Z ; 2024-07-23T01:29:36+01:00 **Lisbonne**

**Extrait pertinent / traduction** : @ClayBro883 : « the wallet with 7.19M DMAGA & 0.0079 SOL still holds the exact same balance of both […] or help me understand ».

**Nouveauté exacte** : Nouvelle discussion critique et nouvel objet de contrôle comptable, non une nouvelle accusation établie. L’original Hasten0x cité 1815479580838555682 est indisponible dans cette collecte.

**Observation** : ClayBro joint deux images montrant le wallet transcrit visuellement HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv, 7 191 363,89 unités marquées DMAGA et 0,007917 SOL. D’autres réponses antérieures contestent déjà le classement ou l’existence de trades. Le texte de ClayBro objecte aussi qu’une vente viderait le pool : c’est son argument, pas un résultat AMM accepté par ce rapport.

**Arguments favorables à la piste** : Adresse complète visible et critiques datées permettent de tester un solde, une période et un montant prétendument réalisé.

**Objections / alternative non incriminante** : Le mint n’est pas visible dans les captures ; la capture peut être périmée, le détenteur peut avoir plusieurs wallets, et le parent perdu ne doit pas être reconstitué depuis les accusations. Le calcul « pool à zéro » n’est pas une preuve de mensonge.

**Données manquantes** : Texte du parent, mint exact, historique et réserves historiques.

**Test falsifiable** : Vérifier d’abord la transcription et le mint, puis les sorties réelles avant le post et les réserves au bloc. Confirmer ou réfuter la vente alléguée sans attribuer le wallet à Hasten0x ; si le parent reste perdu, conclure seulement sur les transactions observables.

**Médias liés** :
- https://pbs.twimg.com/media/GTMyPZ2WMAAyFYC.jpg
- https://pbs.twimg.com/media/GTMyPe2XAAAZDA-.jpg
- https://pbs.twimg.com/media/GTMxjupXwAA6EqY.jpg
- https://pbs.twimg.com/media/GTMxjvJWQAAnuQv.jpg

### N14 — ZOOMER : un contrat du cercle de promoteurs est désormais fixé, sans l’imputer à H3Qs (P2)

**Sources originales** :

- [1814666414705274926](https://x.com/sonder_crypto/status/1814666414705274926) — @sonder_crypto (author_id `1539044217858560000`), 2024-07-20T14:19:22.000Z ; 2024-07-20T15:19:22+01:00 **Lisbonne**
- [1814392628034806077](https://x.com/sonder_crypto/status/1814392628034806077) — @sonder_crypto (author_id `1539044217858560000`), 2024-07-19T20:11:26.000Z ; 2024-07-19T21:11:26+01:00 **Lisbonne**
- [1815800633510727963](https://x.com/0xEnsp1re/status/1815800633510727963) — @0xEnsp1re (author_id `1548005004388098055`), 2024-07-23T17:26:21.000Z ; 2024-07-23T18:26:21+01:00 **Lisbonne**
- [1815800630570516912](https://x.com/0xEnsp1re/status/1815800630570516912) — @0xEnsp1re (author_id `1548005004388098055`), 2024-07-23T17:26:20.000Z ; 2024-07-23T18:26:20+01:00 **Lisbonne**

**Extrait pertinent / traduction** : @sonder_crypto : « $ZOOMER is the one […] CA: 9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU ».

**Nouveauté exacte** : A11 nommait seulement le ticker JOE/ZOOMER. La nouveauté utile est une adresse Solana provenant d’un promoteur contemporain du même espace social ; la simple liste H3Qs n’est pas répétée comme découverte.

**Observation** : Le mint socialement identifié est 9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU. Sonder le répète avant le changement de photo. Le 23 juillet, 0xEnsp1re publie une observation H3Qs/ZOOMER avec l’adresse H3Qs complète et une mise annoncée de 1 700 USD deux mois plus tôt. Mais cette dernière source ne donne aucun mint : il est interdit de fusionner les deux preuves en un swap vérifié.

**Arguments favorables à la piste** : Le contrat associé au promoteur est explicitement écrit et non déduit d’un ticker actuel.

**Objections / alternative non incriminante** : ZOOMER a des homonymes et le contrat acheté par H3Qs reste à contrôler. Le mint JOE n’est toujours pas identifié ; aucun mint BILLY/WIF n’est choisi au hasard non plus.

**Données manquantes** : Tous les mints effectivement tradés par H3Qs durant les trois mois concernés.

**Test falsifiable** : Comparer d’abord les mints du ledger H3Qs à cette adresse candidate. Un match documentaire sans transaction ne suffit pas ; s’il n’existe aucun trade sur ce mint, séparer les homonymes et ne pas invalider automatiquement le tweet générique.

**Médias liés** :
- https://pbs.twimg.com/media/GS79e9wWUAALZMJ.png
- https://pbs.twimg.com/media/GS4EZMJW8AACKNr.png
- https://pbs.twimg.com/media/GTMFCoVXYAALadm.png
- https://pbs.twimg.com/media/GTME9xtX0AAEovA.jpg

### N15 — Le suivi public d’A1UD révèle le risque de confondre jackpot latent et sortie (P1)

**Sources originales** :

- [1815656329887010867](https://x.com/kkashi_yt/status/1815656329887010867) — @kkashi_yt (author_id `1435517423889707012`), 2024-07-23T07:52:56.000Z ; 2024-07-23T08:52:56+01:00 **Lisbonne**
- [1815656223121023203](https://x.com/kkashi_yt/status/1815656223121023203) — @kkashi_yt (author_id `1435517423889707012`), 2024-07-23T07:52:31.000Z ; 2024-07-23T08:52:31+01:00 **Lisbonne**
- [1816071057822056589](https://x.com/kkashi_yt/status/1816071057822056589) — @kkashi_yt (author_id `1435517423889707012`), 2024-07-24T11:20:55.000Z ; 2024-07-24T12:20:55+01:00 **Lisbonne**
- [1816070825877070009](https://x.com/kkashi_yt/status/1816070825877070009) — @kkashi_yt (author_id `1435517423889707012`), 2024-07-24T11:20:00.000Z ; 2024-07-24T12:20:00+01:00 **Lisbonne**
- [1817218497304567925](https://x.com/kkashi_yt/status/1817218497304567925) — @kkashi_yt (author_id `1435517423889707012`), 2024-07-27T15:20:26.000Z ; 2024-07-27T16:20:26+01:00 **Lisbonne**
- [1817218352278024318](https://x.com/kkashi_yt/status/1817218352278024318) — @kkashi_yt (author_id `1435517423889707012`), 2024-07-27T15:19:52.000Z ; 2024-07-27T16:19:52+01:00 **Lisbonne**
- [1820443412040171659](https://x.com/kkashi_yt/status/1820443412040171659) — @kkashi_yt (author_id `1435517423889707012`), 2024-08-05T12:55:06.000Z ; 2024-08-05T13:55:06+01:00 **Lisbonne**
- [1820443349163413780](https://x.com/kkashi_yt/status/1820443349163413780) — @kkashi_yt (author_id `1435517423889707012`), 2024-08-05T12:54:51.000Z ; 2024-08-05T13:54:51+01:00 **Lisbonne**

**Extrait pertinent / traduction** : 23 juillet : « bought $652 $DMAGA […] bag is now worth over $492,000 […] haven’t sold any yet ». 24 juillet : « still hasn’t sold […] about $128,000 in profit ». 5 août : « still holding […] about $66,000 profit ».

**Nouveauté exacte** : Nouvelle série datée portant explicitement sur le satellite A1UD, grâce aux réponses d’adresse complète et aux vrais parents. Ce n’est pas une redécouverte de H3Qs ou de GXZvX.

**Observation** : Les réponses de @kkashi_yt identifient chacune A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J et se rattachent aux parents qui donnent les chiffres. Le 27 juillet, le même récit remonte à environ 193 000 USD de profit latent, puis à 66 000 USD le 5 août ; ce n’est donc pas une série monotone ni un relevé de pertes réalisées. Le coût annoncé de 652 USD doit être réconcilié avec les financements et prix moyens allégués par Jeffro, non fusionné aveuglément.

**Arguments favorables à la piste** : La relation réponse-parent rattache la même adresse aux quatre observations ; les montants ne proviennent pas seulement d’un surnom de tracker.

**Objections / alternative non incriminante** : Un seul auteur commercial et ses captures, pas quatre témoins indépendants. Les termes « profit » et « worth » ne sont pas comptablement équivalents ; des ventes peuvent manquer au tracker.

**Données manquantes** : Ledger complet A1UD jusqu’au 5 août, transferts entrants, ventes, frais et prix historiques.

**Test falsifiable** : Calculer quantité conservée, produit réalisé et PnL latent à chaque publication ; réfuter « n’a pas vendu » si les swaps le contredisent. Ne pas transformer un sommet théorique d’environ 1 M USD en somme encaissée ni en preuve de maîtrise du calendrier.

**Médias liés** :
- https://pbs.twimg.com/media/GTKBs4bbMAAlUIj.jpg
- https://pbs.twimg.com/media/GTKBs4ebsAAzpb8.jpg
- https://pbs.twimg.com/media/GTP6_98bkAAXV7m.jpg
- https://pbs.twimg.com/media/GTP6ycdaYAAFzUN.jpg
- https://pbs.twimg.com/media/GTP6ycdbMAAp9oH.jpg
- https://pbs.twimg.com/media/GTgOlT3bcAASGE1.jpg
- https://pbs.twimg.com/media/GTgOcynbQAAJIl9.jpg
- https://pbs.twimg.com/media/GTgOcyoaMAAydBG.jpg
- https://pbs.twimg.com/media/GUODkZObgAAOLr-.jpg
- https://pbs.twimg.com/media/GUODkZPbIAAfvBZ.jpg

## Annexe : transcription numérique du tableau Noah

Source : https://x.com/Noah_nftn/status/1815372294426124565 ; média https://pbs.twimg.com/media/GTF0A7xbQAA_FKW.jpg. Saisie visuelle, contrôlée par addition ; pas de lecture RPC. Les préfixes ci-dessous ne complètent aucune adresse inconnue.

| Ligne / ensemble graphique | Quantité affichée | % affiché |
|---|---:|---:|
| Eaoxy / groupe 1 | 26,354,876 | 2,63 |
| BteH / groupe 1 | 15,606,900 | 1,56 |
| Nxt / groupe 2 | 26,230,000 | 2,62 |
| 5Qh / groupe 2 | 19,274,396 | 1,92 |
| 7FGo / groupe 2 | 6,747,095 | 0,67 |
| 7md / groupe 2 | 13,900,000 | 1,39 |
| GFpq / groupe 2 | 1,359,843 | 0,13 |
| APfA / groupe 3 | 18,879,206 | 1,88 |
| 9SH / groupe 3 | 17,905,738 | 1,79 |
| 6QFD / hors couleur | 15,392,092 | 1,53 |
| EFdq…UXeD / hors couleur | 14,979,956 | 1,49 |
| 7GVC / groupe 4 | 14,244,892 | 1,42 |
| Aei / groupe 4 | 13,000,000 | 1,30 |
| 9Sxm / groupe 4 | 630,176 | 0,06 |

Somme entière : 204 505 170. À supply=1 000 000 000 : 20,450517 %. Somme des parts affichées : 20,39 %. La capture ne fournit pas de slot ; on ne doit pas opposer mécaniquement cet instantané du 22 juillet aux soldes avant Musk.

## Synthèse probatoire

Les pistes à plus fort rendement technique sont N01/N09 (satellites enfin résolus), N11 (BARRON identifié), N04/N05 (contrats KLLARY/RETIREDI0), et N15 (PnL réalisé vs latent d’A1UD). N06 résout la relation de réponse, N07 resserre une borne documentaire et N08 corrige une précision numérique sans changer le fond de la concentration.

Les quinze résultats ne sont pas quinze enquêtes financières indépendantes : plusieurs proviennent du même auteur ou relisent une même image. Aucune preuve nouvelle de renseignement privé de Musk, de financement par Musk ou de propriété commune des wallets n’est produite. Voir le fichier de couverture pour les pages, les angles morts et le comptage exact.