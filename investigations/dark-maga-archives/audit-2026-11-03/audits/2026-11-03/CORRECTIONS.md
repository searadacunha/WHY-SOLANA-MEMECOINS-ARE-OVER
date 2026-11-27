# Corrections proposées après audit final

Auditeur D, 03/11/2026, commit `01ae5a4`. **Rien n'est appliqué par moi.** Les scripts cités sont dans `audits/2026-11-03/work_D/`. Gravité : MAJEURE si une conclusion ou sa lecture change, MOYENNE si un chiffre publié change, MINEURE sinon. Ordre conseillé : partie B, relance du dérivé, partie A, nouvel audit des conclusions.

## A. À corriger dans le rapport

Fichiers : `docs/CASE_REPORT.md` par son générateur `scripts/rep_90_case.py`, `reports/ATTRIBUTION.md`, `reports/COORDINATION.md`, `reports/TOP_TRADERS.md`, `reports/EARLY_BUYERS.md` par `scripts/rep_70_reports.py`, `rep_72_links.py`.

| Id | Erreur | Preuve | Gravité | Impact | Correctif |
|---|---|---|---|---|---|
| R01 | Le test gelé est présenté comme appui contre une connaissance préalable (Essentiel 3, ligne H2, C39) | `d11_power.txt` : 2,4 % sans effet, 3,3 % à 2 R, 7,5 % fort | MAJEURE | H2 : le test ne départage pas | Garder le texte gelé entre guillemets, ajouter le texte de `AUDIT_FINAL.md` section 4.3. Retirer « Test gelé non significatif » des appuis de H2 |
| R02 | « Contrôles positifs » sans portée | `d11_power.txt`, `synth.md` | MAJEURE | C49 | Écrire « contrôle de la plomberie seulement », citer 3,3 et 7,5 %, nul réel 2,4 % |
| R03 | Copie neuve affirmée, sans trace | Recherche dans le dépôt, journal seul | MOYENNE | C49 | Retirer la phrase, ou joindre le journal d'exécution ; citer la reproduction par A, B et D |
| R04 | Limite de puissance incomplète, C47 | `d11_power.txt`, B-04, B-15 | MOYENNE | Lecture du test | « Le verdict ne bascule que si DMAGA dépasse tous les pairs sur au moins une mesure. M3 et M4 ne peuvent pas ouvrir. Niveau réel 2,4 % » |
| R05 | « Autour du créateur » | `d43_perim.txt` : 0 arête, 0 tx commune ; `d44_misc.txt` : 2 composantes SOL | MAJEURE | Essentiel 4 | Retirer l'expression. Deux périmètres : le groupe de 33 relié par transferts, le périmètre créateur relié par la série et le dépôt |
| R06 | Série Coinbase absente, « un hot wallet coupe la trace » | `d20_series.txt`, `d24_pure.txt` : 13 sur 2 201 en 507 s, témoin au plus 3 contre 10 | MAJEURE | Q1, Q6, C19 | Ajouter N01. Scinder : B pour le même opérateur ou compte sur le créateur et 12 wallets, C pour les 33 et pour un même bénéficiaire |
| R07 | 9W9b « non tranché », argument « 48 expéditeurs seulement » | `d21_match.txt`, `d49_small.txt`, `d43_perim.txt` | MAJEURE | Essentiel 5, Q12, C18 | Compte de dépôt Coinbase niveau B. 31 sur 48 contre 8 sur 1 365. 94,5 % est un plancher, 100 % avec les 6 adresses. Ne pas écrire que la rafale de 9 est unique (`d22_burst.txt`) |
| R08 | `BuHUkjUy` « non interprété » | `d21_match.txt` | MAJEURE | Essentiel 5 | N04, niveau B pour le lien de 2025, sans valeur pour le lancement |
| R09 | 2,4 % et « moins vendeur » | `d43_perim.txt` | MAJEURE | H3, C15, C41 | « Au moins 2,4 %, 2,9 % avec 3 destinataires. Swaps plus transferts : 37,3 % contre 40,8 à 43,7 %, exploratoire » |
| R10 | « Surtout d'échanges » | `d45_funding.txt` | MAJEURE | Q6, C50 | Publier 42,5 ; 22,1 ; 20,5 ; 14,8 %, fenêtre 14/07/2023 au mint, et 189, 189, 109, 4 pour le premier financeur. Dire que la part d'échange est une borne basse |
| R11 | Bots affichés comme acheteurs | `d41_roundtrip.txt` | MAJEURE | Q4, Q5, C05 | Donner 100,78 SOL nets à côté de 145,44. Publier la part d'allers-retours par fenêtre. Sortir les 3 premiers rangs des classements, voir C03 |
| R12 | Mouvements hors brut non cités | `d42_chain.txt` | MAJEURE | Lecture de Données | Ajouter N12 : 27 196 ruptures, 2 845 M, rien avant Musk sauf 84,7 M déjà compensés |
| R13 | C35 | `d40_trades.txt`, `d46_claims.txt` | MOYENNE | Q5 | 09:01:46 ; 18 309 sur 53 893 ; donner 9 885 à plus de 0,1 SOL |
| R14 | C34 | `d46_claims.txt` : 107 des 183 | MOYENNE | Q4 | « Cohortes de premier achat », deux tableaux séparés dans `EARLY_BUYERS.md` |
| R15 | Colonnes « Acheté » lues comme d'avant Musk (C-09) | C-09 repris de C | MINEURE | Lecture | Renommer les colonnes de `COORDINATION.md` |
| R16 | Niveau B des 29 wallets (C-06) | C-06 repris de C ; `d46_claims.txt` pour 166,111 M | MINEURE | C12 | Fourchette 16,0 à 17,7 % |
| R17 | Habp5bnc sort par une règle de poussière (C-07) | C-07 repris de C | MINEURE | C10 | Le dire. 34 wallets et 41 arêtes avec la règle écrite, 217,04 M inchangé |
| R18 | C36 | `d46_claims.txt` | MINEURE | Q6 | G41vRrsH 11 sur 33 ; groupe 11 à 12 sur 33 |
| R19 | « 118 échouées » | `work_A/out/a01_sigs.log`, 83,03 et 90,18 % | MINEURE | Lecture de Données | Écrire les deux taux, A-07 |
| R20 | « 402 SOL » selon le plan seulement | `d40_trades.txt`, 507,93 au vault | MINEURE | Lecture | Ajouter « 508 SOL au vault », A-06 |
| R21 | Limite de l'ordre de vente (C-10) | `d46_claims.txt`, C-10 | MINEURE | Essentiel 5 | Dire que 4 500 USDC rachètent 7 397 559 jetons le 13/07, le créateur déplace sa position. Retirer « non vérifié » pour `Hx1UvdgM` |
| R22 | Sorties d'échanges sans dénominateur | `d48_exits.txt` : 175 427 SOL éq. | MOYENNE | Q7 | Publier ce chiffre et les 14 wallets tronqués sur 65 |
| R23 | 53 889 et 53 893 | `TOP_TRADERS.md`, `CASE_REPORT.md` | MINEURE | Aucun | Préciser les populations de 71 682 et 71 706 wallets |
| R24 | Angles morts limités au détenteur | `d44_misc.txt`, `d46_claims.txt` | MOYENNE | Limites | Ajouter N17 : 90,05 M hors de M6 à S, 76,3 M de transferts nets, achats de l'heure S hors mesures |
| R25 | Biais d'échecs « touche tous les tokens » (A-08) | A-08 repris de A | MINEURE | C48 | Ajouter les deux lignes de A |
| R26 | Comparaisons d'audit hors registre | B-20 : 121 ; `d11`, `d23`, `d30` : ce rapport | MINEURE | Comptage | Écrire que ces comparaisons sont exploratoires, sans les mettre au registre gelé |

