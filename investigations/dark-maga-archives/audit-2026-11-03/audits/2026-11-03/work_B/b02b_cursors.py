"""Lit les cursor.json de ctrl_tx, compare au S du fichier b01_peak.csv."""
import json, os, csv
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
HERE=Path(__file__).parent
root=EXT/"raw/ctrl_tx"
peak={r["pool"]:r for r in csv.DictReader(open(HERE/"b01_peak.csv"))}
tot=0; rows=[]
for p in sorted(x for x in os.listdir(root) if not x.startswith("._")):
    c=json.loads((root/p/"cursor.json").read_text())
    f=c["filters"]["blockTime"]; r=peak[p]
    s20=int(float(r["S20"])) if r["S20"] else None; s10=int(float(r["S10"])) if r["S10"] else None
    S=s20 if s20 else s10
    rows.append(dict(pool=p,n=c["n"],page=c["page"],complete=c.get("complete"),gte=f["gte"],lt=f["lt"],created=int(r["created"]),S20=s20,S10=s10,lt_eq_S20p1=(s20 is not None and f["lt"]==(s20+1)*3600),lt_eq_S10p1=(s10 is not None and f["lt"]==(s10+1)*3600),gte_eq_created=f["gte"]==int(r["created"]),filt_status=c["filters"].get("status")))
    tot+=c["n"]
with open(HERE/"b02b_cursors.csv","w",newline="") as fo:
    w=csv.DictWriter(fo,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print("tx total",tot,"pools",len(rows))
print("complete",sum(1 for r in rows if r["complete"]), "lt=S20+1h",sum(r["lt_eq_S20p1"] for r in rows),"lt=S10+1h seul",sum(r["lt_eq_S10p1"] and not r["lt_eq_S20p1"] for r in rows),"gte=created",sum(r["gte_eq_created"] for r in rows))
print("ni l'un ni l'autre",[ (r["pool"],r["lt"],r["S20"],r["S10"]) for r in rows if not (r["lt_eq_S20p1"] or r["lt_eq_S10p1"])][:10])
print("top n", sorted((r["n"] for r in rows),reverse=True)[:12])
