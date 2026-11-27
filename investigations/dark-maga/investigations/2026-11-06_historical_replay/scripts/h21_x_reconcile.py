"""Réconcilie les 5 155 observations de data/x_posts.jsonl : quel objet X chaque ligne désigne vraiment.

Hors ligne. Trois preuves, gardées séparément :
  1. l'objet RENVOYÉ par fxtwitter et par le point d'intégration (evidence/x_raw) : un ID renvoyé différent de l'ID demandé
     signifie que l'ID demandé est un repost, que ces API résolvent vers l'original ;
  2. les charges X archivées par la Wayback (evidence/x_wayback/recovered.jsonl) : author_id, username, referenced_tweets ;
  3. les champs reply_to_id et quote_id de la ligne.
Le compte dans l'URL d'archive n'est jamais une preuve d'auteur : il est noté à part (`url_account`).
Sortie : data/x_observations_reconciled.csv et data/x_reconcile_summary.json."""
import csv
import json
from collections import Counter
from h_lib import DATA, REPO
from dmaga.xposts import snowflake_utc

RAW = REPO / "evidence" / "x_raw"


def load(p):
    try:
        return json.loads(p.read_text())
    except (FileNotFoundError, ValueError):
        return None


def returned(i):
    """(id, auteur, id auteur, date) de l'objet rendu par chaque API, ou None."""
    out = {}
    fx = (load(RAW / f"{i}.fx.json") or {}).get("tweet") or {}
    if fx.get("id"):
        out["fx"] = (str(fx["id"]), (fx.get("author") or {}).get("screen_name"), str((fx.get("author") or {}).get("id") or ""), fx.get("created_timestamp"))
    sy = load(RAW / f"{i}.synd.json") or {}
    if sy.get("id_str"):
        out["synd"] = (sy["id_str"], (sy.get("user") or {}).get("screen_name"), (sy.get("user") or {}).get("id_str") or "", sy.get("created_at"))
    return out


def classify(r, wb, cdx_url):
    i = r["id"]
    ret = returned(i)
    ids = {v[0] for v in ret.values()}
    row = {"requested_id": i, "requested_snowflake_utc": snowflake_utc(i), "corpus_author": r["author"], "corpus_created_utc_metadata": r["created_utc_metadata"],
           "evidence": "+".join(sorted(ret) + (["wayback"] if wb else [])), "url_account": cdx_url, "relation": "", "object_id": "", "object_author": "",
           "object_author_id": "", "object_created_utc": "", "reposter": "", "reposter_evidence": "", "reply_to_id": r.get("reply_to_id") or "",
           "quote_id": r.get("quote_id") or "", "corpus_author_is_observation_author": ""}
    if len(ids) > 1:
        row["relation"] = "conflict_between_apis"
        return row
    if ids:
        oid = ids.pop()
        src = ret.get("synd") or ret.get("fx")
        row.update(object_id=oid, object_author=src[1] or "", object_author_id=src[2])
        row["object_created_utc"] = (r["created_utc_metadata"] or "") if oid != i else row["requested_snowflake_utc"]
        if oid == i:
            row["relation"] = "quote" if row["quote_id"] else ("reply" if row["reply_to_id"] else "original")
            row["corpus_author_is_observation_author"] = str(r["author"] == row["object_author"])
        else:
            row["relation"] = "repost"
            row["object_created_utc"] = snowflake_utc(oid)
            row["reply_to_id"] = row["quote_id"] = ""  # ces champs décrivent l'original, pas le repost
            if wb and wb.get("username"):
                row.update(reposter=wb["username"], reposter_evidence="wayback_payload")
            elif cdx_url:
                row.update(reposter=cdx_url, reposter_evidence="archived_url_path_unverified")
            row["corpus_author_is_observation_author"] = "False" if row["reposter_evidence"] == "wayback_payload" and wb["username"] != r["author"] else "unknown"
        return row
    if wb:
        refs = {x["type"]: x["id"] for x in wb.get("refs") or []}
        row.update(object_author=wb.get("username") or "", object_author_id=wb.get("author_id") or "", object_created_utc=row["requested_snowflake_utc"])
        if "retweeted" in refs:
            row.update(relation="repost", object_id=refs["retweeted"], reposter=wb.get("username") or "", reposter_evidence="wayback_payload",
                       object_author="", object_author_id="", object_created_utc=snowflake_utc(refs["retweeted"]))
        else:
            row.update(relation="quote" if "quoted" in refs else ("reply" if "replied_to" in refs else "original"), object_id=i,
                       quote_id=refs.get("quoted", row["quote_id"]), reply_to_id=refs.get("replied_to", row["reply_to_id"]))
        row["corpus_author_is_observation_author"] = str(r["author"] == wb["username"]) if wb.get("username") else "unknown"
        return row
    row["relation"] = "unavailable_unclassified"
    return row


def main():
    rows = [json.loads(l) for l in (REPO / "data" / "x_posts.jsonl").open()]
    wb = {}
    for l in (REPO / "evidence" / "x_wayback" / "recovered.jsonl").open():
        x = json.loads(l)
        wb.setdefault(x["id"], x)
    cdx = {}
    for p in sorted((REPO / "evidence" / "x_cdx").glob("*.json")):
        for x in load(p) or []:
            cdx.setdefault(x["id"], x["url"].split("/status")[0].rsplit("/", 1)[-1])
    for r in rows:  # même classe de preuve que l'URL d'archive : la liste CDX d'où vient l'ID
        if r["source_note"].startswith("Wayback CDX list for "):
            cdx.setdefault(r["id"], r["source_note"].rsplit(" ", 1)[-1])
    out = [classify(r, wb.get(r["id"]), cdx.get(r["id"], "")) for r in rows]
    with (DATA / "x_observations_reconciled.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    rel = Counter(o["relation"] for o in out)
    meta_dis = sum(1 for r in rows if r["created_utc_metadata"] and r["created_utc_metadata"] != r["created_utc_snowflake"])
    s = {
        "observations": len(out), "distinct_requested_ids": len({o["requested_id"] for o in out}),
        "relations": dict(rel),
        "repost_by_api_resolution": sum(1 for o in out if o["relation"] == "repost" and ("fx" in o["evidence"] or "synd" in o["evidence"])),
        "repost_by_wayback_refs": sum(1 for o in out if o["relation"] == "repost" and o["evidence"] == "wayback"),
        "metadata_snowflake_disagree": meta_dis,
        "metadata_disagree_explained_by_repost": sum(1 for r, o in zip(rows, out) if r["created_utc_metadata"] and r["created_utc_metadata"] != r["created_utc_snowflake"] and o["relation"] == "repost"),
        "distinct_objects_seen": len({o["object_id"] or o["requested_id"] for o in out}),
        "reposts_whose_original_is_also_a_row": sum(1 for o in out if o["relation"] == "repost" and o["object_id"] in {r["id"] for r in rows}),
        "reposter_evidence": dict(Counter(o["reposter_evidence"] for o in out if o["relation"] == "repost")),
        "corpus_author_check": dict(Counter(o["corpus_author_is_observation_author"] for o in out)),
    }
    assert s["metadata_disagree_explained_by_repost"] == s["metadata_snowflake_disagree"], "écart métadonnée/ID non expliqué par un repost"
    (DATA / "x_reconcile_summary.json").write_text(json.dumps(s, indent=1, ensure_ascii=False))
    print(json.dumps(s, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
