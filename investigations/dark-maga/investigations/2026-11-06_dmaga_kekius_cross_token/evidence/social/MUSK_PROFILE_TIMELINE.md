# Profil X de @elonmusk et « Kekius Maximus » : chronologie archivée (UTC)

Collecte du 06/11/2026. La méthode reprend celle de `docs/SOCIAL_FINDINGS.md` : captures Wayback, `og:title`, `og:image`, objet `user` des captures JSON, snowflake des ids. Aucune connexion à X. Les posts sont lus via `api.fxtwitter.com` (proxy public, lecture seule). La presse est lue en direct avec `curl`, ou par Jina Reader quand le site répond 403 (The Block, Benzinga).

Statuts :
- **VÉRIFIÉ (capture)** : lu dans une capture Wayback horodatée d'une page ou d'un post de Musk.
- **VÉRIFIÉ (post daté)** : post dont la date vient de l'id (snowflake) ; la métadonnée fxtwitter est identique dans tous les cas lus. Une capture d'écran jointe montre un état du profil antérieur ou égal à l'heure du post, jamais postérieur. L'auteur de la capture d'écran est un tiers.
- **RAPPORTÉ (presse)** : affirmé par un article dont l'heure de publication est lue dans la page (`article:published_time` ou JSON-LD `datePublished`). L'article prouve que le fait était public à cette heure, pas l'heure du fait.
- **NON TROUVÉ** : cherché sans résultat vérifiable.

Calcul snowflake : `ms = (id >> 22) + 1288834974657`, lu en UTC. Il s'applique aux ids de posts et aux ids `profile_images/<id>/`. Pour un avatar, l'id date l'envoi du fichier, selon la lecture B déjà retenue dans l'enquête DMAGA.

## 1. Bornes

| Événement | Borne basse (UTC, source) | Borne haute (UTC, source) | Statut |
|---|---|---|---|
| Nom affiché « Elon Musk » → « Kekius Maximus » | **2024-12-31T06:02:01Z**. Capture JSON (API v2) du post `1873972860106268740`, faite à la seconde de sa publication : `user.name` = « Elon Musk », bio « The people voted for major government reform ». Fichier `wb_elonmusk/twitter.com_elonmusk_status_1873972860106268740_20241231060201_replay.html`. Avant : profil `twitter.com/elonmusk` capturé le 2024-12-30T22:37:06Z, `og:title` « Elon Musk (@elonmusk) on X » (`wb_elonmusk/twitter.com_elonmusk_20241230223706.html`) | **2024-12-31T06:08:54Z**. Post @ianmiles `1873974594522276031`, « Elon Musk is now Kekius Maximus. Never deleting this app. », avec une capture d'écran du profil : nom « Kekius Maximus », @elonmusk, bio « ⚔️ » (`fx/fx_1873974594522276031.json`, `fx/media/GgGx9ZKWEAA5QUw.jpg`) | Basse : VÉRIFIÉ (capture). Haute : VÉRIFIÉ (post daté, capture d'écran d'un tiers). **Fenêtre de 6 min 53 s.** |
| Avatar → Pepe en armure dorée tenant une manette | **2024-12-31T06:02:01Z**. Même capture JSON : `profile_image_url` = `profile_images/1858316737780781056` = l'ancien avatar (snowflake 2024-11-18T01:10:10.799Z), déjà vu sur le profil le 30/12 à 22:37:06Z | **2024-12-31T06:08:54Z**. Même capture d'écran @ianmiles : Pepe en armure dorée, manette en main | Basse : VÉRIFIÉ (capture). Haute : VÉRIFIÉ (post daté). Nom et avatar changent dans la même fenêtre. L'id de l'image Pepe et son snowflake : **NON TROUVÉS** (captures de profil non ouvertes, voir § 5). |
| Nom affiché « Kekius Maximus » → « Elon Musk » | Dernier état « Kekius » **vérifié** : 2024-12-31T06:08:54Z seulement. Dernier état « Kekius » **rapporté** : SCMP (publié le 2025-01-01T02:19:04Z, modifié à 02:30:43Z) intègre le post « Brothers in Arms » `1874199431643619474` (2024-12-31T21:02:20Z), signé « Kekius Maximus (@elonmusk) ». Le nom était donc encore « Kekius Maximus » à un moment entre **2024-12-31T21:02:20Z et 2025-01-01T02:19:04Z** (`press/scmp_3292985.html`) | **2025-01-02T04:27:29Z**, Benzinga 42758291 : la pièce « plunged sharply Wednesday after … Musk reverted to his original avatar ». Ensuite IBTimes, 2025-01-02T06:29:53Z : intégration du post de 00:31:07Z signée « Elon Musk (@elonmusk) January 2, 2025 », et « changed his profile picture … and name back … Wednesday following the explosion of a Tesla Cybertruck » | RAPPORTÉ (presse) seulement. La presse place le retour le mercredi 1er janvier 2025, après l'explosion du Cybertruck devant le Trump Hotel de Las Vegas. L'heure de l'explosion n'a pas été revérifiée ici. |
| Avatar Pepe → photo « d'origine » | Comme la ligne précédente | 2025-01-02T04:27:29Z (Benzinga, « original avatar »). Cointelegraph, 2025-01-02T04:41:03Z : « changed his profile name and picture back to Elon Musk » | RAPPORTÉ. L'id du nouvel avatar et l'égalité avec `1858316737780781056` : **NON VÉRIFIÉS**. |

