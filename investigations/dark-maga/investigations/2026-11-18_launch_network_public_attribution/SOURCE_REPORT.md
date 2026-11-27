# DARK MAGA — LAUNCH NETWORK & PUBLIC ATTRIBUTION INVESTIGATION

- **Token** : $DMAGA — mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump` (pump.fun, Solana)
- **Repo de référence** (lecture seule) : `searadacunha/DARK-MAGA` @ `1b15817ca9707555f0c74226385040157f69e0b8` (2026-11-18T13:49:08Z)
- **Date du rapport** : 2026-11-18. Tous les horodatages sont en **UTC** (= heure de Lisbonne en novembre).
- **Méthode** : historical-x-forensics.
  - Un budget a été écrit avant la collecte : `raw/00_BUDGET_AND_PLAN.md`.
  - Journal des requêtes : `raw/query_log.tsv`.
  - Chaque identifiant de post a été contrôlé par snowflake : `epoch_ms = (id>>22) + 1288834974657`.
  - Les preuves ont été prises dans X API v2 (archive complète), Wayback Machine, la RPC publique Solana et IPFS.
- **Niveaux de preuve** :
  - **A** : confirmé
  - **B** : fortement corroboré
  - **C** : indice
  - **D** : non vérifié ou réfuté
- **Statut** : **KNOWN** = déjà dans le repo GitHub ; **NEW** = nouveau ; **PARTIAL** = la donnée est dans le repo mais n'était pas exploitée.
- **Règles suivies** :
  - Un résultat nul n'est pas une preuve d'absence.
  - Une chronologie n'établit pas une causalité.
  - Une interaction sociale ne prouve pas une coordination financière.
  - Aucune donnée privée n'a été utilisée et aucune authentification n'a été contournée.

---

## 1. Synthèse des découvertes nouvelles

1. **Correspondance technique entre le créateur 8YLE et @DarkMagaCoin — B, NEW.** C'est l'avancée principale du rapport en matière d'attribution.
   - Nous avons décodé le `CreateEvent` de la transaction de création (`fePxr7ER…`, 02:05:25Z). Il contient :
     - `name` = « Dark MAGA »
     - `symbol` = « DMAGA »
     - `uri` = `ipfs/QmVYQ4HjjYW2SmswB5n5qnEfRAUY4e6Cy1Vqf4o6yZCTLK`
   - Le fichier de métadonnées contient :
     - `description` : « Dark MAGA patriots in control. »
     - `image` : `QmPkBk2iNbXVn75C1xykV2xbHGupbM3gHkJEy7r5ZEEiPi`
   - Cette image est **identique au pixel près** à la photo de profil de @DarkMagaCoin (media `1812303793645666304`) : distances pHash, dHash et aHash toutes égales à 0, format 366×366.
   - La description reprend mot pour mot le slogan de la bio DMC.
   - La photo de profil a été téléversée **avant** le mint : snowflake 01:51:10Z et en-tête HTTP `Last-Modified` 01:49:10 GMT.
   - Il reste une explication alternative : une image source commune. Elle n'est pas exclue (voir §7).
2. **G41v a tenté deux achats sur pump.fun 29 s et 45 s après le mint — A pour le fait, NEW.** G41v est le bailleur des 13 transferts de 0,5 SOL.
   - Les deux transactions ont échoué pour cause de slippage (`AnchorError 6002 TooMuchSolRequired`) :
     - `5y7rbp2MPWukH3…` à 02:05:54Z
     - `39nfmzR12cVHaM…` à 02:06:10Z
   - Ces deux échecs sont absents du repo.
   - Une minute plus tard, G41v a envoyé 5 SOL à GFpqfj (02:06:57Z). Il a ensuite acheté 3,08 M DMAGA via Jupiter à 02:28:26Z (KNOWN).
   - **Ce que cela établit** : le bailleur des wallets précoces a été lui-même acheteur dans la première minute.
   - **Ce que cela n'établit pas** : une connaissance préalable du mint. Un sniper automatisé peut agir aussi vite.
3. **Premier post DMC corrigé — A, NEW.**
   - Le post supprimé `1812312706826854843`, publié à **02:26:35Z**, dit : « We are live Patriots! ca: 7D7B…pump » et contient une invitation Telegram privée.
   - La capture Wayback (20240714022635) montre l'état du compte à ce moment : 1 abonné, 0 abonnement, `tweet_count` = 1.
   - Le repo date le premier post à 03:00:28Z ; cette date est donc à corriger.
   - Ce résultat affaiblit aussi l'affirmation d'Aristos (oct. 2024) selon laquelle le projet aurait été lancé « deux jours avant Butler » — niveau C.
4. **Liste tierce d'« early buyers » par @ChoupetteJoe, 2024-07-23 14:57Z — B, NEW.**
   - Elle compte 19 adresses : 10 font partie du groupe de 33 wallets du repo, dont 7 destinataires de G41v.
   - Les 9 autres adresses sont de nouvelles pistes.
   - C'est une identification contemporaine et indépendante du cluster, mais **pas une attribution**.
5. **Le ticker « $DMAGA » et la méta « Dark MAGA » existaient avant le token — B, NEW.**
   - Un token ERC-20 `0x4F45D4F1244B22feeB7Bd5409A7B6A777Df714b5` était associé au compte @DARKmagaERC (annonce Moontok du 2024-05-26 15:56:53Z).
   - @DarkMaga_Solana était mentionné le 27/05.
   - @JayDubb365 a posté le 2024-06-01 à 02:29:05Z : « $DMAGA Dark Maga is the meta ».
   - Par ailleurs, l'expression « Dark MAGA » circulait organiquement entre 00:00 et 02:00Z le 14/07, après la tentative d'assassinat de Butler et avant le mint.
   - Ces éléments soutiennent l'hypothèse d'un lancement **opportuniste**.
6. **Déclarations tierces sur l'équipe — C, NEW.**
   - @kanpai, 30/08 14:01:32Z : « @kikisknees — he's the lead of the project ».
   - @Murray_Gothbard, 30/08 07:38:24Z : « my friend developed the token ».
   - @koreanjewcrypto, 17/08 : « Hit 1000x+ on dmaga like a month ago ».
7. **Résultats nuls utiles — A.**
   - Le créateur (972 signatures, historique complet) et G41v (416 signatures, historique complet) n'ont **aucune transaction commune**.
   - Aucun compte cœur n'a publié d'adresse de wallet.
   - Le lien wallet ↔ compte X reste donc **technique (via l'image et le CA), et non financier**.

---

## 2. Chronologie vérifiable (UTC)

| Horodatage UTC | Événement | Source | Niveau | Statut |
|---|---|---|---|---|
| 2024-05-26 15:56:53 | Annonce Moontok d'un token ETH « $DMAGA » (@DARKmagaERC) | X 1794759622026486139 | A | NEW |
| 2024-06-01 02:29:05 | @JayDubb365 : « $DMAGA Dark Maga is the meta » | x07/x14 | A | NEW |
| 2024-06-11 | Création du compte @DarkMagaCoin (id 1800564812889325568) | x01 | A | KNOWN |
| 2024-07-13 ~22:11 | Tentative d'assassinat de Trump à Butler | public | A | KNOWN |
| 2024-07-14 00:00–02:00 | Dizaines de posts « Dark MAGA » organiques | x24 | B | NEW |
| 2024-07-14 00:41:12 | @kikisknees relaie @CryptoOnlyCoims « Dark MAGA Has Begun » | x23/x09 | A | PARTIAL |
| 2024-07-14 01:16 → 02:45 | Aucun post de @kikisknees retrouvé | x03/x09 | C | NEW |
| 2024-07-14 01:32:23 | Le créateur 8YLE reçoit 0,5 SOL de Coinbase 3 | rpc_sigs_8YLE | A | KNOWN |
| 2024-07-14 01:46:23 → 02:03:38 | G41v envoie 13 × 0,5 SOL | rpc_g41v_window_txs | A | KNOWN |
| 2024-07-14 01:49:10 / 01:51:10 | Téléversement de la pfp DMC (Last-Modified / snowflake) | media/ | A | NEW |
| 2024-07-14 01:57:02 | Création du canal Telegram | repo | A | KNOWN |
| 2024-07-14 02:05:25 | Mint ; métadonnées = image et slogan DMC | rpc01 + IPFS | A | NEW (contenu) |
| 2024-07-14 02:05:54 / 02:06:10 | Deux achats de G41v sur pump.fun échouent (slippage 6002) | rpc_g41v_window_txs | A | NEW |
| 2024-07-14 02:06:57 | G41v envoie 5 SOL à GFpqfj | idem | A | KNOWN |
| 2024-07-14 02:11:17 / 02:16:00 | G41v envoie 2 SOL puis 4 SOL à AW63YBXX | idem | A | KNOWN |
| 2024-07-14 02:15:31 | Migration vers Raydium | repo | A | KNOWN |
| 2024-07-14 02:26:35 | Premier post DMC « We are live Patriots! » avec le CA (supprimé depuis) | Wayback | A | NEW |
| 2024-07-14 02:28:26 | G41v achète 3,08 M DMAGA via Jupiter | rpc | A | KNOWN |
| 2024-07-14 02:33:53 | Signal du bot @adamjia7 (fdv $97,451) | x26 | A | NEW |
| 2024-07-14 02:45:55 | @kikisknees retweete « We are live » (1812317575411351639) | x03 | A | PARTIAL |
| 2024-07-14 03:00:28 | Premier post DMC **survivant** | x02 | A | KNOWN |
| 2024-07-14 03:31:32 | dmaga.xyz capturé (liens TG privé, X, DexScreener) | Wayback | A | KNOWN |
| 2024-07-14 03:55:58 | @thecryptoms sollicite Musk | x10 | A | NEW |
| 2024-07-14 04:07:26 | @kikisknees cite le post DMC à l'adresse de @AutismCapital | x03 | A | PARTIAL |
| 2024-07-14 16:47 | Telegram « Dark MAGA Verification Portal », 6 abonnés | Wayback | A | KNOWN |
| 2024-07-16 02:43:07 | @koreanjewcrypto : « haven't sold a single $dmaga » | x20 | A | PARTIAL |
| 2024-07-21 16:00:08 | @kikisknees répond à Musk (média perdu) | repo | A | KNOWN |
| 2024-07-21 16:02:29 | @ChrisWinig « It's time, Elon » (pHash 0 avec l'avatar de Musk) | repo | A | KNOWN |
| 2024-07-21 16:00–19:21 | Sollicitations de Musk : FrancoAppr, EeOo111_, FrankButcher81 (×4), Bitcoin_is_king, Murray_Gothbard | x10/x28 | A | NEW |
| 2024-07-21 19:03:27–19:25:23 | Musk change d'avatar (fenêtre), upload à 19:23:20 | repo | A | KNOWN |
| 2024-07-21 19:39:29 | @koreanjewcrypto : « dmaga ppl made it for me » | x20 | A | KNOWN |
| 2024-07-22 08:10:21 | DMC : « DMAGA team created Elon's pfp… DMed » | repo | A (déclaration) | KNOWN |
| 2024-07-23 02:14–02:16 | G41v, C73Yv, AtZjv et EGtyQ envoient ~8 SOL chacun à 9W9b | repo | A | KNOWN |
| 2024-07-23 14:22:30 | DMC : « The team is still here… The dev is still here » | x31 | A | KNOWN |
| 2024-07-23 14:57:13–14 | Fil @ChoupetteJoe : 19 « early buyers » | x22 | A | NEW |
| 2024-07-24 06:40:49 | DMC : « We sent him the meme and he liked it » | repo | A (déclaration) | KNOWN |
| 2024-08-14 | @ChrisWinig : « Barron and now JD Vance are sending our edits to Trump » | x05 | A (déclaration) | NEW |
| 2024-08-17 | @koreanjewcrypto : « Hit 1000x+ on dmaga » | x20 | A (déclaration) | NEW |
| 2024-08-30 07:38:24 | @Murray_Gothbard : « my friend developed the token » | x25 | A (déclaration) | NEW |
| 2024-08-30 14:01:32 | @kanpai : « @kikisknees — he's the lead of the project » | x21 | A (déclaration) | NEW |
| 2025-07-06 | 5QhJJc envoie 0,032 SOL au créateur 35 s avant sa vente DCA | repo | A | KNOWN |

Pour une déclaration, le niveau A porte sur l'**existence** du post, pas sur la véracité de son contenu.

---

## 3. Graphe des relations publiques

```mermaid
graph LR
  CB[Coinbase 3] -->|0,5 SOL 01:32Z — financier A| CR[8YLE créateur]
  CR -->|mint 02:05Z — A| TOK[(DMAGA 7D7B…pump)]
  TOK -.->|image + slogan identiques — technique B| DMC[@DarkMagaCoin]
  DMC -->|CA publié 02:26Z — publication directe A| TOK
  G41[G41v] -->|13×0,5 SOL 01:46–02:03Z — financier A| GRP[Groupe 33 wallets]
  G41 -->|achats échoués 02:05:54/02:06:10 puis achat 02:28Z — A| TOK
  G41 -->|5 SOL| GF[GFpqfj]
  G41 -->|~8 SOL 23/07| X9[9W9b sortie]
  CR -->|SOL 26/01/2025| X9
  CHO[@ChoupetteJoe] -.->|liste 10/19 adresses — identification tierce B| GRP
  KIKI[@kikisknees] -->|RT 02:45Z, QT 04:07Z — social| DMC
  KIKI -.->|« pfp by me and @ChrisWinig » — déclaration| MUSK[@elonmusk avatar]
  WIN[@ChrisWinig] -->|« It's time, Elon » pHash 0| MUSK
  DMC -.->|« team created Elon's pfp… DMed » — déclaration non prouvée| MUSK
  KAN[@kanpai] -.->|« lead of the project » — C| KIKI
  MUR[@Murray_Gothbard] -.->|« my friend developed » — C| CR
  KJ[@koreanjewcrypto] -.->|« made it for me », « 1000x » — C| DMC
  ARI[@Aristos_Revenge] -.->|« kiki launched DMC… » (supprimé) — D/C| KIKI
  CR -. aucune tx commune — nul A .- G41
