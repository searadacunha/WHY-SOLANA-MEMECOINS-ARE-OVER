#!/usr/bin/env python3
"""Relit les preuves X legeres, sans reseau : C03, C04, C22, C31, C32, C33. Sortie c54.out"""
import json, re, glob, os, hashlib, time
R='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
def snow(i): return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(((int(i)>>22)+1288834974657)/1000))
# C03
d=json.load(open(R+'evidence/web/profiles/fx_DarkMagaCoin.json')); u=d.get('user',d); print('C03 created',u.get('created_at') or u.get('joined'))
t=open(R+'evidence/web/threadreader_1843704335823454430.txt',errors='replace').read()
for m in re.finditer(r'.{140}(kikisknees|Butler|two days|days later).{160}',t,flags=re.S): print('  thread:',m.group(0).replace('\n',' ')[:300]); break
print('  thread mentionne une date ou un mint ?', bool(re.search(r'7D7B|pump\.fun|mint',t)))
# C04
for f in ['twitter.com_20240721190327.html','twitter.com_20240721205925.html']:
    p=R+'evidence/web/wb_elonmusk/'+f
    if os.path.exists(p):
        s=open(p,errors='replace').read(); print('C04',f,re.findall(r'profile_images/(\d+)/',s)[:2])
print('C04 snowflake nouvelle image',snow(1815105297410666496))
xp=[json.loads(l) for l in open(R+'data/x_posts.jsonl')]
print('x_posts',len(xp),list(xp[0].keys())[:14])
by={str(x.get('id') or x.get('post_id')):x for x in xp}
print('C04 Bailey',snow(1815107030606385507),str(by.get('1815107030606385507'))[:240])
# C22 : adresses publiees par le noyau
core={'darkmagacoin','kikisknees','aristos_revenge','chriswinig'}
b58=re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
import collections
found=collections.Counter(); n=collections.Counter()
for x in xp:
    a=str(x.get('author') or x.get('author_handle') or x.get('screen_name') or '').lower().lstrip('@')
    if a in core:
        n[a]+=1
        for z in b58.findall(str(x.get('text') or x.get('full_text') or '')):
            found[(a,z)]+=1
print('C22 posts du noyau',n,'adresses',found.most_common(12))
rec=[json.loads(l) for l in open(R+'evidence/x_wayback/recovered.jsonl')]
print('recovered',len(rec))
fnd=collections.Counter()
for x in rec:
    for z in b58.findall(str(x.get('text',''))): fnd[z]+=1
print('C22 recovered adresses',fnd.most_common(8))
for i in ('1815054158367432804','1815116229117690314','1815116385414209876'):
    r=[x for x in rec if str(x.get('id'))==i or str(x.get('post_id'))==i or str(x.get('tweet_id'))==i]
    print('C32',i,snow(i),str(r[0])[:360] if r else None)
print('C32 IMG_5658',[ (str(x.get('id')),str(x.get('created_utc_snowflake')),str(x.get('text'))[:160]) for x in xp if 'IMG_5658' in json.dumps(x)][:3])
gg=[l for l in open(R+'docs/SOCIAL_FINDINGS.md') if 'IMG_5658' in l][:2]
print('  doc',[g[:400] for g in gg])
# C33
for acc in ('koreanjewcrypto','kanpai','DarkMagaCoin','kikisknees','pmarca'):
    L=[x for x in xp if str(x.get('author') or x.get('author_handle') or x.get('screen_name') or '').lower().lstrip('@')==acc.lower() and re.search(r'dmaga|dark ?maga',str(x.get('text') or ''),re.I)]
    L.sort(key=lambda x:int(x.get('id') or x.get('post_id')))
    print('C33',acc,len(L),[(snow(x.get('id') or x.get('post_id')),str(x.get('text'))[:70]) for x in L[:2]])
L=[x for x in xp if str(x.get('author') or x.get('author_handle') or x.get('screen_name') or '').lower().lstrip('@')=='pmarca']
print('C33 pmarca posts',len(L),[(snow(x.get('id') or x.get('post_id')),str(x.get('text'))[:80]) for x in L][:5])
