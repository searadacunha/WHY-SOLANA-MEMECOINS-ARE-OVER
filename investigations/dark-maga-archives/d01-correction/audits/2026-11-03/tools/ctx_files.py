#!/usr/bin/env python3
"""Contexte masqué d'une empreinte dans les fichiers de key_strict_files.tsv : 45 octets avant, toute valeur UUID ou longue chaîne masquée."""
import csv, hashlib, os, re, sys
U = re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
LONG = re.compile(rb"[A-Za-z0-9_\-]{24,}")
want = set(sys.argv[2:])
done = {}
for r in csv.DictReader(open(sys.argv[1]), delimiter="\t"):
    if r["emp8"] not in want or done.get(r["emp8"], 0) >= 2:
        continue
    p = r["fichier"].replace("~", os.path.expanduser("~"), 1)
    with open(p, "rb") as f:
        tail = b""
        found = False
        while (b := f.read(8 << 20)) and not found:
            buf = tail + b
            for m in U.finditer(buf):
                if hashlib.sha256(m.group()).hexdigest()[:8] == r["emp8"]:
                    ctx = LONG.sub(b"<LONG>", U.sub(b"<UUID>", buf[max(0, m.start() - 45):m.end() + 12]))
                    print(r["emp8"], os.path.basename(p)[:12], repr(ctx)[:150])
                    found = True
                    break
            tail = buf[-200:]
    done[r["emp8"]] = done.get(r["emp8"], 0) + 1
