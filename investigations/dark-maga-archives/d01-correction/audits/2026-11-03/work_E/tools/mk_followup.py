"""Génère x_search_log.jsonl, complète x_posts_new.jsonl et écrit X_FOLLOWUP.md depuis le manifeste.
Les empreintes et les heures viennent des fichiers, jamais d'une saisie. usage: python3 -I mk_followup.py
"""
import gzip, hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

W = e.W
REPO = W.parent.parent.parent
MAN = {}
for l in open(e.MAN):
    r = json.loads(l)
    if r.get("file") and r.get("http") == 200:
        MAN[r["file"]] = r
OLD = {json.loads(l)["id"]: json.loads(l) for l in open(REPO / "data/x_posts.jsonl")}
REC = {}
for l in open(REPO / "evidence/x_wayback/recovered.jsonl"):
    r = json.loads(l)
    if "error" not in r:
        REC[r["id"]] = r
WB = {json.loads(l)["id"]: json.loads(l) for l in open(W / "wb_status_recovered.jsonl")}

# capture d'écran copiée depuis le navigateur : pas de GET, donc ajoutée ici au manifeste
shot = "evidence/x_screens_pmarca_1814763940410499481.jpg"
if shot not in MAN:
    b = (W / shot).read_bytes()
    rec = {"url": "https://x.com/pmarca/status/1814763940410499481 (capture d'écran du navigateur connecté)", "file": shot, "http": 200, "error": None, "content_type": "image/jpeg",
           "collected_utc": "2026-11-03T10:2", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "note": "montre le lien vers /kikisknees/status/1814738306589917312 ; heure de collecte connue à la dizaine de minutes"}
    with e.MAN.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    MAN[shot] = rec

