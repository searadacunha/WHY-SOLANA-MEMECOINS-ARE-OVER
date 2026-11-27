# Dark-MAGA — passe 3, delta documentaire

**Sept résultats, pas quinze. Aucun nouveau flux n’a été certifié sur la blockchain.** Les meilleurs apports sont une capture 6QFD antérieure à Noah, une empreinte de swap 9Sxm lisible, des sources BARRON plus précoces et une erreur d’appariement vidéo. Les autres résultats sont des contrôles négatifs ou de nouvelles sources à tester, non des accusations.

## Index de départ et règle de nouveauté

Arborescence GitHub lue : `65c681bbb48eecd96e4716f09490f5e2081a640d` ; 24 fichiers de référence vérifiés par leur Git blob SHA, dont tous les segments pass2 et data/x_posts.jsonl. Ils contiennent **6121 IDs archivés uniques**, et l’index étendu contient **8116 IDs de posts archivés/cités/parents** ; 1821 handles vus comme auteurs ou mentions et 1577 chaînes candidates d’adresses/contrats sont indexés. Les déclarations des posts et les lignes d’hypothèses des rapports sont conservées séparément dans l’index local. Ce n’est pas un audit de chaque fichier brut de toute l’arborescence.

Le DELTA contient uniquement 316 posts nouveaux de périmètre sélectionné, zéro ID déjà couvert, et non tous les faux positifs des recherches. Un nouveau post répétant une ancienne affirmation n’est pas automatiquement une nouvelle découverte. P3-02 enrichit un média d’un ID ancien, explicitement absent du DELTA ; les autres résultats distinguent nouvelles sources et nouvelles assertions. Les liens vers les repères anciens servent de contexte, pas de découvertes réannoncées.

