import sys,json
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
SRC="src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4"
w="C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae"
n=0
for t in iter_tx(w):
    if SRC in programs(t):
        n+=1
        if n==1:
            m=t["transaction"]["message"]
            print("sig",t["transaction"]["signatures"][0],t["blockTime"])
            for i in m["instructions"]: print(" ix",i.get("programId"),str(i.get("data"))[:200], str(i.get("parsed"))[:200], "accounts",len(i.get("accounts") or []))
            for l in t["meta"]["logMessages"]: print("  L",l[:400])
            print(" pre",[(b["owner"][:8],b["mint"][:8],b["uiTokenAmount"]["amount"]) for b in t["meta"]["preTokenBalances"]])
            print(" post",[(b["owner"][:8],b["mint"][:8],b["uiTokenAmount"]["amount"]) for b in t["meta"]["postTokenBalances"]])
print("n",n)
