"""Suite de i21 après les refus 429, avec plages de blocs fixes. Sortie i22_evm_rest.txt."""
import json,urllib.request,time,os,csv,sys,datetime as dt
OUT="audits/2026-11-03/work_I/"
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/net_evm"
sys.stdout=open(OUT+"i22_evm_rest.txt","w",buffering=1)
B="https://eth.blockscout.com/api"
def api(**k):
    q="&".join(f"{a}={b}" for a,b in k.items());url=B+"?"+q
    req=urllib.request.Request(url,headers={"accept":"application/json","user-agent":"curl/8"})
    time.sleep(6)
    for i in range(4):
        try:
            with urllib.request.urlopen(req,timeout=60) as r: b=r.read()
            open(W+"/api_"+q.replace("&","_").replace("=","-")[:140]+".json","wb").write(b)
            return json.loads(b)
        except Exception as e:
            err=repr(e);time.sleep(25+20*i)
    print("échec",q[:100],err);return None
O=list(csv.DictReader(open(OUT+"i14_orders.csv")))
ep=lambda u:int(dt.datetime.strptime(u,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
for a,b0,b1 in [("0xb29826d809aa04d2ead6f2310d8965a45b87fa67",20318055,21185684),("0x86f99097c563e84dd5190f3e85f6a2988f1c47a5",20358014,20372000)]:
    orders=[r for r in O if r["receiver"]==a and r["take_chain"]=="1"]
    I=(api(module="account",action="txlistinternal",address=a,startblock=b0,endblock=b1,sort="asc",page=1,offset=2000) or {}).get("result") or []
    print("==",a,"ordres",len(orders),"internes",len(I))
    vI={int(x["value"]):x for x in I if x.get("to","").lower()==a and x.get("isError","0")=="0"}
    ok=0;usd=0;uok=0
    for r in orders:
        v=int(r["take_raw"]);g=(int(r["give_amount"])+int(r["fee_pct"]))/1e6;usd+=g;hit=vI.get(v)
        if hit: ok+=1;uok+=g
        print("  ",r["utc"],round(g,2),"take",v,"reçu" if hit else "NON TROUVÉ",hit.get("from") if hit else "",(int(hit["timeStamp"])-ep(r["utc"])) if hit else "")
    print(" exécutés",ok,"sur",len(orders),"USD",round(uok,2),"sur",round(usd,2))
a="0xb947bf7f409e998b28f8e218802fc9575c3c8c57"
T=(api(module="account",action="tokentx",address=a,startblock=20358000,endblock=20530000,sort="asc",page=1,offset=100) or {}).get("result") or []
print("0xb947 jetons du 22/07 au 15/08/2024",len(T))
for x in T:
    print("  ",dt.datetime.fromtimestamp(int(x["timeStamp"]),dt.timezone.utc).strftime("%m-%dT%H:%M:%S"),x["from"],"->",x["to"],x.get("tokenSymbol"),int(x["value"])/10**int(x.get("tokenDecimal") or 0))
L=(api(module="account",action="txlist",address=a,startblock=0,endblock=99999999,sort="asc",page=1,offset=30) or {}).get("result") or []
print("0xb947 premières tx propres",len(L))
for x in L[:30]:
    print("  ",dt.datetime.fromtimestamp(int(x["timeStamp"]),dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),x["from"],"->",x["to"],int(x["value"])/1e18,x.get("functionName","")[:30])
for z in ("0x555ce236c0220695b68341bc48c68d52210cc35b","0xe7351fd770a37282b91d153ee690b63579d6dd7f"):
    time.sleep(6)
    j=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://eth.blockscout.com/api/v2/addresses/{z}",headers={"user-agent":"curl/8"}),timeout=40).read())
    print(z,"is_contract",j.get("is_contract"),"name",j.get("name"),"tags",j.get("public_tags"),j.get("metadata"))
