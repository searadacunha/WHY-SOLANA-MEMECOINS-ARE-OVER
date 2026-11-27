# Suivi social et documentaire, Dark MAGA ($DMAGA)

> **Erratum du 03/11.** Ce rapport a été relu sur le brut par un relecteur adverse : aucun constat central ne tombe, mais plusieurs chiffres et phrases sont faux ou trop forts (le résumé « contredit », `$DMAGA` coupé dans une liste). `audits/2026-11-03/work_I/REFUTATION.md` fait foi. Le rapport d'origine n'est pas réécrit.

Collecte du 03/11/2026, de 10:05 à 11:16 UTC, coupure forcée par une limite d'usage, puis reprise de 13:31 à 14:00 UTC environ. Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Heures en UTC.
Personne n'est accusé. Aucune identité civile n'est recherchée. Les pseudos désignent des comptes, pas des personnes établies.

Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice, **D** non vérifié ou contredit.
**FAIT** observé dans un fichier sauvegardé, **DÉCLARATION** ce qu'un compte affirme, **HYPOTHÈSE** à vérifier.
Preuves : `evidence/`, `evidence_manifest.jsonl` (url, heure de collecte, sha256), `x_posts_new.jsonl` (170 posts lus en direct, 1249 textes de posts supprimés lus dans la Wayback), `x_search_log.jsonl` (les 30 recherches X), `tools/`.

## 1. Ce qui change le dossier

1. **La chronologie du visuel recule de plus de 3 heures.** La plus ancienne image connue du visuel de Musk n'est plus @ChrisWinig à 16:02:29. C'est @kikisknees à **12:50:45**, en réponse à @pmarca (variante rouge sans drapeau). L'image exacte de l'avatar est publiée par @FrancoAppr à **16:00:59**, 90 s avant @ChrisWinig. Le plus ancien envoi connu de cette famille à Musk est @GreatBambin0 à **15:58:21**.
1. **@kikisknees vise Musk avec le ticker dès le 18/07.** À 22:22:13, en réponse à @elonmusk : « We are building an army for you for that purpose. $DMAGA », avec une image de Musk aux yeux laser (autre composition, publiée dès le 16/07 par @FrancoAppr). Trace publique et datée, trois jours avant l'avatar. Rien ne montre que Musk l'a vue.
2. **L'image perdue de 16:00:08 est retrouvée.** Ce n'est pas Musk. C'est le Trump « dark maga » de @DarkMagaCoin, même fichier au sha256 près.
3. **Les images de @kikisknees ne sont pas perdues.** La Wayback les garde sous `pbs.twimg.com/media/<clé>?format=...&name=orig`. Il faut une CDX avec joker. 17 images récupérées.
4. **@pmarca a repris une image de @kikisknees, c'est visible sur son post.** Réponse de @kikisknees le 20/07 à 19:05:03, post de @pmarca à 20:46:54 avec un lien vers ce statut, même image (pHash 0).
5. **« Lancé deux jours avant Butler » est contredit par toutes les dates objectives lues** (compteur du compte X, certificat du site, Telegram, avatar, mint, 167 posts de @kikisknees sur 187 entre le 11/07 et le tir).
6. **La source sociale de `9PrmF8…` est retrouvée**, et une trace plus ancienne : @XHEILIGX publie cette adresse le 30/03/2024, puis promeut $DMAGA. Indice de niveau C, pas une attribution.
7. **Défaut du corpus : 372 lignes sur 5155 de `data/x_posts.jsonl` ont une date fausse dans `created_utc_snowflake`.** Leur id est celui d'un repost, le texte et la métadonnée sont ceux de l'original. Le dossier écrit que les deux dates sont toujours égales. Cela touche des lignes de `docs/TIMELINE.md`, voir partie 7.

## 2. Question 1, chronologie du visuel

Quatre images, comparées à l'œil et par pHash (méthode de `scripts/ana_40_visual.py`, table `derived/visual_new.csv` et `derived/visual_wb.csv`) :
- **V0**, Musk aux yeux laser devant une foule de Pepe, 1125 x 1003. Autre photo, autre composition. Pas l'avatar.
- **V1**, rouge uni, armure, sans drapeau, 900 x 900. pHash 14 à 16 avec l'avatar, 2 entre l'image de @kikisknees et celle de @EeOo111_. Le seuil de 12 du dépôt ne la classe pas comme proche.
- **V2**, avec drapeau, gauche bleue et violette, 1024 x 1024. pHash 0 et dHash 0 avec l'avatar de Musk. C'est l'image identique.
- **V3**, avec drapeau, tout rouge, 900 x 900.

| UTC | Compte | Variante | Destinataire | Niveau |
|---|---|---|---|---|
| 16/07 20:32:13 | @FrancoAppr `1813310692243480937` | **V0**, Musk aux yeux laser, autre composition (foule de Pepe), ni V1 ni V2, 1125 x 1003 | @elonmusk | A pour la date, C pour un lien avec l'avatar |
| 18/07 22:22:13 | @kikisknees `1814063148917256375` | même image de Musk aux yeux laser, pHash 0, image retrouvée | @elonmusk, « We are building an army for you for that purpose. $DMAGA » | A |
| 21/07 12:50:45 (image envoyée à 12:50:21) | @kikisknees `1815006501896872388` | **V1, la plus ancienne connue** | @pmarca, « Is Elon mooning with us? » | A |
| 15:58:21 | @GreatBambin0 `1815053713330876681` | V1 | @elonmusk, « There's only one option Elon » | A |
| 16:00:49 | @GreatBambin0 `1815054330740785513` | V1 | @elonmusk | A |
| **16:00:59** | @FrancoAppr `1815054374982324401` | **V2, la plus ancienne identique connue** | @elonmusk, « Time to join Dark MAGA » | A |
| 16:01:01 | @EeOo111_ `1815054381823221968` | V1 | @elonmusk, « Whoa, ELON IN DARK MAGA » | A |
| 16:01:29 | @GreatBambin0 `1815054499955777575` | V1 | @elonmusk | A |
| 16:02:29 | @ChrisWinig `1815054750775173447` | V2, ancienne référence du dossier | @elonmusk | A |
| 16:12:38 | @DarkMagaCoin `1815057307836842034` | V1, premier envoi du compte du jeton trouvé | @elonmusk, « Based GC members: » | A |
| 16:32:02 | @GreatBambin0 `1815062189763703119` | V3, la plus ancienne connue | @elonmusk | A |
| 17:54 à 18:48 | @GreatBambin0, 5 posts | V3 | @elonmusk | A |
| 18:31:46 | @FrancoAppr `1815092319244128645` | V2 | @elonmusk, « A changed Elon could use a changed profile picture » | A |
| 18:40:09 | @Murray_Gothbard `1815094431152029711` | V2 | @elonmusk | A |
| 18:46:37 | @kikisknees `1815096055337496944` | V3, image retrouvée | @elonmusk | A |
| 19:23:20 | @elonmusk, id d'avatar `1815105297410666496` | V2 | | B pour l'heure, voir le contrôle |

