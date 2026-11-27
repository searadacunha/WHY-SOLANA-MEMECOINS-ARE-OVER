"""Relit sur la chaîne chaque référence citée dans FINDINGS.md. Réseau requis (RPC public, Helius pour Solana) ; le cache brut est réutilisé.
EVM (0x + 64 hex) : reçu au statut 0x1, sinon doit être un orderId présent dans evidence/dln_orders_evm.csv.
Solana (base58, 80 à 90 caractères) : transaction trouvée, sans erreur. Sortie : ../evidence/s98_refs_check.csv ; code 1 si une référence échoue."""
import csv, re, sys
sys.path.insert(0, ".")
import ev_lib as E
txt = open("../FINDINGS.md").read()
evm = sorted(set(re.findall(r"0x[0-9a-f]{64}(?![0-9a-f])", txt)))
sol = sorted(set(m for m in re.findall(r"(?<![1-9A-HJ-NP-Za-km-z])[1-9A-HJ-NP-Za-km-z]{80,90}(?![1-9A-HJ-NP-Za-km-z])", txt)))
oids = {r["orderId"] for r in csv.DictReader(open("../evidence/dln_orders_evm.csv"))}
rows, bad = [], 0
for h in evm:
    r = E.rpc("eth_getTransactionReceipt", [h]) if h not in oids else None
    st = "orderId décodé" if h in oids else ("ok" if r and r.get("status") == "0x1" else "ÉCHEC")
    bad += st == "ÉCHEC"; rows.append(dict(chain="ethereum", ref=h, status=st, block=int(r["blockNumber"], 16) if r else ""))
if sol:
    import sol_lib as S
    for s in sol:
        t = S.tx(s)
        st = "ok" if t and t["meta"]["err"] is None else "ÉCHEC"
        bad += st == "ÉCHEC"; rows.append(dict(chain="solana", ref=s, status=st, block=t["slot"] if t else ""))
with open("../evidence/s98_refs_check.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(evm), "références Ethereum,", len(sol), "signatures Solana,", bad, "échec(s)")
sys.exit(1 if bad else 0)
