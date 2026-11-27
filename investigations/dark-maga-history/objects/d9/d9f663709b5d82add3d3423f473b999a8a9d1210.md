# DMAGA : constats sociaux et documentaires

Session sociale et documentaire, 2024-2026, collecte du 02/11/2026. Mint : `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`.
Aucune collecte on-chain. Fichiers écrits : `data/x_posts.jsonl`, `data/x_candidates.jsonl`, `data/social_wallet_mentions.jsonl`, `evidence/` et ce document.

Conventions : **[FAIT]** observé dans un fichier sauvegardé ; **[DÉCLARATION]** ce qu'un compte ou un média affirme, non prouvé ; **[HYPOTHÈSE]** à vérifier. Les heures sont en UTC. Fiabilité : A = métadonnée ou capture horodatée de la source elle-même, B = un seul média ou un seul compte, C = déclaration non étayée.

> **Correctifs du 06/11/2026 (rejeu historique, `investigations/2026-11-06_historical_replay/FINDINGS.md` §1-2).** Le texte d'origine ci-dessous n'est pas réécrit ; ces points le remplacent.
> - Cinq identifiants cités ici sont des **reposts** : fxtwitter et le point d'intégration rendent l'original, dont l'auteur, la date et le texte ont été recopiés sous l'ID du repost. Originaux : @pmarca `1814763940410499481` (20/07 20:46:54Z, et non 21:47:23Z) et `1814920352134537332` (21/07 07:08:26Z, et non 12:43:30Z) ; @kanpai `1812984492157771825` (15/07 22:56:01Z, « Wild PA… ») et `1813086353741230327` (16/07 05:40:46Z, seul à parler des pfp rouges aux yeux bleus) ; @CryptoOnlyCoims `1812326326176469155` (14/07 03:20:42Z, et non 03:23:16Z). Les URL d'archive des reposts sont au nom de @DarkMagaCoin (preuve faible : X redirige toute URL).
> - **Borne haute du changement de photo de Musk : 19:27:24Z** (post `1815106321810919673` de @AutismCapital, capture du profil, avatar à pHash 4/64 du visuel ; médiane 30 sur 703 médias). Fenêtre documentée : [19:03:27Z ; 19:27:24Z], 23 min 57 s. L'heure est celle du post, pas du clic.
> - Sur l'ensemble du corpus : 482 reposts sur 5 156 observations (372 résolus par les API, 110 par les charges Wayback). Les 372 écarts entre métadonnée et ID s'expliquent tous ainsi.

Limites générales, valables pour tout le document :
- Aucune recherche X native : les ids viennent d'articles, de la Wayback CDX et des posts suivis. Un post absent de ces listes n'est pas vu, ce n'est pas la preuve qu'il n'existe pas.
- Les lignes de `x_posts.jsonl` dont le `source_note` dit « Wayback CDX list for DarkMagaCoin » (ou kikisknees) ne sont PAS toutes écrites par ce compte : la CDX liste des URL `/<compte>/status/<id>` dont l'id appartient souvent à un tiers (citation, reprise, capture d'un fil). L'auteur réel est celui renvoyé par fxtwitter. Le lien entre le compte et ces posts n'est pas établi.
- Dates : `created_utc_snowflake` est toujours calculée depuis l'id ; `created_utc_metadata` vient de l'endpoint public (identique dans tous les cas lus).

---

## 1. Thread d'@Aristos_Revenge du 08/10/2024 (id 1843704335823454430)

