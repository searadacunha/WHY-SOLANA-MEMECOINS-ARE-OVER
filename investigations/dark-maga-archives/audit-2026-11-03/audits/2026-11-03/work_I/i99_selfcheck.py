"""Autocontrôle de REFUTATION.md : chaque adresse, signature ou hash complet doit se retrouver tel quel dans une sortie de work_I ou dans un fichier source cité. Aucun tiret cadratin ni demi-cadratin. Sortie i99_selfcheck.txt, code 1 si échec."""
import re,glob,gzip,sys,os
OUT="audits/2026-11-03/work_I/"
md=open(OUT+"REFUTATION.md",encoding="utf-8").read()
assert "—" not in md and "–" not in md,"tiret interdit"
toks=set(re.findall(r"(?<![A-Za-z0-9])[1-9A-HJ-NP-Za-km-z]{32,90}(?![A-Za-z0-9])",md))|set(re.findall(r"0x[0-9a-f]{40,64}",md))|set(re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])",md))
hay=""
for p in glob.glob(OUT+"*.txt")+glob.glob(OUT+"*.csv"):
    hay+=open(p,encoding="utf-8",errors="ignore").read()
for p in ("audits/2026-11-03/work_G/flow_boundaries.csv","audits/2026-11-03/work_G/g30_in.csv","audits/2026-11-03/work_E/X_FOLLOWUP.md","reports/TOP_TRADERS.md","audits/2026-11-03/work_G/prefixes.txt"):
    hay+=open(p,encoding="utf-8",errors="ignore").read()
bad=[t for t in sorted(toks) if t not in hay]
L=open(OUT+"i99_selfcheck.txt","w")
print("références",len(toks),"introuvables",len(bad),file=L)
for b in bad:print("  ",b,file=L)
print("références",len(toks),"introuvables",bad)
sys.exit(1 if bad else 0)
