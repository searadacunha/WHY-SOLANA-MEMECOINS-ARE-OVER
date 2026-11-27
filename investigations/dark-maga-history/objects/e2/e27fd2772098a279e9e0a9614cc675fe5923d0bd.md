# Rejeu historique des sources X (6 novembre 2026)

Question : que valent, transaction par transaction, les pistes du mémo historique (`docs/historical/`) ? Provenance des posts, borne de l'avatar de Musk, circuits de @JeffroBTC et de @Noah_nftn, puis AtZj, GXZvX, KLLARY, RETIREDIO et H3Qs.

| Fichier | Contenu |
|---|---|
| `FINDINGS.md` | Constats hiérarchisés (CONFIRMÉ, CORROBORÉ, HYPOTHÈSE, REJETÉ), signatures, heures, montants |
| `METHODOLOGY.md` | Sources, règles, reproduction, limites |
| `data/x_observations_reconciled.csv` | Les 5 156 observations X : original, repost, réponse, citation, objet réel et preuve |
| `data/ledger_7GVC_*.csv`, `data/ledger_9Sxm_*.csv` | Grands livres décodés instruction par instruction, 13-25/07/2024 |
| `data/jeffro_claims.csv`, `data/jeffro_satellites.csv` | Affirmations de Jeffro, verdicts, signatures |
| `data/noah_*.csv` | Avoirs à l'heure du post (contrôlés par ATA), arêtes, contreparties communes et leur revue |
| `data/windows_sensitivity.csv`, `data/trades_1927_1930.csv` | Effet des bornes corrigées sur les fenêtres d'achat |
| `data/ata_*.csv`, `data/rotation_*.csv`, `data/contracts_verified.json` | KLLARY et RETIREDIO : tests par ATA, relectures, contrats |
| `data/h3qs_*.csv`, `data/atzj_gxzvx.json`, `data/counterparty_*.csv` | H3Qs, AtZj, GXZvX, fournisseur `HBsgbpsM…` |
| `evidence/receipts/` | 76 transactions citées, figées ; `INDEX.json` dit pourquoi |
| `evidence/x_hist/` | Réponses brutes fxtwitter et syndication des posts du mémo |
| `scripts/`, `tests/` | Collecte, calcul ; 16 tests hors ligne |

Tests : `python3 -I -m unittest discover -s investigations/2026-11-06_historical_replay/tests -v`
