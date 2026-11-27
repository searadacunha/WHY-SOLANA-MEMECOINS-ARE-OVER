# deBridge : livraison sur BSC des ordres de 8YSi5yNR (Dark MAGA, 13/11/2026)

Suite du dossier `../2026-11-05_debridge_winners/` (point 3 de `REPRISE.md`) : vérifier que les deux ordres deBridge du 20/03/2025 de `8YSi5yNR…` vers BSC `0xfb2ec4e5…` ont bien été payés.

## Résultat en bref
- **Livraison vérifiée (A)** : les deux ordres ont été livrés sur BSC en 8 et 16 secondes ; les reçus contiennent l'identifiant de chaque ordre (`FINDINGS.md` C1).
- **Non relu (D)** : la continuité des soldes Solana de `8YSi5yNR` entre juillet 2024 et mars 2025 (C2).
- **Aucune nouvelle entité** : le preneur est un solveur DLN (service partagé).

## Fichiers
| Fichier | Contenu |
|---|---|
| `FINDINGS.md` | Constats, preuves, niveaux |
| `data/ordres_dln.csv` | Les deux ordres : montants, destinataire, transactions de création et de livraison, contrôle des reçus |
| `evidence/` | Réponses brutes de l'API DLN et des reçus BSC, avec `INDEX.csv` (URL, sha256, date) |
| `scripts/dm_debridge_ol07.py` | Collecte et contrôle (bibliothèque standard ; `onchain.py` archive chaque réponse) |

## Reproduire
`scripts/dm_debridge_ol07.py` a tourné depuis l'espace de travail d'origine (dossier `scripts/`, Python 3.12) ; sans clé : API publique `stats-api.dln.trade` et RPC BSC public. Chaque transaction se vérifie aussi sur un explorateur public.
