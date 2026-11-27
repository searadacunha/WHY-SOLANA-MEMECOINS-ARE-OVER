# Constats : livraison sur BSC des ordres deBridge de 8YSi5yNR (13/11/2026)

Échelle du dépôt : **A** vérifié directement, **B** fortement corroboré, **C** indice ou hypothèse, **D** non vérifié ou contredit. Une adresse n'est pas une personne ; rien ici n'accuse quiconque.

Piste d'origine : `investigations/2026-11-05_debridge_winners/REPRISE.md` (point 3) et `RAPPORT_RESULTATS_NOUVEAUX.md` §3 : deux ordres du 20/03/2025 de `8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7` vers BSC `0xfb2ec4e51680198f4d0351d67702d4eebdfa625f`, « paiement BSC non vérifié » (l'API DLN renvoyait alors une erreur Cloudflare 1015).

## C1 | A | Les deux ordres ont été livrés sur BSC à `0xfb2ec4e51680198f4d0351d67702d4eebdfa625f`

| Ordre DLN | Créé (UTC, transaction Solana) | Donné (Solana) | Reçu (BSC) | Livré (UTC) | Transaction BSC | Bloc | Statut | Identifiant d'ordre dans les journaux |
|---|---|---|---|---|---|---|---|---|
| `0x96fb4189b1ce2c28a336b164130ae340c666c279030e457d6d68ef3ef255c7a1` | 2025-03-20 20:38:25 (`3bi9qiVpVZdsjgxrTebvHdPbxenKbeiS3s2fjXZRyn49nNCTposWdMp5UkZCxXRinggda1roEfqmbLdVXcvFfXvT`) | 971.224744 USDC | 1.535748176327132 BNB | 2025-03-20 20:38:33 | `0xc93ffe311db5fbaa0a2d5a275a98d195ebdefa1499cca1d3449113078c416b9e` | 47640476 | 1 | True |
| `0x1ffd2fbfa57de871ebd4932ecedc2cc67448cf59261f091f8a0ec49b117c4309` | 2025-03-20 20:39:05 (`3XipCLfThtvdYBYFDxqEeh6Rf3qF562wFSeBWzoDKgqjnZFrpdUte9fXb8vRFHCxK9FcUNg2AemFGd5YnCLCvmyC`) | 8937.637479 USDC | 14.13073416851882 BNB | 2025-03-20 20:39:21 | `0xf3a3bc2217054c6d9665ad035cdb277208d34fdf6b21dd84976b4969e3961c22` | 47640492 | 1 | True |

- Preuves : `data/ordres_dln.csv` ; réponses brutes de l'API DLN et des reçus BSC dans `evidence/` (index `evidence/INDEX.csv`, sha256 et date de lecture).
- Méthode : `scripts/dm_debridge_ol07.py` : ordres par créateur et détail de chaque ordre (`stats-api.dln.trade`), puis `eth_getTransactionReceipt` sur `bsc-rpc.publicnode.com` : statut 1, identifiant de l'ordre présent dans les journaux, destinataire de l'ordre égal à `0xfb2ec4e51680198f4d0351d67702d4eebdfa625f`. État DLN : `ClaimedUnlock` (livré puis débloqué côté source).
- Limites : le preneur `0x663dc15d3c1ac63ff12e45ab68fea3f0a883c251` est un solveur DLN, service partagé : il ne relie personne. Ce constat confirme un paiement déjà attribué par le dossier d'origine ; il n'ajoute aucune entité.

- **Portée du contrôle** : le script exige maintenant le reçu BSC réussi, le hash et le bloc correspondants, l'adresse destinataire exacte, la paire BNB/chaîne 56 et un journal émis par le contrat `DlnDestination` contenant l'identifiant de l'ordre. Les reçus et l'état `ClaimedUnlock` corroborent le fulfilment. Ils ne mesurent pas, à eux seuls, la variation du solde BNB du bénéficiaire : une trace interne ou une différence d'état est encore nécessaire pour cette vérification distincte.

## C2 | D | Continuité des soldes de 8YSi5yNR entre juillet 2024 et mars 2025

Non relue : les 2 840 SOL reçus de `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc` (adresse citée par `README.md` et `data/exit_summary.json` du dépôt) du 24 au 31/07/2024 ont-ils financé ces ordres huit mois plus tard ? Reste ouvert.

## Écart relevé

Le dossier d'origine cite 9 912,83 USDC donnés ; les deux ordres totalisent 9 908,86 USDC (écart de 3,97 USDC, probablement les frais de la préconversion SOL vers USDC, non vérifié). Les 15,666 BNB demandés correspondent à 15,666482 BNB reçus.
