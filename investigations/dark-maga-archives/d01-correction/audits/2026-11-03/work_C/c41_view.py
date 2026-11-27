#!/usr/bin/env python3
"""Bilan du groupe depuis members_table.csv : soldes, ventes, premiers achats, financeurs."""
import csv, json
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
g=json.load(open(REPO+'data/prevent_groups.json'))[0]; M=set(g['members'])
gs=json.load(open(REPO+'data/group_split.json'))
rows={r['wallet']:r for r in csv.DictReader(open(ROOT+'members_table.csv'))}
def f(r,k): return float(r[k] or 0)
print('absents',[m for m in M if m not in rows],'incomplets',[m[:8] for m in M if rows[m]['complete']!='True'])
tot={k:sum(f(rows[m],k) for m in M) for k in ('held_T0h','held_Tlow','held_Thigh','held_T24','buy1h_tokens','buy1h_sol','sell24_tokens','sell24_sol','sell24_usdc','xferout24_tokens','xferin24_tokens','buys_total_tokens','buys_total_sol','sells_total_tokens','sells_total_sol','xfer_in_total','xfer_out_total')}
print({k:round(v,3) for k,v in tot.items()})
print('acheteurs 1h',sum(1 for m in M if f(rows[m],'buy1h_n')>0),[m[:6] for m in M if f(rows[m],'buy1h_n')>0])
print('trades winig-high',[(m[:6],rows[m]['trades_winig_high']) for m in M if int(rows[m]['trades_winig_high'])>0])
ws={m:f(rows[m],'held_Tlow') for m in M}
for s in sorted(M,key=lambda m:-ws[m]): print(s[:10],round(ws[s],3),'T24',round(f(rows[s],'held_T24'),2),'sell24',round(f(rows[s],'sell24_tokens'),2),round(f(rows[s],'sell24_sol'),1),'out24',round(f(rows[s],'xferout24_tokens'),2),'in24',round(f(rows[s],'xferin24_tokens'),2),'ff',rows[s]['first_funder'][:8],rows[s]['first_funder_sol'][:5],rows[s]['n_tx'])
ff=[rows[m]['first_funder'] for m in M]
print('premier financeur dans groupe',sum(1 for x in ff if x in M),'G41',sum(1 for x in ff if x.startswith('G41vRrsH')),'none',sum(1 for x in ff if not x))
small=[m for s in gs['ponts_faibles'] if s['M']==15.0 for m in s['members']]
print('4 wallets',[m[:8] for m in small],round(sum(ws[m] for m in small),3),'29',round(sum(ws[m] for m in M if m not in small),3))
