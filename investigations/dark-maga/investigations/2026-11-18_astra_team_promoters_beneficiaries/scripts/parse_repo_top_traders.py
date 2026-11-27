"""Parse reports/TOP_TRADERS.md table '100 plus gros réalisés, coût connu' (repo-generated, avg-cost realised SOL) into CSV."""
import re, csv, sys
sys.path.insert(0, __import__('os').path.dirname(__file__)); from parse_repo_first_buyers import fnum
def parse(path):
    L = open(path, encoding='utf-8').read().splitlines()
    i = [k for k, l in enumerate(L) if l.startswith('## 100 plus gros')][0]
    rows, seen = [], set()
    for l in L[i:]:
        if l.startswith('## ') and not l.startswith('## 100'): break
        c = [x.strip() for x in l.strip('|').split('|')]
        if len(c) >= 13 and re.match(r'^\d+$', c[0]) and c[1].startswith('`'):
            w = c[1].strip('`')
            if w in seen: continue
            seen.add(w)
            rows.append(dict(rank=int(c[0]), wallet=w, realised_sol=fnum(c[2]), net_flow_sol=fnum(c[3]), bought_sol=fnum(c[4]), sold_sol=fnum(c[5]),
                             pnl_usd=c[6], buys_sells=c[7], residual_M=fnum(c[8]), cohort=c[9], first_buy_utc=c[10], last_sell_utc=c[11], completeness=c[12]))
    return rows
if __name__ == '__main__':
    rows = parse(sys.argv[1])
    w = csv.DictWriter(open(sys.argv[2], 'w', newline=''), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows); print(len(rows))
