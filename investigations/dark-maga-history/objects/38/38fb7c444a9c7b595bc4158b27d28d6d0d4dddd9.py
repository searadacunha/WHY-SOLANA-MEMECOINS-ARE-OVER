"""Piste OL07 (Dark-MAGA) : les ordres deBridge de 8YSi5yNR vers BSC 0xfb2ec4e5 ont-ils été payés sur BSC ?

Le dépôt (investigations/2026-11-05_debridge_winners/REPRISE.md, point 3) note deux ordres du 20/03/2025 vers
0xfb2ec4e51680198f4d0351d67702d4eebdfa625f, « paiement BSC non vérifié » (stats-api.dln.trade bloqué par Cloudflare
ce jour-là ; accessible le 12/11/2026).

Méthode : ordres par créateur (stats-api.dln.trade), détail de chaque ordre (destinataire, transaction de livraison),
puis reçu BSC de la livraison par RPC public : statut, contrat DlnDestination, identifiant d'ordre présent dans les
journaux. Sorties : resultats/dm_debridge_ol07/{ordres.csv,resume.json}.

Usage : python3 scripts/dm_debridge_ol07.py
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone

from onchain import ROOT, http_json, rpc

CASE = "dm_debridge"
CREATOR = "8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7"   # dépôt Dark-MAGA, UNRESOLVED OL07 (adresse complète)
EXPECTED_RECEIVER = "0xfb2ec4e51680198f4d0351d67702d4eebdfa625f"
BSC_RPCS = ("https://bsc-rpc.publicnode.com", "https://bsc-dataseed.bnbchain.org")
OUT = ROOT / "resultats" / "dm_debridge_ol07"


def sv(x):
    return x.get("stringValue") if isinstance(x, dict) else x


def find(d, *keys):
    """Premier champ trouvé, en profondeur (le schéma de l'API varie selon la version)."""
    stack = [d]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            for k in keys:
                if k in cur and cur[k] not in (None, ""):
                    return sv(cur[k])
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return None


def bsc_receipt(txh: str) -> tuple[dict, str]:
    last = None
    for url in BSC_RPCS:
        try:
            r, _ = rpc(CASE, url, "eth_getTransactionReceipt", [txh], retries=2)
            if r:
                return r, url
        except Exception as exc:  # essayer le nœud suivant, garder l'erreur
            last = exc
    raise RuntimeError(f"reçu BSC introuvable pour {txh}: {last}")


def main() -> None:
    lst, _ = http_json(CASE, "https://stats-api.dln.trade/api/Orders/filteredList", {"skip": 0, "take": 50, "creator": CREATOR})
    orders = lst.get("orders") or []
    assert len(orders) == lst.get("totalCount"), "liste d'ordres incomplète"
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for o in orders:
        oid = sv(o["orderId"])
        det, _ = http_json(CASE, f"https://stats-api.dln.trade/api/Orders/{oid}", pause=0.5)
        give, take = o["giveOfferWithMetadata"], o["takeOfferWithMetadata"]
        row = {"order_id": oid, "cree_utc": datetime.fromtimestamp(o["creationTimestamp"], timezone.utc).isoformat(),
               "etat": o.get("state"), "tx_creation_solana": sv(o.get("createEventTransactionHash")),
               "donne": f"{int(sv(give['amount'])) / 10 ** give['decimals']} {give['symbol']} (chaîne {sv(give['chainId'])})",
               "recoit": f"{int(sv(take['amount'])) / 10 ** take['decimals']} {take['symbol']} (chaîne {sv(take['chainId'])})",
               "destinataire": (find(det, "receiverDst") or "").lower(),
               "tx_livraison": sv(((det.get("fulfilledDstEventMetadata") or {}).get("transactionHash")) or {}),
               "livraison_utc": datetime.fromtimestamp((det.get("fulfilledDstEventMetadata") or {}).get("blockTimeStamp") or 0,
                                                       timezone.utc).isoformat(),
               "taker": sv(det.get("taker") or {}),
               "unlock_authority": sv(o.get("unlockAuthorityDst"))}
        txh = row["tx_livraison"]
        if txh:
            rc, node = bsc_receipt(txh)
            logs = rc.get("logs") or []
            row.update({"bsc_statut": int(rc["status"], 16), "bsc_bloc": int(rc["blockNumber"], 16), "bsc_noeud": node,
                        "bsc_contrats_logs": "|".join(sorted({l["address"].lower() for l in logs})),
                        "order_id_dans_logs": any(oid[2:].lower() in (l.get("data", "") + "".join(l.get("topics", []))).lower()
                                                  for l in logs),
                        "destinataire_attendu": row["destinataire"] == EXPECTED_RECEIVER})
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False))
    with (OUT / "ordres.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
        w.writeheader()
        w.writerows(rows)
    (OUT / "resume.json").write_text(json.dumps({"createur": CREATOR, "ordres": len(rows),
                                                  "livres_verifies_bsc": sum(1 for r in rows if r.get("order_id_dans_logs") and r.get("bsc_statut") == 1)},
                                                 indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
