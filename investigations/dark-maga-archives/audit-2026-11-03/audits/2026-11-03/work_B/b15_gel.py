"""Phase 2 : intégrité du gel, dates, chaîne du registre. Sortie : b15_gel.txt."""
import hashlib, json, os, subprocess, datetime as dt
from pathlib import Path
HERE = Path(__file__).parent; ROOT = HERE.parents[2]; ET = ROOT / "etude_final"
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
lock = json.load(open(ET / "PROTOCOL.lock"))
P("gelé le", lock["gele_le_utc"], "commit_head", lock["git"]["commit_head"], "non committés", lock["git"]["fichiers_non_committes"], "immuable", lock["immuable"], "ajouts", [a["t_utc"] for a in lock["ajouts"]])
ok = bad = 0
for f, sha in lock["fichiers"].items():
    q = (ET / f).resolve()
    cur = hashlib.sha256(q.read_bytes()).hexdigest() if q.exists() else None
    if cur == sha: ok += 1
    else:
        bad += 1; P("DIFFERENT", f, sha[:12], (cur or "absent")[:12])
P("empreintes conformes", ok, "différentes", bad)
def mt(p):
    return dt.datetime.fromtimestamp(os.path.getmtime(p), dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
for p in [ET / "analysis_plan.md", ET / "PROTOCOL.lock", ET / "amendements/001-2026-11-03.md", ET / "amendements/002-2026-11-03.md", ET / "derived/metrics.csv", ET / "tables/tests.json", ET / "tables/verdict.json", ET / "tables/funder_share.json", ET / "results.md", ET / "controles/synth.md",
          EXT / "data/controls/selection.jsonl", EXT / "data/controls/swaps_stats.jsonl", EXT / "data/controls/activity.jsonl", EXT / "data/controls/migrations.jsonl"]:
    P("mtime UTC", mt(p), str(p).split("Dark-MAGA-Investigation/")[-1])
for c in ["26cf5c7", "7f6f1c9", "fdb5693"]:
    r = subprocess.run(["git", "-C", str(ROOT), "show", "--stat", "--format=%h %cI %s", c, "--", "etude_final"], capture_output=True, text=True).stdout
    P(r[:1500])
# le dépôt contient-il l'amendement avant les résultats ?
r = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%h %cI", "--", "etude_final/amendements/001-2026-11-03.md"], capture_output=True, text=True).stdout
P("commits de 001 :", r.strip())
r = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%h %cI", "--", "etude_final/derived/metrics.csv"], capture_output=True, text=True).stdout
P("commits de metrics.csv :", r.strip())
# chaîne du registre
prev = "0" * 64
n = 0
for line in open(ET / "registre/tests.jsonl"):
    r = json.loads(line); n += 1
    if r.get("prec") != prev:
        P("rupture de chaîne ligne", n, str(r.get("prec"))[:12], prev[:12])
    prev = hashlib.sha256(line.rstrip("\n").encode()).hexdigest()
P("lignes registre", n, "dernière empreinte recalculée", prev[:16])
tem = Path.home() / ".claude/etudes-gelees/temoins"
if tem.exists():
    for x in sorted(tem.iterdir()):
        if "etude_final" in x.name or "Dark" in x.name or "dmaga" in x.name.lower():
            P("témoin", x.name, x.read_text()[:300])
    P("témoins présents", len(list(tem.iterdir())))
ix = Path.home() / ".claude/etudes-gelees"
P("contenu etudes-gelees :", sorted(y.name for y in ix.iterdir())[:20] if ix.exists() else "absent")
(HERE / "b15_gel.txt").write_text("\n".join(L) + "\n")
