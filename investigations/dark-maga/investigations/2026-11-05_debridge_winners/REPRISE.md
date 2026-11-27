# Reprise : révision deBridge et jonctions financières ($DMAGA)

**Date :** 5 novembre 2026.  
**État :** cohérence des archives contrôlée hors ligne ; validations blockchain complémentaires encore ouvertes.  
**Dépôt :** [searadacunha/Dark-MAGA](https://github.com/searadacunha/Dark-MAGA).  
**PR de travail :** [#13](https://github.com/searadacunha/Dark-MAGA/pull/13), `feat/debridge-crosschain-convergence` → `main`.

## Résultats conservés et périmètre

| Mesure | Valeur exacte ou compte |
|---|---:|
| Ordres décodés dans I14 | 76 |
| USDC source, frais proportionnels inclus | 1 018 687,178289 |
| Ordres émis par les membres exacts des 33 | 68 |
| USDC source de ces 68 ordres | 974 077,946152 |
| Rapprochements Ethereum rapportés dans I21/I22 | 41 |
| Rapprochements avec hash de transaction complet | 31 |
| Rapprochements sans hash imprimé | 10 |
| Arrivées non vérifiées | 35 |

Les archives G et I contenaient déjà la convergence de quatre ordres vers `0xb947bf7f`, les ordres BSC de `8YSi5yNR` et la jonction `7Gw3gL8m`. Ce dossier est une synthèse contrôlée de ces résultats. Aucune nouvelle collecte n'est revendiquée.

Le maker décodé détermine le périmètre. `EGtyQEgM` est dans une population étendue et ne fait pas partie des 33 exacts. Les huit ordres Base vers `0xb29826d8` restent distincts des huit ordres Ethereum. Le rapport ne transforme ni une destination commune en propriété commune, ni un montant demandé en paiement reçu, ni un transfert sortant en bénéfice attribué.

## Fichiers de travail

| Fichier | Usage |
|---|---|
| [RAPPORT_RESULTATS_NOUVEAUX.md](RAPPORT_RESULTATS_NOUVEAUX.md) | Synthèse révisée ; nom de fichier conservé pour la stabilité des liens. |
| [TABLE_DEBRIDGE_ORDERS.csv](TABLE_DEBRIDGE_ORDERS.csv) | 76 lignes normalisées, montants entiers et décimaux, états d'exécution distincts. |
| [TABLE_DEBRIDGE_ORDERS.md](TABLE_DEBRIDGE_ORDERS.md) | Sommes, dénominateurs, schéma des colonnes et commandes de reproduction. |
| [TABLE_NEW_LINKS.md](TABLE_NEW_LINKS.md) | Signatures et hashes effectivement présents dans les sources ; lacunes nommées. |
| [GRAPH_CONNECTIONS.md](GRAPH_CONNECTIONS.md) | Graphes avec chaînes et périmètres séparés. |
| [validate.py](validate.py) et [test_validate.py](test_validate.py) | Vérification hors ligne et tests de régression. |
| [evidence/source_manifest.json](evidence/source_manifest.json) | Provenance des quatre copies inchangées, commit source, SHA256 et blobs Git. |

Les copies sources sont fixées au commit `933ebe8afc0558a2406b189a272311df060aef7a` de la branche de recherche. Les fichiers bruts Solana et les réponses Blockscout originales restent dans l'archive externe décrite par les audits, absente de ce dossier.

## Vérification avant toute publication

Depuis la racine du dépôt :

```bash
python3 investigations/2026-11-05_debridge_winners/validate.py
python3 -m unittest discover -s investigations/2026-11-05_debridge_winners -p 'test_*.py'
```

Ce contrôle est autonome, sans réseau, sans clé et sans dépendance externe. Il vérifie la table CSV et ses sources archivées ; les textes et graphes doivent également être relus. Il n'est pas remplacé par `scripts/chk_90_selfcheck.py`, qui ne couvre pas à lui seul ce dossier et ses références EVM.

Pour l'intégration Git, suivre `AGENTS.md` : état propre ou travail isolé, lecture du HEAD distant courant, conservation des modifications d'autres sessions, garde `scripts/check_publication.py --target main`, diff relu, push normal ou PR. Le README racine et les études gelées ne sont pas modifiés par ce dossier. Le statut de la PR et ses contrôles doivent être relus sur le commit effectivement publié.

## Prochaines vérifications utiles, par priorité

1. **Reconstituer la preuve de chaque arrivée.** Retrouver les dix hashes absents de I22 dans les réponses Blockscout archivées ; extraire les reçus et événements, puis relier les identifiants d'ordre source et destination. Les 31 hashes complets doivent également être vérifiés sur leurs reçus, au-delà de leur présence dans un log.
2. **Compléter les chaînes non vérifiées.** Vérifier les 35 arrivées restantes, en conservant séparément Ethereum, Base, BSC, Polygon et Arbitrum. En cas de refus API ou d'historique incomplet, conserver l'état non vérifié.
3. **Tester la continuité de l'aval H3QsBr.** Rejouer les transferts vers `8YSi5yNR` et ses soldes jusqu'aux ordres BSC de mars 2025. Les montants de juillet 2024 ne suffisent pas à attribuer ces ordres à DMAGA.
4. **Qualifier le rôle de 7Gw3 et des destinataires EVM.** Compléter les historiques, mesurer le nombre et la nature des contreparties, vérifier les explications de paiement ou de service avant toute hypothèse de contrôle commun.

Pour l'hypothèse distincte du financement de créateurs de memecoins par des sorties deBridge, il faut identifier les ordres et leurs makers économiques. Les contrats de paiement et la liquidité des takers ne sont pas, à eux seuls, une attribution de financement à l'entreprise deBridge.