SEARCHES = [
    ("from:DarkMagaCoin until:2024-07-14", 12, "que des reposts, aucun post propre"),
    ("from:ChrisWinig since:2024-07-20 until:2024-07-22", 20, ""),
    ("from:ChrisWinig since:2024-07-11 until:2024-07-20", 37, ""),
    ("from:ChrisWinig since:2024-06-01 until:2024-07-11", None, "résultat perdu, délai du navigateur, refaite en n°8"),
    ("from:kikisknees since:2024-06-01 until:2024-08-01", None, "résultat perdu, délai du navigateur, refaite en n°7"),
    ("to:kikisknees since:2024-07-21 until:2024-07-22", 194, "réponses à des posts supprimés, encore visibles"),
    ("from:kikisknees since:2024-06-01 until:2024-08-01", 29, "1 seul post propre, le reste des reposts"),
    ("from:ChrisWinig since:2024-06-01 until:2024-07-11", 49, ""),
    ("9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", 5, "source sociale retrouvée"),
    ("from:XHEILIGX (dmaga OR \"dark maga\" OR wallet OR bought) since:2024-07-01 until:2024-10-01", 0, "page d'erreur probable, non concluant"),
    ("from:XHEILIGX since:2024-07-10 until:2024-08-05", 0, "page d'erreur probable, non concluant"),
    ("from:DarkMagaCoin (DM OR DMed OR DMd OR \"sent him\" OR \"sent Elon\" OR \"sent it\") since:2024-07-14", 0, "page d'erreur probable, non concluant"),
    ("from:DarkMagaCoin DM since:2024-07-14 until:2024-10-01", None, "« Une erreur s'est produite », limite de débit probable, capture à l'écran"),
    ("from:DarkMagaCoin DM since:2024-07-14 until:2024-10-01", 2, "après pause"),
    ("from:DarkMagaCoin elon since:2024-07-14 until:2024-07-22", 18, ""),
    ("8YLEuUtZ… OR 5QhJJc… OR H3QsBr… OR GXZvX… OR 7FGoCB… OR G41vRr… OR 9W9b3z… OR C73Yv… OR AtZjv3… OR DX9i7J3… (adresses entières)", 33, "commentaires de tiers"),
    ("(elon OR musk OR elonmusk) (\"dark maga\" OR dmaga OR darkmaga) since_time:1721347200 until_time:1721589800", 5, "a révélé @FrancoAppr et @EeOo111_"),
    ("to:elonmusk (from:FrancoAppr OR from:EeOo111_ OR from:greenchartlover OR from:GattodiLargo OR from:ZephyrusOtiosus OR from:Murray_Gothbard OR from:GreatBambin0 OR from:sugee14 OR from:kanpai OR from:Fudrap96 OR from:DefiMamaTake8 OR from:RPPKyle OR from:DarkMagaCoin OR from:ChrisWinig OR from:kikisknees) since_time:1720915200 until_time:1721589800", 23, ""),
    ("(from:GreatBambin0 OR from:FrancoAppr OR from:EeOo111_) since_time:1721347200 until_time:1721576301", 20, ""),
    ("8YLEuUtZ… OR 5QhJJc… OR GXZvX… OR 7FGoCB… OR G41vRr… OR 9W9b3z… OR C73Yv… OR AtZjv3… OR DX9i7J3… OR 6Zoi7ZZE… (adresses entières)", 4, "créateur 8YLEu… jamais nommé"),
    ("FTKTNF… OR F1DRDB… OR 6Lomz4… OR CEzjbQ… OR DKs3wS… OR Go3fTC… OR FHXYk1… OR 9cfRU5… (adresses entières)", 20, "commentaires de tiers"),
    ("(elon OR musk OR pfp) (dmaga OR \"dark maga\") (DM OR DMed OR DMd OR \"sent him\" OR \"sent it\" OR \"sent to\") since:2024-07-21 until:2024-08-05", 2, ""),
    ("from:Aristos_Revenge since:2024-07-13 until:2024-07-23", 0, "« aucun résultat » affiché"),
    ("(elon OR musk) (pfp OR avi OR \"profile pic\" OR dmagafy OR \"dark maga\" OR dmaga) since_time:1721347200 until_time:1721568645", 20, "bruit, requête trop large"),
    ("from:XHEILIGX dmaga", 28, ""),
    ("2BLSXb… OR 2mW45k… OR 2r8DCW… OR 35nAuv… OR 45ruCy… OR 4Eishu… OR 4upmFY… OR 4wComY… OR 5Q544f… OR 6LXutJ… (adresses entières de data/group_split.json)", 25, "ce fichier mêle des services (Raydium, Jupiter) : requête polluée, série arrêtée"),
    ("from:DarkMagaCoin (wallet OR solscan OR bought OR dev OR burn OR treasury OR team) since:2024-07-14 until:2024-12-31", 19, ""),
    ("from:ChrisWinig (elon OR musk OR dmaga OR \"dark maga\" OR bought OR wallet) since:2024-07-22 until:2025-06-01", 23, ""),
    ("from:twicrates (dmaga OR \"dark maga\" OR kiki) since:2024-07-13 until:2024-07-24", 30, ""),
    ("from:koreanjewcrypto (elon OR pfp OR DM OR bought OR wallet OR team OR kiki) since:2024-07-13 until:2024-07-24", 11, ""),
]
assert len(SEARCHES) == 30
with open(W / "x_search_log.jsonl", "w") as f:
    for n, (q, k, note) in enumerate(SEARCHES, 1):
        f.write(json.dumps({"n": n, "query": q, "onglet": "Récents", "resultats_lus": k, "note": note, "fenetre_collecte_utc": "2026-11-03 entre 10:10 et 10:55"}, ensure_ascii=False) + "\n")

# x_posts_new.jsonl : posts live déjà écrits par posts.py, sans les doublons du corpus, plus les textes Wayback
live = [json.loads(l) for l in open(W / "x_posts_new.jsonl")]
live = [x for x in live if not x.get("source_note", "").startswith("Wayback capture")]
keep = {}
for x in live:
    o = OLD.get(x["id"])
    if o and o.get("status") == "ok":
        continue  # déjà dans le corpus, sa preuve brute reste dans evidence/x_raw_new
    if x["status"] == "ok":
        keep[x["id"]] = x


