#!/usr/bin/env python3
"""Table et tests de l'étude de groupe. usage: ana_grp.py table | tests. Verdict et texte fixés par le plan."""
import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from graphe import measures  # noqa: E402
from registre import enregistrer  # noqa: E402

ETUDE = str(HERE.parent)
DMAGA = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
K_MIN = 59
M = ["G1", "G2", "G3"]
FIVE_M = 5 * 10**12


def rank_p(target: float, controls: list[float]) -> float:
    if target != target:
        raise ValueError("mesure indéfinie sur la cible")
    vals = [c for c in controls if c == c]
    return (1 + sum(c >= target for c in vals)) / (len(vals) + 1)


def holm(ps: dict[str, float], alpha: float = 0.05) -> dict[str, bool]:
    out, still = {}, True
    for i, k in enumerate(sorted(ps, key=ps.get)):
        still = still and ps[k] <= alpha / (len(ps) - i)
        out[k] = still
    return out


def verdict(ps: dict[str, float], k: int) -> str:
    if k < K_MIN:
        return f"INCONCLUSIF (collecte) : {k} comparateurs, il en faut {K_MIN}"
    hits = [m for m in M if holm(ps)[m]]
    if not hits:
        return "AUCUNE MESURE NE SORT DES PAIRS. Le test ne détecte qu'un DMAGA au-dessus de tous ses pairs, il n'exclut donc pas une organisation réelle."
    return (f"ORGANISATION INHABITUELLE SUR {', '.join(hits)}. Ceci décrit un écart à des tokens de juillet 2024 à pic tardif, sur des mesures "
            "choisies après avoir vu DMAGA. Ce n'est la preuve ni d'un propriétaire unique, ni d'une connaissance préalable, ni d'un acte illégal.")


def table_rows(lines):
    for line in lines:
        r = json.loads(line)
        base = {"pool": r["pool"], "couverture": r["couverture"], "courbe_tronquee": r["courbe_tronquee"], "ata_tronque": r["ata_tronque"],
                "ata_vides": r["ata_vides"], "extension_plafonnee": r["extension_plafonnee"], "ambigu": r["ambigu"], "nouveaux": r["nouveaux"], "n_aretes": len(r["aretes"])}
        ok = r["couverture"] >= 15
        for name, kw in (("principal", {}), ("V1_5M", {"min_raw": FIVE_M}), ("V2_sans_retrait", {"hub": None})):
            g = measures(r["aretes"], r["soldes"], **kw)
            for m in M:
                base[f"{name}_{m}"] = g[m] if ok else float("nan")
            if name == "principal":
                base["services_retires"] = g["services_retires"]
        yield base


def tests(rows: list[dict]) -> dict:
    target = next(r for r in rows if r["pool"] == DMAGA)
    peers = [r for r in rows if r["pool"] != DMAGA]
    out = {"k_collectes": len(peers), "nan": sum(float(r["principal_G1"]) != float(r["principal_G1"]) for r in peers), "variantes": {}, "compteurs": {}}
    for c in ("courbe_tronquee", "extension_plafonnee"):
        out["compteurs"][c] = sum(r[c] == "True" for r in peers)
    for c in ("ata_tronque", "ata_vides", "ambigu", "services_retires"):
        out["compteurs"][c] = sum(int(r[c]) for r in peers)
    for name in ("principal", "V1_5M", "V2_sans_retrait"):
        block = {}
        for m in M:
            vals = [float(r[f"{name}_{m}"]) for r in peers]
            ok = sorted(v for v in vals if v == v)
            t = float(target[f"{name}_{m}"])
            block[m] = {"dmaga": t, "mediane_pairs": ok[len(ok) // 2], "max_pairs": ok[-1], "part_pairs_a_zero": sum(v == 0 for v in ok) / len(ok),
                        "pairs_au_dessus_ou_egaux": sum(v >= t for v in ok), "centile": sum(v < t for v in ok) / len(ok), "k": len(ok), "p": rank_p(t, vals)}
        out["variantes"][name] = block
    prim = out["variantes"]["principal"]
    ps = {m: prim[m]["p"] for m in M}
    k = min(prim[m]["k"] for m in M)
    out["holm"] = holm(ps)
    out["verdict"] = verdict(ps, k)
    return out


def main():
    d = Path(ETUDE)
    if sys.argv[1] == "table":
        rows = list(table_rows((d / "derived" / "par_token.jsonl").read_text().splitlines()))
        with (d / "derived" / "table.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(len(rows), "tokens")
    else:
        rows = list(csv.DictReader((d / "derived" / "table.csv").open()))
        res = tests(rows)
        (d / "tables").mkdir(exist_ok=True)
        (d / "tables" / "tests.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        (d / "tables" / "verdict.json").write_text(json.dumps({"verdict": res["verdict"]}, ensure_ascii=False))
        for m in M:
            v = res["variantes"]["principal"][m]
            enregistrer(ETUDE, test=f"primary_{m}", declare=True, n=v["k"], agent="analyse-principale", stat=v["dmaga"], p=v["p"], sortie="tables/tests.json")
        for name in ("V1_5M", "V2_sans_retrait"):
            enregistrer(ETUDE, test=f"variante_{name}", declare=True, n=res["k_collectes"], agent="analyse-principale", n_comparaisons=3, sortie="tables/tests.json")
        print(json.dumps({k: res[k] for k in ("k_collectes", "nan", "compteurs", "holm", "verdict")}, ensure_ascii=False, indent=0))
        print(json.dumps(res["variantes"]["principal"], ensure_ascii=False))
        assert not any(math.isnan(v["p"]) for v in res["variantes"]["principal"].values())


if __name__ == "__main__":
    main()
