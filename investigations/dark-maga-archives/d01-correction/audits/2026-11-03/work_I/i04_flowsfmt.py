import gzip,json,os,sys
R="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows/"
w="C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae"
print(sorted(x for x in os.listdir(R+w) if not x.startswith("._")))
for f in sorted(os.listdir(R+w)):
    if f.startswith("._"):continue
    o=json.load(gzip.open(R+w+"/"+f,"rt"))
    s=json.dumps(o)
    print(f,type(o).__name__,len(s), list(o.keys()) if isinstance(o,dict) else len(o))
    print("  ",s[:600])
