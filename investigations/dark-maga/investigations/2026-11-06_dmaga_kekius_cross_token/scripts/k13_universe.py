"""Univers DMAGA à tester : wallets prioritaires, groupe des 33, membres de clusters, adresses citées par les enquêtes.

Sortie : data/dmaga_universe.csv (address, tags). Les tags disent d'où vient chaque adresse ; aucune n'est un « suspect »."""
import csv, glob, json, re
from collections import defaultdict
import duckdb
from k_lib import DATA, DMAGA_BIG, REPO

tags = defaultdict(set)
for r in csv.reader(open(DMAGA_BIG.parent / "data" / "priority_wallets.csv")):
    tags[r[0]].add("priority")
g = json.load(open(REPO / "data" / "group_split.json"))
for se in g["sous_ensembles"]:
    for m in se["members"]:
        tags[m].add("group33")
for (members,) in duckdb.sql(f"select members from '{DMAGA_BIG}/wallet_clusters.parquet'").fetchall():
    for m in members.split(","):
        tags[m].add("cluster")
pat = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")
files = sorted(glob.glob(str(REPO / "investigations/2026-11-0[56]*/**/*.csv"), recursive=True)
               + glob.glob(str(REPO / "investigations/2026-11-0[56]*/*.md")) + [str(REPO / "docs/CASE_REPORT.md")]
               + glob.glob(str(REPO / "reports/*.md")))
for f in files:
    if "dmaga_kekius" in f:
        continue
    for a in pat.findall(open(f, errors="ignore").read()):
        if not a.isdigit():
            tags[a].add("cited")
core = DATA / "core_set.csv"  # produit par k19 (noyau DMAGA et contreparties directes)
if core.exists():
    for r in csv.DictReader(open(core)):
        tags[r["address"]].add("core" if r["via"] == "" else "core_cp")
DATA.mkdir(exist_ok=True)
with open(DATA / "dmaga_universe.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["address", "tags"])
    for a in sorted(tags):
        w.writerow([a, ";".join(sorted(tags[a]))])
print(len(tags), {t: sum(t in v for v in tags.values()) for t in ["priority", "group33", "cluster", "cited", "core", "core_cp"]})
