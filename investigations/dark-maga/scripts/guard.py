#!/usr/bin/env python3
"""Chien de garde : lance une commande et la tue si elle menace la machine partagée.

Le 03/11, ana_60_clusters.py a monté à 2,3 Go de RSS, le swap à 10 Go, le disque interne à 7,77 Go, sous la pause de PolySentinel.
La mémoire devient du disque sur ce Mac : tout calcul lourd de ce projet passe par ici.
usage: guard.py [--rss-mo 1200] [--disk-go 10.6] [--swap-go 7.5] -- <commande...>
Sort en code 75 si le garde a tué le processus : ce n'est jamais un succès silencieux.
"""
import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import time


def rss_tree_mb(root: int) -> float:
    out = subprocess.run(["ps", "-axo", "pid=,ppid=,rss="], capture_output=True, text=True).stdout
    kids: dict[int, list[int]] = {}
    rss: dict[int, int] = {}
    for line in out.splitlines():
        p = line.split()
        if len(p) == 3:
            pid, ppid, r = map(int, p)
            kids.setdefault(ppid, []).append(pid)
            rss[pid] = r
    total, stack = 0, [root]
    while stack:
        x = stack.pop()
        total += rss.get(x, 0)
        stack += kids.get(x, [])
    return total / 1024


def swap_used_gb() -> float:
    s = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"used = ([\d.]+)M", s)
    return float(m.group(1)) / 1024 if m else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rss-mo", type=float, default=1200)
    ap.add_argument("--disk-go", type=float, default=10.6)
    ap.add_argument("--swap-go", type=float, default=7.5)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    free = shutil.disk_usage("/").free / 1e9
    if free < a.disk_go:
        sys.exit(f"garde : disque interne à {free:.2f} Go, sous {a.disk_go} Go, je ne lance pas {cmd[:3]}")
    p = subprocess.Popen(cmd, start_new_session=True)
    peak = 0.0
    while p.poll() is None:
        time.sleep(2)
        rss = rss_tree_mb(p.pid)
        peak = max(peak, rss)
        free = shutil.disk_usage("/").free / 1e9
        swap = swap_used_gb()
        why = None
        if rss > a.rss_mo:
            why = f"RSS {rss:.0f} Mo > {a.rss_mo:.0f}"
        elif free < a.disk_go:
            why = f"disque {free:.2f} Go < {a.disk_go}"
        elif swap > a.swap_go:
            why = f"swap {swap:.2f} Go > {a.swap_go}"
        if why:
            os.killpg(p.pid, signal.SIGKILL)
            print(f"GARDE : tué {cmd[:3]} ({why}), pic {peak:.0f} Mo", file=sys.stderr, flush=True)
            sys.exit(75)
    print(f"garde : fini, code {p.returncode}, pic {peak:.0f} Mo", file=sys.stderr, flush=True)
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()
