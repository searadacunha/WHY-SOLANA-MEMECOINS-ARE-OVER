# Suivi social et documentaire, Dark MAGA ($DMAGA)

Collecte du 03/11/2026, de 10:05 à 11:16 UTC, coupure forcée par une limite d'usage, puis reprise de 13:31 à {{FIN}} UTC environ. Mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Heures en UTC.
Personne n'est accusé. Aucune identité civile n'est recherchée. Les pseudos désignent des comptes, pas des personnes établies.

Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice, **D** non vérifié ou contredit.
**FAIT** observé dans un fichier sauvegardé, **DÉCLARATION** ce qu'un compte affirme, **HYPOTHÈSE** à vérifier.
Preuves : `evidence/`, `evidence_manifest.jsonl` (url, heure de collecte, sha256), `x_posts_new.jsonl` ({{N_LIVE}} posts lus en direct, {{N_WB}} textes de posts supprimés lus dans la Wayback), `x_search_log.jsonl` (les 30 recherches X), `tools/`.

## 1. Ce qui change le dossier

1. **La chronologie du visuel recule de plus de 3 heures.** La plus ancienne image connue du visuel de Musk n'est plus @ChrisWinig à 16:02:29. C'est @kikisknees à **12:50:45**, en réponse à @pmarca (variante rouge sans drapeau). L'image exacte de l'avatar est publiée par @FrancoAppr à **16:00:59**, 90 s avant @ChrisWinig. Le plus ancien envoi connu de cette famille à Musk est @GreatBambin0 à **15:58:21**.
1. **@kikisknees vise Musk avec le ticker dès le 18/07.** À 22:22:13, en réponse à @elonmusk : « We are building an army for you for that purpose. $DMAGA », avec une image de Musk aux yeux laser (autre composition, publiée dès le 16/07 par @FrancoAppr). Trace publique et datée, trois jours avant l'avatar. Rien ne montre que Musk l'a vue.
2. **L'image perdue de 16:00:08 est retrouvée.** Ce n'est pas Musk. C'est le Trump « dark maga » de @DarkMagaCoin, même fichier au sha256 près.
3. **Les images de @kikisknees ne sont pas perdues.** La Wayback les garde sous `pbs.twimg.com/media/<clé>?format=...&name=orig`. Il faut une CDX avec joker. {{N_MEDIA_WB}} images récupérées.
4. **@pmarca a repris une image de @kikisknees, c'est visible sur son post.** Réponse de @kikisknees le 20/07 à 19:05:03, post de @pmarca à 20:46:54 avec un lien vers ce statut, même image (pHash 0).
5. **« Lancé deux jours avant Butler » est contredit par toutes les dates objectives lues** (compteur du compte X, certificat du site, Telegram, avatar, mint, {{W1113_R}} posts de @kikisknees sur {{W1113_N}} entre le 11/07 et le tir).
6. **La source sociale de `9PrmF8…` est retrouvée**, et une trace plus ancienne : @XHEILIGX publie cette adresse le 30/03/2024, puis promeut $DMAGA. Indice de niveau C, pas une attribution.
7. **Défaut du corpus : {{CORPUS_BAD}} lignes sur {{CORPUS_N}} de `data/x_posts.jsonl` ont une date fausse dans `created_utc_snowflake`.** Leur id est celui d'un repost, le texte et la métadonnée sont ceux de l'original. Le dossier écrit que les deux dates sont toujours égales. Cela touche des lignes de `docs/TIMELINE.md`, voir partie 7.

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
- 20/07 20:46:54 : @pmarca publie `1814763940410499481`. Même image, pHash 0. Le post contient le lien `/kikisknees/status/1814738306589917312`, visible dans le navigateur (`evidence/x_screens_pmarca_1814763940410499481.jpg`), le post cité est marqué indisponible.
- 21/07 07:04:09 : id du nouvel avatar de @pmarca. 07:08:26 : « THAT'S RIGHT. » (`1814920352134537332`).

**Contrôle de la lecture « id d'avatar = heure d'envoi »**, marquée à confirmer dans le dossier. Sur les captures API v2 lues, de plusieurs centaines de comptes, chaque avatar est vu après son id ({{AV_OK}} cas sur {{AV_OK}}, 0 contraire) et chaque ancien avatar est vu avant l'id du suivant ({{AV_PREV}} cas sur {{AV_PREV}}, 0 contraire). `tools/avatar_control.py`, `derived/avatar_changes.json`. Niveau B, l'heure du clic reste inconnue. Ce même fichier date d'autres changements : @BasedTorba 20/07 19:05:51, @poosseau 21/07 13:20:32, @notsofast 13:36:46, @Aristos_Revenge 17:36:50, @koreanjewcrypto 19:43:31, @twicrates 23:45:38. L'id date un envoi d'avatar, pas son contenu.

