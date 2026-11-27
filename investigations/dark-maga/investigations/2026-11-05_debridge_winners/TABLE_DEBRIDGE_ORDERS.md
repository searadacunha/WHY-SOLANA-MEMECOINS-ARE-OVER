# Table contrôlée des ordres deBridge / DLN ($DMAGA)

**Date de révision :** 5 novembre 2026.  
**Périmètre :** synthèse des 76 ordres déjà décodés dans l'audit I ; les historiques couvrent le 7 mai 2024 au 9 juin 2025. Il ne s'agit pas d'une nouvelle collecte.

Les montants de cette page sont des **USDC nominaux engagés côté Solana**, montant de l'ordre plus frais proportionnels. Les frais fixes en SOL sont conservés séparément. Un montant source, un montant demandé à destination et un paiement observé sont trois mesures distinctes. Ces sommes ne sont pas une mesure du bénéfice DMAGA.

**Données :** [table normalisée](TABLE_DEBRIDGE_ORDERS.csv), [décodage source inchangé](evidence/i14_orders.csv), [journaux de rapprochement I21](evidence/i21_evm_fill.txt) et [I22](evidence/i22_evm_rest.txt), [population exacte des 33](evidence/group_split.json), [provenance et empreintes](evidence/source_manifest.json).

## 1. Périmètres réconciliés

Le périmètre est déterminé par le **maker décodé dans l'ordre**, et non par le nom du fichier de cache. Quatre ordres de membres des 33 étaient présents dans les caches d'autres adresses.

| Périmètre | Ordres | USDC source, frais proportionnels inclus | Ordres avant le mint | USDC avant le mint |
|---|---:|---:|---:|---:|
| Groupe exact des 33 | 68 | 974 077,95 | 15 | 1 610,18 |
| Hors 33 : P1 | 3 | 3 021,99 | 3 | 3 021,99 |
| Hors 33 : aval de H3QsBr | 2 | 9 912,83 | 0 | 0,00 |
| Hors 33 : autres wallets post-Musk | 3 | 31 674,41 | 0 | 0,00 |
| **Total** | **76** | **1 018 687,18** | **18** | **4 632,17** |

Le total exact est **1 018 687,178289 USDC** ; celui du groupe des 33 est **974 077,946152 USDC**. Les totaux sont calculés avant arrondi. La somme de lignes arrondies séparément peut donc différer d'un centime. La borne du mint est le **14 juillet 2024 à 02:05:25 UTC**.

## 2. Makers appartenant au groupe exact des 33

