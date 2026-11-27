# DMAGA : constats sociaux et documentaires

Session sociale et documentaire, 2024-2026, collecte du 02/11/2026. Mint : `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`.
Aucune collecte on-chain. Fichiers écrits : `data/x_posts.jsonl`, `data/x_candidates.jsonl`, `data/social_wallet_mentions.jsonl`, `evidence/` et ce document.

Conventions : **[FAIT]** observé dans un fichier sauvegardé ; **[DÉCLARATION]** ce qu'un compte ou un média affirme, non prouvé ; **[HYPOTHÈSE]** à vérifier. Les heures sont en UTC. Fiabilité : A = métadonnée ou capture horodatée de la source elle-même, B = un seul média ou un seul compte, C = déclaration non étayée.

Limites générales, valables pour tout le document :
- Aucune recherche X native : les ids viennent d'articles, de la Wayback CDX et des posts suivis. Un post absent de ces listes n'est pas vu, ce n'est pas la preuve qu'il n'existe pas.
- Les lignes de `x_posts.jsonl` dont le `source_note` dit « Wayback CDX list for DarkMagaCoin » (ou kikisknees) ne sont PAS toutes écrites par ce compte : la CDX liste des URL `/<compte>/status/<id>` dont l'id appartient souvent à un tiers (citation, reprise, capture d'un fil). L'auteur réel est celui renvoyé par fxtwitter. Le lien entre le compte et ces posts n'est pas établi.
- Dates : `created_utc_snowflake` est toujours calculée depuis l'id ; `created_utc_metadata` vient de l'endpoint public (identique dans tous les cas lus).

---

## 1. Thread d'@Aristos_Revenge du 08/10/2024 (id 1843704335823454430)

**Fichiers** : `evidence/web/threadreader_1843704335823454430.html` (HTML brut, 69 755 octets, HTTP 200) et `.txt` (texte extrait) ; copie `..._dothtml.html` (variante `.html`, 66 779 octets). Wayback : la CDX ne liste que `threadreaderapp.com/thread/1843704335823454430.html` aux dates 2024-10-08 20:36:17 et 2025-11-09 13:22:15 (pas téléchargées : l'archive répondait 429 puis hors service par moments ; le texte lu en direct suffit, il porte « Oct 8 • 20 tweets »).
**Les 20 posts sont indisponibles en direct** : syndication = `TweetTombstone` « This Post was deleted by the Post author », fxtwitter = 404 (`{"code":404,"message":"NOT_FOUND"}`) et `api.fxtwitter.com/Aristos_Revenge` = `User not found`. La cause (suppression, changement de pseudo, suspension) n'est pas établie. Le seul texte intégral disponible est donc celui de Thread Reader (fiabilité B : un agrégateur tiers, pas une capture de X).

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

**@Aristos_Revenge 1815128699831796065** (21/07/2024 20:56:20Z par snowflake) : indisponible (même tombstone « deleted by the Post author »). Wayback : CDX `twitter.com/Aristos_Revenge/status/1815128699831796065` et `x.com/...` : réponse vide `[]`; CDX de tout le compte : 0 status archivé (`evidence/x_cdx/Aristos_Revenge.json` = `[]`). Texte connu seulement par le Daily Dot (`evidence/web/dailydot_dark-maga.html`) : épinglé, « If you want a red dark Maga pfp, visit http://dmaga.xyz courtesy of the $dmaga coin. It has a conversion tool » ; fiabilité B (citation d'un journaliste). Le Daily Dot présente aussi le compte comme l'un de ceux qui ont changé de pfp.

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

**Fin de la pfp** : `1815763677447852205` @thesolanapost, 2024-07-23T14:59:30Z : « $LASER and $DMAGA are down 50% and 75% ... after Elon Musk removed his laser eyes PFP » (B). Capture Wayback `twitter.com/elonmusk` du 2024-07-23T14:36:29Z : digest `7264MK2T...` (nouveau) ; l'avatar à cette heure n'a pas été téléchargé. Le retrait est donc ≤ 14:59Z le 23/07, non borné par le bas ici.

**Non trouvé** : la date de la capture d'écran de Bailey (il peut l'avoir prise avant de poster) ; l'heure exacte du clic « enregistrer » de Musk. Les médias qui donnent 20:00 UTC ou « early hours » sont des approximations.

---

## 4. CDX Wayback

*(voir section « État des CDX » en fin de fichier, complétée à la fin de la collecte)*

