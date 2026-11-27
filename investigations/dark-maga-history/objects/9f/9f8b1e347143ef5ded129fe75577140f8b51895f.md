# Rejeu historique des sources X du 6 novembre 2026 : constats

Mint étudié : `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Source des pistes : `docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md` (mémo A1-A12). Heures en UTC. Chaque chiffre ci-dessous sort d'un script de `scripts/` et d'une table de `data/` ; les transactions citées sont figées dans `evidence/receipts/` et relues par `tests/`.

Classement d'une relation (même échelle que l'enquête Kekius) :
- **CONFIRMÉ** : transaction relue, montants et heure recalculés ;
- **CORROBORÉ** : plusieurs indices indépendants ;
- **HYPOTHÈSE** : compatible, non démontré ;
- **REJETÉ** : réfuté, ou lien qui passe par un service.

Un virement confirmé ne prouve ni l'identité civile, ni la détention des clés, ni une information privée. Aucune relation de ce dossier ne relie un wallet à Musk ou à l'équipe Dark MAGA.

## 0. Synthèse hiérarchisée

| # | Constat | Classement |
|---|---|---|
| 1 | 482 des 5 157 observations X sont des reposts. Pour 372 d'entre elles, la ligne porte l'auteur, la date et le texte de l'original. La chronologie citait 4 reposts comme des originaux, dont le « post pmarca » des cohortes, daté 1 h 00 min 29 s trop tard. | CONFIRMÉ |
| 2 | Avatar de Musk visible au plus tard à 19:25:23, et non 19:30:13 : captures de la page de profil par @realjohnnewburg (19:25:23) puis @AutismCapital (19:27:24). La fenêtre indécidable passe à 21 min 56 s et ses achats de 148,73 à 20,85 SOL. | CONFIRMÉ (heure des posts), B pour le contenu des captures |
| 3 | Les 190 SOL de 7GVC proviennent de la clôture de sa **propre** position Jupiter Perpetuals : 189,656069 SOL, 33 min 14 s avant la création du mint. Ce n'est pas un financeur tiers. | CONFIRMÉ |
| 4 | Achat de 41,2 M, virement de 20 M à 9Sxm, financements de 5, 60 et 16 SOL vers trois satellites, qui achètent dans la minute ou les 2 min 29 s suivantes. Les trois abréviations se résolvent sans ambiguïté. | CONFIRMÉ (le « 2 minutes » est faux : 11 min 26 s) |
| 5 | Circuit 7GVC ↔ 9Sxm ↔ AeiMit ↔ satellites : virements directs dans les deux sens (SOL, USDC, DMAGA), activation de comptes, balayage commun le 06/11/2024. Aucune co-signature. | CONFIRMÉ pour les virements ; contrôle commun : HYPOTHÈSE forte, non démontrée |
| 6 | Les quatre groupes de Noah se reproduisent : 141 arêtes directes, toutes internes à un groupe, aucune entre groupes. Le plafond « 6,73 % par entité » se retrouve à 6,751 % (groupe 2). Les 50 contreparties communes entre groupes sont des services, de la poussière ou des candidates écartées. | CONFIRMÉ (arêtes et soldes) ; séparation des groupes : CORROBORÉE |
| 7 | `HBsgbpsM…`, payé par les groupes 2 et 4, est un fournisseur au forfait de 700 $ (au moins 5 payeurs, dont un retrait Coinbase de 700 USDC). Il reverse à `9W9b3zg…`, le collecteur déjà décrit. | CONFIRMÉ (paiements) ; lien entre groupes : REJETÉ |
| 8 | AtZj : « IN 20 USD / OUT 60K USD » exact pour son seul achat (19,94 $) et ses 8 ventes (60 107 $), mais les jetons vendus venaient de quatre wallets du lancement, par virement. | CONFIRMÉ ; le rendement du tracker est REQUALIFIÉ |
| 9 | GXZvX : les trois ventes de la capture (88 791 $) sont ses trois dernières, le 23/07 à 11:47-11:48. Elles suivent de 1 h 05 la dernière capture de l'ancien avatar : antériorité au retrait non établie. | CONFIRMÉ (ventes) ; anticipation : REJETÉE comme conclusion |
| 10 | KLLARY authentifié. 7GVC et 9Sxm l'ont échangé du 27/06 au 03/07/2024, deux semaines avant DMAGA. Même geste « achat puis virement » qu'avec DMAGA. | CONFIRMÉ (activité) ; même opérateur sur deux jetons : CORROBORÉ pour 7GVC/9Sxm seulement |
| 11 | Rotation RETIREDIO → DMAGA après l'annonce de Biden : 11 des 35 acheteurs de la fenêtre vendent du RETIREDIO dans l'heure qui précède, contre 4 sur 149 dans la fenêtre témoin. | CORROBORÉ (exploratoire) ; volume faible : 7,27 SOL |
| 12 | `trades.parquet` omet les virements SPL `Transfer` simples, dont le compte du mint est absent : 22 152 arêtes sur 57 828 relevées par l'API de transferts. Les soldes tirés de cette table seule sont faux pour les wallets concernés. | CONFIRMÉ (défaut du pipeline, non corrigé ici) |

## 1. Provenance des posts X (A1)

**Mécanisme** (`h21_x_reconcile.py`, `data/x_observations_reconciled.csv`)
- Pour l'ID d'un repost, fxtwitter et le point d'intégration de X rendent l'**original**.
- Le collecteur a enregistré l'auteur, la date et le texte de cet original sous l'ID du repost.
- Les deux API concordent sur les 372 cas, et `dmaga.xposts.returned_ids` relit ces réponses brutes.

**Comptes** (`data/x_reconcile_summary.json`), sur 5 157 observations : les 5 155 d'origine, plus les posts @AutismCapital et @realjohnnewburg ajoutés le 06/11

| Relation | Nombre |
|---|---|
| Reposts | 482 |
| dont reposts résolus par les API | 372 |
| dont reposts trouvés par les références des charges Wayback | 110 |
| Réponses | 1 925 |
| Citations | 330 |
| Originaux | 911 |
| Indisponibles non classés | 1 509 |

- Les 372 écarts entre métadonnée et ID sont tous des reposts, sans exception ; le script s'arrête s'il en trouve un autre.
- 5 006 objets distincts.
- Auteur du repost :
  - 110 lus dans la charge Wayback ;
  - 370 seulement par le compte de l'URL d'archive, preuve faible, notée `archived_url_path_unverified` ;
  - 2 inconnus.

**Erreurs corrigées à la source**

| Ligne de `TIMELINE` / événement | ID cité (repost) | Original | Écart |
|---|---|---|---|
| @kanpai, avatars rouges aux yeux bleus | `1813004360592552354` (16/07 00:14:58) | `1813086353741230327` (16/07 05:40:46) ; l'ID cité reprenait en fait `1812984492157771825` (15/07 22:56:01, « Wild PA… ») | le texte ne parlait pas d'avatars |
| @pmarca, image rouge (événement `pmarca_image_rouge`) | `1814779160377602331` (20/07 21:47:23) | `1814763940410499481` (20/07 20:46:54) | −1 h 00 min 29 s |
| @pmarca, nouvelle image | `1815004677160776126` (21/07 12:43:30) | `1814920352134537332` (21/07 07:08:26) | −5 h 35 min 04 s |
| @ChrisWinig réagit | `1815107774113587625` (19:33:11) | `1815107549903135205` (19:32:17) | −54 s |

- `docs/SOCIAL_FINDINGS.md` cite aussi @CryptoOnlyCoims `1812326972661412024`, un repost de `1812326326176469155` (03:20:42) ; correctif en tête du document.
- `scripts/rep_75_timeline.py` refuse désormais tout ID de repost : le générateur s'arrête.
- Il cite l'original et le retrouve dans la charge du repost.

**Incohérence A7 levée**
- `1815088727250858444` (18:17:29) répond à `1815084272098697611` de @DegenerateNews (17:59:47, « BREAKING: @JoeBiden DROPS OUT »).
- Il ne répond pas à `1815088124193579253` (18:15:06), qui n'a pas de parent. Le sens des réponses est cohérent.
- Effet de bord utile : l'annonce de Biden est publique au plus tard à 17:59:47 (événement `annonce_biden`, source ajoutée).

## 2. Borne haute de l'avatar de Musk (A2, passe 2 N07) et fenêtres d'achat

**Pièces**

| Post | Heure (UTC) | Image (sha256) | Lecture |
|---|---|---|---|
| `1815105812076904904` de @realjohnnewburg (« Elon Musk just changed his profile pic »), signalé par la passe 2 (N07) | 19:25:23 | `evidence/x_media/1815105812076904904_GTCNAerXYAA-ajC.png`, `93d239a02ca23f83aa3c158e6754786cdf037472f0a4467f3900ecc416cb0ce3` | page de profil `@elonmusk`, « Joined June 2009 », 190,2 M d'abonnés, avatar rouge aux yeux laser bleus ; disque recadré à **pHash 2/64** du visuel |
| `1815106321810919673` de @AutismCapital (« Elon put on the wartime PFP. ») | 19:27:24 | `evidence/x_media/1815106321810919673_GTCNjq-bEAIJvfT.png`, `44246ed67868eabca54bf3a13101d8fc598a1a1e8141069daf73f809c887a255` | profil « Elon Musk », badge certifié et affiliation X ; disque recadré à **pHash 4/64** |

- Pour les deux heures, la métadonnée X et l'ID concordent.
- Contrôle négatif : parmi les 704 médias archivés, la médiane est de 30 ; les plus proches (2 à 4) sont toutes des copies du visuel Winig/Musk.
- Ce que les pièces ne prouvent pas :
  - l'heure du clic ou de la capture, qui précède le post d'un délai inconnu ;
  - l'authenticité des pages capturées, de même nature que la capture Bailey (19:30:13), qui reste citée.
- La borne basse Wayback (19:03:27) ne change pas. Fenêtre documentée : **[19:03:27 ; 19:25:23], 21 min 56 s**.

**Effet sur les fenêtres** (`h40_windows.py`, `data/windows_sensitivity.csv`)
- Même requête et mêmes exclusions qu'`ana_50`, sur les données courantes.
- Les anciennes bornes reproduisent exactement les chiffres publiés : l'écart vient des seules bornes.

| Fenêtre | Achats publiés (SOL) | Nouvelles bornes : achats (SOL) | Nouveaux acheteurs |
|---|---|---|---|
| avant_pmarca | 5 330,66 | 5 327,01 | 1 450 |
| pmarca_a_winig | 815,06 | 818,71 | 89 |
| fenetre_musk [19:03:27 ; 19:25:23) | 148,73 | **20,85** (13 achats) | 8 |
| musk_plus_1h | 5 377,61 | 5 347,29 | 476 |
| reclassé [19:25:23 ; 19:30:13) | — | 127,88 (44 achats, 39 wallets) | 10 |
| dont [19:25:23 ; 19:27:24), avant la capture @AutismCapital | — | 19,02 | 4 |
| partie finale de fenetre_musk [19:23:20 ; 19:25:23) | — | 17,56 | 7 |

- 127,88 SOL d'achats passent de « indécidable » à « après la borne haute ». Les 53 swaps sont listés dans `data/trades_1925_1930.csv`.
- Capitalisation au cours du pool : 834 k$ à 19:23:20, 773 k$ à 19:25:23, 871 k$ à 19:27:24, 1,26 M$ à 19:30:13. La hausse suit les premières captures publiques.
- Avant la première capture, il reste 20,85 SOL d'achats, dont 3,29 SOL avant le téléversement probable de l'image (19:23:20, B).
- `data/windows.csv`, `data/events.json` et `docs/TIMELINE.md` sont régénérés. `musk_borne_haute` vaut 19:25:23 ; `musk_capture_autismcapital` (19:27:24) et `musk_borne_haute_bailey` (19:30:13) sont gardés pour la sensibilité.
- Deux fenêtres dont les bornes n'ont pas bougé changent aussi : `retrait_plus_7j` (106 081 → 102 944 SOL) et `butler_oct`. L'ancien fichier précédait la déduplication du 06/11 (PR #19). Ce n'est pas un effet des bornes.

## 3. Affirmations de @JeffroBTC (A3)

Post `1815291249102119198`, 22/07/2024 07:42:14 ; texte long intégral dans `data/x_hist_posts.jsonl`. Table : `data/jeffro_claims.csv` ; satellites : `data/jeffro_satellites.csv`.

| Affirmation | Verdict | Preuve |
|---|---|---|
| 190 SOL de Jupiter Perpetuals une demi-heure avant l'ouverture | **CONFIRMÉ, source requalifiée** | Crédit de 189,656068999 SOL le 14/07 01:32:11 (slot 277413262), signature `44Sd6xet31me1Hc1PLCxmKTXEjpaqXjziLfB5qkkAeVq4bBM1RXDkERtJfEFDmgyhjDXUsXv83ws8Fg7GD7e3XJW`, soit 33 min 14 s avant la création du mint. `DecreasePosition3` exécuté par le keeper `DFZcDnmE…` ; le compte WSOL fermé rend 189,653006599 SOL à 7GVC (instruction interne `o1.1`), le reste vient du loyer d'un compte de requête. Demandes de clôture signées par 7GVC à 01:11:01 (`2VMyrqES…`) et 01:28:48 (`GFDyshi4…`). Position ouverte par 7GVC le 13/07 (150 SOL à 23:09:07, 50 SOL à 23:36:33). |
| Achat de 41,2 M à 0,00002721 $ en moyenne | **CONFIRMÉ** | Deux achats Pump.fun à 02:08:50 et 02:11:43 (`4QcZWRme…`, `34LDkYZr…`) : 41 197 138,380017 DMAGA pour 7,903073760 SOL, soit 0,00002773 $ au cours de chaque minute (+1,9 %). |
| 20 M à 9Sxm deux minutes plus tard | **Montant CONFIRMÉ, délai FAUX** | 20 000 000 DMAGA à 02:23:09 (slot 277420037), `2FezsDLMjqaseGDiCvkRBBXGAzs8MFyYxSZ4sKzcQmTZzxC7borK6UABkaCW6oC7h7oN9x15BDQ6STnC6ThojTJW`, instruction `o4`, autorité 7GVC. 11 min 26 s après le 2e achat. |
| Ventes simultanées vers 02:26 | **PARTIEL** | 7GVC : 4 ventes de 02:26:48 à 02:29:49, 6 197 138 DMAGA pour 6,670 SOL. 9Sxm : 1 vente à 02:32:39, 2 000 000 DMAGA pour 1,285 SOL. Pas simultanées. |
| 5 SOL à A1UD…vQ8J, 60 SOL à 6QFD…5jqD, 16 SOL à H4mQ…JU5y | **CONFIRMÉ** | Voir le tableau ci-dessous. Les trois satellites sont financés par 7GVC, pas par 9Sxm. |
| Gains d'environ 66 万, 83 万 et 20 万 $ | **REQUALIFIÉ** | Ce sont des valorisations au cours cité (0,0547 $), pas des gains : aucune vente sur un pool avant le post. Le « 9 % vendu » de H4mQ est un solde net transféré : 1,884 M sortis vers `5n8iW65P…`, 1,539 M revenus. |
| Lien avec KLLARY deux semaines plus tôt | **CONFIRMÉ pour 7GVC et 9Sxm** | §6. |

**Les trois satellites**
- Chaque abréviation est résolue par préfixe et suffixe parmi les destinations SOL de 7GVC et 9Sxm : une seule adresse à chaque fois, sinon le script s'arrête.
- Contrôle indépendant : le commentaire de Jeffro `1815291795787690478` (22/07 07:44:25, réponse à son post, signalé par la passe 2, N01) donne les cinq adresses complètes. Elles sont identiques aux cinq de ce rejeu.

| Satellite | Financement par 7GVC | 1er achat DMAGA | DMAGA achetés | Prix moyen | Jeffro |
|---|---|---|---|---|---|
| `A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J` | 5 SOL, 14/07 18:26:42 (`Wy4wZ6Uv…`) | 33 s après | 12 081 680,84 | 0,0000540 $ | 0,000054 |
| `6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD` | 30 + 30 SOL, 15/07 21:51:14 et 16/07 02:21:36 | 149 s après | 15 392 092,62 | 0,0005622 $ | 0,000562 |
| `H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y` | 16 SOL, 17/07 02:02:14 (`3vWWLUvX…`) | 51 s après | 3 768 814,50 | 0,0006669 $ | 0,000666 |

## 4. Circuit 7GVC, 9Sxm, AeiMit et satellites

Sources :
- grands livres décodés instruction par instruction : `data/ledger_7GVC_20240713_20240725.csv` (414 transactions) et `data/ledger_9Sxm_20240713_20240725.csv` (923) ;
- tables de l'enquête d'origine pour la suite.

| Date (UTC) | De → vers | Montant | Signature | Remarque |
|---|---|---|---|---|
| 15/12/2023 → 29/05/2024 | 7GVC → 9Sxm | 118,45 SOL en 9 virements | `funding_edges` | premier crédit de 9Sxm, 0,447 SOL de 7GVC (`2BbrJKkF…`, 15/12/2023) |
| 29/05/2024 04:03:27 | 9Sxm → 6QFD | création du compte de jetons (loyer 0,00203928 SOL) et virement d'un autre jeton, `GrVQemMc…` | `4UiQXVF3UAkRVbmwRxS9WaXxzUjXjuhVYf2CqYb2MZEC21Y32RipJSAFfVLFVqQ2FVVy54vuYWwbZAzR4xmbg1qv` | première transaction de 6QFD, signée par 9Sxm |
| 30/05/2024 04:13:18 | 7GVC → AeiMit | même geste, même jeton `GrVQemMc…` | `4pcw28aApDZVvvJRyPR79FAA1daQTiy3kTGQqh1ESkFCAWBRgioTFhSJuyE6SMQKCMfX5W4qsMH9CEZ4uNdgdoyH` | première transaction d'AeiMit, signée par 7GVC |
| 14/07 02:23:09 | 7GVC → 9Sxm | 20 000 000 DMAGA | `2FezsDLM…` | §3 |
| 15/07 17:30:35 | 9Sxm → 7GVC | 50 SOL | `4xii2Yv7QyoPuZEw6hHssAYJUTHSWtPAEcNFf8ni63rm1mWP967yyqtG44jHiH9EySJBNVMicTCTxhM5rmQjqFY3` | |
| 17/07 01:40:50 | 7GVC → AeiMit | 13 000 000 DMAGA | `3cBqaMYfeqAnnXCeZ5qmsLW9u6kgQh2ugwBaEHLyoBT1dYT1Y82RbVobQ9p7RceVS9pQHyQfg1qJz97C5abNnDx7` | AeiMit = groupe 4 de Noah |
| 17/07 21:00:34 | 6QFD → 7GVC | 4,623 SOL | `RM8AZbLuWLkcaoJ74mDA2RTmR2LhCVHatruAH8XqbgVHLCtpmFYqxnarTenfxJf7MrqB5oG67jowcNXsepjV3YM` | retour d'un satellite |
| 22/07 00:24:12, 01:58:41, 02:15:45 | 9Sxm → 7GVC | 400 + 400 + 500 SOL | `ZPxD2mvu…`, `3KYiz6CL…`, `2BhDm6UH…` | après les ventes de 9Sxm |
| 22/07 02:20:49 | 7GVC → Jupiter DCA | 1 000 SOL | `57oHcDe8cRBDRmoA7qV7LrPJML3nhyrHuyyqz5rSNnxF7XnYWVjnfzXnNWXtKRrn7HENV4omYxqJ9qAziX3WuKs1` | ordre SOL → USDC, pas DMAGA |
| 22/07 22:11:04 | H4mQ → 9Sxm | 76,679 SOL | `ur6ajcoGpHF6detAM9TNDEad56yLEuYwqLuri9VkqethUP5PEVitrXpKeUhzkrtNHR7qjSasGGh3gvdSKP4ZxiD` | retour d'un satellite |
| 15/07/2024 → 12/08/2025 | 9Sxm ↔ 7GVC | vers 7GVC : 2 602,8 SOL (13 virements, ceux du 15 et du 22/07 compris) et 193 943 USDC (3) ; vers 9Sxm : 286 SOL (5) et 359 657 USDC (10) | `exit_flows` | sorties au-dessus des seuils de `col_30` |
| 24/09 → 06/11/2024 | 6QFD, A1UD, AeiMit → 7GVC | 902,0 ; 586,7 ; 707,3 SOL | `exit_flows` | |
| 06/11/2024 00:05-00:08 | A1UD, AeiMit, 6QFD, 9Sxm → 7GVC | petits soldes DMAGA, en 3 minutes | `token_edges` | balayage |

**Lecture**
- Ces virements sont directs, répétés, dans les deux sens et sur plus d'un an.
- 7GVC ou 9Sxm signent la toute première transaction d'AeiMit et de 6QFD : ils y créent leur compte de jetons et leur virent le même jeton `GrVQemMc…`, en mai 2024.
- Les satellites rendent leurs produits à 7GVC.
- Le contrôle commun en est l'explication la plus simple. Il reste une **HYPOTHÈSE** :
  - aucune des 1 337 transactions des deux grands livres n'est co-signée par 7GVC et 9Sxm ;
  - le contrôle des clés ne se prouve pas par des virements.

Autres hypothèses :
- un petit groupe de personnes qui se paient entre elles ;
- un gestionnaire qui opère pour des tiers.

Aucun indice ne relie ce circuit à l'équipe Dark MAGA ni au groupe des 33 (§5).

**Sans incidence sur DMAGA**
- Le grand livre de 7GVC compte 414 transactions entre le 13 et le 25/07.
- 271 sont des transactions de tiers qui le citent sans changer ses soldes (SOL, WSOL, DMAGA) : Drift, Kamino, Marginfi, Mango, Solend.

## 5. Les quatre groupes de @Noah_nftn (A4)

Post `1815372294426124565`, 22/07/2024 13:04:17. Scripts `h32_noah.py`, `h34_verify_balances.py`.

**Avoirs à l'heure du post**
- Les 15 soldes sont confirmés par l'historique complet de l'ATA de chaque adresse : dernière transaction avant le post, `postTokenBalances`, écart nul (`data/noah_holdings_verified.csv`).

| Groupe | Adresses | DMAGA | % de l'offre |
|---|---|---|---|
| 1 | Eaoxy, BteH | 41 961 776,40 | 4,196 |
| 2 | 5QhJJc, NxtX, 7FGo, 7mdC, GFpq | 67 511 335,15 | **6,751** (Noah : 6,73 au plus par entité) |
| 3 | APfA, 9SHto | 36 784 944,71 | 3,678 |
| 4 | 7GVC, AeiMit, 9Sxm | 27 875 069,33 | 2,788 |
| satellites de Jeffro | A1UD, 6QFD, H4mQ | 30 897 113,30 | 3,090 |

- Le « 20,39 % des dix premiers et liés » n'est pas reproductible : Noah ne publie pas sa liste des dix.

**Arêtes** (`data/noah_edges.csv`)
- 141 arêtes directes, DMAGA, SOL et USDC, toutes internes à un groupe ; **aucune entre deux groupes**.
- Exemples :
  - groupe 1 : BteH → Eaoxy, 26 354 876 DMAGA (14/07 02:55) puis 0,1 SOL ;
  - groupe 3 : 9SHto ↔ APfA, SOL dans les deux sens depuis avril 2024, puis 18 879 206 DMAGA ;
  - groupe 2 : arêtes déjà connues du groupe des 33.
- Les groupes 1, 3 et 4 ne font pas partie du groupe des 33.

**Contreparties partagées entre groupes** (`data/noah_cross_group.csv`, `data/noah_candidates_review.csv`)
- 50 au total : 34 services, 12 envois de poussière, 4 candidates. Services : plus de 25 wallets DMAGA, ou étiquette d'exchange, de routeur, de pool ou de Jupiter. Poussière : moins de 0,01 SOL par virement.
- Les 4 candidates, toutes relues :
  - `HBsgbpsM…` (61 transactions) : fournisseur au forfait, §5.1. **REJETÉ** comme lien ;
  - `F8rHedrg…` : plus de 1 000 transactions, reçoit de petits montants de 10 wallets DMAGA en mars 2025. Service probable, **REJETÉ** ;
  - `FJ9LmErk…` : plus de 1 000 transactions, envoie de 0,002 à 0,2 SOL à de gros détenteurs (Eaoxy, 5QhJJc, GXZvX) le 22/07. Sollicitation de masse, **REJETÉ** ;
  - `Cr8oGfjw…` : 375 transactions depuis le 13/11/2024, reçoit des USDC en montants ronds (200 à 2 310) de 10 wallets DMAGA, dont 7mdCA (groupe 2) et 7GVC (groupe 4). **NON RÉSOLU** : non classé sans lecture complète.
- Conclusion : rien ne fusionne deux groupes. La séparation de Noah est **CORROBORÉE**, sous les limites de couverture de §9.

### 5.1 Un fournisseur à 700 $ qui reverse au collecteur 9W9b3zg

`data/counterparty_HBsgbpsM1j1YsNYqtCXcFU4mCRofwcor2qFwifNqddmH.csv` : toute l'activité de cette adresse, 61 transactions.

**Paiements à prix fixe** (le 1er payeur est dans le groupe 2, le 2e dans le groupe 33)

| Payeur | Date (UTC) | Montant | Valeur |
|---|---|---|---|
| 7mdCA | 26/07 17:50:59 | 3,8443 SOL | 700 $ |
| EEdq9C | 26/07 18:25:57 | 3,85 SOL | 701 $ |
| 6GYsKt | 27/07 01:45:32 | 3,85 SOL | 700 $ |
| Coinbase 2 | 27/07 04:22:34 | 700 USDC | 700 $ |
| 4JrabS | 28/07 20:17:19 | 3,8 SOL | 702 $ |

**Autres entrées**
- 7GVC : 10 SOL (1 819 $) ;
- 9Sxm : 30 SOL ;
- d'autres payeurs.

**Sorties**
- 26 + 4,35 + 0,322 SOL vers `9W9b3zgHH9…` ;
- des USDC vers deux autres adresses.

**Lecture**
- Le même prix payé par cinq payeurs distincts, dont un retrait d'exchange, décrit un fournisseur, pas un propriétaire commun.
- `9W9b3zg…` est le collecteur décrit dans `docs/CASE_REPORT.md` (48 expéditeurs, 94,5 % vers Coinbase). Il reçoit donc aussi le produit d'un vendeur à prix fixe.
- Les envois du créateur et de 5QhJJc vers 9W9b3zg peuvent donc, eux aussi, être des achats d'un service. Cette piste n'est pas tranchée ici (§10).

## 6. Autres affirmations (A5, A6, A7, A11, B2, B4)

**A5, AtZj (@Orkusx, « IN 20 USD / OUT 60K USD »)** (`h35_atzj_gxzvx.py`, `data/atzj_gxzvx.json`)

| Élément | Valeur |
|---|---|
| Seul achat d'AtZj | 161 562,14 DMAGA pour 0,138528 SOL (19,94 $) |
| 8 ventes du 21/07, 22:25:43-22:40:28 | 3 000 000 DMAGA pour 327,333 SOL (60 107 $) |

- Ces deux lignes reproduisent exactement le tracker.
- Les jetons vendus venaient de 84,5 M reçus le 14/07, en virements `Transfer` simples signés par chaque expéditeur :
  - 6t2dz4jm 26,65 M ;
  - 8YrEVPQq 23,41 M ;
  - 99Xrt5uu 19,03 M ;
  - AW63YBXX 15,44 M.
- Ces quatre wallets ont acheté au lancement pour 11,29 SOL au total (1 633 $).
- En coût moyen consolidé (achats des expéditeurs au prorata des jetons reçus, plus l'achat propre), les 3 M vendus ont coûté 0,405 SOL (58,54 $). `74qFhHyp…`, qui ne fait que renvoyer des jetons venus d'AtZj, est exclu du coût.
- Le tracker sous-estime donc le coût, mais le rendement reste du même ordre.
- Proceeds réalisés : 60 107 $ ; ce n'est pas un gain latent.

**A6, GXZvX (@JLKHatesYou)**
- 4 achats (7 516 $) et 103 ventes (466 179 $), comme sur la capture.
- Les trois ventes citées : 11:47:09 (21 165 $), 11:47:37 (34 111 $), 11:48:23 (33 515 $), soit 88 791 $ contre 88 771 $ sur la capture.
- Ce sont ses trois dernières ventes : elles soldent la position, entamée le 21/07 à 18:10:11.
- Placement dans le temps :
  - 1 h 05 min 18 s **après** la dernière capture Wayback de l'ancien avatar (10:43:05) ;
  - 2 h 13 avant l'ID de la nouvelle image (14:01:24, B) ;
  - 2 h 48 avant la capture Wayback du nouvel avatar (14:36:29).
- Le retrait de l'avatar a pu précéder ces ventes : l'antériorité n'est pas établie.
- Même établie, une prise de bénéfice qui ferme 103 ventes réparties sur 41 h 38 ne serait pas une anticipation.

**Contrats** (`h50_contracts.py`, `data/contracts_verified.json`)

| Jeton | Mint | Preuve |
|---|---|---|
| KLLARY | `AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump` | CreateEvent Pump.fun décodé dans la transaction de création `5kGaZNhDcm7PaPFAeYhDYctpQGj5VJ6Y3nEDgxBbR9JZTimHAcFdRVmJkgwvd8VP1wnj6F2rBTgGxjvDo5MK5Chf` (26/06/2024 23:59:41) : « The Clinton Kill List », KLLARY, créateur `DhXfnvDz…` ; aucun autre KLLARY en 2024 |
| RETIREDIO | `DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo` | métadonnées Metaplex RETIREDIO ; donné sous « $retiredio » sur Reddit le 13/07/2024 13:11 ; le post X l'écrit avec un zéro ; le lien au compte @dissident42069 est déduit |
| JOE | `JoeXBUqpCJbaNLMTDxC6o1sLTYHsLef32ga2RDRF89m` | métadonnées « JoeCoin » / JOE ; acheté par H3Qs |
| ZOOMER | `9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU` | métadonnées « Zoomer » / ZOOMER ; capture Wayback CoinGecko du 27/05/2024 ; acheté par H3Qs |

Pistes trouvées par un agent de recherche, revérifiées ici sur la chaîne. Ses sources brutes ne sont pas publiées (pages de tiers).

**B4, KLLARY** (`h51_ata_test.py`, `h52_rotation.py`, `data/ata_kllary.csv`)
- Test par ATA de la période avant le post de Jeffro.

| Ensemble | Activité KLLARY |
|---|---|
| Groupe 4 de Noah | 2 sur 3 (7GVC, 9Sxm) |
| Groupes 1-3 | 0 sur 9 |
| Satellites | 0 sur 3 |
| Témoins : 135 des 140 premiers acheteurs DMAGA | 18 (13 %) |

- Fisher unilatéral, groupe 4 contre témoins : p = 0,045, exploratoire. L'absence d'un autre KLLARY en 2024 vient de l'agent de recherche (DexScreener, GeckoTerminal), pas d'un inventaire de la chaîne.
- 7GVC :
  - premier achat le 27/06 04:05:00, 4 h 05 après la création ;
  - 57,77 M pour 5,055 SOL ;
  - le 29/06, 23 M envoyés à `7rSZBE2SgAJ4D2kDqRdTnLb1yqzC6BRoGSy1aJ1x6ETZ` (`yACQEPgg…`).
- 9Sxm : 36,50 M achetés pour 14,56 SOL à partir du 27/06 13:57, revendus 24,05 M pour 13,15 SOL jusqu'au 03/07.
- Jeffro a raison sur la date. Le geste « achat, puis virement d'une partie à un autre wallet » se répète sur les deux jetons.
- KLLARY était courant chez les premiers acheteurs DMAGA (13 % des témoins). Cela ne désigne donc pas, seul, un opérateur unique des deux lancements.
- Un lien entre 7GVC et le créateur de KLLARY (`DhXfnvDz…`) n'a pas été testé.

**B2, RETIREDIO → DMAGA** (`data/ata_retiredio.csv`, `data/rotation_retiredio.csv`)
- Règle fixée avant lecture et appliquée aux deux ensembles : vente de RETIREDIO dans l'heure qui précède le premier achat DMAGA du wallet dans sa fenêtre.

| Ensemble | Rotations |
|---|---|
| Acheteurs de DMAGA entre l'annonce de Biden (17:46) et la borne basse (19:03:27) | **11 sur 35** |
| Témoins : acheteurs de la fenêtre précédente (16:02:29-17:46) | 4 sur 149 |

- Fisher unilatéral : p = 2,2e-6, exploratoire, non corrigé.
- Ces 11 wallets font 7,27 des 13,18 SOL d'achats de la fenêtre.
- La rotation annoncée par @dissident42069 se voit donc, mais elle est petite. Dans la même fenêtre, les ventes de DMAGA font 84,94 SOL.
- Une rotation publique explique une partie des rares achats d'avant l'avatar. Elle ne dit rien de l'avatar lui-même.

**A11, B8 : H3Qs (JOE, ZOOMER)** : §7.

## 7. H3Qs : JOE, ZOOMER et DMAGA (A11, B8)

Sources : `h53_h3qs.py`, `data/h3qs_by_mint.csv` et `data/h3qs_rotations.csv`. Les 267 transactions réussies de H3Qs du 25/04 au 31/07/2024 sont toutes relues ; aucune n'est exclue comme multi-jetons.

**Bilan par mint, en flux de SOL** (44 mints touchés ; total +5 482,6 SOL)

| Jeton | Achats / ventes | Flux net (SOL) | Position au 31/07 |
|---|---|---|---|
| DMAGA | 2 / 48 | **+5 490,9** | close |
| JOE (`JoeXBUqp…`) | 6 / 2 | −21,6 | ouverte |
| ZOOMER (`9MBzpyMR…`) | 7 / 1 | −11,0 | ouverte |
| HARAMBE | 18 / 2 | +15,4 | close |
| $CCP | 3 / 1 | −14,3 | close |
| Tous les autres mints | — | net de −8,2 hors DMAGA | — |

- Deux mints (SEAL, chemp) n'ont que des ventes : leurs achats précèdent la fenêtre.
- Un flux net d'une position ouverte n'est pas un résultat : sa valeur résiduelle n'est pas comptée.

**Lecture**
- Sur trois mois, le résultat de H3Qs tient en un seul trade, DMAGA.
- JOE et ZOOMER, présentés par @toupaiwang comme ses « meilleurs trades », sont des positions perdantes en flux et encore ouvertes au 31/07. Le chiffre de « plus de 1,5 M$ » ne se vérifie que si l'on compte DMAGA (5 490,9 SOL, environ 1 M$ au cours de juillet) et des valorisations.

**Rotations JOE → DMAGA** (vente suivie d'un achat d'un autre jeton dans les 5 minutes)
- 14/07 16:43:35 : vente de JOE (`4nPPf19o…`), puis achat de 10 047 606 DMAGA 23 s plus tard (`5zc5i9VW…`) ; ce premier achat de DMAGA est financé par la vente de JOE ;
- 15/07 13:02:40 : nouvelle rotation JOE → DMAGA, 14 s ;
- 22/07 : DMAGA → `9TR1Yw…` (50 s), puis DMAGA → JOE (38 s).
- Ce sont des rotations d'un spéculateur entre jetons politiques. Rien n'y désigne une information sur Musk.

**Origine de la piste**
- Le premier repérage vient de l'agent de recherche.
- Les chiffres ci-dessus sont recalculés ici sur les transactions relues, et la rotation est testée sur ses reçus.

## 8. Défaut du pipeline : virements `Transfer` absents de `trades.parquet`

**Constat**
- Un virement SPL `Transfer` (non `TransferChecked`) ne cite pas le compte du mint. Il est donc absent de l'historique de signatures du mint, d'où sort `trades.parquet`.
- Relu sur 5 transactions : les 3 `Transfer` ont 0 ligne dans `trades.parquet`, les 2 `TransferChecked` y figurent.

**Ampleur**
- 22 152 des 57 828 arêtes « gtba » (API de transferts, sans étiquette, une contrepartie) n'ont pas leur transaction dans `trades.parquet`.
- Elles déplacent 2 126 M de jetons au total, chaînes comprises.

**Effet**
- Tout solde calculé depuis `trades.parquet` seul est faux pour un wallet concerné.
- Exemple : 6t2dz4jm y garde 26,65 M au 22/07, alors qu'il les a tous envoyés à AtZj le 14/07.
- `token_edges.parquet` contient ces virements pour les wallets suivis. Les 15 soldes du §5 sont contrôlés par ATA et ne sont pas touchés.

**Suite**
- Les rapports qui somment des soldes depuis `trades` sont à relire avant toute correction : le chiffre « 217 M avant Musk » du groupe des 33 est le premier à revoir.
- Ce dossier ne modifie ni le pipeline ni ces chiffres.

## 9. Couverture et limites

**Grands livres décodés**
- Complets pour 7GVC et 9Sxm du 13/07 au 25/07/2024 (414 + 923 transactions).
- Hors de cette fenêtre :
  - signatures complètes (34 985 et 6 386) ;
  - tables Helius de l'enquête d'origine (DMAGA complet, flux SOL au-dessus des seuils de `col_30`).
- Le reste n'est pas décodé :
  - le pool Helius est épuisé depuis le 06/11 ;
  - le RPC public plafonne vers 0,5 transaction/s ;
  - 28 881 transactions réussies prendraient environ 16 h.

**Arêtes entre groupes**
- Testées sur les tables d'origine : financement avant le premier achat, sorties au-dessus de 0,1 SOL ou 100 USDC après la première vente, DMAGA complet.
- Un virement sous ces seuils, ou sur un autre actif, peut manquer.

**Tests par ATA**
- Un compte de jetons non associé y échappe.
- Les tests KLLARY et RETIREDIO sont exploratoires : petits effectifs, aucune correction pour comparaisons multiples, ensembles définis par l'enquêteur avant lecture mais sans gel formel.

**Autres limites**
- Cours en dollars : clôture SOLUSDT Binance de la minute.
- Pistes de la passe 2 (`docs/historical/pass2/`, fusionnée pendant ce rejeu) non traitées : N03 (BILLY), N08 (troncature des % de Noah), N11 (BARRON), N12 (arbitrage atomique), N13 (ventes Hasten), N15 (suivi d'A1UD jusqu'au 5 août). N01 et N07 sont intégrées (§2, §3) ; N04-N06 rejoignent §1 et §6.
- Non traités : A8 (BOSSIE), A9 (appel de @CristusVictor, original retrouvé et archivé : `data/x_hist_posts.jsonl`), A10 (affirmation d'octobre), A12 (homonyme Ethereum), B9.

## 10. Pistes ouvertes

- **`9W9b3zg…`** : collecteur du créateur ou trésorerie d'un fournisseur ? Lire ses entrées par montant, en dollars, comme en §5.1.
- **`Cr8oGfjw…`** : destination USDC commune à 10 wallets DMAGA, à lire en entier (`h33_counterparty.py`).
- **`7rSZBE2S…`** : destinataire de 23 M KLLARY de 7GVC.
- **Pipeline** : correction du trou `Transfer` (§8) et recalcul des soldes publiés.
- **Rapports en aval** : `rep_70`, `rep_72`, `rep_80`, `rep_90` et `ana_64` lisent `events.json`. Ils n'ont pas été régénérés ici, car le swap de la machine bloquait les calculs gardés. `docs/CASE_REPORT.md`, `reports/EARLY_BUYERS.md` et `reports/TOP_TRADERS.md` citent encore la borne 19:30:13.