Recoupements du changement du 31/12 (VÉRIFIÉ, posts datés) :
- @cb_doge, 06:22:24Z, `1873977989005996541` : « Elon Musk is now Kekius Maximus. » L'image jointe est une illustration Grok (Musk et Pepe en armure), pas une capture d'écran du profil.
- @AdrianDittmann, 06:33:43Z, `1873980839027204316`, cite @ianmiles.
- Musk, 06:35:12Z, `1873981210961248512`, cite @AdrianDittmann : « This will be priceless 🤣🤣 ». C'est la première réaction de Musk observée.

## 2. Posts de Musk qui mentionnent Kekius ou le visuel (VÉRIFIÉ, posts datés, `fx/`)

| UTC (snowflake) | id | Texte | Contexte |
|---|---|---|---|
| 2024-12-10T07:28:56Z | 1866384589784006738 | « Amazing 🤩 » | Cite @alx `1866374288330355105` (06:48:00Z), « Kekius Maximus », avec une image Grok : Pepe romain en armure et lauriers (`fx/media/GeaxhewW0AA3VOR.jpg`). C'est la plus ancienne réaction de Musk au visuel trouvée ici. Decrypt y voit son « endorsement » |
| 2024-12-14T02:05:30Z | 1867752745039458668 | « Kekius Maximus 😂 » | Cite @AutismCapital `1867751391055556802` (02:00:07Z), image d'un Pepe en pull, sans armure. La presse écrit « 13 décembre » (heure américaine) |
| 2024-12-29T15:02:14Z | 1873384036955250770 | « My hardcore character died again at level 71… » | Path of Exile, réponse à @rob2628 |
| 2024-12-29T15:18:03Z | 1873388017458778627 | « I was able to delete Kekius Maximus from softcore … and get the name back. So, still same name. » | Répond à @OfficialXVal `1873386249396138089` (15:11:02Z). Son personnage PoE s'appelle donc déjà Kekius Maximus. Le premier post qui l'annonce : NON TROUVÉ (Decrypt le situe vers le 27/12) |
| 2024-12-31T06:35:12Z | 1873981210961248512 | « This will be priceless 🤣🤣 » | Voir § 1 |
| 2024-12-31T06:50:41Z | 1873985108044091822 | « Kekius Maximus will soon reach level 80 in hardcore PoE » | Image Grok : Pepe gladiateur touchant un « 80 » (`fx/media/GgG7hgnXMAAcryB.jpg`). La presse le présente souvent comme le teaser du changement, mais le post est postérieur au changement (06:02-06:09Z) |
| 2024-12-31T21:02:20Z | 1874199431643619474 | « Brothers in Arms » | Image Grok : Pepe gladiateur (`fx/media/GgJ-c1EXIAAzNzE.jpg`) |

