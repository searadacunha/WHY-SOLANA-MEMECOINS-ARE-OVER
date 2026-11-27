#!/usr/bin/env python3
"""Liens de SOL du bloc de 4 et de 7mdCAs, 9u5JKg, C7i9be avec le reste, et createur/G41v/5QhJJc entre eux. Impression."""
import csv, json
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
g=json.load(open(REPO+'data/prevent_groups.json'))[0]; M=set(g['members'])
sol=list(csv.DictReader(open(ROOT+'sol_edges.csv')))
def show(a,minsol=0.005):
    L=[x for x in sol if (x['src'].startswith(a) or x['dst'].startswith(a)) and int(x['lamports'])>=minsol*1e9]
    for x in L: print(' ',x['utc'],x['src'][:8],'>',x['dst'][:8],int(x['lamports'])/1e9,x['sig'][:12],'groupe' if (x['src'] in M and x['dst'] in M) else '')
for a in ['Ei5yGz8d','HGBiExZR','Gcyg2jeL','4wComYHQ','7mdCAs8C','9u5JKgWd','C7i9beNH','35nAuv6j','Akp46Dic','GPMYCuus','NxtXcmEW','AtZjv3Du','74qFhHyp','6t2dz4jm']:
    print(a); show(a)
