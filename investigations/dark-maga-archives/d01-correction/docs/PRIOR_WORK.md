# Inventaire de l'ancien travail sur Dark MAGA

Recherche faite le 02/11/2026 sur `~/Projects`, `~/Documents`, `~/Desktop`, `~/Downloads`,
`~/GitHub-History-Backups`, les dépôts GitHub de `searadacunha`, les transcriptions Claude et Codex.
Termes : DMAGA, Dark MAGA, DarkMagaCoin, kikisknees, Aristos_Revenge, ChrisWinig, le mint, le wallet 9PrmF8.

## Constat principal
**Aucun dossier d'enquête Dark MAGA n'existe sur ce Mac.** Il n'y a ni `*dmaga*` ni script conservé.
Le travail retrouvé tient dans une seule session du 02/08/2026 :
`~/.claude/projects/-Users-benjamindacunha-Downloads/REDACTED_8cf04e823af2.jsonl`.
Ses scripts (`measure_two.py`, `buyers_dmaga.py`, `genesis_funding.py`) étaient dans un scratchpad
disparu. Seules leurs sorties restent dans la transcription. Attention : cette transcription contient
une clé Helius en clair dans une commande.

L'analyse des gros gagnants, des premiers comptes X et des relations décrite dans la mission n'a pas
été retrouvée sur ce Mac : elle a pu exister ailleurs (messages, autre machine). À préciser par Benjamin.

Les 38 autres transcriptions qui matchent le motif sont du bruit base64 (images), vérifié sur extraits.

## Ce que disait la session du 02/08/2026 (à revérifier, pas une source de vérité)
- Bonding curve `87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH`, slot de création 277417695.
- Pas de snipe de courbe : 0,2 SOL dans le slot de création, 10 acheteurs sur 7,7 SOL en 30 s.
- Acheteurs des 30 premières secondes selon `buyers_dmaga.py` :
  `DrKPLzTLWsk9w9ifHjr2QDkQ7nfJYoLmpXYtBhSoXe5g` 2,0246 SOL,
  `BNHsrnuv72vo91szVHnahB2eGYXPMcxWdFyPC4Xge4Fk` 1,9604,
  `BE5S5w9KyC9nrYhGWNQuRunKwP9avhubpiAaQMzf3DTD` 1,8763,
  `E1mh1Wfm7JK78fJSh3Ta8XwV43tuuAkhoikVCvvDWmeg` 1,0000 (voir note),
  `8D2AGAGPMZaPtZRyTgCSHnFfffAJ43RB1WBE6FaQ4FFw` 0,2139,
  `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` 0,2012,
  `Edq7kG2NREc5Z2HsiFBHbGiiUneprcpWg6Qodh4GPPy8` 0,1898,
  `EYykLfeAjyXCH1QojDeRFgoXmv3MfS24gZa8AordnezX` 0,1500,
  `Dj2a99M9EHGaxfQDqWmkp5y5mjbdg7nXWGeFK5GjQoqt` 0,0976,
  `GySdM4D2PcQGMubGgGmpbMPVX82Ys84pyvhYvyax8q16` 0,0001.
- La liste exacte est reconstruite dans `data/trades.parquet` et fait foi.
- « Aucun lien ChangeNOW trouvé » sur les 4 premiers acheteurs, en mode échantillon, genèse non atteinte.
  Conclusion faible à refaire avec un historique complet.
- Le token frère évoqué : Kekius Maximus `XC78JjRHnSqaysrHiTrhR8eRngFbvX3rrHyRjWEpump`, snipe de 81 % de
  la courbe, wallet `Go5rFkwKpTYGVck7emf4Uop81HBozmHHZfEhe2zJDY5u`. Hors du périmètre de cette enquête,
  gardé comme piste de comparaison.
- Le « créateur » commun aux deux tokens renvoyé par DAS (`TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM`)
  est l'autorité de mint de Pump.fun, présente sur tous ses tokens : ce n'est pas un lien.

## Récit de Benjamin dans cette session (déclaration, non vérifiée)
Il dit avoir interrogé des traders, de Bali à Los Angeles, parlé à une équipe derrière DMAGA et Kekius,
et revoir souvent une adresse deBridge (« DBR »). Rien de cela n'est documenté dans les fichiers trouvés.
À traiter comme hypothèse. Il peut fournir ses notes s'il les a.

## Méthodes réutilisables du dépôt WSMO
`~/Documents/Crypto/WSMO-portfolio/code/` : `05_trace_origin.py` (remontée de financement),
`09_bundle_snipe.py` (courbe, slot 0), `hlib.py`, `lib_verif.py`, `a1_null_model.py`, `fetch_sol_usd.py`.
Lecture seule. Le dépôt `Why-Solana-Memecoins-Are-Over` n'est pas modifié par cette enquête.

## Données fortuites
`~/Documents/Crypto/WSMO-historical-edge-2024/historical_edge_2024/data/cache/getBlock/blk_acc_2948531*.json`
contient le mint : blocs d'octobre 2024 d'une autre étude, sans analyse de DMAGA.

## Non cherché à ce stade
Disques externes : une recherche ciblée reste à faire sur `/Volumes/VERBATIM HD` hors sauvegardes.
