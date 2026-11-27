#!/usr/bin/env python3
"""Cherche des clés Helius dans des historiques git et des fichiers. N'écrit JAMAIS une clé : uniquement sha256[:8].

usage: scan_keys.py <sortie.tsv> git <dépôt>... | files <dossier ou fichier>...
Une valeur UUID est comptée si son empreinte complète est connue (pool ou fichier de service), ou si son contexte immédiat
parle de Helius ou d'api-key. shortcut: UUID nus sans contexte et inconnus ignorés, sinon tout identifiant de session ressortirait.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path

UUID = re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
CTX = re.compile(rb"(helius|api[-_]?key)", re.I)
MAX_BLOB = int(os.environ.get("SCAN_MAX_BLOB_MB", "20")) << 20
MAX_FILE = int(os.environ.get("SCAN_MAX_FILE_MB", "0")) << 20  # 0 = pas de limite
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"} if os.environ.get("SCAN_SKIP_DIRS") else set()
SKIP_EXT = (".mp4", ".mov", ".mkv", ".m4a", ".mp3", ".wav", ".png", ".jpg", ".jpeg", ".webp", ".zip", ".parquet", ".duckdb", ".bin", ".uasset", ".dmg", ".iso")
CHUNK = 8 << 20
HOME = Path.home()


def fp(k: bytes) -> str:
    return hashlib.sha256(k).hexdigest()


def known() -> dict[str, str]:
    """empreinte complète -> classe, lu en local, aucune clé utilisée sur le réseau."""
    cfg = json.loads((HOME / ".config/forensics_v2/helius_sources.json").read_text())
    pool_short = set(cfg["pool_fingerprints"])
    out: dict[str, str] = {}
    for src in cfg["sources"]:
        p = Path(src["path"]).expanduser()
        if p.exists():
            for k in UUID.findall(p.read_bytes()):
                if fp(k)[:8] in pool_short:
                    out[fp(k)] = "pool"
    assert sum(v == "pool" for v in out.values()) == len(pool_short), "pool incomplet"
    for name in ("Downloads/.env", "Downloads/.env.local", "Downloads/.env.bak-vierge", "Downloads/.env.bak_1782725977", ".robinhood_bot.env", ".env", ".env.backup", ".hermes/.env"):
        p = HOME / name
        if p.exists():
            for line in p.read_bytes().splitlines():
                if re.search(rb"helius", line, re.I):
                    for k in UUID.findall(line):
                        out.setdefault(fp(k), "service")
    return out


KNOWN = known()


def hits(buf: bytes):
    """(empreinte8, classe, contexte) pour chaque UUID retenu, sans garder la valeur."""
    res = []
    for m in UUID.finditer(buf):
        f = fp(m.group())
        cls = KNOWN.get(f)
        before = buf[max(0, m.start() - 160): m.start()]
        ctx = bool(CTX.search(before))
        if cls or ctx:
            res.append((f[:8], cls or "inconnue", "contexte" if ctx else "nue"))
    return res


def write(out, *cols):
    out.write("\t".join(str(c) for c in cols) + "\n")
    out.flush()


def scan_git(repo: str, out) -> dict:
    base = ["git", "-C", repo]
    chk = subprocess.Popen(base + ["cat-file", "--batch-all-objects", "--unordered", "--batch-check=%(objectname) %(objecttype) %(objectsize)"], stdout=subprocess.PIPE, text=True)
    n = skipped = found = 0
    wanted = []
    for line in chk.stdout:
        sha_, typ, size = line.split()
        if typ not in ("blob", "commit"):
            continue
        if int(size) > MAX_BLOB:
            skipped += 1
            continue
        wanted.append(sha_)
    chk.wait()
    if chk.returncode:
        raise RuntimeError(f"cat-file {repo} code {chk.returncode}")
    bat = subprocess.Popen(base + ["cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for sha_ in wanted:
        bat.stdin.write(sha_.encode() + b"\n")
        bat.stdin.flush()
        hdr = bat.stdout.readline().split()
        size = int(hdr[2])
        data = bat.stdout.read(size)
        bat.stdout.read(1)
        n += 1
        hs = hits(data)
        if hs:
            uniq = sorted(set(hs))
            log = subprocess.run(base + ["log", "--all", "--format=%h %cI", "--find-object=" + sha_], capture_output=True, text=True).stdout.splitlines()
            names = subprocess.run(base + ["log", "--all", "--format=", "--name-only", "--find-object=" + sha_], capture_output=True, text=True).stdout.split("\n")
            path = next((x for x in names if x), "?")
            reach = "atteignable" if log else "non_atteignable"
            for f8, cls, ctx in uniq:
                write(out, "git", repo.replace(str(HOME), "~"), path, f8, cls, ctx, reach, log[-1].split()[0] if log else "-", log[-1].split()[1][:10] if log else "-", len(log))
                found += 1
    bat.stdin.close()
    bat.wait()
    return {"objets": n, "trop_gros": skipped, "lignes": found}


def scan_stream(label: str, f, out, seen: set) -> int:
    tail = b""
    found = 0
    while True:
        b = f.read(CHUNK)
        if not b:
            break
        buf = tail + b
        for f8, cls, ctx in hits(buf):
            k = (label, f8, ctx)
            if k not in seen:
                seen.add(k)
                write(out, "fichier", label.replace(str(HOME), "~"), "-", f8, cls, ctx, "-", "-", "-", "-")
                found += 1
        tail = buf[-200:]
    return found


def walk(p: Path):
    for d, ds, fs in os.walk(p):
        ds[:] = [x for x in ds if x not in SKIP_DIRS]
        for x in fs:
            yield Path(d) / x


def scan_files(root: str, out) -> dict:
    n = found = errs = 0
    seen: set = set()
    p = Path(root)
    files = [p] if p.is_file() else walk(p)
    for q in files:
        if q.name.startswith("._") or q.is_symlink() or not q.is_file():
            continue
        if MAX_FILE and (q.stat().st_size > MAX_FILE or q.suffix.lower() in SKIP_EXT):
            continue
        try:
            n += 1
            if q.name.endswith(".tar.gz"):
                with tarfile.open(q) as t:
                    for m in t:
                        if m.isfile():
                            found += scan_stream(f"{q}!{m.name}", t.extractfile(m), out, seen)
            else:
                with q.open("rb") as f:
                    found += scan_stream(str(q), f, out, seen)
        except (OSError, tarfile.TarError, EOFError):  # archive tronquée ou mal nommée : comptée, le scan continue
            errs += 1
    return {"fichiers": n, "illisibles": errs, "lignes": found}


def main():
    dest, mode, *targets = sys.argv[1:]
    with open(dest, "a") as out:
        for t in targets:
            r = scan_git(t, out) if mode == "git" else scan_files(t, out)
            print(t.replace(str(HOME), "~"), r, flush=True)


if __name__ == "__main__":
    main()
