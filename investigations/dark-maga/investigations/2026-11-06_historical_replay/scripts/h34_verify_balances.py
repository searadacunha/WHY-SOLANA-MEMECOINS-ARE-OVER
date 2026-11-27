"""Contrôle primaire des avoirs de h32 par le compte de jetons associé (ATA) de chaque adresse.

Pour chaque adresse : ATA DMAGA dérivée (k12), toutes ses signatures (RPC public), dernière transaction réussie antérieure au
post de Noah, solde de l'ATA lu dans postTokenBalances. Toute transaction qui touche l'ATA y figure, virements `Transfer` simples
compris : c'est ce qui manque à trades.parquet (voir FINDINGS §5). Un écart est écrit, pas masqué.
Limite : un compte de jetons non associé échappe au contrôle. Sortie : data/noah_holdings_verified.csv."""
import csv
from h_lib import DATA, DMAGA, utc
import k16_pubrpc as pub
from k12_ata import ata
from h32_noah import T_NOAH

if __name__ == "__main__":
    hold = [r for r in csv.DictReader((DATA / "noah_holdings.csv").open()) if r["address"] != "TOTAL"]
    out = []
    for r in hold:
        a = r["address"]
        acc = ata(a, DMAGA)
        sigs, trunc = pub.sigs(acc, max_pages=5)
        before = [x for x in sigs if not x.get("err") and x["blockTime"] <= T_NOAH]
        if before:
            last = max(before, key=lambda x: x["slot"])
            t = pub.tx(last["signature"])
            ks = [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]]
            post = sum(int(b["uiTokenAmount"]["amount"]) for b in t["meta"].get("postTokenBalances") or [] if ks[b["accountIndex"]] == acc) / 1e6
            sig, when = last["signature"], utc(last["blockTime"])
        else:
            post, sig, when = 0.0, "", ""
        out.append({**r, "ata": acc, "ata_signatures": len(sigs), "ata_truncated": trunc, "last_ata_tx_before_post": sig, "last_ata_tx_utc": when,
                    "onchain_ata_balance": round(post, 6), "diff_vs_trades": round(post - float(r["dmaga_at_post"]), 6)})
        print(r["group"], a[:8], r["dmaga_at_post"], round(post, 6), out[-1]["diff_vs_trades"], flush=True)
    with (DATA / "noah_holdings_verified.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
