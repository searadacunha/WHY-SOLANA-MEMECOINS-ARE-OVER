# Pistes non démontrées

| # | Piste | Ce qui manque | Coût estimé |
|---|---|---|---|
| U1 | Test ATA de l'univers DMAGA × KM / XC78 (§7 de FINDINGS) | Fin de la collecte, puis lecture au niveau transaction des candidats non-bots actifs avant 06:02:01 | ~1 h 30 de RPC public restante au 06/11 |
| U2 | Créateur XC78 `9dtGg97Q…` ↔ `Go5rFkwK…` | Financements de l'un et de l'autre avant le 29/12/2024 | quelques dizaines d'appels |
| U3 | Financement des 6 wallets du 4e achat co-signé XC78 (`BmeKXuaj…`, `5JMaYmBp…`, `DHSmQxcw…`, `EawfWPgW…`, `A7ZxBfBx…`, `7qnbEYhM…`) : ils n'ont pas reçu de SOL de Go5 dans la tx de redistribution. `A7ZxBfBx…` et `7qnbEYhM…` appartiennent au groupe payé par `8C9utWVQ…` | Historique avant le slot 310594130 | faible |
| U4 | Où vont les SOL de l'opération XC78 (Go5 et les 16 wallets) après les ventes, et ces fonds touchent-ils un wallet DMAGA ? | Sorties après le 29/12, sans les hubs | moyen |
| U5 | KM : 133 acheteurs sur la courbe en 2 min 01 s. Snipers liés au créateur `4GUgVRft…` ? | Financements des 30 premiers | moyen |
| U6 | KEKIUS Ethereum : les 50 acheteurs du bloc d'ouverture 21397848 sont-ils financés par le créateur ou par un même financeur ? | Historiques de financement (Routescan) | ~50 appels |
| U7 | KEKIUS Ethereum : `0xb1b2d032…` vend 32,25 M sans aucun achat, contre 1 424,10 ETH jusqu'au 04/01. D'où viennent ses jetons ? Wallet de taxe, d'équipe, ou exchange ? | Historique complet (la collecte a échoué : HTTP 502 Routescan) | faible |
| U8 | Trois des 100 premiers acheteurs de KM (`GTvBQnRv…`, `xK5mDD8D…`, `8J9panvq…`) achètent DMAGA pour la première fois en moins de 14 min (05/11/2024 23:53:51 – 06/11 00:07:29) | Lien de fonds entre eux ; un même opérateur de bot reste plausible | faible |
| U9 | Autres copies Kekius (Solana, Base, BSC, Ethereum), dont les envois groupés reçus par b298 sur Base | Inventaire par nom et par heure de création, contrôle des envois groupés | moyen |
| U10 | Part du programme de sniping `9NLjj4Gj…` dans l'ensemble des migrations Raydium | Échantillon de signatures du programme | moyen |
| U11 | Heure exacte du retour du profil de Musk à « Elon Musk », id et snowflake de l'avatar Pepe | Captures Wayback listées dans `MUSK_PROFILE_TIMELINE.md` §5, quand la Wayback répondra normalement, sans contourner son filtre | faible |
| U12 | `8EtTuouE…` (24e acheteur de KM) envoie 32,45 SOL à `CawH4gnd…` le 17/01/2025. Ce dernier figure dans le traçage des financements DMAGA, au niveau 2 | Identifier le wallet DMAGA en aval et le sens du flux | faible |
| U13 | Taux de base : part des acheteurs d'un memecoin Solana comparable qui figurent aussi dans DMAGA | Choisir un témoin de la même période, puis le même test ATA | élevé |
