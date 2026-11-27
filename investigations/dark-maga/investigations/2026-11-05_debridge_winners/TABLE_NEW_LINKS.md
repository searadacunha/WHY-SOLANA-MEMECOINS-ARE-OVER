# Liens financiers : références vérifiées dans les archives ($DMAGA)

**Révision :** 5 novembre 2026. Les montants ci-dessous sont rattachés aux fichiers cités. Les opérations n'ont pas été relues sur un nœud blockchain pendant cette révision. Un rapprochement financier ou une contrepartie partagée n'est pas une preuve de propriété commune.

## 1. Quatre ordres vers le même destinataire Ethereum

Destinataire : `0xb947bf7f409e998b28f8e218802fc9575c3c8c57`, **Ethereum, chaîne 1**. Makers appartenant à la [liste exacte des 33](evidence/group_split.json).

| Réf. | Heure source UTC | Maker Solana | USDC source, frais proportionnels inclus | Signature source |
|---|---|---|---:|---|
| S1 | 2024-07-22T00:54:36Z | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 16,536704 | `3SrZnJG88Ja3GPKzW424pPMTPisjpNyCPKfSuDwyiF4DEbjk6K7Nq2nQA7cad19XUkZjHiTpLjrogQR58svwSmiY` |
| S2 | 2024-07-22T00:57:18Z | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 60 443,988481 | `7pHaeuMNtNPyQzVxT24yK8thFDn5cnHkK7X5L2KAvMoy1GqD1SdHoBqtH9jBU86gbmvpBHeJ5b8mzq3PUL4csWX` |
| S3 | 2024-07-22T01:00:34Z | `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 156 089,016395 | `45PnZWjKkx7c1yeEx2rr1HFCggW5J5Pr1BFz9bkb8ScKf77SQiMEL4DocKcExRsQxFmmADWvyu1r55adNUdaPuC2` |
| S4 | 2024-07-22T01:04:12Z | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | 47 023,609816 | `4kW2yTLkXKzbb6i23StE6wswpcTr8oGNyVKa2ZBK2vTSi5nN9DXiX5YQShcjAP2LyEwNpEAFbQpRPCWEBvXCz8o8` |

Le journal [I21](evidence/i21_evm_fill.txt) contient ces rapprochements, avec les montants reçus imprimés en unités entières :

| Réf. | USDC reçus selon I21 | Délai depuis l'ordre | Hash de transaction Ethereum |
|---|---:|---:|---|
| S1 | 9,992001 | 35 s | `0xdb07ade91b6ed02470a9283a346f7062ba45dbb65ea5030763dd1150b78d8b3d` |
| S2 | 60 382,887121 | 53 s | `0x28becd5f70870d586c3b588df1ebf26e56c1a95950fd75f2a0ab1d26772aa914` |
| S3 | 155 951,578125 | 49 s | `0xf05ec404683b7714c6a95a9abd71f468420607d53f1b40a6a17cb18d934cc21a` |
| S4 | 46 975,647847 | 47 s | `0x79a0ec8b526983483bb1d4d6d8a441746d3cc3e589859ee94c25266c2235dcc6` |

Le contrat payeur observé est `0x555ce236c0220695b68341bc48c68d52210cc35b`. Son utilisation ne permet pas d'identifier le donneur d'ordre économique. Total source : **263 573,151396 USDC** ; total destination imprimé : **263 320,105094 USDC**. Les correspondances reposent sur le destinataire, le montant et le temps ; la jointure par identifiant d'ordre n'est pas incluse dans ces logs.

## 2. Relation historique rapportée entre les deux adresses EVM

Source : [journal I22](evidence/i22_evm_rest.txt). Les hashes ne sont pas imprimés dans ce fichier. Ces lignes servent de repères pour retrouver les reçus, sans leur substituer un montant ou une adresse en guise de hash.

| Date UTC | Source | Destination | Montant rapporté | Hash dans l'archive |
|---|---|---|---:|---|
| 2022-09-11 18:50:18 | `0xb29826d809aa04d2ead6f2310d8965a45b87fa67` | `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` | 0,002085847778473724 ETH | Non imprimé dans I22 ; relu : `0xc7bd63d35a1bdf09bfe5ccb1ad859184a4903117813760a388334003957fad89` |
| 2024-07-25 08:22:23 | `0xb29826d809aa04d2ead6f2310d8965a45b87fa67` | `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` | 50 003,330779 USDC | Non imprimé dans I22 ; relu : `0xac4a12bd7eac6283bec6af0f43b3191c2964ee7c0f77dcefd8c29238566e1211` |
| 2024-07-26 05:56:11 | `0x555ce236c0220695b68341bc48c68d52210cc35b` | `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` | 120 957,888072 USDC | Non imprimé dans I22 ; relu : `0x47e8da75f698f8c40419230c2274136c57666b92a91bef55c481e63a91758e14`. Hors des 76 ordres du corpus : c'est l'ordre DLN `0xc65ba1fa1b9d14301b5b0acaf159a5fd955a18899e4256a7604fd0af1f27a225` de `GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y` |

Les trois hashes « relu » et l'ordre de la dernière ligne viennent de [`../2026-11-05_evm-recipient-deeptrace/FINDINGS.md`](../2026-11-05_evm-recipient-deeptrace/FINDINGS.md) (§1 et §3), pas de l'archive I22.

Les huit ordres Ethereum vers `0xb29826d8` ne doivent pas être confondus avec les huit ordres Base désignant la même représentation d'adresse. La répartition détaillée figure dans [la table des ordres](TABLE_DEBRIDGE_ORDERS.md).

## 3. Jonction 7Gw3 et périmètres des contreparties

`7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` apparaît comme contrepartie dans les archives I. Les libellés P1 et « série » sont les populations de recherche de l'audit, pas une attribution de propriété au créateur.

| Date et heure UTC | Source | Destination | Montant | Signature disponible dans l'audit I |
|---|---|---|---:|---|
| 2024-02-08 21:36:54 | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` | 0,5 SOL | Non imprimée dans I28 |
| 2024-05-15 22:13:33 | `DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT` (P1) | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | 0,7 SOL | `3qmzf3oWcwQjKuR2HS51YbACxMfeiRzp9NGRTLabPP2Eqb7vD4237oqFyv3z7CWGpj8UB829WzScxPdGjx8FmC3h` |
| 2024-07-14 02:18:29 | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` | 4 SOL | Non imprimée dans I28 |
| 2024-08-03 04:40:03 | `EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy` (salve du 23/07, hors 33 exacts) | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | 78,909373285 SOL | `MpbxCDghSqrbz5tu15EdHmYYQmGn1JjMSrNeCPPJj8irX5JCFC2xhpwSQ6iiThknUNBYWg11JdpBghv8ACj89jB` |
| 2024-08-03 04:40:32 | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | `EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy` | 1 SOL | `Zz3sQjpj3LbxybCThNEgEPDHYrv2J6WKbkuaXibHUNNTD3GWUueKszSBEFgzknApvzoSEeV7A9pMKyjW1dQ7qkc` |
| 2024-08-03 04:41:44 | `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | 400 SOL | `2BfutoeRjJDZQmNMjcYEcpecQGn1BmkWUFyFBoZPRPCVarDM4H3ubXm2Qkj47rCyKGL9MRP22gsS6USJ2FEQJFNJ` |
| 2025-07-20 17:10:18 | `6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM` (série) | `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx` | 1 000 USDC | `5Zu1ofkpmCS2Yjwdfq5vEGJeDXHURJ32UqgL1zuR3VPxWWJFn5r1TqzjTdwitP6oNMZZXFsfRjmy6biV5UmdeqE9` |