```

Légende :
- Flèche pleine : fait vérifié on-chain ou sur X.
- Flèche pointillée : déclaration, correspondance ou identification tierce.
- **Aucune arête financière** ne relie un compte X à un wallet.

---

## 4. Tableau des correspondances sociales / on-chain

| # | Élément social | Élément on-chain | Type de lien | Niveau | Statut |
|---|---|---|---|---|---|
| 1 | Pfp @DarkMagaCoin `1812303793645666304` | Image IPFS `QmPkBk2…` dans l'URI de la tx de création signée par 8YLE | correspondance technique | B | NEW |
| 2 | Bio DMC « Dark MAGA patriots in control » | `description` des métadonnées du mint | correspondance technique | B | NEW |
| 3 | Post DMC 1812312706826854843 (02:26:35Z) | CA 7D7B…pump | publication directe d'adresse (du CA, pas d'un wallet) | A | NEW |
| 4 | Pfp DMC téléversée à 01:49–01:51Z | Mint 02:05:25Z ; G41v actif 01:46–02:03Z | coïncidence temporelle | C | NEW |
| 5 | Fil @ChoupetteJoe (4 posts) | 10 wallets du groupe de 33, dont 7 financés par G41v ; 9 hors groupe | identification tierce | B | NEW |
| 6 | DMC « dev is still here » (23/07 14:22Z) | Sortie de G41v et du groupe vers 9W9b (23/07 02:14Z) ; aucune vente du créateur avant juil. 2025 | contradiction conditionnelle | C | PARTIAL |
| 7 | @Murray_Gothbard « my friend developed the token » | 8YLE (opérateur inconnu) | revendication tierce | C | NEW |
| 8 | @kanpai « kiki lead of the project » | — | revendication tierce | C | NEW |
| 9 | @koreanjewcrypto « 1000x+ » | aucun wallet publié | revendication d'entrée précoce | C | NEW |
| 10 | Listes « insiders » H3Qs (dès 30/07) et 9PrmF8 (@0xbeehive 13/08 22:38:02Z) | H3Qs : smart money multi-tokens | mention tierce | C | NEW / KNOWN (cryptosymbiiote) |
| 11 | @kkashi_yt mentionne 5QhJJc (dès 22/07) | 5QhJJc → créateur (2025) | mention tierce | C | PARTIAL |
| 12 | Aucun compte cœur | 8YLE, G41v, 7GVC, 9W9b absents de X | résultat nul | — | NEW |

---

## 5. Matrice d'attribution

| Rôle | Acteur (pseudonyme) | Rôle démontré | Sources | Niveau | Relations | Liens on-chain | Contradictions | Pistes |
|---|---|---|---|---|---|---|---|---|
| Créateur technique | **8YLEuUtZ…** (opérateur inconnu) | A signé le mint ; 0,2 SOL → 7,1 M tokens ; aucune vente avant juil. 2025 | rpc01, repo | A (wallet) | Ses métadonnées reprennent l'image et le slogan de DMC | Coinbase 3 → 8YLE ; 9W9b (2025) ; 5QhJJc | — | Recherche inverse de l'image ; dépôts Coinbase (non publics) |
| Opérateur probable du compte de lancement | **@DarkMagaCoin** | Publie le CA 21 min après le mint ; même image et même slogan que les métadonnées | Wayback, media, IPFS | **B** (lien DMC ↔ créateur) | kiki (RT/QT), Winig, Esoviz (« media team lead »), KJ | aucun wallet publié | « premier post 03:00 » (repo) contredit ; « dev is still here » vs sortie de G41v | Captures du profil antérieures à 02:26Z |
| Bailleur précoce | **G41vRrsH…** | 13 × 0,5 SOL avant le mint ; achats tentés à +29 s et +45 s ; achat à 02:28Z | rpc_g41v_window_txs | A (financier) | aucune tx commune avec 8YLE | GFpqfj, AW63YBXX, 9W9b, 13 destinataires | — | Graphe des contreparties à 2 sauts entre 8YLE et G41v |
| Organisateur public / « lead » présumé | **@kikisknees** | RT/QT de DMC dans les 40 min ; revendique la pfp de Musk « with @ChrisWinig » | x03, x09, x33, repo | B (relais) / C (lead) | Winig, DMC, Aristos, kanpai, Coims | aucun | Muet de 01:16 à 02:45Z ; Aristos (« launched 2 days before Butler ») réfuté par les posts survivants | Posts supprimés (Wayback) |
| Créateur du visuel Musk | **@ChrisWinig** | « It's time, Elon » 16:02:29Z, pHash 0 ; « Thanks, I made it » | repo, x05 | B | kiki, DMC | aucun | ouï-dire « Barron/JD Vance » | Fichiers sources, EXIF (non publics) |
| Équipe média | **@Esoviz** | Désigné « media team lead » par DMC (13/08) | x16 | C | DMC | aucun | — | Vérifier son activité en juillet |
| Promoteur / soutien | **@Aristos_Revenge** | Fil d'oct. 2024 (supprimé) : « kiki launched DMC » | repo pass3 | D (non retrouvé par l'API) | kiki | aucun | chronologie démentie par N03 | Wayback du fil |
| Promoteur / soutien | **@koreanjewcrypto** | « in our corner from DAY ONE », « made it for me », « 1000x+ » | x20, repo | C | DMC, kiki, Winig | aucun | 1er post public DMAGA le 15/07, mais revendique une entrée précoce | — |
| Relais | **@CryptoOnlyCoims** | « Dark MAGA Has Begun » (avant 00:41Z), « Just bought 1 SOL » 03:20:42Z | x23 | B (relais) | kiki | aucun | — | Post exact avant 00:41Z |
| Relais / revendication | **@Murray_Gothbard** | Sollicite Musk 21/07 ; « my friend developed the token » | x25, x28 | C | — | aucun | — | Identité de « friend » |
| Relais | **@kanpai** | « kiki lead of the project » ; « Elon removed his pfp » | x21 | C | kiki | aucun | — | — |
| Bot de signaux | **@adamjia7** | Signal VIP automatisé à 02:33:53Z | x26 | B | — | aucun | — | — |
| Traders précoces | 33 wallets / 40 transferts ; 15 acheteurs en 1 h | Achats précoces | repo, Choupette | A (on-chain) / B (identification tierce) | G41v | 9W9b | — | 9 adresses Choupette hors groupe |
| Bénéficiaires des profits | H3Qs (5 491 SOL), GXZvX (2 540), 9PrmF8 (1 748), deBridge 263 573 USDC | Profits réalisés | repo | A (montants) | listes « insiders » tierces | — | H3Qs = smart money multi-tokens (hypothèse H4) | — |

---

## 6. Hypothèses réfutées ou affaiblies

| Hypothèse | Verdict | Niveau | Base |
|---|---|---|---|
| « DMC lancé deux jours avant Butler » (Aristos) | Affaiblie : `tweet_count` = 1 à 02:26Z, 21 min après le mint ; la seule antériorité démontrée est la création du compte le 11/06 | C/D | N03, N04 |
| « Premier post DMC à 03:00:28Z » (repo) | Réfutée : 02:26:35Z | A | Wayback |
| @adamjia7 serait un organisateur | Réfutée : c'est un bot de signaux | B | x26 |
| Le ticker DMAGA aurait été inventé par cette équipe | Réfutée : ETH $DMAGA en mai 2024 et méta pré-existante | B | x14, x19 |
| Le créateur et G41v partageraient des transactions directes | Non observé dans les historiques complets (lien indirect non exclu) | A (nul) | N06 |
| Un contact direct avec Musk serait prouvé | Non prouvé : seules existent les déclarations DMC et KJ | D | repo, x16 |
| Scénario « connaissance non publique préalable » du changement d'avatar par Musk | Aucun élément : sollicitations publiques massives dès 16:00Z ; repo : DMAGA ne se distingue pas statistiquement de ses pairs (p = 0,156) | D | x10, repo |

Les quatre scénarios de la campagne Musk (14–23/07) :
1. **Campagne publique** : fortement corroborée (B). Les comptes kiki, Winig, Murray et FrankButcher81 ont multiplié les sollicitations publiques entre 16:00 et 19:21Z.
2. **Adoption spontanée** par Musk : compatible et non réfutée (C).
3. **Coordination financière préexistante** : le groupe G41v existait bien dès le lancement (A). En revanche, aucun flux spécifique lié à l'avatar n'est démontré : le repo ne trouve pas d'anomalie statistique.
4. **Connaissance non publique préalable** : aucun indice (D).

---

## 7. Preuves manquantes

- **Une image source commune antérieure** pour la pfp ou le token : une recherche inverse avant 01:49Z le 14/07 n'a pas été faite. Si une source antérieure existe, le lien N01 tombe au niveau C.
- **Les posts supprimés** de DMC, kiki et Aristos : seuls quelques-uns ont été capturés par Wayback.
  - Le média de la réponse de kiki à Musk (16:00:08Z) est perdu.
  - Le fil d'Aristos d'oct. 2024 est introuvable via l'API (x04 et x29 renvoient 0).
- **L'API frontend de pump.fun** (créateur, réponses, trades) : bloquée par Cloudflare (403). Nous ne l'avons pas contournée.
- **Une preuve de DM à Musk** : inexistante publiquement. Les DM sont privés et hors périmètre.
- **Une arête financière entre un compte X et un wallet** : aucun compte cœur n'a publié d'adresse.
- **Le lien 8YLE ↔ G41v** : il n'est observé que par coïncidence temporelle, pas par une transaction commune.
- **Les identités civiles** : aucune n'est publique et liée au rôle de façon fiable. **Aucune n'est retenue.**

---

## 8. Prochaines pistes, par priorité

1. **Recherche inverse de l'image `QmPkBk2…`** (TinEye, Google Lens, Yandex) avec un filtre « avant le 2024-07-14 01:49Z ». C'est le test décisif pour N01.
2. **Contreparties à 2 sauts entre 8YLE et G41v**, en remontant le financement de G41v (premier dépôt le 2023-12-26 17:17:02Z) et les CEX communs.
3. **Délai des snipers** : mesurer le temps entre création et premier achat pour les tokens pump.fun créés entre 01:00 et 03:00Z le 14/07. Cela dira si les +29 s de G41v sont atypiques.
4. **Les 9 adresses Choupette hors groupe** : identifier leur financement et vérifier si elles partagent une sortie avec 9W9b.
5. **Wayback** : passer au CDX les profils et statuts de @kikisknees, @Aristos_Revenge et @DarkMagaCoin entre le 11/06 et le 14/07.
6. **Token ETH $DMAGA** : regarder le déployeur `0x4F45…14b5` et les éventuels bridges vers Solana avant juillet.
7. **Post @CryptoOnlyCoims « Dark MAGA Has Begun »** : en retrouver l'ID et l'heure exacts, ainsi que le contexte de @FrankButcher81 et de @Esoviz.

---

## 9. Sources (UTC, archives)

**Posts X** (URL au format `https://x.com/i/status/<id>`, heures vérifiées par snowflake)
- 1812312706826854843 — DMC « We are live », 2024-07-14T02:26:35Z (supprimé). Archive : `web.archive.org/web/20240714022635/…`
- 1812317575411351639 — kiki RT, 2024-07-14T02:45:55Z
- 1812333956131344692 — DMC « You cannot kill Dark MAGA », 2024-07-14T03:51:01Z
- 1813041645899649082 — KJ, 2024-07-16T02:43:07Z
- 1815754363937124607 — DMC « dev is still here », 2024-07-23T14:22:30Z
- 1815763101196636373, 1815763103063105655, 1815763104954769560, 1815763106770915673 — fil @ChoupetteJoe, 2024-07-23T14:57:13–14Z
- 1794759622026486139 — Moontok ETH $DMAGA, 2024-05-26T15:56:53Z
- 1823536895017599048 — Winig « Barron… JD Vance », 2024-08-14
- 1824912728194248754 — KJ « 1000x+ », 2024-08-17
- 1828679073822134552 — kanpai « Elon removed his Dark MAGA pfp »
- 1829423407915466966 — Murray « my friend developed the token », 2024-08-30T07:38:24Z
- 1829519827268153602 — kanpai « lead of the project », 2024-08-30T14:01:32Z
- Les autres posts sont dans `raw/x*.json`.

