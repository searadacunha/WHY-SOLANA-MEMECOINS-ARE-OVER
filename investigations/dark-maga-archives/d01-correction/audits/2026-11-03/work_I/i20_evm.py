"""Receveurs EVM : contrat ou compte, étiquettes, et exécution des ordres. Blockscout public, sans clé, Ethereum. Réponses brutes gardées dans audits_work/I/net_evm. Sortie i20_evm.txt."""
import json,urllib.request,time,os,csv,sys,datetime as dt
OUT="audits/2026-11-03/work_I/"
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/net_evm";os.makedirs(W,exist_ok=True)
sys.stdout=open(OUT+"i20_evm.txt","w")
BS={"1":"https://eth.blockscout.com","8453":"https://base.blockscout.com"}
def get(chain,path):
    url=BS[chain]+path
    req=urllib.request.Request(url,headers={"accept":"application/json","user-agent":"curl/8"})
    for i in range(4):
        try:
            with urllib.request.urlopen(req,timeout=40) as r: b=r.read()
            fn=W+"/"+chain+"_"+path.replace("/","_").replace("?","_").replace("&","_")[:150]+".json"
            open(fn,"wb").write(b)
            return json.loads(b)
        except Exception as e:
            err=repr(e);time.sleep(2+2*i)
    print("échec",url,err);return None
O=list(csv.DictReader(open(OUT+"i14_orders.csv")))
rec={}
for r in O: rec.setdefault((r["take_chain"],r["receiver"]),[]).append(r)
TOP=sorted(rec,key=lambda k:-sum(int(x["give_amount"]) for x in rec[k]))[:6]
for ch,a in TOP:
    if ch not in BS: continue
    j=get(ch,f"/api/v2/addresses/{a}")
    if not j: continue
    print(ch,a,"is_contract",j.get("is_contract"),"is_verified",j.get("is_verified"),"name",j.get("name"),"public_tags",j.get("public_tags"),"private_tags",j.get("private_tags"),"watchlist",j.get("watchlist_names"),"ens",j.get("ens_domain_name"),"has_token_transfers",j.get("has_token_transfers"),"balance",j.get("coin_balance"),"metadata",json.dumps(j.get("metadata"))[:300])
    c=get(ch,f"/api/v2/addresses/{a}/counters")
    print("   compteurs",c)
    time.sleep(0.5)
