"""G7 sur le brut : ERMtiLod -> HW5MqvM1, GoPCTrS3 -> HKzkNSH2, ventes, versements, retours, et que voit-on chez ces 2 wallets autour des dates ? Base : population des 3 comptes. Sortie i29_g7.txt."""
import sys,collections,datetime as dt,csv
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i29_g7.txt","w")
iso=lambda t:dt.datetime.fromtimestamp(t,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
ERM="ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH";GOP="GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC"
HW="HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6";HK="HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP";GX="GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"
D={"8N4A":"8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx","42MS":"42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv","9kqT":"9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV"}
for w in (HW,HK):
    print("==",w)
    L=sorted(iter_tx(w),key=lambda t:(t["slot"],t["transactionIndex"]))
    print(" tx",len(L),iso(L[0]["blockTime"]),iso(L[-1]["blockTime"]),"premier signataire",signers(L[0])[:2])
    for t in L:
        td,dec=tok_delta(t);sd=sol_delta(t)
        dm=td.get((w,DMAGA),0)/1e6
        s=sd.get(w,0)/1e9
        dep=[k for k,v in D.items() if v in sd and sd[v]>0]
        wsol=td.get((w,WSOL),0)/1e9
        if abs(dm)>=1000 or dep:
            print("  ",iso(t["blockTime"]),"DMAGA",round(dm,1),"SOL",round(s,3),"WSOL",round(wsol,3),"dépôt",dep,"signe",signers(t)[0][:8],"contre",[o[:8] for (o,m),v in td.items() if m==DMAGA and (v<0)!=(dm<0) and o!=w],t["transaction"]["signatures"][0][:16])
print("\nDépôts GXZ : expéditeurs >= 0,01 SOL")
for tag,a in D.items():
    c=collections.Counter();f={}
    for t in iter_tx(a):
        if not ok(t):continue
        sd=sol_delta(t)
        if sd.get(a,0)>0:
            for k,x in sd.items():
                if x<0 and k!=a:c[k]+=sd[a]/1e9;f[k]=min(f.get(k,t["blockTime"]),t["blockTime"])
    print(tag,[(k[:8],round(v,2),iso(f[k])[:10]) for k,v in c.most_common() if v>=0.01])
# Sortie de chaque compte
for tag,a in D.items():
    c=collections.Counter();n=0
    for t in iter_tx(a):
        if a in signers(t) and ok(t):
            n+=1
            sd=sol_delta(t)
            for k,x in sd.items():
                if x>0 and k!=a:c[k]+=x/1e9
    print(tag,"signées",n,"sorties",[(k[:10],round(v,2)) for k,v in c.most_common(4)])
