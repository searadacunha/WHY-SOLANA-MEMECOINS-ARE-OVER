#!/usr/bin/env python3
"""Restore a sanitized branch or commit into a new directory, using the archive."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
def records(name):
    return [json.loads(line) for line in (HERE / name).read_text().splitlines() if line]
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ref", help="source commit SHA or source ref (e.g. heads/main)")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit("Destination must be empty")
    refs = {r["ref"]: r["commit"] for r in json.loads((HERE / "refs.json").read_text())}
    commits = {r["commit"]: r for r in records("commits.jsonl")}
    blobs = {r["blob"]: r for r in records("blobs.jsonl")}
    sha = refs.get(args.ref, args.ref)
    chain = []
    while sha:
        c = commits[sha]
        chain.append(c)
        sha = c["parents"][0] if c["parents"] else None
    files = {}
    for c in reversed(chain):
        for path, mode, obj in c["changes"]:
            if mode == "000000":
                files.pop(path, None)
            else:
                files[path] = (mode, obj)
    destination.mkdir(parents=True, exist_ok=True)
    omitted = []
    for path, (mode, obj) in sorted(files.items()):
        p = (destination / path).resolve()
        if not p.is_relative_to(destination):
            raise ValueError("unsafe source path")
        b = blobs.get(obj)
        if mode == "160000" or not b or b["kind"] == "excluded":
            omitted.append(path)
            continue
        raw = (REPO / b["location"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != b["published_sha256"]:
            raise ValueError("archive integrity mismatch: " + path)
        p.parent.mkdir(parents=True, exist_ok=True)
        # Symlink targets are restored as plain text, never executed.
        p.write_bytes(raw)
        if mode == "100755":
            p.chmod(0o755)
    print(f"Restored {len(files)-len(omitted)} files; {len(omitted)} omitted.")
    if omitted:
        (destination / "ARCHIVE_OMISSIONS.json").write_text(json.dumps(omitted, indent=2))
if __name__ == "__main__":
    main()
