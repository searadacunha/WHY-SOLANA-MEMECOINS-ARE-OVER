#!/usr/bin/env python3
"""Aplatit raw/flows/<wallet>/dmaga_all.json.gz et note les troncatures. Sortie: audits_work/C/flows_dmaga.csv.gz + flows_files.csv.gz"""
import csv, gzip, json, time
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
OUT = EXT/"audits_work"/"C"
fl = EXT/"raw"/"flows"
fo = gzip.open(OUT/"flows_dmaga.csv.gz","wt",compresslevel=3,newline="")
ff = gzip.open(OUT/"flows_files.csv.gz","wt",compresslevel=3,newline="")
w = csv.writer(fo); wf = csv.writer(ff)
w.writerow("wallet sig slot idx bt type from_u to_u from_ta to_ta amount ii jj".split())
wf.writerow("wallet query truncated n".split())
n=0
for d in sorted(x for x in fl.iterdir() if x.is_dir() and not x.name.startswith("._")):
    for q in sorted(x for x in d.iterdir() if x.name.endswith(".json.gz") and not x.name.startswith("._")):
        j=json.load(gzip.open(q,"rt"))
        name=q.name[:-8]
        if "rows" not in j:
            continue
        wf.writerow([d.name,name,j["truncated"],len(j["rows"])])
        if name=="dmaga_all":
            for r in j["rows"]:
                w.writerow([d.name,r["signature"],r["slot"],r.get("transactionIdx"),r["blockTime"],r["type"],r.get("fromUserAccount"),r.get("toUserAccount"),r.get("fromTokenAccount"),r.get("toTokenAccount"),r["amount"],r.get("instructionIdx"),r.get("innerInstructionIdx")])
                n+=1
    if n and n%50000<50: print(n,d.name,flush=True)
fo.close(); ff.close(); print("FIN",n)
