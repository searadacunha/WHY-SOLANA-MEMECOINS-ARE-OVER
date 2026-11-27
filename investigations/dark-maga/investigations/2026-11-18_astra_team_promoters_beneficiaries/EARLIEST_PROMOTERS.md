# EARLIEST_PROMOTERS — premiers promoteurs publics de $DMAGA (X)

Le mint a lieu le 2024-07-14 à **02:05:25 UTC**. Pour chaque compte, seule la première publication qui se rapporte au token compte (ticker, CA ou image $DMAGA).

**Couverture de la collecte**
- Recherche X API v2 `search_posts_all` sur DMAGA, du 02:05:25 au 02:50:30. Elle est **complète** : la page 2 est vide.
- Timelines ciblées :
  - Murray : nuit complète, 25 posts ;
  - Esoviz et kiki : 0 résultat sur la fenêtre de lancement.
- Archives Wayback du dépôt (DMC, kiki).
- Toutes les heures sont recalculées depuis le snowflake. Données : `data/earliest_promoters.csv` et `data/x_ids.csv`.

## Classement (10 premiers comptes distincts, + 2 de contexte)

| # | Compte | UTC | Type | Contenu | Preuve | Niveau (origine) |
|---|---|---|---|---|---|---|
| 1 | @DarkMagaCoin | 02:26:35 | post, supprimé depuis | « We are live Patriots! ca: 7D7B…pump » + lien Telegram | Wayback 20240714022635 ; texte recopié dans le RT archivé de kiki `1812317575411351639` | A (RO, snowflake VI) |
| 2 | @Murray_Gothbard (handle @ChristienPhoto à l'époque) | **02:31:29** | post | « What is happening?!?! Trump rises up. » + image de Trump aux yeux laser portant **« $DMAGA »** (média `3_1812313858226163712`, 02:31:09) | `evidence/x/ax03_*`, `evidence/media/murray_GSah2h0WkAAPiNc.jpg` | **A (VI, NOUVEAU)** |
| 3 | @adamjia7 | 02:33:53 | post de bot (« sent 30seconds ago in vip group ») | CA + fdv 97 451 $ | `evidence/x/ax01_*` | A (VI ; connu en passe 4) |
| 4 | @Official67Token | 02:44:08 | RT de Murray (02:41:55) | « He will rise, higher and stronger $DMAGA » | ax01 | A (VI) |
| 5 | @SpecialBea99061 | 02:45:49 / 02:45:54 | RT de Murray puis réponse « $DMAGA » | — | ax01 | A (VI) |
| 6 | @kikisknees | 02:45:55 | RT du post DMC « We are live » | CA | Wayback (`evidence/x_wayback/recovered.jsonl` du dépôt) ; l'API répond Not Found | A (RO) |
| 7 | @BoredNap66757 | 02:46:00 | RT de Murray | — | ax01 | A (VI) |
| 8 | @Jacwin_n | 02:46:16 | RT de Murray | — | ax01 | A (VI) |
| 9 | @eseleo | 02:46:33 | réponse à DMC | « $DMAGA💯 » | ax01 | A (VI) |
| 10 | @CryptoOnlyCoims | 02:48:08 | réponse à DMC + vidéo | « $DMAGA Time. Libtards on notice. » | ax01/ax02 | A (VI) |
| (11) | @Fudrap96 (créé le 2024-06-17) | 02:49:46 / 02:50:16 | RT de Murray + « We are $DMAGA » | — | ax01 | A (VI) |
| (12) | @DarkMagaCoin | 03:00:28 | vidéo | « Dark MAGA patriots in control. $DMAGA » | ax02 | A (VI) |

Pour situer la diffusion de Murray : 5 des 10 premiers relais (n° 4, 5, 7, 8, 11) sont des RT de son post de 02:41:55. Le CA lui-même circule d'abord via DMC, kiki et le bot adamjia7.

## Faits de contexte (activité avant le mint, pas des promotions du token)

| Heure | Fait | Lien avec le token |
|---|---|---|
| 00:18:44 | Murray RT un post qui contient le CA de **$KLLARY** (`AUS4wt…pump`) | aucun |
| 00:41:12 | kiki RT @CryptoOnlyCoims « Dark MAGA Has Begun » | slogan, pas de ticker ni de CA |
| 02:03:54 | Murray RT @KILLARYonSOL | aucun |
| 02:04:25 | Murray répond à @KILLARYonSOL « They almost got him! » | aucun |

Sur ce contexte :
- La phrase « Dark MAGA Has Begun » prouve que le **slogan** précède le token. Elle ne prouve pas que le token était connu de son auteur.
- @KILLARYonSOL a été créé le 2024-06-12, un jour après DMC ; le token KLLARY a été créé le 2024-06-26. Ce **voisinage thématique** est indicatif (D), sans lien prouvé.

**Faux positif écarté :** @Stopaso375689 à 02:20:05 (« the dead dmaga ») parle d'autre chose que du token.

## Résultats négatifs

- Aucun post DMAGA de @kikisknees, @Esoviz ni @ChrisWinig dans la fenêtre 02:05–02:50 via l'API.
- @Aristos_Revenge est protégé : impossible de vérifier.
- Aucun post indexé avec le ticker ou le CA avant 02:20 : la recherche `DMAGA OR <CA>` du 2024-07-13 00:00 au 2024-07-14 02:20 donne **0 résultat sur 2 pages** (`evidence/x/ax08_*`). Le premier post indexé est @Stopaso375689 à 02:20:05, hors sujet. Limite : les posts supprimés ne sont pas indexés ; le post DMC de 02:26:35 n'est d'ailleurs connu que par Wayback.
- La recherche est plafonnée à 25 résultats par appel. La seconde page vide confirme qu'elle a été épuisée.
