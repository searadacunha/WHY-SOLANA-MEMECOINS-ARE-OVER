"""Archive les réponses réseau de rep_72 depuis les rapports du commit 01ae5a4 (sorties complètes, jamais retapées). Écrit reports/data_checks/rep72_reseau.json."""
import json, re, subprocess
def show(p): return subprocess.run(["git", "show", f"01ae5a4:{p}"], capture_output=True, text=True, check=True).stdout
def table_after(txt, titre):
    i = txt.index(titre); lines = txt[i:].splitlines()[1:]
    while not lines[0].startswith("|"): lines = lines[1:]
    out = []
    for l in lines[2:]:
        if not l.startswith("|"): break
        out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out
co, at = show("reports/COORDINATION.md"), show("reports/ATTRIBUTION.md")
prep = table_after(co, "### Autres virements de SOL avant le lancement")
link = table_after(at, "## Lien entre le créateur et le groupe")
m = re.search(r"le créateur n'a reçu que (\d+) virements d'au moins [^:]*: (.*?)\. Le virement", at, re.S)
res = {"source": "reports/*.md au commit 01ae5a4, réponses getTransfersByAddress du 03/11, réseau non rappelé", "prep": prep, "link_rows": link, "creator_in_n": int(m.group(1)), "sources_in": m.group(2)}
json.dump(res, open("reports/data_checks/rep72_reseau.json", "w"), indent=1, ensure_ascii=False)
print(len(prep), len(link), m.group(1), m.group(2)[:200]); print(prep[0]); print(link[0])