**La réponse de @kikisknees à 16:00:08** (`1815054158367432804`) : image retrouvée, clé `GTBeEjGXgAAbn4S`, capture Wayback du 22/07/2024 21:16:26. Son sha256 commence par `cce3b01b` et égale celui des images de @DarkMagaCoin du 17/07 (`1813683527575302497`) et du 20/07 (`1814719737378607482`). C'est Trump en rouge avec le texte « dark maga ». **FAIT, A : ce n'est pas le visuel de Musk.** Même fichier pour `1815116385414209876` à 20:07:24 (« That's a $DMAGA pfp, made by me. »). Cette dernière phrase ne montre donc pas l'image de Musk.

**Chaîne @kikisknees vers @pmarca**, FAIT, A :
- 20/07 19:05:03 : @kikisknees répond à @pmarca (`1814738306589917312`), texte lu dans `evidence/x_wayback/1815123417064255531.raw`, image `GS8-wUDWMAAqpGm` retrouvée, Charlie Brown rouge.
- 20/07 20:46:54 : @pmarca publie `1814763940410499481`. Même image, pHash 0. Le post contient le lien `/kikisknees/status/1814738306589917312`, visible dans le navigateur (`evidence/x_screens_pmarca_1814763940410499481_recadre.jpg, version recadrée pour retirer le compte connecté, original conservé hors de git`), le post cité est marqué indisponible.
- 21/07 07:04:09 : id du nouvel avatar de @pmarca. 07:08:26 : « THAT'S RIGHT. » (`1814920352134537332`).

**Contrôle de la lecture « id d'avatar = heure d'envoi »**, marquée à confirmer dans le dossier. Sur les captures API v2 lues, de plusieurs centaines de comptes, chaque avatar est vu après son id (787 cas sur 787, 0 contraire) et chaque ancien avatar est vu avant l'id du suivant (67 cas sur 67, 0 contraire). `tools/avatar_control.py`, `derived/avatar_changes.json`. Niveau B, l'heure du clic reste inconnue. Ce même fichier date d'autres changements : @BasedTorba 20/07 19:05:51, @poosseau 21/07 13:20:32, @notsofast 13:36:46, @Aristos_Revenge 17:36:50, @koreanjewcrypto 19:43:31, @twicrates 23:45:38. L'id date un envoi d'avatar, pas son contenu.

**Reste inconnu.** Un post avec image seule, sans mot-clé, ne ressort pas d'une recherche X : une occurrence antérieure de V1 ou V2 reste possible. La grande majorité des 164 images 900 x 900 de @kikisknees antérieures au 21/07 12:51 ne sont pas lues, seuls leurs textes le sont. L'auteur du fichier V2 n'est pas établi : @kikisknees écrit « $DMAGA pfp by me and @ChrisWinig » (DÉCLARATION). @FrancoAppr, @ChrisWinig et @Murray_Gothbard publient chacun un 1024 x 1024 de pHash 0, comme le IMG_5658 de la capture de @DarkMagaCoin (1024 x 1024, 235 Ko, 06:17, fuseau inconnu) : HYPOTHÈSE d'un fichier partagé avant 16:00:59. Le format 900 x 900 de V1 est celui des pfp faits par @kikisknees, celui de V2 ne l'est pas : c'est compatible avec « by me and @ChrisWinig », sans le prouver (C). Ce que Musk a vu n'est pas établi.

## 3. Question 2, publications avant l'adoption

**@DarkMagaCoin.** La recherche native `from:DarkMagaCoin until:2024-07-14` ne rend que 12 reposts. FAIT, A : la capture du repost de @kikisknees à 02:45:55 le 14/07 donne le premier post propre, `1812312706826854843`, à **02:26:35** (« We are live Patriots! », avec le mint), et non 03:00:28. Elle donne aussi les compteurs du compte à cet instant : 1 post, 0 abonnement, 0 like, 7 abonnés. À 04:07:26 : 6 posts. Avant l'avatar, ni la recherche `from:DarkMagaCoin elon` ni `data/x_posts.jsonl` ne contiennent de texte propre du compte avec « elon » ou « musk ». Le compte reposte @kikisknees à 16:02:54 et @ChrisWinig à 16:04:53, puis envoie V1 à Musk à 16:12:38. « GC » répond au post de Musk « 𝕏 is the group chat for Earth » (`1807491298015768981`) : ne pas y lire un groupe privé.

**@ChrisWinig.** Le CDX reste vide (`[]`, retesté). La recherche native comble ce trou : 106 lignes rendues du 01/06 au 22/07, doublons compris, sans aucune mention de DMAGA, Dark MAGA ou Musk avant Butler. Vidéos à 23:05:26 et 23:40:42 le 13/07, après le tir. Première publication du mint par ce compte : `1813680552031195437`, 17/07 21:01:54. Citation de lui par @DarkMagaCoin cinq minutes plus tard (déjà au dossier).

**@kikisknees.** Ses posts propres de 2024 sont presque tous supprimés : la recherche native n'en rend qu'un, du 04/06 (`1798040845041709555`). Ses reposts restent visibles. Couverture Wayback ci-dessous. Sur 453 posts lus du 11/06 au tir de Butler : 0 mention de « Dark MAGA » ou « DMAGA », 0 ticker écrit par lui. Mentions de Musk écrites par lui sur cette période : 0. Attention, du 11/06 au 10/07 la lecture reste partielle, voir la table.

Premières réponses de @kikisknees qui nomment @elonmusk après Butler, parmi les textes lus ici :
- `1814063148917256375` 2024-07-18T22:22:13Z : « @elonmusk "Freedom & merit is what America should be about." We are building an army for you for that purpose. »
- `1814468452024766699` 2024-07-20T01:12:44Z : « @elonmusk @growing_daniel Hell yeah https://t.co/y2Lu5h31l1 »
- `1814705312219213971` 2024-07-20T16:53:56Z : « @elonmusk What did he mean by this? https://t.co/iwoBjxkBAp »
- `1814705414325354820` 2024-07-20T16:54:21Z : « @elonmusk Yes, let's do it. #DarkMAGA https://t.co/VDZCWbcC0l »
- `1814863915186016702` 2024-07-21T03:24:10Z : « @FoxNews @elonmusk Building an army for $DMAGA IS smart. https://t.co/mUTWTgeIGY »

| Fenêtre | Ids CDX | Lus avant le 03/11 | Lus ici | Restent |
|---|---|---|---|---|
| 11/06 au 10/07 | 1592 | 0 | 286 | 1306 |
| 11/07 au 13/07 22:11 (avant Butler) | 187 | 0 | 167 | 20 |
| 13/07 22:11 à minuit | 10 | 0 | 10 | 0 |
| 14/07 au 19/07 | 780 | 67 | 659 | 54 |
| 20/07 au 21/07 12:51 | 136 | 2 | 126 | 8 |
| 21/07 12:51 au 22/07 07:00 | 150 | 139 | 0 | 11 |
| 22/07 07:00 au 26/07 | 379 | 0 | 0 | 379 |

**Traces datées d'une intention de cibler Musk.** Toutes sont publiques, aucune n'établit un plan de l'équipe :
- 16/07 20:32:13 : @FrancoAppr répond à Musk avec une image de Musk aux yeux laser. Il répond à Musk avec des images rouges dès le 15/07 19:31:46 (`1812933091335229648`). FAIT, A.
- **18/07 22:22:13 : @kikisknees à @elonmusk (`1814063148917256375`), en réponse à `1814057109056598382` : « "Freedom & merit is what America should be about." We are building an army for you for that purpose. $DMAGA », avec V0, image retrouvée (capture Wayback à 22:22:20, pHash 0 avec l'image de @FrancoAppr). FAIT, A pour le post et sa date. C'est la plus ancienne trace trouvée d'un compte du noyau qui s'adresse à Musk avec le ticker.**
- 20/07 01:12:44, 16:53:56, 16:54:21 : @kikisknees répond à Musk avec des images, dont « Yes, let's do it. #DarkMAGA » (`1814705414325354820`). Images retrouvées pour deux d'entre elles : Trump et des catcheurs, pas Musk. FAIT, A.
- 21/07 00:06:42 : @kikisknees reprend V0 à @3orovik, « We do. $DMAGA does too. » (`1814814222213165057`). 03:24:10 : « @FoxNews @elonmusk Building an army for $DMAGA IS smart. ». FAIT, A.
- 21/07 12:50:45 : « @pmarca Is Elon mooning with us? » avec V1. Le post répond à @pmarca « I have some ideas who to send. » (`1814954001227821426`), lui-même une citation de Musk sur une base lunaire (`1814882075519971504`). Le contexte est donc une plaisanterie sur la Lune. La ligne « sollicite publiquement @pmarca sur Elon » de la chronologie est à nuancer, l'image de Musk, elle, est là.
- 21/07 14:34:19 : @GreatBambin0, « When Elon pfp change? @DarkMagaCoin $Dmaga » (`1815032564895150177`), 4 h 49 avant l'avatar. 15:33:00 : « wen pfp.. Now pfp » à @koreanjewcrypto (`1815047331609219106`). DÉCLARATION, plus ancienne question écrite trouvée sur un changement de pfp de Musk. Ce compte écrit aussi « My bets rn are $Psyop and $Dmaga » (`1815046522066661717`) et n'est déclaré membre par personne dans ce qui est lu.
- 21/07 18:31:46 : @FrancoAppr à Musk, « A changed Elon could use a changed profile picture », 52 min avant l'avatar. DÉCLARATION, FAIT pour la date.

**Comptes proches, régularités.** FAIT : @greenchartlover, @GattodiLargo et @ZephyrusOtiosus répondent au même post de @kikisknees à moins de 3 min d'écart, 8 fois sur 24 posts archivés, du 21/07 00:39 au 22/07 16:55, presque toujours dans cet ordre (`1814822589627572491`, `1814846068984828205`, `1814852996158922838`, `1814857941411110928`, `1814865768368250901`, `1815126121283018815`, `1815425498010489235`, `1815429791681781782`). @FrancoAppr et @EeOo111_ envoient leurs images à Musk à 0,6 s d'écart (ids média 16:00:59,094 et 16:00:59,685). HYPOTHÈSE : coordination ou opérateur commun, non établie. Le délai court entre image et post n'est pas un signal, environ 27 % des 1 182 posts mesurés sont sous 2 s (`tools/delay_check.py`).

**Piste voisine, HYPOTHÈSE, niveau C.** Le thread d'@Aristos_Revenge parle d'un prototype politique sur Solana, sans nom. @kikisknees reposte 33 fois @Barronsolana dans les 1248 textes lus ici (compte créé le 19/04/2024 d'après son id, Telegram `BARRONTRVMP` créé le 21/04/2024). Il écrit le 12/07 « Me and @twicrates called up Barron » (`1811855145753260238`). @twicrates écrit le 15/07 « being in kiki coins rules » (`1812965882827842030`), @kritcheye le 21/07 « Kiki watch out for $barron » (`1814880500311294441`). Aucun contrat BARRON de 2024 n'est identifié ici, et la mise en page Safeguard du Telegram est banale. À traiter comme une piste, pas un lien.

## 4. Question 3, le DM revendiqué

**Niveau D pour le DM lui-même : ni prouvé ni réfuté.** Aucune capture de DM n'est trouvée, sur aucune source.

Ordre daté des formulations :
| UTC | Compte | Texte | Nature |
|---|---|---|---|
| 21/07 20:44:29 | @kikisknees `1815125720785391758` | « decided to use a wartime PFP that we made for him », surprise déclarée | DÉCLARATION |
| 21:18:14 | @DarkMagaCoin `1815134212426543404` | « made this pfp specifically for Elon » | DÉCLARATION |
| 21:56:34 | @DarkMagaCoin `1815143858075758890` | « We made the PFP for him, and Elon chose us. » | DÉCLARATION |
| 23:49:20 | @Shill_Matic1 `1815172240234950777` | « the pfp that was sent to him created by $DMAGA admin @ChrisWinig », premier « sent » trouvé | DÉCLARATION d'un tiers |
| 22/07 01:28:07 | @SundayFundayLFG `1815197098813399267` | « I was told that Elon got his new PFP from the Dark MAGA team » | DÉCLARATION d'un tiers |
| 03:23:20 | /biz/ 58770350, Warosu | « It was provided to elon by dmaga admin » | DÉCLARATION anonyme |
| 08:10:21 | @DarkMagaCoin `1815298322325811663` | « DMed to him by a team member », première mention d'un DM à Musk trouvée | DÉCLARATION |
| 24/07 06:40:49 | @DarkMagaCoin `1816000567740633335` | « No, he did not. We sent him the meme and he liked it. » Renvoie au post du DM | DÉCLARATION |
| 26/07 14:43:42 | @DarkMagaCoin `1816846863649124596` | « sent Elon his pfp second » | DÉCLARATION |
| 13/10 17:06:55 | @ChrisWinig `1845511546681823704` | « We memed the greatest entrepreneur... into the Dark Maga cult », sans DM | DÉCLARATION |

**Ce qui est établi autour.**
- FAIT, A : le visuel a bien été **envoyé à Musk en public**, plusieurs fois, avant l'adoption (partie 2). La formule du 24/07 « We sent him the meme » est donc vraie au moins en ce sens, sans qu'un DM soit nécessaire. Cela affaiblit la valeur du mot « DMed » sans le réfuter.
- FAIT, A : le DM est une pratique documentée de ce réseau envers d'autres comptes : @kikisknees à @twicrates (« Check DM », 14/07 05:39:32 et 18:48:36, « (check DM brother) », 16/07 21:34:23, `1813326337567842412`), à @pt0kes (« LOL (check DM) », 15/07 15:46:47, `1812876474778894760`), à @Fudrap96 (« (Check DM brother) », 17/07 19:58:02, `1813664478598471790`), à @alx (« check your DMs brother, I sent you one already », 21/07 20:41:16, après Musk), @DarkMagaCoin à @pt0kes (« I sent in DM brother », 22/07 00:36:08). Aucun de ces messages ne vise Musk. Le contenu de ces DM n'est pas connu.
- La séquence va de « fait pour lui » à « envoyé » puis « DM », puis retour à « envoyé ». La première mention d'un DM arrive 12 h 47 après l'avatar. FAIT pour les dates, pas de conclusion sur l'intention.
- La surprise déclarée par @kikisknees à 20:44:29 et par le thread d'@Aristos_Revenge reste en tension avec « DMed by a team member ».
- Les messages publics à Musk du 18/07 22:22:13 et du 21/07 18:31:46 montrent une attente publique, pas un contact privé.
- Le 21/07 à 19:35:17, @koreanjewcrypto écrit « team gave elon 1% of supply » (`1815108304823050265`), en réponse à @ashtoshii. Ton possiblement ironique, aucune trace. D.

**Reste à essayer.** Lire la réponse de Musk, s'il y en a une, aux posts du 18/07 et du 21/07 : aucune trouvée. Ses likes sont privés depuis juin 2024 (connaissance générale, non revérifiée). Le fichier d'origine de V1 ou V2, une capture de DM, une prise de parole dans le Space du 04/11/2024 annoncé par @DarkMagaCoin (`1853482649979146405`, avec @kikisknees, @Aristos_Revenge et d'autres) si un enregistrement existe.

## 5. Question 4, chronologie du lancement

| UTC | Fait | Source | Niveau |
|---|---|---|---|
| 11/06/2024 16:25:03 | Compte X @DarkMagaCoin créé | `created_at` des captures API et profil du dépôt | A |
| 13/07 22:11 | Tir de Butler | dossier, non revérifié ici | C |
| 13/07 23:25:04 | @CryptoOnlyCoims, « Dark MAGA Has Begun » (`1812267029078094144`), reposté par @kikisknees à 00:41:12 | direct et capture | A |
| 14/07 01:51:10 | Id de l'avatar de @DarkMagaCoin (`1812303793645666304`) | captures API | B |
| 14/07 01:57:02 | Telegram @DMAGACoin créé, photo à 01:57:03 | `evidence/telegram/tg_DMAGACoin_s.html` | A |
| 14/07 02:05:25 | Mint. Métadonnées IPFS : nom, symbole, « Dark MAGA patriots in control. », image. **Aucun X, Telegram ni site** | URI lue dans `raw/full_mint`, `evidence/token/ipfs_meta_gateway.pinata.cloud.json` | A |
| 14/07 02:26:35 | Premier post du compte, avec le mint | capture du repost | A |
| 14/07 02:41:38 | **Premier certificat de dmaga.xyz**, GoDaddy, crt.sh 13729224712 | `evidence/domains/crtsh_dmaga.xyz.json` | A |
| 14/07 02:45:55 | Compte X : 1 post, 0 abonnement, 7 abonnés | capture | A |
| 2024-07-15 17:44:54 | Plus ancienne réponse lue de @kikisknees avec une image carrée de 900 x 900, son format de pfp sur mesure. 164 réponses de ce format lues jusqu'au 21/07 12:51 (« Your pfp friend », « Here you are », « Sorry I missed yours brother! »). Couverture partielle | `wb_status_recovered.jsonl` | A pour le post, B pour l'usage |
| 21/07 20:45 à 20:47 | Outil de pfp annoncé (`1815126432164818991`), après l'avatar de Musk | post | A pour la date |
| 01/08/2024 | Premier certificat de darkmaga.com. Domaine enregistré le 15/03/2022, propriétaire de 2024 inconnu | crt.sh, RDAP du dépôt | A |
| 03/08/2024 18:26:57 | Première capture Wayback de darkmaga.com sur 2022 à 2024, même site DMAGA | `evidence/domains/wb_darkmaga_20240803.html` | A |
| 07/10/2024 | darkmagacoin.com, enregistrement et premier certificat | crt.sh, RDAP du dépôt | A |
| 06/11/2024 | darkmagapls.com, enregistrement | `evidence/domains/rdap_darkmagapls.com.json` | A |

**Verdict sur « lancé deux jours avant Butler » : D, contredit.** Le seul élément antérieur au tir est la création du compte X, 32 jours avant et non deux. @kikisknees : 167 posts lus sur 187 entre le 11/07 et le tir, sans mention du nom. Son propre avatar date du 16/07 16:27:11. Une mention d'un montage DMAGA de @kikisknees comme pfp arrive le 17/07 18:58:08 (`1813649402445156470`, @TrvthfvlTreason). Le 11/07, @kikisknees et @Aristos_Revenge échangent sur un problème de DM (`1811456429758243267`), sans parler d'un jeton : ils sont en contact avant le tir, rien de plus. La limite : le compteur de posts ne voit pas un post supprimé avant la capture, et une préparation privée reste possible. Les 20 posts du thread sont supprimés, la phrase exacte n'est connue que par Thread Reader.

**Domaine et chaîne plus anciens, indice C.** Un projet distinct existe : `$DARKMAGA`, Telegram `t.me/darkmagaonsol` créé le 09/05/2024 17:13:36, site darkmagaonsol.com (certificat et Wayback dès le 29/02/2024), X @darkmagaonsol suspendu, mint `6Zoi7ZZE7awFqBsXK44WVnP8T2b96RX1qptBiFSwmJa8`, signataire `DX9i7J3rujZJv7sXqk7pQ6zBZ4ecSGRv958FFfGta6n2` (révocation et brûlage du 09/05, RPC public). Or dmaga.xyz affiche en contact `DarkMAGAonSOL@proton.me` dès juillet 2024 (capture du dépôt). Même chaîne de caractères, rien de plus. Test simple : `DX9i7J3…` n'a aucune ligne dans `trades.parquet` et n'apparaît dans aucun rapport. HYPOTHÈSE, à trancher côté on-chain.

## 6. Question 5, adresses publiées

**Aucun compte du noyau ne publie de wallet dans ce qui est lu.** Inchangé, et mieux couvert : recherche native sur @ChrisWinig et @DarkMagaCoin, 1249 textes de plus pour @kikisknees. Niveau A pour ce qui est lu, D comme preuve d'absence. @Aristos_Revenge : recherche native vide, posts supprimés.

**`9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq`.** La source sociale manquante est trouvée. FAIT, A pour les posts :
- 13/08/2024 22:38:02 @0xbeehive `1823489213817610303`, 15/08 @thekuchh `1824139700187304048`, 17/08 @0xchromium `1824779938626736278`, 19/08 @cryptosymbiiote `1825526180616827284`. Ce sont des fils de type « wallets d'initiés », qui citent $DMAGA et $ELON. Chiffres de tiers, C. Pas de lien avec le wallet.
- **30/03/2024 02:01:36, @XHEILIGX `1773893309028577383`** : l'adresse seule, avec « #Pezi », en réponse à @pezitoken `1773892399875727679` (« Free $PEZI tokens from community fund! », tag de 2 amis). Soit 106 jours avant le mint.
- Le même compte répond à @kikisknees et @DarkMagaCoin le 21/07 à 00:41:03 (« $DMAGA #SOL », `1814822863695655368`), 18 h 42 avant l'avatar. Il garde la promotion en 2025 (`1881584209468223574`, `1900213105461776772`), et son profil (`evidence/profiles/fx_XHEILIGX.json`) renvoie vers des domaines « dmaga ».

**Lecture, INDICE C, pas une attribution.** On donne en général son propre wallet pour recevoir un don, et ce wallet a acheté dès le 14/07 02:28:56 d'après `reports/ATTRIBUTION.md`. Mais une adresse se copie, et le compte n'est pas du noyau. Pour prouver il manquerait : une phrase du compte disant que c'est son wallet, une signature de message, ou au minimum la réception de $PEZI par cette adresse après le 30/03/2024, à vérifier côté on-chain. Même avéré, ce lien désignerait un promoteur public, pas l'équipe.

**Autres adresses.**
- `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc` : en entier dès le 22/07 09:15:08 (@haspidox `1815314626596512111`), puis nombreux fils. Commentaires de tiers. Personne ne dit « mon wallet ».
- `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` : en entier dès le 22/07 12:06:23 (@kkashi_yt `1815357723577340268`). Commentaire de tiers.
- `F1DRDBNW1CX3BPoZPQafidvMeaepg6LS19J4vHqn7xMt` et `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` : mêmes fils de tiers.
- Créateur `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR`, `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E`, `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE`, `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` : aucun post rendu par la recherche X. Ne prouve pas qu'il n'en existe aucun.
- Les 10 adresses de `data/group_split.json` testées mêlent des services (Raydium, Jupiter). Les posts rendus parlent d'autres sujets, je n'en tire rien et la série a été arrêtée. Les 33 du groupe ne sont donc pas toutes testées.

**Déclarations d'achat ou de dotation, sans adresse.**
- @twicrates, 23/07 22:17:15 (`1815873841870299404`), en réponse à « You never bought yours anyway » : **« i never sold any dmaga i didnt buy at market, i was sent some that ive never touched »**. DÉCLARATION de jetons reçus sans achat. À rapprocher de @kikisknees à ce compte le 14/07 : « Check DM », et de « I heard @twicrates was going to buy 60% of the supply ». C pour le fait, rien pour l'adresse. Piste on-chain : wallets ayant reçu du DMAGA par transfert direct du groupe et jamais vendu.
- @koreanjewcrypto, 16/07 02:43:07 (`1813041645899649082`) : « I haven't sold a single $dmaga, bought more actually ». Sans adresse.
- @CryptoOnlyCoims, 14/07 03:20:42 (`1812326326176469155`) : « Just bought 1 SOL ». Test (`derived/trades_probe.txt`) : aucun achat de 0,9 à 1,1 SOL dans `trades.parquet` entre 03:00 et 03:20:42, 124 entre 02:05 et 03:00. Pas de candidat unique, aucun lien posé.
- @SundayFundayLFG et @bazingahappy, 22/07 : « bought with size », après coup, sans adresse.

## 7. Corrections proposées à l'existant, non appliquées

Je n'ai rien modifié hors de `work_E`. Le choix revient à Benjamin.

| Fichier | Écrit | Fait lu | Preuve |
|---|---|---|---|
| `docs/SOCIAL_FINDINGS.md`, `docs/TIMELINE.md` | les deux dates sont identiques dans tous les cas lus | 372 lignes sur 5155 diffèrent : l'id est celui d'un repost | `data/x_posts.jsonl` |
| TIMELINE | @pmarca 20/07 21:47:23 | vrai post 20:46:54, `1814763940410499481` | `evidence/x_raw_new/` |
| TIMELINE | @pmarca 21/07 12:43:30 | vrai post 07:08:26, `1814920352134537332` | idem, et capture du repost de @kikisknees à 12:43:02 |
| TIMELINE | premier post @DarkMagaCoin 03:00:28 | 02:26:35, `1812312706826854843` | capture `1812317575411351639` |
| TIMELINE | @ChrisWinig réagit à 19:33:11 | 19:32:17, `1815107549903135205` | direct |
| SOCIAL_FINDINGS | @wallstreetbets 19:59:04, @haruspectra 17:31:13, @koreanjewcrypto 21:08:23 et 22:23:23 | 19:40:23, 17:30:45, 21:07:05, 21:47:13 | ids `1815109589592858692`, `1815076964354470215`, `1815131407951561080`, `1815141504551092423` dans `data/x_raw` ou `work_E` |
| SOCIAL_FINDINGS | @kanpai 16/07 00:14:58 et 14:33:40 | 15/07 22:56:01 et 16/07 05:40:46 | ids `1812984492157771825`, `1813086353741230327` |
| MISSING_EVIDENCE | images de @kikisknees « absentes de la Wayback » | présentes avec `?format=...&name=orig` | `evidence/wb_cdx/` |
| MISSING_EVIDENCE, ATTRIBUTION | source sociale de `9PrmF8…` non retrouvée | retrouvée | partie 6 |
| TIMELINE, `data/events.json` | @ChrisWinig, plus ancienne image exacte | @FrancoAppr 16:00:59 pour V2, @kikisknees 12:50:45 pour V1 | partie 2 |
| TIMELINE | @kikisknees sollicite @pmarca sur Elon | contexte de plaisanterie sur la Lune, mais image de Musk jointe | partie 3 |

**Attention, étude gelée.** `etude_final/analysis_plan.md` fixe E = publication de @ChrisWinig à 16:02:29, et la cohorte « avant visuel » de `reports/TOP_TRADERS.md` s'y rattache. Je n'y touche pas. Ce point précède 16:02:29 de 90 s pour V2 et de 3 h 12 pour V1 : c'est une décision d'amendement pour Benjamin, pas une correction. Le plan pourrait tester une fenêtre supplémentaire déclarée comme exploratoire. La date d'un repost peut aussi avoir servi ailleurs : tout script qui utilise `created_utc_snowflake` comme date du post est à relire.

## 8. Table chronologique des éléments nouveaux

Heure : snowflake de l'id pour un post, date objective du document sinon. Chemins relatifs à `work_E`. Auteur réel lu dans la réponse, pas dans l'URL.

| UTC | Auteur | Type | Preuve (fichier, sha256) | Niveau |
|---|---|---|---|---|
| 2024-03-30T01:58:00Z | @pezitoken `1773892399875727679` | offre de jetons contre tag, parent de la réponse de @XHEILIGX | `evidence/x_raw_new/1773892399875727679.fx.json` c8d3715f215b8e8c8cc457f68375600edd885f387b60de52693f42fd0fae90bd | A |
| 2024-03-30T02:01:36Z | @XHEILIGX `1773893309028577383` | publie l'adresse entière 9PrmF8… 106 jours avant le mint | `evidence/x_raw_new/1773893309028577383.fx.json` 806ff5ba429f98698532867f507deb8c223f95bb9177d215fa8eda684e1b9165 | A pour le post, C pour le contrôle du wallet |
| 2024-04-21T20:02:30Z | Telegram BARRONTRVMP | création, voisin de @Barronsolana | `evidence/telegram/tg_s_BARRONTRVMP.html` e3d33fa33af5cfb40bdbe306aa44f801f7cd2ebc4338a2b0c942ba3b7364df36 | A |
| 2024-05-09T17:13:36Z | Telegram darkmagaonsol | création, projet $DARKMAGA | `evidence/telegram/tg_s_DarkMAGAonSOL.html` 555e414a9bb7d7060b1c675cf4684c0396a09ffedb552a818ee1a6b6a9994a0a | A |
| 2024-05-09T18:10:33Z | @Ralvero `1788632665182052689` | annonce d'achat de #DARKMAGA, mint 6Zoi7ZZE…, projet distinct du 09/05/2024 | `evidence/x_raw_new/1788632665182052689.fx.json` a0da315816f5c110cac9445ca563ecfcb598fef5e716c731b8cc4bd80e298be4 | A pour le post, C pour le lien |
| 2024-05-09T18:11:30Z | transaction du mint revoke | signataire DX9i7J3…, mint 6Zoi7ZZE… | `evidence/darkmagaonsol/tx_2PAQ7iTyAXAEgkLM.json` eb727511e3c2a4c92abaa5a95492f997168379ee9c4941efc0ebad1b2f2a93e1 | A |
| 2024-07-14T02:05:25Z | métadonnées IPFS du mint | aucun X, Telegram ni site à la création | `evidence/token/ipfs_meta_gateway.pinata.cloud.json` 6cb1d57ff347616e3a5b243117bc7e497f70cb768677424bfb0ae7e344c739a9 | A |
| 2024-07-14T02:05:25Z | image IPFS du mint | Trump rouge aux yeux laser | `evidence/token_img/ipfs_token_image.bin` 884bdca6ff32245fa4ec21252698f0ade6a1b8546697a30ef196762420f83432 | A |
| 2024-07-14T02:41:38Z | crt.sh dmaga.xyz | premier certificat, GoDaddy, id 13729224712 | `evidence/domains/crtsh_dmaga.xyz.json` 3e88f0119b2d54a9b638d1b43647aa7b155652f4b47d94dadbe97073e9ecf188 | A |
| 2024-07-14T03:20:42Z | @CryptoOnlyCoims `1812326326176469155` | « Just bought 1 SOL », vrai post, DÉCLARATION | `evidence/x_raw_new/1812326326176469155.fx.json` 70ce5c5439febac0f53c9163fa45cb4f9badd06c607b043710b212a7247b08f5 | C |
| 2024-07-14T04:36:51Z | /pol/ post 80672624, Palanq | « He doesn't know Dark MAGA is online », sans lien avec le jeton | `evidence/chan/palanq_pol_dark___maga_.json` f25633052e1e9a9750dd37e5ea5f66a95c1f250af9178b5f804ef8f9e90f0488 | C |
| 2024-07-15T21:42:04Z | @twicrates `1812965882827842030` | « being in kiki coins rules », DÉCLARATION | `evidence/x_raw_new/1812965882827842030.fx.json` fbeb9896bf3fb3812eb4fa62e6b44714f4603406acccf012025fe484d5b3b8fe | C |
| 2024-07-16T02:43:07Z | @koreanjewcrypto `1813041645899649082` | « I haven't sold a single $dmaga, bought more actually », DÉCLARATION | `evidence/x_raw_new/1813041645899649082.fx.json` ed5d06f5b35bfdec9fe6eac112e0fa85b4c2694e9e8c89785c6278c52a030c43 | C |
| 2024-07-16T20:32:13Z | @FrancoAppr `1813310692243480937` | réponse à @elonmusk, Musk aux yeux laser sur fond rouge, autre composition | `evidence/x_raw_new/1813310692243480937.fx.json` 5a0d17d6b05bc9dce8ed6ef1dcba0f1eedcfdac7cec581a342c62fd9fe64073e ; image `evidence/x_media_new/1813310692243480937_GSosdsSWYAACOIC.jpg` b18592ff6b5d946c7a41bf4012a31999eb675bbe69137687626ea0324bbe7d55 | A pour la date, C pour le lien avec l'avatar |
| 2024-07-18T22:22:13Z | @kikisknees `1814063148917256375` | réponse à @elonmusk, « We are building an army for you for that purpose. $DMAGA », V0 | `evidence/wb_status/1814063148917256375.raw` 2c2feb1b87684b7098791ffb39db90f3975acf811b88748352ea78c5e707e3d3 ; image `evidence/x_media_wb_new/GSzYuoTXgAA63zz_20240718222220.jpg` 78c5f5746f552be3f6d5d489a783ad72636704bbad9add02b2d43927ea80e0f3 | A |
| 2024-07-20T16:54:21Z | @kikisknees `1814705414325354820` | réponse à @elonmusk avec #DarkMAGA, image de catcheurs, pas Musk | `evidence/wb_status/1814705414325354820.raw` d52b50b203c7c3a0f43fb33a6a4ca63fca3374c4558842eb52bd48b988a3fb4c ; image `evidence/x_media_wb_new/GS8g7B3WEAEmKSw_20240722171755.jpg` 812c5c5a92f1841b484fc594f82b3dcd6edadb9ac73f121083dad9e0c43be5aa | A |
| 2024-07-20T19:05:03Z | @kikisknees `1814738306589917312` | réponse à @pmarca, Charlie Brown rouge, pHash 0 avec l'image de @pmarca | `../../../evidence/x_wayback/1815123417064255531.raw` 0cbf473345a3ef3ee836365d12fae016c43201c903296a8e4da8fa4c8b5d3f4d ; image `evidence/x_media_wb_new/GS8-wUDWMAAqpGm_20240722174904.png` 5905fe775b65b8413beb7d47a23742631f508d2a646feac9b0227bf55edb7dee | A |
| 2024-07-20T20:46:54Z | @pmarca `1814763940410499481` | publie la même image, le post lie le statut de @kikisknees | `evidence/x_raw_new/1814763940410499481.fx.json` 2218a4684267c6accc4c748be5ab127415d7b51bff87f81d7eeacdb5a76a116e | A |
| 2024-07-21T00:06:42Z | @kikisknees `1814814222213165057` | V0 reprise, « We do. $DMAGA does too. » | `evidence/wb_status/1814814222213165057.raw` da782122e6331b4144969a6f7e287b8abbb7a88caf920073bd92330f1e2a9165 ; image `evidence/x_media_wb_new/GS-D11oXEAAfsvX_20240722201641.jpg` 48e4ebc81ffec63bad958c689fe3dd4a6eb2ddd9c631229e8626f52e38f0c267 | A |
| 2024-07-21T00:41:03Z | @XHEILIGX `1814822863695655368` | réponse à @kikisknees et @DarkMagaCoin, « $DMAGA #SOL » | `evidence/x_raw_new/1814822863695655368.fx.json` 3570382868fd8659b8278c32a2be1a50e7b1722adeae637e62b9bfc6a5ddc20d | A |
| 2024-07-21T03:24:10Z | @kikisknees `1814863915186016702` | réponse à @FoxNews et @elonmusk, « Building an army for $DMAGA IS smart. » | `evidence/wb_status/1814863915186016702.raw` 5fa0dbc7c49968b8c7c43baf5a3b9b43dc82526df2bdc593cc0d5c92f9e0f9c6 | A |
| 2024-07-21T04:30:04Z | @kritcheye `1814880500311294441` | « Kiki watch out for $barron », DÉCLARATION | `evidence/x_raw_new/1814880500311294441.fx.json` 7072174cad611945eb4cf15e11990f70f3972c05e20b80090776fda1f1aa3834 | C |
| 2024-07-21T07:08:26Z | @pmarca `1814920352134537332` | « THAT'S RIGHT. », vrai post, 5 h 35 avant la date du dossier | `evidence/x_raw_new/1814920352134537332.fx.json` cf73526010564096cf29eb604352b0251a6a84fbd7281023956eb87b5eb7bf13 | A |
| 2024-07-21T12:50:45Z | @kikisknees `1815006501896872388` | **plus ancienne image connue du visuel de Musk**, variante V1, réponse à @pmarca | `../../../evidence/x_wayback/1815006501896872388.raw` cdfce2180a4e4b60e2b39856a19e2275f954f0d7e8ca8a053d8a74ab8c8d5651 ; image `evidence/x_media_wb_new/GTAytGIW4AE9_93_20240723023716.png` dc2bed87096844d67d765b631ade81a3d9d896067175dda44839d5916566d812 | A |
| 2024-07-21T14:34:19Z | @GreatBambin0 `1815032564895150177` | « When Elon pfp change? », DÉCLARATION | `evidence/x_raw_new/1815032564895150177.fx.json` 71487e09c89b283ff67c621ecb8737226007ead27cdbc75745daaf444ebb0c73 | A |
| 2024-07-21T15:33:00Z | @GreatBambin0 `1815047331609219106` | « wen pfp.. Now pfp », réponse à @koreanjewcrypto | `evidence/x_raw_new/1815047331609219106.fx.json` f6444ceccb59bf1920eb791f91cf80ad6afe9898d13dc48f6ce289dd65a10a21 | A |
| 2024-07-21T15:58:21Z | @GreatBambin0 `1815053713330876681` | **plus ancien envoi connu à Musk**, V1, 21 s avant son « Whoa » | `evidence/x_raw_new/1815053713330876681.fx.json` d3ec6bdac37b5b62b3fa94d4905b4edf6963fd08d1211272f4cfad5ca2544740 ; image `evidence/x_media_new/1815053713330876681_GTBdu7vXgAARcaz.jpg` 769d62ef2851b6265e2c662a23b69894062a0b1d22fdf5dc3ca1374a19685a82 | A |
| 2024-07-21T16:00:08Z | @kikisknees `1815054158367432804` | réponse à Musk, image retrouvée, c'est le Trump « dark maga », pas Musk | `../../../evidence/x_wayback/1815054158367432804.raw` 4cef76b46548624ca0f1e3afd9204867e06c79f2604418646641fb9cf74335dd ; image `evidence/x_media_wb_new/GTBeEjGXgAAbn4S_20240722211626.jpg` cce3b01b864a264dac2c02ceff2dce50365a7e0b2adaa0a39d471d30c3eecccb | A |
| 2024-07-21T16:00:59Z | @FrancoAppr `1815054374982324401` | **plus ancienne image identique connue**, V2, pHash 0 avec l'avatar | `evidence/x_raw_new/1815054374982324401.fx.json` 7bcb8e343cbb7338325ff2e62c71680043cf2baa23667bc3fb6c14b7ec647ebb ; image `evidence/x_media_new/1815054374982324401_GTBeVcVXAAAVa3o.jpg` ad1e48a6f01d5076221f0a48c0aae80191d892d53a15218a7ae7864353d5c22f | A |
| 2024-07-21T16:01:01Z | @EeOo111_ `1815054381823221968` | V1, « Whoa, ELON IN DARK MAGA » | `evidence/x_raw_new/1815054381823221968.fx.json` fbe0e49b781ae2c9c93e6927303836a1408e8ed810f4c7d31bd1c3b8c657b068 ; image `evidence/x_media_new/1815054381823221968_GTBeVlkXsAAgbTW.jpg` 2b06fed973b5ddc070646003408e8aa28d54115070c87c3782be750609fd9b4b | A |
| 2024-07-21T16:12:38Z | @DarkMagaCoin `1815057307836842034` | V1 en réponse à Musk, « Based GC members: » | `evidence/x_raw_new/1815057307836842034.fx.json` c082fbf9919cc2abadee47d6c1307c51c1ba22cbfd62df742ce6d78a1b4c8742 ; image `evidence/x_media_new/1815057307836842034_GTBg8wsXoAAouzI.png` 898c752573c08a4ebafa79bf9c5229f4fd1365d7a758117ac0cc7a358993ef94 | A |
| 2024-07-21T16:32:02Z | @GreatBambin0 `1815062189763703119` | plus ancienne variante V3 connue | `evidence/x_raw_new/1815062189763703119.fx.json` 21e4ea9fbc480e98e62f173d13a88ac2d549283c30903f4cead91b0e852b64d2 ; image `evidence/x_media_new/1815062189763703119_GTBlcMpWkAABbvL.jpg` 9f9c2e47648ccb012e2d3e51ec9295489dd93f9f0f2fce92310b132be4bad9cb | A |
| 2024-07-21T18:31:46Z | @FrancoAppr `1815092319244128645` | « A changed Elon could use a changed profile picture », V2, 52 min avant l'avatar | `evidence/x_raw_new/1815092319244128645.fx.json` 06b28cf130fc3477e28164d243e755a397cb3ecd9fea72d46f79c5307cbe4ba0 ; image `evidence/x_media_new/1815092319244128645_GTCA2FyXcAAH6aD.jpg` ad1e48a6f01d5076221f0a48c0aae80191d892d53a15218a7ae7864353d5c22f | A |
| 2024-07-21T18:40:09Z | @Murray_Gothbard `1815094431152029711` | V2 en réponse à Musk | `evidence/x_raw_new/1815094431152029711.fx.json` 54722af6650e2a7b8763f47853b25d94551d58be78dd5f6e8beb11bae0db962f ; image `evidence/x_media_new/1815094431152029711_GTCCxFyWMAA4Cy1.jpg` ad1e48a6f01d5076221f0a48c0aae80191d892d53a15218a7ae7864353d5c22f | A |
| 2024-07-21T18:46:37Z | @kikisknees `1815096055337496944` | réponse à Musk, image retrouvée, V3 | `../../../evidence/x_wayback/1815096055337496944.raw` 8c6d9693abd9f609816a81d0caf1f5550e502d8c834d48fc0c2f4e5e674b3615 ; image `evidence/x_media_wb_new/GTCEEQ2WoAAm65s_20240723081618.png` 0b59ba6ac603749f62829003c5a72dab7da831ae589d3657ee65eba98f5ee2dc | A |
| 2024-07-21T19:32:17Z | @ChrisWinig `1815107549903135205` | vrai post « Elon just made this his profile picture! », 54 s avant la date du dossier | `evidence/x_raw_new/1815107549903135205.fx.json` 5ca6ad9f96c23f6540f343bb4d8138498fc7fca61591e59f7769230053efabb1 | A |
| 2024-07-21T19:35:17Z | @koreanjewcrypto `1815108304823050265` | « team gave elon 1% of supply », DÉCLARATION sans preuve, ton possiblement ironique | `evidence/x_raw_new/1815108304823050265.fx.json` cb755118b493b96c54f7de185a4608f6b3358cb3143e37c96a038a324765f54b | D |
| 2024-07-21T20:07:24Z | @kikisknees `1815116385414209876` | « That's a $DMAGA pfp, made by me. », image retrouvée, Trump, pas Musk | `../../../evidence/x_wayback/1815116385414209876.raw` d0accaaa9e9a3ff9babf84bdfd58d0de74ba296bf04d4ca1f617bffe8b47b8f9 ; image `evidence/x_media_wb_new/GTCWqbzXUAAYsUP_20240723080042.jpg` cce3b01b864a264dac2c02ceff2dce50365a7e0b2adaa0a39d471d30c3eecccb | A |
| 2024-07-21T23:49:20Z | @Shill_Matic1 `1815172240234950777` | « the pfp that was sent to him », DÉCLARATION | `evidence/x_raw_new/1815172240234950777.fx.json` a8a8d0986f70e9b2486f36d7a239e54d9bc9dba0d92569de6e479aa412059f0a | C |
| 2024-07-22T01:28:07Z | @SundayFundayLFG `1815197098813399267` | « I was told that Elon got his new PFP from the Dark MAGA team », DÉCLARATION | `evidence/x_raw_new/1815197098813399267.fx.json` 2f4fba0d8f31f7187240da873966bfc9f175d4a7a7f9454eeea916f1bddf1e37 | C |
| 2024-07-22T03:23:20Z | /biz/ post 58770350, Warosu | « provided to elon by dmaga admin » | `evidence/chan/warosu_biz2_dmaga_.html` 64393116ac188bb604268290f25aa983a57f11b33f48c8b5b57a3ec808e5300e | C |
| 2024-07-22T09:15:08Z | @haspidox `1815314626596512111` | plus ancien post retrouvé avec H3QsBr… en entier, commentaire | `evidence/x_raw_new/1815314626596512111.fx.json` 2123c7b34bdb60ec60e0e9af148da23d6017af998479011704d0e14628d8cfc4 | A pour le post, C pour le contenu |
| 2024-07-22T12:06:23Z | @kkashi_yt `1815357723577340268` | plus ancien post retrouvé avec 5QhJJc… en entier, commentaire | `evidence/x_raw_new/1815357723577340268.fx.json` 66cb7f827f1d4ec4075cf98be4a60dbe7f4f0155c3ea2bc2ac275818364a7c21 | A pour le post, C pour le contenu |
| 2024-07-23T22:17:15Z | @twicrates `1815873841870299404` | « i was sent some that ive never touched », DÉCLARATION | `evidence/x_raw_new/1815873841870299404.fx.json` b78ae5c1f8c0517263dbdec2ff69a3270e9fc49bc5471222ef5c0b503c00882e | C |
| 2024-08-01T00:00:00Z | crt.sh darkmaga.com | premier certificat au journal, Sectigo, id 13957636645 | `evidence/domains/crtsh_darkmaga.com.json` 2e3400c877056cad483f8038f1110edea8922a7cf9f4d5eb6ef6c2c0cd7221c5 | A |
| 2024-08-03T18:26:57Z | Wayback darkmaga.com | premier contenu archivé, site DMAGA | `evidence/domains/wb_darkmaga_20240803.html` 1421ddb34acb9d2b7d239fe10be8409acd6af107159ff25d7438777160d9a244 | A |
| 2024-08-13T22:38:02Z | @0xbeehive `1823489213817610303` | « Insider - 9PrmF8… », plus ancien fil d'août retrouvé | `evidence/x_raw_new/1823489213817610303.fx.json` eb19713446322d26fe84d1e2d594bd7abd3f6b0da18b9551ac233fc989aa95fc | A pour le post, C pour le contenu |
| 2024-08-15T17:42:50Z | @thekuchh `1824139700187304048` | « Key Wallet: 9PrmF8… » | `evidence/x_raw_new/1824139700187304048.fx.json` a65098e32ed4d4f5d640ee8c62106a23c76d210ba0d61dc4501aa8355125d318 | A pour le post, C pour le contenu |
| 2024-08-17T12:06:54Z | @0xchromium `1824779938626736278` | adresse 9PrmF8… | `evidence/x_raw_new/1824779938626736278.fx.json` 846026f498e4428b63abc5cee95185d9e18f33c55349dc830234c9724c836ea9 | A pour le post, C pour le contenu |
| 2024-08-19T13:32:12Z | @cryptosymbiiote `1825526180616827284` | « Second Insider ... 9PrmF8… » | `evidence/x_raw_new/1825526180616827284.fx.json` 55e96c27a65670eff1b3155c741dafd693855d1e2cceb810cbb5e53c1706a5b9 | A pour le post, C pour le contenu |
| 2024-10-07T17:24:52Z | crt.sh darkmagacoin.com | premier certificat | `evidence/domains/crtsh_darkmagacoin.com.json` b1c0ffaa9dc641023a870f4b7bacc24c9a9ded2496966ab0919819ea4dab4433 | A |
| 2024-10-13T17:06:55Z | @ChrisWinig `1845511546681823704` | « We memed the greatest entrepreneur... into the Dark Maga cult », DÉCLARATION | `evidence/x_raw_new/1845511546681823704.fx.json` 68539e4752a06a6b635ab66798ef00381beaa0a26507a881de5b21370d45068e | C |
| 2024-11-04T17:01:14Z | @DarkMagaCoin `1853482649979146405` | Space de « the Dark MAGA team » avec @kikisknees, @Aristos_Revenge et d'autres | `evidence/x_raw_new/1853482649979146405.fx.json` 909a2ac143b8739956722f3245123f42af64b2bceb535d2745ff10819ff49011 | A pour le post, C pour le lien |
| 2024-11-06T09:45:19Z | RDAP darkmagapls.com | enregistrement, après l'élection | `evidence/domains/rdap_darkmagapls.com.json` 28c0fec555c590d7f7eb25dac2196c6cc859c373730b9a8e3f162b77f77d8d0c | A |

## 9. Sources essayées

| Source | Essai | Résultat | Ce que cela prouve ou non |
|---|---|---|---|
| Recherche X native, navigateur connecté | 30 recherches, onglet Récents, `x_search_log.jsonl` | 24 lisibles, 2 perdues sur délai, 3 vides sur erreur probable, 1 erreur affichée | Lecture seule, aucune action d'écriture. La plus utile. Absent ne veut pas dire inexistant |
| Post @pmarca ouvert par id | 1 page | Lien vers @kikisknees visible | Capture d'écran gardée, elle montre le pseudo du compte connecté |
| api.fxtwitter.com et syndication | 170 posts lus | Réponses brutes dans `evidence/x_raw_new/` | Un post supprimé répond indisponible |
| Wayback, captures de status @kikisknees | 1290 réponses 200 sur toute la Wayback, 89 refus ou 5xx, reprises avec pauses | Voir la couverture en partie 3, 29 captures non JSON | Reste une limite de collecte, pas une absence |
| Wayback CDX, médias `pbs.twimg.com/media/<clé>*` | Environ 40 clés, dont un lot de 99 images de @kikisknees coupé par l'arrêt forcé | 17 images récupérées, le reste en refus de connexion ou 503, ou non demandé | Méthode reproductible. La grande majorité des 164 images 900 x 900 de @kikisknees antérieures au 21/07 12:51 ne sont pas lues : une V1 antérieure à 12:50:45 n'est pas exclue |
| Wayback CDX @ChrisWinig | `twitter.com/ChrisWinig/status/*` | `[]` | Compte absent de la Wayback, pas de conclusion |
| Wayback darkmaga.com, darkmagaonsol.com | CDX | Premières captures 03/08/2024 et 29/02/2024 | dmaga.xyz en refus de connexion, dates déjà au dossier |
| archive.ph | Profils @kikisknees x.com et twitter.com | Captures du 29/01/2024, 28/03/2025, 10/05/2025, 13/05/2026, 19/08/2026 | Aucune de juillet 2024, non ouvertes |
| ghostarchive | Recherche kikisknees | 12 archives, aucune de juin à août 2024, 3 lues de 2024 sans rapport | Épuisé pour la période |
| Telegram `t.me/s/DMAGACoin` | Aperçu et `?before=` | 3 messages (créé, photo, Safeguard du 16/07), rien avant | Le canal public est vide, le groupe n'est pas lisible |
| Telegram voisins | `DarkMagaCoin`, `darkmaga`, `DarkMAGA`, `DMAGA`, `dmagaportal`, `darkmagasol`, `DarkMAGAonSOL`, `DMAGACoinPortal`, `darkmagacoinsol`, `BARRONTRVMP`, invitation `+30sxDUsH64cyYzdh` | `DarkMagaCoin` groupe de 6 membres sans aperçu, `DMAGA` pseudo à vendre, `DarkMAGAonSOL` projet de mai 2024, invitation sans titre | Noms devinés, un nom absent ne prouve rien |
| Métadonnées du token | URI lue dans `raw/full_mint`, passerelles IPFS | pinata 200, ipfs.io et dweb.link 403 Cloudflare, cf-ipfs.com DNS mort | Résultat obtenu, pas de contournement |
| Commentaires pump.fun | `frontend-api` et `frontend-api-v3` | 403 Cloudflare | Non lus. Pas de contournement. À essayer depuis un navigateur si Benjamin le souhaite |
| DexScreener, GeckoTerminal, CoinGecko | API publiques | 200. Site, X et Telegram actuels. Paire créée le 14/07 02:15:31 | État d'aujourd'hui, pas celui de 2024, sauf la date de paire |
| crt.sh, RDAP | 5 domaines | Dates en partie 5, `darkmagapls.com` en 502 sur crt.sh, `darkmagaonsol.com` absent du RDAP | `not_before` approche l'émission. Une date de domaine ne donne pas le propriétaire |
| urlscan | 3 domaines | 0, recherche limitée à 30 jours sans compte | Ne dit rien sur 2024 |
| 4chan /biz/, Warosu | 5 requêtes par date | 4 posts du 21 au 22/07, tous après l'avatar | Aucune trace avant Musk parmi ces requêtes |
| 4chan /pol/, Palanq | 3 requêtes | 2 posts du 14 et 16/07, sans lien avec le jeton | |
| archived.moe, 4plebs | API de recherche | 403 Cloudflare, page d'attente | Non lus, pas de contournement |
| desuarchive | /biz/ | « No results », couverture de /biz/ non vérifiée | Rien |
| Reddit | arctic-shift et pullpush | arctic-shift exige un subreddit, 5 délais dépassés, 2 listes vides (`solana`, `memecoins`, titres). pullpush 522 | Reddit reste non couvert |
| Exa | 1 requête sans adresse | Daily Dot, UnoCrypto (22/07 11:22, reprend le DM), Benzinga. Page UnoCrypto non sauvegardée, échec du GET | Rien de nouveau |
| YouTube | `ytsearch12` | 3 résultats sans rapport | Rien |

## 10. Limites

- Le navigateur a servi sous le compte connecté de Benjamin, en lecture seule. Les requêtes, dont des adresses, sont passées par X sous ce compte. Onglet fermé.
- Les textes des captures Wayback viennent d'un collecteur tiers de l'API X, à la publication. Je les tiens pour fidèles, je ne connais pas ce collecteur.
- Une image retrouvée dans la Wayback porte la clé média du post. Elle date du 22 au 23/07/2024 pour la capture, et l'heure du post vient de l'id. Le lien repose sur la clé.
- pHash et œil montrent une ressemblance, pas un auteur.
- La recherche X par `until_time` et `from:` peut omettre des posts sans le dire, et les suppressions ne se voient pas.
- `reply_to_user` et `views` sont ceux de l'endpoint public au 03/11/2026.
- Ce qui reste à faire : relancer `tools/wb_status.py` et `tools/wb_media.py` quand la Wayback répond, jusqu'à épuisement des fenêtres ci-dessus. Tester $PEZI sur `9PrmF8…` et les réceptions sans achat pour @twicrates côté on-chain. Identifier un éventuel contrat BARRON de 2024 seulement si Benjamin active cette branche.
