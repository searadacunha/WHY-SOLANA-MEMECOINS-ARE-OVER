# Méthode et limites

## Sources

| Donnée | Source | Clé | Remarque |
|---|---|---|---|
| Signatures et transactions Solana (jsonParsed, instructions internes) | RPC public `api.mainnet-beta.solana.com` via `k16_pubrpc` (enquête Kekius) | aucune | cache par signature hors dépôt (`HIST_EXT/pub`) ; environ 0,5 transaction/s, nombreuses réponses 429 |
| Swaps, virements DMAGA, flux SOL et USDC de l'enquête d'origine | `data_v2/*.parquet` du disque de l'enquête (Helius, 02-03/11) | — | non publiés en entier ; voir §8 de FINDINGS pour le trou `Transfer` |
| Posts X | `api.fxtwitter.com` et `cdn.syndication.twimg.com` (`dmaga.xposts`), charges Wayback déjà archivées | aucune | réponses brutes dans `evidence/x_hist/` et `evidence/x_raw/` |
| Médias X | `pbs.twimg.com` | aucune | seules les empreintes sont publiées ici (`evidence/x_hist_media/MANIFEST.json`), sauf les captures @AutismCapital et @realjohnnewburg, versées au corpus comme les 703 autres médias |
| Cours SOL/USD | archives SOLUSDT 1 min de Binance (`raw/solusd` de l'enquête d'origine) | — | clôture de la minute |
| Contrats KLLARY, RETIREDIO, JOE, ZOOMER | pistes d'un agent de recherche (Reddit 13/07/2024, Wayback CoinGecko 27/05/2024, GeckoTerminal), relues sur la chaîne (`h50`) | aucune | sources brutes de l'agent non publiées |

**Clés Helius**
- Le pool de recherche répondait « toutes les clés épuisées » le 06/11/2026.
- Aucune clé n'a servi à ce dossier, et aucune n'a été lue ni affichée.

## Règles

**Mouvements** (`h_decode.py`)
- Un mouvement se lit dans une instruction System (`transfer`, `createAccount`) ou SPL (`transfer`, `transferChecked`, `closeAccount`), externe ou interne.
- Un compte de jetons est rapporté à son propriétaire par les soldes pre/post de la même transaction.
- Une fermeture de compte WSOL rend le solde courant du compte : loyer plus WSOL reçu plus tôt dans la transaction.

**Soldes à un instant**
- Somme des deltas de `trades.parquet`, puis contrôle primaire par l'ATA : historique complet des signatures, dernière transaction avant l'instant, `postTokenBalances`.
- Les 15 adresses de Noah concordent à 0 près.

**Résolution d'une abréviation (A1UD…vQ8J)**
- Préfixe et suffixe cherchés parmi les seules destinations SOL observées de 7GVC et 9Sxm.
- Plus ou moins d'une adresse, et le script s'arrête. Aucune adresse n'est complétée à la main.

**Services**

| Classe | Critère |
|---|---|
| Service | plus de 25 wallets DMAGA touchés, ou étiquette d'exchange, de pool, de routeur ou de compte Jupiter |
| Poussière | moins de 0,01 SOL par virement |
| Candidate | le reste, relu à la main (`data/noah_candidates_review.csv`) |

- Une destination commune n'est jamais un lien sans lecture de ses autres contreparties.
- `HBsgbpsM…` le montre : 14 payeurs, dont cinq paiements identiques de 700 $, décrivent un service probable, pas un lien entre payeurs.
- La règle « service » s'applique avant la règle « poussière ».

**Tests par ATA** (`h51`, `h52`)
- Ensembles et fenêtres écrits dans le code avant le premier appel ; mêmes requêtes pour testés et témoins.
- Une activité d'ATA est relue jusqu'au solde du jeton avant d'être appelée achat ou vente.
- Fisher unilatéral exact.
- Résultats exploratoires : aucun gel, aucune correction pour comparaisons multiples.

**Fenêtres** (`h40`)
- Même requête et mêmes exclusions qu'`ana_50` (venues, autorité Raydium, courbe, comptes de migration).
- Anciennes et nouvelles bornes calculées sur les mêmes données.

**Provenance X** (`h21`)
- Trois preuves gardées séparées :
  - objet renvoyé par les API ;
  - charge Wayback ;
  - champs `reply_to_id` et `quote_id`.
- Le compte de l'URL d'archive n'est jamais une preuve d'auteur.

## Reproduction

```bash
# hors ligne, depuis la racine du dépôt (CI : historical-replay-evidence.yml)
python -I -m unittest discover -s investigations/2026-11-06_historical_replay/tests -p 'test_*.py' -v

# chaîne complète (réseau, disque de l'enquête monté ; Python : scripts/py.sh)
cd investigations/2026-11-06_historical_replay/scripts
../../../scripts/py.sh h20_xfetch.py && ../../../scripts/py.sh h21_x_reconcile.py
../../../scripts/py.sh h10_sigs.py <7GVC> <9Sxm> <H3Qs>
../../../scripts/py.sh h11_txs.py <wallet> --since 1720828800 --until 1721865600    # puis h30_ledger.py
../../../scripts/py.sh h31_jeffro.py && ../../../scripts/py.sh h32_noah.py && ../../../scripts/py.sh h34_verify_balances.py
../../../scripts/py.sh h33_counterparty.py HBsgbpsM1j1YsNYqtCXcFU4mCRofwcor2qFwifNqddmH
../../../scripts/py.sh h35_atzj_gxzvx.py && ../../../scripts/py.sh h40_windows.py && ../../../scripts/py.sh h50_contracts.py
../../../scripts/py.sh h51_ata_test.py kllary && ../../../scripts/py.sh h51_ata_test.py retiredio
../../../scripts/py.sh h52_rotation.py retiredio && ../../../scripts/py.sh h52_rotation.py kllary
../../../scripts/py.sh h53_h3qs.py && ../../../scripts/py.sh h60_pass3.py && ../../../scripts/py.sh h39_receipts.py
# audit indépendant (hors ligne)
python3 -I ../audit/second_auditor_receipts.py
# chronologie et cohortes corrigées (racine du dépôt)
scripts/py.sh scripts/guard.py -- scripts/py.sh scripts/ana_50_cohorts.py
scripts/py.sh scripts/guard.py -- scripts/py.sh scripts/rep_75_timeline.py
```

## Limites

**Couverture**
- Grands livres décodés seulement du 13 au 25/07/2024 pour 7GVC et 9Sxm. Le reste vient des tables Helius d'origine, avec leurs seuils.
- Arêtes entre groupes : sous les seuils de `col_30` (0,01 SOL en entrée, 0,1 SOL ou 100 USDC en sortie), un virement peut manquer.
- Un compte de jetons non associé échappe aux tests par ATA.
- `trades.parquet` omet les virements `Transfer` simples (FINDINGS §8). Aucun solde de ce dossier n'en dépend sans contrôle par ATA.

**Captures @realjohnnewburg et @AutismCapital**
- Elles prouvent l'heure de publication, pas celle du clic ni de la capture.
- Le pHash compare un disque recadré au visuel : il ne prouve pas que la page capturée était réelle.

**Agent de recherche**
- Il a proposé les quatre contrats et la rotation JOE → DMAGA de H3Qs.
- Tout a été revérifié ici sur la chaîne (`h50`, `h53`, reçus).
- Il est resté plus fiable que la mémoire : deux préfixes et une adresse tapés de mémoire pendant cette session ont été arrêtés par les garde-fous (`h39`, test `NoInventedAddress`) ou corrigés avant publication.
