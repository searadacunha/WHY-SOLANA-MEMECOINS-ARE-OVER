#!/usr/bin/env python3
"""Lance une commande détachée de la session Claude, avec caffeinate lié au PID.

Un simple nohup meurt avec la session (voir la mémoire piege-processus-enfant-de-session).
usage: detach.py <fichier_log> -- <commande...>
"""
import subprocess
import sys

sep = sys.argv.index("--")
log = open(sys.argv[1], "a")
cmd = sys.argv[sep + 1:]
p = subprocess.Popen(cmd, start_new_session=True, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
subprocess.Popen(["caffeinate", "-is", "-w", str(p.pid)], start_new_session=True,
                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(p.pid)