| Maker Solana | Ordres | USDC source | Première → dernière date UTC | Chaînes demandées |
|---|---:|---:|---|---|
| `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 29 | 527 600,40 | 2024-07-21 → 2025-06-09 | Ethereum |
| `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | 18 | 223 079,75 | 2024-07-16 → 2024-11-26 | Base, Ethereum |
| `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 2 | 157 849,92 | 2024-07-22 → 2024-10-11 | Base, Ethereum |
| `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 2 | 60 460,53 | 2024-07-22 → 2024-07-22 | Ethereum |
| `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 2 | 3 234,17 | 2024-06-17 → 2024-08-21 | Ethereum |
| `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 8 | 1 010,20 | 2024-05-07 → 2024-05-07 | Base |
| `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 1 | 634,18 | 2024-07-16 → 2024-07-16 | Ethereum |
| `C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK` | 6 | 208,81 | 2024-05-26 → 2024-06-03 | Base, Polygon |
| **Total** | **68** | **974 077,95** | | |

Huit membres des 33 apparaissent comme makers dans ce corpus. La population de 33 est une composante de transferts ; elle ne constitue pas une attribution à un propriétaire unique.

## 3. Ce que les archives permettent de vérifier à destination

| Chaîne | Ordres | Rapprochements rapportés dans les logs | Dont hash de transaction complet | USDC source associés aux rapprochements | Part des ordres de la chaîne |
|---|---:|---:|---:|---:|---:|
| Ethereum (1) | 44 | 41 | 31 | 942 534,32 | 93,18 % |
| Base (8453) | 27 | 0 | 0 | 0,00 | 0,00 % |
| BSC (56) | 2 | 0 | 0 | 0,00 | 0,00 % |
| Polygon (137) | 2 | 0 | 0 | 0,00 | 0,00 % |
| Arbitrum (42161) | 1 | 0 | 0 | 0,00 | 0,00 % |
| **Toutes chaînes** | **76** | **41** | **31** | **942 534,32** | **53,95 %** |

Les 41 rapprochements représentent **92,52 % du montant source total** et **93,18 % des 44 ordres Ethereum**. Ce sont deux dénominateurs différents. Les **35 autres exécutions restent non vérifiées** dans les archives citées.

Les 31 lignes de I21 contiennent le destinataire, le montant reçu en unités entières, un délai et un hash de transaction. Les 10 lignes de I22 indiquent un rapprochement, un contrat payeur et un délai, mais n'impriment ni le hash ni un champ séparé de montant reçu. Ces champs restent donc vides dans le CSV. `0xe7351fd770a37282b91d153ee690b63579d6dd7f` est une **adresse de contrat DlnDestination**, pas un hash de transaction et pas l'identité du donneur d'ordre économique ([contrats officiels](https://github.com/debridge-finance/dln-contracts)).

Les scripts historiques rapprochent des paiements par destinataire, montant et proximité temporelle. Les copies conservées ici ne fournissent pas de jointure complète `orderId` → événement de réalisation. Le contrôle local reproduit leur contenu ; il ne remplace pas la relecture des reçus et événements bruts sur chaque chaîne.

## 4. Destinations communes, séparées par chaîne

| Destinataire demandé | Chaîne | Makers Solana | Ordres | USDC source | Portée du rapprochement |
|---|---|---|---:|---:|---|
| `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` | Ethereum | Gcyg2jeL, HGBiExZR, Ei5yGz8d | 4 | 263 573,15 | 4 paiements avec hashes dans I21 ; **263 320,105094 USDC reçus** selon ce journal |
| `0xb29826d809aa04d2ead6f2310d8965a45b87fa67` | Ethereum | Ei5yGz8d | 8 | 151 360,77 | 8 rapprochements rapportés dans I22, hashes absents |
| `0xb29826d809aa04d2ead6f2310d8965a45b87fa67` | Base | Ei5yGz8d, HGBiExZR | 8 | 21 217,50 | Exécutions non vérifiées |
| `0x2d86499a410a9ac2139833ba8d6942b8a8700a7b` | Ethereum | C73Yv9iH | 27 | 496 371,59 | 27 paiements avec hashes dans I21 |
| `0x86f99097c563e84dd5190f3e85f6a2988f1c47a5` | Ethereum | C73Yv9iH | 2 | 31 228,81 | 2 rapprochements rapportés dans I22, hashes absents |

La salve des quatre ordres vers `0xb947bf7f` va de **00:54:36 à 01:04:12 UTC le 22 juillet 2024**, soit **9 minutes 36 secondes**. Les 16 ordres vers `0xb29826d8` totalisent **172 578,262490 USDC source**, répartis entre Ethereum et Base. En ajoutant la salve, on obtient **436 151,413886 USDC source** sur deux adresses et deux chaînes ; ce chiffre n'est ni un total reçu sur Ethereum ni une preuve de contrôle commun des makers Solana.

Les 27 ordres de `C73Yv9iH` vers `0x2d86499a` s'étalent du 21 juillet 2024 au 9 juin 2025. Dans les 24 premières heures suivant le premier ordre, 12 totalisent **296 074,50 USDC source**. Le nom `afk.eth` et les compteurs d'activité mentionnés dans l'audit I décrivent son relevé historique ; ils ne sont pas une identification d'une personne.

## 5. Contrat du CSV et reproduction

| Colonnes | Signification |
|---|---|
| `order_index` | Numéro de ligne dans le décodage source ; **ce n'est pas un identifiant on-chain**. |
| `source_wallet`, `source_nonce`, `source_signature` | Maker et nonce décodés, signature de la transaction Solana. Aucun `orderId` cryptographique n'est reconstruit ici. |
| `source_amount_raw`, `source_proportional_fee_raw`, `source_total_raw`, `source_total_usdc` | Unités entières USDC, puis somme exprimée avec 6 décimales ; le total n'est pas un montant reçu à destination. |
| `source_fixed_fee_lamports` | Frais fixes en SOL, exclus du total USDC. |
| `before_mint` | Date antérieure au mint ; information indépendante du statut d'exécution. |
| `destination_chain_id`, `recipient`, `destination_token` | Identité de la destination ; la chaîne est toujours conservée dans la clé de rapprochement. |
| `destination_amount_requested_raw`, `destination_amount_requested` | Montant demandé (`take_raw`), même si l'exécution n'a pas été vérifiée. |
| `destination_amount_observed_raw`, `destination_amount_observed` | Montant effectivement imprimé dans I21 ; vide pour I22 et les ordres non vérifiés. |
| `destination_match_status` | `archive_match_with_tx_hash` (31), `archive_match_without_tx_hash` (10), ou `unverified` (35). |
| `destination_tx`, `destination_payment_contract` | Hash de transaction de 32 octets ou champ vide ; adresse du contrat payeur dans un champ distinct. |
| `source_evidence`, `destination_evidence` | Fichier et ligne justifiant chaque ligne normalisée. |

Depuis la racine du dépôt, Python 3 standard suffit :

```bash
python3 investigations/2026-11-05_debridge_winners/validate.py
python3 -m unittest discover -s investigations/2026-11-05_debridge_winners -p 'test_*.py'
```

Pour régénérer uniquement la table dérivée à partir des quatre copies sources inchangées :

```bash
python3 investigations/2026-11-05_debridge_winners/validate.py --write-csv
```

Les tests couvrent les erreurs de périmètre, le comptage par cache au lieu du maker, les adresses prises pour des hashes, les faux montants reçus, le mélange Ethereum/Base et les modifications des sources. Ils ne certifient ni l'exhaustivité de la collecte, ni une propriété commune, ni l'origine DMAGA de tous les fonds.