Mint Solana imposé : `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Données publiques seulement ; ni identité civile, ni attribution de clé à un handle. Lecture seule GitHub, aucun post/brouillon X, aucune routine ni agent de code lancé.

## Résultats classés par potentiel probatoire

### P3-01 — Une capture 6QFD publiée avant Noah fournit un nouvel instantané de comparaison [P1]

**Sources primaires** :
- [1815370301128974544](https://x.com/VikingXBT/status/1815370301128974544) — @VikingXBT, 2024-07-22T13:56:22+01:00 Lisbonne (2024-07-22T12:56:22.000Z UTC).

**Delta exact** : Nouvelle publication @VikingXBT et nouveau média, absents de l’index initial. Ce n’est pas une redécouverte du rapprochement 6QFD/Jeffro/Noah de N09 : le delta est un affichage antérieur, avec sa propre horloge et son contexte de liquidité.

**Extrait** : « My issue with it is these large holders who bought before it went viral. $1M liquidity for these kind of holdings will kill it. »

**Observation** : Le 22 juillet, Viking publie à 13:56:22 Lisbonne (12:56:22 UTC), soit 7 min 55 s avant le tableau Noah déjà connu. Sa capture Dexscreener affiche la ligne « 6QFDe4…5jqD », 1,53 %, 15.3M et $947.9K ; le panneau de marché affiche $1.0M de liquidité. L’horloge visible est 14:54:58 (UTC+2), soit 13:54:58 Lisbonne / 12:54:58 UTC SI la capture est bien du jour du post ; la date du fichier et le slot ne sont pas démontrés.

**Hypothèse** : Une publication distincte avait déjà rendu visible 6QFD parmi les gros détenteurs avant Noah ; son instantané peut aider à dater la position et à contrôler le récit de financements.

**Arguments favorables** : Interface différente du tableau coloré Noah ; ligne, montants et horloge effectivement lus dans le fichier original téléchargé. L’ordre des publications est vérifié par métadonnées et Snowflakes.

**Meilleure objection / alternative** : Deux publications distinctes ne garantissent pas deux méthodes indépendantes. L’adresse est tronquée, les montants sont arrondis, l’horloge est celle d’une interface et aucun slot n’est donné ; la propriété commune n’est pas démontrée.

**Pièces manquantes** : Slot, supply exact, méthode de calcul Dexscreener, signature du crédit allégué de 60 SOL.

**Test falsifiable** : Sur le mint officiel, rejouer les comptes SPL/ATA de 6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD du 21 au 22 juillet. Sortir les soldes par slot autour du 22 juillet 12:00–13:05 UTC (13:00–14:05 Lisbonne), vérifier les règles d’arrondi de 15.3M/1.53%, puis chercher séparément le crédit System de 60 SOL et son véritable expéditeur. Ne jamais attribuer une contrepartie de service à une personne.

**Preuve documentaire** : A-document : post et pixels disponibles ; interprétation temporelle conditionnelle.

**Vérification financière** : NON VÉRIFIÉ ; aucune nouvelle arête financière certifiée.

**Fichiers effectivement téléchargés** :
- `1815370301128974544_3-1815370118731280385.jpg` — SHA256 `8eace954222fc20badc6c4e3d71bfa31853f3cfd236a96435014292b0a87b01c` ; https://pbs.twimg.com/media/GTF9gTbWMAEBejZ.jpg

### P3-02 — Le média Jeffro donne un événement 9Sxm précis à rechercher, daté du 15 juillet à l’écran [P1]

**Sources primaires** :
- [1815291249102119198](https://x.com/JeffroBTC/status/1815291249102119198) — @JeffroBTC, 2024-07-22T08:42:14+01:00 Lisbonne (2024-07-22T07:42:14.000Z UTC).

**Delta exact** : ID déjà archivé, donc exclu du DELTA. Nouveauté = transcription de détail de son image, absente des déclarations indexées : elle fournit une empreinte de swap exploitable, et non les signatures encore manquantes des 190 SOL.

**Extrait** : « Swapped 1.8M DMAGA* for 17.875 SOL » ; « 15 Jul 2024, 09:59 ».

**Observation** : Sous l’étiquette visible « 9Sxmf2…rHSQS », la dernière ligne indique « Swapped 1.8M DMAGA* for 17.875 SOL » et « 15 Jul 2024, 09:59 ». Le fuseau de cette liste n’est pas affiché : ce n’est PAS une heure UTC établie. Quatre ventes au-dessus affichent 1.18M→9.4624 SOL à 10:03 ; 1.31M→15.48 à 10:01 ; 1.46M→16.914 à 10:00 ; 1.62M→19.576 à 09:59, mais leur propriétaire n’est pas lisible dans le recadrage.

**Hypothèse** : Le trade de 9Sxm peut être retrouvé par sa jambe SOL et sa date affichée, puis relié au lot allégué de 20 M DMAGA sans inventer de signature.

**Arguments favorables** : Lecture directe de l’original 1734×694 et recadrage non destructif. L’étiquette de wallet précède explicitement la dernière ligne.

**Meilleure objection / alternative** : 1.8M est arrondi et DMAGA* n’est pas un mint. Le média ne prouve pas la vente alléguée du 14 juillet à 02:26 ; il peut simplement illustrer des opérations ultérieures. Ce décalage n’invalide donc pas, à lui seul, le récit entier.

**Pièces manquantes** : Fuseau de l’interface, montant token exact, mint, signature, instructions internes et coûts des tokens transférés.

**Test falsifiable** : Rejouer 9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS du 14 au 16 juillet, sans imposer le fuseau de la capture. Chercher un swap du mint officiel ayant environ 1,8 M tokens et une jambe brute proche de 17,875 SOL ; retenir les montants natifs exacts du reçu, frais/rent séparés. Vérifier ensuite, et indépendamment, la provenance des 20 M depuis 7GVC. Ne pas sommer les quatre lignes précédentes sous 9Sxm sans preuve.

**Preuve documentaire** : A-document pour les valeurs affichées, pas pour leur exactitude on-chain.

**Vérification financière** : NON VÉRIFIÉ ; aucun hash de transaction lisible n’a été inventé.

**Fichiers effectivement téléchargés** :
- `1815291249102119198_3-1815288876430426112.jpg` — SHA256 `ee270a37efe721310e43db3bbf1864d6ce94b521ecd05137f12c36fe46093b5a` ; https://pbs.twimg.com/media/GTEznYRagAAWps2.jpg
- `1815291249102119198_3-1815288959033020416.jpg` — SHA256 `58a1990807e006c008cb09acf2a86c7eee312a4ef375d48e21f0ad65acde079e` ; https://pbs.twimg.com/media/GTEzsL_aEAAUgLq.jpg

### P3-03 — Le lien d’équipe BARRON/DMAGA circulait avant sonder, avec une trace Winig antérieure au lancement DMAGA [P1]

**Sources primaires** :
- [1815158757942292949](https://x.com/mocfive/status/1815158757942292949) — @mocfive, 2024-07-21T23:55:46+01:00 Lisbonne (2024-07-21T22:55:46.000Z UTC).
- [1815191565121515817](https://x.com/CristusVictor/status/1815191565121515817) — @CristusVictor, 2024-07-22T02:06:08+01:00 Lisbonne (2024-07-22T01:06:08.000Z UTC).
- [1815355508959682732](https://x.com/BornBullishX/status/1815355508959682732) — @BornBullishX, 2024-07-22T12:57:35+01:00 Lisbonne (2024-07-22T11:57:35.000Z UTC).
- [1815409572686795158](https://x.com/MUDBONE3003/status/1815409572686795158) — @MUDBONE3003, 2024-07-22T16:32:25+01:00 Lisbonne (2024-07-22T15:32:25.000Z UTC).
- [1786883817761820813](https://x.com/ChrisWinig/status/1786883817761820813) — @ChrisWinig, 2024-05-04T23:21:15+01:00 Lisbonne (2024-05-04T22:21:15.000Z UTC).
- [1786151408850362623](https://x.com/Barronsolana/status/1786151408850362623) — @Barronsolana, 2024-05-02T22:50:55+01:00 Lisbonne (2024-05-02T21:50:55.000Z UTC).
- [1786151406958694513](https://x.com/Barronsolana/status/1786151406958694513) — @Barronsolana, 2024-05-02T22:50:55+01:00 Lisbonne (2024-05-02T21:50:55.000Z UTC).

**Delta exact** : N11 ne donnait que l’allégation sonder et le mint candidat BARRON. Nouveaux éléments : @mocfive le 21 juillet, @CristusVictor et @BornBullishX avant sonder ; un post @MUDBONE3003 associe ensuite explicitement le récit au mint HmAgi… ; une réponse ChrisWinig du 4 mai fait déjà la promotion de BARRON.

**Extrait** : « $barron is the same team as $dmaga btw » ; « This is a Community Takeover notice. »

**Observation** : @mocfive écrit « $barron is the same team as $dmaga btw » le 21 juillet à 23:55:46 Lisbonne (22:55:46 UTC), donc après l’avatar mais avant le post sonder du lendemain. @CristusVictor écrit « time traveler on Sol, same team as DMAGA » à 02:06:08 Lisbonne le 22 juillet. @MUDBONE3003 imprime le contrat HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ à côté de « the dev that did $DMAGA did $BARRON ». Le 4 mai, ChrisWinig répond déjà à @Barronsolana : « BARRON is the future! ». Le fil officiel du 2 mai se présente comme une « Community Takeover notice » et mentionne Wifejak et d’autres comptes culturels.

**Hypothèse** : La continuité sociale peut être antérieure à la formulation de sonder et correspondre à une équipe de promotion/illustration ou de reprise communautaire, plutôt qu’au créateur financier des deux mints.

**Arguments favorables** : Plusieurs auteurs publient avant le message sonder précis ; ils ne peuvent pas copier ce message futur. La réponse Winig est contemporaine de mai et le contrat est écrit en toutes lettres dans une source de juillet.

**Meilleure objection / alternative** : Ils peuvent reprendre une même rumeur ou un canal commun ; ce ne sont pas des témoins indépendants d’un contrôle financier. Le message CTO ne contient pas de mint : ne pas supposer qu’il concerne nécessairement HmAgi… sans contrôler l’historique du compte et du token. La promotion de Winig n’est pas un contrôle de clé.

**Pièces manquantes** : Origine de la rumeur, rôle exact de chaque membre, historique de reprise/relancement, créateurs et financeurs propres aux deux mints.

**Test falsifiable** : Obtenir les reçus de création DMAGA et BARRON HmAgi…, dater le mint BARRON par rapport au 2 mai, extraire signataires, fee payers, autorités, retraits et financements initiaux. Chercher des transferts directs hors services et des co-signatures ; une absence de créateur commun ne réfute pas une équipe sociale commune. Ne lier aucun handle à un wallet à partir du seul mot « dev ».

**Preuve documentaire** : A-document pour l’antériorité ; C-hypothèse pour le sens de « même équipe ».

**Vérification financière** : Aucun contrôle commun ni flux intertokens démontré.

**Fichiers effectivement téléchargés** :
- `1786151408850362623_3-1786150063548342272.jpg` — SHA256 `c3aab48f0e5e5576e27aa7da124d07d36b68eed9a772240fc7399bfd560618a5` ; https://pbs.twimg.com/media/GMmuBPVXIAABeiw.jpg
- `1786151408850362623_3-1786150104988012545.jpg` — SHA256 `1e01bb75cce9d62a59527abeae74ec96fd828a56c7eb13180f4b5141fdc99b9c` ; https://pbs.twimg.com/media/GMmuDptWUAE8Hhu.jpg
- `1786151408850362623_3-1786150138043404288.jpg` — SHA256 `3858a6e84bba8a67e19cdebff9d0fada170b24f778442e16a240a78e91989633` ; https://pbs.twimg.com/media/GMmuFk2XkAAaBoi.jpg
- `1786151408850362623_3-1786150354763075584.jpg` — SHA256 `038cbc8621bcd8b5984db4cd9a12d799eb0c35808f3510504f7846751f01a4ce` ; https://pbs.twimg.com/media/GMmuSMMXUAASaBL.jpg

### P3-04 — Une source retrouvée pour 9Prm attache un clip WOLF au récit DMAGA [P1-contrôle]

**Sources primaires** :
- [1825526180616827284](https://x.com/cryptosymbiiote/status/1825526180616827284) — @cryptosymbiiote, 2024-08-19T14:32:12+01:00 Lisbonne (2024-08-19T13:32:12.000Z UTC).
- [1825526177957605756](https://x.com/cryptosymbiiote/status/1825526177957605756) — @cryptosymbiiote, 2024-08-19T14:32:12+01:00 Lisbonne (2024-08-19T13:32:12.000Z UTC).
- [1825526155073700207](https://x.com/cryptosymbiiote/status/1825526155073700207) — @cryptosymbiiote, 2024-08-19T14:32:06+01:00 Lisbonne (2024-08-19T13:32:06.000Z UTC).

**Delta exact** : Le dossier déclarait la provenance sociale 9Prm non retrouvée. Une source nouvelle existe le 19 août, mais son média ne peut pas être utilisé comme preuve visuelle DMAGA/9Prm : cinq frames originales échantillonnées montrent WOLF/SOL.

**Extrait** : « Coin: $DMAGA / Wallet: 9PrmF8… / 3M PnL: +$235,614 » ; le média lu affiche « WOLF/SOL ».

**Observation** : Le post « Second Insider » donne 9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq et DMAGA, achat à $500k MC, vente à $50–70M MC et « 3M PnL +$235,614 ». Les frames à 0, 5, 10, 15 et 19 s du MP4 de 19,666 s montrent WOLF/SOL, LandWolf, Solana/Raydium et un maker tronqué « qn7xMt ». Le message précédent donne précisément WOLF et F1DRDBNW1CX3BPoZPQafidvMeaepg6LS19J4vHqn7xMt.

**Hypothèse** : Erreur d’appariement ou reprise de gabarit/clip du wallet précédent, non preuve de fraude de l’auteur ni relation de fonds entre les deux wallets.

**Arguments favorables** : MP4 téléchargé et haché ; cinq frames enregistrées et vues avec Read. Le fil complet a été reconstruit par auteur/date et relations replied_to.

**Meilleure objection / alternative** : Échantillonnage, pas audit de chaque frame ; l’erreur documentaire ne réfute pas les trades DMAGA vérifiés ailleurs. « 3M PnL » est une statistique de période du wallet, pas nécessairement le profit de ce seul token.

**Pièces manquantes** : Reçus propres à 9Prm, données de calcul PnL du tracker, mint WOLF exact et provenance d’origine du clip.

**Test falsifiable** : Conserver ce post comme déclaration, exclure le clip du paquet de preuves DMAGA. Recalculer uniquement les swaps du mint officiel par 9Prm jusqu’au 19 août, puis séparer PnL DMAGA et PnL tous actifs sur 90 jours. N’attribuer aucun swap WOLF à 9Prm à cause du clip ; F1DR est seulement le wallet déclaré dans le message précédent.

**Preuve documentaire** : A-document pour le désaccord texte/frames ; intention et chaîne non établies.

**Vérification financière** : Aucune nouvelle vente ni attribution confirmée.

**Fichiers effectivement téléchargés** :
- `1825526180616827284_7-1825525900378550272.mp4` — SHA256 `14254f1d509d6b8a27a79fbe7916b9d71d22f9b2a05dc0f4c30d92351ab5c78d` ; https://video.twimg.com/ext_tw_video/1825525900378550272/pu/vid/avc1/1280x720/I4wFD1z4lPvPd1hM.mp4?tag=12

### P3-05 — Un homonyme DMAGA au format EVM et une métrique Hold% sont des faux amis quantitatifs [P2-contrôle]

**Sources primaires** :
- [1815407168700743950](https://x.com/BlizzSolana/status/1815407168700743950) — @BlizzSolana, 2024-07-22T16:22:52+01:00 Lisbonne (2024-07-22T15:22:52.000Z UTC).
- [1815405051302543602](https://x.com/BlizzSolana/status/1815405051302543602) — @BlizzSolana, 2024-07-22T16:14:27+01:00 Lisbonne (2024-07-22T15:14:27.000Z UTC).

**Delta exact** : Nouvelle source et nouvelle lecture de tableau, séparées du mint Solana officiel. Le contrôle porte sur la contamination des recherches et le dénominateur, pas sur un nouveau groupe DMAGA.

**Extrait** : « 22 whales are IN with 70% holds » ; colonnes « Supply / Count / Hold % ».

**Observation** : @BlizzSolana publie le contrat 0x07b74763b630f59eba4f711b4745a4b38dcc15ee et « 22 whales ... 70% holds ». La capture affiche Age 59m, first 45 Hold Supply 46.5%, et ligne Whale : Supply 12.7%, Count 22, Hold 69.9% ; Profit Wallet : Supply 3.1%, Count 7, Hold 71.4%. Les wallets visibles sont au format 0x.

**Hypothèse** : Des résultats de recherche sur le ticker mélangent un actif EVM et DMAGA Solana ; Hold% ne représente pas directement la part de supply totale.

**Arguments favorables** : Contrat écrit dans le post ; format des wallets et intitulés de colonnes effectivement lus.

**Meilleure objection / alternative** : Le réseau EVM précis n’est pas établi par ces pièces. Le tweet peut employer correctement « holds » ; c’est son interprétation comme « 70% de tous les DMAGA Solana » qui serait invalide.

**Pièces manquantes** : Chain ID, contrat vérifié, méthode et dénominateur exact du tableau.

**Test falsifiable** : Identifier le chain ID par les liens originaux et le reçu de déploiement avant tout calcul. Garder ce contrat hors de toutes les jointures sur 7D7BR…pump ; reproduire Supply% et Hold% séparément. Aucune recherche de bénéficiaire humain par le pseudo du compte.

**Preuve documentaire** : A-document pour le contrat publié et le tableau ; chaîne précise non résolue.

**Vérification financière** : Aucune comparaison de positions sur Solana autorisée par cette seule capture.

**Fichiers effectivement téléchargés** :
- `1815407168700743950_3-1815406599332126720.jpg` — SHA256 `fe7c51436bfa220596876c6df0fa8901ba3b61ffe72a4082e2052a79f2410280` ; https://pbs.twimg.com/media/GTGerwQXYAAwSkH.jpg

### P3-06 — PERCY fournit un nouveau témoin de lancement pour le créateur XC78 déjà étudié [P2-contrôle]

**Sources primaires** :
- [1875535213440192682](https://x.com/solmemescope/status/1875535213440192682) — @solmemescope, 2025-01-04T13:30:15+00:00 Lisbonne (2025-01-04T13:30:15.000Z UTC).
- [1875535395351314725](https://x.com/YutiBot/status/1875535395351314725) — @YutiBot, 2025-01-04T13:30:58+00:00 Lisbonne (2025-01-04T13:30:58.000Z UTC).

**Delta exact** : Nouveau mint témoin et nouvelles annonces publiques du 4 janvier, absents de l’index de départ : R4SUGQqwk8r4ZSdXniRV4UDJVspjSE4yfWWeYrLpump. Le caractère de lanceur en série de 9dtGg était déjà acquis ; il n’est pas réannoncé comme découverte.

**Extrait** : « Creator: 9dtGg97QAfxc2UF4LGaxLzYdB4MJpnNMK7Y2iUwGidoy » ; « Percy Verence ($PERCY) ».

**Observation** : @solmemescope et @YutiBot annoncent Percy Verence/PERCY sur Solana à 13:30:15 et 13:30:58 Lisbonne le 4 janvier 2025. Ils donnent comme créateur 9dtGg97QAfxc2UF4LGaxLzYdB4MJpnNMK7Y2iUwGidoy, déjà créateur XC78 dans le dépôt, mais divergent dans les métriques instantanées de holders/top10.

**Hypothèse** : Un contrôle supplémentaire hors de l’événement Kekius permet de distinguer une infrastructure de lancement réutilisée d’un opérateur financier spécifique.

**Arguments favorables** : Deux publications contemporaines donnent exactement le même mint et la même adresse de créateur.

**Meilleure objection / alternative** : Deux bots peuvent partager le même flux ; leur différence de comptage et leur retard n’identifient pas le slot de création. Aucun lien PERCY→DMAGA ni 3oq/Go5 n’est établi.

**Pièces manquantes** : Create-mint, bundle éventuel, financeurs des premiers achats et retours de fonds de ce nouveau mint.

**Test falsifiable** : Résoudre le premier create PERCY, comparer les signataires au créateur allégué puis extraire les 100 premiers acheteurs et leurs instructions de financement. Comparer les flux et co-signatures avec XC78, 3oq et Go5, en retirant Pump.fun, Raydium, Jito et CEX des liens personnels. Un programme commun seul ne confirme rien.

**Preuve documentaire** : B-document : annonces de bots concordantes, pas reçus.

**Vérification financière** : Nouveau témoin proposé, pas nouvelle continuité DMAGA/Kekius démontrée.

### P3-07 — Une mention espagnole de 2d86 précède DMAGA et nomme deux gains à tester [P2-contrôle]

**Sources primaires** :
- [1808330517495836697](https://x.com/juan77758/status/1808330517495836697) — @juan77758, 2024-07-03T03:42:47+01:00 Lisbonne (2024-07-03T02:42:47.000Z UTC).
- [1808330515813929293](https://x.com/juan77758/status/1808330515813929293) — @juan77758, 2024-07-03T03:42:46+01:00 Lisbonne (2024-07-03T02:42:46.000Z UTC).

**Delta exact** : Nouvelles sources du 3 juillet et nouveaux chiffres sociaux PEIPEI/QUBY. Le profil multi-actifs de 2d86 était déjà établi : le delta est un contrôle public antérieur à DMAGA, pas une nouvelle attribution d’identité.

**Extrait** : « ganancia realizada de 105K dolares con ... $PEIPEI ... otra ganancia de 24k ... $QUBY ».

**Observation** : @juan77758 donne l’adresse complète 0x2d86499a410a9ac2139833ba8d6942b8a8700a7b et décrit un win rate de 70% sur 30 jours, $105k de gain réalisé PEIPEI et $24k QUBY ; AKITA/SHI/KIRO sont aussi mentionnés. Les posts précèdent le mint DMAGA de onze jours.

**Hypothèse** : Les fonds et performances de la branche 2d86 peuvent avoir un passé de trading généraliste publiquement commenté, alternative à une spécialisation DMAGA.

**Arguments favorables** : Adresse entière et date pré-événement vérifiées ; chiffres utilisables comme assertions à confronter aux grands livres.

**Meilleure objection / alternative** : Un seul observateur commercial ; contrats et réseaux des tickers absents ; coûts, transferts reçus et fenêtre de calcul inconnus. La simple antériorité d’un gain n’indique ni son propriétaire ni l’origine des fonds ultérieurs.

**Pièces manquantes** : Contrats exacts et chain IDs, toutes les acquisitions/cessions et frais, fenêtre de 30 jours.

**Test falsifiable** : À partir des historiques EVM déjà figés de 2d86, résoudre PEIPEI et QUBY par les vrais contrats des swaps avant le 3 juillet, sans choisir le token populaire par son ticker. Recalculer réalisé/latent/frais et comparer à 105k/24k ; garder les autres actifs et les éventuels dépôts CEX comme explications alternatives, pas comme liens personnels.

**Preuve documentaire** : B-document : publication primaire d’une déclaration, sans reçu financier.

**Vérification financière** : Chiffres non vérifiés, aucune nouvelle sortie deBridge ou Coinbase certifiée.

## Ce qui n’est pas une découverte de cette passe

- Aucune capture montrant réellement le profil de Musk, antérieure à la borne pass2 de 20:25:23 Lisbonne le 21 juillet (19:25:23 UTC), n’a été authentifiée dans les médias examinés. Les nouveaux posts [FlipCrypt 1815105613107433608](https://x.com/FlipCrypt/status/1815105613107433608), 20:24:35 Lisbonne, et [MonetizedLiving 1815105767600771266](https://x.com/MonetizedLiving/status/1815105767600771266), 20:25:12 Lisbonne, ne montrent respectivement qu’un portrait et une image ronde agrandie, sans profil identifiable complet. Ils ne resserrent pas la borne par le même standard de preuve.
- Les nouveaux portraits de FrankButcher81 à 20:21:05 Lisbonne et onthepickle à 20:22:17 Lisbonne ne sont pas non plus des captures du profil ; celui du second représente Trump. Ils servent de contre-exemples, pas de premières publications de l’avatar exact.
- MUDBONE3003 mentionne aussi « a lot of the same early holders from DMAGA » pour KLLRY, mais sans adresse : nouvelle source sociale, pas contrôle de wallets indépendant. La capture montre bien KLLARY/SOL sur Solana/Raydium ; elle ne contient pas le mint lisible.
- Les 190 SOL, les achats 41,2 M, la distribution de 20 M et les crédits 5/60/16 SOL restent à rejouer. Aucune signature nouvelle lisible ne les certifie ici.
- Le clustering exact Noah, ses quatre groupes et l’absence de propriété commune prouvée ne sont pas résolus. Les interfaces et les posts antérieurs ne fournissent pas ses règles.
- Aucun nouveau lien financier discriminant DMAGA/Kekius, ni nouveau destinataire Coinbase/deBridge, ni message privé Musk authentifié. JOE/BILLY/WIF restent non résolus au niveau des contrats des swaps ciblés : aucun rapprochement n’est fait par le seul ticker.

Les missions ci-jointes sont des propositions pour une exécution séparée. Le zip conserve les médias originaux hachés et les cinq frames de vidéo, contrairement à une simple liste de URLs.
