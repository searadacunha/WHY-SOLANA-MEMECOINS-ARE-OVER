#!/bin/zsh
# Python du projet : interpréteur système + bibliothèques sur le disque USB direct (FAT32, sans liens).
export PYTHONPATH="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/pylib:$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
exec /opt/homebrew/bin/python3.12 "$@"
