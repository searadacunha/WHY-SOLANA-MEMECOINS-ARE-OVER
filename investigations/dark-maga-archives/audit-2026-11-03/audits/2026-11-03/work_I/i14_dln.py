"""G4/G5 : décodage propre des journaux DlnSource sur TOUT le brut C/net + G/net. Lit l'événement « Program data » qui suit « Instruction: CreateOrderWithNonce » (ou CreateOrder).
Structure attendue : disc(8) nonce(u64) maker(Vec) give{chain[32], token(Vec), amount[32] BE} take{...} receiver(Vec) patch(Vec) orderAuth(Vec) allowedTaker(Option<Vec>) cancelBenef(Option<Vec>) externalCall(Option<[32]>) puis frais.
Ecrit aussi toutes les autres instructions de src5, les programmes rencontrés (par fichier), et les remboursements éventuels. Sorties i14_orders.csv, i14_other_ix.csv, i14_programs.csv, i14_dln.txt."""
import base64,csv,glob,gzip,json,os,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
SRC="src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4"
B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58(b):
    n=int.from_bytes(b,"big");s=""
    while n: n,r=divmod(n,58);s=B58[r]+s
    return "1"*(len(b)-len(b.lstrip(b"\0")))+s
class Rd:
    def __init__(s,b): s.b=b;s.i=0
    def t(s,n): x=s.b[s.i:s.i+n];assert len(x)==n,"court";s.i+=n;return x
    def u32(s): return int.from_bytes(s.t(4),"little")
    def u64(s): return int.from_bytes(s.t(8),"little")
    def vec(s): n=s.u32();assert n<=64,"vec";return s.t(n)
    def be(s): return int.from_bytes(s.t(32),"big")
    def opt(s,f):
        x=s.t(1)[0];assert x in(0,1),"opt";return f() if x else None
def decode(raw):
    r=Rd(raw);disc=r.t(8);nonce=r.u64();maker=r.vec()
    gc=r.be();gt=r.vec();ga=r.be();tc=r.be();tt=r.vec();ta=r.be()
    rcv=r.vec();patch=r.vec();oauth=r.vec()
    at=r.opt(r.vec);cb=r.opt(r.vec);ec=r.opt(lambda:r.t(32))
    rest=raw[r.i:]
    fix=int.from_bytes(rest[:8],"little") if len(rest)>=8 else None
    pct=int.from_bytes(rest[8:16],"little") if len(rest)>=16 else None
    return dict(disc=disc.hex(),nonce=nonce,maker=b58(maker) if len(maker)==32 else maker.hex(),give_chain=gc,give_token=b58(gt) if len(gt)==32 else gt.hex(),give=ga,take_chain=tc,take_token="0x"+tt.hex(),take=ta,receiver="0x"+rcv.hex(),patch=patch.hex(),oauth="0x"+oauth.hex(),allowed_taker=at.hex() if at else "",cancel_benef=(b58(cb) if cb and len(cb)==32 else (cb.hex() if cb else "")),ext=ec.hex() if ec else "",fix=fix,pct=pct,rest=len(rest))
of=csv.writer(open(OUT+"i14_orders.csv","w"));of.writerow("utc wallet_file signer sig ix nonce maker give_token give_amount fee_fix_lamports fee_pct give_chain take_chain take_token take_raw receiver oauth allowed_taker cancel_benef ext signer_token_delta".split())
ox=csv.writer(open(OUT+"i14_other_ix.csv","w"));ox.writerow("utc file sig instructions signers".split())
pg=collections.Counter();pgsign=collections.Counter()
seen=set();seenx=set()
files=[]
for d in NETS:
    for f in sorted(os.listdir(d)):
        if f.startswith("._") or not f.endswith(".jsonl.gz"): continue
        if f.startswith(("ctrl_deposits","absent_","probe_")): continue
        files.append(f"{d}/{f}")
n=0;errs=[]
for p in files:
    wf=os.path.basename(p).split(".")[0]
    with gzip.open(p,"rt") as h:
        for l in h:
            n+=1
            if SRC not in l and "BrdgN2R" not in l and '"programId"' not in l: continue
            t=json.loads(l)
            ps=programs(t)
            S=signers(t)
            if t["meta"]["err"] is None and wf in S:
                for x in ps: pgsign[x]+=1
            if SRC not in ps: continue
            sg=t["transaction"]["signatures"][0]
            if sg in seen: continue
            seen.add(sg)
            u=dt.datetime.fromtimestamp(t["blockTime"],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            logs=t["meta"].get("logMessages") or []
            if t["meta"]["err"] is not None:
                ox.writerow([u,wf,sg,"ECHEC",S]);continue
            # pile des invocations
            depth=[];ixs=[];ord_=[]
            cur=None
            for i,lg in enumerate(logs):
                if lg.startswith("Program ") and " invoke [" in lg:
                    depth.append(lg.split()[1])
                elif lg.startswith("Program ") and (lg.endswith(" success") or " failed" in lg):
                    if depth: depth.pop()
                elif depth and depth[-1]==SRC and lg.startswith("Program log: Instruction: "):
                    cur=lg.split(": ",2)[2];ixs.append(cur)
                elif depth and depth[-1]==SRC and lg.startswith("Program data: ") and cur and cur.startswith("CreateOrder"):
                    raw=base64.b64decode(lg.split(": ",1)[1])
                    if len(raw)>120:
                        try:
                            d=decode(raw);ord_.append((cur,d))
                        except Exception as e:
                            errs.append((sg,repr(e)))
                        cur=cur+"#done"
            if not any(x.startswith("CreateOrder") for x in ixs):
                ox.writerow([u,wf,sg,"|".join(ixs),S])
            td,dec=tok_delta(t)
            for ix,d in ord_:
                me=d["maker"]
                mdelta={m:v for (o,m),v in td.items() if o==me and v<0}
                of.writerow([u,wf,S[0] if S else "",sg,ix.split("#")[0],d["nonce"],d["maker"],d["give_token"],d["give"],d["fix"],d["pct"],d["give_chain"],d["take_chain"],d["take_token"],d["take"],d["receiver"],d["oauth"],d["allowed_taker"],d["cancel_benef"],d["ext"],json.dumps(mdelta)])
w=csv.writer(open(OUT+"i14_programs.csv","w"));w.writerow(["program","n_tx_signees"])
for k,v in pgsign.most_common(): w.writerow([k,v])
with open(OUT+"i14_dln.txt","w") as f:
    print("fichiers",len(files),"lignes",n,"tx src5",len(seen),"erreurs décodage",errs,file=f)
