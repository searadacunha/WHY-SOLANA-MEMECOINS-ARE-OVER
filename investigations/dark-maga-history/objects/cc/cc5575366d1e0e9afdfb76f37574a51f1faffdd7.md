# Ce qui reste ouvert (05/11/2026)

Chaque point dit ce qui manque, pourquoi, et ce qui le fermerait. Rien ici n'est une conclusion.

> **Mise à jour du 06/11/2026 :** ce document est le relevé historique de l'enquête EVM, avant l'analyse complémentaire Base/BSC/Solana de la [PR #16](https://github.com/searadacunha/Dark-MAGA/pull/16). Les 124 233,75 USDC vers Base et 99 981,82 USDC vers BSC indiqués ci-dessous étaient des bornes **conditionnelles** supposant que le relais ne contenait que des fonds de b947 (H, non démontrée). Les bornes individuelles corrigées sans H sont de 46,814553 USDC pour l'ordre Base du 12/11 (o1), 0 pour l'ordre BSC du 12/11 (o2). Ne pas traiter les anciens chiffres comme des minima inconditionnels.

## 1. Identité derrière b298, b947, `Ei5yGz8d`
- **Manque :** toute identité civile. Aucune étiquette publique sur b298, b947, le relais `0x4978cd7e…`, ni sur les quatre adresses de dépôt inférées.
- **Ce qui la fermerait :** une réquisition auprès de MEXC, Coinbase, KuCoin ou Stake.com sur les adresses de dépôt listées dans `FINDINGS.md` §5. Hors de portée d'un travail on-chain.

## 2. Les quatre adresses de dépôt sont **inférées**, pas étiquetées
- `0x311ef6b5…` (MEXC), `0x100a38ed…` (Stake.com), `0xe1daccdc…` (KuCoin), `0x0ff70a96…` (Coinbase).
- **Méthode :** gaz reçu d'un hot wallet étiqueté de l'exchange juste avant un vidage vers un hot wallet étiqueté du même exchange (preuves dans `FINDINGS.md` §5). C'est le schéma standard d'une adresse de dépôt, mais aucune source ne l'étiquette.
- **Pour `0xe1daccdc`**, la source du gaz n'a pas été lue : seuls les vidages vers KuCoin 3 et des hot wallets KuCoin sont vus. Confiance plus faible.
- **Limite d'interprétation :** une adresse de dépôt appartient à un compte client. Deux wallets qui y versent peuvent appartenir au titulaire du compte, ou payer ce titulaire (OTC, remboursement). Ici, ce signal n'est jamais utilisé seul.

## 3. Chaînes autres qu'Ethereum
- **Base et BSC de b298 non lus.** b298 a 897 tx sur Base, 95 sur BSC, 36 sur Arbitrum et 63 sur Polygon (nonces dans `evidence/s60_crosschain.json`). Blockscout Base, Arbitrum et Polygon répondent 403 (contrôle anti-robot, non contourné). BSC n'a pas d'historique gratuit.
  - Conséquence : l'analyse initiale n'avait pas suivi les sorties de Base ; la valeur de 124 233,75 USDC n'était une borne basse que sous l'hypothèse H, désormais non établie, ni des 157,37 BNB qu'il s'envoie sur BSC le 12/11/2024. On voit seulement qu'une partie revient sur Ethereum vers l'adresse de dépôt MEXC (6 ordres de b298 sur Base, 35 781,16 USDT livrés).
  - **Ce qui le fermerait :** SQD Portal (`base-mainnet`, `binance-mainnet`), filtré sur les journaux Transfer dont topic1 ou topic2 vaut b298, par fenêtres.
- **Ordre de `Ei5yGz8d` vers `0x2ac17414e34c9a1f70f6eadb6230fa503301e878` sur Base** (2 ordres, 5 238,78 USD, corpus i14) : receveur non lu.

## 4. Ce que fait `Ei5yGz8d` des 1 753,73 SOL et 48 960,81 USDC reçus de b298
- Les 24 exécutions sont vérifiées sur Solana (`evidence/s22_sol_fills_check.csv`). Les sorties d'`Ei5yGz8d` après ces réceptions ne sont pas tracées ici, car c'est le périmètre Solana du projet.

## 5. Origine première d'`Ei5yGz8d`
- Il apparaît le 30/03/2024 à 13:18:25 UTC avec 459,667463 USDC d'un signataire `RRbvsvJH…`, puis reçoit 40,68 SOL de `J7CCF72j…` le 31/03 à 03:45:07. Ni l'un ni l'autre n'est étiqueté ici. Il n'est pas établi que b298 l'ait financé à sa création : aucun ordre DLN de b298 n'existe avant le 25/06/2024 dans les données lues, et le pont utilisé, s'il y en a un, n'est pas identifié.

## 6. 2d86 (afk.eth) et 86f9
- Voir `FINDINGS.md` §7. Pour 2d86, la liste des fills DLN entrants est **partielle par construction**. Sur ses 15 425 transferts de jetons, seules les tx dont la méthode ou le taker a déjà servi à un fill confirmé ont été décodées, plus toutes les entrées d'ETH venues de DlnDestination ou du forwarder. Un fill passé par un autre taker ou une autre méthode peut manquer.
- Les transactions internes de 2d86 viennent de Routescan (Blockscout expire sur cette adresse). Routescan est complet pour les tx et les internes sur les adresses testées, mais **pas pour les transferts ERC-20 antérieurs à juillet 2023** (trou silencieux mesuré sur b947 : appels `USDC.transfer` de 2023 sans ligne `tokentx`). Les jetons de 2d86 viennent donc de Blockscout (15 425 lignes, pagination complète).
- **86f9** sort par deux adresses de dépôt à usage unique de FixedFloat. La suite se joue sur une autre chaîne, inconnue.

## 7. API publique deBridge
- `stats-api.dln.trade` a répondu « error code 1015 » (limitation Cloudflare). Non contourné. Elle aurait permis de recouper les états d'ordre et les tx d'exécution sur Base. Les recoupements faits ici reposent sur les journaux on-chain uniquement.

## 8. Ce que les bornes de `evidence/s51_b298_usdc_bounds.csv` ne disent pas
- Elles ne portent que sur l'USDC. Une fois l'USDC venu de b947 converti en ETH par UniswapX ou des solveurs (au moins 247 664 USDC), la part qui finit dans les ordres ETH de b298 vers `Ei5yGz8d` (29,02 ETH le 12/11, 33,52 ETH le 14/11, 34,00 ETH le 17/11/2024) n'est pas bornée. Il faudrait un modèle à deux actifs, au taux de chaque swap.

## 9. Mesures non faites
- Pas de témoin apparié (wallets EVM tirés au hasard parmi les receveurs DLN) pour mesurer à quelle fréquence le schéma « gaz juste-à-temps et vidage complet vers le payeur du gaz » survient entre wallets sans lien. Les signaux sont qualitatifs, sans taux de base.
- Pas d'audit indépendant à l'aveugle de ce dossier.
