# Correction de `blind_seeds.md`, écrite après le sceau

Le fichier scellé n'est pas modifié.

- `blind_seeds.md` écrit que `C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN` reçoit « 15 versements d'exactement 1 M ». Relecture (`c22_hub.py`, `c65_checks.py`) : 13 versements d'environ 1 M par 11 wallets, plus un versement fractionné en 0,005 M et 0,995 M, 14,0005 M au total. Raison : compte fait de mémoire sur une sortie tronquée. Le classement en compte de mise en commun ne change pas.
- `blind_seeds.md` donne une liste d'exclusions sans compter les limites de `c26_continuity.py` après correction : voir `AUDIT_C_ATTRIBUTION.md`, constat C-13.