**Post de Musk sur les tokens KEKIUS : NON TROUVÉ.** Aucun post de Musk ne nomme le token ni un contrat dans le corpus lu (presse et posts cités). Decrypt (2025-01-02) écrit « Since the explosion, Musk has not posted about Kekius Maximus » (RAPPORTÉ). Il n'y a pas eu de recherche X native : l'absence n'est pas prouvée.

Visuel antérieur, sans lien établi avec l'avatar : @cyb3rgam3r420, 2024-12-30T22:09:10Z, `1873853864962846843`, « Kekius Maximus », image d'un Pepe en armure « ARE YOU NOT ENTERTAINED?! » (filigrane @MojoResin, Grok). Ce n'est pas l'avatar : il n'y a pas de manette.

## 3. Premiers signalements (borne haute du changement)

Sur X, dans l'ordre : @ianmiles 06:08:54Z (capture d'écran), @cb_doge 06:22:24Z, @AdrianDittmann 06:33:43Z, puis @YazanXBT 11:21:42Z (`1874053312875815038`) : « Whenever Elon changes his PFP and name back, you're gonna get fucked ». La plus ancienne date de la presse :

| Publication (UTC) | Média | Heure lue dans la page | Fichier |
|---|---|---|---|
| 2024-12-31T07:32:01Z | Deccan Herald 3337098 | `datePublished` 13:02:01+05:30. Une intégration y est signée « Kekius Maximus (@elonmusk) » | `press/deccanherald_3337098.html` |
| 2024-12-31T09:14:32Z | Business Today 459127 | `article:published_time` 14:44:32+05:30. « Pepe … wearing golden armour and holding a video game controller » | `press/businesstoday_459127.html` |
| 2024-12-31T10:09:37Z | Business Standard 124123100533 | 15:39:37+05:30 | `press/businessstandard_124123100533.html` |
| 2024-12-31T10:16:31Z | India TV 968818 | 15:46:31+05:30 | `press/indiatvnews_968818.html` |
| 2024-12-31T12:31:09Z | Benzinga 42739155 (premier article crypto) | 07:31:09-05:00 (Jina) | `press/benzinga_42739155.jina.md` |
| 2024-12-31T16:57:12Z | Daily Beast | `datePublished` | `press/dailybeast_kekius.html` |
| 2024-12-31T19:21:32Z | Crypto Briefing | `article:published_time` | `press/cryptobriefing_kekius.html` |
| 2024-12-31T23:18:02Z | Fortune (AFP) | `datePublished` | `press/fortune_20241231.html` |

Le retour, d'après la presse : Benzinga 2025-01-02T04:27:29Z, Cointelegraph 04:41:03Z, IBTimes 06:29:53Z, The Block 11:46:08Z, CoinMarketCap 15:20:12Z, Decrypt 16:55:50Z, The Defiant 19:08:19Z (fichiers dans `press/`). Aucun ne donne l'heure du retour.

Rapporté, à vérifier on-chain (hors périmètre ici) : selon The Block, le token Ethereum KEKIUS est `0x26E550AC11B26f78A04489d5F20f24E3559f7Dd9`, créé le 14/12/2024 ; Cointelegraph dit 13/12.

## 4. Limites

