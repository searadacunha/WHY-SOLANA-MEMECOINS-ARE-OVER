# Achats antérieurs aux événements clés

Généré par `scripts/rep_70_reports.py`. Ne prouve aucune connaissance préalable : un achat antérieur à un événement est compatible avec un pari ordinaire.

Deux cohortes distinctes : avant le premier visuel public exact (21/07 16:02:29 UTC, @ChrisWinig, plus ancienne image identique dans le corpus archivé ;
une réponse de @kikisknees à Musk à 16:00:08 UTC a un média perdu), et avant l'adoption par Musk (borne basse 21/07 19:03:27 UTC, borne haute 21/07 19:25:23 UTC,
identifiant de l'image 21/07 19:23:20 UTC). Un achat dans cette fenêtre de 21 minutes n'est classé ni avant ni après.

## Activité par fenêtre
| Fenêtre | Heures | SOL acheté | SOL vendu | Achats | Ventes | Wallets | Nouveaux acheteurs | Médiane achat/wallet | Part top 5 % |
|---|---|---|---|---|---|---|---|---|---|
| avant_pmarca | 162,52 | 5327,01 | 5197,05 | 5429 | 4505 | 1541 | 1450 | 0,6642 | 8,6 |
| pmarca_a_winig | 19,26 | 818,71 | 624,53 | 511 | 493 | 250 | 89 | 1,0 | 42,0 |
| winig_a_biden | 1,73 | 240,92 | 279,93 | 306 | 224 | 199 | 73 | 0,5 | 34,0 |
| biden_a_musk_borne_basse | 1,29 | 13,18 | 84,94 | 42 | 78 | 74 | 3 | 0,2 | 55,3 |
| fenetre_musk | 0,37 | 20,85 | 44,04 | 13 | 18 | 25 | 8 | 0,1 | 96,8 |
| musk_plus_1h | 1,0 | 5347,29 | 4987,28 | 1443 | 989 | 749 | 476 | 1,1143 | 37,1 |
| musk_1h_6h | 5,0 | 64318,19 | 62335,96 | 10123 | 7795 | 3995 | 3209 | 2,0 | 15,1 |
| musk_6h_24h | 18,0 | 124379,39 | 122964,7 | 23238 | 16963 | 8490 | 5742 | 1,109 | 12,2 |
| jusqua_retrait | 19,18 | 74835,09 | 77072,26 | 16195 | 12919 | 6455 | 2825 | 1,2964 | 12,6 |
| retrait_plus_7j | 168,0 | 102944,34 | 102673,06 | 46923 | 39577 | 10736 | 5730 | 0,9983 | 18,0 |
| butler_oct | 360,0 | 80900,76 | 79389,9 | 36880 | 38579 | 11393 | 5264 | 0,9915 | 12,4 |

## Plus gros acheteurs dans les 6 h avant le visuel et jusqu'à la borne basse du changement de photo
21/07 10:02:29 à 21/07 19:03:27 UTC. Ce sont les achats à regarder en premier, et aussi ceux qui ont le plus d'explications ordinaires : la promotion publique du projet s'intensifie ce matin-là.

| Wallet | SOL acheté | Jetons M | Achats | Premier | Dernier | Réalisé SOL total | Flux net SOL total | 1er achat du wallet |
|---|---|---|---|---|---|---|---|---|
| `5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx` | 111,49 | 16,73 | 6 | 21/07 13:40:29 | 21/07 17:33:49 | 489,6 | 489,6 | 15/07 15:17:33 |
| `JC5MLur7syXrMRvcdX2dFGNtChP9ZEn5ufnuEyj5QS2K` | 99,22 | 11,52 | 2 | 21/07 13:58:12 | 21/07 14:04:39 | -42.5 | -42.5 | 21/07 13:58:12 |
| `BfkBxeDE29dnFP4ptpEHhQWGL9xMu9LYv7hbUAmzU667` | 45,65 | 6,54 | 11 | 21/07 13:54:42 | 21/07 17:40:42 | 451,7 | 431,5 | 21/07 13:54:42 |
| `5xyUFj7a8sP9y7DS93MnVvAfBAW3Sq3hbcfyuhyawSD9` | 33,84 | 4,98 | 6 | 21/07 13:54:37 | 21/07 14:04:58 | 145,9 | -808.3 | 21/07 13:54:37 |
| `D12r2UMT4yEhQca9p5aJeKMZYoerpaXEPT4zNTxSQ5ir` | 33,28 | 3,76 | 9 | 21/07 14:20:33 | 21/07 15:24:29 | 830,2 | 162,0 | 15/07 15:44:04 |
| `4GVoqTXYLRDyBZPVTeX6PeDsoJ4vJeP4gPdVPeqkeKXe` | 25,00 | 3,56 | 5 | 21/07 13:51:32 | 21/07 17:33:49 | 455,0 | 455,0 | 21/07 02:24:45 |
| `7Mjg8z2FjLAvKGGZmAbz6z52z4K17Lb42QZxhhTtKBdE` | 21,00 | 2,47 | 1 | 21/07 15:08:34 | 21/07 15:08:34 | 42,6 | -36.7 | 21/07 15:08:34 |
| `5cWjvqwYbdiWCNcWbV71nZsM4KyfEnB3Cw1s7UEaftvJ` | 20,00 | 4,20 | 2 | 21/07 12:09:58 | 21/07 13:19:37 | 173,5 | 247,7 | 21/07 12:09:58 |
| `3eJkwFDZVB27emciij1oWUVodmFhFdnkpmzKHjDzH34o` | 18,15 | 2,84 | 4 | 21/07 12:48:22 | 21/07 18:10:12 | 31,9 | 31,9 | 15/07 18:12:19 |
| `Ct6SP2E3ckCGUCDzjAfgVR5SRbwdG6vcAydNVdMXMi3Q` | 17,50 | 2,31 | 10 | 21/07 16:46:29 | 21/07 17:19:17 | 371,9 | -197.5 | 16/07 19:14:17 |
| `EKDB7EyLPD7a2Mqo7Kh8Y4aR7gD26VErY3yj41eZjwCJ` | 15,12 | 3,40 | 1 | 21/07 13:14:44 | 21/07 13:14:44 | 23,6 | -617.5 | 21/07 01:30:27 |
| `85ToHSg65oSMaJU7znUpzKfYuBbScWSsyRMCZavnoPjc` | 13,27 | 1,83 | 2 | 21/07 14:03:50 | 21/07 17:32:40 | 0,1 | 0,1 | 21/07 14:03:50 |
| `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS` | 12,60 | 1,53 | 13 | 21/07 14:15:38 | 21/07 16:59:58 | 1 435,9 | 1 234,6 | 15/07 17:07:21 |
| `6bW7RAdNLWm3543VrmGFHtL47sAmMabgLBynS9mzRjFE` | 12,00 | 1,83 | 3 | 21/07 13:40:29 | 21/07 13:53:45 | 395,8 | 395,8 | 21/07 13:40:29 |
| `FCYZ79sMfmPuC2KMfNEGBqT4wwiHCUf5dzjaoweLRrH1` | 11,90 | 1,56 | 2 | 21/07 15:45:16 | 21/07 17:18:13 | 9,7 | 9,7 | 21/07 15:45:16 |
| `6LFVkW3aa5f7WzhXNVZxoLHycRGhQRZyA8HcWp1a87PL` | 10,00 | 1,08 | 2 | 21/07 15:23:40 | 21/07 15:24:03 | 96,4 | 96,4 | 21/07 15:23:40 |
| `BDFMkurHjWM8HCibLRncxaSF8eQ3oJJztPSr4jUEo3nZ` | 9,16 | 1,15 | 1 | 21/07 16:45:55 | 21/07 16:45:55 | 21,3 | 21,3 | 16/07 01:58:59 |
| `DtxTsytoa5qWzW82UrB7WJnDzUo1rtksVBQ4Mm1jRtJF` | 8,19 | 1,05 | 6 | 21/07 14:21:13 | 21/07 17:05:01 | 70,7 | 64,6 | 20/07 12:01:58 |
| `AnkQY7kybDL1pGPM4e6P7HhdW6App4UXk97x2JKfBdU1` | 7,50 | 1,37 | 2 | 21/07 13:49:32 | 21/07 17:12:22 | 67,7 | 49,6 | 15/07 17:16:54 |
| `71d47bhSDtmnyYhAgg3vEcXft3ip3Rm8ra5r5wgmarug` | 7,40 | 0,72 | 3 | 21/07 14:07:05 | 21/07 14:10:27 | 2,7 | -22.0 | 21/07 14:07:05 |
| `49boQDhjNSLUyRyDMZpiDuZLWYCNeJpgV9jrLQfh8LPX` | 6,73 | 1,28 | 2 | 21/07 13:21:25 | 21/07 13:50:58 | 140,0 | 140,0 | 21/07 13:21:25 |
| `5SvMk7YtF5aR2UbiM8rGpJrBkXV18p5EwVZVzMzjQZZe` | 6,55 | 1,37 | 1 | 21/07 13:16:29 | 21/07 13:16:29 | 2,5 | -71.6 | 21/07 01:26:37 |
| `DQvH7Tkwo4q4eWbnSoFJRyiL33TFZFUYwubDiNumdtB6` | 6,55 | 0,64 | 1 | 21/07 14:07:19 | 21/07 14:07:19 | -10.3 | -21.8 | 21/07 14:07:19 |
| `5KkkbpykJCz69zHrPSovZQcAVwZKpeQeRRhZtQXrRzeo` | 6,08 | 0,86 | 1 | 21/07 16:57:34 | 21/07 16:57:34 | 2,0 | 2,0 | 21/07 16:57:34 |
| `75fXGTvc8BHKBXwNfqriso6dzLe52qMUzvGPu9DV8fog` | 6,08 | 0,72 | 3 | 21/07 16:17:27 | 21/07 16:56:07 | 197,5 | 158,0 | 14/07 02:55:32 |
| `7UDfjuKyYddK7mYEQbPBNfzHPvehHhq7LkouQC9HQZrY` | 5,83 | 1,00 | 1 | 21/07 13:54:37 | 21/07 13:54:37 | 0,2 | 0,2 | 21/07 13:54:37 |
| `9yxEQsmpYZWBhWXFUcpAMguUzNDxg3nUBQEcmNSrakDf` | 5,60 | 0,81 | 1 | 21/07 16:54:24 | 21/07 16:54:24 | 0,3 | 0,3 | 21/07 16:54:24 |
| `FNuKXWBpx1dYeY81rzFUt317fk5TwB29kLFmKfLE1EoQ` | 5,33 | 0,76 | 12 | 21/07 14:15:44 | 21/07 17:39:30 | 3,7 | 1,7 | 15/07 19:38:46 |
| `JARVhtcGADkszZb91SAHQzxh2KrW7aRtZ8CA2FHDj6jF` | 5,00 | 0,51 | 1 | 21/07 16:30:11 | 21/07 16:30:11 | 181,5 | 181,5 | 14/07 02:19:12 |
| `A9CYDXm23UagDkbRnv2NYYuj8FvHQXn52WnFiXoA9woz` | 5,00 | 0,61 | 1 | 21/07 14:04:13 | 21/07 14:04:13 | 1,2 | 1,2 | 21/07 14:04:13 |
| `EUtWKDpegbbHjBPoyDhZj6AijRwAG1x8aF581Wfkeo3C` | 4,62 | 0,68 | 2 | 21/07 13:44:19 | 21/07 14:22:43 | 9,1 | 9,1 | 21/07 13:44:19 |
| `AqPgP5mGnYCUizjPrNd8T8aPWQDFWYiyA2RKtcZbgNJX` | 4,35 | 0,60 | 5 | 21/07 12:32:30 | 21/07 17:24:25 | 37,4 | 13,4 | 15/07 17:38:35 |
| `49YJ8q4EicnZwNnGjtERipEXnRUEwQACUcck2xMgPE5Y` | 4,10 | 0,59 | 17 | 21/07 13:19:43 | 21/07 17:39:24 | 1,4 | 1,4 | 14/07 19:31:29 |
| `4HuspKhV9F5Qu9QrNbiJvbFwt9NYHqhYz1Q2RA5DBPth` | 4,01 | 0,53 | 3 | 21/07 11:49:51 | 21/07 14:10:12 | 26,4 | 26,4 | 21/07 11:49:51 |
| `HqxWXj8VJsGAwJuesYSxfsehfgjeZhu5LKYgvvE4gm9Y` | 4,00 | 0,39 | 1 | 21/07 14:06:21 | 21/07 14:06:21 | 28,4 | 28,4 | 21/07 14:06:21 |
| `BUCkjvR8aGMSLmDpnk5nabFkeijtsUdZ24bRxhTm2koK` | 4,00 | 0,43 | 1 | 21/07 16:19:57 | 21/07 16:19:57 | 72,5 | 72,5 | 21/07 16:19:57 |
| `3eW6W2d2PkQGM8Btjf3AbEKXYswBDt6mDntM9CEuNLXb` | 3,78 | 0,54 | 17 | 21/07 12:10:04 | 21/07 17:39:25 | 1,8 | 1,8 | 14/07 03:27:19 |
| `2GTxgLAsbHPGUWSuj7n2kb7JpW2xQhzfXv3ukqpEjdDi` | 3,75 | 0,57 | 1 | 21/07 17:23:15 | 21/07 17:23:15 | 6,2 | 6,2 | 21/07 17:23:15 |
| `AHA6fNQYjut7TYQ7VsCCtWnGzZm9HEUbGomV5Jv9fKr3` | 3,68 | 0,65 | 2 | 21/07 13:54:05 | 21/07 13:54:11 | 1,1 | 1,1 | 15/07 23:30:51 |
| `9qASz9iM8ZMmx5SWHwr67AJPdnYvYy95YFFmBgHz7UCj` | 3,46 | 0,50 | 11 | 21/07 14:55:36 | 21/07 18:51:38 | 2,6 | 2,6 | 15/07 17:21:37 |
| `5qx8EmzhnxwPDzkNMdRLNFZ245pwpioeUN7EyzH4MhNh` | 3,35 | 0,45 | 12 | 21/07 13:49:39 | 21/07 17:39:25 | 1,7 | 1,7 | 14/07 03:27:19 |
| `5HdmFajexban7WJkfP4QrGXXyt76Mwwp9nFeZDWEf3Hy` | 2,61 | 0,39 | 12 | 21/07 12:10:05 | 21/07 17:39:24 | 1,7 | 1,7 | 14/07 16:44:18 |
| `6uwqPxhsRwLTPLyhrppUi9YPvxKq5eHhDGXQ4GZ1gbyk` | 2,60 | 0,27 | 1 | 21/07 16:33:10 | 21/07 16:33:10 | 6,0 | 6,0 | 21/07 16:33:10 |
| `HRGt3Yr7AZizMzwWcLQnnaUtwdRyqNWpbssqbDEsQAXz` | 2,54 | 0,34 | 13 | 21/07 13:49:37 | 21/07 17:32:45 | 2,1 | 2,0 | 14/07 03:27:43 |
| `Aq9yU6gGnNgJobVmxfhdeXSySarY7bp88sE6BhK6EBDA` | 2,41 | 0,30 | 1 | 21/07 14:55:22 | 21/07 14:55:22 | 131,3 | 74,7 | 15/07 16:30:33 |
| `5fMp94GgJVgvva8ubsR6xRg3PuZL4x7j9cwhL4aWtPLN` | 2,41 | 0,26 | 1 | 21/07 15:43:34 | 21/07 15:43:34 | 12,6 | 12,6 | 21/07 15:43:34 |
| `3AwDdcrXRJpoWU5EQ9Dk7KR82jmQQK7ZAggay62aYZyG` | 2,34 | 0,35 | 9 | 21/07 12:10:04 | 21/07 17:32:51 | 1,3 | 0,7 | 14/07 03:40:05 |
| `7hARSicdYvWR9saun1F3JDQjnnHY3k6wvNH2XXp2EA6A` | 2,32 | 0,28 | 5 | 21/07 14:22:00 | 21/07 17:39:30 | 3,1 | 3,1 | 15/07 17:21:24 |
| `GrQGNjLzyzf7dNAewFnCG7RGnsfekCbNeFkDfdHPJeL6` | 2,26 | 0,24 | 3 | 21/07 16:18:40 | 21/07 16:23:09 | 28,4 | 28,4 | 21/07 16:18:40 |
| `BX3Q7av7AkLAhhEF2SPTJCihYdwSw83GBJYQixEsUk2X` | 2,24 | 0,29 | 3 | 21/07 14:15:53 | 21/07 17:32:58 | -0.0 | -0.2 | 21/07 14:15:53 |

## Plus gros acheteurs dans la fenêtre du changement de photo
21/07 19:03:27 à 21/07 19:25:23 UTC : classement impossible avant ou après.

| Wallet | SOL acheté | Jetons M | Achats | Premier |
|---|---|---|---|---|
| `4DdrfiDHpmx55i4SPssxVzS9ZaKLb8qr45NKY9Er9nNh` | 10,00 | 2,26 | 1 | 21/07 19:25:17 |
| `BDFMkurHjWM8HCibLRncxaSF8eQ3oJJztPSr4jUEo3nZ` | 3,60 | 0,87 | 1 | 21/07 19:25:08 |
| `9zri3mYF16MMznYoyyUFfLhxTf3DERRoxmfqpFzv9nZ4` | 3,08 | 0,60 | 1 | 21/07 19:10:08 |
| `3eJkwFDZVB27emciij1oWUVodmFhFdnkpmzKHjDzH34o` | 3,00 | 0,71 | 1 | 21/07 19:25:08 |
| `ToeAtAps23qivv6qLJJwwSechVQqbRLvsGYfWxLNKiQ` | 0,50 | 0,11 | 1 | 21/07 19:25:18 |
| `EKMKQaH5cAvG6phALpnNNx5bjLLnijZpd4FADtNANRyH` | 0,20 | 0,04 | 1 | 21/07 19:25:20 |
| `3eW6W2d2PkQGM8Btjf3AbEKXYswBDt6mDntM9CEuNLXb` | 0,17 | 0,04 | 1 | 21/07 19:25:23 |
| `3AwDdcrXRJpoWU5EQ9Dk7KR82jmQQK7ZAggay62aYZyG` | 0,11 | 0,03 | 1 | 21/07 19:25:23 |
| `CvBkdpuu9Uj5275svNrbjh2cYXLByPUV7wnxCZ9T8PhC` | 0,10 | 0,02 | 1 | 21/07 19:25:20 |
| `4ihSLYJYGCxQosiAyvfaTMR9WtakNGQs8CXEgC5gjJfS` | 0,10 | 0,02 | 1 | 21/07 19:25:20 |
| `dc5cfqYJ312QL35fu9oZwrs5CxgQVh646TFPGTs3P6J` | 0,10 | 0,02 | 1 | 21/07 19:11:07 |
| `HcnKk4wCCubjoSpH5GkMbDiCAsUbHTvAGunYbHMRVZvt` | 0,07 | 0,01 | 1 | 21/07 19:20:28 |
| `FF3L3uqtddKNWR4vfLDvbh7ncLMQKsbtDA98k2F6aiK8` | 0,05 | 0,01 | 1 | 21/07 19:25:21 |
| `8vTEtGqXmA94F4Vqmg52qS9VcZ9Av8Z45QpRJUFiD6up` | 0,04 | 0,01 | 1 | 21/07 19:11:40 |
| `DZBETeDYyywWwWpGki42VbdkhPqDYU2zLYhgP8eThwGX` | 0,01 | 0,00 | 1 | 21/07 19:25:20 |

## Les 1 000 premiers acheteurs, tous venues
Ordre (slot, index de transaction). `Acheté` et `Réalisé` couvrent tout l'historique du wallet sur DMAGA.