**On-chain** (RPC `api.mainnet-beta.solana.com`)
- Création : `fePxr7ER…`, slot 277417695 (`raw/rpc01_create_tx.json`)
- Achats échoués de G41v :
  - `5y7rbp2MPWukH3R1jSHCHvesrGAwyFbfT84RAH7wonyMUqCDoEu13Mi6DSb5pvoHhpzsnofGsrgijjK8avtPuTnG`
  - `39nfmzR12cVHaMd2EtoHvTmcNDCKFfKPkbmjXcnRXXLH6o5QmvtTnLJseeDTqegtN65MdttuP5B5qd4T8npEUXfG`
- Achat Jupiter de G41v : `5LiTyoCxVPNULBHtKvAY8LkLweP9XvHgFaAacjxj5n93ucsmxUWt4DV9RBBDhq13wTuuoXH1rApcwdoYc1vmh782`
- Historiques complets : `raw/rpc_sigs_8YLEuUtZ.json`, `raw/rpc_sigs_G41vRrsH.json`

**IPFS**
- Métadonnées : `QmVYQ4HjjYW2SmswB5n5qnEfRAUY4e6Cy1Vqf4o6yZCTLK`
- Image : `QmPkBk2iNbXVn75C1xykV2xbHGupbM3gHkJEy7r5ZEEiPi` (passerelle Pinata)

**Wayback**
- dmaga.xyz : captures 20240714033132 et 20240723093256
- t.me/DMAGACoin : capture 20240714164733
- pump.fun : capture 20240717110654 (« Token not found »)

**Repo**
- `searadacunha/DARK-MAGA` @ `1b15817c` : COORDINATION.md, historical_replay, pass3

**Journaux et données**
- `raw/query_log.tsv`
- `assertions.json` et `assertions.csv`