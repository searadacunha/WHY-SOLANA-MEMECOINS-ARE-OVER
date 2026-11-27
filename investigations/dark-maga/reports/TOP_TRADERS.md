# Plus gros gagnants de DMAGA

Généré par `scripts/rep_70_reports.py`, ne pas éditer à la main.

Population : 71 673 wallets, hors réserves de pools, routeurs et échanges. SOL acheté 786 902, SOL vendu 782 178, réalisé cumulé 98 124
(le cumul ne s'annule pas : les frais de plateforme, les positions de liquidité et les jetons reçus sans coût en sortent).

## Comment lire
- **Réalisé** : SOL reçu aux ventes moins coût moyen de ce qui est vendu, sur Raydium v4, CLMM, Meteora DLMM, Orca et la courbe. Une valorisation maximale n'y entre jamais.
- **Flux net** : SOL vendu moins SOL acheté, liquidité comprise. Ne dépend pas d'une hypothèse de coût.
- **USD** : conversion à la minute de chaque trade (SOLUSDT Binance).
- **Résiduel** : jetons restants, valorisés au dernier prix du pool (02/11 23:15:29 2026), bien inférieur au sommet.
- **Complétude** : « partiel » signale des jetons reçus ou sortis hors swap ; le réalisé d'un wallet qui reçoit ses jetons d'un autre est surévalué.
- Cohortes : avant le visuel exact de @ChrisWinig (21/07 16:02:29), avant la borne basse du changement de photo (21/07 19:03:27), dans la fenêtre (21/07 19:03:27 à 21/07 19:25:23), après.

## Résultat par cohorte de premier achat
| Cohorte | Wallets | SOL acheté | SOL vendu | Réalisé cumulé | Réalisé médian | Wallets gagnants |
|---|---|---|---|---|---|---|
| avant visuel | 1645 | 122 345 | 158 294 | 44 080 | 0,053 | 1035 (63 %) |
| avant Musk | 76 | 1 845 | 2 240 | 470 | 1,308 | 62 (82 %) |
| fenêtre Musk | 8 | 50 | 202 | 176 | 0,508 | 8 (100 %) |
| après Musk | 53899 | 662 662 | 572 536 | 4 492 | -0.001 | 18319 (34 %) |
| aucun achat | 16045 | 0 | 48 906 | 48 906 | 0,000 | 7339 (46 %) |

## 100 plus gros réalisés, coût connu
Retenu si moins de 5 % des ventes sont sans quantité connue et moins de 5 % du stock vient de transferts sans coût.

| # | Wallet | Réalisé SOL | Flux net SOL | Acheté SOL | Vendu SOL | P&L USD | Ach./Vte | Résiduel M | Cohorte | 1er achat UTC | Dernière vente UTC | Complétude |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc` | 5 490,9 | 5 490,9 | 7,27 | 5 498,1 | 990 744 | 2/48 | 0,00 | avant visuel | 14/07 16:43:58 | 23/07 14:33:52 | complet sur le pool et la courbe |
| 2 | `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` | 2 540,1 | 2 540,1 | 48,50 | 2 588,6 | 458 663 | 4/103 | 0,00 | avant visuel | 14/07 02:15:41 | 23/07 11:48:23 | complet sur le pool et la courbe |
| 3 | `FTKTNFqeu9wzckDzmsaL1dTgB19BK6fE6DMTHdbETtd1` | 2 046,0 | 2 046,0 | 381,50 | 2 427,5 | 372 356 | 30/135 | 0,00 | après Musk | 21/07 19:47:57 | 23/07 14:29:59 | complet sur le pool et la courbe |
| 4 | `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` | 1 747,8 | 1 747,4 | 281,19 | 2 028,5 | 317 215 | 26/39 | 0,00 | avant visuel | 14/07 02:28:56 | 18/08 18:48:35 | partiel: jetons sortis hors swap |
| 5 | `F1DRDBNW1CX3BPoZPQafidvMeaepg6LS19J4vHqn7xMt` | 1 709,5 | 1 709,5 | 30,00 | 1 739,5 | 310 516 | 1/27 | 0,00 | avant visuel | 15/07 16:54:33 | 23/07 06:07:17 | complet sur le pool et la courbe |
| 6 | `6Lomz4sdWdAwCKmjc8wHFhEHAPDwa5KEmxi1ziEWXp9G` | 1 466,6 | 1 382,2 | 344,62 | 1 726,8 | 246 357 | 81/281 | 6,66 | avant visuel | 14/07 02:07:06 | 29/04 22:08:28 | partiel: jetons reçus sans coût |
| 7 | `CEzjbQqAa5741cJHDstH5Czt4xNiPgLHwax6av449Jyy` | 1 323,0 | 1 322,0 | 32,62 | 1 354,6 | 240 858 | 25/67 | 0,00 | avant visuel | 14/07 02:06:58 | 25/12 08:08:28 | partiel: jetons sortis hors swap |
| 8 | `DKs3wSE35ckDixo9TCYTFpYtdzEHtnGBDZyWc2iHRKP5` | 1 179,8 | 806,8 | 630,00 | 1 188,0 | 97 865 | 21/42 | 0,00 | après Musk | 22/07 05:20:33 | 24/07 09:11:57 | partiel: positions de liquidité |
| 9 | `Go3fTCdm481k8ViaPYN6Y5jVN8Lfg1vRrUJF3ZM9D16b` | 765,3 | 765,3 | 270,00 | 1 035,3 | 141 583 | 17/25 | 0,00 | après Musk | 21/07 19:44:07 | 21/07 23:41:49 | complet sur le pool et la courbe |
| 10 | `FHXYk1x2J9LHrU4Y6CFQUrbrPumjxpQ6uG6bCcaALsx3` | 762,0 | 762,0 | 149,50 | 911,5 | 140 997 | 3/19 | 0,00 | après Musk | 21/07 20:54:03 | 22/07 00:10:22 | complet sur le pool et la courbe |
| 11 | `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` | 729,2 | 729,2 | 231,16 | 960,4 | 129 835 | 17/18 | 0,00 | avant visuel | 14/07 12:59:49 | 22/10 14:12:36 | complet sur le pool et la courbe |
| 12 | `F2kcbXTMKcZZ9ufCarAo4FmCf9M184sDD12TGiKMgYfQ` | 705,8 | 722,9 | 88,42 | 750,6 | 120 757 | 5/58 | 1,10 | avant visuel | 14/07 02:34:43 | 06/11 04:47:13 | partiel: positions de liquidité |
| 13 | `7Fa8XGm1xdzqx9sYQMrPFtVe4j5z37ktGn1FXBu4bzs1` | 646,2 | 646,2 | 250,00 | 896,2 | 115 115 | 2/4 | 0,00 | après Musk | 21/07 22:08:04 | 22/07 09:53:36 | complet sur le pool et la courbe |
| 14 | `EEdq9Cw2GBXoVieSm2nRnCu81KRS5rNCzpKbKVeUXeD` | 618,8 | 617,8 | 15,22 | 633,0 | 111 215 | 16/421 | 0,00 | avant visuel | 14/07 06:48:34 | 01/11 18:39:54 | partiel: jetons sortis hors swap |
| 15 | `ErNKPzqv3eXwaYC8adfgFpuPcyXYFNpwk68NTAbP9LGY` | 588,1 | 588,0 | 35,61 | 623,7 | 105 648 | 12/16 | 0,00 | avant visuel | 15/07 16:48:05 | 06/11 06:48:58 | partiel: jetons sortis hors swap |
| 16 | `7uRDe43iDncwEESfHvyxqYw3tzaVZgvCQn67x3xYyQeY` | 556,4 | -338.7 | 1 190,38 | 558,7 | -115,622 | 3/8 | 0,00 | après Musk | 22/07 00:22:35 | 03/08 00:08:45 | partiel: positions de liquidité |
| 17 | `9CsCwjmi4uHqYGdrDPaKTphqUK9A6A1jzfAFpsWeCkFC` | 549,5 | 549,5 | 5,67 | 555,1 | 100 908 | 6/46 | 0,00 | avant visuel | 14/07 14:20:14 | 23/04 16:22:00 | complet sur le pool et la courbe |
| 18 | `2bUqHhkdryVMR88q3BNxYzuvUxvgzJEMjNgFW5zujZjF` | 545,4 | 545,4 | 667,83 | 1 213,2 | 108 876 | 53/14 | 0,00 | avant visuel | 15/07 14:51:22 | 06/11 06:34:48 | complet sur le pool et la courbe |
| 19 | `53KqxbJvrsECBQ4AwNbiyhmRaKi4U7xGPRByMp6GfoC3` | 531,7 | 531,7 | 151,00 | 682,7 | 95 642 | 5/11 | 0,00 | après Musk | 21/07 19:31:44 | 22/07 08:58:17 | complet sur le pool et la courbe |
| 20 | `5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx` | 489,6 | 489,6 | 32 832,72 | 33 322,3 | 84 281 | 1053/1053 | 0,00 | avant visuel | 15/07 15:17:33 | 07/10 17:24:01 | complet sur le pool et la courbe |
| 21 | `5EdLBiQGNM65tjUEVt5rgk35UCkgMCx2fdSxay2452R4` | 476,8 | 465,5 | 354,62 | 820,1 | 83 599 | 18/14 | 0,00 | après Musk | 21/07 19:42:03 | 28/10 00:26:41 | partiel: jetons sortis hors swap |
| 22 | `5cLnb3P9sAgVn93w9sXc5VmDi2oV65cz1VvD6TUBWfdB` | 469,5 | 469,5 | 30,40 | 499,9 | 84 607 | 13/33 | 0,00 | avant visuel | 14/07 02:44:05 | 01/08 23:03:38 | complet sur le pool et la courbe |
| 23 | `8Jzeow7v4hSWzxPTVA1Kiyec7adbnkX5M13aZZRjvArZ` | 463,0 | 379,0 | 253,75 | 632,7 | 71 915 | 67/29 | 0,00 | avant visuel | 14/07 06:44:16 | 01/02 06:01:36 | partiel: jetons reçus sans coût |
| 24 | `4SZG7mj4ufaki3FTd65aAqt8ZmGWeubuXUnmWLz564ut` | 460,9 | 432,1 | 1 513,96 | 1 946,0 | 69 523 | 57/18 | 0,26 | après Musk | 23/07 18:07:23 | 06/11 01:08:28 | complet sur le pool et la courbe |
| 25 | `4GVoqTXYLRDyBZPVTeX6PeDsoJ4vJeP4gPdVPeqkeKXe` | 455,0 | 455,0 | 495,00 | 950,0 | 87 454 | 12/9 | 0,00 | avant visuel | 21/07 02:24:45 | 27/07 13:48:22 | complet sur le pool et la courbe |
| 26 | `7HzSjbeUFmTZ6yg6HqbA7VhMWynUofzy6mvV5HxVaPvF` | 446,2 | 446,2 | 166,50 | 612,7 | 80 484 | 30/28 | 0,00 | avant visuel | 14/07 07:24:36 | 02/02 13:14:27 | complet sur le pool et la courbe |
| 27 | `FaQQATa15TpZRqbVSCs7VYtFq5rUp9e6zw5zSzdpfPYJ` | 441,5 | 441,5 | 40,00 | 481,5 | 79 804 | 2/6 | 0,00 | après Musk | 21/07 20:09:55 | 23/07 13:57:17 | complet sur le pool et la courbe |
| 28 | `9cnmZD7HsgV53UZagznTceNVBfthcdxZx6ZWw5wRajHF` | 420,0 | 417,3 | 348,17 | 765,4 | 58 495 | 32/13 | 0,00 | après Musk | 23/07 01:19:22 | 13/08 04:35:35 | partiel: jetons sortis hors swap |
| 29 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | 405,4 | 356,5 | 132,23 | 488,7 | 66 624 | 79/73 | 0,00 | avant visuel | 14/07 02:18:03 | 08/11 06:11:58 | partiel: jetons reçus sans coût |
| 30 | `6bW7RAdNLWm3543VrmGFHtL47sAmMabgLBynS9mzRjFE` | 395,8 | 395,8 | 12,00 | 407,8 | 71 282 | 3/31 | 0,00 | avant visuel | 21/07 13:40:29 | 23/07 14:10:34 | complet sur le pool et la courbe |
| 31 | `3VNB9JhWTQHmb17U5X3eusg99t58y8G6x1YHQcWbL8nR` | 358,2 | 358,2 | 46,40 | 404,6 | 65 408 | 16/34 | 0,00 | avant visuel | 19/07 07:57:19 | 14/10 11:54:20 | complet sur le pool et la courbe |
| 32 | `BBcYhznjGjWVNVhaVGC5oBdkipydkjmqsiNciadXBXbY` | 352,3 | 352,3 | 399,20 | 751,5 | 64 065 | 38/70 | 0,00 | avant visuel | 15/07 17:23:53 | 24/07 03:46:50 | complet sur le pool et la courbe |
| 33 | `8GrFf2zNh8FGsWzEqtq2ASfFpckGqNuhA1pR2RGrrPB8` | 342,7 | 284,4 | 96,23 | 384,6 | 52 333 | 31/17 | 0,00 | avant visuel | 15/07 06:58:05 | 22/09 13:25:03 | partiel: positions de liquidité |
| 34 | `G8FXw4ciLVjZwdNgDHtUADQngi1US9gqVc9rtBQoTUFa` | 339,1 | 335,1 | 50,00 | 385,1 | 60 261 | 1/5 | 0,00 | après Musk | 21/07 20:37:38 | 27/07 00:23:18 | partiel: jetons sortis hors swap |
| 35 | `AtGa4eaTSMjNa3VMLfbti6iLqLhqQ988qjBK6AGo8ypU` | 323,0 | 323,0 | 331,96 | 655,0 | 56 150 | 2/1 | 0,00 | après Musk | 21/07 22:51:01 | 22/07 07:01:50 | complet sur le pool et la courbe |
| 36 | `4RDiixyNxHxN6gGMbH4ZmTVDQxdyeFQ3hksGQUBjqf9b` | 321,0 | 321,0 | 88,00 | 409,0 | 58 077 | 123/58 | 0,00 | avant visuel | 16/07 18:28:55 | 05/11 17:38:08 | complet sur le pool et la courbe |
| 37 | `4tg39jDpd3DhuEyeZz4ELbsR3AU4Y8kdZiPpN6iu8eN8` | 312,0 | 288,9 | 106,73 | 407,6 | 52 943 | 80/95 | 0,00 | avant visuel | 14/07 03:56:19 | 12/12 03:27:24 | partiel: positions de liquidité |
| 38 | `7H3bQRRCPjUyDt2i6wqLyWhjLQWUWPfHQjC2guRkb8Vu` | 301,6 | 299,2 | 792,05 | 1 091,2 | 42 270 | 90/117 | 0,00 | après Musk | 26/09 09:28:51 | 13/10 12:01:15 | partiel: jetons sortis hors swap |
| 39 | `3w3FPZbJRCuMwyPEpUEUba6wGcZZBha6AqwxZHrVdjw8` | 294,1 | 294,1 | 22,40 | 316,5 | 53 394 | 1/6 | 0,00 | après Musk | 21/07 19:58:27 | 22/07 04:22:45 | complet sur le pool et la courbe |
| 40 | `BEdodwDQrzVERnDr4qqc8PhJDt5pw9F5NrPFkxU7kffk` | 287,7 | 287,7 | 38,95 | 326,6 | 51 947 | 20/10 | 0,00 | après Musk | 21/07 21:00:55 | 22/07 05:24:18 | complet sur le pool et la courbe |
| 41 | `7dY2yLDbFxUCdBUMLiNJVz9Mq1PfetrDjr9GXAMnMM4J` | 284,2 | 227,4 | 195,49 | 422,9 | 36 552 | 21/180 | 0,00 | avant visuel | 14/07 02:08:23 | 06/11 07:41:45 | partiel: jetons reçus sans coût |
| 42 | `Dpef6tbNvaiNqojTgh214m6JJ7D7wgHoMUBvh5cdiiWw` | 281,8 | 281,8 | 11,57 | 293,3 | 51 366 | 5/40 | 0,00 | avant visuel | 18/07 00:11:52 | 27/08 18:14:59 | partiel: jetons reçus sans coût |
| 43 | `GDWf6DsXKdnThKMgGzcQbNqdn1TRaiLRMKsQfg1PvzCq` | 277,8 | 277,8 | 440,55 | 718,3 | 51 149 | 34/17 | 0,00 | après Musk | 21/07 19:44:32 | 22/07 01:12:33 | complet sur le pool et la courbe |
| 44 | `7vu8g3mAKWY5QedxNxY1F5FYeNaLJsj8JHfKmmHdC4V5` | 275,9 | 275,9 | 104,54 | 380,5 | 48 673 | 5/4 | 0,00 | après Musk | 21/07 22:43:50 | 22/07 09:52:08 | complet sur le pool et la courbe |
| 45 | `AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS` | 273,6 | 273,6 | 16 739,81 | 17 013,4 | 47 590 | 736/736 | 0,00 | avant visuel | 14/07 02:18:21 | 11/11 17:06:04 | complet sur le pool et la courbe |
| 46 | `4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S` | 268,4 | 259,6 | 9 986,81 | 10 246,4 | 44 866 | 948/1088 | 0,00 | avant visuel | 14/07 02:16:47 | 06/10 15:52:39 | partiel: jetons reçus sans coût |
| 47 | `7Y4tsDrRcRMFuZGWZ6gdSKQ2YmfSuuQP9zYwvAe4DA7Z` | 266,9 | 266,9 | 10,89 | 277,7 | 47 932 | 3/64 | 0,00 | avant visuel | 19/07 17:51:33 | 23/07 14:54:37 | complet sur le pool et la courbe |
| 48 | `71CPXu3TvH3iUKaY1bNkAAow24k6tjH473SsKprQBABC` | 266,1 | 266,1 | 946,00 | 1 212,1 | 23 072 | 44/34 | 0,00 | après Musk | 21/07 22:51:51 | 28/03 16:15:06 | complet sur le pool et la courbe |
| 49 | `Dt2oQeGqcHhWz8f3oQWVUGnZwN9vBeXvk7A4F4sj3qJm` | 258,4 | 258,4 | 7,93 | 266,3 | 47 077 | 1/3 | 0,00 | avant visuel | 16/07 02:53:19 | 23/07 17:18:36 | complet sur le pool et la courbe |
| 50 | `6HUqdT1GHwT3YexzF7xbwjyhbm6YtjJ2SZho5wc2e9Yc` | 254,7 | 254,7 | 163,35 | 418,1 | 46 107 | 75/43 | 0,00 | avant visuel | 15/07 16:56:42 | 30/07 01:48:40 | complet sur le pool et la courbe |
| 51 | `G5WdNYEwF3iePH4ALBD21A9j1fYDiejEg6AxvSb97Ajr` | 253,0 | -50.8 | 339,60 | 288,0 | -472 | 54/10 | 0,00 | après Musk | 05/11 23:54:57 | 19/01 10:45:42 | partiel: positions de liquidité |
| 52 | `9CfNRq45kocvoX31E1vhPbqkkxMqEYYuZKHFSAJYRaCv` | 238,2 | 238,2 | 251,79 | 490,0 | 52 702 | 6/6 | 0,00 | après Musk | 20/08 19:37:01 | 14/11 07:26:12 | complet sur le pool et la courbe |
| 53 | `W4ytsNZWrW24K5fYLiDy3JmZeXCr4Hhdm2ghc9GHzPm` | 233,8 | 86,5 | 210,95 | 239,7 | 4 670 | 21/6 | 0,00 | après Musk | 29/10 16:03:21 | 01/11 18:40:21 | partiel: positions de liquidité |
| 54 | `8GRasxaCgMV7JHWTgWSmgJKWVhgynbyczExJ82GVitaJ` | 226,5 | -30.9 | 234,38 | 240,3 | 794 | 66/35 | 0,00 | après Musk | 21/07 22:42:41 | 24/07 13:29:24 | partiel: positions de liquidité |
| 55 | `5U3KFv4Yay2tUVu1ee5ztieVaCp9NmpT9Jm8ErA2wH2C` | 221,2 | 46,7 | 299,50 | 291,4 | -1,583 | 43/48 | 0,00 | après Musk | 21/07 22:53:55 | 06/10 01:11:29 | partiel: positions de liquidité |
| 56 | `6K2d9LvM3i47P9FxzEQP4hXZwiHA2c2wgfzGTeTvJqj8` | 218,7 | 218,7 | 312,67 | 531,4 | 41 185 | 3/2 | 0,00 | après Musk | 21/07 22:59:28 | 06/11 04:20:46 | complet sur le pool et la courbe |
| 57 | `234xKniKxoMzxRTJxMWQdkErLyM7CUs7E4Sf47WX5bdS` | 217,7 | 217,7 | 5,00 | 222,7 | 40 192 | 1/1 | 0,00 | avant visuel | 21/07 01:13:30 | 21/07 23:09:51 | complet sur le pool et la courbe |
| 58 | `GqKS8ikYMTpVrJeLv8jk91s454vMnE3sPmNxZ5AzrwAZ` | 214,3 | 214,3 | 217,80 | 432,1 | 37 988 | 8/9 | 0,00 | après Musk | 21/07 21:50:52 | 22/07 21:30:17 | complet sur le pool et la courbe |
| 59 | `4Xm3yjXYpArUFb8nmtXmuuNuxJjsJrNNfjmS8FWRJ1Q3` | 212,2 | 212,2 | 144,87 | 357,0 | 36 654 | 4/4 | 0,00 | après Musk | 21/07 20:48:28 | 04/03 19:21:22 | complet sur le pool et la courbe |
| 60 | `9BYH65sp6apnsSXy9ZbG94AwiYzBCjRhmYPpSuMdiCzm` | 211,2 | 211,2 | 99,00 | 310,2 | 38 301 | 6/8 | 0,00 | après Musk | 21/07 22:36:50 | 22/07 20:48:35 | complet sur le pool et la courbe |
| 61 | `5aVPkEUnF8zztQ1sGvvNSpJXUgbWfHcGuvz9MaF6LWjp` | 207,9 | 207,9 | 14,09 | 222,0 | 37 847 | 6/9 | 0,00 | avant visuel | 20/07 22:25:24 | 12/11 23:32:52 | complet sur le pool et la courbe |
| 62 | `5eQ8aGfsJLkvawp6goP5DYhkfQyTqsw49KmLucQpCxpA` | 207,2 | 207,2 | 19,80 | 227,0 | 37 680 | 2/4 | 0,00 | avant visuel | 15/07 16:55:55 | 23/07 20:45:42 | complet sur le pool et la courbe |
| 63 | `3W7AKDzLZE3U7k4RPVPviA1qQxvtEppK1rrL57fx2rU1` | 205,1 | 205,1 | 190,00 | 395,1 | 35 797 | 8/10 | 0,00 | après Musk | 21/07 22:51:08 | 23/07 05:06:42 | complet sur le pool et la courbe |
| 64 | `kmQzXPDdXd1n4pMTU28HKyDdHP1eZkRiYhfbw7hq6VC` | 202,4 | 202,4 | 102,86 | 305,3 | 36 653 | 4/12 | 0,00 | après Musk | 21/07 19:34:02 | 22/07 19:57:55 | complet sur le pool et la courbe |
| 65 | `3sQk5QKPiBD9dy99KXQsuLqULN7gRf42t3KBuuy8iYiS` | 195,6 | 195,6 | 20,14 | 215,7 | 34 850 | 6/10 | 0,00 | avant visuel | 15/07 23:29:02 | 22/07 23:12:16 | complet sur le pool et la courbe |
| 66 | `HqAkiPZDHzvpPmruL4yCPuYwWTYjroyk6KLWtC6HRn2q` | 194,2 | 56,3 | 206,95 | 194,6 | -2,422 | 22/6 | 0,00 | après Musk | 10/11 11:00:56 | 11/11 11:23:10 | partiel: positions de liquidité |
| 67 | `HwNxZfACbJgmDug7ATmfFdJaaY3FWWhTw3XFdN7XkQVW` | 193,7 | 77,3 | 219,72 | 195,5 | -4,697 | 2/76 | 0,00 | après Musk | 21/07 23:45:23 | 22/07 18:17:09 | partiel: positions de liquidité |
| 68 | `H7ivexjsSUjhgbk8dsBzSG4uoyRWUprRR7MKfP1h95Sn` | 192,2 | 192,2 | 19,00 | 211,2 | 35 106 | 1/3 | 0,00 | après Musk | 21/07 19:37:41 | 22/07 18:19:42 | complet sur le pool et la courbe |
| 69 | `H9zE2cWhpThd1A9HgkQL7u11Xxe8BT4a5f5s1kU1CYyV` | 190,9 | 190,9 | 12,99 | 203,9 | 34 526 | 7/5 | 0,00 | avant visuel | 21/07 01:43:40 | 04/08 19:40:12 | complet sur le pool et la courbe |
| 70 | `EML2VjgoWaakEBq2hrkd6EVvZdmCe4dFsWH4m1EW3XC8` | 188,4 | 188,4 | 18,00 | 206,4 | 34 279 | 3/15 | 0,00 | après Musk | 21/07 20:24:03 | 23/07 14:19:37 | complet sur le pool et la courbe |
| 71 | `5FzhCSWLT84QdgX9wYWWuWY1ZY3G9kMUu2fRifxLLhmx` | 187,9 | 187,9 | 4 004,32 | 4 192,2 | 32 282 | 551/431 | 0,00 | après Musk | 23/07 05:06:35 | 28/11 00:47:16 | partiel: jetons reçus sans coût |
| 72 | `HVEChdWCbP6nNVGtxquFXiCZ6HQSq4fsm5Lc3WbKRhXc` | 183,2 | 172,5 | 22,30 | 194,8 | 32 022 | 3/9 | 0,00 | avant visuel | 15/07 18:06:56 | 17/12 14:11:20 | partiel: jetons sortis hors swap |
| 73 | `65uKukVPZP3pNuoxuL2CLjpo6f7DcnTmUZNEbTCwNVP1` | 182,7 | 182,7 | 3,21 | 185,9 | 33 061 | 1/1 | 0,00 | avant visuel | 15/07 18:08:50 | 22/07 15:47:29 | complet sur le pool et la courbe |
| 74 | `JARVhtcGADkszZb91SAHQzxh2KrW7aRtZ8CA2FHDj6jF` | 181,5 | 181,5 | 30,50 | 212,0 | 31 433 | 8/20 | 0,00 | avant visuel | 14/07 02:19:12 | 13/08 00:57:02 | complet sur le pool et la courbe |
| 75 | `uaTvk1e3ftFToMZHByqgVhLjaTZQt2Wh47zpq4D183c` | 178,1 | 178,1 | 10,00 | 188,1 | 32 819 | 1/3 | 0,00 | avant visuel | 16/07 03:40:33 | 23/07 14:57:24 | complet sur le pool et la courbe |
| 76 | `5cWjvqwYbdiWCNcWbV71nZsM4KyfEnB3Cw1s7UEaftvJ` | 173,5 | 247,7 | 110,00 | 268,9 | 25 743 | 6/3 | 0,00 | avant visuel | 21/07 12:09:58 | 28/10 04:01:10 | partiel: positions de liquidité |
| 77 | `DP7RLhHXPeCjJ1zSYkSzDwALG7XpAyBo2KNBZzsEQXsr` | 173,0 | 173,0 | 204,05 | 377,1 | 27 189 | 14/10 | 0,00 | après Musk | 22/07 18:47:30 | 13/08 04:37:00 | complet sur le pool et la courbe |
| 78 | `7vPresTpJfJr3nmjxfDDmArqBkewAVM9kiPBSaxZ1asZ` | 173,0 | 173,0 | 60,86 | 233,8 | 30 504 | 1/1 | 0,00 | après Musk | 21/07 19:34:28 | 23/07 14:28:20 | complet sur le pool et la courbe |
| 79 | `Att5H7aB69u4cCS6Qe6pKiXAQ7mAeRtcUqkViuVwzm7h` | 171,4 | 171,4 | 83,22 | 254,7 | 25 183 | 9/29 | 0,00 | après Musk | 21/07 20:11:21 | 13/08 01:18:19 | complet sur le pool et la courbe |
| 80 | `2vJzVg42K1nz5J9t4irAe48jWJc3GHaGakpkpqBjFD66` | 169,0 | 36,4 | 90,00 | 169,0 | 14 030 | 2/8 | 0,00 | après Musk | 22/07 02:48:30 | 22/07 22:35:38 | partiel: positions de liquidité |
| 81 | `DcY85bX4LdqN8VZqbUkLu3cFhJoBwpmXiQBoJEsr4nvY` | 168,9 | 155,9 | 24,13 | 180,0 | 27 920 | 2/5 | 0,51 | avant visuel | 15/07 17:16:37 | 20/12 19:12:55 | complet sur le pool et la courbe |
| 82 | `FXzcpJSkuvjMoQRh7a1bf7LXVhrm3kiXQWsuFD6b5goJ` | 165,7 | 165,7 | 13,00 | 178,7 | 29 954 | 4/8 | 0,00 | avant visuel | 14/07 03:45:23 | 31/07 00:08:44 | complet sur le pool et la courbe |
| 83 | `AHZsyBU3eDcZvahiTnijig6hEYwhDz4cGNpcKJn7tEju` | 162,6 | 162,6 | 190,00 | 352,6 | 29 674 | 51/4 | 0,00 | après Musk | 26/07 22:06:50 | 27/07 20:13:07 | complet sur le pool et la courbe |
| 84 | `4yDTSAH4hspmAQyp9xoxZQQDCRgYn6RF2DtYVttdcsBR` | 162,4 | 162,4 | 237,60 | 400,0 | 28 699 | 11/19 | 0,00 | après Musk | 22/07 00:00:45 | 22/07 04:24:18 | complet sur le pool et la courbe |
| 85 | `C4KV1Q5vhshFZKYF5nhSWH17qLivMYA69Xi25PauZ2J2` | 161,0 | -1,059.6 | 975,00 | 161,0 | -146,334 | 11/11 | 0,00 | après Musk | 22/07 06:19:52 | 23/07 16:26:27 | partiel: positions de liquidité |
| 86 | `3ffix9bwCn7Yyi6d6ygA3VVfEWdYMdaFDUWpNh8Fy1A8` | 160,5 | 160,5 | 86,00 | 246,5 | 29 217 | 7/8 | 0,00 | après Musk | 21/07 19:36:02 | 14/08 05:34:31 | complet sur le pool et la courbe |
| 87 | `6Jzx6jKZaYnKT5qgJZSHknfsnKm3P1MfU8XjqD7WTBuw` | 160,3 | 251,2 | 45,00 | 205,3 | 28 836 | 5/15 | 0,00 | après Musk | 21/07 23:33:38 | 25/07 15:26:58 | partiel: positions de liquidité |
| 88 | `Bsco8UvQrPTraZyNQUE7166fTSk5aytfTa24HePrNVrp` | 160,2 | 160,2 | 283,00 | 443,2 | 27 081 | 2/1 | 0,00 | après Musk | 21/07 23:48:24 | 22/07 08:23:59 | complet sur le pool et la courbe |
| 89 | `EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy` | 158,8 | 158,8 | 7,39 | 166,2 | 28 238 | 4/4 | 0,00 | avant visuel | 14/07 02:09:34 | 27/09 19:51:02 | partiel: jetons sortis hors swap |
| 90 | `2cxjRs8bt5EBxbcSJkY1AXLX5UCYq23pWn83EckDMdCv` | 154,6 | 154,6 | 247,50 | 402,1 | 29 057 | 12/17 | 0,00 | avant visuel | 15/07 16:56:23 | 22/07 03:53:05 | complet sur le pool et la courbe |
| 91 | `Fcrb13c591razQWyhrwYmPZR3CJPN8u8Fo1Hyd25fyha` | 153,6 | 153,6 | 117,38 | 271,0 | 24 817 | 6/51 | 0,00 | après Musk | 23/10 21:02:55 | 06/11 00:38:03 | complet sur le pool et la courbe |
| 92 | `AQwdk9o33dusTLbZB4CtcAqii8uj9QFVmtjEGxmSKpvP` | 152,1 | 152,1 | 282,15 | 434,2 | 25 472 | 16/31 | 0,00 | après Musk | 05/11 23:53:38 | 02/02 04:48:06 | complet sur le pool et la courbe |
| 93 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 148,5 | 134,5 | 19,80 | 154,3 | 23 775 | 12/54 | 0,00 | avant visuel | 14/07 02:07:26 | 14/05 17:48:31 | partiel: jetons reçus sans coût |
| 94 | `CQQqZgro3PwGgD23vtWCeneQzVBYQ9Yn4bqBdyYpYeDR` | 143,0 | 143,0 | 32,81 | 175,8 | 25 702 | 9/7 | 0,00 | après Musk | 21/07 19:35:54 | 30/07 01:06:22 | complet sur le pool et la courbe |
| 95 | `DMAUfa1LsBV1bqgmZifPY3Rdma2ud3X9PLGSYinWgdAt` | 142,8 | 142,8 | 2,00 | 144,8 | 26 326 | 1/35 | 0,00 | avant visuel | 18/07 06:47:11 | 23/07 14:34:11 | complet sur le pool et la courbe |
| 96 | `8W23ydHZTkrjV7ZKGLvaFAK2DuJDquvp9zj2jg7DGk5S` | 140,2 | 140,2 | 70,83 | 211,0 | 25 471 | 3/12 | 0,00 | après Musk | 21/07 19:46:58 | 31/07 21:55:39 | complet sur le pool et la courbe |
| 97 | `49boQDhjNSLUyRyDMZpiDuZLWYCNeJpgV9jrLQfh8LPX` | 140,0 | 140,0 | 14,85 | 154,9 | 25 467 | 5/16 | 0,00 | avant visuel | 21/07 13:21:25 | 06/11 07:18:02 | complet sur le pool et la courbe |
| 98 | `BmanDqQELF7QY5uRPw8vg3eMjR74WZnszKmNbLJKkay3` | 139,2 | 139,2 | 12 869,29 | 13 008,5 | 22 581 | 628/695 | 0,00 | après Musk | 11/08 20:22:33 | 04/03 20:11:56 | complet sur le pool et la courbe |
| 99 | `7MVEWuwpVoELMose1KnwF6a66mKCavJaBeFUdL2YgCXz` | 137,6 | 137,6 | 126,00 | 263,6 | 24 332 | 9/17 | 0,00 | après Musk | 21/07 22:40:32 | 23/07 05:24:28 | complet sur le pool et la courbe |
| 100 | `C2LDog5ENFm4NYJzxb7gQuZDhsuCdjXin61sGkBoA48t` | 137,0 | 137,0 | 9,90 | 146,9 | 25 031 | 5/20 | 0,00 | avant visuel | 15/07 18:35:52 | 03/06 21:50:39 | complet sur le pool et la courbe |

## Plus gros vendeurs dont le coût n'est pas connu : aucun gain ne peut être affirmé
Leur stock vient de transferts sans prix. Cas typique : `GCvHhEUYQwTJ8jyf8Lc4bv8jBXyZU4LMMsZCobwEPzvM` et `Gtf4RWqjHhkoio55QkkYM7K3vP4BAT3eSUYPwSZKk8Wi` reçoivent leur stock de `3eGdjMdQqFUNc4G64BZb7YCALDEaturLUWcixjJfKxEh`, un hub actif depuis 2023 avec plus de 200 adresses entrantes, puis vendent sur Raydium à partir d'août 2024. Comportement compatible avec un arbitrage entre un échange et le pool ; non attribué.

| # | Wallet | SOL reçu aux ventes | Vendu M | Vendu sans quantité M | Reçu par transfert M | Acheté SOL | Ventes | 1re vente | Dernière vente |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `GCvHhEUYQwTJ8jyf8Lc4bv8jBXyZU4LMMsZCobwEPzvM` | 8 181,7 | 478,4 | 74,1 | 410,4 | 0,0 | 3312 | 04/08 13:42:22 | 01/02 14:46:16 |
| 2 | `Gtf4RWqjHhkoio55QkkYM7K3vP4BAT3eSUYPwSZKk8Wi` | 4 489,9 | 141,9 | 0,0 | 142,0 | 0,0 | 2677 | 22/07 13:03:44 | 04/01 06:00:09 |
| 3 | `CnZzdTH1e6ZT3mtgaXqggexCWfubm375UMuFpAycDd1r` | 2 662,0 | 88,0 | 0,0 | 7,6 | 2 655,4 | 18326 | 21/07 23:07:26 | 25/10 10:42:51 |
| 4 | `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS` | 2 433,6 | 38,2 | 0,0 | 22,9 | 1 199,0 | 490 | 14/07 02:32:39 | 19/11 00:56:18 |
| 5 | `2V3Kt8V4j3CJRcsXkRwRMdkZk1YvV6tLYS1AcfNFJFvc` | 1 980,9 | 24,6 | 0,0 | 4,0 | 1 343,7 | 40 | 22/07 10:04:02 | 06/11 04:21:15 |
| 6 | `7cPoMtk448csbdk9fcTeEcU22qiLCR9kcMjSLrqC4ygZ` | 1 971,3 | 60,1 | 0,0 | 9,8 | 1 903,5 | 95 | 15/07 17:02:04 | 06/11 00:45:36 |
| 7 | `ERjCjBRinnL5zGgURC2DneErtqzojV7oNHhqiGnHcXW1` | 1 785,4 | 12,2 | 0,0 | 8,9 | 534,9 | 9 | 21/07 20:26:43 | 23/07 14:26:43 |
| 8 | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 1 691,5 | 28,1 | 0,0 | 23,6 | 5,5 | 74 | 15/07 17:05:40 | 04/10 14:53:03 |
| 9 | `CKBCxNxdsfZwTwKYHQmBs7J8zpPjCjMJAxcxoBUwExw6` | 1 494,9 | 269,8 | 0,5 | 283,4 | 878,4 | 1167 | 03/12 15:16:32 | 17/01 18:24:10 |
| 10 | `55jmAu4vsxdtfACbZMhbbD6chZQLeysgpuigKHzZZVqr` | 1 376,8 | 31,9 | 0,0 | 5,4 | 1 474,5 | 180 | 23/07 15:13:19 | 29/09 10:02:08 |
| 11 | `D12r2UMT4yEhQca9p5aJeKMZYoerpaXEPT4zNTxSQ5ir` | 1 243,5 | 39,7 | 0,0 | 20,5 | 1 081,5 | 555 | 15/07 17:10:08 | 14/03 16:28:50 |
| 12 | `8Y5MBFF1ywWa2u9GyTmoqG7BC7VLSk66JDCVmZH5EFVV` | 1 223,2 | 20,3 | 0,0 | 25,7 | 1 005,3 | 91 | 08/08 18:02:44 | 17/10 08:02:41 |
| 13 | `FgXrfMULZgycE8e2VxdKgNgtMwkmArkY7WxG2rbZbLhj` | 1 183,4 | 4,3 | 0,0 | 2,9 | 200,0 | 21 | 22/07 05:15:12 | 23/07 05:27:16 |
| 14 | `63D3AGXFNq63xx8ZczhHVnZgqMv1icv4M5GPF8nPpv7H` | 1 135,3 | 5,0 | 0,0 | 8,0 | 295,0 | 15 | 23/07 05:02:08 | 23/07 05:11:50 |
| 15 | `GM4UPhkM51URjXRkSbBTV5DaNsPxNZq8KaJab2Fg5xS1` | 1 116,1 | 30,6 | 0,0 | 25,5 | 971,0 | 52 | 19/08 17:58:38 | 30/10 13:03:18 |
| 16 | `F9HrC8S68AnnVpF26JGkxfMxw3EiG8PN23YQGpyzvR5t` | 1 065,8 | 20,1 | 0,0 | 6,6 | 438,7 | 79 | 22/07 03:10:40 | 02/11 15:03:11 |
| 17 | `GPiP7Ak94JF8NW352yRAtNWxSKCfiQHZwnRimGwRYFse` | 959,1 | 2,5 | 0,0 | 2,5 | 0,0 | 41 | 22/07 06:38:42 | 22/07 09:55:48 |
| 18 | `FTV3gs23xuk72Y8vFZ8fxFBrRPg6Ld7mSMFfY4HyZMYu` | 942,9 | 10,7 | 0,0 | 4,0 | 226,1 | 10 | 21/07 20:24:49 | 19/08 20:38:14 |
| 19 | `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 929,8 | 10,1 | 0,0 | 20,1 | 248,0 | 37 | 21/07 22:30:00 | 31/07 22:59:48 |
| 20 | `DswkYbBhV9MKWhymaawezWEEZoWPV1az79wcm1J644na` | 922,0 | 12,4 | 0,0 | 10,8 | 878,8 | 50 | 02/08 17:00:06 | 12/08 00:07:11 |
| 21 | `JCDpQ6m7mb5n2bUSQ3GQpVLxVsZtRUHhmvRXeE2Gg1rn` | 869,5 | 12,2 | 0,0 | 5,0 | 202,0 | 96 | 15/07 17:01:39 | 29/07 15:27:44 |
| 22 | `63A99xoxxUVBm8VUguBcJZbYWDLi9AjYvYtB16xWqCzw` | 845,4 | 27,3 | 0,0 | 10,0 | 1 200,0 | 17 | 10/10 18:03:05 | 23/10 20:58:58 |
| 23 | `H4Y7WByTJPwEm25A7S31WcsTu5unhY3x2WJfgvjTbsia` | 830,1 | 17,8 | 0,0 | 1,5 | 872,6 | 571 | 22/07 15:22:23 | 10/02 02:13:51 |
| 24 | `3Sa8PwzwHgd5wy4opAxf6fAfawfFjHCVb6bqXb1FVfr5` | 825,8 | 15,2 | 0,0 | 3,7 | 863,8 | 41 | 23/07 06:09:23 | 07/10 17:59:26 |
| 25 | `2mvZRMsoSciXaLeYfQpFk1TtHMvyfKpfgF8ao8c1T9Wi` | 808,4 | 16,2 | 0,0 | 2,4 | 1 027,4 | 41 | 23/07 04:34:00 | 08/10 09:16:49 |
| 26 | `DdqzapetQXM2zX5XmijChfX7vUELx5EVs4u336pY9NVU` | 801,2 | 13,0 | 0,0 | 4,1 | 779,3 | 18 | 08/10 04:29:49 | 06/11 00:04:24 |
| 27 | `FZLmLkf93NPU44zwCTcrRwYfFfx4orZN2cqdUSufft8i` | 800,3 | 4,4 | 0,0 | 5,5 | 4,2 | 31 | 21/07 22:30:43 | 10/08 16:19:50 |
| 28 | `9SQA7PSu8dyHnnLrsExRrwoX19SUDENgZeoJoNTUbj46` | 780,8 | 2,3 | 0,0 | 4,7 | 1 126,6 | 20 | 22/07 12:19:01 | 22/07 12:24:10 |
| 29 | `HGh5acuYdhoBBJxUuLyW1weAcp6H8ck49nkwAP3kT1yG` | 758,1 | 12,8 | 0,0 | 1,3 | 771,8 | 39 | 23/07 17:35:59 | 16/08 17:39:15 |
| 30 | `2PF9meafUQg5sCaohLhqt8hdQQmmNeQ21SkcWMsrF7yE` | 741,9 | 1,9 | 0,0 | 1,9 | 0,0 | 49 | 22/07 03:49:33 | 22/07 04:43:56 |
| 31 | `HRRq3jAZ2jeWEudg9scS1n42NYAkqEiTygjsMBGn9CqU` | 735,8 | 12,7 | 0,0 | 18,1 | 439,9 | 206 | 15/07 15:50:18 | 16/04 10:24:36 |
| 32 | `BfkBxeDE29dnFP4ptpEHhQWGL9xMu9LYv7hbUAmzU667` | 725,7 | 10,9 | 0,0 | 3,1 | 294,2 | 8 | 22/07 03:02:17 | 13/09 17:57:00 |
| 33 | `6HP8MZ7qHG4pVhEaBo85SkSAKZmLt6ufow5orah9Cddq` | 688,5 | 14,2 | 0,0 | 8,1 | 655,9 | 97 | 24/07 19:06:29 | 05/10 14:44:29 |
| 34 | `GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y` | 686,9 | 29,3 | 0,0 | 32,3 | 0,0 | 2 | 23/07 17:30:22 | 26/07 05:48:58 |
| 35 | `3fz8i7d4YJd6JNi1Nn96c1M4mHa2kmH8YFFXo5xfJ5yg` | 678,1 | 15,6 | 0,0 | 4,1 | 414,2 | 29 | 17/07 02:15:17 | 16/02 05:50:47 |
| 36 | `75fXGTvc8BHKBXwNfqriso6dzLe52qMUzvGPu9DV8fog` | 677,9 | 10,1 | 0,0 | 4,1 | 519,9 | 123 | 15/07 19:36:52 | 21/02 15:17:00 |
| 37 | `FMbfmHxYGECZAoNA7LdXa5dN9rKTKgeiyzdrVh7egrym` | 667,7 | 12,3 | 0,0 | 8,1 | 492,8 | 59 | 24/07 23:22:20 | 28/10 23:36:25 |
| 38 | `AYrXz7yZ3PuC73Rxx4u9QAcW3qQgZYLXjtBAcU7gDjX5` | 648,7 | 13,9 | 0,0 | 1,8 | 761,9 | 22 | 23/07 15:24:24 | 07/10 14:57:02 |
| 39 | `CLegS2MSiCsBksVazCg4Y7Gz3NqeBK21QyvzK4Q7S168` | 638,9 | 6,3 | 0,0 | 4,1 | 138,6 | 8 | 21/07 23:48:31 | 05/08 00:55:14 |
| 40 | `Ao3Fcz11pHnN3WMgKxyi1HZqgg6DBWsSHjKQUfpyUtV6` | 597,4 | 13,6 | 0,0 | 8,7 | 1 028,0 | 14 | 27/07 23:11:26 | 17/10 09:54:09 |

## 100 plus gros acheteurs (SOL engagé)
| # | Wallet | Acheté SOL | Coût USD | Achats | Réalisé SOL | Flux net SOL | Cohorte |
|---|---|---|---|---|---|---|---|
| 1 | `5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx` | 32 832,7 | 5 566 546 | 1053 | 489,6 | 489,6 | avant visuel |
| 2 | `AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS` | 16 739,8 | 2 853 290 | 736 | 273,6 | 273,6 | avant visuel |
| 3 | `BmanDqQELF7QY5uRPw8vg3eMjR74WZnszKmNbLJKkay3` | 12 869,3 | 2 166 573 | 628 | 139,2 | 139,2 | après Musk |
| 4 | `D4zVhwuUsFbcaty7wJhNEZ7VEwPHXQ5d2heXPxM5yWhL` | 10 510,1 | 1 721 739 | 1188 | 127,4 | 126,9 | après Musk |
| 5 | `4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S` | 9 986,8 | 1 767 204 | 948 | 268,4 | 259,6 | avant visuel |
| 6 | `8aHVf4T3t4Z2kjnNojLh87zswhH21EU2iFnVoadN3MXx` | 6 270,7 | 1 113 133 | 409 | 74,3 | 74,3 | après Musk |
| 7 | `Bya5eBy9KgqaXfnLKuvFYBaqzYqxip3JVimhtToKRxLp` | 4 588,9 | 780 620 | 5211 | 0,0 | -4,588.9 | après Musk |
| 8 | `5FzhCSWLT84QdgX9wYWWuWY1ZY3G9kMUu2fRifxLLhmx` | 4 004,3 | 679 209 | 551 | 187,9 | 187,9 | après Musk |
| 9 | `6Tt9iP2YacNi8om4qwwuTsWtrEqsftvoqaG57QqdS3GF` | 3 886,3 | 618 831 | 7155 | -2.4 | -3,886.2 | après Musk |
| 10 | `6bKNmmyckNZNtcgPbxZU9arsQwGEFosvZtLGsXixhxED` | 3 341,5 | 590 467 | 51 | -808.2 | -808.2 | avant visuel |
| 11 | `7gEQ6syDZmyPE4JdfJm4qatawnDqvqdh6i8jJjCXio6h` | 2 872,5 | 468 726 | 8778 | -5.9 | -2,871.8 | après Musk |
| 12 | `ErP2uLSVN2p17d4VPJzGWb9U88tNrSCDdP3rm4C9KTyW` | 2 732,4 | 493 273 | 266 | 122,7 | 122,7 | avant visuel |
| 13 | `CnZzdTH1e6ZT3mtgaXqggexCWfubm375UMuFpAycDd1r` | 2 655,4 | 397 636 | 17705 | 473,3 | 7,3 | après Musk |
| 14 | `AtTjQKXo1CYTa2MuxPARtr382ZyhPU5YX4wMMpvaa1oy` | 2 476,7 | 524 022 | 98 | 26,3 | 26,3 | après Musk |
| 15 | `G11LHDyKR4RiyL4Fq4sDFsMTMTHDsHC35YTn7rDueYuq` | 2 429,1 | 379 866 | 56 | -114.7 | -114.7 | après Musk |
| 16 | `CPUvH6fYkpYBK5raccquTMNJAGc6eQ37VVqBgHq3hwjp` | 2 218,7 | 368 699 | 85 | 0,6 | 0,6 | avant visuel |
| 17 | `BfkNvWDMwM46uQ2WYCr7xGzmtCtH39zf48NKJ5ozCNn9` | 2 030,0 | 366 700 | 79 | 0,0 | -2,030.0 | après Musk |
| 18 | `7cPoMtk448csbdk9fcTeEcU22qiLCR9kcMjSLrqC4ygZ` | 1 903,5 | 292 081 | 102 | 495,9 | 67,8 | avant visuel |
| 19 | `EkBN5xbXB64tPdK1s65bkkSbw1RjS3rjuvLxvyWthUVk` | 1 676,6 | 270 902 | 202 | 16,3 | -2.9 | après Musk |
| 20 | `7fcPCcbeR9kGnwkZXxGkYrceruS666PruaACzcBfH9gb` | 1 641,5 | 298 656 | 99 | 17,4 | 17,4 | après Musk |
| 21 | `E4tnUjHy7RAkK9dRyg2uawPhR2d1zG1kPm67FKk52ZJv` | 1 603,0 | 287 016 | 16 | -650.0 | -650.0 | après Musk |
| 22 | `E1okLxi6D9LdYcKKwrafSXB2MEsxtKJWp2p6vKuEugPo` | 1 602,9 | 307 833 | 35 | -673.6 | -673.6 | après Musk |
| 23 | `5y8PN2FuT3rt9ML5Y2j6TpaoB7G7FCcJJSBh58EqGHxi` | 1 593,0 | 250 804 | 468 | 44,9 | 44,9 | après Musk |
| 24 | `C5UEc3UCcwnjEjNqmFz9YGFmA6z5BYr3XFcQM9sKwcs8` | 1 515,0 | 277 532 | 106 | 7,2 | 7,2 | après Musk |
| 25 | `4SZG7mj4ufaki3FTd65aAqt8ZmGWeubuXUnmWLz564ut` | 1 514,0 | 231 707 | 57 | 460,9 | 432,1 | après Musk |
| 26 | `55jmAu4vsxdtfACbZMhbbD6chZQLeysgpuigKHzZZVqr` | 1 474,5 | 226 464 | 313 | 246,0 | -97.6 | après Musk |
| 27 | `hnu5iBK8UoHb51UFsH1RYTUAYdrhjHvV5YMTf9T1CYN` | 1 388,6 | 240 862 | 241 | 6,7 | 6,7 | après Musk |
| 28 | `6iKmev4X51r5rQ5Eo2BpG3egJh9JCQ3pk2azVTUxCLR7` | 1 357,0 | 246 234 | 36 | -958.8 | -958.8 | après Musk |
| 29 | `32kF3rvA6NpA8ZFam2mpca6axLKpggQ6XGq1y7pssPvJ` | 1 353,2 | 239 394 | 17 | -480.1 | -527.1 | après Musk |
| 30 | `2V3Kt8V4j3CJRcsXkRwRMdkZk1YvV6tLYS1AcfNFJFvc` | 1 343,7 | 226 258 | 191 | 914,1 | 637,2 | après Musk |
| 31 | `H4uHhYkos7z2gJTQpmd2xVRDeRrSxwat2uqpguoNVv7h` | 1 336,4 | 238 707 | 297 | -141.0 | -141.3 | après Musk |
| 32 | `2VuEndiRaXwTi7zF2p9CkV4Kgn8y9kdcZqHLJLebS8uF` | 1 316,4 | 233 383 | 53 | -29.2 | -29.2 | après Musk |
| 33 | `8zFZHuSRuDpuAR7J6FzwyF3vKNx4CVW3DFHJerQhc7Zd` | 1 287,0 | 228 076 | 25 | -1,100.1 | -1,100.1 | avant visuel |
| 34 | `3eJkwFDZVB27emciij1oWUVodmFhFdnkpmzKHjDzH34o` | 1 264,9 | 206 277 | 224 | 31,9 | 31,9 | avant visuel |
| 35 | `9utpET26mRofwVaeL7y1qpmDTSs3VbDfNXFjfXWk92Rc` | 1 252,1 | 200 499 | 409 | 11,7 | 11,7 | après Musk |
| 36 | `BHCm58VsiSq9p3hqjprLAs6wtjXjtuGnz6vj1i3Upe7X` | 1 220,0 | 213 919 | 18 | -476.0 | -476.0 | après Musk |
| 37 | `63A99xoxxUVBm8VUguBcJZbYWDLi9AjYvYtB16xWqCzw` | 1 200,0 | 171 780 | 6 | 84,7 | -354.6 | après Musk |
| 38 | `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS` | 1 199,0 | 213 852 | 266 | 1 435,9 | 1 234,6 | avant visuel |
| 39 | `7uRDe43iDncwEESfHvyxqYw3tzaVZgvCQn67x3xYyQeY` | 1 190,4 | 213 364 | 3 | 556,4 | -338.7 | après Musk |
| 40 | `CH7MJuK5Kh2e7cribybdQLPzSxLqL4AgWwKZgaNoHA7J` | 1 180,6 | 258 960 | 104 | 8,6 | 8,6 | après Musk |
| 41 | `9SQA7PSu8dyHnnLrsExRrwoX19SUDENgZeoJoNTUbj46` | 1 126,6 | 201 025 | 30 | 780,8 | -345.8 | après Musk |
| 42 | `6zrQ5r6k2qrvuKDvzj6XhG8okx4cGzwtFS6WVmvQCZAo` | 1 114,6 | 208 826 | 213 | -82.3 | -95.1 | après Musk |
| 43 | `DZzbus8RDN6MVrfeDYhbfnQW91WTeVR4QufnXng35rQx` | 1 105,6 | 200 965 | 103 | -32.9 | -73.8 | après Musk |
| 44 | `APXdahWMvNUUBYqgZDoWEgcFce7xoWUkZuDKJNTRhWFB` | 1 099,0 | 184 436 | 33 | 2,1 | 2,1 | après Musk |
| 45 | `94cW9n4vXENhDnzKCpXMFwxP9czqQmeLDzRKYZTXhW6s` | 1 098,3 | 169 290 | 184 | 264,4 | -698.1 | après Musk |
| 46 | `BuFVTfkT3BjocQY7JCJePffG3nPBuM7iY4Aca8NpUzh8` | 1 093,6 | 171 763 | 55 | -45.0 | -104.6 | après Musk |
| 47 | `5xyUFj7a8sP9y7DS93MnVvAfBAW3Sq3hbcfyuhyawSD9` | 1 081,6 | 187 702 | 1115 | 145,9 | -808.3 | avant visuel |
| 48 | `D12r2UMT4yEhQca9p5aJeKMZYoerpaXEPT4zNTxSQ5ir` | 1 081,5 | 201 540 | 336 | 830,2 | 162,0 | avant visuel |
| 49 | `6CirGdBKT2pSZE45oMSwi8UreoYjyaBgmxE92cpMWQGv` | 1 037,0 | 185 937 | 9 | -511.9 | -511.9 | après Musk |
| 50 | `7T3hQdqWPZwNpYoJiFy6qac3kATZLRbVvr2FfXkgPHJU` | 1 030,8 | 162 336 | 79 | -6.2 | -6.2 | après Musk |
| 51 | `CvoFixYaRKMny1DeecfXCkbiAJe8cLSc4vT5z2UcarnP` | 1 029,6 | 183 826 | 22 | -496.3 | -496.3 | après Musk |
| 52 | `Ao3Fcz11pHnN3WMgKxyi1HZqgg6DBWsSHjKQUfpyUtV6` | 1 028,0 | 153 703 | 28 | 400,1 | -430.6 | après Musk |
| 53 | `2mvZRMsoSciXaLeYfQpFk1TtHMvyfKpfgF8ao8c1T9Wi` | 1 027,4 | 161 324 | 392 | 10,1 | -94.6 | après Musk |
| 54 | `4AVe3VMDWnfwxo3Ydi4N8m411TvPwe3BjXmPnRg4GU4a` | 1 017,5 | 148 602 | 19 | 0,2 | 0,2 | avant visuel |
| 55 | `8Y5MBFF1ywWa2u9GyTmoqG7BC7VLSk66JDCVmZH5EFVV` | 1 005,3 | 151 073 | 80 | 847,2 | 217,9 | après Musk |
| 56 | `7FHsHvHy6BXeiwX35pZFz2dWQbyNbHvuGuGsrkRn8Ca5` | 1 000,0 | 173 325 | 2 | -681.5 | -681.5 | après Musk |
| 57 | `X7n7WXZz714vaYcnGs5nffsiMLkthoqouMcAL1kAsyn` | 994,2 | 177 832 | 25 | 338,5 | -465.7 | après Musk |
| 58 | `7HGwBPjoGBqHnSPqv2JF9QnySKuojmUKgH8hiHYGesQA` | 993,0 | 172 707 | 20 | -271.2 | -271.2 | après Musk |
| 59 | `4URH6BFKDzieB6fpCpDjbxMjMdCXgGqW6XMbAreDMk47` | 990,0 | 179 289 | 33 | 41,0 | 41,0 | après Musk |
| 60 | `TRxDrc58zVhiF4L7usEgAYAMkavWoVcgy97E6xAedes` | 975,7 | 158 178 | 33 | 39,5 | 39,5 | après Musk |
| 61 | `5MfLoKjCPkULUTas7Li79vtq7BafYsR5f3vw3cNxp1mS` | 975,0 | 206 432 | 66 | -94.9 | -94.9 | après Musk |
| 62 | `C4KV1Q5vhshFZKYF5nhSWH17qLivMYA69Xi25PauZ2J2` | 975,0 | 174 841 | 11 | 161,0 | -1,059.6 | après Musk |
| 63 | `GM4UPhkM51URjXRkSbBTV5DaNsPxNZq8KaJab2Fg5xS1` | 971,0 | 150 665 | 24 | 671,4 | 145,1 | après Musk |
| 64 | `BjcHe1tZqcJ93RekSEks4hqY81Gx7qWTcZNvc76teXfM` | 961,6 | 162 770 | 54 | -166.2 | -177.1 | après Musk |
| 65 | `FTnNcCHtCsjHgGoFw1D4dEUMe94SQkM23BQ9JSATXDV` | 951,9 | 162 547 | 1709 | 49,2 | -855.8 | avant visuel |
| 66 | `Hic9ZRfeCnmAxCjXjihFRo59ge3LVKixJ5iRsYT9ZzVa` | 946,5 | 142 835 | 49 | 113,9 | 113,9 | après Musk |
| 67 | `71CPXu3TvH3iUKaY1bNkAAow24k6tjH473SsKprQBABC` | 946,0 | 166 867 | 44 | 266,1 | 266,1 | après Musk |
| 68 | `425DZohsnqJjyMtMe2XfHsEuiAf9xBRAqsGSGsH8PKdc` | 926,1 | 199 166 | 2220 | 98,6 | 66,0 | après Musk |
| 69 | `G1Q7A8kWoruNm81bWHQuRmQi8rLnHX5bT1oDwTvzWYMy` | 924,6 | 163 190 | 10 | -94.1 | -94.1 | après Musk |
| 70 | `B5QzGuMknM2jTwUPzTBL4SbV6Zta6VAGMpTADCkbiwAq` | 905,0 | 149 973 | 22 | 25,3 | 25,3 | après Musk |
| 71 | `8DBMRQq11VuXxUyxacPqgtkNRyRxRN7BzDSyqnBsBNew` | 900,0 | 164 937 | 63 | 3,8 | 3,8 | après Musk |
| 72 | `A6fykdwWidpRMUndqPF975mQWfgMSTRJ984GNELhRhCi` | 889,0 | 165 552 | 38 | -502.6 | -502.6 | après Musk |
| 73 | `56hsftf9ZEDREubqk47pD1sz6aNKzVE1h52Uk3Ppwzqx` | 885,7 | 147 974 | 246 | 50,9 | 50,9 | après Musk |
| 74 | `DswkYbBhV9MKWhymaawezWEEZoWPV1az79wcm1J644na` | 878,8 | 132 194 | 12 | 93,6 | 43,2 | après Musk |
| 75 | `CKBCxNxdsfZwTwKYHQmBs7J8zpPjCjMJAxcxoBUwExw6` | 878,4 | 167 453 | 1686 | 1 413,1 | 616,5 | après Musk |
| 76 | `H4Y7WByTJPwEm25A7S31WcsTu5unhY3x2WJfgvjTbsia` | 872,6 | 129 104 | 1673 | 26,2 | -42.5 | après Musk |
| 77 | `3Sa8PwzwHgd5wy4opAxf6fAfawfFjHCVb6bqXb1FVfr5` | 863,8 | 129 734 | 107 | 182,0 | -38.1 | après Musk |
| 78 | `CquphN7FNEj4PTGugmuvzVwhjUV5srUk9J9XEhJNpUvk` | 861,3 | 157 398 | 30 | 126,6 | 126,6 | après Musk |
| 79 | `4FaACTjBtk2mFe5PNvdDknamvkk996WeUSomvtjPTQbz` | 853,8 | 153 566 | 73 | -12.2 | -792.4 | après Musk |
| 80 | `6i2xuLFm5Nww3tfP5ouxXXEJ9mvH8kfTVT7a7qjg4UwR` | 850,8 | 172 657 | 100 | -91.3 | -91.3 | après Musk |
| 81 | `5fU83xwyB78A7ozDtVUn6Y7okfcATzv9BkSourayEhgD` | 847,0 | 146 058 | 14 | 126,8 | -369.4 | après Musk |
| 82 | `cJTLFVgwumqJh2QQYrZvdUJmkCnj7pFM9CmtaeFasHA` | 840,7 | 152 536 | 17 | -15.5 | -15.5 | après Musk |
| 83 | `BW4oXEu4syZsS4U5HeUXjeG2uQJEA49zp5ByYTR7hywp` | 839,4 | 146 871 | 11 | -298.9 | -298.9 | après Musk |
| 84 | `E3Btto2Md2KujnL3bzu1e94D6fuwhyo3eDRa1rgtffSC` | 820,0 | 147 345 | 19 | -52.8 | -52.8 | avant visuel |
| 85 | `3meDSsXbxUYNtbS887A4YdZqDQVnQAdcHQkb77sbTMCu` | 800,0 | 146 634 | 56 | 2,3 | 2,3 | après Musk |
| 86 | `ACgGWUySLSudRFPdfVe1R5i4m1j6M3ovb42oF7hcL8Ud` | 799,2 | 145 860 | 6 | -528.5 | -528.5 | après Musk |
| 87 | `BDFMkurHjWM8HCibLRncxaSF8eQ3oJJztPSr4jUEo3nZ` | 795,6 | 136 225 | 102 | 21,3 | 21,3 | avant visuel |
| 88 | `7H3bQRRCPjUyDt2i6wqLyWhjLQWUWPfHQjC2guRkb8Vu` | 792,0 | 116 199 | 90 | 301,6 | 299,2 | après Musk |
| 89 | `CbkM2ru4VLLkuErVji9TyT5RDKoYeaNGvWhSdRWnoiDf` | 788,0 | 114 524 | 124 | 27,0 | 27,0 | après Musk |
| 90 | `DdqzapetQXM2zX5XmijChfX7vUELx5EVs4u336pY9NVU` | 779,3 | 118 800 | 21 | 194,4 | 21,8 | après Musk |
| 91 | `8B5ekuLtBXypSiGq8xugLtk5UHq4JiW2U3haYJPi3u7p` | 778,5 | 123 460 | 40 | -171.8 | -418.4 | après Musk |
| 92 | `Haee7H5bKDCnm6dXLkeR9DcWw9Puhnkwk71QBUSHcpUt` | 777,0 | 141 546 | 1 | -656.8 | -656.8 | après Musk |
| 93 | `HGh5acuYdhoBBJxUuLyW1weAcp6H8ck49nkwAP3kT1yG` | 771,8 | 121 075 | 43 | 3,2 | -13.6 | après Musk |
| 94 | `AYrXz7yZ3PuC73Rxx4u9QAcW3qQgZYLXjtBAcU7gDjX5` | 761,9 | 128 947 | 35 | 2,6 | -113.1 | après Musk |
| 95 | `AJxeihsujZjZVfAda3d7AyqQWZ9fdb5etiPASnrMZhX2` | 757,8 | 137 157 | 17 | -579.9 | -579.9 | après Musk |
| 96 | `7sUKVgYPcdAghuDQYR4qdzt7qZRLn3HeSoyTxh6tYCEJ` | 749,2 | 112 193 | 58 | -44.8 | -48.1 | après Musk |
| 97 | `GmibrdRC6WjajT7t5sTsFVmnwy5rEYKBdeQqfctoR4F` | 747,0 | 166 852 | 132 | -38.8 | -41.1 | après Musk |
| 98 | `8S9fHNjW1wDUodFmX41mkG2mjf8hzbfg1fpbbyypqi5m` | 738,3 | 108 787 | 95 | 33,3 | -6.7 | après Musk |
| 99 | `BgrBGqmUZzFCJ4bceCUwhykn1c6vU7JatwW2k62GMN27` | 735,8 | 115 608 | 198 | 5,3 | 1,3 | après Musk |
| 100 | `Ct6SP2E3ckCGUCDzjAfgVR5SRbwdG6vcAydNVdMXMi3Q` | 732,4 | 129 233 | 211 | 371,9 | -197.5 | avant visuel |

## 25 plus gros résiduels
| # | Wallet | Jetons M | Valeur SOL au dernier prix | Acheté SOL | Réalisé SOL | Cohorte |
|---|---|---|---|---|---|---|
| 1 | `7gEQ6syDZmyPE4JdfJm4qatawnDqvqdh6i8jJjCXio6h` | 122,28 | 83,9 | 2 872,51 | -5.9 | après Musk |
| 2 | `HGs9NdwD2c4mYHb9fYdgp2Due5gbaSEdUV871wAiCkTd` | 34,35 | 23,6 | 0,00 | 0,0 | aucun achat |
| 3 | `GWRC1i1XhmM8kNpgFno8BZpYWuY9Ae8DbLvf8PNjW2cW` | 20,00 | 13,7 | 76,58 | -10.6 | après Musk |
| 4 | `EL14tsaYVWKk6d2PAZkHawrP9XBVtvNkvGEDKpo2m6Jh` | 19,34 | 13,3 | 46,45 | 0,0 | après Musk |
| 5 | `HvhFFm5SvZyyAsCdGpScwKFQAhQopxc6v8MKMTg2iq86` | 18,96 | 13,0 | 18,29 | 0,0 | après Musk |
| 6 | `9cVfhg6ATxAf7uSQbHiQXHMhzW4Wp1eZ9wbchkhTvecf` | 18,33 | 12,6 | 61,39 | 12,5 | après Musk |
| 7 | `EH2Pezn6kHqbpaRMCzpdb7hm7xGjZt9QjGbqvTq1AS7b` | 17,34 | 11,9 | 482,76 | 0,0 | après Musk |
| 8 | `6S6Ws4bDn4MtQvMALVjyRM4wLrUBRHVyuTFV8TvniEgz` | 15,64 | 10,7 | 160,70 | -3.4 | après Musk |
| 9 | `WeCSv83PaMBqtaf6WJqRffSrXkUBKoWdjZrKWYiaKS8` | 14,78 | 10,1 | 57,69 | 0,0 | après Musk |
| 10 | `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` | 13,41 | 9,2 | 338,03 | 44,8 | après Musk |
| 11 | `6JKsihiTDLf5aHUY9YgX359J2y7hdFHpoyj2JVXTkjfD` | 11,88 | 8,2 | 101,43 | 29,8 | après Musk |
| 12 | `9fye85GKngHLmzyQ7w9ZbvfE9UEts3QNrzmLQBJkWAFS` | 10,11 | 6,9 | 21,82 | 0,0 | après Musk |
| 13 | `5aQ6dDXoqgeeLVWF7PLf6zPSLTF1Hw8bhNyweci8herC` | 8,69 | 6,0 | 4,48 | 5,0 | avant visuel |
| 14 | `7X1pXmV8roiJWnGkruzC1FFMVSC1tq8qzY6T5eDCrDA` | 8,12 | 5,6 | 29,42 | 9,5 | après Musk |
| 15 | `8iZTJ6U2mjFbZT4hSTB5iT9Zzq8268j1LwxpNxMoKJiP` | 8,00 | 5,5 | 135,65 | 0,0 | après Musk |
| 16 | `tVfxX891Y69S2MXorrr8ytjZT8bQqc7PRToWeTw6qBw` | 8,00 | 5,5 | 21,75 | 1,8 | après Musk |
| 17 | `6Tt9iP2YacNi8om4qwwuTsWtrEqsftvoqaG57QqdS3GF` | 7,60 | 5,2 | 3 886,32 | -2.4 | après Musk |
| 18 | `Dt5zbqrjXsfVshbUiueZs6khKttzExBREcmFpL7aryqu` | 7,55 | 5,2 | 167,66 | -0.1 | après Musk |
| 19 | `CmymY1AksY8QSH6GmhXqfa4HM8VBi2QQBDgUMDyHNZJW` | 7,16 | 4,9 | 4,81 | 0,0 | après Musk |
| 20 | `6Lomz4sdWdAwCKmjc8wHFhEHAPDwa5KEmxi1ziEWXp9G` | 6,66 | 4,6 | 344,62 | 1 466,6 | avant visuel |
| 21 | `CtBtkUoSy87VpyDNQgLyqtqPqCWPBYrcKX5VpmREdon2` | 6,46 | 4,4 | 37,59 | 0,0 | après Musk |
| 22 | `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 6,19 | 4,3 | 0,49 | 0,0 | avant visuel |
| 23 | `5W7QfkK172oWiXALgVk5xaF41mnZ6GEk8SnN8AwzGdGG` | 5,91 | 4,1 | 260,00 | 0,0 | après Musk |
| 24 | `5LuZkLTr854dfoq5wG1zP8fwfXNGESxbDyBsJsFZc5nR` | 5,84 | 4,0 | 65,15 | 0,0 | après Musk |
| 25 | `5kWhWXVdh75cMKfxSG96PNA3faUrK5H9t1kE7v4zbZDA` | 5,39 | 3,7 | 282,98 | -222.9 | après Musk |