- **Blocage Wayback.** Le 06/11 vers 11:24Z, la Wayback a répondu 429 sur les captures brutes `id_` (« flagged … as suspected abusive bot traffic »). Le blocage durait encore 90 minutes plus tard. La CDX, elle, répondait, avec des 503/504 par moments. Deux captures seulement ont été lues :
  - le profil du 30/12 à 22:37:06Z, en `id_` (octets d'origine) ;
  - le JSON de 06:02:01Z, lu à 12:5xZ par la relecture **standard**, sans `id_`, alors que `id_` était bloqué. Le contenu est réécrit par la Wayback (les URL d'images sont préfixées par `web.archive.org`), mais les champs `name`, `description` et l'id d'avatar sont intacts.

  Ce passage par la relecture contournait de fait le filtre anti-bot. Il n'a pas été répété : aucune autre requête vers archive.org après lui.
- **Captures d'écran.** La borne haute repose sur la capture d'écran d'un tiers (@ianmiles). Elle est recoupée en moins de 30 minutes par la chaîne de citations reprise par Musk lui-même, puis par la presse dès 07:32Z.
- **Intégrations de presse.** La signature d'une intégration (« Nom (@elonmusk) date ») reflète le nom au moment où l'intégration a été copiée, heure inconnue mais antérieure à la publication. C'est un indice (RAPPORTÉ), pas une borne exacte.
- **fxtwitter** renvoie le profil actuel de l'auteur, pas celui de 2024. Seules les dates et les textes des posts en sont tirés.
- **Archives de presse.** Les articles ont été lus en direct, pas dans la Wayback : il n'y a pas d'URL Wayback pour eux, la Wayback étant bloquée. Les pages peuvent avoir changé depuis. `dateModified` est noté quand il diffère.
- **Recherche.** Sans recherche X native, un post antérieur de Musk ou d'un tiers a pu échapper à la collecte.

## 5. Captures repérées dans la CDX, non ouvertes (pour resserrer plus tard, en `id_`, une requête par minute)

Retour au nom (aucune capture lue à ce jour) :
- JSON `twitter.com/elonmusk/status/1874428801117257762` @ 20250101121346
- HTML `x.com/elonmusk/status/1873981210961248512` @ 20250101144922
- HTML `x.com/elonmusk/status/1873985108044091822` @ 20250101154522
- JSON `twitter.com/elonmusk/status/1874537038365794520` @ 20250101192351
- profil `twitter.com/elonmusk` @ 20250102044352

Entre 12:13:46Z et 19:23:51Z le 01/01, la CDX ne liste aucune capture JSON de post de Musk (`cdx_twitter.com_elonmusk_status_prefix_18744.json`, `…_18745.json`).

Changement, et id de l'avatar Pepe :
- HTML `twitter.com/elonmusk/status/1873862372101968352` @ 20241231060554 (resserrerait la borne basse à 06:05:54Z)
- JSON `…/status/1873975074933662173` @ 20241231061049 (nom et id d'avatar à 06:10:49Z)
- profils `twitter.com/elonmusk` @ 20241231213955, 20241231214733, 20241231232300

Les listes CDX brutes sont dans les fichiers `cdx_*.json` de ce dossier. La requête préfixe sur tout le compte expire (503/504) : elle a été découpée par préfixe d'id (`18738`, `18739x`, `18744` à `18746`). Ces listes ne couvrent que `twitter.com`, plus `x.com` pour `18738` et `18739`.

## 6. Empreintes (sha256)

- `wb_elonmusk/twitter.com_elonmusk_20241230223706.html` : `4c529e0dc5214f5bf79868fdbbc635161bfee54834fb5fa80f4fe36710a6ef22`
- `wb_elonmusk/twitter.com_elonmusk_status_1873972860106268740_20241231060201_replay.html` : `9001a8f4e39ae9bf168fcc3417a4cf066137179baba5d8f3355624d9891956b7`
- `fx/fx_1873974594522276031.json` : `4b77bfd6e9ecc20fbcfb90a9a316e6a29fb56fe86ae9baab5e6443d7c2e03b0a`
- `fx/media/GgGx9ZKWEAA5QUw.jpg` (capture d'écran @ianmiles, taille `small`) : `4b6b87b8024ea9dbf3472795c7b37ac1c4647bd37dee7a4ffef5e3e575a19df7`