def wbrow(i, x, src):
    un = {u["id"]: u["username"] for u in x.get("users") or []}
    refs = x.get("refs") or []
    return {"id": i, "author": x.get("username"), "author_name": None, "created_utc_metadata": (x.get("created_at") or "").replace(".000Z", "Z") or None,
            "created_utc_snowflake": e.sf(i), "ts_reliability": "metadata+snowflake" if x.get("created_at") else "snowflake_only", "text": x.get("text"),
            "reply_to_user": un.get(x.get("reply_to_user")) or x.get("reply_to_user"), "reply_to_id": next((r["id"] for r in refs if r["type"] == "replied_to"), None),
            "quote_id": next((r["id"] for r in refs if r["type"] == "quoted"), None), "retweets": None, "likes": None, "replies": None, "views": None,
            "media": [m.get("url") or m.get("preview_image_url") for m in x.get("media") or []], "status": "unavailable", "fx_http": None, "synd_type": None,
            "source_note": src, "provenance": [x["file"]], "fetched_utc": e.now()}


for i, x in WB.items():
    if x.get("text") and i not in keep and x.get("account_in_url"):
        p = "audits/2026-11-03/work_E/" + x["file"]
        keep[i] = wbrow(i, {**x, "file": p}, "Wayback capture API v2 à la publication, post supprimé en direct, lu le 03/11/2026 (work_E)")
# premier post propre de @DarkMagaCoin : texte connu par la capture du repost de @kikisknees
cap = json.load(open(REPO / "evidence/x_wayback/1812317575411351639.raw"))
t0 = next(t for t in cap["includes"]["tweets"] if t["id"] == "1812312706826854843")
keep["1812312706826854843"] = {"id": "1812312706826854843", "author": "DarkMagaCoin", "author_name": "Dark Maga", "created_utc_metadata": t0["created_at"].replace(".000Z", "Z"),
                               "created_utc_snowflake": e.sf("1812312706826854843"), "ts_reliability": "metadata+snowflake", "text": t0["text"], "reply_to_user": None, "reply_to_id": None, "quote_id": None,
                               "retweets": None, "likes": None, "replies": None, "views": None, "media": [], "status": "unavailable", "fx_http": 404, "synd_type": None,
                               "source_note": "texte lu dans evidence/x_wayback/1812317575411351639.raw (repost par @kikisknees)", "provenance": ["evidence/x_wayback/1812317575411351639.raw"], "fetched_utc": e.now()}
with open(W / "x_posts_new.jsonl", "w") as f:
    for i in sorted(keep, key=int):
        f.write(json.dumps(keep[i], ensure_ascii=False) + "\n")
keys0 = set(next(iter(OLD.values())))
assert all(set(x) == keys0 for x in keep.values()), "schéma différent de data/x_posts.jsonl"


# couverture Wayback
def load(n):
    p = REPO / f"evidence/x_cdx/{n}.json.gz"
    return json.load(gzip.open(p)) if p.exists() else json.load(open(REPO / f"evidence/x_cdx/{n}.json"))


cdx = load("kikisknees")
COV = []
for a, b, lab in [("2024-06-11", "2024-07-11", "11/06 au 10/07"), ("2024-07-11", "2024-07-13T22:11", "11/07 au 13/07 22:11 (avant Butler)"), ("2024-07-13T22:11", "2024-07-14", "13/07 22:11 à minuit"),
                  ("2024-07-14", "2024-07-20", "14/07 au 19/07"), ("2024-07-20", "2024-07-21T12:51", "20/07 au 21/07 12:51"), ("2024-07-21T12:51", "2024-07-22T07", "21/07 12:51 au 22/07 07:00"), ("2024-07-22T07", "2024-07-27", "22/07 07:00 au 26/07")]:
    s = [x["id"] for x in cdx if a <= x["created_utc_snowflake"] < b]
    COV.append((lab, len(s), sum(1 for i in s if i in REC), sum(1 for i in s if i in WB and WB[i].get("text"))))
