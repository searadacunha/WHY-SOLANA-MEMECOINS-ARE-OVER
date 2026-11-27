"""Structure d'une transaction brute (phase aveugle)."""
import gzip, json
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
p = EXT/"raw/ctrl_tx/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k/p000000.jsonl.gz"
with gzip.open(p,"rt") as f:
    line=f.readline()
print(len(line)); r=json.loads(line); print(type(r), list(r.keys()) if isinstance(r,dict) else len(r))
def show(o,ind=0,maxk=30):
    pad=" "*ind
    if isinstance(o,dict):
        for k,v in list(o.items())[:maxk]:
            if isinstance(v,(dict,list)):
                print(pad+str(k), type(v).__name__, len(v)); show(v,ind+2,maxk)
            else: print(pad+str(k), repr(v)[:100])
    elif isinstance(o,list) and o:
        print(pad+"[0]:", type(o[0]).__name__)
        if isinstance(o[0],(dict,list)): show(o[0],ind+2,maxk)
        else: print(pad, repr(o[0])[:100])
show(r)
