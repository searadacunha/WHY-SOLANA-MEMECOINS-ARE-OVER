#!/usr/bin/env python3
"""Rafraîchit data/collector.json sans réseau : ana_65 reste la collecte, ses réponses sont archivées dans le fichier du dépôt.

Seuls changent les champs tirés du dérivé local (réalisé et appartenance au groupe des expéditeurs, groupes touchés). Expéditeurs : sortie complète de l'audit D.
"""
import csv
import json
from pathlib import Path

from dmaga.db import connect
from dmaga.paths import BIG, DATA, SOURCES, exige_v2

exige_v2()
COL = json.loads((SOURCES / "collector.json").read_text())
senders = {r["sender"] for r in csv.DictReader(Path("audits/2026-11-03/work_D/d20_senders.csv").open())}
assert len(senders) == COL["expediteurs"] == 48
groups = json.loads((DATA / "prevent_groups.json").read_text())
members = set(groups[0]["members"])
con = connect(mem="300MB")
pnl = dict(con.execute(f"SELECT owner, realized_sol FROM read_parquet('{BIG}/wallets.parquet')").fetchall())
for r in COL["wallets_de_l_enquete"]:
    r["realise_dmaga"] = pnl.get(r["wallet"])
    r["groupe"] = r["wallet"] in members
for c in COL["salves"]:
    c["groupe"] = c["wallet"] in members
touched = [g for g in groups if senders & set(g["members"])]
COL["groupes_touches"] = [{"n": g["n"], "held_M": g["held_before_musk_M"], "realized_sol": g["realized_sol"], "expediteurs": sorted(senders & set(g["members"]))} for g in touched]
COL["ensemble_elargi_held_M"] = sum(g["held_before_musk_M"] for g in touched)
(DATA / "collector.json").write_text(json.dumps(COL, indent=1, ensure_ascii=False))
print("groupes touchés", len(touched), "élargi M", round(COL["ensemble_elargi_held_M"], 1))