covrows = "\n".join(f"| {a} | {b} | {c} | {d} | {b - c - d} |" for a, b, c, d in COV)
parse_err = sum(1 for x in WB.values() if x.get("parse_error"))
pre = [x for x in WB.values() if x.get("text") and x["snowflake"] < "2024-07-13T22:11"]
pre_hits = [x for x in pre if re.search(r"dark\s*maga|dmaga", x["text"], re.I)]
pre_coin = [x for x in pre if re.search(r"\$[a-z]{3,}", x["text"], re.I) and not x["text"].startswith("RT @")]
pre_musk = [x for x in pre if re.search(r"\belon\b|musk", x["text"], re.I) and not x["text"].startswith("RT @")]
first_musk = sorted([x for x in WB.values() if x.get("text") and re.search(r"@elonmusk", x["text"]) and not x["text"].startswith("RT @")], key=lambda x: int(x["id"]))
early_musk = [x for x in first_musk if x["snowflake"] >= "2024-07-13T22:11"][:6]
early_txt = "\n".join("- `%s` %s : « %s »" % (x["id"], x["snowflake"], re.sub(r"\s+", " ", x["text"].replace("&amp;", "&"))[:110].strip()) for x in early_musk) or "- aucun"
pre_musk_txt = "\n".join(f"- `{x['id']}` {x['snowflake']} : « {re.sub(chr(10), ' ', x['text'])[:110]} »" for x in sorted(pre_musk, key=lambda x: int(x["id"]))[:12]) or "- aucun"
wb_err = sum(1 for l in open(e.MAN) if "web.archive.org" in json.loads(l)["url"] and (json.loads(l).get("error") or json.loads(l).get("http") in (429, 502, 503, 504)))
wb_ok = sum(1 for l in open(e.MAN) if "web.archive.org" in json.loads(l)["url"] and json.loads(l).get("http") == 200)
n_new_live = sum(1 for x in keep.values() if x["status"] == "ok")
n_new_wb = sum(1 for x in keep.values() if x["status"] != "ok")
media_wb = sorted(p.name for p in (W / "evidence/x_media_wb_new").iterdir())


def media_file(key):
    for f in MAN:
        if f.startswith("evidence/x_media_wb_new/" + key) or (f.startswith("evidence/x_media_new/") and key in f):
            return f
    raise KeyError(key)


def ref(i):
    f = f"evidence/x_raw_new/{i}.fx.json"
    if f in MAN and MAN[f]["bytes"] > 100 and b'"code":200' in (W / f).read_bytes()[:40]:
        return f, MAN[f]["sha256"]
    if i in WB:
        return WB[i]["file"], MAN[WB[i]["file"]]["sha256"]
    if i in REC:
        return f"../../../evidence/x_wayback/{i}.raw", REC[i]["sha256"]
    raise KeyError(i)


def row(i, auteur, typ, niveau, media=None, cap=None):
    if cap:
        f, s = f"../../../evidence/x_wayback/{cap}.raw", REC[cap]["sha256"]
    else:
        f, s = ref(i)
    cell = f"`{f}` {s}"
    if media:
        mf = media_file(media)
        cell += f" ; image `{mf}` {MAN[mf]['sha256']}"
    return e.sf(i), f"| {e.sf(i)} | @{auteur} `{i}` | {typ} | {cell} | {niveau} |"


def doc(file, utc, auteur, typ, niveau):
    return utc, f"| {utc} | {auteur} | {typ} | `{file}` {MAN[file]['sha256']} | {niveau} |"