**À ne pas reprendre des audits :**
- A-03 : « 22 % ... 68 % » et le titre « 12 mois avant le mint ». 55,9 % de ce SOL est postérieur au mint.
- B-06 et section 5.4 de B : « 845,72 M jetons » comme stock invisible. Stock à S : 90,05 M.
- C-03 : « B pour même bénéficiaire », « Dépôt partagé écarté » sur la seule rafale, et « 9 contre 3 au plus » sans le filtre.
- C-01 : 0,55 % comme taux de comparaison du retour à 9W9b. Ce taux porte sur DMAGA. Le témoin direct est dans `d24_pure.txt`.

## B. À corriger dans le code dérivé, hors gel

| Id | Erreur | Preuve | Gravité | Impact | Correctif |
|---|---|---|---|---|---|
| K01 | Lignes doublées dans `trades.parquet` | `d40_trades.txt` : 5 903, 4 966 du 24/07, 937 en venues | MOYENNE | PnL, C23, C35, groupe, top 100 | `dmaga/db.py`, `scripts/ana_19_export.py` : dédoublonner par (signature, kind, owner, venue, token_delta). Couper la tranche `full_pool/t1721777789` à minuit à la normalisation, sans toucher le brut. Relancer `scripts/run_derive.sh` puis la suite de `state/STATE.md` |
| K02 | Pas d'assertion contre les doublons | K01 | MOYENNE | Récidive | `scripts/chk_90_selfcheck.py` : échec si une ligne apparaît deux fois |
| K03 | `GpMZbSM2` compté comme réserve de tous ses pools | `d40_trades.txt` : 1 434 tx et 1 136 lignes | MOYENNE | PnL de wallets isolés, 0,19 % du volume selon A | `dmaga/normalize.py`, `_is_venue_account` : même exclusion que `RAYDIUM_AUTH`, puis `nrm_10_trades.py --force`. Mes valeurs « avec A-02 » sont à remplacer |
| K04 | Résiduels sur flux | `d46_claims.txt` : 7gEQ6syD 122,28 M pour 0, somme 937,1 M | MOYENNE | `TOP_TRADERS.md` | `scripts/ana_20_pnl.py` : résiduel lu sur les soldes de comptes, `completeness` = partiel dès qu'un compte a une rupture |
| K05 | `dmaga_all` tronqué pour 20 wallets | A-05, A-15 | MINEURE | Réalisés tardifs | Lever le plafond si le budget le permet, sinon le publier |
| K06 | Pas d'étiquette pour les allers-retours | `d41_roundtrip.txt` : 103 wallets, 106 048 SOL | MOYENNE | Classements | Étiquette `bot_aller_retour` : non signataire à programme propre, ou plus de 50 % d'allers-retours sous 10 s. Identifier `3GMsedVP` avant toute conclusion (A-16) |
| K07 | `uiAmount` à 0 décimale | `d48_exits.txt` : 5 001 lignes au-dessus de 100 000 SOL, 3 wallets, sans effet sur C37 ; `d45_funding.txt` | MINEURE | Sommes non filtrées | `scripts/ana_30_flows.py` : `amount / 10**9` |
| K08 | Dédoublonnage de `funding_edges` | `d45_funding.txt` : 214 paires en double entre `first_in` et `in_before` | MINEURE | Sommes | Une ligne par (wallet, signature, src) |
| K09 | Contrôles de chaîne partiels | A-14 | MINEURE | Aucun aujourd'hui | Retirer le `LIMIT` de `chk_20_vault_chain.py` ; côté WSOL dans `chk_21_venue_chain.py` |
| K10 | Venues absentes et programmes AMM | A-11 | MINEURE | Quelques dizaines de tx | Relancer `col_03` sur 6 adresses, compléter `AMM`, seulement si le budget le permet |
| K11 | Classes d'étiquettes | A-13 | MINEURE | Lecture | `dmaga/labels.py`, `ana_22_nodes.py` : classe `service`, filtrer les mints du fichier Jupiter |
| K12 | Famille Coinbase non étiquetée | `d21_match.txt`, `d49_small.txt` | MOYENNE | Q6, Q7, liens | Liste séparée `hot_presume` pour `FpwQQhQQ`, `D89hHJT5`, `DPqsobys`, `9obNtb5G`, `4NyK1AdJ`, `8JUEoHNM`, `5g7yNHyG`, jamais présentée comme étiquette vérifiée |

