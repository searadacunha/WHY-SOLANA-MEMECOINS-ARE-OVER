"""Sceau de la phase aveugle : sha256 des fichiers aveugles + heure UTC. À lancer une seule fois."""
import hashlib, datetime, sys
from pathlib import Path
H = Path(__file__).parent
S = H / "SEAL.txt"
assert not S.exists(), "sceau déjà posé"
L = [f"sceau posé {datetime.datetime.now(datetime.timezone.utc).isoformat()} par l'auditeur B"]
for n in ["blind_metrics.csv", "blind_selection.csv", "b04_ranks_blind.csv", "b03_r1.csv", "b03_r3.csv", "b02_stats.jsonl", "blind_ambiguites.md", "b01_peak.py", "b02_parse.py", "b03_metrics.py", "b04_blind_out.py"]:
    L.append(f"{hashlib.sha256((H / n).read_bytes()).hexdigest()}  {n}")
S.write_text("\n".join(L) + "\n")
print(S.read_text())