T = [
    row("1813310692243480937", "FrancoAppr", "réponse à @elonmusk, Musk aux yeux laser sur fond rouge, autre composition", "A pour la date, C pour le lien avec l'avatar", "GSosdsSWYAACOIC"),
    row("1814063148917256375", "kikisknees", "réponse à @elonmusk, « We are building an army for you for that purpose. $DMAGA », V0", "A", "GSzYuoTXgAA63zz"),
    row("1814814222213165057", "kikisknees", "V0 reprise, « We do. $DMAGA does too. »", "A", "GS-D11oXEAAfsvX"),
    row("1814738306589917312", "kikisknees", "réponse à @pmarca, Charlie Brown rouge, pHash 0 avec l'image de @pmarca", "A", "GS8-wUDWMAAqpGm", cap="1815123417064255531"),
    row("1814763940410499481", "pmarca", "publie la même image, le post lie le statut de @kikisknees", "A"),
    row("1814705414325354820", "kikisknees", "réponse à @elonmusk avec #DarkMAGA, image de catcheurs, pas Musk", "A", "GS8g7B3WEAEmKSw"),
    row("1814863915186016702", "kikisknees", "réponse à @FoxNews et @elonmusk, « Building an army for $DMAGA IS smart. »", "A"),
    row("1814920352134537332", "pmarca", "« THAT'S RIGHT. », vrai post, 5 h 35 avant la date du dossier", "A"),
    row("1815006501896872388", "kikisknees", "**plus ancienne image connue du visuel de Musk**, variante V1, réponse à @pmarca", "A", "GTAytGIW4AE9_93"),
    row("1815032564895150177", "GreatBambin0", "« When Elon pfp change? », DÉCLARATION", "A"),
    row("1815047331609219106", "GreatBambin0", "« wen pfp.. Now pfp », réponse à @koreanjewcrypto", "A"),
    row("1815053713330876681", "GreatBambin0", "**plus ancien envoi connu à Musk**, V1, 21 s avant son « Whoa »", "A", "GTBdu7vXgAARcaz"),
    row("1815054158367432804", "kikisknees", "réponse à Musk, image retrouvée, c'est le Trump « dark maga », pas Musk", "A", "GTBeEjGXgAAbn4S"),
    row("1815054374982324401", "FrancoAppr", "**plus ancienne image identique connue**, V2, pHash 0 avec l'avatar", "A", "GTBeVcVXAAAVa3o"),
    row("1815054381823221968", "EeOo111_", "V1, « Whoa, ELON IN DARK MAGA »", "A", "GTBeVlkXsAAgbTW"),
    row("1815057307836842034", "DarkMagaCoin", "V1 en réponse à Musk, « Based GC members: »", "A", "GTBg8wsXoAAouzI"),
    row("1815062189763703119", "GreatBambin0", "plus ancienne variante V3 connue", "A", "GTBlcMpWkAABbvL"),
    row("1815092319244128645", "FrancoAppr", "« A changed Elon could use a changed profile picture », V2, 52 min avant l'avatar", "A", "GTCA2FyXcAAH6aD"),
    row("1815094431152029711", "Murray_Gothbard", "V2 en réponse à Musk", "A", "GTCCxFyWMAA4Cy1"),
    row("1815096055337496944", "kikisknees", "réponse à Musk, image retrouvée, V3", "A", "GTCEEQ2WoAAm65s"),
    row("1815107549903135205", "ChrisWinig", "vrai post « Elon just made this his profile picture! », 54 s avant la date du dossier", "A"),
    row("1815108304823050265", "koreanjewcrypto", "« team gave elon 1% of supply », DÉCLARATION sans preuve, ton possiblement ironique", "D"),
    row("1815116385414209876", "kikisknees", "« That's a $DMAGA pfp, made by me. », image retrouvée, Trump, pas Musk", "A", "GTCWqbzXUAAYsUP"),
    row("1815172240234950777", "Shill_Matic1", "« the pfp that was sent to him », DÉCLARATION", "C"),
    row("1815197098813399267", "SundayFundayLFG", "« I was told that Elon got his new PFP from the Dark MAGA team », DÉCLARATION", "C"),
    row("1815873841870299404", "twicrates", "« i was sent some that ive never touched », DÉCLARATION", "C"),
    row("1812965882827842030", "twicrates", "« being in kiki coins rules », DÉCLARATION", "C"),
    row("1813041645899649082", "koreanjewcrypto", "« I haven't sold a single $dmaga, bought more actually », DÉCLARATION", "C"),
    row("1812326326176469155", "CryptoOnlyCoims", "« Just bought 1 SOL », vrai post, DÉCLARATION", "C"),
    row("1845511546681823704", "ChrisWinig", "« We memed the greatest entrepreneur... into the Dark Maga cult », DÉCLARATION", "C"),
    row("1853482649979146405", "DarkMagaCoin", "Space de « the Dark MAGA team » avec @kikisknees, @Aristos_Revenge et d'autres", "A pour le post, C pour le lien"),
    row("1773892399875727679", "pezitoken", "offre de jetons contre tag, parent de la réponse de @XHEILIGX", "A"),
    row("1773893309028577383", "XHEILIGX", "publie l'adresse entière 9PrmF8… 106 jours avant le mint", "A pour le post, C pour le contrôle du wallet"),
    row("1814822863695655368", "XHEILIGX", "réponse à @kikisknees et @DarkMagaCoin, « $DMAGA #SOL »", "A"),
    row("1823489213817610303", "0xbeehive", "« Insider - 9PrmF8… », plus ancien fil d'août retrouvé", "A pour le post, C pour le contenu"),
    row("1824139700187304048", "thekuchh", "« Key Wallet: 9PrmF8… »", "A pour le post, C pour le contenu"),
    row("1824779938626736278", "0xchromium", "adresse 9PrmF8…", "A pour le post, C pour le contenu"),
    row("1825526180616827284", "cryptosymbiiote", "« Second Insider ... 9PrmF8… »", "A pour le post, C pour le contenu"),
    row("1815314626596512111", "haspidox", "plus ancien post retrouvé avec H3QsBr… en entier, commentaire", "A pour le post, C pour le contenu"),
    row("1815357723577340268", "kkashi_yt", "plus ancien post retrouvé avec 5QhJJc… en entier, commentaire", "A pour le post, C pour le contenu"),
    row("1788632665182052689", "Ralvero", "annonce d'achat de #DARKMAGA, mint 6Zoi7ZZE…, projet distinct du 09/05/2024", "A pour le post, C pour le lien"),
    row("1814880500311294441", "kritcheye", "« Kiki watch out for $barron », DÉCLARATION", "C"),
    doc("evidence/token/ipfs_meta_gateway.pinata.cloud.json", "2024-07-14T02:05:25Z", "métadonnées IPFS du mint", "aucun X, Telegram ni site à la création", "A"),
    doc("evidence/token_img/ipfs_token_image.bin", "2024-07-14T02:05:25Z", "image IPFS du mint", "Trump rouge aux yeux laser", "A"),
    doc("evidence/domains/crtsh_dmaga.xyz.json", "2024-07-14T02:41:38Z", "crt.sh dmaga.xyz", "premier certificat, GoDaddy, id 13729224712", "A"),
    doc("evidence/domains/crtsh_darkmaga.com.json", "2024-08-01T00:00:00Z", "crt.sh darkmaga.com", "premier certificat au journal, Sectigo, id 13957636645", "A"),
    doc("evidence/domains/wb_darkmaga_20240803.html", "2024-08-03T18:26:57Z", "Wayback darkmaga.com", "premier contenu archivé, site DMAGA", "A"),
    doc("evidence/domains/crtsh_darkmagacoin.com.json", "2024-10-07T17:24:52Z", "crt.sh darkmagacoin.com", "premier certificat", "A"),
    doc("evidence/domains/rdap_darkmagapls.com.json", "2024-11-06T09:45:19Z", "RDAP darkmagapls.com", "enregistrement, après l'élection", "A"),
    doc("evidence/telegram/tg_s_DarkMAGAonSOL.html", "2024-05-09T17:13:36Z", "Telegram darkmagaonsol", "création, projet $DARKMAGA", "A"),
    doc("evidence/darkmagaonsol/tx_2PAQ7iTyAXAEgkLM.json", "2024-05-09T18:11:30Z", "transaction du mint revoke", "signataire DX9i7J3…, mint 6Zoi7ZZE…", "A"),
    doc("evidence/telegram/tg_s_BARRONTRVMP.html", "2024-04-21T20:02:30Z", "Telegram BARRONTRVMP", "création, voisin de @Barronsolana", "A"),
    doc("evidence/chan/warosu_biz2_dmaga_.html", "2024-07-22T03:23:20Z", "/biz/ post 58770350, Warosu", "« provided to elon by dmaga admin »", "C"),
    doc("evidence/chan/palanq_pol_dark___maga_.json", "2024-07-14T04:36:51Z", "/pol/ post 80672624, Palanq", "« He doesn't know Dark MAGA is online », sans lien avec le jeton", "C"),
]
T.sort(key=lambda x: x[0])
table = "\n".join(x[1] for x in T)