Sources : [I28](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_I/i28_7gw.txt), [I71](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_I/i71.txt), [rapport I, section 5](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_I/REFUTATION.md). I28 indique des historiques tronqués. Le financement initial est le premier trouvé dans ce relevé, pas une garantie d'absence de financement antérieur.

Le retour de 1 SOL suit le premier versement de 29 s ; celui de 400 SOL arrive 72 s plus tard. Ces temps sont mesurables. Le rôle de trésorier, une dépense de gaz ou une origine particulière des 400 SOL restent des interprétations à vérifier.

## 4. 8YSi5yNR : ordres BSC, paiements non vérifiés

Maker : `8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7`. Destinataire demandé : `0xfb2ec4e51680198f4d0351d67702d4eebdfa625f`, BSC (56).

| Heure source UTC | USDC source | BNB demandés | Signature source |
|---|---:|---:|---|
| 2025-03-20T20:38:25Z | 971,613389 | 1.535748176327131837 | `3bi9qiVpVZdsjgxrTebvHdPbxenKbeiS3s2fjXZRyn49nNCTposWdMp5UkZCxXRinggda1roEfqmbLdVXcvFfXvT` |
| 2025-03-20T20:39:05Z | 8 941,213964 | 14.130734168518820689 | `3XipCLfThtvdYBYFDxqEeh6Rf3qF562wFSeBWzoDKgqjnZFrpdUte9fXb8vRFHCxK9FcUNg2AemFGd5YnCLCvmyC` |

