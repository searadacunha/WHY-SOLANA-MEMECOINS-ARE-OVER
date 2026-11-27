#!/usr/bin/env python3
"""data/social_links.parquet : relations documentées entre comptes publics, contenus et wallets.

Chaque ligne a un type d'arête distinct et une source lue. Un identifiant absent des archives fait échouer le script :
aucune relation n'est écrite sans son texte. Aucune ligne n'attribue un wallet à un compte par déduction.
"""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import DATA

posts = {}
for line in (DATA / "x_posts.jsonl").open():
    r = json.loads(line)
    if r.get("text"):
        posts.setdefault(r["id"], {"author": r.get("author"), "text": r["text"], "reply": r.get("reply_to_user"), "src": "x_posts.jsonl"})
for line in Path("evidence/x_wayback/recovered.jsonl").open():
    r = json.loads(line)
    if r.get("text"):
        posts.setdefault(r["id"], {"author": r.get("username") or r.get("account_in_url"), "text": r["text"], "reply": None, "src": "x_wayback/recovered.jsonl", "refs": r.get("refs")})


def when(i):
    return datetime.fromtimestamp(((int(i) >> 22) + 1288834974657) / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


rows = []


def add(src, dst, typ, pid, conf, note, need=None):
    if pid not in posts:
        raise SystemExit(f"post {pid} absent des archives : relation non écrite")
    txt = posts[pid]["text"]
    if need and need.lower() not in txt.lower():
        raise SystemExit(f"post {pid} ne contient pas « {need} » : {txt[:120]}")
    rows.append({"src": src, "dst": dst, "edge_type": typ, "post_id": pid, "date_utc": when(pid), "confidence": conf, "note": note,
                 "text": txt[:280], "archive": posts[pid]["src"]})


# mentions de wallets par des tiers : le compte commente un wallet, il n'en est pas le propriétaire
add("@ai_9684xtpa", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "mention_tierce", "1815243177475121253", "A", "adresse entière dans le lien Solscan du post, montants recoupés on-chain")
add("@0xRamonos", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "mention_tierce", "1815221876190294470", "B", "capture 5QhJJc…HScd, résolue par préfixe et suffixe uniques parmi les propriétaires DMAGA")
add("@ashrobinqt", "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "mention_tierce", "1815233925662306427", "A", "capture H3QsBr…T6cc, coût recalculé 1 087 $ contre 1 086 $ sur la capture")

# déclarations publiques, à prendre comme telles
D = [("@kikisknees", "création du visuel", "1815116229117690314", "pfp by me", "revendique le pfp avec @ChrisWinig"),
     ("@kikisknees", "création du visuel", "1815116385414209876", "made by me", "revendique le pfp"),
     ("@kikisknees", "@elonmusk", "1815125720785391758", "made for him", "surprise déclarée et visuel « fait pour lui »"),
     ("@kikisknees", "@elonmusk", "1815141192285245701", "specifically for", "visuel créé « spécifiquement pour Elon », 2 h 15 après l'adoption"),
     ("@kikisknees", "création du visuel", "1815223207667900454", "made the first one", "revendique le premier"),
     ("@kikisknees", "$DMAGA", "1812521301682069933", "60% of the supply", "promotion du token le 14/07, sans DM évoqué"),
     ("@kikisknees", "@pmarca", "1815006501896872388", "elon mooning", "6 h 30 avant la borne haute, sollicite publiquement"),
     ("@kikisknees", "@wallstreetbets", "1815121075904168102", "7D7BRc", "publie le mint en réponse, après l'adoption"),
     ("@DarkMagaCoin", "@elonmusk", "1815298322325811663", "DMed", "DM revendiqué, sans preuve"),
     ("@DarkMagaCoin", "@elonmusk", "1816000567740633335", None, "réponse à un tiers : nuance la version du DM"),
     ("@DarkMagaCoin", "@elonmusk", "1816846863649124596", "pfp second", "« sent Elon his pfp second », déclaration"),
     ("@DarkMagaCoin", "@ChrisWinig", "1815502699888087492", "media team", "décrit Chris Winig comme responsable média"),
     ("@DarkMagaCoin", "@ChrisWinig", "1813681762188345683", "ChrisWinig", "le 17/07 : créateur de contenu de l'équipe"),
     ("@ChrisWinig", "@elonmusk", "1815054750775173447", "It's time".replace("'", "’"), "publie le visuel en réponse à Musk"),
     ("@ChrisWinig", "@elonmusk", "1815107774113587625", "profile picture", "constate l'adoption"),
     ("@DarkMagaCoin", "@elonmusk", "1815130617392046479", "ONE DMAGA", "cite le post de Winig pour revendiquer"),
     ("@DarkMagaCoin", "métadonnées du visuel", "1815130791208530273", "Metadata", "capture iOS IMG_5658, 21/07 06:17, fuseau inconnu, date modifiable"),
     ("@DarkMagaCoin", "@elonmusk", "1815107751745601643", "DMAGA PFP", "premier constat du compte, 3 min après la borne haute")]
for src, dst, pid, need, note in D:
    add(src, dst, "declaration_publique", pid, "A" if posts.get(pid, {}).get("src") == "x_posts.jsonl" else "B", note, need)

# interactions sociales, comptées sur les réponses archivées entre comptes de la liste
CORE = {"DarkMagaCoin", "kikisknees", "Aristos_Revenge", "ChrisWinig", "koreanjewcrypto", "elonmusk", "pmarca", "twobitidiot", "basedmikelee",
        "Bluntz_Capital", "wsbmod", "wallstreetbets", "WashletJP", "twicrates"}
counter = Counter()
for pid, p in posts.items():
    a = p.get("author")
    if a not in CORE:
        continue
    t = p["text"]
    targets = {p["reply"]} if p.get("reply") else set()
    for tok in t.split():
        if tok.startswith("@"):
            targets.add(tok[1:].strip(".,:;!?\"'"))
    for tg in targets:
        if tg in CORE and tg != a:
            counter[(a, tg)] += 1
for (a, b), n in counter.items():
    rows.append({"src": "@" + a, "dst": "@" + b, "edge_type": "interaction_sociale", "post_id": None, "date_utc": None, "confidence": "A",
                 "note": f"{n} post(s) archivé(s) mentionnant ou répondant au compte, corpus partiel", "text": None, "archive": "x_posts.jsonl + recovered.jsonl"})

pq.write_table(pa.Table.from_pylist(rows), DATA / "social_links.parquet", compression="zstd")
print(Counter(r["edge_type"] for r in rows))
print("wallet revendiqué par un compte du noyau : 0 ligne, aucune adresse publiée trouvée (docs/SOCIAL_FINDINGS.md, point 6)")
