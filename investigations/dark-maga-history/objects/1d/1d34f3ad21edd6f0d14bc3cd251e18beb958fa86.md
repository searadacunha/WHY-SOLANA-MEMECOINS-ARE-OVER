# Attribution : liens vérifiables, hypothèses, niveaux

Généré par `scripts/rep_72_links.py`. Échelle : **A** vérifié directement, **B** fortement corroboré, **C** indice, **D** non vérifié ou contredit. Aucune identité civile n'est recherchée ni établie. Un wallet cité n'est accusé de rien.

## Conclusion courte
**Aucun lien documenté entre un wallet et un compte du noyau (@DarkMagaCoin, @kikisknees, @Aristos_Revenge, @ChrisWinig).** Aucun de ces comptes n'a publié d'adresse dans ce qui est archivé. Le lien compte ↔ wallet reste une lacune, pas une absence prouvée. Le corpus X est partiel.

## Les quatre pistes publiques
| Wallet | Source | Acheté SOL | Réalisé SOL | P&L USD | 1er achat UTC | Ach./Vte | Reçu transfert M | Sorti transfert M |
|---|---|---|---|---|---|---|---|---|
| `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` | mission ; source sociale non retrouvée | 281.19 | 1,747.8 | 317,215 | 14/07/2024 02:28:56 | 39/26 | 0.00 | 0.16 |
| `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` | @ai_9684xtpa, id 1815243177475121253, adresse entière dans le lien | 48.50 | 2,540.1 | 458,663 | 14/07/2024 02:15:41 | 103/4 | 0.00 | 0.00 |
| `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | @0xRamonos, id 1815221876190294470, capture | 53.36 | 74.2 | 12,118 | 14/07/2024 02:10:11 | 13/208 | 37.79 | 76.26 |
| `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc` | @ashrobinqt, id 1815233925662306427, capture | 7.27 | 5,490.9 | 990,744 | 14/07/2024 16:43:58 | 48/2 | 0.00 | 0.00 |

- **Les quatre désignent-ils une même entité ?** Non établi, et rien ne le soutient pour `H3QsBr…`, `GXZvX…` et `9PrmF8…` : après retrait des services, aucun chemin direct ne les relie entre eux ni au groupe de lancement (`H3QsBr…` n'a aucune arête directe, `GXZvX…` une seule voisine, `9PrmF8…` une petite composante de 9 wallets). Une absence d'arête n'exclut pas un lien par échange : les quatre passent par des échanges (A pour le fait, C pour toute interprétation).
- **Rapprochement des captures :** `5QhJJc…HScd` et `H3QsBr…T6cc` sont uniques parmi les propriétaires de DMAGA pour ce préfixe et ce suffixe. Pour `H3QsBr…`, 1 087 $ recalculés contre 1 086 $ sur la capture et 16,82 M contre 16,8 M (A). Pour `5QhJJc…`, la capture dit 37 transactions et 28,4 M : l'écart avec les 208 achats totaux s'explique en partie par des ordres DCA Jupiter (keepers `DCAK…`) et des transferts (B). La date « 3 jours » du post correspond aux achats DCA du 17 au 19/07, alors que le wallet achetait dès le 14/07.

## Lien entre le créateur et `5QhJJc…` : A pour la transaction, B pour une action concertée en 2025, C pour un acteur unique au lancement
| UTC | De | Vers | Montant | Actif | Ce que c'est | Signature |
|---|---|---|---|---|---|---|
| 14/07/2024 01:32:23 | `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0.5 | SOL | Le créateur reçoit de Coinbase 3, premier mouvement du wallet | `5Ys6ggx4Fr3eYA4fdaDwowiuZg4HEbcRd6MYcPfspDX3g9KzLKMuKVh7ukUNVy3bpZwwhFT9ZLe2tQFMunHea4Dd` |
| 14/07/2024 01:40:50 | `2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm` | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 1.05 | SOL | `5QhJJc…` reçoit de Coinbase 2, 8 min 27 s plus tard, premier mouvement du wallet | `RpB7AKeKUJMiJ3rRKBtdxuuHsFvGrDN8gVKNxKFCaBQ64A5rxB2YuVVv5KnvWvw3asdg5ZGmq1KWob1wuhPPVdR` |
| 19/02/2025 22:04:04 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `sYBdq543ZX4iAXpNzhT4kTvKBaEDUGkiUo9jBFYdaNd` | 3561097.392281 | DMAGA | `5QhJJc…` avait ouvert un ordre DCA du même type, 4,5 mois plus tôt | `2WJCLkibEpkEbpYqPFfuUchKjqhEm3rkRN7ybmtvy7vxNgKFiDbWUzUMSE4U2VzWSttJBRoSgGWTDg1pJswhSosU` |
| 06/07/2025 02:18:38 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0.032 | SOL | **`5QhJJc…` signe seul un virement de SOL vers le créateur, 35 s avant la ligne suivante** | `Nfzx313VrsXHoEhpfXadwi16CXZyReEEjJA1hojZERATrdgRtz8TdNrveT4wTXPbyUFPySSzFPPXBtXB4LBSYM4` |
| 06/07/2025 02:19:13 | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | `AYymVrcAyPgcMcFkk5NqaEBLj7C4KH2NYvLognUGCEq5` | 7105960.2649 | DMAGA | Le créateur signe un ordre Jupiter DCA de vente sur tous ses jetons ; le destinataire est l'escrow de l'ordre | `2BUp8LXmhuhpiEtp1w4pNLHTuywq7Jf1hxpPHWx9jXmRA3kzwRDutXwfKne4nKVULvwsbCPyN5j57d1j7itbfT1k` |