Source : [I14](evidence/i14_orders.csv). Total demandé : **15,666482344845952526 BNB**. Le CSV ne renseigne aucun montant reçu ni aucun hash BSC pour ces deux ordres.

Le transfert antérieur agrégé de **2 840 SOL depuis H3QsBr** est rapporté dans [l'audit G](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_G/FLOW_BOUNDARIES.md), du 24 au 31 juillet 2024. Sa série complète de signatures et la continuité des soldes jusqu'en mars 2025 doivent être rejouées avant d'attribuer les ordres BSC à ces fonds précis.

## 5. Jonctions indirectes autour de GXZvXsD6

Les archives décrivent deux suites de transferts. Chaque étape est distincte ; le montant d'une étape n'est pas automatiquement le produit de la précédente.

| Date UTC | Source | Destination | Actif et montant | Signature |
|---|---|---|---:|---|
| 2024-07-15 18:39:06 | `ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH` | `HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6` | 1 500 000 DMAGA | `4HEH3WcanD16CFvbym5NwzxojkgmfpshSXMa3MEsmamaTYc4M9b8hwdsegGvtUBXQhhY5QC5tmbMZJsP7L4R9C1c` |
| 2024-07-25 14:11:03 | `HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6` | `42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv` | 95 SOL | `2gh2nvDNTab6im9PJqL6HCebM6MtHm74KKvQZL9hqxwfYguDMaLQxeZbVvgK9WMxKY9KTY5odxSiQte6tKaUDG4M` |
| 2024-07-21 23:00:23 | `GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC` | `HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP` | 1 000 000 DMAGA | `2bHLM1r9t7YAih6rp2QQ8V7Kk4sXYFxGMqfSByj6aHr7KP8wawojaDNDRTLxbVa4rqt9HQCHpS1dbzK3aKERT4uZ` |
| 2024-09-30 03:13:01 | `HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP` | `8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx` | 54,8 SOL | `2Jkz5aWG2a87AMCUnzcQ1hFfiAtz3BxLzaShtCEHR25wa17gywQvSev9NWhLmwb4KpFVkFSngnZHxne5Mbe6pUE5` |
| 2024-10-01 14:54:50 | `HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP` | `8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx` | 54 SOL | `3H3DVGf5AXq1DvESdJDHDLxZDQTJR6TiU9gUJBBb3xsmpX5sY8XjHff3TSCcyrwz1oiAaXNs2V2RChhhvTBxwdDR` |

Sources : [références G](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_G/g61_refs.md), [chronologie G48](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_G/g48.txt), [audit I, section 6](https://github.com/searadacunha/Dark-MAGA/blob/933ebe8afc0558a2406b189a272311df060aef7a/audits/2026-11-03/work_I/REFUTATION.md).

Les comptes de destination ont plusieurs expéditeurs et sont aussi utilisés dans l'aval de GXZvXsD6. Le dossier ne démontre ni un transfert direct de la série à GXZvXsD6 ni un contrôle commun. En particulier, G48 montre du trading intermédiaire en septembre avant les versements de 54,8 et 54 SOL : les présenter comme la sortie du million de DMAGA reçu en juillet serait injustifié.
