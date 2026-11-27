"""Exécution sur Ethereum des ordres vers les 4 receveurs principaux : ETH interne et USDC reçus dans la fenêtre, comparés à take_raw. Puis ce que fait 0xb947 de ses USDC. Blockscout public. Sortie i21_evm_fill.txt."""
import json,urllib.request,time,os,csv,sys,datetime as dt,collections
OUT="audits/2026-11-03/work_I/"
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/net_evm"
sys.stdout=open(OUT+"i21_evm_fill.txt","w")
B="https://eth.blockscout.com/api"
def api(**k):
    q="&".join(f"{a}={b}" for a,b in k.items())
    url=B+"?"+q
    req=urllib.request.Request(url,headers={"accept":"application/json","user-agent":"curl/8"})
    for i in range(5):
        try:
            with urllib.request.urlopen(req,timeout=60) as r: b=r.read()
            open(W+"/api_"+q.replace("&","_").replace("=","-")[:140]+".json","wb").write(b)
            return json.loads(b)
        except Exception as e:
            err=repr(e);time.sleep(2+3*i)
    print("échec",q,err);return None
def block(ts):
    j=api(module="block",action="getblocknobytime",timestamp=int(ts),closest="before")
    return int(j["result"]["blockNumber"])
O=list(csv.DictReader(open(OUT+"i14_orders.csv")))
ep=lambda u:int(dt.datetime.strptime(u,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
for a in ["0x2d86499a410a9ac2139833ba8d6942b8a8700a7b","0xb947bf7f409e998b28f8e218802fc9575c3c8c57","0xb29826d809aa04d2ead6f2310d8965a45b87fa67","0x86f99097c563e84dd5190f3e85f6a2988f1c47a5"]:
    orders=[r for r in O if r["receiver"]==a and r["take_chain"]=="1"]
    t0=min(ep(r["utc"]) for r in orders);t1=max(ep(r["utc"]) for r in orders)
    b0=block(t0-60);b1=block(t1+3600*6)
    time.sleep(.3)
    internal=api(module="account",action="txlistinternal",address=a,startblock=b0,endblock=b1,sort="asc",page=1,offset=2000)
    time.sleep(.3)
    tok=api(module="account",action="tokentx",address=a,contractaddress="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",startblock=b0,endblock=b1,sort="asc",page=1,offset=2000)
    I=(internal or {}).get("result") or []
    T=(tok or {}).get("result") or []
    print("==",a,"ordres",len(orders),"blocs",b0,b1,"internes",len(I),"USDC",len(T))
    vI={int(x["value"]):x for x in I if x.get("to","").lower()==a and x.get("isError","0")=="0"}
    vT={int(x["value"]):x for x in T if x.get("to","").lower()==a}
    ok=0;usd=0;usd_ok=0
    for r in orders:
        v=int(r["take_raw"]);g=(int(r["give_amount"])+int(r["fee_pct"]))/1e6;usd+=g
        if r["take_token"].startswith("0x000000"): hit=vI.get(v)
        else: hit=vT.get(v)
        if hit is None:
            # le preneur peut donner plus que le minimum : on cherche le plus proche dans les 2 h suivantes
            cand=[(int(x["value"]),x) for x in (I if r["take_token"].startswith("0x000000") else T) if x.get("to","").lower()==a and 0<=int(x["timeStamp"])-ep(r["utc"])<7200 and int(x["value"])>=v and int(x["value"])<=v*1.02]
            hit=cand[0][1] if cand else None
        if hit is not None:
            ok+=1;usd_ok+=g
            frm=hit.get("from","")
            print("  ",r["utc"],round(g,2),"take",v,"reçu",hit["value"],"de",frm,"écart s",int(hit["timeStamp"])-ep(r["utc"]),hit.get("hash") or hit.get("transactionHash"))
        else:
            print("  ",r["utc"],round(g,2),"take",v,"NON TROUVÉ")
    print(" exécutés vus",ok,"sur",len(orders),"USD",round(usd_ok,2),"sur",round(usd,2))
    time.sleep(.5)
# Devenir des USDC de 0xb947
a="0xb947bf7f409e998b28f8e218802fc9575c3c8c57"
b0=block(ep("2024-07-22T00:00:00Z"));b1=block(ep("2024-09-01T00:00:00Z"))
tok=api(module="account",action="tokentx",address=a,startblock=b0,endblock=b1,sort="asc",page=1,offset=200)
print("0xb947 transferts de jetons 22/07 à 01/09/2024",len((tok or {}).get("result") or []))
for x in (tok or {}).get("result") or []:
    print("  ",dt.datetime.fromtimestamp(int(x["timeStamp"]),dt.timezone.utc).strftime("%m-%dT%H:%M:%S"),x["from"][:12],"->",x["to"][:12],x.get("tokenSymbol"),int(x["value"])/10**int(x.get("tokenDecimal") or 0))
