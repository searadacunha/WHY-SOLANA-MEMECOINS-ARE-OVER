import gzip,json,collections,time
from dmaga.labels import label
A="H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi"
o=collections.Counter();i=collections.Counter();n=0
for l in gzip.open(f"/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/{A}.jsonl.gz","rt"):
    t=json.loads(l);n+=1
    seq=list(t['transaction']['message']['instructions'])
    for g in t['meta'].get('innerInstructions') or []: seq+=g['instructions']
    for x in seq:
        p=x.get('parsed')
        if x.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer':
            if p['info']['source']==A: o[p['info']['destination']]+=int(p['info']['lamports'])
            if p['info']['destination']==A: i[p['info']['source']]+=int(p['info']['lamports'])
print('n',n,'sorties',[(k[:10],label(k),round(v/1e9,1)) for k,v in o.most_common(8)]);print('entrees',[(k[:10],label(k),round(v/1e9,1)) for k,v in i.most_common(5)])
