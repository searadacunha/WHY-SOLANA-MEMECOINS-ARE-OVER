# Synthèse contrôlée des flux deBridge et des jonctions financières ($DMAGA)

**Révision :** 5 novembre 2026.  
**Token :** `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump` (Solana).  
**Dossier :** [tables, graphes et reprise](./REPRISE.md).

Ce dossier rassemble des résultats déjà présents dans les audits G et I. La révision vérifie leur cohérence, explicite les périmètres et rend la table de 76 ordres reproductible hors ligne. Elle ne présente pas ces observations comme trois nouvelles découvertes ni comme une nouvelle collecte blockchain.

## 1. Trois makers Solana, quatre ordres, un destinataire Ethereum

Le **22 juillet 2024, de 00:54:36 à 01:04:12 UTC**, trois membres de la composante exacte de 33 wallets — `Gcyg2jeL`, `HGBiExZR` et `Ei5yGz8d` — ont émis quatre ordres deBridge désignant le même destinataire Ethereum :

`0xb947bf7f409e998b28f8e218802fc9575c3c8c57`

La fenêtre source dure **9 minutes 36 secondes**. Les quatre ordres engagent **263 573,151396 USDC côté Solana**, frais proportionnels inclus. Le journal I21 leur associe quatre paiements totalisant **263 320,105094 USDC reçus** sur Ethereum, 35 à 53 secondes après les ordres. Les montants source et destination ne sont donc pas interchangeables. Les quatre signatures Solana et hashes Ethereum complets figurent dans [la table des liens](TABLE_NEW_LINKS.md).

**Constat :** les trois makers ont désigné le même bénéficiaire on-chain. Les paiements associés sont documentés dans l'archive par destinataire, montant exact et délai. Ce rapprochement n'identifie pas le titulaire du destinataire et ne suffit pas à attribuer les trois makers à un même opérateur. Une relation de service, un paiement ou un bénéficiaire partagé restent possibles.

Sources : [ordres décodés](evidence/i14_orders.csv), [rapprochements I21](evidence/i21_evm_fill.txt). Le raccord complet des identifiants d'ordre aux événements d'exécution reste à reconstituer à partir des reçus bruts.

## 2. Deux adresses EVM liées historiquement, avec Ethereum et Base séparés

Les mêmes historiques contiennent **16 ordres** désignant :

`0xb29826d809aa04d2ead6f2310d8965a45b87fa67`

Ils se décomposent en :

| Chaîne demandée | Makers | Ordres | USDC source, frais proportionnels inclus | Exécution dans les archives |
|---|---|---:|---:|---|
| Ethereum | `Ei5yGz8d` | 8 | 151 360,766904 | Rapprochement rapporté dans I22 ; hashes non imprimés |
| Base | `Ei5yGz8d`, `HGBiExZR` | 8 | 21 217,495586 | Non vérifiée |
| **Total** | | **16** | **172 578,262490** | |

Le [journal I22](evidence/i22_evm_rest.txt) décrit également un transfert d'ETH de `0xb29826d8` vers `0xb947bf7f` dès le **11 septembre 2022**, puis un transfert de **50 003,330779 USDC le 25 juillet 2024**. Les hashes de ces deux opérations ne sont pas imprimés dans ce journal ; il faut retrouver les reçus archivés avant d'en faire une preuve transactionnelle autonome.

Ces observations établissent une relation financière historique rapportée entre deux adresses. Elles renforcent une piste de relation opérationnelle ; elles ne démontrent ni une personne commune derrière les adresses ni le contrôle des wallets Solana.

Le cumul **436 151,413886 USDC source** additionne les quatre ordres vers `0xb947bf7f` et les seize vers `0xb29826d8`. Il couvre **deux chaînes**, inclut huit arrivées non vérifiées sur Base et ne représente pas un « volume contrôlé » ni un montant reçu sur Ethereum.

Le versement additionnel de **120 957,888072 USDC** signalé dans I22 le 26 juillet 2024 n'est relié à aucun des 76 ordres du corpus. Sa chaîne et son donneur d'ordre d'origine restent inconnus ; il est exclu des totaux.