`etude_final/`, `dmaga/collect.py`, `dmaga/helius.py`, `dmaga/config.py`, `scripts/col_40_controls.py` ne sont pas concernés : gel à respecter. Les parseurs gelés de B-13 restent tels quels.

## C. Ce qui demanderait un amendement décidé par Benjamin

| Id | Point | Preuve | Gravité | Impact | Correctif proposé |
|---|---|---|---|---|---|
| P01 | Décision sur l'amendement 001, laissée ouverte par 002 | `d30_amend.txt` | MOYENNE | R1, R2, aucun effet sur le verdict | Conserver, voir `AUDIT_FINAL.md` section 6 |
| P02 | Texte « ordre d'activité, sans lien avec les mesures » | Spearman 0,9995 | MINEURE | Description | Rectificatif daté, `work_D/projet_amendement_003.md` |
| P03 | R1 et R2 présentés comme robustesse | R2 : 29 sur 287, tous de juin | MOYENNE | Lecture de la bande large | Requalifier en variantes partielles, même projet |
| P04 | Compteur `tronque_sans_S20` absent | `d30_amend.txt` : 5, tous `reporte_budget` | MINEURE | Aucun | Publier, même projet |
| P05 | `selection.jsonl` hors verrou | B-14, C-11 | MINEURE | Reproductibilité de 731 capitalisations | Annexe datée d'empreinte, sans valeur rétroactive |
| P06 | « R3 le borne » | B-11 | MINEURE | Lecture | Limite ajoutée, plan inchangé |
| P07 | Interprétation à côté du verdict dans `results.md` | `d11_power.txt` | MOYENNE | Lecture | Section datée, verdict inchangé |

Hors de cet amendement, et seulement pour une prochaine étude : seuil de puissance sur vraies données à la place de `k < 139`, mesures sans plafond qui bloque l'ouverture, marge d'équivalence fixée d'avance, réponses de `getTransfersByAddress` et de `fdv_at` archivées, tirage au hasard par tranche des comparateurs de variantes.

**Interdit :** changer le verdict, les mesures, les seuils, retirer un comparateur, promouvoir un test exploratoire.
