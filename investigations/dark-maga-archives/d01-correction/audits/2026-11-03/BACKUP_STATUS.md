# État des sauvegardes, enquête Dark MAGA

Relevé du 03/11/2026, commit de référence `01ae5a4`. Contrôles lancés depuis ce Mac, scripts dans `tools/`.

## Verdict
**VULNÉRABILITÉ OUVERTE : les données brutes n'ont qu'une seule copie physique.** Aucune seconde destination physique indépendante n'est disponible sur ce Mac aujourd'hui. Rien n'a été copié, rien n'a été déplacé, rien n'a été supprimé.

## Où sont les données

| Quoi | Taille | Copie 1 | Copie 2 |
|---|---|---|---|
| Brut listé au manifeste (`raw/` sauf `ctrl_tx`, `data/`) | 7,08 Go, 33 033 fichiers | `/Volumes/VERBATIM HD/Dark-MAGA-Investigation` | **aucune** |
| Brut des comparateurs (`raw/ctrl_tx`) | 12,57 Go, 16 548 fichiers | même disque | **aucune** |
| Code, rapports, étude gelée, preuves légères | 208 Mo | `~/Projects/Dark-MAGA-Investigation` | GitHub privé, jusqu'au commit poussé |
| Instantané du projet | 13,7 Mo | `project_snapshot_20261103.tar.gz` sur VERBATIM | sans objet |

Le disque VERBATIM est un seul disque USB mécanique en FAT32. Si ce disque meurt, le brut disparaît. Il faudra le recollecter chez Helius. Le coût n'a pas été mesuré ici, l'amendement 001 estime déjà environ 2 millions de crédits pour une partie des comparateurs. Les preuves X et Wayback légères survivraient, elles sont dans le dépôt.

## Contrôle d'intégrité fait aujourd'hui
- `evidence/RAW_MANIFEST.tsv` : **33 033 fichiers sur 33 033 conformes, 0 différent, 0 manquant**, 7,08 Go relus en 685 s. Sortie : `work_integrity/raw_verify.json`.
- `evidence/MANIFEST.sha256` (preuves légères) : aucun écart à `shasum -c`.
- **Trou du manifeste :** `scripts/mk_manifest.py` exclut `ctrl_tx`. Les 12,57 Go de transactions des comparateurs, soit tout ce qui alimente le test gelé, n'avaient aucune empreinte. Empreintes créées aujourd'hui : `work_integrity/CTRL_TX_MANIFEST.tsv`, 16 548 lignes. Limite : ce manifeste date du 03/11 08:30 UTC, il protège pour la suite, il ne prouve pas que ces fichiers n'ont pas bougé depuis leur collecte.
- `etude_final/` : `gel.py verifier` dit intact, 17 fichiers conformes au gel du 02/11 23:47:06 UTC.

## Destinations recherchées

| Destination | Résultat | Utilisable ? |
|---|---|---|
| Disques externes | `diskutil list` : un seul, disk4, VERBATIM | Non, c'est la source |
| `/Volumes/PHI-Data` | image disque posée sur le même VERBATIM | Non, même disque physique |
| Time Machine | `tmutil destinationinfo` : aucune destination | Non |
| Disque interne | 25,9 Go libres, plancher 13,5 Go, soit 12,4 Go au mieux, pour 19,65 Go à copier | Non, et consigne : ne pas le remplir |
| iCloud | `brctl quota` : 0 octet restant | Non |
| rclone | aucune configuration | Non |
| SSH, NAS | `~/.ssh/config` sans hôte, aucun partage monté | Non |
| Appareil adb `192.168.1.98` | Smart TV, 2,9 Go libres | Non |
| GitHub | 67 Mo sur le dépôt privé, sans le brut | Non, pas une sauvegarde complète |

## Ce qui reste à décider par Benjamin
1. **Le vrai correctif :** brancher un second disque physique d'au moins 32 Go, hors de ce Mac et rangé ailleurs. Ensuite, copie et relecture par les deux manifestes, une heure environ sur ce disque mécanique.
2. **Palliatif partiel, non fait :** copier sur le disque interne les parquet dérivés (`data/` sans `controls` et sans shards, environ 0,23 Go) sous `diskguard.py run`. Cela ne protège pas le brut, cela évite seulement de refaire les calculs si le brut est recollecté.
3. **Palliatif réseau, non fait :** paquets chiffrés avec `age` dans les GitHub Releases du dépôt privé, comme le fait déjà `phi-backup`. Faisable techniquement, mais 19,65 Go sur GitHub demande ton accord.

## Ce qui protège déjà
Les manifestes, dont `CTRL_TX_MANIFEST.tsv`, partent sur GitHub avec ce rapport. Une recollecte future pourra donc être comparée aux empreintes de la collecte d'origine, sous réserve que les réponses de Helius soient rendues à l'identique, ce qui n'a pas été testé octet par octet à grande échelle.
