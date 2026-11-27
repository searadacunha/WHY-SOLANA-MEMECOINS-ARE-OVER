import sys
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse
hits = {d for t in history("Ej5Qv3UBQYTuX1dnJ5Fvgx8H9JUSZ6zWgqyDhPzPCwgA") for k, a, m, s, d, r, dc in parse(t)["moves"] if a == "DMAGA" and s.startswith("Ej5Qv3UB")}
assert len(hits) == 1, hits
print(hits.pop())