**Fichiers** : `evidence/web/threadreader_1843704335823454430.html` (HTML brut, 69 755 octets, HTTP 200) et `.txt` (texte extrait) ; copie `..._dothtml.html` (variante `.html`, 66 779 octets). Wayback : la CDX ne liste que `threadreaderapp.com/thread/1843704335823454430.html` aux dates 2024-10-08 20:36:17 et 2025-11-09 13:22:15 (pas téléchargées : l'archive répondait 429 puis hors service par moments ; le texte lu en direct suffit, il porte « Oct 8 • 20 tweets »).
**Les 20 posts sont indisponibles en direct** : syndication = `TweetTombstone` « This Post was deleted by the Post author » (les 20 ids), fxtwitter = 404 (`{"code":404,"message":"NOT_FOUND"}`). Le compte existe encore : `api.fxtwitter.com/Aristos_Revenge` répond 200 (profil `evidence/web/profiles/fx_Aristos_Revenge.json` : créé le 2022-06-20, 140 424 abonnés au 02/11/2026, 17 447 posts). Un premier appel avait répondu `User not found` : fxtwitter est instable, une 404 isolée ne prouve rien ; le tombstone de la syndication, lui, est explicite. Constat : les posts ont été supprimés par leur auteur, la date et la raison ne sont pas connues. Observation sans conclusion : ce compte date de juin 2022, le thread parle de janvier 2022. Le seul texte intégral disponible est donc celui de Thread Reader (fiabilité B : un agrégateur tiers, pas une capture de X).

Ids des 20 posts (attribut `data-tweet` du HTML, ordre du thread) : 1843704335823454430, 1843704340143616145, 1843704343717183562, 1843704346451816614, 1843704349861773555, 1843704353804431506, 1843704357608718578, 1843704360691536204, 1843704363300335635, 1843704366429241676, 1843704371336630475, 1843704378672460047, 1843704382246076710, 1843704385119088992, 1843704389229523437, 1843704393348329977, 1843704397362278671, 1843704401564971049, 1843704404974940482, 1843704408238182472. Tous du 2024-10-08 entre 17:25:42Z et 17:26Z (snowflake).

**Ce que dit le thread (DÉCLARATIONS d'Aristos_Revenge, non vérifiées)** :
- Histoire : en janvier 2022, quelqu'un dans un groupe de discussion privé aurait plaisanté qu'une image de Yugi (Yu-Gi-Oh) était « Dark MAGA » ; des montages de Trump « gothique » et des pfp aux yeux laser ont suivi, y compris pour des politiques. Des « hit pieces » (il cite ISD et Mother Jones 2022) ont pris la blague au sérieux ; les « Dark Brandon » seraient une réaction. Le groupe « a rangé » le sujet.
- Wifejak : « cette année » un membre d'un groupe de discussion aurait lancé « Wifejak » ; « l'un de nos gars qui fait de la crypto » aurait fait une memecoin Wifejak qui « a fait de l'argent ». Aucun nom ni contrat n'est donné.
- Prototype politique : l'idée de « Culture Coin » (incitation financière à un certain type de posts) ; test avec « une pièce prototype de nature politique sur Solana », avec un Telegram « de jeets » qui postait du contenu politique. « Cette pièce a plutôt bien marché », « beaucoup d'erreurs » sur la gestion d'une memecoin. Nom et contrat non donnés.
- DMAGA : « @kikisknees a lancé @DarkMagaCoin » et fabriquait des pfp avec le filtre rouge et les yeux laser, « pour moderniser l'esthétique Dark MAGA de 2022 ». « Deux jours plus tard Trump a survécu à une tentative d'assassinat à Butler » ; « Kiki travaillait en heures sup ».
- Adoption : « ce qu'on n'avait pas prévu, c'est qui utiliserait les pfp : Andreessen, @basedmikelee, puis, à notre surprise, Elon Musk lui-même. La pièce a explosé, et quelques jours plus tard Musk est revenu à sa pfp normale. » (Surprise déclarée.)
- Réseau : « des gens du groupe suivis par Elon, donc il avait de la visibilité » ; « beaucoup de comptes proches d'Elon » ont posté des actualités avec leurs images DMAGA. L'objectif déclaré était d'amener Musk à remettre sa pfp. Il cite le Daily Dot.
- Fin : Musk au rassemblement de Butler (« pas seulement MAGA, mais Dark MAGA »), la campagne reprend l'expression ; « ce qui est arrivé à $dmaga est exactement ce à quoi on pouvait s'attendre, à vous d'en juger » ; l'objectif était de voir si on peut « faire passer une idée et une esthétique sur les lèvres de sénateurs, d'un président et d'un des hommes les plus riches du monde » et si « des masses de types de la crypto » peuvent soutenir une élection, « juste pour voir ».
- Wallets et contrats cités : **aucun** dans les 20 posts (le seul identifiant de type adresse du HTML, `3ATGMxNzCUFzxpMCHL5sWSt4DVtS8UqXpi`, est du texte du bandeau latéral de Thread Reader, format non Solana, sans lien avec le thread ; non retenu).

**Écarts avec les sources lues** (faits, pas de procès d'intention) :
- Chronologie : Aristos écrit que le lancement de DarkMagaCoin a eu lieu deux jours avant Butler. Les traces archivées disent autre chose : chaîne Telegram @DMAGACoin « Channel created » `2024-07-14T01:57:02+00:00` (point 6), premier post archivé de @DarkMagaCoin `1812321235688157500` le 2024-07-14T03:00:28Z, capture Wayback de dmaga.xyz le 2024-07-14T03:31:32Z avec le mint déjà affiché. Le tir de Butler date du 13/07/2024 (connaissance générale, non revérifié ici). La CDX n'est pas exhaustive : un post antérieur non archivé reste possible. La date de création du mint appartient à la session on-chain.
- Jonction 2022 : le terme « Dark MAGA » est documenté par Mother Jones (20/05/2022, `evidence/web/motherjones_2022_05_cawthorn.html`) : conversation Twitter Spaces « Dark MAGA is inevitable » en mars 2022, hashtag #DarkMAGA, fil d'Urban Dictionary. Le « janvier 2022 » du thread n'est pas confirmé ; le plus ancien jalon lu est mars 2022. Un post de mars 2022 cité par l'article (`1504954278338826242`, @ConservativeIn9, 2022-03-18T22:53:55Z) est indisponible.
- Surprise : le thread dit que l'adoption par Musk a surpris l'équipe. @DarkMagaCoin écrit le 2024-07-22T08:10:21Z (`1815298322325811663`) que « l'équipe DMAGA a créé la pfp d'Elon spécialement pour lui, il l'a choisie après qu'un membre de l'équipe la lui a envoyée en DM », puis le 2024-07-24T06:40:49Z (`1816000567740633335`) « non, il ne l'a pas fait. On lui a envoyé le mème et il l'a aimé » (réponse à un tiers). Le Daily Dot note que le compte n'a fourni aucune preuve du DM. DM revendiqué, non prouvé.

**@Aristos_Revenge 1815128699831796065** (21/07/2024 20:56:20Z par snowflake) : indisponible (même tombstone « deleted by the Post author »). Wayback : CDX `twitter.com/Aristos_Revenge/status/1815128699831796065` et `x.com/...` : réponse vide `[]` ; CDX de tout le compte (twitter.com et x.com) : 0 status archivé (`evidence/x_cdx/Aristos_Revenge.json` = `[]`). Aucune capture du texte original n'existe donc dans la Wayback ; le texte vient du Daily Dot seul. Texte connu seulement par le Daily Dot (`evidence/web/dailydot_dark-maga.html`) : épinglé, « If you want a red dark Maga pfp, visit http://dmaga.xyz courtesy of the $dmaga coin. It has a conversion tool » ; fiabilité B (citation d'un journaliste). Le Daily Dot présente aussi le compte comme l'un de ceux qui ont changé de pfp.

---

## 2. Article Daily Dot (22/07/2024)

Fichier : `evidence/web/dailydot_dark-maga.html` (222 637 octets, HTTP 200 sur `https://dailydot.com/dark-maga-laser-eye-pfp-trump-musk-andreessen`) et `.txt`. L'URL avec `www.dailydot.com/debug/...` répond 404. Auteur : Marlon Ettinger. `datePublished` 2024-07-22T20:57:30+00:00 (page : « 3:57 PM CDT on July 22, 2024 »), `dateModified` 2026-02-01T17:15:59+00:00 : le texte lu est la version de 2026, pas forcément celle de 2024.

Identifiants de posts présents dans le HTML : `1815128699831796065` (@Aristos_Revenge, tombstone), `1815298322325811663` (@DarkMagaCoin, archivé), `1815269272370766086` (@WashletJP « Something cringe is afoot », 2024-07-22T06:14:55Z, 1,55 M vues, média `GTEhyAhXYAAzv7j.jpg`, archivé), `1516506143958388737` (@ti_84_plus_c, 2022-04-19, #DarkBRANDON, lien de contexte, archivé). Le tweet `0LTIbw2qj6` est le `pic.twitter.com` de WashletJP (même post).
Faits rapportés par l'article (B) : Musk, Andreessen et Torba ont une pfp rouge aux yeux laser ; liquidité de 1 M USD ; +130 000 % depuis le 21/07 ; le compte DarkMagaCoin n'a pas répondu aux questions de preuve.

---

## 3. Heure du changement de photo de Musk

**Fenêtre documentée : [2024-07-21T19:03:27Z ; 2024-07-21T19:30:13Z]**, et plus précisément le fichier image du nouvel avatar a été téléversé à **19:23:20,585Z**.

Preuves (par ordre de force) :
1. **[FAIT, A] Wayback, profil `twitter.com/elonmusk`** : `evidence/web/wb_elonmusk/twitter.com_20240721190327.html` (capture 19:03:27Z) contient `og:image` `pbs.twimg.com/profile_images/1780044485541699584/p78MCn3B_200x200.jpg` = ANCIENNE photo. `twitter.com_20240721205925.html` (capture 20:59:25Z) contient `profile_images/1815105297410666496/584umYRz_200x200.jpg` = NOUVELLE photo. Les captures 18:45:10Z (twitter.com) et 02:34:33Z (x.com) montrent aussi l'ancien identifiant. Les captures x.com du 21/07 à 14:46, 18:59, 19:00, 20:34 sont des pages vides (2 642 octets) et ne disent rien.
2. **[FAIT, A, calcul]** L'identifiant média 1815105297410666496 est un snowflake : 2024-07-21 19:23:20,585Z. L'ancien, 1780044485541699584 : 2024-04-16T01:24:11Z. Hypothèse de lecture (B) : l'identifiant d'une image de profil X est attribué à l'envoi du fichier, donc le changement a eu lieu à 19:23:20Z ou après (pas avant). À confirmer par un autre exemple.
3. **[FAIT, A] Premier post qui montre le nouvel avatar** : `1815107030606385507` @DavidFBailey, 2024-07-21T19:30:13Z, « 👀🫢 », capture du profil de Musk avec la nouvelle photo (`evidence/x_media/1815107030606385507_GTCOG4JXAAAcJMs.jpg`). Donc changement effectif au plus tard à 19:30:13Z. Aussitôt : @DarkMagaCoin 19:33:05Z (`1815107751745601643`, « Our resident genius @elonmusk has a DMAGA PFP and YOU'RE FADING??? »), @ChrisWinig 19:33:11Z (`1815107774113587625`, « Elon just made this his profile picture! DARK MAGA RISES!!! »), @DzambhalaHODL 19:43:25Z, Times Now 19:41:22Z (`evidence/web/timesnow_111909176.html`, `datePublished`), @wallstreetbets 19:59:04Z, @EleanorTerrett 20:13:52Z (« changed his profile picture to laser eyes », `1815118014494244986`), @KardashevX 20:55:03Z.
4. **Dernier post de Musk sans preuve visuelle avant** : `1815105968381820966` (19:26:00Z, texte, sans média) ; `1815092002083471731` (18:30:30Z). Un post de Musk ne montre pas l'avatar en soi : ces deux ids bornent seulement l'activité.
5. **Cohérence** : @0xSunNFT (`1815221871820046474`) écrit que le cours restait autour de 5 M entre « 3 h 30 et 5 h 30 du matin » (heure de Pékin probable = 19:30 à 21:30Z) ; cohérent avec 19:30Z, sans valeur de preuve (déclaration C).

**Le visuel existait avant** : @ChrisWinig a répondu à « Whoa » de Musk (`1815053805077086351`, 15:58:43Z) par « It's time, Elon » (`1815054750775173447`, 16:02:29Z) avec une image rouge aux yeux laser (`evidence/x_media/1815054750775173447_GTBerExWkAEFQuT.jpg`). À l'œil, cette image est la même composition que la pfp de Musk (visage, drapeau, armure) ; l'analyse perceptuelle formelle est faite ailleurs. Soit 3 h 21 avant le téléversement de l'avatar. Odaily/BlockBeats décrivent ce reply comme l'origine de l'image (B). Fait ≠ cause : ce que Musk a regardé avant de changer n'est pas établi.

**Jalons avant le changement, par @kikisknees (captures Wayback, point 4)** : 16:00:08Z réponse à @elonmusk avec une image (supprimée), 17:00:03Z « vast swathe of blood red pfp's » ; ils confirment que le visuel circulait avant 19:23Z, rien de plus.

**Fin de la pfp (laser)** [FAIT, A] : Wayback `twitter.com/elonmusk` du 2024-07-23T10:43:05Z (`evidence/web/wb_elonmusk/twitter.com_20240723104305.html`) montre encore l'avatar laser (`profile_images/1815105297410666496`) ; celui du 2024-07-23T14:36:29Z (`twitter.com_20240723143629.html`) montre un nouvel avatar `profile_images/1815749056821346304`, dont l'identifiant (snowflake) = **2024-07-23T14:01:24,789Z**. Fenêtre du retour à une photo sans filtre : [10:43:05Z ; 14:36:29Z], téléversement à 14:01:24Z (même lecture que ci-dessus : identifiant attribué à l'envoi du fichier). Concordance : `1815763677447852205` @thesolanapost, 2024-07-23T14:59:30Z, « $LASER and $DMAGA are down 50% and 75% respectively in the last hour after Elon Musk removed his laser eyes PFP » (B). Donc l'avatar laser a duré d'environ 19:23Z le 21/07 à environ 14:01Z le 23/07, soit ~42 h 38 min (calcul sur les identifiants média ; ordre de grandeur). Aristos écrit « quelques jours plus tard » : compatible. Les trois fichiers d'avatar sont dans `evidence/x_media/profile_old_*`, `profile_new_*`, `profile_after_*` (sha256 : ancien `7c9f0800...8541`, laser `bc40a049...d792`, après `28c2cb2f...6e17`). **Constat visuel** : l'ancien et le nouvel avatar « après » sont la même photo de Musk en armure rouge sur fond bleu, sans filtre ; l'avatar laser est un filtre rouge, yeux bleus et drapeau sur une photo de ce type, ce qui est cohérent avec le texte de Winig (« Musk's original head portrait with laser eyes »). L'analyse perceptuelle formelle est faite ailleurs.

**Non trouvé** : la date de la capture d'écran de Bailey (il peut l'avoir prise avant de poster) ; l'heure exacte du clic « enregistrer » de Musk. Les médias qui donnent 20:00 UTC ou « early hours » sont des approximations.

---

## 4. CDX Wayback

Commande : `python3 -m dmaga.xposts cdx <compte>` (twitter.com et x.com, `collapse=urlkey`, `limit=20000` par hôte : une liste proche de 20 000 est peut-être tronquée). Fichiers : `evidence/x_cdx/<compte>.json` ; les plus gros ont été compressés en `.json.gz` pour tenir sous 150 Mo (même contenu). Fenêtre demandée : ids dont la date snowflake est entre 2024-06-01 et 2024-10-31. Un `wayback_ts` identique à la seconde près à la date snowflake et un code `-` (revisit) signalent une capture de flux faite à la publication, pas une page rendue (voir l'encadré kikisknees).

| Compte | ids CDX (total) | dans la fenêtre | ids archivés via `fetch` | ok / indisponibles | posts qui touchent DMAGA (texte) | note |
|---|---|---|---|---|---|---|
| DarkMagaCoin | 4 934 | 2 740 | 1 073 (14/07 au 02/08) | 942 / 131 | 281 | fenêtre de `fetch` restreinte ; les ids dont l'auteur réel est un tiers sont des reprises (voir limites) |
| kikisknees | 19 998 | 4 865 | 1 419 (14/07 au 26/07) | 12 / 1 407 | 5 | 1 378 « deleted by the Post author », 25 « from a suspended account », 2 « limits who can view », 2 autres ; voir encadré |
| Aristos_Revenge | 0 | 0 | 0 | | | liste vide `[]` |
| ChrisWinig | 0 | 0 | 0 | | | liste vide `[]` |
| koreanjewcrypto | 20 255 | 15 | 15 | 15 / 0 | 3 | tous archivés ; premiers posts DMAGA : 15/07 |
| 0xSunNFT | 2 045 | 536 | 95 (14/07 au 05/08) | 82 / 13 | 1 | le post du 22/07 sur DMAGA |
| ai_9684xtpa | 10 698 | 1 320 | 485 (14/07 au 05/09) | 474 / 11 | 4 | contient le post de l'adresse GXZvX (point 5) |
| 0xRamonos | 13 860 | 5 264 | 939 (14/07 au 05/08) | 913 / 26 | 1 | le post du 22/07 (capture 5QhJJc...HScd) ; le reste est du trading sans lien |
| ramonos | 3 744 | 0 | 0 | | | |
| ashrobinqt | 14 230 | 2 198 | 191 (14/07 au 05/08, 60 pour 20/07 à 25/07) | 172 / 19 | 1 | |
| ashrobin | 3 183 | 0 | 0 | | | CDX relancée le 02/11 après un refus de connexion |
| twobitidiot | 19 837 | 124 | 8 (20/07 au 25/07) | 0 / 8 | 0 | tous indisponibles |
| basedmikelee | 18 000 | 10 215 | 559 (20/07 au 25/07) | 477 / 82 | 3 | posts « #NewProfilePic » le 23/07 (point 7) |
| Bluntz_Capital | 6 736 | 1 011 | 37 (20/07 au 25/07) | 34 / 3 | 8 | échanges avec koreanjewcrypto le 21/07 |
| wsbmod | 4 342 | 620 | 49 (20/07 au 25/07) | 42 / 7 | 0 | aucune mention DMAGA |
| wallstreetbets | 19 818 | 9 756 | 254 (partiel, interrompu) | 215 / 39 | 0 | seul post pertinent : `1815114291281817967` « We're so fucking back @elonmusk », 2024-07-21T19:59:04Z |
| WashletJP | 14 601 | 391 | 1 | 1 / 0 | 0 | seul le post cité par le Daily Dot ; le reste de la fenêtre n'a pas été archivé |
| @elonmusk | non demandée | | | | | posts cités seulement (point 3) |

Cause des trous : arrêt volontaire des `fetch` hors noyau pour rester sous le plafond de 150 Mo ; la Wayback a refusé des connexions (`Connection refused`, HTTP 503, timeouts) à plusieurs reprises le 02/11 et a ralenti la récupération du point suivant. Le noyau (les 4 premiers comptes) est couvert comme suit : DarkMagaCoin du 14/07 au 02/08, kikisknees du 14/07 au 26/07, Aristos_Revenge et ChrisWinig sans aucun status archivé.

**Encadré kikisknees : posts supprimés, texte récupérable dans la Wayback** [FAIT, A]. Sur les 1 419 ids de @kikisknees du 14/07 au 26/07/2024, 1 407 sont indisponibles en direct (tombstone « deleted by the Post author » pour 1 378 d'entre eux ; 25 « from a suspended account », probablement des reprises de comptes suspendus ; 2 « limits who can view » ; 2 autres) alors que ses posts de mars 2022 sont lisibles. La Wayback conserve pour ces ids une capture de l'API v2 de X (JSON, `wayback_ts` = heure du post, compteurs à zéro : prise à la publication, probablement par un collecteur de flux). Récupération : `evidence/x_wayback/recovered.jsonl` (une ligne par id : texte, `created_at`, `author_id`, pseudo, médias, références, sha256 et taille de la capture) et `evidence/x_wayback/<id>.raw` (capture brute). Ces captures contiennent aussi des profils : `author_id 1474749663039401987` = kikisknees, compte créé le 2021-12-25, 7 509 abonnés au 14/07/2024. La récupération est partie des ids les plus proches du 21/07/2024 20:00Z ; elle a été interrompue par les refus de la Wayback. **Couverture au moment de l'arrêt : 244 ids tentés, 225 captures lues** (208 de kikisknees datées du 2024-07-14T00:00:08Z au 2024-07-22T06:52:31Z, 17 de DarkMagaCoin), 19 erreurs (connexion refusée ou 503) consignées dans `recovered.jsonl` avec le champ `error`. Les ~1 150 autres ids indisponibles de kikisknees (22/07 au 26/07 surtout), de DarkMagaCoin (114 sur 131), de 0xSunNFT, ai_9684xtpa n'ont pas été récupérés : l'absence de texte pour eux est une limite de collecte, pas une preuve. La suppression est un fait ; sa date, son auteur effectif et son motif ne le sont pas. Les images jointes sont en 404 sur `pbs.twimg.com` (testé sur 6 médias de kiki du 21/07).

Ce que ces captures de kikisknees disent (DÉCLARATIONS de kikisknees, A pour la date, C pour le contenu) :
- `1815054158367432804` 2024-07-21T16:00:08Z, réponse à `@elonmusk` (post `1815053281925767571`) : « He survived, they didn't expect that. » avec une image (supprimée) ; 3 minutes avant le post de ChrisWinig.
- `1815069240304509322` 17:00:03Z (avant le téléversement de l'avatar de Musk à 19:23Z) : « Imagine being a libtard on Twitter and seeing a vast swathe of blood red pfp's laughing at you ... Dark MAGA is a movement. »
- `1815078341659246690` 17:36:13Z : « MAGA chad @twicrates might tell you this ticker if you ask nicely ».
- `1815116229117690314` 20:06:46Z, réponse à @blknoiz06 : « $DMAGA pfp by me and @ChrisWinig » ; `1815116385414209876` 20:07:24Z : « That's a $DMAGA pfp, made by me. ».
- `1815121075904168102` 20:26:02Z, réponse à @wallstreetbets et @elonmusk : « Nice $DMAGA pfp Elon. 7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump ».
- `1815125720785391758` 20:44:29Z : « I almost didn't believe my eyes when I looked and saw that @elonmusk decided to use a wartime PFP that we made for him. But it's real, so no blackpilling. » (cohérent avec la surprise déclarée dans le thread ; le post a été écrit 74 minutes après le premier screenshot du nouvel avatar).
- `1815149897567375822` 22:20:34Z : « We have a Dark MAGA pfp maker working now on the website ... Buy $DMAGA. »
- 14/07/2024 : `1812521301682069933` 16:15:27Z « I heard @twicrates was going to buy 60% of the supply of this in revenge for what happened yesterday. I also heard that Dark Patriots are in control. » (image supprimée) ; `1812527580282495222` 16:40:24Z « There can be only one. » (citation de `1812357823264596171`).
Un « DM envoyé à Musk » n'apparaît dans aucune de ces captures ; kiki écrit « that we made for him », pas « that we sent him ».

---

## 5. Pistes wallets

Fichier : `data/social_wallet_mentions.jsonl` (6 lignes : `post_id` ou `url`, `auteur`, `adresse_telle_quecrite`, `tronquee`, `montants_rapportes`, `date_utc`, `sha_source`, plus `fichier` et `note`).

**GXZvX... (22/07/2024)** : retrouvé. Post original `1815243177475121253` de `@ai_9684xtpa`, 2024-07-22T04:31:13Z (snowflake et métadonnées), `evidence/x_raw/1815243177475121253.fx.json`. Le corps du texte l'écrit tronqué `GXZvX...ZG2Ra`, mais le lien solscan du même post contient l'**adresse entière** `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` (44 caractères, base58 valide ; lien : `https://solscan.io/account/GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra?token_address=7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump#balanceChanges`). Montants rapportés par @ai_9684xtpa (DÉCLARATION non vérifiée on-chain, à confronter à la session on-chain) : achat de 48,5 SOL pour 14,69 M de DMAGA, prix moyen 0,0004826 USD, « six jours avant » ; vente de 136 000 USD une heure avant le post (qu'il relie à une baisse de 41,89 % vers 0,4211 USD) ; 66 % de la position vendue, profit réalisé 210 000 USD, reste 5 M DMAGA (latent 340 000 USD), rendement 7688 %. Reprises : ChainCatcher `2134603` (publié 2024-07-22T04:47:05Z), qklw.com, BlockBeats flash 257312 (tronqué à `GXZvX`), PANews/AiCoin `409533` (`GXZvX…ZG2Ra`) : toutes tronquées, aucune ne donne l'adresse entière. Fiabilité : A pour l'existence du post et de l'adresse écrite, C pour les chiffres. Le même compte relie le post à `https://x.com/0xSunNFT/status/1815221871820046474` (post suivant, 04:32:21Z).

**9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq (août 2024, DMAGA et ELON)** : **introuvable**. Cherché : l'adresse entière en recherche web (WebSearch et Exa : 0 résultat pertinent), son préfixe `9PrmF8sf` couplé à DMAGA et ELON (rien), les textes des quelque 5 200 posts archivés (`x_posts.jsonl`) et des pages sauvegardées (`grep` : 0 occurrence hors mes propres requêtes dans `exa_searches.txt`). Causes : il n'y a pas de recherche X native ici ; les posts d'août de @DarkMagaCoin et @ai_9684xtpa n'ont été archivés que jusqu'au 02/08 et au 05/09 respectivement, sans occurrence ; l'origine de cette adresse (quelle source l'a donnée à la session on-chain) ne m'a pas été communiquée. Aucune adresse n'est devinée.

**Adresses tronquées vues sur des captures** (posts du 22/07, noyau de la piste « achat avant Musk ») :
- `5QhJJc...HScd` : capture dans `1815221876190294470` (@ramonos, 2024-07-22T03:06:35Z) : « Dolphin », achat 4 962 USD pour 28,4 M DMAGA (37 txns), vendu 0, latent 1,8 M USD, « Holder since: 7d 8h » ; le texte du post dit pourtant « 3 jours ». Contradiction interne non résolue.
- `H3QsBr...T6cc` : capture dans `1815233925662306427` (@ashrobin, 2024-07-22T03:54:27Z) : « Whale », achat 1 086 USD pour 16,8 M DMAGA (2 txns), vendu 175,9 K USD pour 2,6 M, latent 1,0 M USD, « 7d 11h ». La capture DexScreener jointe montre un maker `szT6cc` qui vend 336 000 DMAGA par lot ; la fin concorde (`T6cc`), sans preuve d'identité. La même capture indique « Pair created 8d 1h ago » à l'heure de l'horloge de la capture (22:51:41 UTC-5, soit 03:51:41Z le 22/07), donc paire Raydium créée vers le 14/07 ~02:50Z (lecture approximative).
- Créateur pump.fun `8YLE…zBzR` (page du jeton, extrait Exa non daté ; à résoudre on-chain).
**Aucune de ces adresses n'est complétée.**

Autres adresses vues dans les posts de @ai_9684xtpa et sans lien avec DMAGA (autres sujets) : non retenues.

---

## 6. Adresses et infrastructure publiées par les comptes du noyau

Faits (FAIT, sauf mention) :
- **Mint** `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump` : publié par @DarkMagaCoin dès `1813030370260230389` (2024-07-16T01:58:19Z) « Come join us Dark Patriot. t.me/DMAGACoin ca: 7D7B... » ; bio actuelle du compte : « Dark MAGA patriots in control | $DMAGA / Join us on telegram: https://t.me/DMAGACoin / CA: 7D7B... » (compte créé le 2024-06-11T16:25:03Z, `evidence/web/profiles/fx_DarkMagaCoin.json`).
- **Paire/pool** `CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k` : `1814470221849034981` (@DarkMagaCoin, 2024-07-20T01:19:46Z, lien GeckoTerminal « thanks to the Coingecko team »). Les copies minuscules de cette adresse dans des posts de @koreanjewcrypto (`1815131732464882018`) et @bazingahappy sont des URL dexscreener mises en minuscules, pas l'écriture originale.
- **Jupiter** : `1817954689130098730` (2024-07-29T16:05:48Z) « DMAGA has been Strict Listed by @JupiterExchange » avec lien `jup.ag/swap/SOL-7D7B...` ; annonce préalable `1817648228575379795` (07-28).
- **Aucune adresse de don ni wallet revendiqué** n'est publié par @DarkMagaCoin, @ChrisWinig, @kikisknees (fenêtre archivée) ni dans le thread d'Aristos. Les bios actuelles (`profiles/`) de kikisknees, ChrisWinig, koreanjewcrypto et Aristos_Revenge ne contiennent pas d'adresse.
- **dmaga.xyz** : captures Wayback `evidence/web/wb_dmaga_xyz_*.html` (id_ = octets d'origine). **2024-07-14T03:31:32Z** : le site existe avec le mint affiché (`7D7B...`), lien Telegram invité `https://t.me/+30sxDUsH64cyYzdh`, lien `x.com/DarkMagaCoin` (page de 76 Ko). 2024-07-23T09:32:56Z : ajout « DARK MAGA YOUR PFP (right click on the image to save) » et « Contact: DarkMAGAonSOL@proton.me » (adresse de contact publiée par le projet). 2024-08-08 : même contenu. 2024-09-11T22:23:56Z : 404. Le `robots.txt` du 14/07 existe. La capture date de 31 minutes après le premier post archivé de @DarkMagaCoin (03:00:28Z) : le site existait au plus tard à 03:31:32Z, et sa date de mise en ligne n'est pas bornée par le bas.
- **darkmaga.com** : capture 2024-09-19 et 2024-10-08 (`wb_darkmaga_com_*.html`) : même site DMAGA (« PRESS THE BUTTON TO OPEN THE DARK MAGAFY APP »). Le domaine : RDAP `darkmaga.com` enregistré le **2022-03-15T19:11:08Z**, registrar GoDaddy, NS Afternic (à vendre), dernier changement le 2026-11-02 (`evidence/web/rdap_darkmaga.com.json`) ; le propriétaire de 2024 n'est pas public. Coïncidence de date à noter, sans conclusion : le plus ancien status archivé de @kikisknees est du 2022-03-15T20:16:59Z et le thread d'Aristos situe l'origine en 2022. Aucune pièce ne relie le domaine à une personne.
- **dmaga.xyz (RDAP)** : enregistrement actuel du 2025-09-29, registrar CommuniGal, donc le domaine a changé de main après 2024 (la page de 2024 appartient à l'ancien titulaire, inconnu). **darkmagacoin.com** : enregistré le 2024-10-07 (après les faits ; non pertinent pour juillet). Whois en direct : le serveur n'a pas répondu (`whois: connect(): Operation timed out`), RDAP utilisé à la place. Les données personnelles sont masquées ; aucune n'a été recherchée.
- **Telegram** : `https://t.me/s/DMAGACoin` (`evidence/web/tg_DMAGACoin.html`) : chaîne « Dark MAGA Verification Portal », 1,26 K abonnés, « Channel created » à `2024-07-14T01:57:02+00:00` (la page ne donne que l'heure du message de service), 1er message visible du 2024-07-16 18:53 (« being protected by @SafeguardClick », 26,5 K vues). Le groupe de discussion n'est pas lisible sans compte. Le lien invité `+30sxDUsH64cyYzdh` n'a pas été ouvert (aucune connexion).
- **Pages d'outil PFP** vues dans les résultats : `dmagafy.netlify.app` et `darkmagapls.com/pfpapp` ; non archivées, appartenance non établie.

---

## 7. Recherche web, premières mentions, Wifejak, prototype

**Premières mentions de DMAGA** (dates snowflake, fiabilité A sauf mention) :
- 2024-07-14T01:57:02Z : création de la chaîne Telegram (voir point 6).
- 2024-07-14T03:00:28Z : premier post archivé de @DarkMagaCoin `1812321235688157500` « Dark MAGA patriots in control. $DMAGA » (vidéo, non téléchargée).
- 2024-07-14T03:23:16Z : première mention tierce lue, `1812326972661412024` @CryptoOnlyCoims « Just bought 1 SOL worth of Dark MAGA $DMAGA ... Contract Address: 7D7B... ».
- 2024-07-14 : Wayback `dmaga.xyz` à 03:31:32Z ; kikisknees promeut « this » le jour même (16:15:27Z).
- 2024-07-15T16:45:07Z et 16:56:29Z : @koreanjewcrypto « It's time to get dark maga » puis « Patriots in control. The ticker is $dmaga ». @DarkMagaCoin écrit le 21/07 22:23:53Z que « KJ has been in our corner from DAY ONE » (DÉCLARATION) ; PANews écrit que KJ Crypto est « a member of the DarkMAGA team » (DÉCLARATION relayée) ; @koreanjewcrypto écrit lui-même « $dmaga was made a week ago and Elon is literally using the pfp they made for him » (1815150606967017711, 21/07 22:23:23Z), à la 3e personne.
- 2024-07-16 : @kanpai `1813004360592552354` (00:14:58Z) et `1813220461867573395` (14:33:40Z) : « Everyone's pfps will be red tinted with blue laser eyes ».
- 2024-07-17T21:06:43Z `1813681762188345683` @DarkMagaCoin : « We have the best content creators on our team, like @ChrisWinig » ; `1815502699888087492` (22/07 21:42:28Z) « one of our media team leads, Chris Winig » ; @Shill_Matic1 (`1815173943159931297`, 21/07 23:56:07Z) écrit « $DMAGA admin @ChrisWinig » (DÉCLARATION d'un tiers). @saiyananakamoto (`1816215029655691487`, 24/07) annonce être « officially part of the Dark MAGA mod team ».
- Avant DMAGA : « Dark MAGA » existe depuis mars 2022 (Mother Jones, 20/05/2022, point 1).

**Le visuel et les comptes qui l'ont repris avant Musk** : @pmarca publie le 2024-07-20T21:47:23Z (`1814779160377602331`) et le 2024-07-21T12:43:30Z (`1815004677160776126`, « THAT'S RIGHT. ») une image rouge à yeux laser (Charlie Brown au drapeau, vérifiée à l'œil sur `evidence/x_media/1814779160377602331_GS9WLZJbIAMcF-_.png`), soit environ 21 h avant l'avatar de Musk ; @DarkMagaCoin répond à @pmarca le 20/07 21:52:50Z (`1814780532666040732`, « Defenders of Freedom, rise! »). @DzambhalaHODL (`1815110350351781888`, 19:43:25Z) écrit que les yeux laser de Musk « are downstream of @pmarca ». @haruspectra `1815077079928443383` « #NewProfilePic » (17:31:13Z). @wallstreetbets (19:59:04Z) et @EleanorTerrett (20:13:52Z) réagissent après. Après le 21/07 : @BasedMikeLee publie « #NewProfilePic » avec une image le 2024-07-23T13:01:10Z (`1815733899349155922`) ; trois autres posts identiques le même jour (05:58:35Z `1815627550988878128`, 06:04:20Z `1815628995800785227`, 18:26:36Z `1815815797245431848`) sont listés mais leurs images ne sont pas toutes téléchargées. Mike Lee n'est pas cité dans le Daily Dot ; le thread d'Aristos le cite. Proximité politique, pas attribution financière.

**Posts utiles, DÉCLARATIONS** : `1816450777453342888` @trader1sz (25/07 12:29:48Z) « Elon now posting DMAGA pic on his alt acc » (non vérifié) ; `1816846863649124596` @DarkMagaCoin (26/07) « we built DMAGA first, sent Elon his pfp second » ; `1818007760237187308` @CristusVictor (29/07) « Trump posted a screenshot of Elon with a Dark MAGA pfp » (non vérifié) ; `1815295193853100323` @DarkMagaCoin « @cb_doge Welcome to the DMAGA team! » (22/07 07:57:55Z), réponse de bienvenue non réciproque : rien n'indique que @cb_doge soit membre.

**Wifejak et prototype politique** : le thread ne nomme aucun contrat. Recherche : « WIFE (wifejak) » `4y3oUrsJfSp431R3wJrWiaLxRPsnYtpkVJmoV2bYpBiy` (Solflare, DexRabbit), « WIFEJAK » `8AciyqMog6ERxrvu2H8o36CLbzfD6g6pjH3ZKrBrcPAK` (orbmarkets), au moins une douzaine de clones pump.fun, et le site `wifejak.fun` (« WIFE JAK ON ETH », contrat Ethereum `0xbF32358EB5C2bb6884917d409939522bE83071f4`, page non datée). **Aucun n'est relié par une source lue à @Aristos_Revenge ou à son groupe** : pas d'attribution. Le prototype politique sur Solana : non identifié (aucun nom, aucun contrat dans le thread, aucune source tierce lue).

**Homonymes DMAGA à ne pas agréger** : Ethereum `0x5640e0560e6afd6a9f4ddb41230d0201d181fea7` (Zerion « DARK MAGA (DMAGA) »), Ethereum `0x8bbd724923f7fb00efc04d451acef0a4dbbe566c` (deportfolio « DARK MAGA on Ethereum », CoinGecko « dark-maga-2 »/« 2ea7ec »), Solana « Dark Maga P-Nut » `GDGDUfKsALzQsuVYezURap2adARmTsv2SUuX2ACzpump` (pump.fun, dérivé), « DARK ELON », « LASER ». Aucun n'est le mint `7D7B...`.

**Sources de presse sauvegardées** (`evidence/web/`) : Odaily/BlockBeats 22/07 (`odaily_5197004.html`, 2024-07-22 14:59 UTC+8), ChainCatcher 2134649 (`2024-07-22 16:42:01`), Coinlive 15 548 % (`2024/07/22 15:36`), Times Now (19:41:22Z), Bitcoin.com (08:30:52Z), Bitcoinist (2024-07-22T06:04:28Z), Deccan Herald (16:45 IST), PANews/AiCoin. Pages bloquées en direct : Benzinga (HTTP 403 Cloudflare), Crypto Briefing (403), BlockBeats `news/54305` (403), streetbeat (HTTP 000). Crypto.news « Dark MAGA coin spikes » (Butler) sauvegardé : `cryptonews_dmaga_butler.html` (non exploité ici).

---

## 8. Visuels

- Médias : `evidence/x_media/` (originaux `name=orig` pour les posts jusqu'au 22/07 ~06:15Z, miniatures `360x360` ensuite pour tenir sous 150 Mo) ; sha256, url source et octets pour chacun : `evidence/x_media_manifest.jsonl`. Les vidéos (@DarkMagaCoin, plusieurs mp4 de 6 à 18 Mo, dont le premier post du 14/07) n'ont pas été conservées (plafond) ; leurs urls restent dans `x_posts.jsonl`. Les médias de kikisknees des captures Wayback sont en 404.
- Candidats : `data/x_candidates.jsonl`, 381 posts avec auteur, date snowflake (et métadonnée), url, texte, fichier et sha256 des médias téléchargés. Critère : tri couleur automatique (rouge moyen > 1,8 x vert moyen sur vignette 32x32), puis relecture à l'œil de planches-contact ; **ce n'est ni l'analyse perceptuelle ni une preuve de yeux laser**. Auteurs : 284 pour @DarkMagaCoin, le reste réparti sur une soixantaine de comptes.
- Ce que montrent les planches (observation) : dès le 14/07, @DarkMagaCoin publie des portraits de Trump en rouge avec yeux bleus lumineux (« YOU MISSED », « Dark MAGA Rises »), donc le style rouge/laser précède de 7 jours l'avatar de Musk ; l'avatar de Musk est un portrait de Musk à l'armure sur drapeau, dans la même palette. Le visuel de ChrisWinig `1815054750775173447` est l'image de cet avatar (comparaison à l'œil) avant le téléversement.
- Le plus ancien candidat : `1812333956131344692` @DarkMagaCoin 2024-07-14T03:51:01Z (« You cannot kill Dark MAGA »).

---

## Adresses Solana complètes trouvées (avec la source)

| Adresse | Nature | Source exacte |
|---|---|---|
| `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump` | mint DMAGA | `x_posts.jsonl` id `1813030370260230389` (et 15 autres) ; `evidence/web/wb_dmaga_xyz_20240714033132.html` |
| `CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k` | paire/pool DMAGA (Raydium, GeckoTerminal, DexScreener) | `x_posts.jsonl` id `1814470221849034981` (écriture originale) |
| `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` | wallet d'un acheteur précoce (déclaré par @ai_9684xtpa) | post `1815243177475121253`, `evidence/x_raw/1815243177475121253.fx.json` (lien solscan) |

Adresses vues seulement **tronquées** (non complétées) : `5QhJJc...HScd`, `H3QsBr...T6cc`, `szT6cc` (6 derniers), `8YLE…zBzR` (créateur pump.fun), `GXZvX...ZG2Ra` (forme tronquée du post de la ligne précédente).
Adresses non Solana relevées : Ethereum `0xbF32358EB5C2bb6884917d409939522bE83071f4` (wifejak.fun), `0x5640e0560e6afd6a9f4ddb41230d0201d181fea7`, `0x8bbd724923f7fb00efc04d451acef0a4dbbe566c` (homonymes) ; Tron `TDMMKKFrsE4zd7WUQ7duFxbMoLFdEB8Brm` (post de koreanjewcrypto du 21/08, sans lien avec DMAGA).
Adresse introuvable : `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` (fournie par la consigne, aucune source sociale trouvée).

## Évaluation des outils de recherche X

README lus sans les exécuter (`evidence/web/readme_vladkens_twscrape.md`, `readme_d60_twikit.md`, via `gh`, lecture seule). **twscrape** : « requires authorized X/Twitter accounts » (pool de comptes ; mise en place recommandée par cookies `auth_token` et `ct0` exportés d'un navigateur connecté). **twikit** : exemple `client.login(...)` avec identifiant, mot de passe et `cookies_file`. Les deux exigent donc un compte X connecté, ce que la consigne exclut : non utilisés. Grok : sans crédit (consigne). Aucun accès authentifié ni navigateur de l'utilisateur n'a servi.