**Reste inconnu.** Un post avec image seule, sans mot-clé, ne ressort pas d'une recherche X : une occurrence antérieure de V1 ou V2 reste possible. La grande majorité des {{KIKI900_N}} images 900 x 900 de @kikisknees antérieures au 21/07 12:51 ne sont pas lues, seuls leurs textes le sont. L'auteur du fichier V2 n'est pas établi : @kikisknees écrit « $DMAGA pfp by me and @ChrisWinig » (DÉCLARATION). @FrancoAppr, @ChrisWinig et @Murray_Gothbard publient chacun un 1024 x 1024 de pHash 0, comme le IMG_5658 de la capture de @DarkMagaCoin (1024 x 1024, 235 Ko, 06:17, fuseau inconnu) : HYPOTHÈSE d'un fichier partagé avant 16:00:59. Le format 900 x 900 de V1 est celui des pfp faits par @kikisknees, celui de V2 ne l'est pas : c'est compatible avec « by me and @ChrisWinig », sans le prouver (C). Ce que Musk a vu n'est pas établi.

## 3. Question 2, publications avant l'adoption

**@DarkMagaCoin.** La recherche native `from:DarkMagaCoin until:2024-07-14` ne rend que 12 reposts. FAIT, A : la capture du repost de @kikisknees à 02:45:55 le 14/07 donne le premier post propre, `1812312706826854843`, à **02:26:35** (« We are live Patriots! », avec le mint), et non 03:00:28. Elle donne aussi les compteurs du compte à cet instant : 1 post, 0 abonnement, 0 like, 7 abonnés. À 04:07:26 : 6 posts. Avant l'avatar, ni la recherche `from:DarkMagaCoin elon` ni `data/x_posts.jsonl` ne contiennent de texte propre du compte avec « elon » ou « musk ». Le compte reposte @kikisknees à 16:02:54 et @ChrisWinig à 16:04:53, puis envoie V1 à Musk à 16:12:38. « GC » répond au post de Musk « 𝕏 is the group chat for Earth » (`1807491298015768981`) : ne pas y lire un groupe privé.

**@ChrisWinig.** Le CDX reste vide (`[]`, retesté). La recherche native comble ce trou : 106 lignes rendues du 01/06 au 22/07, doublons compris, sans aucune mention de DMAGA, Dark MAGA ou Musk avant Butler. Vidéos à 23:05:26 et 23:40:42 le 13/07, après le tir. Première publication du mint par ce compte : `1813680552031195437`, 17/07 21:01:54. Citation de lui par @DarkMagaCoin cinq minutes plus tard (déjà au dossier).

**@kikisknees.** Ses posts propres de 2024 sont presque tous supprimés : la recherche native n'en rend qu'un, du 04/06 (`1798040845041709555`). Ses reposts restent visibles. Couverture Wayback ci-dessous. Sur {{PRE_N}} posts lus du 11/06 au tir de Butler : {{PRE_HITS}} mention de « Dark MAGA » ou « DMAGA », {{PRE_COIN}} ticker écrit par lui. Mentions de Musk écrites par lui sur cette période : {{PRE_MUSK}}. Attention, du 11/06 au 10/07 la lecture reste partielle, voir la table.

Premières réponses de @kikisknees qui nomment @elonmusk après Butler, parmi les textes lus ici :
{{EARLY_MUSK}}

| Fenêtre | Ids CDX | Lus avant le 03/11 | Lus ici | Restent |
|---|---|---|---|---|
{{COV}}

