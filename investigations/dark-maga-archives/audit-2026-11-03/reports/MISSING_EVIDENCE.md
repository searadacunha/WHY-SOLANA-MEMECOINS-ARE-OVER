# Preuves manquantes, accès refusés, pistes ouvertes

Ce qui n'a pas pu être établi, et pourquoi. Une absence n'est jamais rapportée ici comme une preuve d'absence.

## X et archives
| Élément | État | Cause | Ce qui débloquerait |
|---|---|---|---|
| Recherche X native (tous les posts d'un compte, toutes les réponses) | Partielle : 30 recherches en lecture seule le 03/11, `audits/2026-11-03/work_E/x_search_log.jsonl` | Une recherche ne rend pas une image seule sans mot-clé | Accès API X ou export d'un compte |
| Posts de @kikisknees du 14 au 26/07/2024 | 1 407 sur 1 419 indisponibles, dont 1 378 supprimés par l'auteur. Texte récupéré pour 208 via Wayback, plus 17 de @DarkMagaCoin | La Wayback a refusé la suite (connexion refusée, 503) | Reprendre la lecture Wayback plus tard, `evidence/x_cdx/kikisknees.json*` liste les identifiants |
| Images des posts supprimés de @kikisknees | En partie retrouvées dans la Wayback sous `?format=...&name=orig`, dont celle de 16:00:08 UTC : Trump « dark maga », pas le visuel de Musk | La plupart des 164 images 900 x 900 d'avant le 21/07 12:51 restent à relire | Reprendre la Wayback |
| Thread d'@Aristos_Revenge du 08/10/2024 | Texte lu par Thread Reader seulement | 20 posts supprimés par l'auteur ; compte Wayback vide | Copie originale |
| Post d'@Aristos_Revenge du 21/07 20:56 UTC | Texte connu par le seul Daily Dot | Supprimé, absent de la Wayback | Capture d'époque |
| Réponses, citations et portée complètes | Partielles | Les points d'accès publics ne listent pas les réponses | API X |
| Historique complet des avatars des comptes | Non établi | X ne le fournit pas | Captures datées |
| Post original de @ai_9684xtpa | Trouvé, id `1815243177475121253` ; d'autres versions citées par la presse non retrouvées | Pas de recherche native | API X |
| Source sociale du wallet `9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq` | **Retrouvée :** fils de tiers d'août 2024, et @XHEILIGX le 30/03/2024, indice C | Il manque une revendication, une signature, ou la réception de $PEZI à vérifier sur la chaîne | `audits/2026-11-03/work_E/X_FOLLOWUP.md`, partie 6 |

## Audits
Audit du 03/11 (A données, B statistiques, C attribution, D confrontation) : **NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent**, voir `audits/2026-11-03/`.

Trois auditeurs à l'aveugle de la méthode (fuites, statistiques, protocole) n'ont pas été lancés. `etude_final/audit/` n'existe pas. L'amendement 001 a été décidé par l'agent, pas par Benjamin : voir l'amendement 002.

## Le DM à Musk
Le DM revendiqué par @DarkMagaCoin n'est **ni prouvé ni réfuté**. Un DM n'est pas observable sans la capture ou le compte. Le Daily Dot note que le compte n'a pas répondu à la demande de preuve. Le fichier d'origine du visuel n'est pas disponible : seule une capture de l'app Photos, dont la date est modifiable, a été publiée (`IMG_5658`, fuseau inconnu).

## On-chain
| Élément | État | Cause |
|---|---|---|
| API Wallet Helius (`identity`, `funded-by`) | HTTP 403 sur les clés disponibles | Plan ; remplacé par `getTransfersByAddress` et les étiquettes Dune |
| Étiquettes Solscan et Solana.fm | Inaccessibles | Solana.fm répond 502, l'API publique Solscan 404 ; liste Dune Spellbook utilisée (117 adresses), archivée avec son empreinte dans `evidence/labels/` |
| Identité des services non étiquetés | Partielle | `3LoAYHuS…`, `HFqp6ErW…`, `GP8StUXN…`, `3CgvbiM3…`, `7iWnBRRh…` sont publiés par Jupiter (`evidence/labels/`). `FERjPVNE…`, `3eGdjMdQ…` et de nombreux hubs restent non nommés : on mesure leur comportement, pas leur marque |
| Titulaire d'un compte d'échange | **Hors de portée sans réquisition** | Un dépôt sur un hot wallet ne dit pas qui détient le compte. Aucune continuité n'est créée à travers lui, sauf un indice ponctuel : un montant apparié à l'écart exact près (`docs/CASE_REPORT.md`, N04) |
| Venues sans historique, programmes AMM hors liste | Non collectés, K10 | 6 adresses de `venues.json` sans dossier `full_venue`, quelques dizaines de transactions (A-11). Demande du réseau |
| Requêtes de flux tronquées | Partielles sur les wallets très actifs | Plafonds de pages. Chaque fichier de `raw/flows` indique `truncated`, et `exit_flows.parquet` et `funding_edges.parquet` le portent ligne par ligne |
| Transferts SPL sans référence au mint sur les wallets non tracés | Non vus | Seuls les wallets tracés (`getTransfersByAddress`) les révèlent. Leur réalisé peut donc être surévalué, signalé par la colonne de complétude |

## Enquête secondaire : Wifejak et prototype politique : DÉSACTIVÉE
Le thread d'@Aristos_Revenge ne nomme aucun contrat. Plusieurs candidats portent le nom (`4y3oUrsJfSp431R3wJrWiaLxRPsnYtpkVJmoV2bYpBiy`, `8AciyqMog6ERxrvu2H8o36CLbzfD6g6pjH3ZKrBrcPAK`, des clones Pump.fun, un site sur Ethereum), mais rien de lu ne les relie au thread. Comparer leurs acheteurs à ceux de DMAGA reviendrait à chercher un lien sur un contrat choisi au hasard. Le wallet créateur de DMAGA n'a créé aucun autre token Pump.fun sur ses 972 transactions. Pour activer cette branche, il faudrait un nom ou un contrat venant d'une source.

## Récit de Benjamin du 02/08/2026
Des échanges avec des traders « de Bali à Los Angeles », une équipe derrière DMAGA et Kekius, une adresse deBridge récurrente : aucun fichier trouvé sur ce Mac ne le documente. Ces éléments restent des hypothèses. L'ancienne analyse des gros gagnants n'a pas été retrouvée non plus (`docs/PRIOR_WORK.md`).

## Ce qui établirait une connaissance préalable
1. La conversation d'origine : capture ou export du DM, avec date, expéditeur et destinataire.
2. Le fichier d'origine du visuel avec ses métadonnées intactes.
3. Une communication datée entre un wallet identifié et un compte proche de Musk avant 19:03 UTC le 21/07.
4. Une attribution vérifiable d'un wallet acheteur à un compte du noyau : adresse revendiquée, signature de message, ou réquisition à un échange.

Sans l'un de ces quatre éléments, les données on-chain seules ne peuvent pas démontrer une connaissance préalable.
