"""Parse the repository's generated table 'Les 1 000 premiers acheteurs, tous venues' (reports/EARLY_BUYERS.md) into CSV.
The repo table mixes number formats (1 323,0 / -42.5 / -1.100.1); normalisation documented in fnum()."""
import re, csv, sys
def fnum(s):
    s = s.strip().replace('\u202f', '').replace('\xa0', '').replace(' ', '')
    if ',' in s: s = s.replace('.', '').replace(',', '.')
    elif s.count('.') > 1:
        head, tail = s.rsplit('.', 1); s = head.replace('.', '') + '.' + tail
    return float(s)
def parse(path):
    L = open(path, encoding='utf-8').read().splitlines()
    i = [k for k, l in enumerate(L) if l.startswith('## Les 1 000')][0]
    rows = []
    for l in L[i:]:
        m = re.match(r'^\| (\d+) \| `(\w+)` \| (\d+) \| ([\d/ :]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|', l)
        if m:
            dd, hh = m.group(4).split(' ')
            rows.append(dict(rank=int(m.group(1)), wallet=m.group(2), slot=int(m.group(3)), utc=f"2024-{dd[3:5]}-{dd[0:2]}T{hh}Z",
                             first_buy_sol=fnum(m.group(5)), first_buy_M=fnum(m.group(6)), bought_sol_total=fnum(m.group(7)),
                             realised_sol=fnum(m.group(8)), residual_M=fnum(m.group(9))))
    return rows
if __name__ == '__main__':
    rows = parse(sys.argv[1]); out = sys.argv[2]
    w = csv.DictWriter(open(out, 'w', newline=''), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows))
