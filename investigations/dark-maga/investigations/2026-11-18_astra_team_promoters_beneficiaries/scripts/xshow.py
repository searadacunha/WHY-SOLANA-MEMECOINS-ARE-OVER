import json,sys,datetime
def load(f):
    s=open(f).read()
    if '{' not in s: return {}
    return json.JSONDecoder(strict=False).raw_decode(s[s.index('{'):])[0]
if __name__=='__main__':
    d=load(sys.argv[1])
    for p in d.get('data',[]):
        sf=datetime.datetime.fromtimestamp(((int(p['id'])>>22)+1288834974657)/1000,datetime.UTC).strftime('%H:%M:%S')
        print(p['id'],p.get('created_at'),sf,p.get('url','').split('/')[3] if p.get('url') else '',[r['type'] for r in p.get('referenced_tweets',[])],repr(p['text'][:200]))
