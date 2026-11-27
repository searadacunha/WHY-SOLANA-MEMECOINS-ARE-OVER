# Pistes non démontrées

| # | Piste | Ce qui manque | Coût estimé |
|---|---|---|---|
| U1 | Fait le 06/11 : test ATA complet, 14 304 couples (FINDINGS §7). Reste : les comptes de jetons non associés, invisibles à ce test | Pour les wallets du noyau, relecture complète de leurs tx de décembre 2024 | moyen |
| U2 | Créateur XC78 `9dtGg97Q…` (1 839 tx depuis mars 2024) ↔ opérateur `3oqARBND…` / `Go5rFkwK…` | Transferts entre eux avant le 29/12/2024 | quelques dizaines d'appels |
| U3 | Résolu le 06/11 : les 16 acheteurs groupés de XC78 sont financés par `3oqARBND…` dans une seule tx (`3UrcoNZA…`, FINDINGS §4.7) | | |
| U4 | Écran des sorties de l'opérateur : 16 668,98 SOL de variations positives sur 1 510 comptes candidats ; trois correspondent à des tables DMAGA, sans signal discriminant (FINDINGS §4.7) | Rejouer les instructions natives et internes pour confirmer les transferts directs ; identifier `MfJ9N5ao…` et les 20 premiers candidats | moyen |
| U5 | KM : 133 acheteurs sur la courbe en 2 min 01 s. Snipers liés au créateur `4GUgVRft…` ? | Financements des 30 premiers | moyen |
| U6 | KEKIUS Ethereum : 44 des 50 acheteurs du bloc d'ouverture n'ont aucune tx entrante de valeur avant ce bloc (`data/eth_open_block_funders.csv`) | Transactions internes et contrats de bots qui livrent ces adresses | moyen |
| U7 | Résolu le 06/11 : `0xb1b2d032…` retire ses KEKIUS de MEXC 21, Gate.io et CoinEx (FINDINGS §5). Où vont ses 1 424 ETH ? | Historique complet (Routescan répond 502 ou expire sur cette adresse) | faible |
| U8 | Trois des 100 premiers acheteurs de KM (`GTvBQnRv…`, `xK5mDD8D…`, `8J9panvq…`) achètent DMAGA pour la première fois en moins de 14 min (05/11/2024 23:53:51 – 06/11 00:07:29) | Lien de fonds entre eux ; un même opérateur de bot reste plausible | faible |
| U9 | Autres copies Kekius (Solana, Base, BSC, Ethereum), dont les envois groupés reçus par b298 sur Base | Inventaire par nom et par heure de création, contrôle des envois groupés | moyen |
| U10 | Part du programme de sniping `9NLjj4Gj…` dans l'ensemble des migrations Raydium | Échantillon de signatures du programme | moyen |
| U11 | Heure exacte du retour du profil de Musk à « Elon Musk », id et snowflake de l'avatar Pepe | Captures Wayback listées dans `MUSK_PROFILE_TIMELINE.md` §5, quand la Wayback répondra normalement, sans contourner son filtre | faible |
| U12 | `8EtTuouE…` (24e acheteur de KM) envoie 32,45 SOL à `CawH4gnd…` le 17/01/2025. Ce dernier figure dans le traçage des financements DMAGA, au niveau 2 | Identifier le wallet DMAGA en aval et le sens du flux | faible |
| U13 | Taux de base : part des acheteurs d'un memecoin Solana comparable qui figurent aussi dans DMAGA | Choisir un témoin de la même période, puis le même test ATA | élevé |

| U14 | `CKMVA5xe…` et `aaYqdhGp…` (clusters DMAGA 777 et 626) achètent DMAGA à 94 s d'intervalle le 05/10/2024 et KM avant le changement | Transferts entre eux, ou financeur commun | faible |
| U15 | `5QhJJc…` → `DMJmb8aJ…` 7 000 USDC (20/01/2025) : même propriétaire ou paiement ? `DMJmb8aJ…` est un trader à haute fréquence, qui achète KM le 14/12/2024 | Autres échanges entre les deux, financeurs de `DMJmb8aJ…` | moyen |
