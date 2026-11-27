#!/usr/bin/env python3
"""Comptabilite du groupe avant Musk par post-soldes et par flux, avec et sans transferts internes ; trades des ensembles elargis pendant la fenetre visuel-bascule ; gagnants ; 13 destinataires G41v. Sortie c58.out, accounting_Tlow.csv"""
import csv, gzip, json, os, time, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[2]
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
MINT="7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"; T0=1720922725; TW=1721577749; TL=1721588607; TH=1721590213
BASE={"ComputeBudget111111111111111111111111111111","TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA","ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL","11111111111111111111111111111111","MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr","Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo","TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb","DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ","HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx","L2TExMFKdjpN9kozasaurPirfHy9P8sbXoAN1qA3S95"}
M=set(json.load(open(REPO/'data/prevent_groups.json'))[0]['members'])
SER={r['wallet'] for r in csv.DictReader(open(ROOT/'cb_series.csv'))}
SEND={r['sender'] for r in csv.DictReader(open(ROOT/'9W9b3z_senders.csv'))}
G13=[r['recipient'] for r in csv.DictReader(open(ROOT/'g41v_recipients.csv'))]
W=sorted(M|SER|SEND|set(G13)|{'H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc','GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra','9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq'})
acc=[]
win=collections.defaultdict(list)
tot=collections.defaultdict(lambda:[0,0.0,0,0.0,0,0,0])
for a in W:
    p=NET+a+'.jsonl.gz'
    if not os.path.exists(p): continue
    buy=sell=xi=xe=oi=oe=0
    for l in gzip.open(p,'rt'):
        t=json.loads(l); bt=t['blockTime']; me=t['meta']; m=t['transaction']['message']
        keys=[k['pubkey'] for k in m['accountKeys']]
        seq=list(m['instructions'])
        for g in me.get('innerInstructions') or []: seq+=g['instructions']
        nonb={i['programId'] for i in seq}-BASE
        own={};d=0
        for s,n in ((-1,'preTokenBalances'),(1,'postTokenBalances')):
            for b in me.get(n) or []:
                if b['mint']==MINT:
                    own[keys[b['accountIndex']]]=b.get('owner')
                    if b.get('owner')==a: d+=s*int(b['uiTokenAmount']['amount'])
        fee=me['fee'] if keys[0]==a else 0
        i0=keys.index(a) if a in keys else None
        nat=(me['postBalances'][i0]-me['preBalances'][i0]+fee) if i0 is not None else 0
        if d and nonb:
            tot[a][0]+=max(d,0); tot[a][1]+=-nat/1e9 if d>0 else 0
            tot[a][2]+=max(-d,0); tot[a][3]+=nat/1e9 if d<0 else 0
            if TW<=bt<=TH: win[a].append((time.strftime('%H:%M:%S',time.gmtime(bt)),round(d/1e12,3),t['transaction']['signatures'][0]))
        if bt<TL:
            if d>0 and nonb: buy+=d
            elif d<0 and nonb: sell+=-d
            elif not nonb and d:
                for i in seq:
                    q=i.get('parsed')
                    if i.get('program')=='spl-token' and isinstance(q,dict) and q.get('type') in('transfer','transferChecked'):
                        inf=q['info']; so,de=own.get(inf['source']),own.get(inf['destination'])
                        am=int(inf.get('amount') or inf['tokenAmount']['amount'])
                        if de==a and so!=a: 
                            if so in M: xi+=am
                            else: xe+=am
                        if so==a and de!=a:
                            if de in M: oi+=am
                            else: oe+=am
    acc.append((a,buy,sell,xi,xe,oi,oe))
wc=csv.writer(open(ROOT/'accounting_Tlow.csv','w',newline='')); wc.writerow('wallet in33 buys sells xfer_in_internal xfer_in_external xfer_out_internal xfer_out_external net'.split())
S=collections.Counter()
for a,b,s,xi,xe,oi,oe in acc:
    wc.writerow([a,a in M,b/1e12,s/1e12,xi/1e12,xe/1e12,oi/1e12,oe/1e12,(b-s+xi+xe-oi-oe)/1e12])
    if a in M:
        S['buys']+=b;S['sells']+=s;S['xi']+=xi;S['xe']+=xe;S['oi']+=oi;S['oe']+=oe
print('33 avant T_LOW (M): achats',S['buys']/1e12,'ventes',S['sells']/1e12,'transferts internes in',S['xi']/1e12,'out',S['oi']/1e12,'externes in',S['xe']/1e12,'out',S['oe']/1e12,'net',(S['buys']-S['sells']+S['xi']+S['xe']-S['oi']-S['oe'])/1e12)
print('somme naive achats+recus internes',(S['buys']+S['xi'])/1e12)
print('trades fenetre visuel-bascule, ensembles elargis',{a[:8]:(v,'33' if a in M else ('serie' if a in SER else 'exp9W')) for a,v in win.items()})
for a in ('H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc','GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra','9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq'):
    print(a[:8],'achats M',tot[a][0]/1e12,'SOL',round(tot[a][1],2),'ventes M',tot[a][2]/1e12,'SOL',round(tot[a][3],2),[r for r in csv.DictReader(open(ROOT/'cb_window.csv')) if r['dest']==a][:2])
print('G13 achats',[(a[:6],round(tot[a][0]/1e12,2)) for a in G13])
print('reduction 33 si on retire 7mdCAs et 9u5JKg',[r for r in acc if r[0].startswith(('7mdCAs','9u5JKg'))])
