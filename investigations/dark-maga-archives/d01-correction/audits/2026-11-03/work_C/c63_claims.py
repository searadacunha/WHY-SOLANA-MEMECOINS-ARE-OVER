#!/usr/bin/env python3
"""Ecrit claims_C.csv : verdict de chaque assertion dont l'auditeur principal est C. Controle que la liste est complete."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
A = {r["id"] for r in csv.DictReader(open(ROOT.parent / "CLAIMS_INPUT.csv")) if r["auditeur_principal"] == "C"}
V = [
    ("C03", "PASS", "créé 2024-06-11T16:25:03Z ; thread : started @DarkMagaCoin, two days later Butler ; aucun mint ni date de mint", "evidence/web/profiles/fx_DarkMagaCoin.json ; evidence/web/threadreader_1843704335823454430.txt lignes 55-57 ; c54.out"),
    ("C04", "PASS", "19:03:27 ancienne image 1780044485541699584 ; 20:59:25 nouvelle 1815105297410666496 ; snowflake 19:23:20 ; Bailey 19:30:13", "evidence/web/wb_elonmusk/ ; c54.out"),
    ("C10", "PASS", "33 wallets, 40 transferts rejoués, 40 sur 40 identiques (source, destination, montant), source signataire, aucun programme d'échange ; ma règle donne 34 et 41 si Habp5bnc n'est pas exclu", "edges40_replay.csv ; c42.out ; c45.out ; constat C-07"),
    ("C11", "PASS", "217,0365 M par post-soldes ; 938,00 M = 1 000 M moins 62,00 M Raydium ; 23,14 %", "members_table.csv ; accounting_Tlow.csv ; c46_market.out ; c58.out"),
    ("C12", "PASS", "29 wallets, 166,111 M, 17,71 % ; niveau B moyen, 149,7 M et 15,96 % sans 7mdCAs et 9u5JKg", "c41_view.out ; member_evidence.csv ; constat C-06"),
    ("C13", "PASS", "4 wallets (Ei5yGz8d, HGBiExZR, Gcyg2jeL, 4wComYHQ), 50,926 M ; un seul lien 4wComYHQ vers 74qFhHyp 15 M ; aucun lien SOL avec le reste", "c41_view.out ; c44.out"),
    ("C14", "PASS", "15 sur 33 ; 206,872 M ; 52,5 SOL frais compris contre 52,3", "c41_view.out"),
    ("C15", "PASS", "groupe 48,80 M, 4 408,7 SOL plus 18 935 USDC, soit environ 4 515 SOL ; marché 190 551 lu dans trades.parquet, Raydium brut sens vente 187 715 SOL ; 2,37 à 2,41 %. Plancher : 2,9 % avec les 973 SOL vendus par 3 destinataires", "c41_view.out ; c46_market.out ; c57.out ; c50.out ; constat C-05"),
    ("C16", "PASS", "0,032 SOL, 35 s, ordre DCA sur 7 105 960,2649 jetons ; solde du créateur avant 0,001288 SOL", "Nfzx313Vrs, 2BUp8LXmhu ; c15_bal.py ; c14_tx.py"),
    ("C17", "PASS", "16:11:24 à 16:14:34, 190 s ; en réalité 15 wallets en 2 rafales", "chrono_9W9b3z.csv ; bursts_9W9b.csv ; c47.out"),
    ("C18", "PASS", "48 expéditeurs à 0,001 SOL ou plus, 94,456 % vers les 3 hot wallets étiquetés ; les 5,5 % restants vont vers des hot wallets de la même famille", "c07_9w9b.py ; c56.out ; constat C-03"),
    ("C19", "FAIL", "A vrai, B mérité, C sous-évalué : 13 des 15 retraits Coinbase d'avant le mint reviennent au même dépôt, B proposé pour le créateur et cette série, C maintenu pour les 33", "cb_series.csv ; c52.out ; constats C-01, C-02, C-04"),
    ("C20", "PASS", "aucun virement de SOL ni transfert propre de DMAGA, toutes tailles, entre les 3 et le périmètre de 81 wallets ; 9PrmF8 sort vers le dépôt H9Xezqfd, distinct de 9W9b ; historiques H3QsBr et 9PrmF8 plafonnés à 1 200 tx, période DMAGA couverte", "c47.out ; c58.out ; c62.out ; c59.out"),
    ("C22", "PASS", "seules adresses publiées par le noyau : mint et pool ; corpus partiel", "c54.out"),
    ("C28", "PASS", "33 min 02 s, 0,5 SOL de Coinbase 3, 7,106 M pour 0,2012 SOL, première sortie le 06/07/2025", "chrono_8YLEuU.csv ; seed_token_summary.csv"),
    ("C30", "PASS", "13 virements 01:46:23 à 02:03:38 ; 7 sans aucun achat ; 2 wallets à 65 min 44 s et 65 min 17 s", "g41v_recipients.csv ; c58.out ; c44.out"),
    ("C31", "PASS", "pHash recalculé par mon code : distance 0 Winig contre avatar, 18 contre l'ancienne photo ; plus ancienne image proche dans le corpus", "c55_phash.py ; c55.out"),
    ("C32", "PASS", "texte « $DMAGA pfp by me and @ChrisWinig » 20:06:46 ; réponse 16:00:08 sans média lisible ; post IMG_5658 id 1815130791208530273", "evidence/x_wayback/recovered.jsonl ; c54.out"),
    ("C33", "PASS", "@koreanjewcrypto 15/07 16:45:07 ; @kanpai 16/07 00:14:58 ; @DarkMagaCoin 14/07 03:00:28 ; @pmarca 2 posts sans DMAGA", "data/x_posts.jsonl ; c54.out"),
    ("C36", "PASS", "11 sur 33 dans le groupe, 11 sur 33 G41vRrsH : le wallet non tracé CZsBW8yC est financé par G41vRrsH", "members_table.csv ; c50.out ; constat C-08"),
    ("C37", "INCONCLUSIVE", "seul le chemin 9PrmF8, 2 025,5 SOL vers H9Xezqfd, puis 3 hot wallets Coinbase, est recalculé ; montants par échange non recalculés", "c59.out ; c62.out"),
    ("C38", "PASS", "grappe de 345 wallets ; ma composante toutes dates 104 à 123 wallets, 6 à 10 M ; elle contient le compte de mise en commun C7qEaB6a", "c50.out ; sens_threshold.csv ; constat C-14"),
    ("C39", "INCONCLUSIVE", "jugement d'interprétation, non calculable ; le second membre tient (C22)", "lecture de CASE_REPORT"),
    ("C40", "PASS", "0 swap sur les 33 de 16:02:29 à 19:30:13 ; sur 79 wallets élargis, un achat de 0,011 M par B252jsFK à 19:26:13", "members_table.csv ; c58.out"),
    ("C41", "PASS", "22,49 % contre 34,96 % sur les seuls swaps ; 37,3 % contre 41,8 % avec les transferts sortants ; autres détenteurs lus dans trades.parquet", "c41_view.out ; c46_market.out ; constat C-05"),
    ("C42", "PASS", "07:57:16 à 08:33:36 ; 14:22:00 à 14:25:44 ; 25,5 M", "edges40_replay.csv ; c42.out"),
]
assert {v[0] for v in V} == A, A ^ {v[0] for v in V}
w = csv.writer(open(ROOT / "claims_C.csv", "w", newline=""))
w.writerow(["id", "verdict", "valeur_recalculee", "preuve"])
for v in V:
    w.writerow(v)
print(len(V))