| # | Wallet | Slot | UTC | 1er achat SOL | 1er achat M | Acheté SOL | Réalisé SOL | Résiduel M |
|---|---|---|---|---|---|---|---|---|
| 1 | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 277417695 | 14/07 02:05:25 | 0,201 | 7,106 | 28,00 | 0,0 | 0,00 |
| 2 | `EYykLfeAjyXCH1QojDeRFgoXmv3MfS24gZa8AordnezX` | 277417696 | 14/07 02:05:25 | 0,150 | 5,268 | 0,15 | 0,0 | 0,00 |
| 3 | `Edq7kG2NREc5Z2HsiFBHbGiiUneprcpWg6Qodh4GPPy8` | 277417700 | 14/07 02:05:28 | 0,190 | 6,592 | 0,19 | 0,0 | 0,00 |
| 4 | `E1mh1Wfm7JK78fJSh3Ta8XwV43tuuAkhoikVCvvDWmeg` | 277417728 | 14/07 02:05:39 | 1,000 | 33,419 | 6,00 | 4,0 | 0,00 |
| 5 | `Dj2a99M9EHGaxfQDqWmkp5y5mjbdg7nXWGeFK5GjQoqt` | 277417737 | 14/07 02:05:43 | 0,098 | 3,223 | 0,10 | 0,1 | 0,00 |
| 6 | `BNHsrnuv72vo91szVHnahB2eGYXPMcxWdFyPC4Xge4Fk` | 277417743 | 14/07 02:05:46 | 1,960 | 60,710 | 1,96 | 31,0 | 0,00 |
| 7 | `8D2AGAGPMZaPtZRyTgCSHnFfffAJ43RB1WBE6FaQ4FFw` | 277417752 | 14/07 02:05:50 | 0,214 | 6,194 | 0,21 | 3,2 | 0,00 |
| 8 | `GySdM4D2PcQGMubGgGmpbMPVX82Ys84pyvhYvyax8q16` | 277417754 | 14/07 02:05:51 | 0,000 | 0,002 | 0,00 | 0,0 | 0,00 |
| 9 | `DrKPLzTLWsk9w9ifHjr2QDkQ7nfJYoLmpXYtBhSoXe5g` | 277417760 | 14/07 02:05:54 | 2,025 | 54,923 | 2,02 | 0,8 | 0,00 |
| 10 | `BE5S5w9KyC9nrYhGWNQuRunKwP9avhubpiAaQMzf3DTD` | 277417762 | 14/07 02:05:54 | 1,876 | 45,583 | 1,88 | 0,4 | 0,00 |
| 11 | `gYVsQ5UG6du5zjXnamSkgQrQoKbwn36cEYSuteEVbUx` | 277417764 | 14/07 02:05:56 | 1,142 | 25,578 | 1,14 | 0,0 | 0,00 |
| 12 | `HcnutbkSQTwWutqn15XGvSB4jATpQbRxMGzm7sK4ecaT` | 277417768 | 14/07 02:05:57 | 0,425 | 9,132 | 0,42 | 0,1 | 0,00 |
| 13 | `GS7aGEQc5NomZsmm6qfN8WUNE8z7B9Lqgb5cv6aKdeS2` | 277417780 | 14/07 02:06:04 | 0,980 | 20,321 | 0,98 | -0.1 | 0,00 |
| 14 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 277417789 | 14/07 02:06:07 | 1,051 | 20,701 | 2,05 | 0,0 | 0,00 |
| 15 | `GZVLzg7NH1VKUiqutUXMRHYbtQzSATJuyNH7AEznbaor` | 277417805 | 14/07 02:06:15 | 0,496 | 9,483 | 0,50 | 1,0 | 0,00 |
| 16 | `2W83fCmMoUXWnuMJmLnmp1aQwqHdvsvStcZNY772wA2d` | 277417820 | 14/07 02:06:21 | 0,008 | 0,189 | 0,01 | 0,1 | 0,00 |
| 17 | `D9iUhx1x1pA1Uq55JsYmoetUcYGFeLfmUB6HTdNF1nRD` | 277417828 | 14/07 02:06:24 | 0,100 | 2,401 | 0,10 | 0,0 | 0,00 |
| 18 | `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | 277417833 | 14/07 02:06:26 | 1,005 | 23,409 | 1,00 | 0,0 | 0,00 |
| 19 | `Ei1uVf6KvvctoUxXmF1ao1jYi9kSe84iUxH63nDAfB7b` | 277417833 | 14/07 02:06:26 | 0,980 | 21,668 | 1,96 | 21,6 | 0,00 |
| 20 | `H4bVhVzQyen8VA1oughQzXrP3uw7iCS6svKuUpUzMiEU` | 277417839 | 14/07 02:06:29 | 0,206 | 4,203 | 0,21 | 1,7 | 0,00 |
| 21 | `Hk74YpjsPbYxtTxaxcfXL3wgdJeo5gZ48U9Mc1NhJD4M` | 277417858 | 14/07 02:06:38 | 0,500 | 10,015 | 5,81 | 92,7 | 0,00 |
| 22 | `543jATiP6NHiMRRyKuk1LU2ZHVfgyurUP4rdvvF2yhGr` | 277417874 | 14/07 02:06:46 | 2,814 | 55,237 | 2,81 | 6,0 | 0,00 |
| 23 | `GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC` | 277417891 | 14/07 02:06:53 | 0,400 | 7,256 | 0,40 | 0,0 | 0,00 |
| 24 | `CEzjbQqAa5741cJHDstH5Czt4xNiPgLHwax6av449Jyy` | 277417900 | 14/07 02:06:58 | 0,880 | 17,887 | 32,62 | 1 323,0 | 0,00 |
| 25 | `3uVdau2jzFZ3mc4Hwri3XsVVce5iRyC2Wzw2fc7r336z` | 277417905 | 14/07 02:07:00 | 0,920 | 17,887 | 0,92 | 4,0 | 0,00 |
| 26 | `6Lomz4sdWdAwCKmjc8wHFhEHAPDwa5KEmxi1ziEWXp9G` | 277417916 | 14/07 02:07:06 | 1,256 | 23,167 | 344,62 | 1 466,6 | 6,66 |
| 27 | `B4wzDHUaJzW9SJW4FwXo6KMt1JzhhHjKEhboRUCaLQdW` | 277417930 | 14/07 02:07:11 | 2,127 | 36,243 | 2,13 | 0,6 | 0,00 |
| 28 | `4gcriuBoeERYmMxqfphYk8tiGAhaRGRfWgcgPKSkAYHA` | 277417948 | 14/07 02:07:20 | 0,300 | 4,830 | 0,65 | 1,8 | 0,00 |
| 29 | `AYctTz2Drkbr7epaURTZbrhQsUQTTP9P2JDfJ23DxbHe` | 277417950 | 14/07 02:07:20 | 0,507 | 8,022 | 0,51 | 0,7 | 0,00 |
| 30 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 277417962 | 14/07 02:07:26 | 4,411 | 62,923 | 19,80 | 148,5 | 0,00 |
| 31 | `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | 277417993 | 14/07 02:07:39 | 0,999 | 12,732 | 2,50 | 0,0 | 0,00 |
| 32 | `FuqoZkDJyDdYaQaWDgyfnyfyA7495e4XcWi8jHUCJ3zw` | 277418005 | 14/07 02:07:45 | 0,250 | 3,105 | 0,25 | 1,6 | 0,00 |
| 33 | `CjzJRj5RmnSoXxRLUMhmbVKkzsGZsJH6YNw23AQhLzuG` | 277418013 | 14/07 02:07:49 | 0,470 | 6,436 | 0,47 | 0,4 | 0,00 |
| 34 | `6Jf4iDyKGVY8CXynmHqrgUzGbx1GwerMyR2gZQ9LWFje` | 277418016 | 14/07 02:07:50 | 0,184 | 2,489 | 0,18 | 0,2 | 0,00 |
| 35 | `9SHtoDswbWxmqyFm2CYj6fcJgnQMgefG1ZtwerEg2BZZ` | 277418016 | 14/07 02:07:50 | 2,893 | 36,785 | 16,75 | 103,4 | 0,00 |
| 36 | `89zyQK42DVeDV7NyqxAXSmKARRMHanHLHQVC25UFTykd` | 277418022 | 14/07 02:07:52 | 3,283 | 37,056 | 14,52 | 18,7 | 0,00 |
| 37 | `824RSNq928FmyDCpuCwQs7oFBHRk5M89nHLHLt1HQpsA` | 277418030 | 14/07 02:07:56 | 1,998 | 20,467 | 5,00 | 3,3 | 0,00 |
| 38 | `F1x9bJEUj7jZsuFyYQGTaBAFdutvwHcD42EQXHJDYUPr` | 277418057 | 14/07 02:08:09 | 0,200 | 1,970 | 0,20 | 0,1 | 0,00 |
| 39 | `5GrXfCW6dEk1FSPV3Rj4vUbLwQm3tkE2TtRaRutTsJF2` | 277418057 | 14/07 02:08:09 | 0,695 | 6,739 | 0,70 | 30,8 | 0,00 |
| 40 | `EaoAuWyPcQhuYfYHVYabZZM7Ng35s8iF1CQM6JX5pfKL` | 277418068 | 14/07 02:08:14 | 0,100 | 0,956 | 0,10 | 0,1 | 0,00 |
| 41 | `H66mLE5yGYQsngy88hfGnKyqfhXjgnkCppLt4Jku9JgP` | 277418079 | 14/07 02:08:19 | 0,001 | 0,010 | 0,00 | 0,0 | 0,00 |
| 42 | `2YT3e7cdpoQUTWgtDw1AGt1VYm7nznjHhqfKyX1c5WJP` | 277418081 | 14/07 02:08:19 | 0,799 | 7,528 | 6,80 | 4,6 | 0,00 |
| 43 | `7dY2yLDbFxUCdBUMLiNJVz9Mq1PfetrDjr9GXAMnMM4J` | 277418086 | 14/07 02:08:23 | 1,285 | 11,685 | 195,49 | 284,2 | 0,00 |
| 44 | `BteHCeVLvbSDYy9X5ZUZLyfLLzE7MrQ4jcrWSF7F65D2` | 277418107 | 14/07 02:08:33 | 5,000 | 41,077 | 18,00 | 8,5 | 0,00 |
| 45 | `DvF9iT2hFB5cKuFuQWzjL2uxfi5uyKJ7teciBS3PZtyu` | 277418129 | 14/07 02:08:43 | 0,500 | 3,764 | 0,50 | 1,3 | 0,00 |
| 46 | `HCLibUwr9JYtrpt5QgZY2eWfJbphTM7w9t69mGjayC7f` | 277418136 | 14/07 02:08:46 | 0,609 | 4,505 | 11,68 | 21,7 | 0,00 |
| 47 | `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j` | 277418144 | 14/07 02:08:50 | 2,992 | 21,753 | 385,04 | 5,5 | 0,00 |
| 48 | `AhnfVHPtyf5kvtc7oqzfZhw22gGYzJFS3gSFy14y8noe` | 277418164 | 14/07 02:08:59 | 1,998 | 13,561 | 4,04 | -0.0 | 0,00 |
| 49 | `H5eycVAcvdPDRLGW2Bj9bjDfCTW3r6ssBsdFqBFyWwh7` | 277418180 | 14/07 02:09:06 | 0,499 | 3,270 | 0,85 | 0,1 | 0,00 |
| 50 | `EDLySUHr77oWTpy8cLCkWn5Q29aEG8VSf2kBVmqgt4tZ` | 277418189 | 14/07 02:09:09 | 0,500 | 3,227 | 0,50 | -0.0 | 0,00 |
| 51 | `8YpS4QPQ9WVfw9fgdg3FyXC8MfyQp3GjSfm5xWnajbTm` | 277418194 | 14/07 02:09:12 | 0,254 | 1,619 | 0,25 | 0,0 | 0,00 |
| 52 | `B95TyUXXYVA1yhs2YMDTyzfXfCL8c1kFG2kLT6rVGidJ` | 277418196 | 14/07 02:09:13 | 0,845 | 5,315 | 0,85 | 0,1 | 0,00 |
| 53 | `2QhYSomEnt9VuNgEBojgMYcvdCYmyFKAKQVS9yk2ZkwV` | 277418196 | 14/07 02:09:13 | 2,061 | 12,453 | 4,06 | 0,4 | 0,00 |
| 54 | `4hyqAFymbwakh8Ct8j1grNxuKphnWQ3ZnbMRhqwWdgmJ` | 277418199 | 14/07 02:09:14 | 0,546 | 3,182 | 1,05 | 1,7 | 0,00 |
| 55 | `9ydT8BdB5BQ16GUciPkEL5xW4Gk5PzxcgZ5RVjz5BRTA` | 277418204 | 14/07 02:09:17 | 1,094 | 6,269 | 5,09 | 2,2 | 0,00 |
| 56 | `9XjHYiB6LR5vxvCQGGFjWh6JF6fCUtCirvHrR1in2Mr6` | 277418208 | 14/07 02:09:18 | 1,030 | 5,736 | 2,55 | 2,9 | 0,00 |
| 57 | `AVqS3vAwoBdBZQHtxCRA8cKbzT1fkXEuWLruavvQNMhq` | 277418231 | 14/07 02:09:28 | 3,006 | 16,291 | 9,11 | 9,5 | 0,00 |
| 58 | `EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa` | 277418234 | 14/07 02:09:29 | 0,443 | 2,458 | 0,44 | 25,2 | 0,00 |
| 59 | `AHMbt3grMH8LU2kKqfT9skMxARbWhP1JGcAPKSGR2KUW` | 277418242 | 14/07 02:09:32 | 0,498 | 2,730 | 7,07 | 32,5 | 0,00 |
| 60 | `EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy` | 277418246 | 14/07 02:09:34 | 0,392 | 2,773 | 7,39 | 158,8 | 0,00 |
| 61 | `J515RL7DcWKudyuqwDu5aDSLSX8QrA6cGR82sFmttZEQ` | 277418249 | 14/07 02:09:36 | 0,490 | 3,425 | 0,49 | 1,7 | 0,00 |
| 62 | `6b29tKMdF8QZ67v4eSgKywQwJrmH9998eGRp4XBirnbJ` | 277418252 | 14/07 02:09:38 | 1,500 | 10,879 | 32,97 | 102,6 | 0,05 |
| 63 | `6NKn35eQqVRzaRGxTkZjR5f7rviWujwpANaMvLkpgMqX` | 277418252 | 14/07 02:09:38 | 0,348 | 2,458 | 3,78 | 115,0 | 0,14 |
| 64 | `E14Mpov1GeNvhp3AQ95UVpgqD5tF2XXkeJQZ5ivozMG2` | 277418260 | 14/07 02:09:41 | 2,006 | 13,675 | 3,27 | 11,8 | 0,10 |
| 65 | `ECRuj7ryDcevdPa8ntQ2UVxgqWC9HVavqYpDo2Bmzyrv` | 277418262 | 14/07 02:09:41 | 0,411 | 2,741 | 0,41 | 1,0 | 0,00 |
| 66 | `ciK6UXTcjJEb8aUaogGcoWmGGNUvo7MwgAbv8qbHrqJ` | 277418265 | 14/07 02:09:43 | 0,106 | 0,702 | 0,11 | 0,2 | 0,00 |
| 67 | `3MtyHisCCt7hQq9YLmvzMy1Pgtt5m93bbhFmxvjfUHu1` | 277418270 | 14/07 02:09:45 | 0,980 | 6,393 | 0,98 | 0,1 | 0,00 |
| 68 | `947Rt6cM4Aj8LyLFFFo1vNoNso2bS1Hr5bUkeXhuv8yp` | 277418302 | 14/07 02:09:59 | 0,098 | 0,575 | 0,10 | 0,4 | 0,00 |
| 69 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 277418329 | 14/07 02:10:11 | 0,924 | 5,671 | 53,36 | 74,2 | 0,00 |
| 70 | `3mhPLjS3dH16PAzUdNkirtt6yskUTKfmP5NAwJ2R4PPY` | 277418361 | 14/07 02:10:26 | 0,992 | 5,836 | 3,02 | 2,2 | 0,00 |
| 71 | `23CSpFii5HL3MtkigfiGu3wo7cgAyYBMqvK7hgKikEnf` | 277418368 | 14/07 02:10:29 | 1,027 | 5,885 | 1,03 | 3,6 | 0,00 |
| 72 | `FB8241Dxskd2CiSsNC3aB6gsSMPmsxpJKwJRaUj4G2o5` | 277418412 | 14/07 02:10:49 | 3,000 | 15,478 | 5,00 | 78,4 | 0,00 |
| 73 | `4pKFTQxsc69nzioRwPuAwUm49MRP4KzBmvrfjRCpEe5g` | 277418428 | 14/07 02:10:56 | 0,980 | 4,673 | 42,74 | 7,7 | 0,00 |
| 74 | `An3nGSMocgNSm414LNGzDx9ZgHgQenNX1HficRFyBjqe` | 277418435 | 14/07 02:11:00 | 0,512 | 2,398 | 0,51 | 0,8 | 0,00 |
| 75 | `F4nH4RBFF164KJQUZgMAU9E25N1Vr5FktycneKrYzqXJ` | 277418439 | 14/07 02:11:00 | 0,506 | 2,339 | 0,51 | 1,9 | 0,00 |
| 76 | `77eYkXk6oCrUy6oMi2GLB8zjuKpxFdpVTjPSpoHdm9wd` | 277418468 | 14/07 02:11:13 | 1,049 | 4,543 | 4,63 | 105,8 | 0,00 |
| 77 | `CtCvYhDLxA9y8NBDNSoksqjywL2bcJQsJiZrRR8A9fGf` | 277418470 | 14/07 02:11:14 | 0,161 | 0,688 | 0,16 | 0,0 | 0,00 |
| 78 | `6MkuktixipxKpExP7jnRNN3VnFbUqzTgiSBoTiWM3fCf` | 277418484 | 14/07 02:11:21 | 0,050 | 0,213 | 0,05 | 0,1 | 0,00 |
| 79 | `EN1DfXH568svWHPR8sbmnzQLZ67MVb8b31NKs4S77KhX` | 277418500 | 14/07 02:11:30 | 0,104 | 0,426 | 0,10 | 0,0 | 0,00 |
| 80 | `5Kt6RbrTAHKUQtw4TGdohdGjGNgLuTYaQGN4Yos9CDPR` | 277418509 | 14/07 02:11:33 | 0,151 | 0,618 | 0,92 | -0.0 | 0,00 |
| 81 | `BzguDreyZHsGpfwLNmetETCnwDf1fSkpvDNEkjZxyTmc` | 277418511 | 14/07 02:11:34 | 0,052 | 0,213 | 0,05 | 0,0 | 0,00 |
| 82 | `CsgmfojoX1mUgmJwdf6bZwHCK4c7Qvy8NsjbJpa8s5hK` | 277418541 | 14/07 02:11:46 | 1,106 | 4,133 | 1,11 | 1,5 | 0,00 |
| 83 | `EzR9JxmUs8TX4eskgAeBf7BWLrS6xYerCy3h2Z6PRikZ` | 277418545 | 14/07 02:11:48 | 0,245 | 0,902 | 0,25 | 0,2 | 0,00 |
| 84 | `CJWxxEeNYvHf2w3uNPcWSxBKANvgCZaq1fXUoLMZzypr` | 277418561 | 14/07 02:11:55 | 1,000 | 3,634 | 108,16 | 96,6 | 0,00 |
| 85 | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 277418563 | 14/07 02:11:56 | 1,837 | 6,480 | 5,74 | 0,0 | 0,00 |
| 86 | `Gmc1EGGV4TQfS3Hs8qvNV6u9MMWoS6AJ6f6WLHS9VRjd` | 277418578 | 14/07 02:12:02 | 0,967 | 3,357 | 20,97 | 8,9 | 0,00 |
| 87 | `8EcGxcMb92mXSZpkWsfbfoaAnLLm4LZWULCp9oZMKzjG` | 277418580 | 14/07 02:12:03 | 0,011 | 0,037 | 0,01 | 0,0 | 0,00 |
| 88 | `2qyz7CvLhzBRW1VyKpYAk1D7YHZPW19shJSNYNw4TBj6` | 277418580 | 14/07 02:12:03 | 1,069 | 3,634 | 6,48 | 7,0 | 0,00 |
| 89 | `FgHjf7uYD8hkyN1nGnWUNZwnZyr1BmGMsb7aWsWcgwMZ` | 277418593 | 14/07 02:12:08 | 0,600 | 1,971 | 0,60 | 0,4 | 0,00 |
| 90 | `EDPUTp3jsjWANZxLBFUxKTG3dUtLkAUYVcSHuuWFeTHb` | 277418604 | 14/07 02:12:14 | 0,504 | 1,638 | 2,24 | 0,2 | 0,00 |
| 91 | `GvjCQ1oKSvYaJjn4JupBRQaHq7VYuhKMU1VocY4oTfnK` | 277418614 | 14/07 02:12:18 | 2,358 | 7,464 | 6,36 | -0.2 | 0,00 |
| 92 | `vvvJGe2eckHxQibTmH2tu9UscUTVCLGhnW8XEcBsMzu` | 277418625 | 14/07 02:12:24 | 0,171 | 0,540 | 0,27 | 0,4 | 0,00 |
| 93 | `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 277418631 | 14/07 02:12:27 | 0,382 | 1,232 | 0,38 | 92,6 | 0,00 |
| 94 | `GmxmUrtQYBnYEfz33DKzgrgnkux7JGKUBggRZ5hptA4R` | 277418632 | 14/07 02:12:27 | 4,904 | 15,035 | 4,90 | 4,4 | 0,00 |
| 95 | `4mQiwj1KK7cH1wo4ssGe5KvpscwEG9w2MdPiTLg12ccK` | 277418644 | 14/07 02:12:31 | 0,245 | 0,714 | 0,34 | 0,7 | 0,00 |
| 96 | `5kSveYbcRaB5hn1EneKY5yyAi2d6NPhMoShN6xdtzZY8` | 277418661 | 14/07 02:12:40 | 0,061 | 0,179 | 6,41 | 1,1 | 0,00 |
| 97 | `GQFY2ueByHcwxyAq1nPipmRy7xUKNWAwCiUVC8SNGrKG` | 277418667 | 14/07 02:12:42 | 0,498 | 1,476 | 2,18 | -0.2 | 0,00 |
| 98 | `CK4wFVRhsJMVjREqJCFDnCnrvjDPeN7P6imw7vJu33v6` | 277418667 | 14/07 02:12:42 | 0,296 | 0,870 | 1,00 | 0,1 | 0,00 |
| 99 | `4bHFSuLGjY5vr8hKv75yprv5psWnVZsrUds8DUoVkt68` | 277418668 | 14/07 02:12:43 | 0,980 | 2,845 | 0,98 | 1,9 | 0,00 |
| 100 | `HzBuHZ8YWoptjgP6u7KZBPCFbmS1vA7KAnQAVwGV2dSg` | 277418674 | 14/07 02:12:46 | 1,010 | 2,938 | 27,01 | 62,2 | 0,00 |
| 101 | `851K4FPH5hxvVMkVZT2HrveDmbfrwJZwFgYRuNMyk6pp` | 277418676 | 14/07 02:12:47 | 0,980 | 2,799 | 0,98 | -0.1 | 0,00 |
| 102 | `BvKBZvJMdeRbFaB9WNUak6ZrfcLNkTTGaf8GVK1Wzgw8` | 277418680 | 14/07 02:12:49 | 0,200 | 0,564 | 0,20 | 2,4 | 0,00 |
| 103 | `Vbap3nLNpn2ddfeabXct6gy3yYxH2HNBb1ZGViX7GHA` | 277418684 | 14/07 02:12:51 | 0,173 | 0,488 | 0,95 | 0,8 | 0,00 |
| 104 | `BVKGYaELCHvmBp5VcQbj4f2Me87Rq6XzkP7rBp8zzdt6` | 277418685 | 14/07 02:12:51 | 0,207 | 0,582 | 1,36 | 1,0 | 0,00 |
| 105 | `FpMnKkJBiTpC165wjgUBaaXkWXzXxV1X46Yau91Jx6C4` | 277418686 | 14/07 02:12:51 | 1,453 | 4,019 | 1,45 | 0,5 | 0,00 |
| 106 | `5FionLB7KZ9fT3dXQ4CiQy5EGDhD1Z5X1KpSPP2fivYa` | 277418689 | 14/07 02:12:52 | 5,382 | 13,741 | 5,38 | 0,9 | 0,00 |
| 107 | `FJkb8WnWocfuQYj4v4vg5VpZoST3LebjQk8WpuD7VbgC` | 277419048 | 14/07 02:15:33 | 5,000 | 12,286 | 5,00 | 1,9 | 0,00 |
| 108 | `HWo91qXVDTdbUku86V5EKDLrYbNT35zjHgTLhyzZkDdW` | 277419048 | 14/07 02:15:33 | 0,010 | 0,023 | 0,01 | 0,0 | 0,00 |
| 109 | `4xu2vjQoXh4cArYQTMtWCPRGmZKkJL6WAW1chY9aNiqD` | 277419048 | 14/07 02:15:33 | 0,000 | 0,000 | 0,00 | 0,0 | 0,00 |
| 110 | `86dS9g9LztHT1ewaaeHuBciZNvSBF5Cfo7EP5oykf8kB` | 277419049 | 14/07 02:15:33 | 5,000 | 10,904 | 5,00 | 1,0 | 0,00 |
| 111 | `6jxCHvecKU8PiGxcsi44jbWxhuenjsh9BcW185TWbAEx` | 277419049 | 14/07 02:15:33 | 0,000 | 0,000 | 0,00 | 0,0 | 0,00 |
| 112 | `AiCFF2L2zRKFEcx4uaDAApJDfu3f1VSuBCwKWZLK6qWi` | 277419049 | 14/07 02:15:33 | 0,000 | 0,001 | 0,00 | 0,0 | 0,00 |
| 113 | `2ChX2HnZBL3qyWB2TPE4XzNexba3YDpYoDfeFKhoDLg6` | 277419049 | 14/07 02:15:33 | 0,101 | 0,208 | 0,10 | -0.0 | 0,00 |
| 114 | `3D1NrXFyMTf9q2yWDULadJGiMm45NGDZTUR5mTAbtUDD` | 277419049 | 14/07 02:15:33 | 0,010 | 0,021 | 0,01 | 0,1 | 0,00 |
| 115 | `5p6YJQu3BJ4SnrwLv11QQRYCvCcaP7LQDJfYpcKGSkHN` | 277419049 | 14/07 02:15:33 | 0,200 | 0,410 | 0,20 | -0.0 | 0,00 |
| 116 | `9g2hZBQd28WttL7LodoWKCbyptt3EWp4MqQ59rxgDSu9` | 277419050 | 14/07 02:15:34 | 0,800 | 1,621 | 0,80 | 0,0 | 0,00 |
| 117 | `zfg3djiUUfhkvFAk9hh3tf5GbLYFMZ7QkbZNC9MZy6p` | 277419051 | 14/07 02:15:34 | 0,001 | 0,002 | 0,00 | 0,0 | 0,00 |
| 118 | `J7xLYnWtTPRqEajrhVb4UbPqSCn9eyv3ZGmNHkp878oU` | 277419052 | 14/07 02:15:35 | 0,100 | 0,232 | 0,10 | 0,0 | 0,00 |
| 119 | `BeQiSPBnYBjzhzFPN6fMaUr2KnW2SPenguuEsHB44meu` | 277419052 | 14/07 02:15:35 | 0,050 | 0,116 | 0,05 | 3,8 | 0,00 |
| 120 | `7q8gcdv6bU5CzTaUetLMFZKEzLCZ7xoopsQU1emhs4Bh` | 277419056 | 14/07 02:15:36 | 0,500 | 1,153 | 1,00 | -0.4 | 0,00 |
| 121 | `7bTTrJpjBouGt8b19hyakFntZ61pG7xgYtusftE4qFT7` | 277419057 | 14/07 02:15:36 | 0,000 | 0,000 | 0,00 | 0,0 | 0,00 |
| 122 | `DnAfbThEaMf8BQfezh1GVzbNa88jzzzYY61mzLZvgHrz` | 277419057 | 14/07 02:15:36 | 0,147 | 0,338 | 0,15 | 0,0 | 0,00 |
| 123 | `DCHeUps8TVTKVBEebXY6WnxVmYzvQB2AnQ7U4YPGMVXQ` | 277419058 | 14/07 02:15:37 | 0,800 | 1,818 | 1,50 | 0,1 | 0,00 |
| 124 | `EQUQo3ji1zBrVY4gbw9fQAfdStGHjRumCXFeGu9rBUu5` | 277419059 | 14/07 02:15:37 | 1,000 | 2,225 | 1,00 | 0,9 | 0,00 |
| 125 | `5E5N7Nup6KHYJtUPxDBEQWpQNRH4h2ziBXPEs7wCSURg` | 277419060 | 14/07 02:15:38 | 1,980 | 4,068 | 2,48 | -1.5 | 0,00 |
| 126 | `9JHLpRAHY2iHL65FmgYSpnKwgTJYUEjYJ27Up77hJrTu` | 277419060 | 14/07 02:15:38 | 0,099 | 0,199 | 0,10 | -0.0 | 0,00 |
| 127 | `HJZJun4ezRsHBgwHfQotdSLpMzsiZZNcc2EjJzJ4gWna` | 277419060 | 14/07 02:15:38 | 0,200 | 0,426 | 0,20 | 0,1 | 0,00 |
| 128 | `4ZH2xnniJ7HzsiwsdRmuQmLq1KBtBuhxKCxfe3NPBJ8M` | 277419060 | 14/07 02:15:38 | 0,110 | 0,233 | 0,11 | 0,1 | 0,00 |
| 129 | `FpPyN444MaDvLqwLFrJWxRxaq3tpT3zx8Aqr4bpyvMWe` | 277419064 | 14/07 02:15:40 | 0,050 | 0,106 | 0,05 | 4,1 | 0,00 |
| 130 | `H4dWNS7ydys4Je2G4WgsmJDSmqGtNmf8CT99r9rDnacf` | 277419064 | 14/07 02:15:40 | 0,000 | 0,001 | 0,00 | 0,2 | 0,00 |
| 131 | `2U88amZGXywruP7JkMNWxSgT31tL249akEQfw6VKi4Hx` | 277419065 | 14/07 02:15:40 | 0,010 | 0,021 | 0,01 | 0,0 | 0,00 |
| 132 | `9SipcuCJBzMZc5NvkuUCWVUVPTTvSNJunx7UupyQesCQ` | 277419065 | 14/07 02:15:40 | 0,030 | 0,063 | 0,03 | 0,0 | 0,00 |
| 133 | `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` | 277419066 | 14/07 02:15:41 | 2,500 | 5,139 | 48,50 | 2 540,1 | 0,00 |
| 134 | `6pzmHQ7MENjfJzH77Ui5yP2JCzT4dN4YsFp3kDuiBv8H` | 277419066 | 14/07 02:15:41 | 0,350 | 0,697 | 0,35 | -0.1 | 0,00 |
| 135 | `68pmyHPNWnSRbm3gDunT1oMam6nXr3E6Um2xkQKHRnL` | 277419069 | 14/07 02:15:42 | 0,001 | 0,002 | 0,00 | 0,2 | 0,00 |
| 136 | `5SQqB1qti6CTkyEWZMHTL68svQbMTCu2VifWuCkAZuoM` | 277419069 | 14/07 02:15:42 | 0,200 | 0,396 | 0,20 | 0,1 | 0,00 |
| 137 | `CcYqnZftP2muZ2EJxfd7AQqc1bF6Y6um4M9TPED7LTv` | 277419071 | 14/07 02:15:43 | 0,200 | 0,394 | 0,20 | -0.0 | 0,00 |
| 138 | `ATomG2gRJcB2jNvwcjo2zBMoyLsHZzLgwqy651zzYoCq` | 277419073 | 14/07 02:15:44 | 0,000 | 0,000 | 0,00 | -0.0 | 0,00 |
| 139 | `CaShxDq2Vbdp2XryjDdUZthbTzwYsvKuH6Knn9pPi4xU` | 277419074 | 14/07 02:15:45 | 0,000 | 0,000 | 0,00 | 0,0 | 0,00 |
| 140 | `DQeJQ91Uzcuyk4iAtpQ9FwD8Ddwr62NeWd8hoE1kgLLs` | 277419074 | 14/07 02:15:45 | 0,000 | 0,000 | 0,00 | 0,0 | 0,00 |
| 141 | `9F7eCZmzGZ6okSNrTZLNcwVexbZv7brJCHFvnR5NXtyo` | 277419077 | 14/07 02:15:46 | 0,200 | 0,440 | 0,40 | -0.0 | 0,00 |
| 142 | `BXGaEMDLd5j9R9miUL4zUSew6GGVn1gVWWKYicvoYrrh` | 277419077 | 14/07 02:15:46 | 0,070 | 0,154 | 0,07 | 0,0 | 0,00 |
| 143 | `DmjHk56Qc6TpC5f75dv3CnYEKp1smVLWY8UNa851npGS` | 277419078 | 14/07 02:15:47 | 0,500 | 1,091 | 1,50 | -0.2 | 0,00 |
| 144 | `ESamwEmETkdxUpoQwEtvb7kAnopiXjQk7vrJAZF422Sv` | 277419080 | 14/07 02:15:48 | 0,099 | 0,214 | 0,10 | 0,1 | 0,00 |
| 145 | `6juKVF1Zz5PAtbdZePbzZ2qgNKuFRB2oaj9CazbXizoT` | 277419080 | 14/07 02:15:48 | 0,020 | 0,043 | 0,02 | 0,0 | 0,00 |
| 146 | `7ry1VJ772FxKQ5Mg1BdBDx68n4k1tTRb5ADs2xzifwDA` | 277419098 | 14/07 02:15:56 | 0,030 | 0,072 | 0,03 | 0,0 | 0,00 |
| 147 | `CHyTZVegRWUhDJCVkcKMYWjoX5HKpyK6VtQCy11UH5Vj` | 277419098 | 14/07 02:15:56 | 0,100 | 0,238 | 0,40 | -0.1 | 0,00 |
| 148 | `6b9iQzj1P6z8XpmJSAoyHdLZC4oyK8pmTXQVc9iVTEEr` | 277419101 | 14/07 02:15:57 | 1,000 | 2,352 | 9,00 | 10,9 | 0,00 |
| 149 | `HUBBQMbrasRfHc6cJhZzotZn9H5bnJ8FEToAQ3h7senL` | 277419102 | 14/07 02:15:58 | 0,080 | 0,186 | 0,08 | 0,0 | 0,00 |
| 150 | `J656oRsbRKDNormqoG7TEuP4ZV7WTpx8hZTgfKG9e3Gw` | 277419107 | 14/07 02:16:01 | 0,100 | 0,234 | 0,10 | 0,2 | 0,00 |
| 151 | `6UKgFMfgzSXemW7T1QPNEYovA1JytbYpurhY9ULsyDPy` | 277419108 | 14/07 02:16:02 | 0,250 | 0,583 | 1,00 | 0,1 | 0,00 |
| 152 | `31q2grFg79cJGGsSfMDZd4KjXYcHBNEmTKhQZmPpL1Qh` | 277419108 | 14/07 02:16:02 | 0,030 | 0,070 | 0,06 | 0,0 | 0,00 |
| 153 | `8AUDVko6SgLrgb9qgr3NSDMmNQebq1Ao94BhXvssAfP9` | 277419111 | 14/07 02:16:03 | 0,010 | 0,023 | 0,02 | 0,0 | 0,00 |
| 154 | `AFD9mnqBHxCzxTBSgXwi8EXC1tafZZuNG3R35we1bF6x` | 277419112 | 14/07 02:16:03 | 0,200 | 0,463 | 0,20 | 0,2 | 0,00 |
| 155 | `CMUbeQzwYHemz8iJWwsnhVaWUEy4RJK7Akw5FS2CbZvR` | 277419112 | 14/07 02:16:03 | 0,248 | 0,571 | 0,59 | -0.2 | 0,00 |
| 156 | `AhR3EskCfh8G4RErzGoHkV3PZeY9iUJEKfE3vLSdDctA` | 277419113 | 14/07 02:16:03 | 4,000 | 8,770 | 141,70 | 9,4 | 0,00 |
| 157 | `DioqgcJSZCSsNMv8P76kwrJTKRBo72kfd9hdyHAi8mRD` | 277419113 | 14/07 02:16:03 | 0,140 | 0,293 | 0,28 | -0.2 | 0,00 |
| 158 | `AtfeGDiY5qyRX6jVkfNyh7utLa9a6deUZ1i99f99dU7n` | 277419113 | 14/07 02:16:03 | 0,040 | 0,083 | 0,08 | -0.0 | 0,00 |
| 159 | `BpHuEpQkcCYkZBtpVsmTJ8RUmTWPTDHN2QBsQAACmpDc` | 277419127 | 14/07 02:16:10 | 0,990 | 2,087 | 5,94 | 3,0 | 0,00 |
| 160 | `BVdjLEkqzntNjnz4ZV13gPtamdwV8yUMeK1KRyDRFzre` | 277419128 | 14/07 02:16:11 | 1,000 | 2,061 | 1,00 | 1,5 | 0,00 |
| 161 | `W2z1Kme95N1vabvDX7qPpMar341hmKucPiQw1H4sgY5` | 277419129 | 14/07 02:16:11 | 1,000 | 2,016 | 1,00 | -0.1 | 0,00 |
| 162 | `8j9vuGozcTzcLK3NAsQy1NwMnt99jCdcUznuVyUibjnW` | 277419146 | 14/07 02:16:20 | 0,100 | 0,217 | 0,20 | 0,1 | 0,00 |
| 163 | `2duKG6GUaDETtvNudFSBBVdW93gtGgTEMfxWkFsHshb3` | 277419147 | 14/07 02:16:20 | 0,495 | 1,077 | 16,34 | 20,6 | 0,00 |
| 164 | `FQHDCqFcPDSvT4ChieB87NiTP8jLeSSNVzeVTCFAtMMw` | 277419151 | 14/07 02:16:22 | 0,082 | 0,186 | 0,08 | 0,2 | 0,00 |
| 165 | `8E3BaArUmFXTUynUVBbohMVJ64s48mAjWC2NcioGgEGX` | 277419158 | 14/07 02:16:25 | 0,100 | 0,227 | 0,20 | 0,1 | 0,00 |
| 166 | `AfLHJxt3LT3hF4VX4by3Awbmb6weXwJLtLyHj15T6VA1` | 277419160 | 14/07 02:16:27 | 0,100 | 0,232 | 0,12 | 0,1 | 0,00 |
| 167 | `7WuDKXG4eN8S4PbDd9TPh9SF2CG8cKsBfsMzaLDwtNu3` | 277419168 | 14/07 02:16:30 | 0,100 | 0,247 | 1,70 | 0,2 | 0,00 |
| 168 | `3BqGJjJjWBSStsRjdVtCtJgKNVBKzeUWhBsmaeZzvvzL` | 277419169 | 14/07 02:16:30 | 0,198 | 0,488 | 0,20 | 0,2 | 0,00 |
| 169 | `8XkTJ7pza7ENCYk3iA8LmQR8MpTNVRa74mpDfhbRmmW6` | 277419190 | 14/07 02:16:41 | 7,000 | 16,226 | 7,00 | 4,3 | 0,00 |
| 170 | `AEX7ScQuxPEvK6h9ppJvYJAeA1TMyuoVazAXW3Y26xoU` | 277419196 | 14/07 02:16:44 | 0,300 | 0,689 | 0,50 | 0,1 | 0,00 |
| 171 | `HPTsBt2gTZM2T9NAwBpTFgvEABs8ju43aJxmrtNP82RA` | 277419198 | 14/07 02:16:44 | 0,081 | 0,204 | 0,08 | 0,0 | 0,00 |
| 172 | `4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S` | 277419202 | 14/07 02:16:47 | 3,624 | 8,682 | 9 986,81 | 268,4 | 0,00 |
| 173 | `y8qoAFuiuWC7hGqeRFfNbisgL6xe7bAEujhQ1TpRq9X` | 277419202 | 14/07 02:16:47 | 1,000 | 2,266 | 1,00 | -0.5 | 0,00 |
| 174 | `aifnEdBbPUH7c4rk6jWnBKrDYL1N4AnccEQe9RAcUKF` | 277419204 | 14/07 02:16:48 | 0,010 | 0,024 | 0,01 | 0,0 | 0,00 |
| 175 | `2gx8cYv92EqXAdoSaLdPtvWoJY76PhohRS27XfmbVLbK` | 277419205 | 14/07 02:16:48 | 0,130 | 0,324 | 0,13 | 0,0 | 0,00 |
| 176 | `9iW656DssPhB3hCihuxeTG8xHL37xrLPY2AtozThSyPt` | 277419208 | 14/07 02:16:50 | 0,010 | 0,024 | 0,65 | -0.0 | 0,00 |
| 177 | `Dcp3qD9FRQ5V4x45X5z3Ct2WAFndp98h9Ezp8HNShfvp` | 277419208 | 14/07 02:16:50 | 0,300 | 0,725 | 0,30 | 0,4 | 0,00 |
| 178 | `FfhdwP7fs48HuHG4zbeZZVa4LS2qr1A215eGBsiowgPq` | 277419216 | 14/07 02:16:54 | 9,900 | 19,492 | 9,90 | 4,1 | 0,00 |
| 179 | `F61Z4MfSVAHgc3wmRUHb3iwB3Luc5Tf341ed3pq1eUqB` | 277419224 | 14/07 02:16:57 | 1,000 | 1,748 | 28,00 | -0.9 | 0,00 |
| 180 | `8RLzJXUwjcUL9y71Mn6kMyfgnfNfcFPV8NC2NrDq6gV8` | 277419236 | 14/07 02:17:02 | 0,300 | 0,520 | 282,63 | 8,8 | 0,00 |
| 181 | `9bq3rK9zoFViRwvT14S1SZjVyXJVEP4KpnKKcZRYbnE1` | 277419237 | 14/07 02:17:02 | 0,230 | 0,396 | 0,23 | 0,1 | 0,00 |
| 182 | `8ukk81hYB68Kzx1mdhAK3tXjKBzRcDtJrGsMynFxqLZM` | 277419241 | 14/07 02:17:04 | 0,100 | 0,172 | 0,10 | -0.0 | 0,00 |
| 183 | `3UQZ49fX6TQTAknFYRdkXhe7gJmci9bZqv5Ncwv4Wehe` | 277419243 | 14/07 02:17:05 | 0,250 | 0,429 | 0,25 | 0,1 | 0,00 |
| 184 | `AV9k4n1nywDHa58cZ1jDQtetEY2aDKjMRby4hmn3dJw` | 277419244 | 14/07 02:17:06 | 0,990 | 1,676 | 3,96 | 1,6 | 0,00 |
| 185 | `4XvV37ym4pd2NLEPLaQBmHiZvtNQhZHP4RrrgS1LTWoF` | 277419248 | 14/07 02:17:08 | 1,000 | 1,709 | 1,00 | 0,1 | 0,00 |
| 186 | `A4F2VNmARbWJbWpNzCaaNvBTBvcmbxSpbuYVxoh1PKzG` | 277419253 | 14/07 02:17:09 | 7,000 | 10,898 | 7,00 | -4.4 | 0,00 |
| 187 | `GwehqDFnJ6rBkXiy8DfprMBdePPHBSBJnYzMUU8GFqtP` | 277419260 | 14/07 02:17:13 | 0,070 | 0,102 | 0,07 | -0.0 | 0,00 |
| 188 | `J8fYZbmCnAL5WByigxqoum1disKUrZbsAmupfkXMvrmw` | 277419264 | 14/07 02:17:14 | 1,980 | 2,840 | 16,83 | -0.5 | 0,00 |
| 189 | `BX1smfE1HuvuzRaEB9bSohWogNSAghH1GDDM8zS1sfM2` | 277419272 | 14/07 02:17:18 | 2,000 | 2,764 | 4,00 | 0,3 | 0,00 |
| 190 | `3KoyuwnHuopH7HSJYxw3yF2PfRtLnBZdKvfoUcyimAdc` | 277419274 | 14/07 02:17:18 | 0,050 | 0,067 | 0,54 | -0.1 | 0,00 |
| 191 | `HZph5VTw4v1Y53oo8DhLqVNrD2yAoqy67ZxoYWTePgen` | 277419280 | 14/07 02:17:22 | 0,500 | 0,709 | 0,50 | 0,1 | 0,00 |
| 192 | `A2JZiT8Pg1sdJksWYhWXQ38Zyv2sQAm5XNcMaM52dnyz` | 277419282 | 14/07 02:17:22 | 2,000 | 2,772 | 5,00 | 0,4 | 0,00 |
| 193 | `3jLaAuhjq7xAAd3BSUJwTas1ZrfnyhNBES2AfeZZrKGx` | 277419282 | 14/07 02:17:22 | 0,500 | 0,677 | 0,50 | 0,1 | 0,00 |
| 194 | `HrA4mAhw6JDX6NmxNgaBGEg1ctJ6LX3tirCZpCWED6Sm` | 277419296 | 14/07 02:17:29 | 1,000 | 1,347 | 1,00 | -0.0 | 0,00 |
| 195 | `ykED64UJKk5ij8pbdi4TLwokcoysGWu6BF34qgSKX59` | 277419296 | 14/07 02:17:29 | 1,000 | 1,323 | 1,00 | 0,0 | 0,00 |
| 196 | `7diguufq6MqCVLznx3w8UgEngRfuH7XRmSMJEAQHfs9z` | 277419300 | 14/07 02:17:30 | 0,750 | 0,967 | 0,75 | 6,5 | 0,00 |
| 197 | `D1mYKXUATzWyV2BazTJbYSZQayJv7uEgrWMxm3T5daz8` | 277419304 | 14/07 02:17:33 | 0,500 | 0,674 | 1,25 | 0,2 | 0,00 |
| 198 | `86aiwxvV3nGYM2YCXBf68gcALj2ZpQrLNCvPF6bJfw8B` | 277419304 | 14/07 02:17:33 | 1,980 | 2,609 | 11,88 | -0.1 | 0,00 |
| 199 | `5EuSanvrWPGj9go9JnA7robkisHTREgfu32Vzdqg1GcF` | 277419306 | 14/07 02:17:33 | 0,300 | 0,387 | 0,30 | -0.0 | 0,00 |
| 200 | `GzKj2Stu8ix4KxQDJDrcrMeejJQ2Nckmts9q7NVBo8to` | 277419320 | 14/07 02:17:40 | 0,099 | 0,124 | 0,10 | 0,0 | 0,00 |
| 201 | `A5PvR7kxQtG3nkcvzu4jjy3sHzeCmwDzgzNKBGu6Lr2Y` | 277419324 | 14/07 02:17:42 | 1,000 | 1,246 | 1,00 | -0.4 | 0,00 |
| 202 | `64gCXuzpjvt6LjzDzj4VTsMEsqUFzpjgy3fjvDCnQcp9` | 277419324 | 14/07 02:17:42 | 1,000 | 1,224 | 1,00 | -0.4 | 0,00 |
| 203 | `w8MHwTeJX6FL3AzxceEutW4e27nV8t9WMTjGkpUyxRG` | 277419324 | 14/07 02:17:42 | 0,500 | 0,604 | 1,00 | -0.1 | 0,00 |
| 204 | `G7sRVhLXUeFnCoDdTFR4ia1TqvzfGudg5WbrBYHKfPtC` | 277419332 | 14/07 02:17:46 | 5,000 | 6,122 | 20,00 | -4.0 | 0,00 |
| 205 | `6RXYzsvSQEtHp1X8ikXmoTwmBGMPLrwMr27MWfdCGDhx` | 277419336 | 14/07 02:17:48 | 0,100 | 0,120 | 12,10 | 0,5 | 0,00 |
| 206 | `26iK94L8idC64jV1wX5scApGiL52Fjy3d4KcjZHoHW1x` | 277419339 | 14/07 02:17:50 | 0,200 | 0,241 | 0,40 | -0.0 | 0,00 |
| 207 | `6tm9WKym4BzwDimvNrR5X6YHFucxtvg6ELwkxtuVPQUJ` | 277419339 | 14/07 02:17:50 | 0,800 | 0,957 | 0,80 | -0.3 | 0,00 |
| 208 | `94yinPSx12hr9uJfBUtWwumis9wHsuAao7MPpy5ze65L` | 277419339 | 14/07 02:17:50 | 0,560 | 0,662 | 0,56 | -0.1 | 0,00 |
| 209 | `3mXhjD7LZ2PdsC7FgtrL7wkfthX97uZoF4pjz1b1WiTU` | 277419339 | 14/07 02:17:50 | 0,560 | 0,656 | 0,56 | -0.1 | 0,00 |
| 210 | `2gMh6Q393kURb1aYYGAUPaNMPPGQVmohF4WpzX1jVvRj` | 277419339 | 14/07 02:17:50 | 0,560 | 0,650 | 0,56 | -0.1 | 0,00 |
| 211 | `4YbQKCWKytrRYFUoYuAeKxAJyExkk8tyWVBvfavBy1XG` | 277419341 | 14/07 02:17:50 | 0,148 | 0,171 | 0,15 | 0,0 | 0,00 |
| 212 | `7k7QFSjmCdoDYjLuYXnfD9qBGmPmeZp2EUFo9HB8VzST` | 277419352 | 14/07 02:17:56 | 0,800 | 1,143 | 0,80 | 0,1 | 0,00 |
| 213 | `2Mctt4C9boLu5LHMhF7PwGNsAXE7GAKqtUWoYAnA3Bko` | 277419352 | 14/07 02:17:56 | 0,300 | 0,427 | 0,30 | 0,0 | 0,00 |
| 214 | `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 277419353 | 14/07 02:17:56 | 1,000 | 1,406 | 1,00 | 35,3 | 0,00 |
| 215 | `DxYm6ZuiLJTt1eFKpLFQ9FUjpSPHyRA5QxgoCRTQUYnv` | 277419354 | 14/07 02:17:57 | 0,091 | 0,181 | 0,58 | 0,0 | 0,00 |
| 216 | `CyEPCJcKkEsmrf6Uew9nZ1tsfgpF66nKwGXL5EuuQ8GE` | 277419357 | 14/07 02:17:58 | 0,090 | 0,180 | 0,09 | 0,0 | 0,00 |
| 217 | `7VC24Cu1fsWpgqzAKTxrLZaYktNhMWYhda5Q7dyo6sL3` | 277419360 | 14/07 02:18:00 | 1,596 | 3,163 | 4,21 | 1,0 | 0,00 |
| 218 | `3h4Ty6hjTt5Yg2dtGbSdnqM5KPgnXrVgofz7EPbhVYCy` | 277419361 | 14/07 02:18:00 | 0,100 | 0,197 | 0,10 | 0,2 | 0,00 |
| 219 | `8xEtKGvkBb727ato62CmZLLHB7HWve1bwEhNVHpsmZJe` | 277419362 | 14/07 02:18:01 | 0,990 | 1,955 | 46,53 | 1,1 | 0,00 |
| 220 | `9C9fuT1FA7FFi4euHamiaBZzqsbf9FHoAJTAq3DZ2QJf` | 277419366 | 14/07 02:18:02 | 0,205 | 0,439 | 0,21 | 0,1 | 0,00 |
| 221 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | 277419368 | 14/07 02:18:03 | 5,000 | 9,074 | 132,23 | 405,4 | 0,00 |
| 222 | `5esrMxxrtyRVpw8g2xdZ8xV9RD7hBuE9eFLhoAb22rva` | 277419370 | 14/07 02:18:04 | 0,100 | 0,165 | 0,10 | 0,0 | 0,00 |
| 223 | `8cTEbRM2feDhD68xC7BA9TXzGYsQZ5GvTZ3Wf8xqVPCD` | 277419374 | 14/07 02:18:06 | 0,010 | 0,017 | 0,17 | 0,0 | 0,00 |
| 224 | `FWRYqoPYSmN4B3aeX2NC1m84sGbeSCjmeKJ8mPmbog2H` | 277419380 | 14/07 02:18:10 | 0,120 | 0,229 | 0,12 | -0.1 | 0,00 |
| 225 | `Az2zbEnGUqFnGrdP46LXRf89RHqRFckCfnBgaobWUo4h` | 277419380 | 14/07 02:18:10 | 0,500 | 0,950 | 0,50 | 0,4 | 0,00 |
| 226 | `34Q4jfZa3EQsid3Cfw3VBDzAqoQd2CvdYmCjQM8BWZzu` | 277419381 | 14/07 02:18:10 | 0,100 | 0,189 | 0,10 | 0,0 | 0,00 |
| 227 | `7fMtvzA3xjFexxMAzxKdFesrASeUrUQzgpSCAcoBwP6S` | 277419388 | 14/07 02:18:13 | 0,495 | 0,930 | 0,49 | 0,2 | 0,00 |
| 228 | `HLMnFCHYLxhWLHmjcYLyUdAnv198xHUs3VSFsfdAuBXr` | 277419388 | 14/07 02:18:13 | 0,020 | 0,039 | 0,02 | 0,0 | 0,00 |
| 229 | `AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS` | 277419405 | 14/07 02:18:21 | 7,689 | 14,052 | 16 739,81 | 273,6 | 0,00 |
| 230 | `J7VoHEyVxJ8vACAPHwqPMqmdSug7oMab7WPQUewvKaKA` | 277419405 | 14/07 02:18:21 | 1,500 | 2,490 | 2,50 | 0,9 | 0,00 |
| 231 | `8z39KrQxgTBL8gtXtYgvY6NqTPzPwyVzbLX9uFGL5sf3` | 277419409 | 14/07 02:18:23 | 1,980 | 3,904 | 2,97 | 8,7 | 0,00 |
| 232 | `FEiWNj9VJZwo3vVBAbfKvt4aEGfUTcyevNdvu4jFjhLj` | 277419417 | 14/07 02:18:27 | 0,050 | 0,096 | 0,05 | 0,0 | 0,00 |
| 233 | `4tHR1BS3Dgr9nErgEEXiRE5J5XbVgoPjVbAa3vyScYXz` | 277419417 | 14/07 02:18:27 | 0,060 | 0,115 | 0,06 | 0,1 | 0,00 |
| 234 | `5zjjJPJJkPwtvpUWNgHNZ6nw3cnLrXfL6CWNXV24ET4G` | 277419421 | 14/07 02:18:29 | 0,031 | 0,059 | 0,03 | 0,0 | 0,00 |
| 235 | `CCcwced8ETD8xhmr8ccLtnTKAntb4ni57c2tZQ3MhcG8` | 277419421 | 14/07 02:18:29 | 0,200 | 0,379 | 0,20 | 0,1 | 0,00 |
| 236 | `3PtXEHipj6PRAYKUtTQ9YWFxQNA4dfwKgbmzE69QMphh` | 277419429 | 14/07 02:18:32 | 0,500 | 0,958 | 1,50 | 0,4 | 0,00 |
| 237 | `Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt` | 277419435 | 14/07 02:18:35 | 1,000 | 1,886 | 1,00 | 3,2 | 0,00 |
| 238 | `Gk4rLVXDrKA8XdJ7bC6m6v7EKDct1ztxQvKB3yqSrJYd` | 277419452 | 14/07 02:18:43 | 5,000 | 9,224 | 19,00 | 2,1 | 0,00 |
| 239 | `6dobypUVEFj3TKG85Xe7SuUQqbqGov5Scdmf1tVjv6Bh` | 277419456 | 14/07 02:18:44 | 0,396 | 0,690 | 1,19 | 0,5 | 0,00 |
| 240 | `787TDD9dFHqDNuZnVFRSfqtqbhWr3P9VvypAjNnXDxkj` | 277419458 | 14/07 02:18:44 | 0,500 | 0,863 | 0,50 | 0,1 | 0,00 |
| 241 | `9h7cwTLM98FHtk6avQrEqHMCqyVEwEUEuH8YZEeMrHi2` | 277419465 | 14/07 02:18:48 | 1,980 | 3,334 | 1,98 | 0,3 | 0,00 |
| 242 | `4WCjDPeFEkzWCjYpYMp9bzcEzMHPVRZneHE8FqfaVwiD` | 277419475 | 14/07 02:18:51 | 0,050 | 0,083 | 0,05 | 0,0 | 0,00 |
| 243 | `D9eMisBwNwuL8Em2MQ2YVgV5P7uYm4xj5Q3B9gxVWfWD` | 277419475 | 14/07 02:18:51 | 0,200 | 0,330 | 0,20 | -0.1 | 0,00 |
| 244 | `bQ1FQU4psKBbtPdWbnQjes3xqELoXE2fEdwQbaAR6kT` | 277419476 | 14/07 02:18:52 | 0,100 | 0,165 | 0,10 | 0,0 | 0,00 |
| 245 | `KZUoeqr8aUTVPqC4wrijvZSSvzTuHhXJC9bcBTBobbY` | 277419493 | 14/07 02:18:59 | 2,057 | 2,910 | 2,06 | 0,3 | 0,00 |
| 246 | `HjEAzQhAh45ftfxQNJur1D1mFpFHfkLxaScuCnm8K1vm` | 277419500 | 14/07 02:19:03 | 0,500 | 0,691 | 0,50 | -0.2 | 0,00 |
| 247 | `8tVPfty43Gyi1nF1g59oQU2HV2sbCF3pQ9msRSmdrbgd` | 277419506 | 14/07 02:19:05 | 0,015 | 0,021 | 0,01 | 0,0 | 0,00 |
| 248 | `787ps6owL8VxqgoyU8QgefBZVAeZhjBzhopWD7QP6cY3` | 277419508 | 14/07 02:19:06 | 0,050 | 0,069 | 0,05 | -0.0 | 0,00 |
| 249 | `Avi3reHpDmFbKjh3K5y4vmgpbjBhyvyGbBxtPEjWifFV` | 277419512 | 14/07 02:19:08 | 0,079 | 0,109 | 0,08 | 0,0 | 0,11 |
| 250 | `5H4Gx7Sy5jVdkp6tNASarRvRfuJ7NiqeVMe7YXyFzR63` | 277419512 | 14/07 02:19:08 | 0,500 | 0,687 | 1,50 | 0,0 | 0,00 |
| 251 | `2r1G8RPy51zqSc7yLxE6VvWQrJNCTGsMSME4GmKYKpQS` | 277419512 | 14/07 02:19:08 | 3,000 | 3,956 | 4,00 | -1.8 | 0,00 |
| 252 | `JARVhtcGADkszZb91SAHQzxh2KrW7aRtZ8CA2FHDj6jF` | 277419520 | 14/07 02:19:12 | 2,000 | 2,865 | 30,50 | 181,5 | 0,00 |
| 253 | `EJN5CX5zPWCqCZq1TbWt8bF8VMnuYrfzkicgB9aKNKhM` | 277419532 | 14/07 02:19:18 | 0,500 | 0,734 | 0,50 | 0,0 | 0,00 |
| 254 | `FGP8fzEDp22WmcYgihZWByckyxzKiCefPZ2Jied4ZB7T` | 277419532 | 14/07 02:19:18 | 0,050 | 0,073 | 0,05 | 0,1 | 0,00 |
| 255 | `3SeHbwz4GLRYmir2EEY6JozHFeWQnqvkFpKBLgiZ8BJD` | 277419538 | 14/07 02:19:20 | 5,000 | 6,987 | 11,50 | 5,3 | 0,00 |
| 256 | `5s3ogzsq8cvwHtS1B6MhwUUp9CyzugJ6y3WqLPM9Ee3C` | 277419541 | 14/07 02:19:21 | 1,000 | 1,323 | 1,00 | 37,7 | 0,00 |
| 257 | `CvWCUxyt5bfYpn5ftWJS5ExGpmZdPjmPzCATTSYpD9Q3` | 277419552 | 14/07 02:19:26 | 0,300 | 0,389 | 0,60 | -0.1 | 0,00 |
| 258 | `GwWmqHFps53ouq9XEWxQeUSQBJRJohSPpjD7QGadJaug` | 277419556 | 14/07 02:19:27 | 0,750 | 0,975 | 1,50 | -1.1 | 0,00 |
| 259 | `8G2ko7SYMXQKh7EtbuLkyC27KWbWbTZcDcywC7ZZ17SX` | 277419566 | 14/07 02:19:31 | 0,010 | 0,014 | 0,01 | 0,0 | 0,00 |
| 260 | `EoV8yxVM3aHcWWcjTgz9zmzQwveYxtNAUvspcwJQStcR` | 277419569 | 14/07 02:19:33 | 0,040 | 0,054 | 0,11 | 0,0 | 0,00 |
| 261 | `83Deb6VWRyW4s1cJGQMjCezNvLh2Nwnm7VMXSXS5y4oi` | 277419569 | 14/07 02:19:33 | 0,020 | 0,027 | 0,02 | 0,0 | 0,00 |
| 262 | `3dBU2Yeqp8tqYPJfyME79VhRs8UVQDCM9QQnuzcXAunj` | 277419570 | 14/07 02:19:33 | 0,010 | 0,014 | 0,01 | 0,0 | 0,00 |
| 263 | `9mZvXvq24nNZcKgscjPUHTuinKV8ooGFBRykuAcJJbk5` | 277419581 | 14/07 02:19:38 | 1,000 | 1,404 | 7,00 | -1.8 | 0,00 |
| 264 | `3eYumiApWHZdbPVTv5aos5UA7Fs6xtNS3RKTy5S5Vwki` | 277419603 | 14/07 02:19:48 | 0,010 | 0,014 | 0,01 | -0.0 | 0,00 |
| 265 | `AMzZjHCU4ZsLWBdYAGae7RymvfhqSDMDreVmNpBNPDFm` | 277419611 | 14/07 02:19:52 | 1,000 | 1,345 | 1,00 | -0.0 | 0,00 |
| 266 | `4HBwdVag97btPDcq1CxSY8oeg5ymbfDEqHj7rwQa3u3W` | 277419613 | 14/07 02:19:53 | 1,000 | 1,321 | 2,00 | -0.4 | 0,00 |
| 267 | `4nvXCo6iCs2QvZpdG1NCnZkjENnWGURsWJKRJzf78Eox` | 277419613 | 14/07 02:19:53 | 0,200 | 0,261 | 0,30 | -0.1 | 0,00 |
| 268 | `AAYrGGKhHJuq8iBjXXJD1qFfyQznyxuvfCWCJkc8MFAu` | 277419616 | 14/07 02:19:55 | 0,500 | 0,653 | 1,00 | -0.1 | 0,00 |
| 269 | `oar4hYyKyzfCtHUkRkoJtr98tmv2oTzE7AmuBxGqFfr` | 277419620 | 14/07 02:19:57 | 0,500 | 0,664 | 0,50 | -0.0 | 0,00 |
| 270 | `AeNCwp4cUpFehinuP5yhEVueTAi8WxFXR17WKug5FSrn` | 277419624 | 14/07 02:19:58 | 0,200 | 0,264 | 0,20 | 0,0 | 0,00 |
| 271 | `CebrRi1PF1BV8JwTB89vB5HEws19ujWs2y3X1RmewkQt` | 277419625 | 14/07 02:19:58 | 0,495 | 0,649 | 0,49 | -0.1 | 0,00 |
| 272 | `5ZAom4DBAc7FCcBeC8dtti6pnY1pUa1BbqiGcDCSpweF` | 277419625 | 14/07 02:19:58 | 0,450 | 0,585 | 0,45 | 1,6 | 0,00 |
| 273 | `Aq3HogK9Xe9NWXm9UrDU3ufMf7LXezDYLsSqiNj26ZKT` | 277419627 | 14/07 02:20:01 | 0,010 | 0,013 | 0,01 | -0.0 | 0,00 |
| 274 | `CLwS11FCY1aAwfZ3AP66scZEyAeSXd6gavbjfWD6h1KT` | 277419633 | 14/07 02:20:03 | 0,000 | 0,000 | 0,00 | 0,0 | 0,00 |
| 275 | `3xvfezkvakcRLvQxYkKWXARNsyG61CtyDQeavPr8xy3V` | 277419637 | 14/07 02:20:05 | 0,200 | 0,257 | 0,20 | 0,0 | 0,00 |
| 276 | `GK6FKvXHDAZNqzaoMTSxiRbiXVSoEDh5xPW2BVNNCQbM` | 277419644 | 14/07 02:20:08 | 0,500 | 0,652 | 0,50 | -0.1 | 0,00 |
| 277 | `DaCmbtAJ4fUfdZA8mk7Nw9YizXPxJjKYHeFo4BNEwJ1A` | 277419645 | 14/07 02:20:08 | 0,500 | 0,647 | 0,50 | 0,0 | 0,00 |
| 278 | `BGj2PVzDkSCnWS7N248kN6ZoiH4Br8CkHzt6F9JYof6r` | 277419653 | 14/07 02:20:12 | 0,008 | 0,010 | 0,01 | 0,0 | 0,00 |
| 279 | `6Cq8MGcqH9nwKsJHsLaXNuMkWPcTggKzTPLCSSkmCJkk` | 277419655 | 14/07 02:20:13 | 0,165 | 0,228 | 0,26 | 0,0 | 0,00 |
| 280 | `5PhuVS72Y9ZPHi77dSztGEXXquMQ839y7v3A6xC6Gme3` | 277419661 | 14/07 02:20:16 | 0,021 | 0,031 | 0,02 | -0.0 | 0,00 |
| 281 | `HcdRRJPv9gTZy93BTMyB9PaMyWNb795CeGBrZTRcLTmH` | 277419664 | 14/07 02:20:17 | 0,072 | 0,105 | 0,07 | 0,0 | 0,00 |
| 282 | `68XKi2erFn5Eudw9qnKRR2Hg6iWuZcKfr6D3JgymrDoG` | 277419666 | 14/07 02:20:18 | 0,100 | 0,147 | 0,30 | 0,0 | 0,00 |
| 283 | `FZUhawnmwK4JAzZjceYHw5MJHfonoAyaSJwJb2GKMxWb` | 277419676 | 14/07 02:20:22 | 0,100 | 0,162 | 0,10 | -0.0 | 0,00 |
| 284 | `38XZh1e1HuAythXuBqFkU6dzHPeMW5be6nasjN67Ae9B` | 277419686 | 14/07 02:20:26 | 4,950 | 7,711 | 4,95 | -1.5 | 0,00 |
| 285 | `8ThFC8kfdy2ASjB6T5XhzjrivTwEL5gU21hofBWzJdRu` | 277419690 | 14/07 02:20:27 | 0,875 | 1,289 | 3,97 | 0,0 | 0,00 |
| 286 | `CeQQwsrkjHsH6wf7hPBcRRFo6tdYxXzp51Smz3oeHQJd` | 277419696 | 14/07 02:20:31 | 0,500 | 0,739 | 2,30 | -0.0 | 0,02 |
| 287 | `GqpZccM8Wjyj1146ovDYqVEEEv6pN9z1VKPL3Wq1b5i` | 277419696 | 14/07 02:20:31 | 0,294 | 0,431 | 0,29 | -0.2 | 0,00 |
| 288 | `73BtjvLnBJeT5K1REtrLsiVbjCTbSnTA8xpmvhApNpU` | 277419702 | 14/07 02:20:33 | 0,050 | 0,073 | 0,05 | -0.0 | 0,00 |
| 289 | `4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx` | 277419708 | 14/07 02:20:36 | 0,490 | 0,713 | 0,49 | 0,0 | 0,00 |
| 290 | `A39qjL6Mpn6pjKdmDjBVjFKUSdC5JrvWrzqBgNvCrMTr` | 277419725 | 14/07 02:20:44 | 2,000 | 2,845 | 7,00 | 0,4 | 0,00 |
| 291 | `Nv3GRJLFMLzar59uzUpHkHKhK9PtseR1dvSFCuB19gs` | 277419732 | 14/07 02:20:48 | 3,000 | 4,132 | 3,00 | 0,5 | 0,00 |
| 292 | `696qrsoFD124Kk2sho5U6rqWTwdKPWmbk2wJnXfNydct` | 277419759 | 14/07 02:21:00 | 0,161 | 0,237 | 0,16 | 0,0 | 0,00 |
| 293 | `2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d` | 277419761 | 14/07 02:21:01 | 0,490 | 0,715 | 0,49 | 21,4 | 0,00 |
| 294 | `DoTLkk4aFrcTdzYzsX7tUKFwiTBnfnqVnfb9ijmK8dZj` | 277419770 | 14/07 02:21:05 | 0,120 | 0,179 | 0,12 | -0.0 | 0,00 |
| 295 | `DXNRWHudMcr35M38yxbicdBUBumgJpYRsXj4SL8tp3F7` | 277419773 | 14/07 02:21:06 | 2,000 | 2,953 | 4,00 | 2,8 | 0,00 |
| 296 | `2LNivrG5hNDWtgc1jhHRCWJmRvF3pJCv9uMy8TkCCKt8` | 277419776 | 14/07 02:21:09 | 0,300 | 0,429 | 0,80 | 2,0 | 0,00 |
| 297 | `6NyuWEruLGsugdSeQvfoLKE7pTyDps46TxTti3m5ovSj` | 277419776 | 14/07 02:21:09 | 5,000 | 6,842 | 5,00 | 0,1 | 0,00 |
| 298 | `BdeyumYXmaag9SnZ6KPSsK2zarrrmayii1Bjyv6rYZgb` | 277419817 | 14/07 02:21:27 | 5,000 | 6,061 | 10,00 | -0.8 | 0,00 |
| 299 | `Hyf8vJb7RVUjEMFy5qjNA87cysVo1Esn3civABHPrGMm` | 277419845 | 14/07 02:21:40 | 0,100 | 0,125 | 0,10 | 0,0 | 0,00 |
| 300 | `7XwXWta4jNkbpzJ9Ry8P1NnAqCLpcoxCFMVeKR9SSbUe` | 277419846 | 14/07 02:21:41 | 0,150 | 0,187 | 0,70 | 0,0 | 0,00 |
| 301 | `A7PRKosLtBug5sc35jrqKUz8Z85HSSZBzicYGAkNWWGV` | 277419852 | 14/07 02:21:43 | 0,539 | 0,681 | 1,68 | -0.1 | 0,00 |
| 302 | `Chg91E9ehK91HHVUAwyjYY1Pwd7U1vfd8e23Z16PP7j5` | 277419853 | 14/07 02:21:43 | 0,494 | 0,624 | 0,59 | -0.3 | 0,00 |
| 303 | `69u4b3NcEvx8eZm5rvsPWwmy81RSUW3jpq1yKiVayJyS` | 277419853 | 14/07 02:21:43 | 0,250 | 0,345 | 0,45 | 0,2 | 0,00 |
| 304 | `7ccQ1sr91MTUVQPJ6Ja27CtwpKk9PfnT1LKzxPp2BgAu` | 277419861 | 14/07 02:21:47 | 0,020 | 0,028 | 0,04 | 0,0 | 0,00 |
| 305 | `FGjqLvbEPAjH3dyTeWBKryjJu9G3FhgkUWsgQ38dWmMf` | 277419865 | 14/07 02:21:48 | 0,099 | 0,140 | 0,10 | 0,0 | 0,00 |
| 306 | `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 277419866 | 14/07 02:21:49 | 0,490 | 0,691 | 0,49 | 0,0 | 6,19 |
| 307 | `7c5RBJ5ZK6HKhUSxUNqvwQ8B47hoax9H6ZVeStZNBHKq` | 277419875 | 14/07 02:21:53 | 0,007 | 0,010 | 0,01 | -0.0 | 0,00 |
| 308 | `CF1JPQBQmRqRUMXKtKUV22skes4PernkeJHdgZrAJWfg` | 277419876 | 14/07 02:21:54 | 0,200 | 0,278 | 0,20 | -0.2 | 0,00 |
| 309 | `A8sUdrwZCmLhw62YqAW4Ji6cnG9X4nfnCaGxBYvivaqE` | 277419883 | 14/07 02:21:57 | 0,010 | 0,014 | 0,01 | -0.0 | 0,00 |
| 310 | `8J4qAVF7hYKzLdn3y8fSx2VRQS353kXsyPr8p1DmM52T` | 277419888 | 14/07 02:22:00 | 0,060 | 0,082 | 0,06 | 0,0 | 0,00 |
| 311 | `GYHdjU91Dih9Z7u7kCJu4wKfxUucWfcuuTk3Wwm5PKfZ` | 277419888 | 14/07 02:22:00 | 1,500 | 2,036 | 3,40 | -2.2 | 0,00 |
| 312 | `BV7K4vXJWu9v6553YwD98yQaewqqn4mszYZcpjmRR9pD` | 277419889 | 14/07 02:22:00 | 1,000 | 1,327 | 103,50 | 13,2 | 0,00 |
| 313 | `CsewBLGF3n9abLVDDrkFnpNZKxq4tuC4yNV3RxyS6nzV` | 277419900 | 14/07 02:22:06 | 0,114 | 0,160 | 0,11 | 0,1 | 0,00 |
| 314 | `CHy7DCbdpuP7MqvMijJ4gncyn2JKr7m9SPFDbArAbNdV` | 277419905 | 14/07 02:22:08 | 0,100 | 0,142 | 0,12 | 0,1 | 0,00 |
| 315 | `A1Uhb5tUBmtW3e9u23wih1xaQUUqKy7XGPPRfWueM2Vo` | 277419908 | 14/07 02:22:10 | 0,020 | 0,028 | 0,04 | -0.0 | 0,00 |
| 316 | `HnoPbxAjALqpBagr2cX7iXAYs52x36WjqhFft9wohcUy` | 277419913 | 14/07 02:22:11 | 0,020 | 0,027 | 0,02 | -0.0 | 0,00 |
| 317 | `8TrFe2eV2FMkkr6Xq95r3AFxVwbdGDBZT1kVLietKy7Y` | 277419916 | 14/07 02:22:13 | 0,040 | 0,054 | 0,04 | 0,0 | 0,00 |
| 318 | `FTnNcCHtCsjHgGoFw1D4dEUMe94SQkM23BQ9JSATXDV` | 277419925 | 14/07 02:22:17 | 4,000 | 5,362 | 951,94 | 49,2 | 0,00 |
| 319 | `BVmZ7m5ZaSsLazajzH8Q36neMJwpK9mtmYUEP4xZ9829` | 277419937 | 14/07 02:22:22 | 0,030 | 0,042 | 0,03 | 0,0 | 0,00 |
| 320 | `sjZ4SB46dfVrx9JsbyU6e2zCRkh5b1tYv84qihLoKky` | 277419944 | 14/07 02:22:26 | 0,140 | 0,194 | 0,14 | 0,1 | 0,00 |
| 321 | `AWZa6LXfpGuseEYKKcrrFuAvkk3uwhviCBThDmkrVq2p` | 277419952 | 14/07 02:22:29 | 0,020 | 0,028 | 8,45 | 10,0 | 0,00 |
| 322 | `8nV2bdZftfTz1uEJRnoVgVTZpqhj8tkM7SJhvDY9hfjb` | 277419956 | 14/07 02:22:31 | 7,000 | 8,992 | 7,00 | -4.3 | 0,00 |
| 323 | `CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW` | 277419979 | 14/07 02:22:41 | 0,490 | 0,603 | 0,49 | 23,9 | 0,00 |
| 324 | `3vZDWpqU6jr1iNrFu4PqHuA1W3j7Znrnyn4NC3k2pjmq` | 277419989 | 14/07 02:22:45 | 0,010 | 0,013 | 0,03 | 0,0 | 0,00 |
| 325 | `3sm9HBjpQcWtTcbYv3BaGVHdaG23ULeTzSqXsaBwo8iV` | 277419993 | 14/07 02:22:47 | 0,500 | 0,637 | 0,50 | 0,4 | 0,00 |
| 326 | `2peoGcUgeBZy6eER7Ue6aqMfRxgebQ2dKUGigucUsqhW` | 277420001 | 14/07 02:22:51 | 0,146 | 0,184 | 0,27 | -0.1 | 0,00 |
| 327 | `DZwQ66i2hQypHU2J4QdFs3gbxUmbcpd22qdLSfkc7NGg` | 277420008 | 14/07 02:22:54 | 0,247 | 0,297 | 0,25 | -0.1 | 0,00 |
| 328 | `BAa8v3ksJst4byEBJymtFDJxUtkfcqVuVc9MRFJt7SPP` | 277420014 | 14/07 02:22:57 | 0,060 | 0,074 | 0,12 | -0.0 | 0,00 |
| 329 | `3FceUx41i4ARjdSX5neXdSGcLQZADgDYdRgDwr2ZXgRM` | 277420018 | 14/07 02:23:00 | 0,017 | 0,021 | 0,03 | -0.0 | 0,00 |
| 330 | `Gnzd8wjUtp4UcyBMXEjMfm3i9vUd27YfpkxGUptXuLtP` | 277420024 | 14/07 02:23:02 | 0,200 | 0,246 | 0,20 | 0,1 | 0,00 |
| 331 | `DGSg7bXZr9z5n9xNyv4zuQCLrQKjgzYYEa4DGfbWSM5v` | 277420025 | 14/07 02:23:02 | 3,000 | 3,595 | 3,00 | 10,9 | 0,00 |
| 332 | `APDBPg5ePPa3aCpNyhmv1fbSk9R9b4qosBexLJNHN1En` | 277420034 | 14/07 02:23:08 | 0,306 | 0,356 | 1,75 | 0,1 | 0,00 |
| 333 | `6oiKT2vCid3jxcbGuA9y7tffq9fCpJxWUKGT1BMgjmuA` | 277420036 | 14/07 02:23:09 | 0,100 | 0,115 | 0,10 | -0.0 | 0,00 |
| 334 | `2mv4Q2HqnmuDnGbwm57UFVqmQwTkA2gT2JzAu9QEgQ1T` | 277420039 | 14/07 02:23:11 | 1,300 | 1,498 | 7,52 | 0,1 | 0,00 |
| 335 | `8yjL1D79xazL7rvbDQFYhvBxcNDfG4WXYqoefXiGgnMk` | 277420040 | 14/07 02:23:11 | 0,990 | 1,119 | 0,99 | 4,4 | 0,00 |
| 336 | `CsnzQtFhxd6RzKbiKiyohJv2kYYAF5ts48ziAYgJbn4A` | 277420041 | 14/07 02:23:11 | 0,100 | 0,112 | 0,60 | 0,0 | 0,00 |
| 337 | `HsHE9BLPN9ez1dJpTq8V3KNMXz7oBKNqmxzok3FzGKpH` | 277420061 | 14/07 02:23:20 | 0,028 | 0,032 | 0,03 | 0,1 | 0,00 |
| 338 | `86xcR6bSt4rCcmWwZDJ2tKK39chd6Bf1cwwEbUk2f9QM` | 277420073 | 14/07 02:23:25 | 0,070 | 0,078 | 0,07 | -0.0 | 0,00 |
| 339 | `GaoGtbyaE9Z9r5jtcWXdziCGYfMusPTWPGdii7FN78xh` | 277420075 | 14/07 02:23:26 | 0,050 | 0,056 | 0,15 | 0,0 | 0,00 |
| 340 | `2iebKWyaWiJHauqoyheBB3R2nsQhXT8Q8GDHmVT9Ey2p` | 277420094 | 14/07 02:23:35 | 0,100 | 0,121 | 0,10 | -0.1 | 0,00 |
| 341 | `Cxmyq2nwYWMvnuw5WqSRcmqLpWvJVM584E16wSpCHnNB` | 277420102 | 14/07 02:23:39 | 0,630 | 0,719 | 1,33 | 0,1 | 0,00 |
| 342 | `2Dh3t3kWYc9GoRiSKkgbwkSDc36MGFQaXpxCW1hHAu7A` | 277420108 | 14/07 02:23:42 | 0,495 | 0,560 | 6,19 | -1.2 | 0,00 |
| 343 | `FTzRk28MLQk23ZbvgPmgAhyBcPNRuAeEcXfmuDySjMTB` | 277420115 | 14/07 02:23:44 | 0,070 | 0,079 | 0,07 | -0.0 | 0,00 |
| 344 | `D6pmupjtXBKTtbvjfxQyA3uE47Fo8sEJ2ViRz1ZtCoRs` | 277420120 | 14/07 02:23:47 | 1,000 | 1,115 | 10,80 | 5,6 | 0,00 |
| 345 | `9At8NQvVCGtfan7xKrsTZfWojyHNFqGxiuVx4MHP3HSV` | 277420120 | 14/07 02:23:47 | 0,500 | 0,551 | 0,50 | 0,0 | 0,00 |
| 346 | `8C3AJ16RPgRkhG1fgi1p8rcLdD2UWw3uE2ZaJCg3ZwLB` | 277420124 | 14/07 02:23:49 | 1,000 | 1,077 | 1,20 | -0.5 | 0,00 |
| 347 | `BXwai7Pn4zoPgTVNpUxTc5QZgd1UqgAoPVdGCamnFS5n` | 277420133 | 14/07 02:23:52 | 0,100 | 0,108 | 0,10 | 0,0 | 0,00 |
| 348 | `4xnhWkWmZooxQuSNefSfk45ehbESaZCcGEasJAwnB93P` | 277420135 | 14/07 02:23:54 | 1,000 | 1,074 | 1,00 | 0,0 | 0,00 |
| 349 | `GSgUZ1gMbfAuF96YPJjiKxDwjwFPJE5puoVqgmCYb6ee` | 277420157 | 14/07 02:24:02 | 1,000 | 1,057 | 3,50 | -0.2 | 0,00 |
| 350 | `8n5ZGuxajCMnwtY3VqMY7SKcxZxPyPo9JvnSUFkP1i4B` | 277420168 | 14/07 02:24:07 | 0,010 | 0,010 | 0,01 | -0.0 | 0,00 |
| 351 | `6spRNyhG4BdrYomcT7PLEYAJ9NdzmC15dvcS8VNfNrce` | 277420172 | 14/07 02:24:09 | 0,050 | 0,052 | 0,22 | 0,0 | 0,00 |
| 352 | `5Cwu2AaFLAdsn9QTQjn5ixPD3DcPNXsXn1knKLixjwGZ` | 277420192 | 14/07 02:24:17 | 0,060 | 0,061 | 0,11 | -0.0 | 0,00 |
| 353 | `Db8dUBPw8KhEVsrbW3mzwzEPVXDXBmGV3h11yrDcUXZj` | 277420200 | 14/07 02:24:21 | 0,200 | 0,202 | 0,20 | -0.0 | 0,00 |
| 354 | `CcnX32yqNXtFMbL5JPth8WAcb37FuxXBMEvjB6bbwiA5` | 277420208 | 14/07 02:24:24 | 0,099 | 0,100 | 0,10 | 0,0 | 0,00 |
| 355 | `AGmyWHVgewAQTL7FMXJiPRG5xRmsohKFqTaPciEkcKJP` | 277420221 | 14/07 02:24:30 | 0,040 | 0,041 | 0,08 | -0.0 | 0,00 |
| 356 | `9nJMnsVMoCuVR1b7W8FjBVYAA5yD2ma62ZHK2sR3yKHF` | 277420225 | 14/07 02:24:32 | 0,500 | 0,505 | 0,50 | -0.0 | 0,00 |
| 357 | `6UA1gDRXTofu9znraV551mouy3b6EaKWHfC9oN9AkA7L` | 277420246 | 14/07 02:24:42 | 0,890 | 0,934 | 2,15 | 1,2 | 0,00 |
| 358 | `3vgcY7dtWmyLGuouDufGkeXmqkAQwZNcDTuqB7XG6gyL` | 277420254 | 14/07 02:24:45 | 0,200 | 0,209 | 0,20 | -0.1 | 0,00 |
| 359 | `BFkzwjwxfjkDMMRWSj4XS9Gxu79AWvge7UsYB1beSp3R` | 277420255 | 14/07 02:24:45 | 0,250 | 0,260 | 0,25 | -0.0 | 0,00 |
| 360 | `Ek3W2sNPsyjq9HazPB7RZXR4c3Zkt3yGFQq4jWwrCM9S` | 277420265 | 14/07 02:24:50 | 1,000 | 1,030 | 1,00 | 0,5 | 0,00 |
| 361 | `HvUXQHZmWs9eUQwYB2pABTFshMjVpAQMFfwBRpvZoouP` | 277420268 | 14/07 02:24:52 | 0,006 | 0,006 | 0,09 | -0.1 | 0,00 |
| 362 | `7skZC9vuCa2CKuWezcQJtVtjtwPtcQY6FtCFLM5YMUP2` | 277420272 | 14/07 02:24:53 | 0,250 | 0,252 | 0,25 | -0.0 | 0,00 |
| 363 | `FFyMNEHpz2Qfo4UUmGWuHhd8pahY3d32uZQRPcp1pDky` | 277420288 | 14/07 02:25:00 | 0,002 | 0,002 | 0,00 | -0.0 | 0,00 |
| 364 | `Bu1UD4EizxT3z1iWFmWDYb4SSivh48A4KBtxaLABzyj9` | 277420300 | 14/07 02:25:05 | 0,100 | 0,111 | 0,11 | -0.0 | 0,00 |
| 365 | `3wN8prQvW6gF6r3qjuMi3Yzgfh7cEw9m6bdBqLFq75ed` | 277420300 | 14/07 02:25:05 | 0,008 | 0,008 | 0,01 | 0,0 | 0,00 |
| 366 | `85jZzQo4sQtVZZg8Rxd9qM7Z6TXmjL54UTkZAkJhTQJb` | 277420300 | 14/07 02:25:05 | 0,540 | 0,597 | 0,66 | -0.4 | 0,00 |
| 367 | `GgMLFST1Vu2CWA3hkJcRtLhWCeVwZ6r5iyMNGH1aVsX3` | 277420313 | 14/07 02:25:11 | 0,205 | 0,226 | 1,22 | 0,0 | 0,00 |
| 368 | `Ea5nYiNKspnUdLLyXwuxXfvjNfe1mbZfQjdiiM8mRzBp` | 277420320 | 14/07 02:25:15 | 0,100 | 0,110 | 0,10 | -0.0 | 0,00 |
| 369 | `5vLde7TcYj3xiXy31Ec2FZu17QBCeYzi9KoJrccQhVeP` | 277420328 | 14/07 02:25:18 | 0,050 | 0,056 | 0,05 | 0,0 | 0,00 |
| 370 | `Hp2wiZ9k2uGrwyPWrhvXhDiV4yWk7Kjj7EVgmrf2Y7P8` | 277420354 | 14/07 02:25:30 | 0,100 | 0,117 | 82,74 | 21,2 | 0,00 |
| 371 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 277420361 | 14/07 02:25:33 | 0,139 | 0,162 | 0,14 | 327,3 | 0,00 |
| 372 | `jhueu3HzbaUkzPztAZhjfsRjJ4osM5VZhpMY9C7Fm6Q` | 277420369 | 14/07 02:25:37 | 0,150 | 0,174 | 0,15 | 0,0 | 0,00 |
| 373 | `9RAPaAEy3Tf3jkpL7JEGH7qDe6ch95epJoseErUU7Mxw` | 277420402 | 14/07 02:25:51 | 3,000 | 3,410 | 3,00 | 1,0 | 0,00 |
| 374 | `FwRLa6dKFDHHDZyrHDwEzGMHZfdbZnbGukyRVdT5146r` | 277420414 | 14/07 02:25:56 | 0,099 | 0,110 | 0,45 | 0,0 | 0,00 |
| 375 | `7oNCuV8HAqFsz4PgSPgddYEKTxMqDh5Z6XiREmH9HrZT` | 277420440 | 14/07 02:26:08 | 0,300 | 0,360 | 8,90 | -0.5 | 0,00 |
| 376 | `CCBcV2cwG7nTY8Fp3xb3LAo1e6i2GTaw5wdz471sEXnJ` | 277420454 | 14/07 02:26:14 | 5,000 | 5,664 | 31,00 | 2,1 | 0,00 |
| 377 | `E3PNawBkU4rUbMj4sYa4mED2iW2Z1rHjcbQ4hMj5Wg9S` | 277420457 | 14/07 02:26:16 | 4,950 | 5,172 | 4,95 | 1,0 | 0,00 |
| 378 | `DBUn2QkCJBLE6n6rsQeDWUQWKVFPL6GUYy4fe7mKdeWx` | 277420458 | 14/07 02:26:16 | 0,495 | 0,516 | 24,75 | 2,9 | 0,00 |
| 379 | `E6F1DsZ2gf5jSbFrs9VKF1gyn1eGYbj8KWvqKYQrSNSm` | 277420467 | 14/07 02:26:20 | 0,099 | 0,105 | 0,15 | -0.0 | 0,00 |
| 380 | `8osetrvj4ZBTrMYkQb91dJyE7VFoAEqq76dXn9tvBzKD` | 277420492 | 14/07 02:26:30 | 0,200 | 0,210 | 0,20 | -0.1 | 0,00 |
| 381 | `CJwXN2p2sBDmvoztsBkYR7oCbZosyysXKtZAbMdDNyqV` | 277420510 | 14/07 02:26:38 | 0,500 | 0,530 | 0,50 | 0,3 | 0,00 |
| 382 | `2VX3Lg8Gbx3gco24tj4hBty7PfxMm8Lkd8yZbm9bbD8f` | 277420512 | 14/07 02:26:39 | 0,022 | 0,024 | 0,07 | 0,1 | 0,00 |
| 383 | `F65wH41YW9rFYtgsj1afj2kc7FZnnDVJTVyRwJzNRojM` | 277420525 | 14/07 02:26:44 | 0,100 | 0,105 | 0,28 | -0.0 | 0,00 |
| 384 | `6DTd7NYzdXtn8MFxzbAdCiokHVaJq9i1qp7iA8dWStUf` | 277420546 | 14/07 02:26:54 | 1,534 | 1,630 | 1,53 | -0.1 | 0,00 |
| 385 | `CtNQwrbEskXq5dw4A9evrsnj3FfGJZ8CvVsWWeTfGWK7` | 277420556 | 14/07 02:26:59 | 0,100 | 0,106 | 0,10 | -0.0 | 0,00 |
| 386 | `FaPBdnJkHVawUv56YHtk2Ycm9FPEF9chrLN4DoumT7be` | 277420565 | 14/07 02:27:02 | 3,000 | 2,993 | 3,00 | -0.9 | 0,00 |
| 387 | `DRTSJGapRuUzsYC9bFnnkSy7Mo3NNLPbxEz44VcFiyQ5` | 277420572 | 14/07 02:27:05 | 0,099 | 0,097 | 0,10 | 0,0 | 0,00 |
| 388 | `2YzLm31u8xcpfAC4CtGLiaabiLjzgFPz1EhUmKJ7d75J` | 277420587 | 14/07 02:27:12 | 0,010 | 0,010 | 0,03 | -0.0 | 0,00 |
| 389 | `2ostLDD9TdbR6dmjo8Ud28JMRRFj2QRmTWSFKZUBpxFV` | 277420598 | 14/07 02:27:16 | 0,100 | 0,100 | 0,10 | 0,0 | 0,00 |
| 390 | `54h3yeSoei8HJfmCTS96KFiCF7m3ht7MJF48rFqEA5J4` | 277420604 | 14/07 02:27:19 | 1,000 | 0,962 | 2,00 | -0.3 | 0,00 |
| 391 | `EypgXuKMS4AJKYaZpCLferBwzjKTzCuwQYob1ordafD6` | 277420610 | 14/07 02:27:22 | 0,440 | 0,419 | 1,19 | 0,0 | 0,00 |
| 392 | `6N87vLyvJzGpSEvFopsb3yw9VqddddArX1eHaYcLYzn9` | 277420612 | 14/07 02:27:23 | 0,100 | 0,095 | 0,40 | 1,4 | 0,00 |
| 393 | `4ppYLp6o7bkFVBVfXSmdqmNV9xN6Nc6L4rfLx2SWsem5` | 277420617 | 14/07 02:27:25 | 0,100 | 0,095 | 0,50 | -0.3 | 0,00 |
| 394 | `8tM1yVcLcWxeGG6j4CoQXcx4xmCWgfrFi2Gsmt6TdxMK` | 277420617 | 14/07 02:27:25 | 1,782 | 1,663 | 4,55 | 0,2 | 0,00 |
| 395 | `8hMaiwUDhDwHaV14HMnmgD76UyQNaFwWweAuYTh9x4jj` | 277420618 | 14/07 02:27:25 | 0,200 | 0,184 | 0,40 | 0,1 | 0,00 |
| 396 | `7wbE7UST6sFiRr6axkcz6BT2JnkWdbVsdHhjjnJk6K5y` | 277420631 | 14/07 02:27:31 | 0,090 | 0,083 | 0,09 | -0.0 | 0,00 |
| 397 | `4HB4SJyeLoHpr1EAqxk5ZCswR8SaT8cMQJ2f8mAyQnE9` | 277420638 | 14/07 02:27:34 | 0,070 | 0,064 | 0,07 | 0,0 | 0,00 |
| 398 | `9hevMZ83xbm6VZLobxmraf1pD4mESjPz4Hu6PvnWbCpA` | 277420646 | 14/07 02:27:39 | 0,143 | 0,138 | 0,25 | -0.1 | 0,00 |
| 399 | `ALvNd3nTN4ZrigqjQxmTdoSxqEwpppbwK61AHggDE6Y6` | 277420647 | 14/07 02:27:39 | 0,150 | 0,145 | 1,15 | 2,3 | 0,00 |
| 400 | `xKuKXXJfBp4X1o9oazgjY3JpjAB2Jzh5rWWM54qvUaP` | 277420648 | 14/07 02:27:40 | 0,500 | 0,481 | 0,50 | 0,0 | 0,48 |
| 401 | `6q8gqyrkmdczhJGWjYb7Xs7oskMiSDxchsBybjdPvhhq` | 277420653 | 14/07 02:27:42 | 0,030 | 0,029 | 0,03 | -0.0 | 0,00 |
| 402 | `8ud34byCVSK4AFutfvq6WWRzsJGCf4You3m9adL88x8D` | 277420656 | 14/07 02:27:44 | 1,000 | 0,975 | 4,80 | -0.8 | 0,00 |
| 403 | `B4rr51J5bRPE3nkaRge66ZPztfCF3nZRREFCjQxfhcRs` | 277420657 | 14/07 02:27:44 | 0,099 | 0,096 | 0,10 | 0,0 | 0,00 |
| 404 | `G6rBMbdvdcNRUK1ujh9UCwDKkkgZwRLwv4WeDjPhMZH6` | 277420661 | 14/07 02:27:45 | 0,035 | 0,033 | 0,03 | 0,0 | 0,00 |
| 405 | `3zVjzpjGUsUVnqoZeosinwTTT1uueXA4diJ6X25NRraY` | 277420663 | 14/07 02:27:47 | 0,250 | 0,222 | 1,50 | -0.4 | 0,00 |
| 406 | `GXUZs9pmnZJbfbfApTaRyGnzBkZgoVzC5MHUW3D5jRfS` | 277420668 | 14/07 02:27:49 | 0,435 | 0,376 | 0,96 | -0.0 | 0,00 |
| 407 | `32XpSnGBFbgqFGGXAgZu1B5a3efBp3KcwEVvUubQU9J6` | 277420703 | 14/07 02:28:04 | 0,040 | 0,033 | 0,12 | -0.0 | 0,00 |
| 408 | `E1L9bRozAvChY9igWf1sK6kwZsdbBWt7MneQdg59Y1ja` | 277420712 | 14/07 02:28:08 | 0,800 | 0,665 | 1,30 | -0.3 | 0,00 |
| 409 | `7Mn5TmuuQyafDkE2KdzrXbJy5bFAnqF2q1xQ3cu5pSGW` | 277420720 | 14/07 02:28:11 | 0,200 | 0,165 | 0,20 | -0.1 | 0,00 |
| 410 | `7mMVsDdKykG31CWL5nvqS1zwHnQokmoV6Cx3LV24bvom` | 277420720 | 14/07 02:28:11 | 0,500 | 0,407 | 0,50 | -0.1 | 0,00 |
| 411 | `58PTVL55i7x5zrGU56KKha8A61voXaxqrfpU7sGxGo8t` | 277420721 | 14/07 02:28:11 | 0,500 | 0,408 | 0,50 | -0.3 | 0,00 |
| 412 | `ByL8BxkGHhgRhzMqimsaZuxyAPNFZYhYTaQkxLpD564f` | 277420729 | 14/07 02:28:14 | 1,000 | 0,817 | 1,00 | 0,1 | 0,00 |
| 413 | `FG3522tEiaNYeDvM2BPXG8kFXFE65emXREqGyFdsCpwk` | 277420736 | 14/07 02:28:18 | 1,000 | 0,799 | 1,00 | -0.6 | 0,00 |
| 414 | `FnsRitJKgMF9tjgZ85dBZeBwqppD2THqs85UL8da81rE` | 277420750 | 14/07 02:28:23 | 0,163 | 0,132 | 0,16 | -0.1 | 0,00 |
| 415 | `EvAS1VtQ2QPxruqbx5QpWN1v3yy3EFMzwcKCL9QSCKhq` | 277420755 | 14/07 02:28:26 | 0,050 | 0,040 | 0,05 | -0.0 | 0,00 |
| 416 | `ANwEEjSZKJvEuU64bPQ6Nbhey27wrY2rzWuTJjjffqDA` | 277420755 | 14/07 02:28:26 | 1,000 | 0,803 | 1,50 | -0.8 | 0,00 |
| 417 | `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` | 277420756 | 14/07 02:28:26 | 4,000 | 3,079 | 4,00 | 30,3 | 0,00 |
| 418 | `2H1n9wQyhbFR5ugsxy6UQ6SnN85gM4oa7oVrFsEWNQXj` | 277420764 | 14/07 02:28:30 | 1,000 | 0,761 | 11,50 | 40,2 | 0,00 |
| 419 | `Hyvoj1rP9FCg8ozUBpArZVomDoGwTmbdxDWPE2dtr62C` | 277420764 | 14/07 02:28:30 | 2,000 | 1,493 | 2,00 | -1.7 | 0,00 |
| 420 | `GSMBgqdmzBsASToeqeL8f5Vfjqzc8ceJ38PBZae5e8nT` | 277420780 | 14/07 02:28:38 | 0,050 | 0,036 | 0,05 | -0.0 | 0,00 |
| 421 | `7XeLd1ppzkzYUU9kHjgxEG5aQTKiRGT6wmSD45aoALmb` | 277420781 | 14/07 02:28:38 | 0,099 | 0,073 | 0,10 | 0,2 | 0,00 |
| 422 | `GmnrkNZkmXuSAir3YmGrfvPvgudcofFZtZPTLwtFPYqz` | 277420781 | 14/07 02:28:38 | 2,000 | 1,451 | 4,00 | -1.1 | 0,00 |
| 423 | `2GgZRVYA51EG9zDf7zkMpDvXYXjN5dJswpaNAfsyA7z2` | 277420788 | 14/07 02:28:41 | 2,000 | 1,413 | 4,70 | 0,4 | 0,00 |
| 424 | `GKhzbG7pPCFoBDARJkjLQ8QuhebfDYXoPP3UrwtWe7B3` | 277420796 | 14/07 02:28:45 | 1,000 | 0,703 | 1,00 | -0.1 | 0,00 |
| 425 | `EDnYsFRLcRuEeJ9sothVZdqgK9j7UCA2SN6uHRJUkFsq` | 277420800 | 14/07 02:28:47 | 1,000 | 0,697 | 1,00 | -0.1 | 0,00 |
| 426 | `GzdemcN4NnMiFreLJXUKzmzEy9oUUzsjWUuA9Jsfbj5f` | 277420800 | 14/07 02:28:47 | 0,250 | 0,173 | 0,75 | -0.3 | 0,00 |
| 427 | `12G3w5qmS93Jh3L5joVTQTZgWJcgJkDSR979eWvytwxa` | 277420813 | 14/07 02:28:52 | 0,100 | 0,069 | 0,20 | -0.0 | 0,00 |
| 428 | `PcAMtGKiGTzGPibyJK6ZG8mBRRqa8XjZo8eGsMHHLi6` | 277420813 | 14/07 02:28:52 | 0,010 | 0,007 | 0,01 | -0.0 | 0,00 |
| 429 | `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` | 277420821 | 14/07 02:28:56 | 4,197 | 2,864 | 281,19 | 1 747,8 | 0,00 |
| 430 | `DFtiPdqGAuNjfx8tciKLrBEfrJVeW3kGhiAhvTpiKVP7` | 277420852 | 14/07 02:29:09 | 0,110 | 0,078 | 19,76 | 29,2 | 0,00 |
| 431 | `EKpM4VqEehCEF9chkR6LrsXeM1iRbTdTfNDydWs3X3CC` | 277420860 | 14/07 02:29:12 | 0,050 | 0,035 | 0,05 | -0.0 | 0,00 |
| 432 | `65bNEfgr5msaHewx9vZbPauJ2bb7LSVymMkBb4HNBEcU` | 277420861 | 14/07 02:29:12 | 0,445 | 0,317 | 0,45 | -0.2 | 0,00 |
| 433 | `Hofpy8WmVsUsUGpTEHdT2HEoQe9pWNmNvgm9GqW7peo9` | 277420869 | 14/07 02:29:16 | 0,004 | 0,003 | 0,00 | 0,7 | 0,00 |
| 434 | `HcA1h8YG1MLFV5woGZM1zF3SCBy1qBsuDxscJHkbDsPS` | 277420874 | 14/07 02:29:19 | 0,007 | 0,005 | 0,01 | -0.0 | 0,00 |
| 435 | `GzMXM4YHmtkhDddmL7NC2DGBQJjaqBZBkEp3W3a4XiTe` | 277420874 | 14/07 02:29:19 | 1,500 | 1,061 | 42,81 | -0.5 | 0,00 |
| 436 | `4MKESGhF7q1bdzaYUuR2oWr3pJx5oPKxqQYwGbQybmEW` | 277420875 | 14/07 02:29:19 | 0,008 | 0,006 | 0,01 | 0,0 | 0,00 |
| 437 | `EjdSPgWLHg3GaDgqyhkHeD88dXg2HUqfbtjEVXoPBV5o` | 277420884 | 14/07 02:29:23 | 0,100 | 0,070 | 0,10 | -0.0 | 0,00 |
| 438 | `9tMC5pPoQ566JURYRA7HmSJbhipmQ5xXwu6BKbgS5cG1` | 277420893 | 14/07 02:29:27 | 0,020 | 0,014 | 0,02 | -0.0 | 0,00 |
| 439 | `GpmYqfDwY2Q5GKYTRzz9oGV38ZuCeZ9SwNEBYGVjSDVn` | 277420923 | 14/07 02:29:42 | 0,495 | 0,371 | 0,49 | -0.2 | 0,00 |
| 440 | `5NQWpTcFUUSXs6Rw2fWE732Tv9FRBXnArbYt6Xcwyrbw` | 277420928 | 14/07 02:29:45 | 0,028 | 0,021 | 0,10 | -0.0 | 0,00 |
| 441 | `Bs7Gp1gfRAQPhADv7udyupHPAtP5ZFtwc4ne7NdTt86Q` | 277420934 | 14/07 02:29:47 | 0,500 | 0,368 | 0,50 | -0.3 | 0,00 |
| 442 | `AAWrpdJG9ykAFpyPUSq7wdWrfbVy6kbRvGM4JCm2rp62` | 277420934 | 14/07 02:29:47 | 0,247 | 0,183 | 0,25 | -0.2 | 0,00 |
| 443 | `5B54xeBdJ7mLT78tJAGmJB2a7Nqa24oZYNgxU6t9jNRz` | 277420934 | 14/07 02:29:47 | 0,100 | 0,074 | 0,10 | -0.1 | 0,00 |
| 444 | `53Rk9vHqHDYN9sf6g4CnMqCcm1B4nhkY9wc3oaXP46NP` | 277420948 | 14/07 02:29:54 | 2,300 | 1,731 | 2,30 | -1.1 | 0,00 |
| 445 | `6iDRWu5MvJP8EcyFqBDqpC1SkGW1PtzRnhe4MrzCigJ1` | 277420951 | 14/07 02:29:55 | 0,035 | 0,026 | 0,17 | -0.1 | 0,00 |
| 446 | `BHQeqgnbgmx2T4mD3BZjNmxArKABRjXsjCuhYC5wJeBe` | 277420960 | 14/07 02:29:59 | 0,200 | 0,147 | 0,40 | 3,4 | 0,01 |
| 447 | `dc5cfqYJ312QL35fu9oZwrs5CxgQVh646TFPGTs3P6J` | 277420994 | 14/07 02:30:13 | 0,100 | 0,074 | 694,57 | 1,3 | 0,00 |
| 448 | `4Mcyd8HKz92VJQ1VUPSnSbGUcPax8Pay71pArzrFUvHn` | 277421009 | 14/07 02:30:19 | 0,050 | 0,037 | 0,13 | -0.0 | 0,00 |
| 449 | `HSReKCXSztVWqT8SbPFSw3fCw1iDwZPAh1C4vigXsJD2` | 277421029 | 14/07 02:30:28 | 0,010 | 0,007 | 0,75 | -0.1 | 0,00 |
| 450 | `9ShDwsTK2e8sC6dVwNFH9fvco7fbLrRMT7tY8WJvKpZQ` | 277421029 | 14/07 02:30:28 | 0,076 | 0,056 | 0,14 | -0.1 | 0,00 |
| 451 | `4wpyRXpeLdsREDxFwKCD89YXxK8yxXF9rNrWzwpjFEgS` | 277421029 | 14/07 02:30:28 | 0,010 | 0,007 | 0,02 | -0.0 | 0,00 |
| 452 | `ENtbEDyUXQRDpqqXovz9gHjSZn6oPjwFN3zcoz1SubiR` | 277421032 | 14/07 02:30:30 | 0,200 | 0,149 | 0,20 | -0.1 | 0,00 |
| 453 | `54Mc8dg48t29uyRy4d1QuyUYL4vrJHbvqouhjbnFK2WQ` | 277421041 | 14/07 02:30:34 | 0,030 | 0,024 | 0,18 | -0.1 | 0,00 |
| 454 | `55K4o83uaBwVSR4W7ocUTjBb6zocAFtkahqkJPsLFy4P` | 277421047 | 14/07 02:30:37 | 4,643 | 3,616 | 4,64 | -2.4 | 0,00 |
| 455 | `Djb17FNiBgBGKcFf9HJoJmFr4G9TsACrwmyVfb7uqVnV` | 277421050 | 14/07 02:30:39 | 0,005 | 0,004 | 0,01 | -0.0 | 0,00 |
| 456 | `6xsRjCUcLQxnR2Fz5o5mb38x5Zorb4PAaJrDSHU2LVsw` | 277421073 | 14/07 02:30:48 | 0,050 | 0,041 | 0,37 | -0.1 | 0,00 |
| 457 | `3gQSpr3CQ94pUBNk3kYdmqkJUfy64BGydAqdyfNY1HVM` | 277421079 | 14/07 02:30:51 | 1,000 | 0,875 | 1,00 | 11,0 | 0,00 |
| 458 | `BpkyJcQ9jha62ztMz4rFHwy9q2Jai9QDkUkM7NCXBrZy` | 277421080 | 14/07 02:30:52 | 0,150 | 0,129 | 0,15 | -0.1 | 0,00 |
| 459 | `GwZyyPMRmdNCMyUmSyVz4X6uuUNfSW6iHmseS2mXS71C` | 277421080 | 14/07 02:30:52 | 1,000 | 0,861 | 3,00 | -0.3 | 0,00 |
| 460 | `27eBjiCk1FVbRbGjCsdPZsKAD1JivQcSaDHHy8kEtwKB` | 277421092 | 14/07 02:30:58 | 0,040 | 0,036 | 0,04 | 1,0 | 0,00 |
| 461 | `5iP3wAQdcNrwuGBbeZaBtAa84yGq2KkRihTHGU6MpmxY` | 277421116 | 14/07 02:31:09 | 0,079 | 0,072 | 0,08 | -0.0 | 0,00 |
| 462 | `6LUMUNUcN7V6U2DRWSGPJqLAaoqPZEYdg4yBRMSGyqz` | 277421144 | 14/07 02:31:22 | 0,100 | 0,098 | 0,10 | -0.0 | 0,00 |
| 463 | `8C6eo97Vy6S1qNPLXyP3XfMTv3mWeCjWJdNhVMfq6tQb` | 277421169 | 14/07 02:31:32 | 0,250 | 0,291 | 0,25 | -0.1 | 0,00 |
| 464 | `5VKFnP1NMqs2TRPbzXVhaJ7zjnC9mofU85SiMLbH7NYV` | 277421169 | 14/07 02:31:32 | 0,198 | 0,232 | 0,35 | 0,0 | 0,00 |
| 465 | `DpKnca3xCxNm29GvMrLtuXRYjHC5cTdaffu2abDGszHN` | 277421196 | 14/07 02:31:46 | 0,750 | 1,153 | 0,75 | -0.0 | 0,00 |
| 466 | `8466CpDxsDC2k2yV2xbeUnvnwHzzLjzT8tJrzowiN8Hf` | 277421197 | 14/07 02:31:46 | 1,000 | 1,534 | 1,60 | 19,4 | 0,00 |
| 467 | `8Qrc6dYrTpuHuAvicPt5M7v24YpNTBugyBoQ6AZxzxCd` | 277421200 | 14/07 02:31:48 | 0,100 | 0,152 | 0,10 | 0,0 | 0,00 |
| 468 | `9jxuQStKiW1AsLTDEgeXzb9sF1m6MyTBzyxzovJzMEAb` | 277421204 | 14/07 02:31:50 | 0,500 | 0,788 | 1,25 | 0,1 | 0,00 |
| 469 | `6TTdRW9SFygtxCp34yoNymMWU7ipkfRemPMcmWSjphpP` | 277421233 | 14/07 02:32:03 | 0,689 | 1,183 | 1,59 | -0.5 | 0,00 |
| 470 | `CVuSwLJZXqtBZMA51DNtQ8Hh8QCUuWzBiGdpk5RBvMXW` | 277421251 | 14/07 02:32:10 | 0,200 | 0,353 | 0,40 | 0,1 | 0,00 |
| 471 | `8cFsF9a3e5nVtdffFxdguD2vwuHZFXG6NYgxBPNosQVa` | 277421253 | 14/07 02:32:11 | 1,000 | 1,707 | 1,50 | -0.5 | 0,00 |
| 472 | `E4ycsWzjaA43vfhmRJ1gcMo5wb8fZcBm1S4Te3nT77St` | 277421257 | 14/07 02:32:13 | 0,990 | 1,627 | 0,99 | -0.0 | 0,00 |
| 473 | `93zz7MS6NVKPk2vrVBKMqhzSbXELT2pAVWMMTgjRXDWp` | 277421282 | 14/07 02:32:23 | 0,846 | 1,471 | 2,30 | -0.5 | 0,00 |
| 474 | `GgZdaBTyaghebGJj3ukkz772AmMFVNv2Ti847JXiXhr8` | 277421285 | 14/07 02:32:25 | 2,970 | 4,953 | 2,97 | 0,5 | 0,00 |
| 475 | `8eMWNRmYzHymEnSQDa6w7gKLBjRAPTrQQNcRS2yLPfxm` | 277421296 | 14/07 02:32:31 | 0,500 | 0,819 | 0,50 | 0,2 | 0,00 |
| 476 | `5FufKgV9nRpNTDrVWHjovKH4hJ5xWtd6bYNwDAKQ9qmo` | 277421298 | 14/07 02:32:31 | 0,900 | 1,450 | 0,90 | 0,0 | 0,00 |
| 477 | `7HxZfDgSY26PocqQP52xputuchMahLXfNM3vsyrZ4NKH` | 277421308 | 14/07 02:32:36 | 0,560 | 0,872 | 0,56 | 0,0 | 0,00 |
| 478 | `9MqCSKTQp8YuZkzrexTeycBhj5jCmNTNiPPgvUTgsSVz` | 277421336 | 14/07 02:32:50 | 0,200 | 0,288 | 0,20 | 0,0 | 0,00 |
| 479 | `8vNCHXxdfXzJyJGGDgrHgisN6eenpMuHEJU2DF3q9iHx` | 277421337 | 14/07 02:32:50 | 0,871 | 1,243 | 4,04 | 0,4 | 0,00 |
| 480 | `84Buo3mAnNvZE9paeF2Dd469Exyc23GEh4Ypp3GYRvL` | 277421345 | 14/07 02:32:54 | 0,200 | 0,297 | 14,40 | 63,7 | 0,00 |
| 481 | `CUiKhR4bjEwoe8xRuDmTB55tfwkbKe1VNhEpCeF1ykZy` | 277421347 | 14/07 02:32:55 | 0,099 | 0,147 | 0,10 | 0,0 | 0,00 |
| 482 | `uSyK3b2c6fMEnMiQzFM5UAP7F64CTXRU1zmbBiDMFfC` | 277421359 | 14/07 02:33:01 | 0,337 | 0,495 | 0,34 | 0,2 | 0,00 |
| 483 | `3vntK4bvdF1dQzEu7xyJSmoTKY6SPnxMu2efkM66UZZj` | 277421360 | 14/07 02:33:02 | 0,050 | 0,075 | 0,15 | -0.0 | 0,00 |
| 484 | `7RVuuYrRmnjiKsLU8vxdNAQSmia8faiBypaVi4i79WXE` | 277421411 | 14/07 02:33:24 | 0,050 | 0,073 | 0,05 | 0,0 | 0,00 |
| 485 | `2wPj1dRc66sfhnRRyR2J9JCLK3D8JigEv66rJHD9vER3` | 277421428 | 14/07 02:33:32 | 1,000 | 1,460 | 2,00 | -0.4 | 0,00 |
| 486 | `5SERykT6AjkyS6QVfxFEBkLejFvsbqaGrJMCy5GsGQHi` | 277421433 | 14/07 02:33:34 | 0,100 | 0,144 | 1,10 | 0,0 | 0,00 |
| 487 | `BsJaQmvNgtuYKGnYWRCiKxMayJt6vGjHJB1myhG8nhzf` | 277421438 | 14/07 02:33:36 | 0,229 | 0,329 | 0,23 | 0,1 | 0,00 |
| 488 | `FXMCXYRKrt157PArCREDNoqeFnpQ89oYmmMsMqc9xMQs` | 277421446 | 14/07 02:33:39 | 0,390 | 0,568 | 10,54 | 2,2 | 0,00 |
| 489 | `EbMsz19CroR1RxtGNreXpTkMSnraZKDdT8UY68F346Kr` | 277421447 | 14/07 02:33:40 | 0,008 | 0,012 | 0,01 | -0.0 | 0,00 |
| 490 | `21rXzC52d6Wxtg85djmNaCTJoA4Syeo871zn5Nqa5cfE` | 277421456 | 14/07 02:33:45 | 0,100 | 0,147 | 0,30 | 0,0 | 0,00 |
| 491 | `47LQa9bG31scTZ6ksxYRAqZmKSTsxFB9SrWomzoFkffq` | 277421461 | 14/07 02:33:47 | 0,200 | 0,294 | 0,20 | -0.1 | 0,00 |
| 492 | `4yWHYBYNgmsnYRc2xnPB9GV8EYTanzNuuqqsVYQ2QNUv` | 277421461 | 14/07 02:33:47 | 1,000 | 1,452 | 1,00 | -0.3 | 0,00 |
| 493 | `DkWNuPd9Yzf6qoQ4y9DPqu37krFuWoxtD4CHsiXdjXRm` | 277421472 | 14/07 02:33:53 | 0,100 | 0,138 | 0,10 | -0.0 | 0,00 |
| 494 | `HBb79m4q9iPSAir4KUqaPd2boCxorFNYptNXa6gGG7ag` | 277421484 | 14/07 02:34:00 | 0,030 | 0,043 | 0,03 | -0.0 | 0,00 |
| 495 | `CdD1XPF7oitjEQJV9J6mCrDVoQEjF3G5FBtG1LcDddq3` | 277421501 | 14/07 02:34:06 | 0,028 | 0,040 | 0,11 | 0,0 | 0,00 |
| 496 | `BgHGYp1adY1NyHch3MocgCWhm1KDjVGbLFxZyLv3mKpK` | 277421519 | 14/07 02:34:17 | 0,200 | 0,311 | 4,20 | -0.6 | 0,00 |
| 497 | `92xAv7vJ8aeEXcvRaEdgDbKS9JRJm33q4b643aTbd3NV` | 277421525 | 14/07 02:34:19 | 0,200 | 0,300 | 0,20 | 0,0 | 0,00 |
| 498 | `Er7g5kLJboyPfcAPxwFVnPzt9BcyX5tf4qhhNkV4HWfg` | 277421548 | 14/07 02:34:30 | 0,200 | 0,304 | 1,50 | -0.1 | 0,00 |
| 499 | `5x4JHRoJEB7buXaKRpFxr4qtuXaY8YGiRXqrVYUovtih` | 277421554 | 14/07 02:34:31 | 5,000 | 7,014 | 13,50 | 3,6 | 0,00 |
| 500 | `BzWERBEwhDC93ZPAT1GmGN7CK7CMzymW4PxgSTdqh6rf` | 277421572 | 14/07 02:34:40 | 0,247 | 0,361 | 0,25 | 0,1 | 0,00 |
| 501 | `Gjeufiib8f6LeeMT7JQ3zjmq9MGRPqHiakB35syfSp1A` | 277421572 | 14/07 02:34:40 | 0,050 | 0,073 | 0,24 | -0.1 | 0,00 |
| 502 | `F2kcbXTMKcZZ9ufCarAo4FmCf9M184sDD12TGiKMgYfQ` | 277421581 | 14/07 02:34:43 | 3,000 | 4,400 | 88,42 | 705,8 | 1,10 |
| 503 | `61zL6bXggckHyyPxP13Xi9hUEBFD3SfL1enx1dE5hhfT` | 277421592 | 14/07 02:34:49 | 5,000 | 6,531 | 170,00 | -2.6 | 0,00 |
| 504 | `3cACjXwjnGzfQq3GvN3ThzC9M8maH1ZuSDjKUMn1gaoV` | 277421613 | 14/07 02:34:59 | 0,010 | 0,013 | 0,01 | 0,0 | 0,00 |
| 505 | `E23s7RPXSm84DDhzuzBMU2ATctYoenv9TSvYZ9k7jNQ3` | 277421640 | 14/07 02:35:12 | 0,150 | 0,200 | 0,15 | 0,0 | 0,00 |
| 506 | `3MGR1WrnnLCV9yCeWX7uZicBqciWqa4MAmiro4q56dX8` | 277421653 | 14/07 02:35:17 | 0,310 | 0,410 | 0,31 | 0,0 | 0,00 |
| 507 | `GzGmeK74BeySXa5g1ePQW6C69vyptVbKcmZXZmcvsWcM` | 277421665 | 14/07 02:35:23 | 0,050 | 0,061 | 0,05 | 0,0 | 0,00 |
| 508 | `Ee73qvWwtwUPVsbZTKn7GX2dvRdDfTARDm9ZZctgJEEb` | 277421678 | 14/07 02:35:28 | 0,099 | 0,121 | 0,10 | 0,0 | 0,00 |
| 509 | `G1KE5Qc2qF85k2V8BfWLoXBeft5AHVqrFemGiAd5uvue` | 277421726 | 14/07 02:35:51 | 0,050 | 0,061 | 0,05 | 0,0 | 0,00 |
| 510 | `8Cwp2QJQ7UGeZgUTua8vKXTQXYu5JhZwekRRTpm5B6EE` | 277421794 | 14/07 02:36:22 | 0,150 | 0,194 | 0,15 | -0.0 | 0,00 |
| 511 | `6ZMaqHjPYpPdYor9qNGJP7bmunaFCuWcDVjDkR5H3b1J` | 277421795 | 14/07 02:36:22 | 0,950 | 1,218 | 50,95 | 124,5 | 0,00 |
| 512 | `DtWoHwwMDEV9pg1mFHSaPKViJ65whA8quBDqgFYWGNvn` | 277421830 | 14/07 02:36:38 | 0,341 | 0,442 | 0,94 | 58,4 | 0,00 |
| 513 | `FSPkK6ZrMyGtgqoVwsBAYaespjVTHcZfMbQ3jtefY9G1` | 277421844 | 14/07 02:36:45 | 0,423 | 0,544 | 0,42 | -0.2 | 0,00 |
| 514 | `HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ` | 277421850 | 14/07 02:36:47 | 0,950 | 1,322 | 0,95 | 0,0 | 0,00 |
| 515 | `32UdKXcJL5Ncxp72ebxMQCYSv2VMyvh5hsJ2SEjFDezH` | 277421890 | 14/07 02:37:04 | 6,117 | 8,719 | 6,12 | -1.5 | 0,00 |
| 516 | `CVhCttyPw9asFQsqUD1h7LRh3TQnnHNSdxXzdeyxsQDy` | 277421923 | 14/07 02:37:19 | 2,902 | 3,833 | 4,44 | 1,1 | 0,00 |
| 517 | `F7RPEsYjGsrBjFHVyTEo6vt8edm4YT5CpoT7VV7Cx4nN` | 277421965 | 14/07 02:37:39 | 0,026 | 0,034 | 0,03 | -0.0 | 0,00 |
| 518 | `64xtWDYWyyPSWZVwFJTRdr7g38K4NPiqfytsz6nF7zGW` | 277421987 | 14/07 02:37:48 | 0,990 | 1,237 | 0,99 | 0,1 | 0,00 |
| 519 | `4QHS1Ln6Yv1zvwWfP4GEN6Wo3XqGU6iHH75xt94WmzUJ` | 277422011 | 14/07 02:37:59 | 0,100 | 0,123 | 0,10 | -0.0 | 0,00 |
| 520 | `4aBEsjbfGKoGmK6Rb48YNmtZSRCkKAuKWbhFtUEB61Y1` | 277422061 | 14/07 02:38:20 | 0,144 | 0,169 | 0,90 | -0.0 | 0,00 |
| 521 | `FQvLXcKvM6y3w853b91y7KF1UG2PJT6gTj4ojSrrCEDX` | 277422069 | 14/07 02:38:24 | 0,030 | 0,035 | 0,03 | 0,0 | 0,00 |
| 522 | `8RnGzGyU14zF2MrQ526ozVkJK94SMhEk4JZphpJp21i9` | 277422072 | 14/07 02:38:25 | 0,100 | 0,116 | 0,10 | -0.1 | 0,00 |
| 523 | `7zgjeB1t2GXDwvDGq8sFM5QFzpQBKEL5jRWxrS6Xb9pk` | 277422077 | 14/07 02:38:27 | 1,000 | 1,161 | 67,44 | 311,5 | 0,00 |
| 524 | `71ukLMgHyok4cEJsQFyuk37QNW1CchPngtzD1CzVmCHF` | 277422144 | 14/07 02:38:58 | 0,500 | 0,554 | 0,50 | -0.1 | 0,00 |
| 525 | `4MZ91kW6XVCsEfVLyZFZ4mev6WaVDMax2XHBAfYem2xf` | 277422162 | 14/07 02:39:06 | 0,070 | 0,078 | 0,07 | -0.0 | 0,00 |
| 526 | `GEnFT7rTczr7TvXG9tMY3v2KjKf4dcgXGSbqdKsy4cuT` | 277422207 | 14/07 02:39:26 | 0,112 | 0,125 | 0,13 | 66,7 | 0,00 |
| 527 | `4ppF6JzuX4JpQDh22J77LiLMSXofZMjKup8VymD31KsW` | 277422212 | 14/07 02:39:29 | 0,150 | 0,167 | 0,20 | -0.1 | 0,00 |
| 528 | `8VW7YT4c9nv85fibLSpVYw2Xio5taY2idkwyZgTfV5ZZ` | 277422262 | 14/07 02:39:50 | 0,297 | 0,319 | 0,59 | -0.2 | 0,00 |
| 529 | `HWq6dGHuw24nkg9Ge1KxENK6WUZVWE3gBJpuKmV5c7ga` | 277422272 | 14/07 02:39:55 | 2,000 | 2,156 | 2,00 | -1.1 | 0,00 |
| 530 | `GYCAnT2krgSAUX5FgCYwh29Wdpzm6mBFjvRX84XCuxTt` | 277422281 | 14/07 02:39:58 | 0,005 | 0,005 | 0,00 | 0,0 | 0,00 |
| 531 | `AZgy8J8G3dZj2JM8YrnxGvGEMd7KUBDe8DkZRQBVQZvh` | 277422292 | 14/07 02:40:03 | 0,495 | 0,520 | 0,49 | 0,0 | 0,00 |
| 532 | `AEiuzGKnAo1JnH9haNDLUxgyksEw9h2Jr7gqzankm3Tg` | 277422321 | 14/07 02:40:16 | 0,030 | 0,031 | 0,03 | -0.0 | 0,00 |
| 533 | `2mintAgDfKYo65Ew5BDqJds7a33DLY7rZmsndSu6LJfj` | 277422368 | 14/07 02:40:38 | 0,030 | 0,031 | 0,03 | -0.0 | 0,00 |
| 534 | `AuKf2i8JGu8JRekCi63QdvZm2ywmoZwuadXxsj6dYkwy` | 277422368 | 14/07 02:40:38 | 0,050 | 0,051 | 0,15 | -0.1 | 0,00 |
| 535 | `8r3HTtyE43xwmo5MZgvr4D3gWSS9H2aBwngF8us4qAEP` | 277422393 | 14/07 02:40:49 | 0,100 | 0,103 | 0,20 | 0,0 | 0,00 |
| 536 | `CX39Mc7RoZ4nADY4USKGaPvwFPXJRWRYc5tA5qzG2rED` | 277422455 | 14/07 02:41:16 | 3,000 | 3,019 | 7,20 | 5,4 | 0,00 |
| 537 | `2kKcXXxCajAmgJqWF1YDcdFSc881UqamWEyKGVZSKYUV` | 277422524 | 14/07 02:41:47 | 0,200 | 0,186 | 0,20 | -0.1 | 0,00 |
| 538 | `CCebNWun4rACQNATBseuYeFzFovoEaowThY8YKZbHCq1` | 277422537 | 14/07 02:41:54 | 0,300 | 0,282 | 0,30 | -0.1 | 0,00 |
| 539 | `5zNVkMnCYT7QU7CWxUbxDraxNtdFpynBrNWKW75myu4z` | 277422612 | 14/07 02:42:26 | 1,000 | 0,936 | 4,00 | 16,5 | 0,00 |
| 540 | `7ZY7p8VjgutzqZWJvGNDYyGXiE5XcBy5sPj5wTwpV95b` | 277422614 | 14/07 02:42:27 | 0,191 | 0,185 | 0,19 | -0.0 | 0,00 |
| 541 | `7UY8W5dpRvNXkKkibNr2YzgFZDAUvnL4am9QgH4XMBkV` | 277422637 | 14/07 02:42:37 | 4,950 | 4,818 | 4,95 | -1.0 | 0,00 |
| 542 | `3xJnng7EtrALKS6ufRSbqsRK2y4jnMANykrXeiH2Ebj7` | 277422668 | 14/07 02:42:51 | 0,193 | 0,232 | 32,59 | -0.3 | 0,00 |
| 543 | `J1GxVu6C5amQVGXRPxpcmpxRoxiacx4xLBP8fkGffhhE` | 277422709 | 14/07 02:43:08 | 0,538 | 0,870 | 114,68 | 0,8 | 0,00 |
| 544 | `CxYPnnNtPLWk7786J8d3Rurk6dgbcgZV1fT17V4Ry1D9` | 277422709 | 14/07 02:43:08 | 0,236 | 0,379 | 8,28 | 0,4 | 0,00 |
| 545 | `5jiqmf6wCFEm2YgdvXd9MywbTHb58TJxXSgQkAvMRRzq` | 277422716 | 14/07 02:43:12 | 0,990 | 1,516 | 0,99 | 0,2 | 0,00 |
| 546 | `GxBdupQ6A6FguULAyckreu8yF1tsJR3ep9YBEFqweTdn` | 277422757 | 14/07 02:43:29 | 0,100 | 0,131 | 0,10 | -0.1 | 0,00 |
| 547 | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 277422760 | 14/07 02:43:33 | 5,500 | 6,856 | 5,50 | 1 686,1 | 0,00 |
| 548 | `Bnv5C4J7hsS25Xjf2HoAsS5XVSccn8nDvN6nJfj14NMK` | 277422788 | 14/07 02:43:44 | 0,020 | 0,026 | 0,02 | -0.0 | 0,00 |
| 549 | `8Pj7Nm5KiwV8GeMhrTNK3GpZuBbThboiddtUCJHCg4Kn` | 277422805 | 14/07 02:43:52 | 0,100 | 0,128 | 0,10 | -0.0 | 0,00 |
| 550 | `5cLnb3P9sAgVn93w9sXc5VmDi2oV65cz1VvD6TUBWfdB` | 277422834 | 14/07 02:44:05 | 1,700 | 2,123 | 30,40 | 469,5 | 0,00 |
| 551 | `5fWtJsKti7QmoFNdgikZctjg5yAmA8RgzJMYDaPPHiVz` | 277422857 | 14/07 02:44:16 | 1,500 | 1,843 | 1,50 | -0.9 | 0,00 |
| 552 | `CgrjzC9jgY9RHuYsUB6bxV2damSiuwwY7NMgRoqW1GsF` | 277422889 | 14/07 02:44:30 | 8,400 | 9,555 | 8,40 | -4.9 | 0,00 |
| 553 | `4w9hg8MwXG34rvyavWaCzXYF662f51HuAWwgMUf667cS` | 277422905 | 14/07 02:44:38 | 0,200 | 0,216 | 0,20 | -0.1 | 0,00 |
| 554 | `ABWcsuxqsu83c9EiTQg3PPqHxMFJtetBiAbnZbqvPmVo` | 277422920 | 14/07 02:44:44 | 0,300 | 0,327 | 0,50 | -0.3 | 0,00 |
| 555 | `pHe5Jfbd6Ca27pF9vw68YabrqtBaK5nj16fq1sawhab` | 277422940 | 14/07 02:44:53 | 0,107 | 0,117 | 0,20 | -0.1 | 0,00 |
| 556 | `8MVmiVo1dtB8SQGxdgJ6Tgg88QAdCu1FHhpeHoryYL5H` | 277422952 | 14/07 02:44:58 | 0,300 | 0,333 | 20,10 | 51,4 | 0,00 |
| 557 | `2vBH8wHnu41xQTSw8fxgsv1GjuEx4Kqq57xqkLV7Kkha` | 277422984 | 14/07 02:45:13 | 0,010 | 0,011 | 0,01 | -0.0 | 0,00 |
| 558 | `3aj9CgVSrXiZwsuPzKN2AP6p8ERXsxXhGts7DVmUFxbL` | 277423066 | 14/07 02:45:52 | 1,400 | 1,499 | 1,40 | -0.3 | 0,00 |
| 559 | `9yQHa18NgFZn2QpMaZUYNrVpjBPhBw2ovZ4NSL9SnEfh` | 277423075 | 14/07 02:45:57 | 0,199 | 0,210 | 0,20 | -0.1 | 0,00 |
| 560 | `6DLskHmp2n25jEUjuni2td7L4hMUZ9oe2v2m16F9oqoK` | 277423101 | 14/07 02:46:09 | 0,348 | 0,378 | 0,35 | -0.1 | 0,00 |
| 561 | `4JrabSska1B3eJyhVkrjQXQ5FVDT1xV3gES5PVrPouvX` | 277423122 | 14/07 02:46:19 | 1,000 | 1,078 | 136,52 | 247,2 | 0,00 |
| 562 | `QhiNVePYuq2bETvLdSadB5tktngiaLi5RrEyDmCpkQF` | 277423173 | 14/07 02:46:42 | 0,174 | 0,190 | 0,17 | 3,9 | 0,00 |
| 563 | `2cUt9a6C8iUtwBR5BfeuqxBTTD3GYLBU8zNTLgcK1NWj` | 277423220 | 14/07 02:47:03 | 0,012 | 0,014 | 0,01 | -0.0 | 0,00 |
| 564 | `DfArQ9WLQtAzoAfHRijkduF6dkQy4jFEW53HYUkRvDUS` | 277423325 | 14/07 02:47:51 | 1,071 | 1,563 | 1,07 | -0.4 | 0,00 |
| 565 | `FB8K7NEyD4oMppB2fn587ULMmDCcTGFSWS7Qz4Tdpo7U` | 277423353 | 14/07 02:48:04 | 0,070 | 0,102 | 0,07 | -0.0 | 0,00 |
| 566 | `J2NVdJ7iifQ8T72qnXy8S7eSwkwbc8xp6biJzXssrcDT` | 277423402 | 14/07 02:48:26 | 0,200 | 0,280 | 0,50 | -0.2 | 0,00 |
| 567 | `EXVFt5JQMazU4dB2FbFEwcZJaoyHsuxP6nmFSkEZTuyc` | 277423453 | 14/07 02:48:50 | 0,900 | 1,212 | 0,90 | -0.1 | 0,00 |
| 568 | `88SqgTiqv9qrdhpz3YAKQz7jeaVSweESuys42ubUYnrj` | 277423509 | 14/07 02:49:13 | 0,191 | 0,254 | 0,69 | -0.1 | 0,00 |
| 569 | `ADdhKdaWtjrYx4s1mzRkPuiPNGg46EnbrK4Ss2EkfWCi` | 277423516 | 14/07 02:49:16 | 0,500 | 0,660 | 0,50 | -0.2 | 0,00 |
| 570 | `EeU6AV3khcRHSWiTtfmj37FPS1tPB6dPRGi5B2ZjL6vH` | 277423554 | 14/07 02:49:32 | 0,070 | 0,095 | 0,07 | -0.0 | 0,00 |
| 571 | `KtQWAKS9tX5Rb1SkNcu89Eg71jUwGNpfre2mTTgAEDu` | 277423577 | 14/07 02:49:42 | 0,100 | 0,136 | 0,10 | -0.0 | 0,00 |
| 572 | `FQYVCLHvoMVcVdWQ5ogARpQXxEoZAC7PdZuXhd9DmB9p` | 277423692 | 14/07 02:50:35 | 0,052 | 0,134 | 0,05 | 0,0 | 0,00 |
| 573 | `CcMc78XywnXwsXiZFWw5zHnnAjGzRRpprYSTD4aLW5HE` | 277423696 | 14/07 02:50:37 | 2,600 | 6,424 | 2,60 | 0,6 | 0,00 |
| 574 | `E2pbWb9MqzzyU6ajGwY4AtJrSTf6LFrdFDsAX4HNzGgc` | 277423706 | 14/07 02:50:41 | 0,250 | 0,597 | 9,11 | 1,6 | 0,00 |
| 575 | `ArrE1ddaN2dYWEoHgcJmmYH2mhYgvKhkmcMo8yk52jes` | 277423725 | 14/07 02:50:49 | 0,247 | 0,589 | 0,25 | 0,1 | 0,00 |
| 576 | `DdTYjbnZLRgC1UGc4FjVqh8vnsh6NH7CAVSqeB1qdyat` | 277423745 | 14/07 02:50:57 | 0,099 | 0,191 | 0,20 | 13,3 | 0,00 |
| 577 | `EbkMR4XW9YNQScFPkwmzbc6VyuGZcPfqzut5YvNAkJXi` | 277423747 | 14/07 02:50:58 | 0,500 | 0,957 | 1,00 | 0,0 | 0,00 |
| 578 | `7Gt57NfrPD82K8YpTsSijPB2tfdob7Hy1nU7C67P1J52` | 277423752 | 14/07 02:51:00 | 0,149 | 0,305 | 110,30 | 1,8 | 0,00 |
| 579 | `7nc3X7MpAqCmw636uYZSgUBYdsDmaszvTPJ8y5JMdm9T` | 277423789 | 14/07 02:51:17 | 0,203 | 0,412 | 2,15 | -0.0 | 0,00 |
| 580 | `4uZbWYcAk3Wuw2cyFXK2Cw7Mo38khTz9phC3VD1KXTbX` | 277423796 | 14/07 02:51:20 | 0,172 | 0,340 | 125,96 | 1,9 | 0,00 |
| 581 | `14hHLPAQax9vwpYMpeLnNqnW5mKt2F9uikBTJo3aFZQC` | 277423828 | 14/07 02:51:34 | 0,050 | 0,096 | 0,05 | -0.0 | 0,00 |
| 582 | `8qeUp8YW4GNHasCWUZXhY2ywh4GgK5b4xsaVoVJydNtw` | 277423867 | 14/07 02:51:52 | 0,007 | 0,013 | 0,01 | 0,1 | 0,00 |
| 583 | `aVag5MtkBbnwFSekoqsgEmXAFUuVGYVqcLFQEY9c1Gr` | 277424051 | 14/07 02:53:16 | 0,480 | 0,911 | 0,48 | -0.2 | 0,00 |
| 584 | `CYH7pGZPwT8AQppXsrQJdA5V9LHwge22NKVRdXrkyz3L` | 277424094 | 14/07 02:53:37 | 0,500 | 0,909 | 1,00 | -0.3 | 0,00 |
| 585 | `DXmxdFgFo8Pxwwku6RRNk1GjyTSkL6kdAjyG52CoREtT` | 277424188 | 14/07 02:54:19 | 0,100 | 0,186 | 0,10 | -0.0 | 0,00 |
| 586 | `ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH` | 277424229 | 14/07 02:54:39 | 0,950 | 1,754 | 0,95 | 0,0 | 0,00 |
| 587 | `5eWh4hyTfHP6bWD1o14Cnx3dSLAqm6kvVEPexEpbHKp6` | 277424243 | 14/07 02:54:45 | 0,108 | 0,201 | 0,11 | -0.1 | 0,00 |
| 588 | `9fQxpdzdMR2QeqcGrkj6tvZMKsGk16E4qT5KC5PKQsXt` | 277424243 | 14/07 02:54:45 | 0,500 | 0,921 | 0,50 | -0.2 | 0,00 |
| 589 | `EDqjDcXzZJLudZY5ShhvoskKhzD8rQydCWTa5M768Czo` | 277424319 | 14/07 02:55:19 | 0,030 | 0,055 | 0,03 | -0.0 | 0,00 |
| 590 | `75fXGTvc8BHKBXwNfqriso6dzLe52qMUzvGPu9DV8fog` | 277424346 | 14/07 02:55:32 | 0,500 | 0,905 | 519,90 | 197,5 | 0,00 |
| 591 | `HE6HXy1oLbZKs9eTdKkdS5jGcHeocuMm587oJT7HTCgC` | 277424440 | 14/07 02:56:17 | 0,200 | 0,403 | 0,20 | -0.1 | 0,00 |
| 592 | `X5Wix22oNkZZk1FCWTDnYeeTbxzyC7NiEtSKP65GbgX` | 277424662 | 14/07 02:57:57 | 0,410 | 1,028 | 0,41 | 0,0 | 0,00 |
| 593 | `9NKD9hFGe5f3rXPr8Au8Nk2Je55nxMYWJ6qjEvi9ySbS` | 277424677 | 14/07 02:58:04 | 0,005 | 0,014 | 0,01 | -0.0 | 0,00 |
| 594 | `BfxpFD6LeuoWZf9EZDAokCCgmtoe137TuN9Rdc7fRLSo` | 277424701 | 14/07 02:58:15 | 0,202 | 0,512 | 28,96 | 21,2 | 0,00 |
| 595 | `GssjY5Fd5kh4VqGHbPbakgPuZafSgUnws2vmazKqxbiS` | 277424701 | 14/07 02:58:15 | 0,040 | 0,101 | 0,04 | -0.0 | 0,00 |
| 596 | `HNX2Cn2nXYsJiGTNnPaHj3K3vkLWSvYRChCVRzfUmmGu` | 277424763 | 14/07 02:58:43 | 1,000 | 2,527 | 70,53 | 44,0 | 0,00 |
| 597 | `BUp1egG4oXUNDt5zHJiiPxL62Wh99uEQ3ZvoB7YigFYy` | 277424764 | 14/07 02:58:44 | 0,600 | 1,492 | 1,68 | -0.2 | 0,00 |
| 598 | `F3ubkMVaPxTQNWejaEvipBHXqbaqXq3eSeDTgLXsyC7j` | 277424892 | 14/07 02:59:43 | 1,000 | 2,409 | 1,00 | -0.2 | 0,00 |
| 599 | `EDQDTR11HnHs47Gimurm8pjNZFXEtXKBYQNEtabemF6k` | 277424952 | 14/07 03:00:10 | 0,696 | 1,659 | 114,61 | -56.0 | 0,00 |
| 600 | `49oRRdxqj6TTZijAFsjG6YGCeiQAgJDMbiy9mFocT1ST` | 277425045 | 14/07 03:00:53 | 2,200 | 5,022 | 2,20 | -0.3 | 0,00 |
| 601 | `69ztZMzmiqx1ExLy5rzDpddWUeM5Fqor3JiGKWLM72kD` | 277425054 | 14/07 03:00:56 | 0,279 | 0,622 | 0,28 | -0.1 | 0,00 |
| 602 | `HpbGQurKZdpX4ZeWcJa8ZFmM1uSLtVutBiZ12bonxtos` | 277425216 | 14/07 03:02:11 | 0,050 | 0,110 | 2,42 | -0.3 | 0,00 |
| 603 | `3DzNAKUn3Nr1f7oUaqg23Sxbad2c8TJHHynZKoe5r3WS` | 277425390 | 14/07 03:03:30 | 0,020 | 0,048 | 0,02 | -0.0 | 0,00 |
| 604 | `Bg1PqLNr5u6a6iPQ21ut6iGDTNN7oaX4tRa3fBat66oQ` | 277425404 | 14/07 03:03:36 | 0,402 | 0,947 | 0,40 | -0.0 | 0,00 |
| 605 | `Ay62LoZhmPV697nNGkkinariZtprRXjyUFM3m8LuqGgM` | 277425436 | 14/07 03:03:51 | 0,500 | 1,165 | 0,50 | -0.1 | 0,00 |
| 606 | `8rHVeG2Xo26fZDGCDACz3uEs7PUrwpfxwyfW9EJfRhW4` | 277425545 | 14/07 03:04:42 | 0,200 | 0,493 | 0,20 | -0.1 | 0,00 |
| 607 | `4Wctj7u7UVeiuGv2EGzryGrFQDeB6FJwFdzc8ZGyJUA5` | 277425664 | 14/07 03:05:37 | 0,200 | 0,524 | 0,40 | -0.0 | 0,00 |
| 608 | `GF6nqgdSJavPRMpRKhw3b8hsfafqPumSP5iBvDpUg1Zx` | 277425772 | 14/07 03:06:30 | 0,001 | 0,003 | 0,00 | 0,0 | 0,00 |
| 609 | `2N9nYFi9voCScnP88TqsmKuXDwfca2ZaUTwiSbF4c8Ak` | 277425885 | 14/07 03:07:20 | 0,014 | 0,041 | 0,02 | -0.0 | 0,00 |
| 610 | `GtKLbxBnQqPD8m8wiQRMY2BwoQdR84R7QbJa5LfibzBF` | 277425962 | 14/07 03:07:55 | 0,093 | 0,280 | 0,18 | -0.0 | 0,00 |
| 611 | `A2x4D3jf6qc4Wggh1x5trtsP7ByaDG6MTxFad558z6qE` | 277426072 | 14/07 03:08:50 | 0,200 | 0,721 | 0,20 | -0.0 | 0,00 |
| 612 | `EQa8GCoqLbRK7TBDBARPZFXvMkQk4697rWLvFfMXa3jC` | 277427166 | 14/07 03:17:14 | 0,400 | 1,821 | 26,13 | 42,8 | 0,00 |
| 613 | `GEzhU2NqwFtzWkc4tNNpW2heF5VZL9jZQeaW5BKzdRR6` | 277427941 | 14/07 03:23:11 | 0,500 | 2,394 | 2,50 | 0,6 | 0,00 |
| 614 | `5qx8EmzhnxwPDzkNMdRLNFZ245pwpioeUN7EyzH4MhNh` | 277428476 | 14/07 03:27:19 | 0,106 | 0,471 | 178,80 | 1,7 | 0,00 |
| 615 | `3eW6W2d2PkQGM8Btjf3AbEKXYswBDt6mDntM9CEuNLXb` | 277428476 | 14/07 03:27:19 | 0,174 | 0,768 | 221,08 | 1,8 | 0,00 |
| 616 | `3mUGxxHAte6SL6siUNJ4H7PnY7GryhAeRKEYJ9ZLEgdd` | 277428480 | 14/07 03:27:20 | 0,212 | 0,933 | 193,61 | 1,0 | 0,00 |
| 617 | `7TFy4p7CfojssdiatBcdPg1bAyBZNCcy6uZCiYKyFR5E` | 277428480 | 14/07 03:27:20 | 0,056 | 0,245 | 67,56 | 1,4 | 0,00 |
| 618 | `CDNWUknR7i1PAhJkap2cxRASp4ttfPFai9B3SE1iFcvK` | 277428522 | 14/07 03:27:40 | 0,056 | 0,241 | 138,34 | 0,7 | 0,00 |
| 619 | `PKt5x4i2JRHYbPcuEsTELyCfkn1EEMYhDKBC6n6Ya4g` | 277428529 | 14/07 03:27:43 | 1,829 | 7,655 | 264,70 | 0,4 | 0,00 |
| 620 | `HRGt3Yr7AZizMzwWcLQnnaUtwdRyqNWpbssqbDEsQAXz` | 277428529 | 14/07 03:27:43 | 0,174 | 0,707 | 115,34 | 2,1 | 0,00 |
| 621 | `8nR9ztLLKj5DvtHo3ubJ5DuFn3x3SYhCxoPxrdmm7rzn` | 277429654 | 14/07 03:36:20 | 0,090 | 0,391 | 0,74 | 0,5 | 0,00 |
| 622 | `LqNsHTzZprVjJ3X439PqsSdRAi6PQTDJoJWgaC8e5YW` | 277429757 | 14/07 03:37:08 | 0,500 | 2,012 | 0,50 | 0,1 | 0,00 |
| 623 | `3AwDdcrXRJpoWU5EQ9Dk7KR82jmQQK7ZAggay62aYZyG` | 277430148 | 14/07 03:40:05 | 0,179 | 0,631 | 151,69 | 1,3 | 0,00 |
| 624 | `8K4TPixLEoxZX2MEXkGuBeFTZPbTqRPEtrt63o3QSxYm` | 277430225 | 14/07 03:40:40 | 0,100 | 0,349 | 0,10 | 0,0 | 0,00 |
| 625 | `C9Wxwm81vc5vZ2KdkGAeC4PprDxyNsiLqPvccfu175qh` | 277430326 | 14/07 03:41:28 | 0,347 | 1,220 | 287,99 | 1,5 | 0,00 |
| 626 | `5aQ6dDXoqgeeLVWF7PLf6zPSLTF1Hw8bhNyweci8herC` | 277430326 | 14/07 03:41:28 | 1,000 | 3,451 | 4,48 | 5,0 | 8,69 |
| 627 | `7xY2NMmeqTo4i6qJSbx5qivfDBX5s4DVerFeb7aaLvLU` | 277430523 | 14/07 03:42:56 | 0,009 | 0,028 | 0,01 | -0.0 | 0,00 |
| 628 | `Fbrwz4t4AX7YLwnz1pMdgFgcw883d4iJAnocKaq7Vwf2` | 277430523 | 14/07 03:42:56 | 0,280 | 0,869 | 0,84 | 0,2 | 0,00 |
| 629 | `FXzcpJSkuvjMoQRh7a1bf7LXVhrm3kiXQWsuFD6b5goJ` | 277430843 | 14/07 03:45:23 | 0,800 | 2,449 | 13,00 | 165,7 | 0,00 |
| 630 | `B3ub5NbHSc3LBhXgQv7howfD2X7ThwCRwdKU252YoxZm` | 277430882 | 14/07 03:45:42 | 0,060 | 0,182 | 0,06 | -0.0 | 0,00 |
| 631 | `5SJc2eSLjhBCbZUcBpVKG7bqKKwFJdoQgTgL5S32MDoN` | 277430892 | 14/07 03:45:46 | 0,150 | 0,453 | 0,15 | -0.0 | 0,00 |
| 632 | `G7QHX4qNECP2CYbAQQVA33JjfvhyLzuhn8rVWS7frK2k` | 277431768 | 14/07 03:52:32 | 0,099 | 0,264 | 0,10 | -0.0 | 0,00 |
| 633 | `CEUQt7LtdQseaaCZfAwwXcKo6EWJyeiWC8CZCZDhFPxH` | 277432116 | 14/07 03:55:09 | 0,774 | 2,079 | 0,77 | -0.1 | 0,00 |
| 634 | `2hgnb68Qd4Rs4Fd59jiK6ooKQfBAtTsTLAq6F9U2yPxU` | 277432200 | 14/07 03:55:49 | 0,100 | 0,265 | 2,02 | 0,1 | 0,00 |
| 635 | `4tg39jDpd3DhuEyeZz4ELbsR3AU4Y8kdZiPpN6iu8eN8` | 277432263 | 14/07 03:56:19 | 0,610 | 1,619 | 106,73 | 312,0 | 0,00 |
| 636 | `AFC73btpLXVaMSjUWYCN6PbbKEKkFm5DFJaWLTQ6xWVV` | 277432599 | 14/07 03:58:58 | 0,088 | 0,230 | 0,09 | -0.0 | 0,00 |
| 637 | `77x4hjEqvSbQvW9LQqbqZqAL4gZLbGdPhSDUQMcWjoVa` | 277433357 | 14/07 04:04:54 | 0,201 | 0,494 | 140,15 | 0,8 | 0,00 |
| 638 | `FknP8WQWdkmWp1KPNoaeU9xk3aM3KD2L8XsGtE2dta8A` | 277433361 | 14/07 04:04:56 | 0,201 | 0,489 | 62,14 | 0,9 | 0,00 |
| 639 | `HJzbESXk7pXaeBnJVCr2PYNEjovo7XS7YhmMSLVT9TWx` | 277433387 | 14/07 04:05:07 | 0,065 | 0,150 | 77,41 | 0,9 | 0,00 |
| 640 | `8g6LpJRc3aAw5JNXSD4f6NQgcjrG2U83jaNiwk6M4a4n` | 277433619 | 14/07 04:06:55 | 0,100 | 0,233 | 0,15 | 0,0 | 0,00 |
| 641 | `4fX2uKeSrkQpzZoadS16pWZQbEj4qoFJYuqVkU652eys` | 277434234 | 14/07 04:11:39 | 0,020 | 0,061 | 0,02 | -0.0 | 0,00 |
| 642 | `8cvLTPcb5JbkCHgXEJBzkVVhNo1mqQArXtBGhDajt1pW` | 277434506 | 14/07 04:13:47 | 0,100 | 0,327 | 3,70 | 24,7 | 0,00 |
| 643 | `AEjLfStN57ZxUvGTMk9YHwZroyX5Uzr6YhvLQRPsVYaQ` | 277434973 | 14/07 04:17:26 | 1,740 | 7,098 | 6,14 | 0,0 | 0,00 |
| 644 | `HFP6Zr5qHnpACA4VxyAbZezrj534LKUnPBohCY31SmLp` | 277435021 | 14/07 04:17:48 | 0,945 | 3,759 | 20,65 | 0,6 | 0,00 |
| 645 | `DcXZyDwZUF7E4T7fUPcoZ3jp5nL9G2VEBbGWu9kxyaf` | 277435936 | 14/07 04:24:43 | 1,000 | 3,904 | 1,00 | 0,0 | 0,00 |
| 646 | `J1WeBBYKS6PKs3xoikuSZVdDFUo7C6GvnQvSAqmLyANd` | 277435993 | 14/07 04:25:08 | 0,100 | 0,384 | 0,10 | -0.0 | 0,00 |
| 647 | `B6NE1pFA3U7Am1fhoj7UyRh87CbfChQCLJFakYLep7QY` | 277436777 | 14/07 04:31:00 | 0,199 | 0,804 | 200,62 | 0,2 | 0,00 |
| 648 | `8yEd6KJypsZ54TxawvXd8oCerwbsmKxfhQQTfzdt6Ztt` | 277438573 | 14/07 04:44:46 | 0,100 | 0,407 | 0,10 | -0.0 | 0,00 |
| 649 | `2nYMLn73jSTbDBsQSzK4w9FFmYRmAaXH6UD1yPNpnySY` | 277438795 | 14/07 04:46:28 | 0,203 | 0,822 | 25,02 | 118,8 | 0,00 |
| 650 | `FSzufLkuimD28LwfoWajtr3Cq2FZvGP89QCtsCdAnfWR` | 277439288 | 14/07 04:50:13 | 0,629 | 2,716 | 24,20 | 0,0 | 0,00 |
| 651 | `3YpaY5wSQUmW8z9xW2uXXoF2ieSW5USTJQeEfmVsgXTq` | 277439874 | 14/07 04:54:37 | 0,250 | 1,068 | 6,13 | 0,4 | 0,00 |
| 652 | `9D8MFu7Ay3Txz8n5XybZzBoU7bJ8cfA9dXz7S5d88SoC` | 277440041 | 14/07 04:55:53 | 0,500 | 2,110 | 40,33 | 8,8 | 0,00 |
| 653 | `7i6p15vfxKiXVo5Ai1TV7yzLz6z5xMmzrfSgpobteycx` | 277442379 | 14/07 05:13:32 | 0,063 | 0,253 | 181,84 | 1,2 | 0,00 |
| 654 | `A3cgkzkkyPzaLeje3YXn114nwTgeQVbt4o9ovp1wcwNt` | 277445300 | 14/07 05:35:36 | 0,010 | 0,043 | 0,01 | -0.0 | 0,00 |
| 655 | `AFDkwJXJPCkZUjGo4mrrRZY53xU1vMSvXsyQiKdEZN93` | 277450182 | 14/07 06:12:56 | 0,050 | 0,261 | 0,47 | 79,0 | 0,00 |
| 656 | `CJGc1RFrViUV7atc2vksLGvhGJePUkZcDj8gYCdogFGG` | 277451038 | 14/07 06:19:30 | 0,110 | 0,560 | 0,11 | 0,0 | 0,00 |
| 657 | `8Jzeow7v4hSWzxPTVA1Kiyec7adbnkX5M13aZZRjvArZ` | 277454300 | 14/07 06:44:16 | 3,452 | 17,967 | 253,75 | 463,0 | 0,00 |
| 658 | `HTfV8WGwtA2oaFZfHuHfNdA4Cb28KEvdmFnb3CumXUTD` | 277454492 | 14/07 06:45:44 | 0,032 | 0,156 | 0,03 | 0,7 | 0,00 |
| 659 | `6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM` | 277454725 | 14/07 06:47:29 | 2,100 | 10,044 | 2,10 | 50,3 | 0,00 |
| 660 | `EEdq9Cw2GBXoVieSm2nRnCu81KRS5rNCzpKbKVeUXeD` | 277454866 | 14/07 06:48:34 | 1,000 | 4,511 | 15,22 | 618,8 | 0,00 |
| 661 | `D6ekfu32NUDCMtywYZh38oVaECWHttUVHZGoV8FrhwmM` | 277454901 | 14/07 06:48:50 | 0,386 | 1,535 | 1,14 | 0,1 | 0,00 |
| 662 | `9gypDDi7yKnSfU884HfncXqRt6GzLiE7BkLqxKeuKsnv` | 277454901 | 14/07 06:48:50 | 0,262 | 1,079 | 1,30 | 0,1 | 0,00 |
| 663 | `BJhCHKDHXLxfMbZcTnUMtJaY4hUTRV5qjAsepfwnJkcP` | 277454904 | 14/07 06:48:52 | 0,166 | 0,708 | 0,75 | 0,0 | 0,00 |
| 664 | `RQzw5yAo1oD2mKkcY2PCf4jYR4tAhmshtjxiquf22KB` | 277454904 | 14/07 06:48:52 | 0,165 | 0,699 | 0,88 | 0,1 | 0,00 |
| 665 | `49HZsCzQsvymnVNFPwv8SdLyocWtj5nrv76gzSdWA6Sk` | 277454904 | 14/07 06:48:52 | 0,157 | 0,662 | 0,51 | 0,0 | 0,00 |
| 666 | `8fkDb3TRbtkFNbFyYUfwPXoF1Boqp2xQrePbpqh5csB5` | 277454927 | 14/07 06:49:03 | 3,428 | 13,711 | 337,66 | 0,3 | 0,00 |
| 667 | `EyffBnQng8ckz1y1taqsrsQBrQhkGV2WTfHZJTrWh7oi` | 277454927 | 14/07 06:49:03 | 0,247 | 0,934 | 0,25 | -0.0 | 0,00 |
| 668 | `44FEatsrN9wNBVnJMXZjfAriFLYNZaqjhurGR2ttrK6G` | 277454939 | 14/07 06:49:08 | 0,165 | 0,687 | 0,89 | -0.0 | 0,00 |
| 669 | `3kw5CHFbTSoQKFL9nYjgpdpS2Ems8K4i6syqjDf7BEHq` | 277454945 | 14/07 06:49:10 | 0,113 | 0,469 | 0,15 | -0.0 | 0,00 |
| 670 | `BYC89Srapi2qYPpUexZihDSvMf5d3nngqeqPgftG8juX` | 277454945 | 14/07 06:49:10 | 0,117 | 0,483 | 0,16 | -0.0 | 0,00 |
| 671 | `4ZpmpcWAdacYFdMVbsGz2e7rGCJxtVAJ8GMdaa4gto9x` | 277455055 | 14/07 06:50:03 | 0,218 | 0,897 | 0,22 | -0.0 | 0,00 |
| 672 | `5qtHwhGbhuVGe7sDrWPtXbpequNNyaDrDatV7PNbJ96m` | 277458142 | 14/07 07:14:01 | 0,025 | 0,104 | 0,03 | 0,0 | 0,00 |
| 673 | `2BbW7TZtvNVBM6v9kooraTn4SVEQ1sJjMPSLoQLwMprH` | 277458296 | 14/07 07:15:12 | 2,000 | 8,051 | 2,00 | -0.6 | 0,00 |
| 674 | `8UToyTprmvPLXWRy4aGC8ePLVMZEL7kWe7oXHv8T4pig` | 277459040 | 14/07 07:20:56 | 0,179 | 0,696 | 0,18 | 0,0 | 0,00 |
| 675 | `7HzSjbeUFmTZ6yg6HqbA7VhMWynUofzy6mvV5HxVaPvF` | 277459507 | 14/07 07:24:36 | 1,000 | 3,857 | 166,50 | 446,2 | 0,00 |
| 676 | `DMxWvADMEDXBdSa2FxcULCDxoG4MegbJpo83PRDwahLk` | 277465773 | 14/07 08:12:43 | 0,110 | 0,412 | 56,40 | 4,2 | 0,00 |
| 677 | `Grkpt1SM9bBhwzUSaxB6vwzRW5osAKpXaCxoFyqs7ev5` | 277482296 | 14/07 10:18:14 | 0,150 | 0,535 | 7,30 | -0.3 | 0,00 |
| 678 | `DouvvAiw55ReYsT635zmo4CwQ1gsGzw7jGhjxwPGHLb3` | 277489517 | 14/07 11:14:31 | 0,000 | 0,000 | 1,00 | 76,7 | 0,00 |
| 679 | `5EtCT1idgTT8G4QVU5vVFPXSiXR7vzDJ94deTFNQ1vaP` | 277489944 | 14/07 11:17:52 | 0,300 | 1,038 | 1,08 | 0,1 | 0,00 |
| 680 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 277490445 | 14/07 11:21:48 | 3,500 | 11,486 | 3,50 | 4,8 | 0,00 |
| 681 | `8nwxAVzjAWYJSLdyUM86hK96EyiwPDSav7owzrMiPkaB` | 277490477 | 14/07 11:22:04 | 0,018 | 0,056 | 20,62 | 0,3 | 0,00 |
| 682 | `7JkRcHFhSR9cMxtgHNHH87zMgZNTozyVV4gD6QaeMcR6` | 277490483 | 14/07 11:22:08 | 0,217 | 0,675 | 1,58 | 0,1 | 0,00 |
| 683 | `FeZg6AEeXRn8Qa9qSJzV43CaNRLPSGwZ7rSssJTuVnoT` | 277490492 | 14/07 11:22:13 | 0,366 | 1,125 | 4,54 | 0,1 | 0,00 |
| 684 | `4PFdhMPP9vPPN4wY7w3LDW1Qqzb1wtnRTZQxEArbCMZB` | 277490493 | 14/07 11:22:13 | 0,276 | 0,841 | 6,48 | 0,1 | 0,00 |
| 685 | `FfQkDYXQBZfqAxCg12hgaN2aFKsim9iAxTre6XpxmWpS` | 277490493 | 14/07 11:22:13 | 0,220 | 0,666 | 40,00 | 0,4 | 0,00 |
| 686 | `HhbvRD7BBHXxW3wa68HLGRBYYABa4JDaMvoKbyyW8Mn7` | 277490496 | 14/07 11:22:14 | 0,180 | 0,543 | 307,72 | 2,7 | 0,00 |
| 687 | `5VwagjrkToKwJTiLRC7B6tuSteBxc9WzBUTnNbS6UTx5` | 277493528 | 14/07 11:45:16 | 0,080 | 0,251 | 4,21 | 93,9 | 0,00 |
| 688 | `2UNhNgHpypVB8DgJGTPkn17Jsc3NcTGY5sA5pAJFT9W7` | 277498279 | 14/07 12:21:25 | 0,500 | 3,512 | 0,50 | 0,5 | 0,00 |
| 689 | `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` | 277503232 | 14/07 12:59:49 | 2,970 | 16,642 | 231,16 | 729,2 | 0,00 |
| 690 | `CtXRQVs2iNvufASRLGatP8xjaKQFen9QxKtHojwgaxGw` | 277504824 | 14/07 13:12:08 | 1,980 | 8,946 | 184,19 | 131,5 | 0,00 |
| 691 | `7utSeMKTNBwYphXmmJf1vpPHt7Eb1qEDbPqTMuimsbpq` | 277506757 | 14/07 13:27:03 | 0,343 | 1,178 | 159,38 | 0,2 | 0,00 |
| 692 | `DRcQM77stHZwv7htvFBjwmax5aVQusk64AqCSTiniAV9` | 277506837 | 14/07 13:27:39 | 0,700 | 2,311 | 0,70 | -0.0 | 0,00 |
| 693 | `J3r3QV2373A4KfRKhGkZhjnVdCgdPmxYgK2uctjkNed5` | 277508064 | 14/07 13:37:05 | 1,000 | 3,421 | 2,00 | 0,1 | 0,00 |
| 694 | `FHu2jjTebYNLRKAg46kXCK9tX38ji3V7NFraCMmR6zYr` | 277508070 | 14/07 13:37:08 | 0,250 | 0,847 | 2,65 | 0,6 | 0,00 |
| 695 | `3HRospuJFML9mDRYGvtr7Bw2Gewzd8bPPZzAy6Yqcm1T` | 277508463 | 14/07 13:40:19 | 0,600 | 1,984 | 0,60 | -0.0 | 0,00 |
| 696 | `eA2XsgFAsa3HrTWCKNBUao535ABKrWgNyZ5mXLEUdhB` | 277509029 | 14/07 13:44:41 | 0,070 | 0,236 | 0,07 | 1,1 | 0,00 |
| 697 | `KMG98hz7PTCuX6erXB7JAdibYVRH2xE8Kk4MV7p63DS` | 277509817 | 14/07 13:50:51 | 0,735 | 2,500 | 6,40 | 4,5 | 0,00 |
| 698 | `D967cejV8fCEyov6Mt2gyhjfUcT93pARoEVnypQXpvUA` | 277509877 | 14/07 13:51:19 | 0,126 | 0,411 | 0,52 | -0.2 | 0,00 |
| 699 | `9qVEXF45JGaRkA8voddVSLYbt5wzxcWr7ZdYMwAH2Exy` | 277509877 | 14/07 13:51:19 | 0,112 | 0,367 | 0,67 | 0,0 | 0,00 |
| 700 | `6r8CqiPG63qFwHoPyUhrnz2DtMNyiKrkFQC6BZ2V4Xe8` | 277509880 | 14/07 13:51:21 | 0,122 | 0,392 | 330,74 | 0,3 | 0,00 |
| 701 | `FXYKNueTUkCvKAofjYxkj1NLeMdeHTRpfuJ13WTipfLf` | 277509885 | 14/07 13:51:23 | 0,148 | 0,471 | 0,61 | 0,0 | 0,00 |
| 702 | `GsjuXdLzE8wQh6RTNkq36VdSRKvp8LbtmkxZgEBboR4s` | 277511152 | 14/07 14:01:25 | 0,397 | 1,233 | 0,40 | 0,4 | 0,00 |
| 703 | `8LCVMEQaJ8LSdgXtcWHmrqVjcypAdx2VpHo9if9x4xrM` | 277512894 | 14/07 14:14:54 | 5,000 | 14,012 | 144,16 | 429,3 | 0,00 |
| 704 | `HWQz4rD8MhTRtEcnUAdG48hApQ7Abi7mg67cVXavgpWp` | 277512913 | 14/07 14:15:02 | 0,100 | 0,274 | 0,25 | -0.1 | 0,00 |
| 705 | `5gJF7pZChBEwT4ufEN2vaupFx48KCv5XZJTmeLcdyggK` | 277512920 | 14/07 14:15:06 | 2,602 | 6,928 | 19,22 | 0,0 | 0,00 |
| 706 | `6JtHTee2Fmwjt87sc7XPDRyv3Hmcx3t11f3h8259XPhN` | 277512933 | 14/07 14:15:11 | 0,688 | 1,851 | 173,56 | 1,7 | 0,00 |
| 707 | `49Bs4dxgPqUVfbXJkW3XNkcDerteNhTmTBVxeBzZN4JQ` | 277512938 | 14/07 14:15:13 | 0,291 | 0,776 | 3,91 | -0.1 | 0,00 |
| 708 | `5xtRtwHq7DcN3C7ifQPXTt4RbyJq4ey64xrif6CbQzhb` | 277512979 | 14/07 14:15:32 | 0,070 | 0,182 | 6,40 | 0,1 | 0,00 |
| 709 | `AJhip3wQPQua5vp1xSUR8q7VBy18xeoCA3tyTnkWwfYC` | 277513001 | 14/07 14:15:42 | 1,000 | 2,580 | 3,40 | 0,9 | 0,00 |
| 710 | `8dHh231H3EEHNyjjMux9KhpS8h3jd1KfUvoHVVcksEaL` | 277513198 | 14/07 14:17:13 | 1,985 | 4,940 | 1,98 | -0.5 | 0,00 |
| 711 | `9CsCwjmi4uHqYGdrDPaKTphqUK9A6A1jzfAFpsWeCkFC` | 277513574 | 14/07 14:20:14 | 2,514 | 6,247 | 5,67 | 549,5 | 0,00 |
| 712 | `HrffBj3D7VMnRoupx28f66Jzj1KBiNrcYTQAdvPx62Ca` | 277513642 | 14/07 14:20:44 | 0,113 | 0,270 | 0,11 | -0.0 | 0,00 |
| 713 | `DJG7mQMYkPLzpumUXFPX7UY3d5LpYh7ffL3GpG1tXzsx` | 277520323 | 14/07 15:12:03 | 0,035 | 0,113 | 2,56 | 0,7 | 0,06 |
| 714 | `CKzBUFi5J9cdfoG9EXxpji2UWxShvwvvGs9xdnz42wyE` | 277520721 | 14/07 15:15:11 | 0,100 | 0,325 | 5,80 | 3,5 | 0,00 |
| 715 | `VPcHCh18nhjVRYUuGPahDuYoy6apXk6uN18VvcASBkh` | 277525173 | 14/07 15:49:32 | 0,011 | 0,038 | 0,50 | 5,5 | 0,00 |
| 716 | `AuebSMSpCW7Fzo2DY1nQCwBPwpCZw4mtfnQiswNbzt4A` | 277526160 | 14/07 15:57:10 | 0,120 | 0,411 | 1,31 | 2,7 | 0,00 |
| 717 | `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc` | 277532233 | 14/07 16:43:58 | 3,025 | 10,048 | 7,27 | 5 490,9 | 0,00 |
| 718 | `CBGwseFBDm2hSdqYUecSFsjfSmjAZtPmNGRpN6kWjt3r` | 277532262 | 14/07 16:44:11 | 2,604 | 7,984 | 2,60 | 0,0 | 0,00 |
| 719 | `5HdmFajexban7WJkfP4QrGXXyt76Mwwp9nFeZDWEf3Hy` | 277532275 | 14/07 16:44:18 | 0,103 | 0,325 | 85,65 | 1,7 | 0,00 |
| 720 | `4DFczd9SY8vkFJjiRWpUVWgcWiwrpu15Bpaq4EDXy7Cg` | 277545382 | 14/07 18:25:47 | 1,000 | 2,980 | 1,00 | 94,0 | 0,00 |
| 721 | `A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J` | 277545574 | 14/07 18:27:15 | 0,750 | 2,184 | 4,50 | 0,0 | 0,00 |
| 722 | `BMn5hm3sJ6zumPM4GFxHsKkRm9RRvu45FUMeqvVUywgA` | 277549224 | 14/07 18:54:59 | 0,050 | 0,116 | 0,05 | -0.0 | 0,00 |
| 723 | `BGc1RN7U3BSh6DAsdkRuv71KG5peFK9Pxb9yKDDP18iu` | 277549852 | 14/07 18:59:53 | 0,100 | 0,230 | 11,63 | 5,0 | 0,00 |
| 724 | `FiBYMoxDE4iCCAAYKZVGSFr7UqEhSj142FuNZAfLhBfT` | 277550253 | 14/07 19:03:05 | 0,500 | 1,145 | 1,50 | 0,7 | 0,00 |
| 725 | `9Js15JmZyNutFyRyBNMVwo3JhVUXzFeXJQNhZKzDuTum` | 277551380 | 14/07 19:11:41 | 0,197 | 0,415 | 104,22 | 5,6 | 0,00 |
| 726 | `9Rzuu3iWG2TFKB4H7sM6jNmDTtSRn22FqWiHEp4q4UqF` | 277551384 | 14/07 19:11:43 | 0,043 | 0,091 | 6,52 | -0.1 | 0,00 |
| 727 | `49YJ8q4EicnZwNnGjtERipEXnRUEwQACUcck2xMgPE5Y` | 277553962 | 14/07 19:31:29 | 0,099 | 0,222 | 88,55 | 1,4 | 0,00 |
| 728 | `CwXGXQuMjDPytRdS2Eh1zSQ7SAgwgRaMUtqbYGazMY9q` | 277555763 | 14/07 19:45:31 | 0,002 | 0,005 | 34,43 | 5,5 | 0,00 |
| 729 | `4PUi4nHwhjkRYJs7PzNXFpMWAXcmhzgfH9osparmJwV7` | 277559501 | 14/07 20:14:31 | 0,500 | 1,189 | 0,67 | 5,1 | 0,00 |
| 730 | `B252jsFK2BKMfHRFzrHcxyVayPvC32h4ZXU8jmsm4Gsp` | 277571716 | 14/07 21:48:19 | 0,800 | 1,895 | 19,19 | 24,9 | 0,00 |
| 731 | `6BmVhvbYg2hurehP6gSfcYKwiCPvicCU9e6nXsc1FEwa` | 277583586 | 14/07 23:18:58 | 0,085 | 0,222 | 0,09 | 1,1 | 0,00 |
| 732 | `9mBMZDxcHSNypTqKNu5PMfNyWoGYL5CEfhsutW6qAVC5` | 277622395 | 15/07 04:15:07 | 0,610 | 1,710 | 9,59 | 29,5 | 0,00 |
| 733 | `D9C6VijsDY7Bz1mzSGQCr49GjnSdwzGL9AP5tLdDeiZW` | 277632535 | 15/07 05:33:03 | 0,498 | 1,342 | 0,50 | 7,1 | 0,00 |
| 734 | `8GrFf2zNh8FGsWzEqtq2ASfFpckGqNuhA1pR2RGrrPB8` | 277643498 | 15/07 06:58:05 | 1,500 | 3,615 | 96,23 | 342,7 | 0,00 |
| 735 | `7cPoMtk448csbdk9fcTeEcU22qiLCR9kcMjSLrqC4ygZ` | 277643899 | 15/07 07:01:11 | 2,895 | 6,629 | 1 903,50 | 495,9 | 0,00 |
| 736 | `CeBydZBAEoKwmBd1ujZhq75ES3rNxRCf5UZ9MsihvN6d` | 277650125 | 15/07 07:48:24 | 2,000 | 3,578 | 8,00 | 3,5 | 0,00 |
| 737 | `9Fy6iWkoDGH9ZnVBnd5pyFXJicSVBRVDHPYbsLZ82fvQ` | 277650178 | 15/07 07:48:49 | 3,000 | 5,014 | 5,00 | -0.0 | 0,00 |
| 738 | `8xAgop8WmMwMfCq2gcmDD9ciXCb74LdE8AT4ZRUYWWiA` | 277650988 | 15/07 07:55:15 | 0,010 | 0,017 | 0,01 | 0,1 | 0,00 |
| 739 | `2NsiXJEBdZYmheNfmcaJBsuNQBuE8o6fnsYL85akyrCw` | 277651332 | 15/07 07:57:50 | 0,100 | 0,166 | 2,10 | 8,3 | 0,00 |
| 740 | `UmhC2gMqzyBMNVBvVZrb1szoXZHQAtPFEgyN5F7pDGT` | 277652390 | 15/07 08:06:05 | 0,500 | 0,801 | 0,50 | 0,0 | 0,00 |
| 741 | `5NG1REUryumDNXzgrahWXHxagC2dj9hAKHCgdMuRs1BU` | 277652555 | 15/07 08:07:20 | 0,449 | 0,722 | 121,02 | 60,3 | 0,00 |
| 742 | `8LNfbwSgSL4ZUvDPHNX4nuHQud8vPpnRXXdh6snXfYVX` | 277653685 | 15/07 08:16:04 | 0,170 | 0,249 | 9,73 | -1.4 | 0,00 |
| 743 | `G9r8SRCuqaEtbZohoUCwYtGJJePKmuXwuqXjDxKYaYjw` | 277658276 | 15/07 08:51:31 | 1,000 | 1,633 | 13,80 | 7,3 | 0,05 |
| 744 | `Csuuj4zm46ZicuK263yZSMD3stnkSGnEMiZM79riskHG` | 277658860 | 15/07 08:56:01 | 0,500 | 0,806 | 0,50 | 0,3 | 0,00 |
| 745 | `GWtj8LGQYVdEattsykQWYH3mZ5UAg6RtqAUGxZDuu4Vh` | 277659377 | 15/07 08:59:55 | 0,148 | 0,238 | 0,15 | 0,8 | 0,00 |
| 746 | `JDMxEMcpiSZa21QR9JYeRqeVMJCLcJ4r9mj6fAPurnGF` | 277660301 | 15/07 09:07:00 | 0,495 | 0,787 | 15,89 | 24,9 | 0,00 |
| 747 | `Ejh8nKp4PyjGqrmPkrX9SpfwtNnD2yRMWRvAFsdUDVCF` | 277690936 | 15/07 13:03:09 | 0,346 | 0,525 | 0,56 | -0.0 | 0,00 |
| 748 | `B5fC3Dg42BRT8GffXg8nPy6ktQtgQ1UL5pHTZ7rnsmmR` | 277693161 | 15/07 13:20:29 | 0,500 | 0,778 | 2,50 | 2,4 | 0,00 |
| 749 | `5wAN1pX3ttnJ2piSPpXsAx2J2rv7tPbHA4bHfFP5R7ij` | 277693806 | 15/07 13:25:24 | 0,100 | 0,155 | 0,10 | 0,7 | 0,00 |
| 750 | `JCDpQ6m7mb5n2bUSQ3GQpVLxVsZtRUHhmvRXeE2Gg1rn` | 277698336 | 15/07 14:00:22 | 3,000 | 4,504 | 202,01 | 704,6 | 0,90 |
| 751 | `ApNso5pym1xLic1RXE7vkXn6H5QA5oHp6i5pnQKZnoxV` | 277698372 | 15/07 14:00:38 | 0,271 | 0,388 | 106,67 | 1,5 | 0,00 |
| 752 | `7vdw3tSLyTTJRcYoCCeK2LJ3CyfDtYvTRJsGbDSUQJHp` | 277700101 | 15/07 14:14:08 | 0,500 | 0,714 | 0,50 | 5,2 | 0,00 |
| 753 | `cAMHzvfwJoSyYUH8aFfKjb195QtUEjhLonkRHaDkuYA` | 277700101 | 15/07 14:14:08 | 0,500 | 0,707 | 0,50 | 5,2 | 0,00 |
| 754 | `Ge6tSATHdMCGoQztf7u7W4mRWTyiLC1MHqDnZyDGeLei` | 277701505 | 15/07 14:25:11 | 0,100 | 0,149 | 2,17 | 0,6 | 0,00 |
| 755 | `GMVm9BWUVEuSSzvBbChcyAGD3iXRcSFQEqaAJCv3zs5c` | 277702967 | 15/07 14:36:30 | 0,827 | 1,168 | 13,08 | 5,9 | 0,00 |
| 756 | `pmmgQLHq6ZZrcDez6V2pfRwAwctRBvgEGzJLDbPYqBQ` | 277703697 | 15/07 14:42:10 | 0,247 | 0,360 | 0,74 | 3,4 | 0,00 |
| 757 | `EgqRdhJXivFeHt73Y3VXyoMaNxU8CtonyA1FX673mdKr` | 277703789 | 15/07 14:42:54 | 0,001 | 0,001 | 166,49 | 14,1 | 0,00 |
| 758 | `2bUqHhkdryVMR88q3BNxYzuvUxvgzJEMjNgFW5zujZjF` | 277704893 | 15/07 14:51:22 | 3,500 | 4,762 | 667,83 | 545,4 | 0,00 |
| 759 | `8z2MvtcKDxfrexPgMzREgGs3auavduvZSXrKd7adngRz` | 277708055 | 15/07 15:15:58 | 3,000 | 3,907 | 24,51 | 49,3 | 0,00 |
| 760 | `5ZTLzj4spvB4VsU6Qe48iGFGA2Lb7FRpyKXWbq48MjVS` | 277708160 | 15/07 15:16:49 | 0,290 | 0,365 | 184,25 | 3,7 | 0,00 |
| 761 | `HD8YggbjQ5b3qFmhizf2zySZR3zHC8CR3cgQW7Bj3Lqk` | 277708177 | 15/07 15:16:56 | 0,182 | 0,226 | 118,68 | 5,9 | 0,00 |
| 762 | `5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx` | 277708259 | 15/07 15:17:33 | 0,248 | 0,303 | 32 832,72 | 489,6 | 0,00 |
| 763 | `5prcrnXbd1TSjxxRqXmHY44vCYKJgBJychNGvCuhSkGi` | 277708259 | 15/07 15:17:33 | 1,307 | 1,561 | 54,10 | 8,4 | 0,00 |
| 764 | `AzU4r8PErWXPqrUN6mpLh1zWVf1ve2rhPzkxscUsfvA8` | 277709443 | 15/07 15:26:47 | 0,340 | 0,431 | 10,24 | 79,0 | 0,00 |
| 765 | `BdTBb9CtwifSncdXcrwENNS4yNC5wnF5X2kBwcgKj7si` | 277709565 | 15/07 15:27:44 | 0,200 | 0,253 | 2,38 | -0.6 | 0,00 |
| 766 | `tdNaNGqbKpxgVdSHri6BevbD11ncnjR8GtFMagF2FGV` | 277709677 | 15/07 15:28:37 | 1,500 | 1,771 | 12,50 | 2,0 | 0,00 |
| 767 | `9mRn9Zp1WhmV1hEJZFiPkjC4wp5neX1uuiYc5KxoNF72` | 277709844 | 15/07 15:29:56 | 0,500 | 0,585 | 6,28 | -0.7 | 0,00 |
| 768 | `DfJHvjBpbyDbr7ofsx8L8WNZcJ6WexiYN7xgnqPfAr2h` | 277709892 | 15/07 15:30:19 | 1,100 | 1,267 | 37,08 | 478,5 | 0,00 |
| 769 | `5B1jWQKDisQhd2H4PcZG7f4DTYijHEWyzhMJC6sAZVNt` | 277710229 | 15/07 15:32:55 | 2,000 | 2,297 | 3,60 | 3,9 | 0,00 |
| 770 | `FHiX5WwpWa8iX43cusYojR3WfiMLFAWL29yVpWKaha6K` | 277710582 | 15/07 15:35:44 | 0,500 | 0,526 | 0,50 | 0,4 | 0,00 |
| 771 | `4QpLx9URPJTk59szL5KgoLYyVH7EWeYub8y4GMwDPTtQ` | 277710793 | 15/07 15:37:21 | 1,000 | 1,058 | 1,00 | 0,0 | 0,00 |
| 772 | `HRRq3jAZ2jeWEudg9scS1n42NYAkqEiTygjsMBGn9CqU` | 277711336 | 15/07 15:41:38 | 0,990 | 1,027 | 439,92 | 715,1 | 0,00 |
| 773 | `dQyiUnrBuhhbpRfkkBVhvoNnJXHwkx3axAtmxYLzc8i` | 277711441 | 15/07 15:42:27 | 0,330 | 0,335 | 191,53 | 268,8 | 0,00 |
| 774 | `Mw9DA84QcNhgbS78wsAtj1NSzDMmTFThNXsLuTRqLQW` | 277711622 | 15/07 15:43:51 | 0,250 | 0,256 | 4,97 | 1,4 | 0,00 |
| 775 | `D12r2UMT4yEhQca9p5aJeKMZYoerpaXEPT4zNTxSQ5ir` | 277711649 | 15/07 15:44:04 | 0,500 | 0,503 | 1 081,55 | 830,2 | 0,00 |
| 776 | `GVjmBfuuPRRcmpZWx3id4a5v3FhGASDxcmyhzxpm7Niu` | 277711677 | 15/07 15:44:17 | 0,278 | 0,263 | 2,65 | -0.1 | 0,00 |
| 777 | `ExJBT52Hac3KJXZfNcQVacpZcpcvZvPtdvDpsQdAFZes` | 277711680 | 15/07 15:44:19 | 0,125 | 0,118 | 5,88 | 0,0 | 0,00 |
| 778 | `FJQxGVmeN5uriMQyr2ZaMRYpSUYCA11GDT5vktKKhGdg` | 277711774 | 15/07 15:45:02 | 0,495 | 0,463 | 5,69 | 18,9 | 0,00 |
| 779 | `5t64s5pD4YdeuNkd6XFaUUzhdDEfpgkKxK95JjzH1U9d` | 277711792 | 15/07 15:45:11 | 0,015 | 0,014 | 0,10 | 1,6 | 0,00 |
| 780 | `9afDK39TkF9xiFSDAyaBXHvBHomGZ2cgQwscrRfxqHy8` | 277711900 | 15/07 15:46:01 | 0,500 | 0,490 | 4,10 | 0,3 | 0,00 |
| 781 | `815QDRYBgUEekqUd6Gbm1Db2pn81HCjiUxqxKap8MnWh` | 277711971 | 15/07 15:46:34 | 1,637 | 1,604 | 2,64 | 78,2 | 0,02 |
| 782 | `ACxreg3E89JmWmSP4ciLUKGtvBMDjmoonW7BcPubJSUF` | 277712121 | 15/07 15:47:42 | 1,000 | 0,959 | 6,00 | -1.3 | 0,00 |
| 783 | `DQQmbufqZxLkj1EKcHXJR2h5EP4B364hves64Ka3cTEq` | 277712417 | 15/07 15:50:00 | 0,500 | 0,501 | 0,50 | 3,0 | 0,00 |
| 784 | `BW8C8y1nvexUCrvFGaytLt3bjePHU26q173Btr2WxB93` | 277712512 | 15/07 15:50:44 | 2,746 | 2,724 | 11,59 | 17,2 | 0,00 |
| 785 | `HGvKQZhxYmJE4vXepdFY9WrjL9eorywgkJ6G7Pfubszm` | 277712786 | 15/07 15:52:49 | 0,080 | 0,079 | 5,80 | 30,8 | 0,00 |
| 786 | `HkfdTXmcVygHjoJHR9nU2Nz4UUqhXLRXV7mE4cYZr8cd` | 277713032 | 15/07 15:54:43 | 1,213 | 1,182 | 9,10 | 1,8 | 0,00 |
| 787 | `6GDHJhuMDvM9rMRzBt27syscrvVUPihVzURSeKq5k9mB` | 277713084 | 15/07 15:55:08 | 2,970 | 2,829 | 8,22 | 19,9 | 0,00 |
| 788 | `GUpBnGLKNeu9uv4ubzXMqc2XA4QwtntQFAzxA337NX2U` | 277713573 | 15/07 15:58:54 | 0,001 | 0,001 | 0,00 | 0,0 | 0,00 |
| 789 | `bH1iNP3CjC9mcCTwRNVGRX9KACePYZLEngKSSNue5Zi` | 277713857 | 15/07 16:01:10 | 3,135 | 2,666 | 3,14 | 28,3 | 0,00 |
| 790 | `4cX4a1ZprMm14aFWtRW1e1nzpnVKqVJySZQpyRuMFMw4` | 277713936 | 15/07 16:01:46 | 1,096 | 0,914 | 18,11 | 64,8 | 0,00 |
| 791 | `4sDexZPVc3BbSQpH9G8Gt1nfWG7xZkwk54s8K2aJurx9` | 277714825 | 15/07 16:08:31 | 0,400 | 0,332 | 42,62 | 24,9 | 0,00 |
| 792 | `4jHn428b44a4K5TbeSoW3fJYdzWyrGt4q4xbBzBzRfX8` | 277715059 | 15/07 16:10:19 | 0,300 | 0,238 | 75,70 | 0,5 | 0,00 |
| 793 | `Au3jhxMMVZ37ufRmJMEVndidzqz71SSPVnPdVMUkuep7` | 277715225 | 15/07 16:11:33 | 1,000 | 0,780 | 13,19 | 3,2 | 0,00 |
| 794 | `AaHipEzweXZPBSX2KsiNNCRwMi8QJ11sQNg1spwszSZw` | 277716145 | 15/07 16:18:28 | 0,200 | 0,156 | 11,02 | -0.6 | 0,00 |
| 795 | `F1r5QWfAfFRyXmaLVukFPp6ADTBgcnFxFZENeUzjbv2R` | 277716296 | 15/07 16:19:40 | 0,200 | 0,158 | 0,20 | 0,3 | 0,00 |
| 796 | `EHq1omcxJDfevgX4TQgsBKYspSCe92D2NtG8CzFNgp4b` | 277717233 | 15/07 16:26:43 | 2,100 | 1,701 | 12,60 | 10,2 | 0,00 |
| 797 | `GAc6Lx79zTmoYAJQU5X5v4TTKLjMkYEWxqxwNmKM4my9` | 277717438 | 15/07 16:28:19 | 0,803 | 0,655 | 613,82 | 92,4 | 0,00 |
| 798 | `Aq9yU6gGnNgJobVmxfhdeXSySarY7bp88sE6BhK6EBDA` | 277717730 | 15/07 16:30:33 | 2,176 | 1,770 | 76,02 | 131,3 | 0,00 |
| 799 | `4AVe3VMDWnfwxo3Ydi4N8m411TvPwe3BjXmPnRg4GU4a` | 277718070 | 15/07 16:33:14 | 3,593 | 2,807 | 1 017,48 | 0,2 | 0,00 |
| 800 | `HQaMctYLBDvL8tCAyx655HKeYvQZCrwBcLVEd4Ptf3Gd` | 277718250 | 15/07 16:34:38 | 1,000 | 0,792 | 1,00 | 69,5 | 0,00 |
| 801 | `2unemzH569fsRsPZvgwdy4zUSwdDApG9vyvvfJLr4z8b` | 277719666 | 15/07 16:45:31 | 1,000 | 0,768 | 6,00 | 1,5 | 0,00 |
| 802 | `Gm7q8U7p2gJnhyJABLr2QZ4YNDf8D3bduUQ6rqc3xUJc` | 277719674 | 15/07 16:45:34 | 0,150 | 0,114 | 0,30 | 0,1 | 0,00 |
| 803 | `GwE9tKErrVUvsKPfonkEPG6gDRLFSS7fA1LhisegcpfA` | 277719767 | 15/07 16:46:15 | 3,000 | 2,241 | 54,00 | 16,8 | 0,00 |
| 804 | `8Z868ETuaHiio9xnMQUP5wqAmXNK8jVW9WEaKTm8D7ex` | 277719931 | 15/07 16:47:32 | 1,000 | 0,692 | 1,00 | 4,0 | 0,00 |
| 805 | `ErNKPzqv3eXwaYC8adfgFpuPcyXYFNpwk68NTAbP9LGY` | 277720005 | 15/07 16:48:05 | 3,000 | 2,005 | 35,61 | 588,1 | 0,00 |
| 806 | `EwQsse55h42L8RDcqgWhZVK25uSKEyBELQ5GHhkggNkF` | 277720017 | 15/07 16:48:11 | 0,300 | 0,196 | 0,60 | 3,8 | 0,00 |
| 807 | `CBdnDKmGvmHnT47oJJVpdF2Pssbbp3k5qEXgoAf8eUTq` | 277720086 | 15/07 16:48:46 | 0,150 | 0,098 | 1,15 | 1,0 | 0,00 |
| 808 | `8KHe9uSsTDRLhQtS4ryvuuHanGZC3yfM3erZ8QN4kfvu` | 277720158 | 15/07 16:49:18 | 5,000 | 3,163 | 5,00 | 3,5 | 0,00 |
| 809 | `DmdrUanasUnPEurAuVQuFZqn7oz3kDhNuW3ZydBjTJDS` | 277720228 | 15/07 16:49:49 | 5,000 | 2,950 | 118,00 | 17,7 | 0,00 |
| 810 | `9uokMo4GoSJiL45dNYJu6MyuFVWkLikQKWhbNLenA6ef` | 277720262 | 15/07 16:50:05 | 3,000 | 1,724 | 3,00 | 0,9 | 0,00 |
| 811 | `531b6cXPCqifDuk344Rknc7vxruNrZ8xbHiTgAuWdLzU` | 277720264 | 15/07 16:50:06 | 0,500 | 0,282 | 0,50 | 0,2 | 0,00 |
| 812 | `GiXKvBb1s4uAe58pvLrH8DWWo5t57dZ8KdtY1ZfAsTJ9` | 277720266 | 15/07 16:50:06 | 2,970 | 1,640 | 29,70 | 10,4 | 0,00 |
| 813 | `8YaggZKR1uc5zjPk2myPQbAmffd2296xHq4xm5r7wPES` | 277720277 | 15/07 16:50:12 | 0,200 | 0,109 | 0,30 | 0,3 | 0,00 |
| 814 | `BH6b86hoDRv3HLkqSAkqPRscCrmy19QKJGVRRtsxH7nv` | 277720281 | 15/07 16:50:15 | 0,100 | 0,054 | 0,10 | 0,1 | 0,00 |
| 815 | `465Asn2KQxxCcKCUdP8CcpVREMPqQgs4rhN8iYMSvZH7` | 277720287 | 15/07 16:50:18 | 0,083 | 0,045 | 207,51 | 0,0 | 0,00 |
| 816 | `Edh6MAjA7VvbtYw6ESvW5GpxHUySA1LW7bZ9ThEqASsy` | 277720287 | 15/07 16:50:18 | 19,000 | 9,401 | 19,00 | 15,1 | 0,00 |
| 817 | `AMUK2589VnKrFftEU5igjzXZNeJYDo3o1xXEzX7UoVSR` | 277720304 | 15/07 16:50:27 | 0,200 | 0,091 | 0,20 | 0,1 | 0,00 |
| 818 | `8kkAsy5zKw7f6hcExfcjk9etXesMgCRpsy5Qium5uwaW` | 277720320 | 15/07 16:50:35 | 2,000 | 0,884 | 2,00 | 5,7 | 0,00 |
| 819 | `7gV1CkcyQpTBzQwbcLqkwSW3NctmY8H896k2phgFwdjf` | 277720320 | 15/07 16:50:35 | 10,000 | 4,165 | 27,00 | -9.5 | 0,00 |
| 820 | `8ZWvaahypb83Xs48JJYYq7QAtSWErhNi2fNUDtT49owZ` | 277720342 | 15/07 16:50:45 | 1,000 | 0,396 | 1,00 | 1,8 | 0,00 |
| 821 | `J25tPg161aaj4RV7yYaKZnBZUNSUpBMkTDiQ9s76CGwW` | 277720342 | 15/07 16:50:45 | 0,100 | 0,039 | 0,10 | 0,2 | 0,00 |
| 822 | `D9GmmDsvwmXfbJin1dBXtN7BmsWgr1JhEohoVq7KPEHo` | 277720346 | 15/07 16:50:46 | 0,100 | 0,039 | 11,10 | 0,5 | 0,00 |
| 823 | `5YiBJKZ1tgjHBFNXU5W4CMioygvVQhWz9fEyZzyPFDVo` | 277720459 | 15/07 16:51:37 | 1,980 | 0,789 | 1,98 | 3,4 | 0,00 |
| 824 | `3zfWPJBKxH5WwEjcozrtfqvRXjnGekWBa9YLpS194HVj` | 277720508 | 15/07 16:52:00 | 0,500 | 0,197 | 10,30 | 3,1 | 0,00 |
| 825 | `3Z97RPoyJScqmhGLTw7CTiAFm377qeHqDx61sEaRnX4q` | 277720576 | 15/07 16:52:32 | 0,014 | 0,006 | 0,13 | -0.1 | 0,00 |
| 826 | `8zFZHuSRuDpuAR7J6FzwyF3vKNx4CVW3DFHJerQhc7Zd` | 277720732 | 15/07 16:53:44 | 14,850 | 6,308 | 1 287,00 | -1,100.1 | 0,00 |
| 827 | `3K1D8FhoWcocjP3TaXZ8MJ5GYjEbMMg4DnuBfAEfw9J3` | 277720737 | 15/07 16:53:46 | 0,340 | 0,134 | 3,80 | 2,9 | 0,00 |
| 828 | `DokV4tWxMMGmws7YskM3dvwcLTxkwbXWuLHjgy3opa1X` | 277720737 | 15/07 16:53:46 | 0,050 | 0,020 | 0,10 | 0,0 | 0,03 |
| 829 | `F1zvM186XTLCsFxykgaPC7NhtqWomBQ6zpVDyxBLxQwZ` | 277720740 | 15/07 16:53:48 | 4,000 | 1,543 | 101,00 | 2,8 | 0,00 |
| 830 | `69YfL1dJUmuPQeYhwo5BhQLMzE9Va8H6sjLEf4AXwMH8` | 277720758 | 15/07 16:53:57 | 1,000 | 0,377 | 6,00 | 3,7 | 0,00 |
| 831 | `BnfXWQyz4bN4srnLj8oFj1aEohcm1u47LT1w7X6Gd1ok` | 277720760 | 15/07 16:53:58 | 1,000 | 0,373 | 26,00 | 5,0 | 0,00 |
| 832 | `A8Uc5jqWVfeMrVcbv38YCCSn3AfkQnXkpLTzeW95TdZA` | 277720760 | 15/07 16:53:58 | 2,475 | 0,909 | 39,60 | 32,1 | 0,00 |
| 833 | `8oM9G5o2iJKsUEXoDKWxRxmhHiSfspfbqnqkrScXy9Fk` | 277720760 | 15/07 16:53:58 | 19,800 | 6,590 | 19,80 | 8,3 | 0,00 |
| 834 | `DGen7hBBRZYvMpwmmqAdWARw9pExZkfZzXt9iDD4VPaH` | 277720763 | 15/07 16:54:00 | 9,900 | 2,899 | 9,90 | 2,4 | 0,00 |
| 835 | `79CxhdY2TeFHpGNcaHgnHJTWnv7KA3KgMFoeHrJg77ru` | 277720776 | 15/07 16:54:06 | 10,000 | 2,703 | 35,02 | -6.0 | 0,00 |
| 836 | `ERDokVW3jctyVoaVtZzMs6BBBjvHnmpiDRHt3AwzMpuS` | 277720779 | 15/07 16:54:06 | 4,950 | 1,262 | 115,83 | 4,2 | 0,00 |
| 837 | `4wgM9b8321Vs63pLy4dMoxAVwyhKPg7T24dw4MvbSj1P` | 277720781 | 15/07 16:54:07 | 0,250 | 0,062 | 0,25 | 0,0 | 0,00 |
| 838 | `Gx8m9n269YHZxteT6ZBCJN3unDTzupKb5YNUghThK4Y2` | 277720790 | 15/07 16:54:12 | 0,200 | 0,049 | 0,90 | 0,4 | 0,00 |
| 839 | `HQq78KzPo3GmYiJtBMnTp3Lkvf9HMcZGPXkVURjbyeUc` | 277720791 | 15/07 16:54:13 | 1,980 | 0,481 | 172,04 | 29,4 | 0,00 |
| 840 | `3PGm9V46zmPaa9hbYpNVCvzqGjxomdmtBfWCgsBFHcHH` | 277720791 | 15/07 16:54:13 | 0,050 | 0,012 | 1,06 | -0.1 | 0,00 |
| 841 | `BSfyn7CncEtBfdjJcXUoPMEcgsRKKZmua9yRr3LUXrvq` | 277720796 | 15/07 16:54:16 | 0,990 | 0,238 | 0,99 | 0,6 | 0,00 |
| 842 | `69Um89cpyXwo5XhjmdspcteE85ucTu4Shv79qrSySo6G` | 277720806 | 15/07 16:54:21 | 0,400 | 0,094 | 2,60 | 0,6 | 0,00 |
| 843 | `JMFPVNgosHt3MnMyjtbnTRvDYuu63aNtbTg7PgJezAB` | 277720812 | 15/07 16:54:23 | 0,150 | 0,035 | 0,15 | 0,2 | 0,00 |
| 844 | `9p4LXuXDsY6Ec168bdLM8vL5PwYrfpNcoHYg3cifz97F` | 277720817 | 15/07 16:54:25 | 2,000 | 0,466 | 2,00 | 0,0 | 0,00 |
| 845 | `Cs55xZ79Qbh28aZVGmPVCzgeqwdXhrYro5Vp5gohHyWE` | 277720821 | 15/07 16:54:27 | 0,990 | 0,229 | 0,99 | 0,7 | 0,00 |
| 846 | `94jTj69kanDXAP89htcRMbBmWVyz5UpPPtygNSeqvaz6` | 277720822 | 15/07 16:54:27 | 0,060 | 0,014 | 0,06 | 0,1 | 0,00 |
| 847 | `6LvziJ7aK5ksL7JqFtVmoJTCGT3G4uKF65CVxtFMMJQz` | 277720829 | 15/07 16:54:31 | 4,950 | 1,119 | 4,95 | 8,9 | 0,00 |
| 848 | `2TvYDht6fQ9WencbkdHo5zisdWU6z4EDvvTjdVekmqSJ` | 277720832 | 15/07 16:54:33 | 15,000 | 3,250 | 75,00 | 6,5 | 0,00 |
| 849 | `F1DRDBNW1CX3BPoZPQafidvMeaepg6LS19J4vHqn7xMt` | 277720833 | 15/07 16:54:33 | 30,000 | 5,583 | 30,00 | 1 709,5 | 0,00 |
| 850 | `4T3ScHJgMvoR7Su9ey3AB2Ld9NHtFXCA4FyURAdYtgSi` | 277720848 | 15/07 16:54:41 | 0,024 | 0,004 | 0,02 | 1,2 | 0,00 |
| 851 | `4rSemZQTuirXTVUdL4733gfhRDGsjB7THLWVovSVdxgZ` | 277720848 | 15/07 16:54:41 | 0,100 | 0,017 | 0,10 | -0.0 | 0,00 |
| 852 | `5znHPmFWi8TdqoVzgGcB1JrnhZVUAuWQ5NTN3TNw1o2S` | 277720849 | 15/07 16:54:41 | 1,000 | 0,168 | 1,00 | 1,2 | 0,00 |
| 853 | `FVBZzBjGGTxgwWdcN5f4hQWrStxUJrkkMt1mZ3dCGCsa` | 277720850 | 15/07 16:54:41 | 1,980 | 0,324 | 3,96 | 3,8 | 0,00 |
| 854 | `9DUha92M9FSahBDrFbewV8r6ST2oNyXJ8mE9HvtkuMoV` | 277720851 | 15/07 16:54:42 | 0,999 | 0,164 | 35,96 | -0.3 | 0,00 |
| 855 | `5dByDJZ3UCZia1MaDcQUhrTRwnsrB8GHb6ihJwVCbbvZ` | 277720858 | 15/07 16:54:45 | 5,000 | 0,836 | 5,00 | 1,9 | 0,00 |
| 856 | `HJvwnKW8NJuSVWG1duQh13Ue688HQ3grgYJAzAp2R3oX` | 277720858 | 15/07 16:54:45 | 9,900 | 1,582 | 14,85 | 2,1 | 0,00 |
| 857 | `99FPDGtjSgaxmuk4uoXgr6JeCx6rahh6xdy4WP6y82Wd` | 277720866 | 15/07 16:54:49 | 24,750 | 3,572 | 44,55 | 115,7 | 0,00 |
| 858 | `44MjSxZswPi6wEiyjW6E2ocLC7Dn9Aa2snpbvNczZLDv` | 277720870 | 15/07 16:54:50 | 1,000 | 0,145 | 13,00 | 1,1 | 0,00 |
| 859 | `KFUyoV9Fe5SY36Q2EGQsJirBghXdxVRkkUcjJZxiHb1` | 277720872 | 15/07 16:54:52 | 0,099 | 0,015 | 0,10 | 0,1 | 0,00 |
| 860 | `H4XtGYqe8NxWasxQ2f36GEUVF4hCcNwiWrEiBXgroGz9` | 277720876 | 15/07 16:54:53 | 5,000 | 0,744 | 5,00 | 0,9 | 0,00 |
| 861 | `DQZiirZHJDk7R1qJXWcUudZAyUUGxrEo89S6Urbfxcva` | 277720876 | 15/07 16:54:53 | 3,000 | 0,436 | 3,00 | 0,1 | 0,00 |
| 862 | `C2X8MT6MZfM2GMLeoaJvdnMCqbSQDJ2kHk3vsCHrZ2H5` | 277720880 | 15/07 16:54:55 | 0,500 | 0,071 | 0,50 | 0,0 | 0,00 |
| 863 | `3M71Fct47s7YhHr7PiF9Bx3puVP5PTkPBaPR4Pfesqnk` | 277720881 | 15/07 16:54:55 | 1,000 | 0,143 | 1,00 | 0,0 | 0,00 |
| 864 | `13qZC9NxSrhSZxhnKXNYKVwa895z9cmsYPKTxncGFmcp` | 277720889 | 15/07 16:54:59 | 0,500 | 0,073 | 70,50 | -25.2 | 0,00 |
| 865 | `HiHjHb8WUvKa6KybSakVxdwBkkQYFtQZdXxH6k5pPJ39` | 277720903 | 15/07 16:55:05 | 9,900 | 1,356 | 9,90 | 3,1 | 0,00 |
| 866 | `pHxTahF1iCMAhY69pmacWveKSXW4iKKN7NutaWQFYR9` | 277720909 | 15/07 16:55:08 | 1,000 | 0,139 | 1,00 | -0.4 | 0,00 |
| 867 | `7vcwFb9pyknd771bz2tvJBCLhayWiRPTi2LSG19Mxowe` | 277720913 | 15/07 16:55:09 | 1,000 | 0,140 | 1,00 | -0.1 | 0,00 |
| 868 | `8bCChpmWsr1vB6Lg8yZn7EXhvCkcY287TecXMzoZUV3o` | 277720915 | 15/07 16:55:10 | 1,000 | 0,140 | 21,00 | -18.0 | 0,00 |
| 869 | `DtfHSNhSDrbHNYvc6SwPEz5w8NuLNDy5NbXzsHi2G8Xt` | 277720920 | 15/07 16:55:13 | 10,000 | 1,295 | 15,00 | 3,4 | 0,00 |
| 870 | `5qnqGMqVwMGyrt1bxoEp8BcVWoWbovUZurmFyKf7Ne8E` | 277720923 | 15/07 16:55:14 | 10,000 | 1,321 | 10,00 | 0,1 | 0,00 |
| 871 | `A4vcNBzUNxEXr5PFC9pUeKzwNiRvyTsaApXkg1bCbDVd` | 277720923 | 15/07 16:55:14 | 10,000 | 1,251 | 10,00 | 0,0 | 0,00 |
| 872 | `BP5S62ypMjucnhFhZ4DhZtVZBY663Mmu3gWpnKXXtH1F` | 277720932 | 15/07 16:55:18 | 0,990 | 0,120 | 0,99 | 0,4 | 0,00 |
| 873 | `6JY2SQR5RfFRejQySXxJYkTDBix2tBw5wjZdBNahvmoc` | 277720937 | 15/07 16:55:20 | 3,000 | 0,357 | 3,00 | 74,4 | 0,00 |
| 874 | `2eqXTbykS8shPH2j1q17J4ewWUiRHATSYoEZWrDTGDqF` | 277720941 | 15/07 16:55:22 | 4,962 | 0,625 | 4,96 | 2,6 | 0,00 |
| 875 | `EWyV7Y8sqjoXVPhe9KmecJVeJt8qDHPQtBjFoFHooXMF` | 277720943 | 15/07 16:55:23 | 0,500 | 0,061 | 1,50 | 0,7 | 0,00 |
| 876 | `6NJojUNdnuvQoKzkSsMACiwPwZDpV6Y8Q4xTAQYngrH3` | 277720954 | 15/07 16:55:28 | 0,099 | 0,013 | 0,94 | -0.1 | 0,00 |
| 877 | `3XzzqaGN7Hop2z6gRiWrx72uJSP9wbMg7GxCaVYE2ec3` | 277720978 | 15/07 16:55:39 | 0,065 | 0,009 | 0,06 | -0.0 | 0,00 |
| 878 | `AGseT8871WpBEi6QKLkVUo8VS34M6XnwxhvwCpT435he` | 277721007 | 15/07 16:55:52 | 2,000 | 0,278 | 16,00 | 0,2 | 0,00 |
| 879 | `5eQ8aGfsJLkvawp6goP5DYhkfQyTqsw49KmLucQpCxpA` | 277721013 | 15/07 16:55:55 | 9,901 | 1,329 | 19,80 | 207,2 | 0,00 |
| 880 | `EFLpYvWB4f49zvS3JUqt6TdVrM13kEFLc83na49TY4dE` | 277721017 | 15/07 16:55:57 | 0,189 | 0,025 | 0,58 | -0.1 | 0,00 |
| 881 | `DKgvpfttzmJqZXdavDwTxwSVkajibjzJnN2FA99dyciK` | 277721020 | 15/07 16:55:59 | 24,750 | 3,151 | 94,05 | -28.3 | 0,00 |
| 882 | `BEX5JEfAdbJszPQmXZWaSKF9WcLMjNmGa1PRTpivEc2t` | 277721022 | 15/07 16:55:59 | 3,500 | 0,422 | 10,50 | 0,3 | 0,00 |
| 883 | `BrtB8KvG1Ckk1t4oUXd1bJFMocARmFMB4gEFCS4XHngQ` | 277721024 | 15/07 16:56:01 | 0,050 | 0,006 | 0,05 | 0,1 | 0,00 |
| 884 | `CrbRdA6Qup2AvztyxFJfHd9xGzUxMP58Z94ibCSpdhoR` | 277721024 | 15/07 16:56:01 | 0,100 | 0,012 | 0,30 | 0,1 | 0,00 |
| 885 | `B5QoqGXJJGzHn9vxASgUv3QLH2cwuCSQBf6yFTEsMJgB` | 277721024 | 15/07 16:56:01 | 0,500 | 0,060 | 1,50 | -1.0 | 0,00 |
| 886 | `5zwmmvQtqbFjAMyFPhLwEUV1wcwqM5bwLfFC2WxKSNuy` | 277721024 | 15/07 16:56:01 | 0,050 | 0,006 | 0,15 | 0,0 | 0,00 |
| 887 | `GiixUMSFRNrvQ3ZD7JCFLjd36aTVcEEZRNLZLGBoTkQV` | 277721027 | 15/07 16:56:02 | 0,050 | 0,006 | 0,25 | -0.1 | 0,00 |
| 888 | `6R55G3ebShUC4a27Js2yHhiHe5v7FTFLqVKDtJNiw6f5` | 277721033 | 15/07 16:56:05 | 0,247 | 0,034 | 0,94 | -0.4 | 0,00 |
| 889 | `FbJh3AJiZGxiC7A7sS4jN2yDYZ42mn86nCwp8VpXx4dQ` | 277721036 | 15/07 16:56:07 | 0,080 | 0,011 | 0,08 | 0,0 | 0,00 |
| 890 | `6W3Z732QBdnxLPSi5kx1EURsEAoc7PiMbhMV9c6bTHVK` | 277721039 | 15/07 16:56:07 | 0,140 | 0,019 | 0,14 | -0.1 | 0,00 |
| 891 | `B1jpTKUwqmQfiFRzKtk2p9AJ8fihUqtULDidjnEX53ed` | 277721040 | 15/07 16:56:08 | 0,002 | 0,000 | 0,00 | -0.0 | 0,00 |
| 892 | `CMKgzJ4d5kSodnfot6aEKDz4GHWeqTTfhKfh6GMj3yTC` | 277721043 | 15/07 16:56:09 | 0,500 | 0,070 | 4,50 | 2,5 | 0,00 |
| 893 | `DgNwDfonMXxwuRxFXBmnc7jamnXhWodzDJSt2AVN5j1T` | 277721060 | 15/07 16:56:18 | 0,150 | 0,022 | 0,15 | 0,0 | 0,00 |
| 894 | `G3qx9PwFUVpiG4BMFqqQKdy7zDvzJZ1kjUuBdwreMar5` | 277721061 | 15/07 16:56:18 | 0,080 | 0,012 | 0,08 | 0,1 | 0,00 |
| 895 | `BJoBbAu3hqBRGYVp9tuR1yp4NbvrwzYgajLtPVhTZgdo` | 277721063 | 15/07 16:56:19 | 4,950 | 0,723 | 59,40 | 12,4 | 0,00 |
| 896 | `D1KBfZWPFvVAD1qxj4FdbzTXmiY8PGFumKTqMx5jAx5Q` | 277721073 | 15/07 16:56:23 | 2,475 | 0,367 | 419,87 | -288.7 | 0,00 |
| 897 | `2cxjRs8bt5EBxbcSJkY1AXLX5UCYq23pWn83EckDMdCv` | 277721073 | 15/07 16:56:23 | 9,900 | 1,417 | 247,50 | 154,6 | 0,00 |
| 898 | `FfJfkBPrjCZA8NX2m59Cg1R5FC3m3DfPK9SfhEzeYPnz` | 277721076 | 15/07 16:56:25 | 0,099 | 0,014 | 0,10 | 2,3 | 0,00 |
| 899 | `3jm7rzfXkKMhQqZxq1NwWCgeYMuvCP481ASa9GkS6FqQ` | 277721081 | 15/07 16:56:27 | 0,200 | 0,029 | 0,20 | 0,3 | 0,00 |
| 900 | `GP6D4jcbGpbKvjuFR9NVytXQAXxNKw2w4MauQNRz4EUm` | 277721082 | 15/07 16:56:27 | 0,500 | 0,071 | 2,20 | -0.7 | 0,00 |
| 901 | `7HP8S61Jij9gDS6zcQ41zP9NEh8cx9zT4JLK3Yj9YgeC` | 277721091 | 15/07 16:56:32 | 4,950 | 0,696 | 9,90 | 5,2 | 0,00 |
| 902 | `4gVwFzkPwX1reY1GJSbhHvkDbXo9ALM5yzd33Hio4ngk` | 277721096 | 15/07 16:56:35 | 4,950 | 0,644 | 137,61 | 6,5 | 0,00 |
| 903 | `6HUqdT1GHwT3YexzF7xbwjyhbm6YtjJ2SZho5wc2e9Yc` | 277721110 | 15/07 16:56:42 | 2,200 | 0,274 | 163,35 | 254,7 | 0,00 |
| 904 | `FHFSFfwE9CiAZJMxcEC1VW2a5tAMYHqtKbFjBTsWopao` | 277721112 | 15/07 16:56:43 | 0,990 | 0,124 | 1,98 | 1,6 | 0,00 |
| 905 | `E3Btto2Md2KujnL3bzu1e94D6fuwhyo3eDRa1rgtffSC` | 277721114 | 15/07 16:56:43 | 10,000 | 1,299 | 820,00 | -52.8 | 0,00 |
| 906 | `3yLJmveo9sf1XdwmZdTUVRxUa7pggRUys8hbVKGhQuCJ` | 277721132 | 15/07 16:56:51 | 0,990 | 0,125 | 8,91 | 0,6 | 0,00 |
| 907 | `7xvXcftveYtsgVjwgaqwM5u1TwmLWChkByLaHNT91E5z` | 277721140 | 15/07 16:56:54 | 9,900 | 1,213 | 44,55 | -10.3 | 0,00 |
| 908 | `Hd21XNFPbbinut8pUGMVUnqqCGvkgvwTs4bVssnoUQw2` | 277721141 | 15/07 16:56:54 | 12,000 | 1,388 | 166,73 | -15.0 | 0,00 |
| 909 | `7QZ9vAkrED9At3p7vUnmzgbFXeR4tSDB81a6JXNjMm43` | 277721148 | 15/07 16:56:58 | 4,950 | 0,563 | 7,92 | -2.8 | 0,00 |
| 910 | `GQ26EXd1K4cbSiPaCxDTLNmt63Ef6AUFNo8aXNe1KhBf` | 277721149 | 15/07 16:56:58 | 10,000 | 1,102 | 210,00 | 0,3 | 0,00 |
| 911 | `GXZfBB4rgSTmoaJmcSMEy1jCrd2ya8W5GFTC51xYwJza` | 277721151 | 15/07 16:56:59 | 0,500 | 0,054 | 0,50 | 0,3 | 0,00 |
| 912 | `C4vs5woNqbLqDvFZdhecuqYNYVve62Z4qoVqF4axzyDP` | 277721160 | 15/07 16:57:03 | 0,500 | 0,054 | 1,45 | 20,9 | 0,00 |
| 913 | `B9DqARH37rMLdyMHc1wmVX53q5BF6YRHzUrppLKTBXR9` | 277721189 | 15/07 16:57:17 | 1,000 | 0,106 | 7,00 | 1,4 | 0,00 |
| 914 | `9bBi7QcfuSzc5jeUmFU3V4RLo8tsMKRA6vTemUvhcp98` | 277721189 | 15/07 16:57:17 | 0,300 | 0,032 | 0,30 | 0,2 | 0,00 |
| 915 | `FkEViZA85bv1k6eymQZNcy4Cwc887DAVMaZc5XEpf2L6` | 277721192 | 15/07 16:57:19 | 4,950 | 0,522 | 4,95 | -1.6 | 0,00 |
| 916 | `D7j3EY4oV8U7rAqhpD2YJjiiGQ8wAezvmsHsq87KRedu` | 277721208 | 15/07 16:57:26 | 0,100 | 0,010 | 0,10 | -0.1 | 0,00 |
| 917 | `5VLF9t9MJrqfZvmzzKBmbZeKKrEqCbhEZzoVKzaafdF2` | 277721216 | 15/07 16:57:29 | 0,495 | 0,050 | 26,23 | 0,4 | 0,00 |
| 918 | `AgPsPtpAiQqMtcmSsGEGvje1dXTco3NGi1gAF7gvYC7L` | 277721234 | 15/07 16:57:38 | 0,250 | 0,027 | 6,83 | 0,2 | 0,00 |
| 919 | `8GtQhiyph4cuc6fvQMXNXA9egUBou3zGFHaaDWk47QpX` | 277721235 | 15/07 16:57:38 | 5,000 | 0,538 | 6,00 | 3,5 | 0,00 |
| 920 | `8A1HLL8PhK9yeofuj2BRvAFvQUzsMk6oZvVngeCoHJ9M` | 277721242 | 15/07 16:57:41 | 3,000 | 0,317 | 37,50 | -15.4 | 0,00 |
| 921 | `6bKNmmyckNZNtcgPbxZU9arsQwGEFosvZtLGsXixhxED` | 277721244 | 15/07 16:57:43 | 30,000 | 2,928 | 3 341,50 | -808.2 | 0,00 |
| 922 | `DydnZica7gYa4PuhSdnwWujoh12prHoBHi9cB9cQFEuN` | 277721245 | 15/07 16:57:43 | 0,200 | 0,018 | 0,20 | 0,1 | 0,00 |
| 923 | `9Pei378iQbg5VjvwTPXw8hhkfaDRU4Jo9ofCigRvSxWm` | 277721254 | 15/07 16:57:48 | 5,000 | 0,468 | 55,00 | -2.4 | 0,00 |
| 924 | `24QgyAUJeLWLwZfapyLY22x56xvXfc9tYedrkJaFuEM8` | 277721254 | 15/07 16:57:48 | 0,050 | 0,005 | 0,08 | -0.0 | 0,00 |
| 925 | `5wQaABAbgA52cBks6zqXmk9nFftZgy18f78im6UxXhNU` | 277721265 | 15/07 16:57:53 | 20,000 | 1,837 | 20,00 | 2,8 | 0,00 |
| 926 | `Dd5fYguD4vwiyuNEFCXE6Vczb3MkiGKoW3xTCCLvqaDJ` | 277721268 | 15/07 16:57:54 | 20,000 | 1,678 | 21,50 | 2,1 | 0,00 |
| 927 | `F3TBLxjAPCwBmdoN6s8pwLTSojP14S46vJdxhjLfB8du` | 277721274 | 15/07 16:57:58 | 0,500 | 0,040 | 0,50 | 0,0 | 0,00 |
| 928 | `2jwiMYSEyESGxPw5vKDdiR1kCNEdFwNrwBJK4CVmPvUf` | 277721274 | 15/07 16:57:58 | 1,000 | 0,080 | 31,00 | 0,9 | 0,00 |
| 929 | `BpdRwLLjJXPew8qcmR8tSnjS1mryjTMtVD8c9czu6boH` | 277721275 | 15/07 16:57:58 | 0,500 | 0,040 | 0,50 | -0.0 | 0,00 |
| 930 | `4zY7eP4x5r8Pmv7Q2jeMGTqogtgvqGFXTF3XhbsH3Dn4` | 277721276 | 15/07 16:57:59 | 5,000 | 0,394 | 5,00 | -2.1 | 0,00 |
| 931 | `wNryapC8deX4SercjAXPchqEQfY9XFdarUVBt3YhZZW` | 277721277 | 15/07 16:57:59 | 0,720 | 0,056 | 0,72 | -0.0 | 0,00 |
| 932 | `8Hw9X9UwBso7Sp2CFnEEeUGW8pGDj9wghc78ccWFZWpU` | 277721278 | 15/07 16:58:00 | 9,900 | 0,754 | 34,65 | 44,1 | 0,00 |
| 933 | `HET8ALFb24vuWtQDxWkuNNqjRjKzFWFJD6UM5wu69TyG` | 277721281 | 15/07 16:58:01 | 0,453 | 0,034 | 0,45 | 0,1 | 0,00 |
| 934 | `8ZCTJAkCJYdCatjS71d8bTq3cEf6vp3AARMZWewdkirf` | 277721284 | 15/07 16:58:03 | 1,000 | 0,075 | 1,00 | -0.1 | 0,00 |
| 935 | `ANnFtVsyCwa22wJZbfRVRMRvnZSDvcxopdzJAnogsx85` | 277721285 | 15/07 16:58:03 | 2,000 | 0,136 | 4,00 | -3.0 | 0,00 |
| 936 | `5G6LnLPQA5a4SgHtCM83ZStxLPwPAnzYATjABy4Uvh6f` | 277721286 | 15/07 16:58:03 | 0,130 | 0,009 | 0,13 | 0,0 | 0,00 |
| 937 | `2U5HsRVvZCGcmQQ5JKoGs2HmzXr3jkX2Ah9BV4XcXsDs` | 277721288 | 15/07 16:58:04 | 0,076 | 0,005 | 0,08 | -0.0 | 0,00 |
| 938 | `BoQ6eDEtTQbXMS6caFPajjp3DdnRu6jmwJPryyQaCXrg` | 277721289 | 15/07 16:58:04 | 1,000 | 0,067 | 3,00 | -1.5 | 0,00 |
| 939 | `U2SMVXhAWQmwyPHCKr1xiYPu86WcoQor1DRRtWbrLNE` | 277721292 | 15/07 16:58:06 | 1,980 | 0,133 | 6,93 | -1.9 | 0,00 |
| 940 | `9GHnccVUKwNcPBsv3a9tEF6VGgThwoea8TNnaqoLHyhv` | 277721296 | 15/07 16:58:08 | 0,150 | 0,010 | 1,35 | 0,7 | 0,00 |
| 941 | `4sX2YuQzcB6RCF929r38JAMrXshtcMRiZEPSmC4kgnD8` | 277721296 | 15/07 16:58:08 | 0,250 | 0,017 | 0,85 | 3,8 | 0,00 |
| 942 | `6CD7UAyYhYGcHxcDwa4q9kAVeHaDAF3H4BQvkajsSAKZ` | 277721304 | 15/07 16:58:11 | 9,900 | 0,597 | 9,90 | 2,2 | 0,00 |
| 943 | `669BSKLJjTSdH6bYF6aNEynfJJroTGSinceuWv21wC9T` | 277721307 | 15/07 16:58:12 | 5,000 | 0,293 | 10,00 | -6.6 | 0,00 |
| 944 | `o5kiZ3ozwddacRUAs1CbNuzZd9hG3aN6FHdLw2rJVTX` | 277721307 | 15/07 16:58:12 | 1,000 | 0,058 | 1,50 | -1.2 | 0,00 |
| 945 | `2PCpLxqZHEUKSc4Ns1dMvAKmJXLh3prtzu3ZJ2oZxn8K` | 277721308 | 15/07 16:58:13 | 1,980 | 0,114 | 1,98 | -0.3 | 0,00 |
| 946 | `7FkyNLvL2eZuzDPw5fbDTQepsJ3ZgzmSxFWARedrvQUm` | 277721309 | 15/07 16:58:13 | 1,000 | 0,057 | 6,00 | -0.9 | 0,00 |
| 947 | `ENdw8JWyTWFVq8ocPwrB7QCu5SGGdYcFbh16iiz5W1CL` | 277721309 | 15/07 16:58:13 | 5,000 | 0,284 | 5,00 | -1.1 | 0,00 |
| 948 | `8yszVVELBTsLYcYeFAbx2wShLu62UUkmBNq4C765oFm7` | 277721309 | 15/07 16:58:13 | 1,980 | 0,111 | 1,98 | -0.3 | 0,00 |
| 949 | `8r2275LAAvaNQZR5U1z4xdCfixE4NMP7HSTJdJEAqpGv` | 277721312 | 15/07 16:58:15 | 15,000 | 0,816 | 20,00 | -11.6 | 0,00 |
| 950 | `2Xcbas4qSnB1rtJhQUUxBGiWoVjQuuSvYsLpvdHY54ED` | 277721312 | 15/07 16:58:15 | 5,000 | 0,262 | 5,00 | -0.7 | 0,00 |
| 951 | `fXnXpjveAF1vy57VRVWWveatHisxAXRYx9qPJ3FVron` | 277721316 | 15/07 16:58:16 | 9,900 | 0,507 | 9,90 | -3.1 | 0,00 |
| 952 | `5kvY5pFMPQc8kjsFRahsbDvDTAY5Ekcmr5ZjQGRFb8PS` | 277721317 | 15/07 16:58:16 | 2,000 | 0,100 | 6,00 | -3.2 | 0,00 |
| 953 | `FZCtmtcfQ4mF1Nxy5tv2dLrXzTbi77Rq5BSvHajtBAk4` | 277721320 | 15/07 16:58:18 | 9,901 | 0,493 | 19,80 | -2.5 | 0,00 |
| 954 | `2ZBQmC1yUU8qRa8y6WV7UKirXpvWEdZB2xXDspzj6HLk` | 277721320 | 15/07 16:58:18 | 1,000 | 0,049 | 76,00 | 7,0 | 0,00 |
| 955 | `4Mz8LUHrFi1umWLTb4BvMHMLvKawiE9KZ8JbLuXUTSFe` | 277721321 | 15/07 16:58:18 | 2,500 | 0,121 | 2,50 | -2.1 | 0,00 |
| 956 | `BRu1ykwX3jnXte2tUskTh4QcWCQP2LTMoeJtkrqJ6uyk` | 277721323 | 15/07 16:58:20 | 1,000 | 0,049 | 1,00 | -0.7 | 0,00 |
| 957 | `2EX432GBXct64ZKAiUN7Buk8Jskv2KxkPmgc944yAtW7` | 277721325 | 15/07 16:58:20 | 0,297 | 0,015 | 0,30 | -0.1 | 0,00 |
| 958 | `uj41vD41kNfMT8xU3cFKEAvsV8pBLxZeT9k3T8QJwgR` | 277721326 | 15/07 16:58:21 | 0,100 | 0,005 | 0,14 | -0.1 | 0,00 |
| 959 | `7rBsMzstp18yDPCvDdWqUcjvAz1eRqgNobPRMoC5j8aq` | 277721331 | 15/07 16:58:23 | 1,000 | 0,050 | 1,50 | -0.7 | 0,00 |
| 960 | `7utFnhb3BRqgPXjemsusT4GijbDTdEPydQeoHwbDgdu4` | 277721331 | 15/07 16:58:23 | 1,000 | 0,050 | 2,00 | -1.5 | 0,00 |
| 961 | `CFqvjiaHR4P76biCBoqWLcWiTCwJCdoMfjM4gsQXZSyY` | 277721333 | 15/07 16:58:23 | 25,000 | 1,199 | 25,00 | -9.7 | 0,00 |
| 962 | `iCXXCUrTk5P7hUGr6gbto2difywhkgYM1c4bW6cnCUm` | 277721337 | 15/07 16:58:26 | 1,000 | 0,064 | 1,00 | -0.3 | 0,00 |
| 963 | `CdYvHhdXt5EyWni1s6f2wEx5p6WQUEPnerDYnDVroarK` | 277721338 | 15/07 16:58:27 | 0,179 | 0,012 | 0,81 | -0.0 | 0,00 |
| 964 | `BKGQbZwYAk3yUmGsRNEVfKY4NrHEsPSLuRf23q17YTxZ` | 277721344 | 15/07 16:58:29 | 0,250 | 0,016 | 0,25 | -0.2 | 0,00 |
| 965 | `43TfZXbtSNatR1HnrwzCgQ87iEFGnjoAFZBted9VcaG6` | 277721344 | 15/07 16:58:29 | 15,000 | 0,952 | 48,00 | -0.3 | 0,00 |
| 966 | `D8TUVVXoYfouwuGWsiyqJJ7izEGtnBhV1Xa7DwXadoRE` | 277721345 | 15/07 16:58:29 | 0,200 | 0,012 | 2,40 | -0.2 | 0,00 |
| 967 | `5qXMG6JtMaPENmajSUmgNdHmDVCtR8XcyVWesHAkauRr` | 277721345 | 15/07 16:58:29 | 0,497 | 0,030 | 5,20 | -0.2 | 0,00 |
| 968 | `FXWWph4ChEZW6As1v4GUoAVRpT2XFmegws4BUUb3wjVW` | 277721346 | 15/07 16:58:30 | 9,900 | 0,590 | 9,90 | 2,0 | 0,00 |
| 969 | `FWh2ECivHqpsCiPtJiVePQTj5tkqueubSwufZamcbHdJ` | 277721346 | 15/07 16:58:30 | 0,100 | 0,006 | 0,20 | -0.1 | 0,00 |
| 970 | `5ECJRxtixX8exysTBoAHAhXr5gWTmvxs1eg3vfSztekn` | 277721349 | 15/07 16:58:31 | 0,099 | 0,006 | 0,20 | -0.0 | 0,00 |
| 971 | `En9k2qRCb9qwrWxE1rqrGYVC5qJfDdGs4H2nyaAZhbdL` | 277721352 | 15/07 16:58:33 | 10,000 | 0,575 | 20,00 | -11.8 | 0,00 |
| 972 | `EEbhYqSd4PQbjw6M2AQG8mqvfswB2wixv6EVHvTz8x4r` | 277721352 | 15/07 16:58:33 | 4,950 | 0,277 | 4,95 | 0,5 | 0,00 |
| 973 | `CY6S8UB3sEgUbHR5r5knPk1zp8fgguFwt5rRkRTNajVb` | 277721353 | 15/07 16:58:33 | 1,000 | 0,055 | 2,30 | -1.3 | 0,00 |
| 974 | `7WNou8DqaWTnveECZoboV8o2jCyQJ2ebLW554q76yctL` | 277721354 | 15/07 16:58:33 | 9,900 | 0,541 | 218,80 | -33.6 | 0,00 |
| 975 | `JBib9Ahy67QfXH74viXkQwrUV5hdd8k8KXmxZL8Qkavz` | 277721354 | 15/07 16:58:33 | 20,000 | 1,036 | 20,00 | -4.7 | 0,00 |
| 976 | `ASUyichxo66odQhpSFxeEzEM4ofmenRLqavAVqA3HAQk` | 277721364 | 15/07 16:58:38 | 3,000 | 0,143 | 3,00 | -1.6 | 0,00 |
| 977 | `RichswLQjgkzvbyrZYxkjj1fdgtLN7Za58vsafGPqAw` | 277721364 | 15/07 16:58:38 | 1,000 | 0,047 | 1,00 | -0.4 | 0,00 |
| 978 | `J85hGxCx6U9bdeMS4zRyuefyaJtPVQG1udaFqVK8Ky6s` | 277721365 | 15/07 16:58:38 | 0,200 | 0,010 | 0,20 | -0.1 | 0,00 |
| 979 | `FVcFW4jFERZpMyxuU5WZXmSDYhXjjSRWFMUBZbzxDoby` | 277721367 | 15/07 16:58:40 | 4,950 | 0,241 | 10,89 | -6.3 | 0,00 |
| 980 | `3TZ9Z5VLHLAZfdvCB2JFg2SLVUgZvq5JnKewTXnrEKbE` | 277721377 | 15/07 16:58:43 | 0,005 | 0,000 | 0,00 | -0.0 | 0,00 |
| 981 | `Cv6Pr18KKNaG3RvBDq258grvA9YLEiwMRNwPBkpoUwMM` | 277721378 | 15/07 16:58:44 | 0,500 | 0,025 | 1,00 | 6,6 | 0,00 |
| 982 | `EXMttShCJdaoDe55sbssWAR8qrh8e8wbZaMVj6gWZ6v4` | 277721388 | 15/07 16:58:49 | 0,990 | 0,061 | 9,99 | -5.9 | 0,00 |
| 983 | `4yQE6SEMqW9DUMnPW5U6AhijY5dWyjDi2ZEtzMwiA1X6` | 277721395 | 15/07 16:58:51 | 0,100 | 0,006 | 0,10 | -0.1 | 0,00 |
| 984 | `CQnf6SXc3CXMpJPivtr7S8YVtyHPoVFbZnubtQ6n4Nhv` | 277721400 | 15/07 16:58:54 | 3,960 | 0,243 | 3,96 | 0,0 | 0,24 |
| 985 | `EqQzi6axvQnCwJx2J7ovcYoY5rFsmbiCgw1kAYCRRwJn` | 277721401 | 15/07 16:58:54 | 2,000 | 0,121 | 2,00 | -1.1 | 0,00 |
| 986 | `BGzNaHyAX32wL8Vecd2uS2PaX8f45QUof6Si7pvJx1dj` | 277721402 | 15/07 16:58:55 | 0,500 | 0,030 | 0,80 | -0.4 | 0,00 |
| 987 | `HMd15vPTMg6s8f8xSKhNfvYaqUM2VHMqUqpKHQgAQhHA` | 277721409 | 15/07 16:58:58 | 1,980 | 0,131 | 7,92 | -4.7 | 0,00 |
| 988 | `GG2tZubU6MerRt6Cx5pMC4xtp8Mk3KEqTkqXPLBAGkcN` | 277721416 | 15/07 16:59:02 | 4,000 | 0,264 | 24,00 | -3.4 | 0,00 |
| 989 | `5sHCYpdkgR4WeAqirCMSu1fmr3qFVxJwS555saFZTfPp` | 277721418 | 15/07 16:59:03 | 3,000 | 0,197 | 8,50 | -3.2 | 0,00 |
| 990 | `FydGWrVmqtPtyUvFnbMMtv8WuHFVNuVBc2TAogFN6duR` | 277721419 | 15/07 16:59:03 | 0,050 | 0,003 | 0,09 | 1,0 | 0,00 |
| 991 | `9f3auDyGomvQPQmjDFitBWiRMrSUhRdCEbvzq7gGAc9Y` | 277721427 | 15/07 16:59:07 | 0,100 | 0,007 | 0,20 | 0,7 | 0,00 |
| 992 | `opWm8TJsJLkmXGD1QriCFi3CgCav5S8Wte4kyWgLLM7` | 277721427 | 15/07 16:59:07 | 0,150 | 0,011 | 0,15 | -0.1 | 0,00 |
| 993 | `FypTLjtQMCBC18BGYxsdMhCz256HbbMDy6Nr9nthpF2Z` | 277721429 | 15/07 16:59:07 | 0,250 | 0,018 | 0,35 | -0.2 | 0,00 |
| 994 | `CmtcXpY7CCFEaxEoyKXvuGJqqc2u25TUnoL8YQZbWNZm` | 277721432 | 15/07 16:59:09 | 0,100 | 0,007 | 0,20 | -0.1 | 0,00 |
| 995 | `E6jKjUStwHTpeCggxi36YrmH8ZfJVz5seoRNDHnyYrzJ` | 277721443 | 15/07 16:59:14 | 1,414 | 0,114 | 1,41 | -0.6 | 0,00 |
| 996 | `AwbqGAyLb1scfGhPWSgfZR6F8EpC91gYwLidjrQ1KaJd` | 277721443 | 15/07 16:59:14 | 0,247 | 0,020 | 0,49 | -0.3 | 0,00 |
| 997 | `9W4y47eR9eqrTUvziqic37e9mz7VC4CkcWmSRRwyPv8q` | 277721450 | 15/07 16:59:17 | 17,000 | 1,187 | 17,00 | -12.3 | 0,00 |
| 998 | `49J648RxFF5raRNzabw3FMPzMDMKo2og8LbLwZccqLg2` | 277721457 | 15/07 16:59:20 | 5,940 | 0,612 | 52,47 | 7,4 | 0,00 |
| 999 | `ErP2uLSVN2p17d4VPJzGWb9U88tNrSCDdP3rm4C9KTyW` | 277721457 | 15/07 16:59:20 | 4,950 | 0,497 | 2 732,40 | 122,7 | 0,00 |
| 1000 | `D4LcpxEj5ryL6ZPikTABGkEa5846KATEmJd9ANNJGAyk` | 277721459 | 15/07 16:59:21 | 0,200 | 0,018 | 0,50 | -0.2 | 0,00 |
