import csv, sys
rows = [r for r in csv.DictReader(open("audits/2026-11-03/work_G/g10_dest.csv"))]
rows = [r for r in rows if r["venue"] == "False" and not r["label"]]
print("sans étiquette ni venue", len(rows))
# destinations touchant le périmètre
per = [r for r in rows if r["roles"]]
per.sort(key=lambda r: (-sum(int(x.split(":")[1]) for x in r["roles"].split(";")), -float(r["soleq"])))
print("touchant un périmètre", len(per))
for r in per[:70]:
    print(r["dst"], "ns", r["n_senders"], "n", r["n"], "eq", r["soleq"], r["first"], r["last"], r["roles"])