En plus de deux ans, le créateur n'a reçu que 3 virements d'au moins 0,003 SOL : 0.5 SOL de Coinbase 3 (14/07/2024), 0.57681998 SOL de Raydium AMM v4 authority (16/07/2024), 0.032 SOL de 5QhJJcFZ… (06/07/2025). Le virement de `5QhJJc…` arrive 35 secondes avant qu'il vide sa position.
- **Vérifié (A) :** ces transactions et leurs signataires (`reports/data_checks/group_edges_check.json`).
- **Fortement corroboré (B) :** en juillet 2025, celui qui contrôle `5QhJJc…` et celui qui contrôle le wallet créateur agissent ensemble, ou sont la même personne.
- **Indice seulement (C) :** qu'ils étaient déjà le même acteur au lancement. Les deux financements Coinbase à 8 minutes d'écart, 33 et 25 minutes avant la création, vont dans ce sens, mais un hot wallet sert tout le monde. Une clé peut aussi changer de main en un an. L'usage commun de Jupiter DCA ne vaut rien seul : l'outil est répandu.
- **Ce qui n'est pas établi :** qui. @0xRamonos a seulement commenté ce wallet : **rien ne le relie à lui ni à personne au-delà de sa publication.**

## Relations documentées (`data/social_links.parquet`)
Types distincts : `mention_tierce` (un compte commente un wallet), `declaration_publique` (ce qu'un compte affirme), `interaction_sociale` (réponses et mentions). Aucune arête `wallet_revendique` : zéro.
Déclarations de l'équipe, toutes à prendre pour ce qu'elles sont : « $DMAGA pfp by me and @ChrisWinig », « a wartime PFP that we made for him » (@kikisknees) ; « DMAGA team created Elon's pfp specifically for him » (@DarkMagaCoin).

## Hypothèses non retenues
- **« Musk ou ses proches ont organisé »** : D. Aucun élément ne relie un wallet à Musk ou à son entourage. Il a adopté une image publique.
- **« Ansem, deBridge, la Solana Foundation »** (récit de Benjamin du 02/08) : D. Rien dans ces données. Non testé en profondeur : aucune adresse fournie.