**Traces datées d'une intention de cibler Musk.** Toutes sont publiques, aucune n'établit un plan de l'équipe :
- 16/07 20:32:13 : @FrancoAppr répond à Musk avec une image de Musk aux yeux laser. Il répond à Musk avec des images rouges dès le 15/07 19:31:46 (`1812933091335229648`). FAIT, A.
- **18/07 22:22:13 : @kikisknees à @elonmusk (`1814063148917256375`), en réponse à `1814057109056598382` : « "Freedom & merit is what America should be about." We are building an army for you for that purpose. $DMAGA », avec V0, image retrouvée (capture Wayback à 22:22:20, pHash 0 avec l'image de @FrancoAppr). FAIT, A pour le post et sa date. C'est la plus ancienne trace trouvée d'un compte du noyau qui s'adresse à Musk avec le ticker.**
- 20/07 01:12:44, 16:53:56, 16:54:21 : @kikisknees répond à Musk avec des images, dont « Yes, let's do it. #DarkMAGA » (`1814705414325354820`). Images retrouvées pour deux d'entre elles : Trump et des catcheurs, pas Musk. FAIT, A.
- 21/07 00:06:42 : @kikisknees reprend V0 à @3orovik, « We do. $DMAGA does too. » (`1814814222213165057`). 03:24:10 : « @FoxNews @elonmusk Building an army for $DMAGA IS smart. ». FAIT, A.
- 21/07 12:50:45 : « @pmarca Is Elon mooning with us? » avec V1. Le post répond à @pmarca « I have some ideas who to send. » (`1814954001227821426`), lui-même une citation de Musk sur une base lunaire (`1814882075519971504`). Le contexte est donc une plaisanterie sur la Lune. La ligne « sollicite publiquement @pmarca sur Elon » de la chronologie est à nuancer, l'image de Musk, elle, est là.
- 21/07 14:34:19 : @GreatBambin0, « When Elon pfp change? @DarkMagaCoin $Dmaga » (`1815032564895150177`), 4 h 49 avant l'avatar. 15:33:00 : « wen pfp.. Now pfp » à @koreanjewcrypto (`1815047331609219106`). DÉCLARATION, plus ancienne question écrite trouvée sur un changement de pfp de Musk. Ce compte écrit aussi « My bets rn are $Psyop and $Dmaga » (`1815046522066661717`) et n'est déclaré membre par personne dans ce qui est lu.
- 21/07 18:31:46 : @FrancoAppr à Musk, « A changed Elon could use a changed profile picture », 52 min avant l'avatar. DÉCLARATION, FAIT pour la date.

**Comptes proches, régularités.** FAIT : @greenchartlover, @GattodiLargo et @ZephyrusOtiosus répondent au même post de @kikisknees à moins de 3 min d'écart, 8 fois sur 24 posts archivés, du 21/07 00:39 au 22/07 16:55, presque toujours dans cet ordre (`1814822589627572491`, `1814846068984828205`, `1814852996158922838`, `1814857941411110928`, `1814865768368250901`, `1815126121283018815`, `1815425498010489235`, `1815429791681781782`). @FrancoAppr et @EeOo111_ envoient leurs images à Musk à 0,6 s d'écart (ids média 16:00:59,094 et 16:00:59,685). HYPOTHÈSE : coordination ou opérateur commun, non établie. Le délai court entre image et post n'est pas un signal, environ 27 % des 1 182 posts mesurés sont sous 2 s (`tools/delay_check.py`).

**Piste voisine, HYPOTHÈSE, niveau C.** Le thread d'@Aristos_Revenge parle d'un prototype politique sur Solana, sans nom. @kikisknees reposte {{BARRON_N}} fois @Barronsolana dans les {{WB_TEXT}} textes lus ici (compte créé le 19/04/2024 d'après son id, Telegram `BARRONTRVMP` créé le 21/04/2024). Il écrit le 12/07 « Me and @twicrates called up Barron » (`1811855145753260238`). @twicrates écrit le 15/07 « being in kiki coins rules » (`1812965882827842030`), @kritcheye le 21/07 « Kiki watch out for $barron » (`1814880500311294441`). Aucun contrat BARRON de 2024 n'est identifié ici, et la mise en page Safeguard du Telegram est banale. À traiter comme une piste, pas un lien.

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
| {{KIKI900_FIRST}} | Plus ancienne réponse lue de @kikisknees avec une image carrée de 900 x 900, son format de pfp sur mesure. {{KIKI900_N}} réponses de ce format lues jusqu'au 21/07 12:51 (« Your pfp friend », « Here you are », « Sorry I missed yours brother! »). Couverture partielle | `wb_status_recovered.jsonl` | A pour le post, B pour l'usage |
| 21/07 20:45 à 20:47 | Outil de pfp annoncé (`1815126432164818991`), après l'avatar de Musk | post | A pour la date |
| 01/08/2024 | Premier certificat de darkmaga.com. Domaine enregistré le 15/03/2022, propriétaire de 2024 inconnu | crt.sh, RDAP du dépôt | A |
| 03/08/2024 18:26:57 | Première capture Wayback de darkmaga.com sur 2022 à 2024, même site DMAGA | `evidence/domains/wb_darkmaga_20240803.html` | A |
| 07/10/2024 | darkmagacoin.com, enregistrement et premier certificat | crt.sh, RDAP du dépôt | A |
| 06/11/2024 | darkmagapls.com, enregistrement | `evidence/domains/rdap_darkmagapls.com.json` | A |

**Verdict sur « lancé deux jours avant Butler » : D, contredit.** Le seul élément antérieur au tir est la création du compte X, 32 jours avant et non deux. @kikisknees : {{W1113_R}} posts lus sur {{W1113_N}} entre le 11/07 et le tir, sans mention du nom. Son propre avatar date du 16/07 16:27:11. Une mention d'un montage DMAGA de @kikisknees comme pfp arrive le 17/07 18:58:08 (`1813649402445156470`, @TrvthfvlTreason). Le 11/07, @kikisknees et @Aristos_Revenge échangent sur un problème de DM (`1811456429758243267`), sans parler d'un jeton : ils sont en contact avant le tir, rien de plus. La limite : le compteur de posts ne voit pas un post supprimé avant la capture, et une préparation privée reste possible. Les 20 posts du thread sont supprimés, la phrase exacte n'est connue que par Thread Reader.

**Domaine et chaîne plus anciens, indice C.** Un projet distinct existe : `$DARKMAGA`, Telegram `t.me/darkmagaonsol` créé le 09/05/2024 17:13:36, site darkmagaonsol.com (certificat et Wayback dès le 29/02/2024), X @darkmagaonsol suspendu, mint `6Zoi7ZZE7awFqBsXK44WVnP8T2b96RX1qptBiFSwmJa8`, signataire `DX9i7J3rujZJv7sXqk7pQ6zBZ4ecSGRv958FFfGta6n2` (révocation et brûlage du 09/05, RPC public). Or dmaga.xyz affiche en contact `DarkMAGAonSOL@proton.me` dès juillet 2024 (capture du dépôt). Même chaîne de caractères, rien de plus. Test simple : `DX9i7J3…` n'a aucune ligne dans `trades.parquet` et n'apparaît dans aucun rapport. HYPOTHÈSE, à trancher côté on-chain.

## 6. Question 5, adresses publiées

**Aucun compte du noyau ne publie de wallet dans ce qui est lu.** Inchangé, et mieux couvert : recherche native sur @ChrisWinig et @DarkMagaCoin, {{N_WB}} textes de plus pour @kikisknees. Niveau A pour ce qui est lu, D comme preuve d'absence. @Aristos_Revenge : recherche native vide, posts supprimés.

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
- @CryptoOnlyCoims, 14/07 03:20:42 (`1812326326176469155`) : « Just bought 1 SOL ». Test (`derived/trades_probe.txt`) : aucun achat de 0,9 à 1,1 SOL dans `trades.parquet` entre 03:00 et 03:20:42, {{TP_N}} entre 02:05 et 03:00. Pas de candidat unique, aucun lien posé.
- @SundayFundayLFG et @bazingahappy, 22/07 : « bought with size », après coup, sans adresse.

## 7. Corrections proposées à l'existant, non appliquées

Je n'ai rien modifié hors de `work_E`. Le choix revient à Benjamin.

| Fichier | Écrit | Fait lu | Preuve |
|---|---|---|---|
| `docs/SOCIAL_FINDINGS.md`, `docs/TIMELINE.md` | les deux dates sont identiques dans tous les cas lus | {{CORPUS_BAD}} lignes sur {{CORPUS_N}} diffèrent : l'id est celui d'un repost | `data/x_posts.jsonl` |
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
{{TABLE}}

## 9. Sources essayées

| Source | Essai | Résultat | Ce que cela prouve ou non |
|---|---|---|---|
| Recherche X native, navigateur connecté | 30 recherches, onglet Récents, `x_search_log.jsonl` | 24 lisibles, 2 perdues sur délai, 3 vides sur erreur probable, 1 erreur affichée | Lecture seule, aucune action d'écriture. La plus utile. Absent ne veut pas dire inexistant |
| Post @pmarca ouvert par id | 1 page | Lien vers @kikisknees visible | Capture d'écran gardée, elle montre le pseudo du compte connecté |
| api.fxtwitter.com et syndication | {{N_LIVE}} posts lus | Réponses brutes dans `evidence/x_raw_new/` | Un post supprimé répond indisponible |
| Wayback, captures de status @kikisknees | {{WB_OK}} réponses 200 sur toute la Wayback, {{WB_ERR}} refus ou 5xx, reprises avec pauses | Voir la couverture en partie 3, {{PARSE_ERR}} captures non JSON | Reste une limite de collecte, pas une absence |
| Wayback CDX, médias `pbs.twimg.com/media/<clé>*` | Environ 40 clés, dont un lot de 99 images de @kikisknees coupé par l'arrêt forcé | {{N_MEDIA_WB}} images récupérées, le reste en refus de connexion ou 503, ou non demandé | Méthode reproductible. La grande majorité des {{KIKI900_N}} images 900 x 900 de @kikisknees antérieures au 21/07 12:51 ne sont pas lues : une V1 antérieure à 12:50:45 n'est pas exclue |
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
