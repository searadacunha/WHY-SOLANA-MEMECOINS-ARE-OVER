#!/usr/bin/env python3
"""Read-only Git, README and frozen-protocol checks. Never fetches or publishes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = "state/publication_baselines.json"


def git(*args):
    result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                            text=True, check=False)
    if result.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def commit(ref):
    # An absent object, including a shallow-clone omission, is an error.
    return git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")


def require_ancestor(older, newer, label):
    result = subprocess.run(["git", "-C", str(ROOT), "merge-base",
                             "--is-ancestor", older, newer], capture_output=True,
                            text=True, check=False)
    if result.returncode:
        raise ValueError(f"{label} {older} must be an ancestor of candidate {newer}")


def preserved(path, baseline, expected_blob=None):
    original = git("ls-tree", baseline, "--", path).split(maxsplit=3)
    if len(original) != 4 or original[1] != "blob":
        raise ValueError(f"Missing baseline file: {path}")
    if expected_blob is not None and original[2] != expected_blob:
        raise ValueError(f"Policy does not match the baseline README: {path}")
    current = git("ls-tree", "HEAD", "--", path).split(maxsplit=3)
    if current[:3] != original[:3]:
        raise ValueError(f"Committed file changed or deleted: {path}")
    staged = git("ls-files", "--stage", "--", path).split(maxsplit=3)
    if len(staged) != 4 or staged[:3] != [original[0], original[2], "0"]:
        raise ValueError(f"Index file changed, deleted or conflicted: {path}")
    file = ROOT / path
    components = [file, *file.parents]
    if any(part.is_symlink() for part in components if part != ROOT) or not file.is_file():
        raise ValueError(f"Missing or substituted working file: {path}")
    data = file.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != original[2]:
        raise ValueError(f"Working file changed: {path}")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True,
                        choices=("main", "audit-2026-11-03"))
    parser.add_argument("--target-ref", help="Fetched target ref or CI event base SHA; "
                        "defaults to refs/remotes/origin/<target>")
    args = parser.parse_args()
    try:
        if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
            raise ValueError("The guard must be inside the repository being checked")
        target = commit(args.target_ref or f"refs/remotes/origin/{args.target}")
        head = commit("HEAD")
        require_ancestor(target, head, "Fetched target")
        # The candidate cannot approve its own README or remove a protocol lock.
        # Read the policy accepted at the destination and preserve it in HEAD,
        # the index and the working tree, just like the files it protects.
        policy = json.loads(preserved(POLICY_PATH, target))
        if policy["version"] != 1:
            raise ValueError("Unsupported publication policy version")
        rule = policy["targets"][args.target]
        for key in ("baseline_commit", "readme_blob"):
            if not re.fullmatch(r"[0-9a-f]{40}", rule[key]):
                raise ValueError(f"{key} must be a pinned full Git SHA-1")
        locks = rule["protocol_locks"]
        if (not isinstance(locks, list) or not locks
                or any(not isinstance(name, str) for name in locks)):
            raise ValueError("A frozen-protocol list is required")
        baseline = commit(rule["baseline_commit"])
        require_ancestor(baseline, target, "Required correction")
        require_ancestor(baseline, head, "Required correction")
        preserved("README.md", baseline, rule["readme_blob"])

        frozen_count = 0
        for name in locks:
            lock = json.loads(preserved(name, baseline))
            if not lock["fichiers"]:
                raise ValueError(f"Empty frozen-file list: {name}")
            for relative, checksum in lock["fichiers"].items():
                file = (ROOT / name).parent / relative
                # Keep the declared Git path: resolving links can hide substitution.
                path = Path(os.path.abspath(file)).relative_to(ROOT).as_posix()
                data = preserved(path, baseline)
                if hashlib.sha256(data).hexdigest() != checksum:
                    raise ValueError(f"Frozen checksum mismatch: {path}")
                frozen_count += 1
        print(f"PASS target={args.target} candidate={head}; README unchanged; "
              f"{frozen_count} frozen files preserved. No server protection implied.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"PUBLICATION CHECK FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
