#!/usr/bin/env python3
"""docs/TIMELINE.md : chronologie, chaque ligne vérifiée. Un post cité doit exister dans les archives et sa date vient de l'id.

La capitalisation à chaque instant est lue dans les soldes du pool Raydium (prix × 10^9 × SOLUSDT à la minute).
"""
import csv
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from dmaga.config import DATA, RAW
from dmaga.db import connect
from dmaga.frfmt import fr

con = connect(mem="700MB")
VD, VS ="5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
con.execute(f"""CREATE TEMP TABLE chain AS WITH d AS (SELECT slot, tx_index, block_time, post FROM vault WHERE vault='{VD}'),
    s AS (SELECT slot, tx_index, post FROM vault WHERE vault='{VS}')
    SELECT d.block_time t, d.slot, d.tx_index, (s.post/1e9)/(d.post/1e6) price, s.post/1e9 reserve FROM d JOIN s USING (slot, tx_index) WHERE d.post>0 ORDER BY 1""")
px = {}
for z in sorted((RAW / "solusd").glob("SOLUSDT-1m-*.zip")):
    if z.name.startswith("._"):
        continue
    with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                ms = int(row[0])
                px[(ms // 1000 if ms > 10**14 else ms) // 60000] = float(row[4])


def fdv(t):
    r = con.execute(f"SELECT price, reserve FROM chain WHERE t<={t} ORDER BY t DESC, slot DESC, tx_index DESC LIMIT 1").fetchone()
    if not r or t // 60 not in px:
        return ""
    v = r[0] * 1e9 * px[t // 60]
    return f"{v / 1e6:,.2f} M$" if v >= 1e6 else f"{v / 1e3:,.0f} k$"


posts = {}
for src_ in (DATA / "x_posts.jsonl", Path("audits/2026-11-03/work_E/x_posts_new.jsonl")):
    for line in src_.open():
        r = json.loads(line)
        if not posts.get(r["id"], {}).get("text"):  # le corpus ancien garde des lignes sans texte, la ligne récupérée les remplace
            posts[r["id"]] = r
rec = {}
for line in Path("evidence/x_wayback/recovered.jsonl").open():
    r = json.loads(line)
    rec.setdefault(r["id"], r)


def snow(i):
    return int(((int(i) >> 22) + 1288834974657) / 1000)


def P(i, label, level, note=""):
    """Ligne appuyée sur un post archivé."""
    i = str(i)
    if i in posts and posts[i].get("text"):
        txt, src = posts[i]["text"], "supprimé, texte Wayback" if posts[i].get("status") == "unavailable" else "archivé"
    elif i in rec:
        txt, src = rec[i].get("text") or "", "supprimé, texte Wayback"
    else:
        raise SystemExit(f"post {i} introuvable dans les archives")
    t = snow(i)
    return (t, label, level, f"id {i}, {src}. {note} « {txt[:150].strip()} »".replace("\n", " "))


def T(t, label, level, source):
    return (t, label, level, source)


ath = con.execute("SELECT t, price*1e9 FROM chain ORDER BY price DESC LIMIT 1").fetchone()
sig_create = con.execute("SELECT signature FROM trades WHERE kind='swap' AND venue='pumpfun' ORDER BY slot, tx_index LIMIT 1").fetchone()[0]
sig_pool = con.execute("SELECT signature FROM trades WHERE kind='lp_add' AND venue='raydium' ORDER BY slot, tx_index LIMIT 1").fetchone()[0]

R = [
    T(1718123103, "Création du compte X @DarkMagaCoin", "A", "11/06/2024 16:25:03 UTC, evidence/web/profiles/fx_DarkMagaCoin.json"),
    T(1720908660, "Tentative d'assassinat de Donald Trump à Butler", "C", "13/07 22:11 UTC, connaissance générale et mission, non revérifiée dans un fichier"),
    T(1720920743, "Le futur créateur reçoit 0,5 SOL de Coinbase 3", "A", "premier mouvement du wallet ; étiquette Dune. Premier d'une série de 13 wallets en 507 s, voir `docs/CASE_REPORT.md`, N01"),
    T(1720922222, "Création de la chaîne Telegram @DMAGACoin", "B", "« Channel created » 01:57:02 UTC, evidence/web/tg_DMAGACoin.html"),
    T(1720922725, "Création du mint par 8YLEuUtZ…, achat de 7,1 M pour 0,2 SOL", "A", f"signature `{sig_create}`, slot 277417695. Environ 3 h 54 après Butler. Le thread d'@Aristos_Revenge ne date pas le mint : il écrit que @kikisknees a lancé @DarkMagaCoin et les pfp deux jours avant Butler"),
    T(1720923331, "Migration vers Raydium, 10 min après la création", "A", f"signature `{sig_pool}`"),
    T(snow(1812312706826854843), "Premier post de @DarkMagaCoin, avec le mint", "A", "id 1812312706826854843, lu sur la capture du repost 1812317575411351639"),
    T(1720927892, "dmaga.xyz en ligne, mint affiché", "A", "capture Wayback 03:31:32 UTC, evidence/web/wb_dmaga_xyz_*"),
    P(1812521301682069933, "@kikisknees promeut le token", "B"),
    P(1813004360592552354, "@kanpai annonce des avatars rouges aux yeux bleus", "A"),
    P(1813681762188345683, "@DarkMagaCoin présente @ChrisWinig comme créateur de l'équipe", "A"),
    P(1813310692243480937, "@FrancoAppr répond à Musk avec une image de Musk aux yeux laser, autre composition", "A", "Lien avec l'avatar : C."),
    P(1814063148917256375, "@kikisknees à Musk : « We are building an army for you for that purpose. $DMAGA »", "A", "Même image que le post du 16/07, pHash 0. Rien ne montre que Musk l'a vue."),
    P(1814763940410499481, "@pmarca publie une image rouge aux yeux laser, avec un lien vers une réponse de @kikisknees", "A", "Pas le visuel de Musk. L'id du corpus était celui d'un repost."),
    P(1814920352134537332, "@pmarca, nouvelle image", "A", "L'id du corpus était celui d'un repost."),
    P(1815006501896872388, "@kikisknees répond à @pmarca, plus ancienne image connue de la composition de Musk, sans drapeau", "A", "Contexte de plaisanterie sur la Lune."),
    P(1815018442589663572, "@kikisknees cite la capitalisation", "B", "À comparer à la colonne capitalisation."),
    P(1815053805077086351, "Musk écrit « Whoa » sur un article du NY Post", "A"),
    P(1815053713330876681, "@GreatBambin0 envoie à Musk la variante sans drapeau", "A", "Plus ancien envoi connu de cette composition à Musk."),
    P(1815054158367432804, "@kikisknees répond à Musk avec une image", "A", "Image retrouvée : le Trump « dark maga » de @DarkMagaCoin, pas le visuel de Musk."),
    P(1815054374982324401, "@FrancoAppr répond à Musk avec l'image identique à l'avatar", "A", "Plus ancienne image identique connue, pHash 0."),
    P(1815054750775173447, "@ChrisWinig publie le visuel en réponse à Musk", "A", "pHash 0, 90 s après @FrancoAppr."),
    P(1815096055337496944, "@kikisknees répond à Musk avec une image", "B", "Média perdu."),
    P(1815098229903839717, "@kikisknees répond à @PragmaticPrim8 et Musk avec une image", "B", "Média perdu."),
    T(1721583960, "Annonce du retrait de Joe Biden", "C", "17:46 UTC, donnée de la mission, non revérifiée dans un fichier"),
    T(1721588607, "Borne basse : Musk a encore son ancien avatar", "A", "capture Wayback 19:03:27 UTC, evidence/web/wb_elonmusk/"),
    T(1721589800, "Envoi probable du nouvel avatar", "B", "snowflake de profile_images/1815105297410666496 : 19:23:20,585 UTC. L'id date le téléversement ; lecture à confirmer"),
    P(1815107030606385507, "Borne haute : premier post qui montre le nouvel avatar", "A"),
    P(1815107751745601643, "@DarkMagaCoin réagit", "A"),
    P(1815107549903135205, "@ChrisWinig réagit", "A", "L'id du corpus était celui d'un repost."),
    P(1815116229117690314, "@kikisknees revendique le pfp", "B"),
    P(1815125720785391758, "@kikisknees : surprise et visuel « fait pour lui »", "B"),
    T(1721595380, "@Aristos_Revenge promeut l'outil de pfp et le token", "B", "id 1815128699831796065, supprimé ; texte connu par le seul Daily Dot"),
    P(1815130617392046479, "@DarkMagaCoin cite Winig : « la seule pièce qui pouvait avoir Elon »", "A"),
    P(1815130791208530273, "@DarkMagaCoin publie une capture de métadonnées", "A", "IMG_5658, 21/07 06:17, fuseau inconnu, date modifiable sur iOS. Déclaration, pas une preuve."),
    T(ath[0], f"Sommet du prix dans le pool, {ath[1]:,.0f} SOL de capitalisation", "A", "lu dans les soldes du pool Raydium, valeur maximale et non revente possible"),
    P(1815298322325811663, "@DarkMagaCoin revendique un DM à Musk", "A", "Revendiqué, non prouvé."),
    T(1721743284, "Envoi du nouvel avatar sans laser", "B", "id profile_images/1815749056821346304 : 14:01:24 UTC. Wayback : ancien avatar laser encore vu à 10:43:05 UTC, plus à 14:36:29 UTC"),
    P(1816000567740633335, "@DarkMagaCoin reformule : « on lui a envoyé le mème et il l'a aimé », à comparer au post du DM", "A"),
    P(1816846863649124596, "@DarkMagaCoin : « we built DMAGA first, sent Elon his pfp second »", "A"),
    T(1728408342, "@Aristos_Revenge raconte l'histoire du mouvement, adoption présentée comme une surprise", "B", "20 posts supprimés, texte par Thread Reader, evidence/web/threadreader_1843704335823454430.*"),
]
R.sort(key=lambda r: r[0])
head = """# Chronologie Dark MAGA

Généré par `scripts/rep_75_timeline.py`. Heures UTC. Attention, cette échelle note la **source** de chaque ligne, elle diffère de celle des conclusions du rapport. Fiabilité : A, fait directement contrôlable (transaction, post archivé, capture datée) ; B, une seule source
indirecte ou une lecture à confirmer ; C, non revérifié dans un fichier du projet. Une date de post vient de son identifiant ; dans tous les cas lus, elle
égale la métadonnée d'origine. Capitalisation : prix du pool juste avant l'instant × 10^9 × SOLUSDT à la minute.

| UTC | Fait | Fiabilité | Capitalisation | Source |
|---|---|---|---|---|
"""
body = ""
for t, lab, lvl, src in R:
    d = datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
    body += f"| {d} | {lab} | {lvl} | {fdv(t)} | {src.replace('|', '/')} |\n"
Path("docs/TIMELINE.md").write_text(fr(head + body))
print("lignes", len(R), "sommet", datetime.fromtimestamp(ath[0], timezone.utc).strftime("%d/%m %H:%M"), round(ath[1]))
