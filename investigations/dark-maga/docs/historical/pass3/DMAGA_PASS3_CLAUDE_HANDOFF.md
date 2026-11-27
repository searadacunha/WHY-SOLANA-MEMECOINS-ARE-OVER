# Claude Code — missions réfutables, uniquement après reprise séparée

Aucune de ces missions n’a été exécutée on-chain dans la passe 3. Aucun commit/PR n’a été créé. Travailler dans une copie locale, ne pas écraser les résultats validés ; ne pas attribuer un wallet à une personne à partir d’un handle, d’un programme ou d’un service commun.

## Protocole commun obligatoire

1. Lire d’abord les rapports financiers et les corpus existants. Conserver les signatures et reçus complets avec source, paramètres, date de collecte, slot, blockTime UTC et SHA256 du fichier ; produire une vue Lisbonne pour la restitution humaine. La transcription visuelle du CSV est une assertion, pas un reçu.
2. Mint DMAGA exclusif : `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Pour Solana, partir des datasets complets du dépôt, compléter au besoin par `getSignaturesForAddress(address,{limit:1000,before:cursor})` jusqu’au début de fenêtre. Cette seule requête sur le propriétaire est insuffisante pour des transferts touchant seulement ses comptes SPL : résoudre également les comptes historiques/fermés via les propriétaires des pre/postTokenBalances et les historiques du mint. `getTokenAccountsByOwner` actuel n’est pas un inventaire des comptes fermés.
3. Pour chaque signature candidate, obtenir `getTransaction(signature,{encoding:"jsonParsed",maxSupportedTransactionVersion:0})` ; contrôler réussite, slot, blockTime, signataires, fee payer, comptes chargés v0, instructions externes et internes. Résoudre les propriétaires SPL/ATA et le mint exact, puis extraire quantités natives et décimales. Conserver `amount_raw` entier ; ne pas calculer avec un montant arrondi du tracker.
4. Pour SOL/WSOL, distinguer swap brut, transferts System, fees, priority fees/tips, rent et fermeture des comptes. Ne pas assimiler une variation de solde SOL nette à la jambe brute du swap. Si un décodage manque, classer « indéterminé », pas « absence de transfert ».
5. Pour un solde historique, rejouer depuis un état antérieur vérifié ou toutes les entrées/sorties, mint/burn compris ; `minContextSlot` ne transforme pas un RPC courant en lecture historique. Vérifier conservation des tokens, supply et changements d’autorité.
6. Format de sortie minimal : `mission_id, signature, chain_id, slot_or_block, block_time_utc, owner, account, mint, delta_raw, decimals, source, destination, instruction_path, evidence_sha256, status`. Statuts `CONFIRME / REFUTE / INDETERMINE`, avec critère de décision ; bilan réalisé/latent et frais séparés. Chaque arête doit désigner une véritable instruction, pas une proximité sociale.

## M1 — P1 : identifier l’événement 9Sxm, puis tester sa provenance

**Nouvelle entrée** : image2 de [Jeffro1815291249102119198](https://x.com/JeffroBTC/status/1815291249102119198), fichier `media/1815291249102119198_3-1815288959033020416.jpg` ; ligne sous `9Sxmf2…rHSQS` : **1.8M DMAGA* →17.875 SOL**, **15 Jul 2024,09:59**, fuseau inconnu.

- Extraire tous les swaps du propriétaire `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS` sur le mint officiel du 14 au 16 juillet UTC inclus. Cette fenêtre couvre l’incertitude de fuseau de l’affichage du 15 juillet ; ne pas imposer09:59UTC.
- Trier les candidats par jambe WSOL brute proche de17.875, puis quantité token compatible avec l’affichage1.8M. Montrer la règle d’arrondi/troncature retenue et les valeurs exactes de tous les candidats, sans choisir le plus commode. L’image ne donne pas le mint ; vérifier celui du reçu.
- Pour le candidat identifié, remonter la provenance des tokens jusqu’au crédit allégué de20M depuis `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j` ; dater ce transfert séparément. Rejouer aussi le financement190SOL à partir de son véritable reçu, sans inférer un financier de Jupiter Perpetuals.
- **Confirme** : reçu correspondant aux deux jambes, wallet/mint corrects, puis éventuel transfert20M prouvé séparément. **Réfute l’appariement** : seul candidat sur un autre mint/wallet ou aucun candidat malgré historique complet et fuseaux couverts. **Indéterminé** si couverture incomplète. Ne pas attribuer les quatre ventes au-dessus à9Sxm : leur étiquette n’est pas lisible.

## M2 — P1 : transformer le snapshot Viking en contrainte temporelle 6QFD

**Nouvelle entrée** : [1815370301128974544](https://x.com/VikingXBT/status/1815370301128974544), publié le22juillet13:56:22Lisbonne/12:56:22UTC,7min55avant Noah. L’image montre `6QFDe4…5jqD`,15.3M,1.53%,$947.9K ; horloge14:54:58UTC+2 sans date indépendante.

- Résoudre l’adresse canonique connue `6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD` à partir des sources anciennes, pas en complétant les pixels seuls.
- Rejouer les soldes mint officiel par slot du21au22juillet, puis isoler12:00–13:05UTC le22(13:00–14:05Lisbonne). Produire tous les intervalles compatibles avec15.3M et1.53%, selon arrondi et troncature, sans prétendre connaître le slot de capture.
- Chercher séparément le crédit60SOL allégué et son expéditeur réel ; rapprocher la chronologie du lot token, sans propriété commune automatique. Contrôler aussi les montants5/16SOL des autres wallets seulement avec reçus, pas en les réannonçant comme apport de cette passe.
- **Confirme la compatibilité** si le solde affiché existe dans un intervalle documenté ; **réfute une heure précise** si aucun solde compatible et historique complet ; cela ne prouve ni l’auteur de la capture ni la méthode de Noah. La date manquante de capture doit rester une réserve.

## M3 — P1 : tester « même équipe » BARRON/DMAGA sans confondre CTO et déploiement

**Sources nouvelles** : [mocfive1815158757942292949](https://x.com/mocfive/status/1815158757942292949), [CristusVictor1815191565121515817](https://x.com/CristusVictor/status/1815191565121515817), [MUDBONE1815409572686795158](https://x.com/MUDBONE3003/status/1815409572686795158), [Winig1786883817761820813](https://x.com/ChrisWinig/status/1786883817761820813), [CTO1786151408850362623](https://x.com/Barronsolana/status/1786151408850362623).

- Mint candidat BARRON : `HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ`. Retrouver sa création, ses premiers financeurs, signataires, autorités, migration/pools et retraits ; comparer au mint DMAGA exact.
- Dater BARRON par rapport au CTO du2mai. Le post CTO ne nomme pas le contrat : vérifier archive du compte/annonces avant d’appliquer le contrat de juillet à mai. Promotion Winig ≠ création.
- Pour chaque financeur commun, distinguer CEX, agrégateur, programme, relayer, opérateur de bundle et EOA ; extraire le transfert exact ou la co-signature hors services, puis rechercher des contre-exemples sur des tokens non liés.
- **Confirme une relation financière spécifique** seulement avec transfert/contrôle documenté discriminant. **Réfute le seul modèle “même deployer”** si les signataires diffèrent : cela ne réfute pas une équipe artistique/marketing commune. Résultat social et résultat financier séparés.

## M4 — P1-contrôle : mettre en quarantaine le clip 9Prm/WOLF puis recalculer

**Source retrouvée** : [1825526180616827284](https://x.com/cryptosymbiiote/status/1825526180616827284) ; message précédent [1825526177957605756](https://x.com/cryptosymbiiote/status/1825526177957605756). Le clip original et ses5frames montrent WOLF/SOL et maker `qn7xMt`, pas une preuve DMAGA/9Prm.

- Ne pas réutiliser la vidéo comme preuve financière DMAGA. Si nécessaire inspecter toutes les frames, en conservant la distinction entre échantillonnage fait ici et contrôle complet futur.
- Rejouer séparément le mint officiel pour `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` jusqu’au19août, puis son portefeuille tous actifs sur90jours. Calculer coûts et cessions, fonds entrants, réalisé/latent et frais.
- Tester l’allégation `3M PnL +$235614` comme métrique de portefeuille, pas automatiquement profit du seul DMAGA. Les marketcaps500k/50–70M dépendent du prix/supply au moment du trade ; les recalculer plutôt que les traiter comme sommes investies/retirées.
- `F1DRDBNW1CX3BPoZPQafidvMeaepg6LS19J4vHqn7xMt` est déjà connu, seulement déclaré dans le message WOLF précédent. Résoudre son mint WOLF exact avant comparaison ; aucun lien9Prm/F1DR par le voisinage du fil.
- **Confirme l’erreur d’usage du clip** si aucune image exploitable ne documente9Prm/DMAGA ; cela ne réfute pas les transactions réelles. **Réfute les chiffres sociaux** seulement avec comptabilité complète compatible avec leur fenêtre.

## M5 — P2 : homonyme EVM et dénominateurs du tableau Blizz

**Sources** : [1815407168700743950](https://x.com/BlizzSolana/status/1815407168700743950) et1815405051302543602. Contrat `0x07b74763b630f59eba4f711b4745a4b38dcc15ee`.

- Résoudre chainID, reçu de déploiement, decimals et supply à partir des liens publics originaux ; ne pas dire “Ethereum” sur le seul format0x.
- Garder cet actif hors des tables mintSolana. Reproduire les trois colonnes séparément : WhaleSupply12.7%,Count22,Hold69.9%. Demander la définition historique deHold% avant de l’interpréter.
- **Réfute la lecture “22whales détiennent70% du DMAGA Solana”** : pièce d’un autre contrat et autre dénominateur. Ne pas prétendre pour autant que le tweet de l’auteur commet lui-même cette confusion.

## M6 — P2 : PERCY comme témoin négatif du créateur XC78

**Sources** : [1875535213440192682](https://x.com/solmemescope/status/1875535213440192682), [1875535395351314725](https://x.com/YutiBot/status/1875535395351314725),4janvier13:30:15/13:30:58Lisbonne=UTC.

- Nouveau mint à vérifier : `R4SUGQqwk8r4ZSdXniRV4UDJVspjSE4yfWWeYrLpump`. Créateur allégué connu : `9dtGg97QAfxc2UF4LGaxLzYdB4MJpnNMK7Y2iUwGidoy`.
- Extraire le vrai create et les100premiers acheteurs, financeurs et co-signatures ; comparer aux mints XC78/Kekius déjà identifiés dans le dépôt et aux wallets3oq/Go5. Ne pas reprendre le timestamp du bot comme timestamp de création.
- Construire un contrôle de lancements du même programme et retirer les services communs. **Confirme** seulement les arêtes exactes réellement observées ; **réfute l’attribution de créateur du bot** si les instructions le contredisent ; **aucune continuité DMAGA** par programme/visuel seul.

## M7 — P2 : vérifier les chiffres pré-DMAGA de2d86

**Sources** : [1808330517495836697](https://x.com/juan77758/status/1808330517495836697), parent1808330515813929293,3juillet03:42:47Lisbonne/02:42:47UTC.

- Wallet connu : `0x2d86499a410a9ac2139833ba8d6942b8a8700a7b`. Résoudre PEIPEI/QUBY avec les véritables chainIDs/contrats de ses swaps pré3juillet ; ne pas sélectionner un contrat par le ticker populaire.
- À partir des reçus EVM et logsTransfer/Swap, reconstruire acquisitions, cessions, transferts internes et lots de coûts, gas compris ; conserver les remboursements et swaps multi-hop. Sortir au moins FIFO et coût moyen si la méthode du tracker est inconnue.
- Comparer aux chiffres sociaux `$105k réaliséPEIPEI /$24kQUBY /70%winrate30jours`, en donnant la définition et le nombre de positions du winrate. **Confirme** uniquement avec fenêtre et méthode compatibles ; **indéterminé** si les contrats ou lots antérieurs manquent. Un gain antérieur ne prouve ni identité ni source finale des fonds DMAGA/deBridge.

## M8 — P2-document : graphe et horloges, sans nouvelle arête financière

- Exploiter SOURCE_GRAPH comme graphe documentaire : distinguer `quoted/replied_to/reposted` natifs de `derived_*` annotés. Aucun edge social n’est un transfert.
- Pour les avatars, les timestamps des nouveaux posts sont des publications. Les portraits isolés FlipCrypt/MonetizedLiving ne remplacent pas une capture de profil ; aucun resserrement prouvé de la borne pass2 de20:25:23Lisbonne le21juillet. L’upload Snowflake média ne date pas le changement de profil.
- Remonter les parents indisponibles seulement s’ils deviennent accessibles par une source publique autorisée ; ne pas inventer leur texte depuis les réponses. Les rumeurs BARRON avant sonder ne sont pas nécessairement indépendantes.
- Livrer une table d’arêtes avec niveau de dépendance et toutes les bornes temporelles conditionnelles ; **réfute une origine unique alléguée** seulement par un document antérieur authentifié du même contenu, pas par un récit rétrospectif.