## 3. Dans l'aval de H3QsBr, deux ordres vers BSC à vérifier

L'[audit G](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_G/FLOW_BOUNDARIES.md) rapporte **2 840 SOL** transférés du 24 au 31 juillet 2024 de :

`H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc`

vers :

`8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7`

Le décodage I14 contient ensuite deux ordres émis par `8YSi5yNR` le **20 mars 2025 à 20:38:25 et 20:39:05 UTC**, désignant l'adresse BSC `0xfb2ec4e51680198f4d0351d67702d4eebdfa625f`.

**Montant source : 9 912,827353 USDC. Montant demandé à destination : 15,666482344845952526 BNB.** Aucun paiement BSC n'est vérifié dans les archives fournies.

La suite d'adresses est une piste exploitable. Les huit mois séparant les transferts de SOL des ordres de bridge, ainsi que l'activité intermédiaire du wallet, empêchent d'affirmer ici que ces ordres déplacent précisément les bénéfices DMAGA de H3QsBr. Les 2 840 SOL ne sont pas présentés comme une fraction comptablement attribuée à son profit. Cette piste figurait déjà dans l'audit G.

## 4. La jonction 7Gw3 concerne un périmètre étendu, distinct des 33

L'audit I décrit cette séquence le **3 août 2024** :

| Heure UTC | Transfert rapporté | Montant |
|---|---|---:|
| 04:40:03 | `EGtyQEgM` → `7Gw3gL8m` | 78,909373285 SOL |
| 04:40:32 | `7Gw3gL8m` → `EGtyQEgM` | 1 SOL |
| 04:41:44 | `9cfRU5RK` → `7Gw3gL8m` | 400 SOL |

Les intervalles sont **29 secondes**, puis **72 secondes** ; la séquence complète dure **101 secondes**. Le rôle de « gaz » du retour de 1 SOL, ou l'origine « bénéfices DMAGA » des 400 SOL, ne découle pas du seul transfert.

**`EGtyQEgM` n'appartient pas à la liste exacte des 33** conservée dans [group_split.json](evidence/group_split.json). Il figure dans la salve du 23 juillet étudiée dans le périmètre étendu. Cette séquence ne doit donc pas être décrite comme une preuve directe « groupe des 33 → créateur → gagnant n° 11 ».

Les autres versements rapportés vers `7Gw3gL8m`, depuis `DfYyxDNE` en mai 2024 et `6ty9DM4s` en juillet 2025, étendent sa cartographie de contreparties. Ils ne constituent pas une action simultanée. `9cfRU5RK` est classé n° 11 dans le classement historique cité par l'audit ; ce classement n'identifie pas son propriétaire.

Sources et signatures complètes : [table des liens](TABLE_NEW_LINKS.md), [audit I, section 5](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_I/REFUTATION.md), [lecture des historiques](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_I/i71.txt). Le rôle de trésorerie, de paiement ou d'intermédiation de `7Gw3gL8m` reste à établir sur un historique plus complet.

## 5. Résultat vérifiable de cette révision

Les **76 ordres** totalisent **1 018 687,178289 USDC source** ; les **68 ordres** émis par les membres exacts des 33 totalisent **974 077,946152 USDC**. Les archives rapportent **41 rapprochements Ethereum**, dont **31 avec un hash de transaction complet** et **10 sans hash imprimé**. Les **35 autres arrivées** demeurent non vérifiées.

Le [validateur hors ligne](validate.py) et ses tests recoupent la table normalisée avec quatre fichiers sources inchangés, dont les empreintes sont fixées dans le [manifeste](evidence/source_manifest.json). Ils vérifient les unités, les périmètres, les chaînes, la distinction entre montants demandés et observés, et la présence réelle des références dans les logs. Ils ne simulent pas une nouvelle validation sur les blockchains.

Ce dossier porte sur des **ordres de clients utilisant deBridge**. Un paiement effectué par un contrat DLN ne démontre pas que l'entreprise deBridge finance ou contrôle ces clients. Le rôle du maker et celui du taker fournissant la liquidité à destination sont distincts dans le [protocole officiel](https://github.com/debridge-finance/dln-contracts).
