# METHODOLOGY — addendum ASTRA

## Méthode et sources

**Méthode** : `historical-x-forensics`.
1. Budget écrit avant la collecte (`raw/00_BUDGET_AND_PLAN.md`) : X ≤ 15 appels (≈10 utilisés), RPC ≤ 6 000, web ≤ 15.
2. Collecte bornée.
3. Gel des reçus.
4. Dérivation hors ligne.
5. Tests.
6. Audit de cohérence avec le dépôt.

**Sources**
- **X API v2** (lecture publique) : `search_posts_all` (25 résultats max), `get_posts_by_ids`, `get_users_by_usernames`. Les heures viennent du snowflake : `(id >> 22) + 1288834974657` ms.
- **RPC Solana public** (`api.mainnet-beta.solana.com`) :
  - `getSignaturesForAddress` (une signature étrangère est acceptée comme borne `before`) ;
  - `getTransaction` (jsonParsed) ;
  - `getBlock` (échantillon sniper).
- **Décodage pump.fun** (programme `6EF8rr…`, format de juillet 2024) :
  - discriminants `sha256("global:buy")[:8]` et `sha256("event:TradeEvent")[:8]` ;
  - erreur 6002 = `TooMuchSolRequired`.
- **Web public** :
  - Yandex (recherche inversée, via curl) ;
  - Wayback CDX ;
  - TinEye : **403, non contourné** ;
  - Google Lens : réponse vide, non contourné ;
  - API pump.fun : 403 lors de la mission précédente, non contourné ;
  - ipfs.io : 429.
- **Images** : PIL et imagehash (pHash, dHash, aHash), différences au pixel.
- **Dépôt** (lecture seule, HEAD `643934a`) : `reports/EARLY_BUYERS.md`, `TOP_TRADERS.md`, `COORDINATION.md`, `ATTRIBUTION.md`, `data/collector.json`, `data/exit_summary.json`, `data/group_split.json`, `evidence/x_wayback/recovered.jsonl`. Des copies figées des extraits utilisés sont dans `data/repo_*`.

## Règles d'attribution appliquées

- Services jamais tenus pour un propriétaire commun : CEX (Coinbase 1/2/3, Binance, MEXC), pools, autorité Raydium `5Q544f…`, Jupiter, wallets d'exécution, bridges.
- Un lien de propriété exige une revendication, une signature, une déclaration liée à une tx, une adresse officielle ou un transfert direct reproductible. Sinon : « attribution non établie ».
- Les clusters de comportement (montants, minutage, collecteur commun) sont notés **B** au maximum. Ils ne servent jamais à nommer quelqu'un.
- Pas de KYC, pas de DM, pas de contournement, pas de désanonymisation.

## Reproduction

```bash
# hors ligne (à partir des reçus figés)
python3 scripts/analyze.py --out /tmp/astra_check && diff -r /tmp/astra_check data/derived
python3 -I -m unittest discover -s tests -v          # ou : python -m pytest -q tests
# collecte (réseau, facultative ; résultats mis en cache dans raw/rpc_cache)
python3 scripts/s3_pump_phase.py; python3 scripts/build_pump_phase.py
python3 scripts/s4_funding.py; python3 scripts/s6_sniper_sample.py
python3 scripts/s8_coinbase3_baserate.py; python3 scripts/s9_cex_batches.py; python3 scripts/s10_sibling_flows.py
python3 scripts/freeze_receipts.py
```

Pour les scripts de collecte, `rpc.py` met chaque réponse en cache dans `raw/rpc_cache/` (environ 36 Mo, non livré dans le dépôt). Les reçus effectivement utilisés sont figés dans `evidence/receipts/` (environ 1 Mo, gzip JSONL).
