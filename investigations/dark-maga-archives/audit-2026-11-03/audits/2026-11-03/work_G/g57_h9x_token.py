#!/usr/bin/env python3
"""H9Xezqfd : réception de DMAGA sur un compte présenté comme dépôt. Le jeton reste-t-il ? Programmes signés par H9Xezqfd, autres jetons, frais, cohérence avec un compte de dépôt. Mêmes questions pour Caw4 et 9W9b. Sortie g57.txt."""
import sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse, MINT
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
sys.stdout = open("audits/2026-11-03/work_G/g57.txt", "w")
for A in ("H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi", "Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME", "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL", "AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1", "By6Dao4QMNeBxmdUrqsoQA8dCGbHz7xWj57CdHV5M47r"):
    n = sg = 0; pr = collections.Counter(); prs = collections.Counter(); dm = []; ot = collections.Counter(); kinds = collections.Counter(); last = None
    for t in history(A):
        x = parse(t); n += 1; last = x["bt"]
        signed = A in x["signers"]; sg += signed
        for p in x["progs"]:
            pr[p[:10]] += 1
            if signed: prs[p[:10]] += 1
        for k, a, m, s, d, r, dc in x["moves"]:
            if a == "DMAGA" and A in (s, d): dm.append((iso(x["bt"]), (s or "")[:8], (d or "")[:8], r / 1e6, x["sig"]))
            if a == "other" and A in (s, d): ot["in" if d == A else "out"] += 1
    print(A[:10], "tx", n, "signées", sg, "dernière", iso(last), "programmes signés", prs.most_common(6), "programmes non signés", [(k, v - prs[k]) for k, v in pr.most_common(6) if v - prs[k] > 0][:6], "autres jetons", dict(ot))
    print("   DMAGA", dm[:8])
