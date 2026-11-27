# ASTRA — équipe de lancement, promoteurs et bénéficiaires de $DMAGA (addendum du 2024-07-14, toutes heures UTC)

Cet addendum suit `2026-11-18_launch_network_public_attribution/` (PR #40) **sans la remplacer**.
- Base : dépôt en lecture seule, HEAD `643934a`.
- Collecte : 18/11/2026.
- Échelle de preuve :
  - **A** : confirmé ;
  - **B** : fortement corroboré ;
  - **C** : indice ;
  - **D** : non vérifié ou réfuté.
- Origine du niveau :
  - **RO** : rapport d'origine ou dépôt ;
  - **VI** : vérification indépendante.

> Aucune identité civile n'est attribuée. Aucune corrélation n'est présentée comme une preuve de propriété ou d'intention. « Attribution non établie » signifie qu'aucune preuve admise n'existe.

## Ce qui est nouveau

1. **Cluster Coinbase/9W9b lié au wallet créateur (B, VI).**
   - Fenêtre : 01:32:23–01:40:50, avant le mint.
   - 11 retraits Coinbase 2 et 3 (0,5 / 1,0 / 1,05 SOL) vers 11 wallets frais, dont le **créateur**. Tous enverront plus tard des SOL au même collecteur rare `9W9b3z…`.
   - Taux de base : 607 retraits ; **5/5** retraits de 1,05 SOL ; 4/7 de 0,5 SOL.
   - 6 de ces wallets tentent d'acheter DMAGA entre 48 s et 6 min 18 s après le create. 8 achètent avant le premier post public.
   - Deux d'entre eux (`7FGoCB…`, `5QhJJc…`) sont membres du groupe 33.
2. **Échecs de G41v décodés (A, VI).** `TooMuchSolRequired` à +29 s et +45 s. Limites = 0,5 et 0,4 SOL × 1,01², ce qui correspond à une saisie manuelle dans l'UI. Ce n'est pas un bot sniper : médiane de 2 s sur 54 tokens comparables.
3. **Premier visuel tiers = @Murray_Gothbard (ex-@ChristienPhoto) à 02:31:29 (A, VI).** L'image porte « $DMAGA ». Ce post précède @adamjia7 (02:33:53) et n'était pas repéré par la passe 4.
4. **Rejeu complet de la phase pump.fun (A, VI)** : 436 tx, 181 échecs, 123 achats réussis jusqu'à 02:16:31. Il concorde avec la table des 1 000 premiers acheteurs du dépôt (17 acheteurs / 11,916 SOL dans les 60 s).
5. **Corrections** :
   - la pfp DMC et l'image du token ne sont **pas identiques au pixel** : même image ré-encodée, pHash 0 ;
   - le `Last-Modified` 01:49:10 est un artefact CDN : l'heure à retenir est **01:51:10** (snowflake).

## Fichiers

| Fichier | Rôle |
|---|---|
| `FINAL_REPORT.md` | réponses aux 8 questions + bilan |
| `TEAM_ATTRIBUTION.md` | rôles par compte, cluster créateur, corrections |
| `EARLIEST_PROMOTERS.md` | 10 premiers promoteurs, contexte, résultats négatifs |
| `FIRST_BUYERS.md` | fenêtres 60 s → 24 h, 20 premiers acheteurs, wallets suivis, comparateur sniper |
| `PROMOTER_WALLET_LINKS.md` | phase 4 : comptes → wallets → profits (aucun lien établi) |
| `FINANCIAL_BENEFICIARIES.md` | classement par profit réalisé, sorties, graphe financier |
| `UNRESOLVED_IDENTITIES.md` | inconnues et preuve qui les trancherait |
| `GRAPHS.md` | graphe organisationnel et rappel des 3 classements |
| `REFUTATION.md` | hypothèses concurrentes et résultats négatifs |
| `METHODOLOGY.md` | sources, règles, reproduction |
| `data/` | datasets (voir `PR_NOTES.md`) |
| `data/derived/` | tables régénérées hors ligne par `scripts/analyze.py` |
| `evidence/receipts/` | reçus RPC figés (gzip JSONL) + `key/` (9 tx clés, `INDEX.json`) |
| `evidence/x/`, `evidence/media/`, `evidence/web/` | réponses X brutes (minimisées), images et en-têtes, recherches inversées |
| `scripts/` | collecte (réseau) et dérivation (hors ligne) |
| `tests/test_astra_offline.py` | 14 tests hors réseau |
| `SHA256SUMS.txt` | empreintes |
