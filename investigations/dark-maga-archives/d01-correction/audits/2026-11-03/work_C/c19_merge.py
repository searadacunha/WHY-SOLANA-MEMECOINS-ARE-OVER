#!/usr/bin/env python3
"""Fusionne les transferts >= seuil : brut (cand_edges) + transactions absentes telechargees. Sortie direct_edges_all.csv :
une ligne par transfert inter-proprietaires dans une tx qui ne contient que les programmes de base (propre),
puis classement des autres dans mediated_edges.csv avec le programme mediateur."""
import csv, gzip, json, time, collections, sys
BASE={'ComputeBudget111111111111111111111111111111','TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA','ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL','11111111111111111111111111111111','MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr','Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo','TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb','L2TExMFKdjpN9kozasaurPirfHy9P8sbXoAN1qA3S95','DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ'}
MINT="7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net"
TH=1_000_000_000_000
cols="sig utc slot txidx src dst amount authority payer signers programs clean origin kind".split()
wa=csv.writer(open('direct_edges_all.csv','w',newline='')); wa.writerow(cols)
wm=csv.writer(open('mediated_edges.csv','w',newline='')); wm.writerow(cols)
na=nm=0
for r in csv.DictReader(open('cand_edges_1M.csv')):
    ps=set(r['programs'].split('|'))
    # top-level : instruction SPL externe, signee par la source, sans AMM dans la tx (HQ2UUt, 4MNPdK = etiquettes sans comptes)
    top=r['outer_prog'] in ('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA','TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb')
    clean=(not (ps-BASE)) or (top and r['has_amm']=='False' and r['authority']==r['src'])
    row=[r['sig'],r['utc'],r['slot'],r['txidx'],r['src'],r['dst'],r['amount'],r['authority'],r['payer'],r['signers'],r['programs'],clean,'raw',r['kind']]
    if clean: wa.writerow(row); na+=1
    elif r['has_amm']=='False': wm.writerow(row); nm+=1
nabs=nabs_clean=0
for line in gzip.open(f"{NET}/absent_1M.jsonl.gz","rt"):
    t=json.loads(line)
    m=t['transaction']['message']; me=t['meta']
    keys=[k['pubkey'] for k in m['accountKeys']]
    own={}
    for s in ('preTokenBalances','postTokenBalances'):
        for b in me.get(s) or []:
            if b['mint']==MINT: own[keys[b['accountIndex']]]=b['owner']
    seq=[(i,-1,x) for i,x in enumerate(m['instructions'])]
    progs=[x['programId'] for x in m['instructions']]
    for g in me.get('innerInstructions') or []:
        for j,x in enumerate(g['instructions']):
            seq.append((g['index'],j,x)); progs.append(x['programId'])
    ps=list(dict.fromkeys(progs))
    clean=not (set(ps)-BASE)
    signers=[k['pubkey'] for k in m['accountKeys'] if k['signer']]
    for i,j,x in seq:
        p=x.get('parsed')
        if x.get('program')!='spl-token' or not isinstance(p,dict) or p.get('type') not in('transfer','transferChecked'): continue
        inf=p['info']; s,d=inf['source'],inf['destination']
        if s not in own and d not in own: continue
        amt=int(inf.get('amount') or inf['tokenAmount']['amount'])
        if amt<TH: continue
        so,dd=own.get(s,''),own.get(d,'')
        if so==dd: continue
        top=(j==-1)
        clean2=clean or (top and (inf.get('authority') or inf.get('multisigAuthority'))==so)
        row=[t['transaction']['signatures'][0],time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t['blockTime'])),t['slot'],t.get('transactionIndex'),so,dd,amt,inf.get('authority') or inf.get('multisigAuthority'),signers[0],'|'.join(signers),'|'.join(ps),clean2,'net_absent',p['type']]
        nabs+=1
        if clean2: wa.writerow(row); nabs_clean+=1
        else: wm.writerow(row)
print('propres brut',na,'mediees brut',nm,'absentes',nabs,'absentes propres',nabs_clean)