av = json.load(open(W / "derived/avatar_changes.json"))
av_ok = sum(len(v) for v in av.values())
av_prev = sum(len(v) - 1 for v in av.values())
k900 = sorted([x for x in WB.values() if x.get("text") and not x["text"].startswith("RT @") and "2024-07-14" <= x["snowflake"] < "2024-07-21T12:51" and any((m.get("width"), m.get("height")) in ((900, 900), (900, 899)) for m in x.get("media") or [])], key=lambda x: int(x["id"]))
w1113 = next(c for c in COV if c[0].startswith("11/07"))
tpl = (W / "tools/followup_tpl.md").read_text().replace("{{AV_OK}}", str(av_ok)).replace("{{AV_PREV}}", str(av_prev)).replace("{{W1113_R}}", str(w1113[2] + w1113[3])).replace("{{W1113_N}}", str(w1113[1])) \
    .replace("{{TP_N}}", str(sum(1 for l in open(W / "derived/trades_probe.txt") if l.startswith("172") and len(l.split()) >= 6))).replace("{{FIN}}", e.now()[11:16]).replace("{{KIKI900_N}}", str(len(k900))).replace("{{KIKI900_FIRST}}", k900[0]["snowflake"][:19].replace("T", " ")).replace("{{BARRON_N}}", str(sum(1 for x in WB.values() if (x.get("text") or "").startswith("RT @Barronsolana")))).replace("{{WB_TEXT}}", str(sum(1 for x in WB.values() if x.get("text"))))
out = tpl.replace("{{TABLE}}", table).replace("{{COV}}", covrows).replace("{{N_LIVE}}", str(n_new_live)).replace("{{N_WB}}", str(n_new_wb)).replace("{{WB_OK}}", str(wb_ok)).replace("{{WB_ERR}}", str(wb_err)) \
    .replace("{{PARSE_ERR}}", str(parse_err)).replace("{{PRE_N}}", str(len(pre))).replace("{{PRE_HITS}}", str(len(pre_hits))).replace("{{PRE_COIN}}", str(len(pre_coin))).replace("{{PRE_MUSK}}", str(len(pre_musk))) \
    .replace("{{PRE_MUSK_TXT}}", pre_musk_txt).replace("{{EARLY_MUSK}}", early_txt).replace("{{N_MEDIA_WB}}", str(len(media_wb))).replace("{{CORPUS_BAD}}", str(sum(1 for x in OLD.values() if x.get("created_utc_metadata") and x["created_utc_metadata"] != x["created_utc_snowflake"]))).replace("{{CORPUS_N}}", str(len(OLD)))
assert "{{" not in out, re.findall(r"\{\{\w+\}\}", out)
bad = [c for c in ("—", "–") if c in out]
assert not bad, bad
(W / "X_FOLLOWUP.md").write_text(out)
# auto-contrôle : tout id cité a une preuve dans le corpus, les captures ou work_E
ids = set(re.findall(r"\b(1[6-9]\d{17})\b", out))
# ids sans ligne propre : avatars, ou posts lus dans le fx.json d'un repost ou d'une citation, ou dans une capture
LUS_AILLEURS = {"1812984492157771825", "1813086353741230327", "1815131407951561080", "1812303793645666304", "1815105297410666496", "1814738306589917312", "1814882075519971504"}
miss = [i for i in ids if i not in OLD and i not in keep and i not in REC and i not in WB and i not in LUS_AILLEURS and not (W / f"evidence/x_raw_new/{i}.fx.json").exists()]
print("ids", len(ids), "sans preuve", miss)
print("posts nouveaux", len(keep), "live", n_new_live, "wayback", n_new_wb, "pre", len(pre), "hits", len(pre_hits), [x["id"] for x in pre_hits][:5], "pre_musk", len(pre_musk), "wb ok/err", wb_ok, wb_err)
print(early_txt)
print(pre_musk_txt)
print(sum(1 for f in W.rglob("*") if f.is_file()), sum(f.stat().st_size for f in W.rglob("*") if f.is_file()) // 1024 // 1024, "Mo")
