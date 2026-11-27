#!/usr/bin/env python3
"""Page interactive autonome (viz/index.html) : chronologie prix + événements + posts, et graphe financier.

Aucune dépendance externe, aucun réseau à l'ouverture. Les données viennent des fichiers de data/ et de BIG.
"""
import csv
import json
from pathlib import Path

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.labels import label

con = connect()
con.execute(f"CREATE VIEW w AS SELECT * FROM read_parquet('{BIG}/wallets.parquet')")
con.execute(f"CREATE VIEW l AS SELECT * FROM read_parquet('{BIG}/link_edges.parquet')")

price = []
with (DATA / "price_hourly.csv").open() as f:
    for r in csv.DictReader(f):
        t = int(r["hour_utc"])
        if t < 1725148800:  # jusqu'au 01/09/2024
            price.append([t, float(r["close_sol"]) * 1e9])  # capitalisation en SOL : prix × offre 10^9
events = json.loads((DATA / "events.json").read_text())

CORE = {"DarkMagaCoin", "kikisknees", "Aristos_Revenge", "ChrisWinig", "elonmusk", "pmarca", "koreanjewcrypto", "ai_9684xtpa", "ramonos", "ashrobin"}
posts = []
seen = set()
for line in (DATA / "x_posts.jsonl").open():
    r = json.loads(line)
    if r["id"] in seen or r.get("author") not in CORE or r.get("status") != "ok":
        continue
    txt = (r.get("text") or "")
    if not any(k in txt.lower() for k in ("dmaga", "dark maga", "pfp", "laser", "7d7brc")) and r["id"] not in ("1815054750775173447", "1815053805077086351"):
        continue
    seen.add(r["id"])
    import datetime as dt
    t = int(dt.datetime.strptime(r["created_utc_snowflake"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
    posts.append({"t": t, "a": r["author"], "x": txt[:180], "id": r["id"]})
for line in Path("evidence/x_wayback/recovered.jsonl").open():
    r = json.loads(line)
    txt = r.get("text") or ""
    if r["id"] in seen or txt.startswith("RT @") or not any(k in txt.lower() for k in ("dmaga", "dark maga", "pfp", "elon")):
        continue
    seen.add(r["id"])
    t = int(((int(r["id"]) >> 22) + 1288834974657) / 1000)
    posts.append({"t": t, "a": r.get("username") or r.get("account_in_url"), "x": txt[:180] + " [supprimé, texte Wayback]", "id": r["id"]})
posts = [p for p in posts if 1720900000 < p["t"] < 1722000000]
posts.sort(key=lambda p: p["t"])

edges = con.execute("SELECT src, dst, type, sum(amount), count(*), min(block_time), any_value(signature) FROM l GROUP BY 1,2,3").fetchall()
ids = {}
for s, d, *_ in edges:
    ids.setdefault(s, len(ids))
    ids.setdefault(d, len(ids))
meta = {r[0]: r[1:] for r in con.execute("SELECT owner, realized_sol, net_sol_all, bought_sol, residual_qty, first_buy_time FROM w").fetchall()}
REPORTED = {"9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq": "signalé", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra": "@ai_9684xtpa",
            "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd": "@0xRamonos", "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc": "@ashrobinqt",
            "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR": "créateur"}
nodes = []
for a, i in ids.items():
    m = meta.get(a)
    nodes.append({"id": i, "a": a, "tag": REPORTED.get(a), "lab": label(a),
                  "real": round(m[0], 1) if m else None, "net": round(m[1], 1) if m else None,
                  "buy": round(m[2], 2) if m else None, "res": round((m[3] or 0) / 1e6, 2) if m else None, "fb": m[4] if m else None})
links = [{"s": ids[s], "t": ids[d], "k": k, "amt": round(a or 0, 2), "n": n, "at": t, "sig": sig} for s, d, k, a, n, t, sig in edges]
data = {"price": price, "events": events, "posts": posts, "nodes": nodes, "links": links}

HTML = r"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Dark MAGA, chronologie et graphe financier</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><style>
:root{color-scheme:light;--s:#fcfcfb;--t:#0b0b0b;--t2:#52514e;--g:#e6e5e0;--c1:#2a78d6;--c2:#eb6834;--c3:#1baf7a;--c4:#eda100;--c5:#e87ba4}
@media(prefers-color-scheme:dark){:root{color-scheme:dark;--s:#1a1a19;--t:#f0efec;--t2:#c3c2b7;--g:#32322f;--c1:#3987e5;--c2:#d95926;--c3:#199e70;--c4:#c98500;--c5:#d55181}}
body{margin:0;background:var(--s);color:var(--t);font:14px/1.45 -apple-system,system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:20px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;margin:26px 0 6px}p{color:var(--t2);margin:4px 0 10px}
.row{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin:8px 0}label{cursor:pointer}svg,canvas{display:block;width:100%;border:1px solid var(--g);border-radius:6px}
#tip,#detail{font-size:13px}#tip{position:fixed;pointer-events:none;background:var(--s);border:1px solid var(--g);border-radius:6px;padding:6px 8px;max-width:340px;display:none;box-shadow:0 2px 8px #0003}
#detail{border:1px solid var(--g);border-radius:6px;padding:8px 10px;min-height:66px}code{font-size:12px;word-break:break-all}.sw{display:inline-block;width:14px;height:3px;margin-right:5px;vertical-align:middle;border-radius:2px}
table{border-collapse:collapse;width:100%;font-size:12.5px}td,th{border-bottom:1px solid var(--g);padding:3px 6px;text-align:left}th{color:var(--t2);font-weight:600}a{color:var(--c1)}
</style></head><body><main>
<h1>Dark MAGA ($DMAGA) : chronologie et graphe financier</h1>
<p>Une arête dit qu'une transaction ou un fait existe, pas que deux adresses ont le même propriétaire. Les services (échanges, pools, routeurs) sont retirés du graphe.</p>
<h2>Capitalisation du pool Raydium en SOL, échelle log, avec les événements et les posts archivés</h2>
<div class="row"><label><input type="range" id="zoom" min="0" max="2" value="0"> <span id="zoomL"></span></label></div>
<svg id="c" viewBox="0 0 1140 380" role="img" aria-label="Capitalisation de DMAGA en SOL dans le temps, avec événements"></svg>
<h2>Graphe financier : wallets et types de preuve</h2>
<div class="row" id="filters"></div>
<canvas id="g" width="1140" height="620" role="img" aria-label="Graphe des wallets reliés"></canvas>
<div id="detail">Cliquer un wallet pour voir ses chiffres.</div>
<h2>Vue tableau des arêtes les plus fortes</h2><table id="tb"></table>
</main><div id="tip"></div><script>
const D=__DATA__;const TIP=document.getElementById('tip');
const fmt=t=>new Date(t*1000).toISOString().slice(0,16).replace('T',' ')+' UTC';
const showTip=(e,h)=>{TIP.innerHTML=h;TIP.style.display='block';TIP.style.left=Math.min(e.clientX+14,innerWidth-360)+'px';TIP.style.top=e.clientY+14+'px'};const hideTip=()=>TIP.style.display='none';
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const RANGES=[['14/07 au 31/08',1720900000,1725148800],['14/07 au 26/07',1720900000,1722000000],['21/07, 12 h à 24 h UTC',1721563200,1721606400]];
function chart(){const R=RANGES[+zoom.value];zoomL.textContent='Période : '+R[0];const [_,a,b]=R;const W=1140,H=380,L=60,T=14,BB=56;const P=D.price.filter(p=>p[0]>=a&&p[0]<=b);
const ys=P.map(p=>Math.log10(Math.max(p[1],1)));const y0=Math.floor(Math.min(...ys)),y1=Math.ceil(Math.max(...ys));
const X=t=>L+(t-a)/(b-a)*(W-L-12),Y=v=>T+(y1-v)/(y1-y0)*(H-T-BB);let s='';
for(let v=y0;v<=y1;v++){s+=`<line x1="${L}" x2="${W-12}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--g)"/><text x="${L-6}" y="${Y(v)+4}" text-anchor="end" font-size="11" fill="var(--t2)">${(10**v).toLocaleString('fr-FR')}</text>`}
s+=`<polyline fill="none" stroke="var(--c1)" stroke-width="2" points="${P.map(p=>X(p[0]).toFixed(1)+','+Y(Math.log10(Math.max(p[1],1))).toFixed(1)).join(' ')}"/>`;
D.events.filter(e=>e.t>=a&&e.t<=b).forEach(e=>{s+=`<line class="ev" data-h="${esc(e.name)} : ${fmt(e.t)}<br>${esc(e.source)} (fiabilité ${e.fiabilite})" x1="${X(e.t)}" x2="${X(e.t)}" y1="${T}" y2="${H-BB}" stroke="var(--c2)" stroke-width="3" stroke-opacity=".55"/>`});
D.posts.filter(p=>p.t>=a&&p.t<=b).forEach(p=>{s+=`<circle class="ev" data-h="@${esc(p.a)}, ${fmt(p.t)}<br>${esc(p.x)}<br>id ${p.id}" cx="${X(p.t)}" cy="${H-BB+14}" r="4" fill="var(--c3)" stroke="var(--s)" stroke-width="1"/>`});
const days=b-a>4*86400?(b-a>20*86400?7:1):0;if(days){for(let t=Math.ceil(a/(86400*days))*86400*days;t<b;t+=86400*days){s+=`<text x="${X(t)}" y="${H-12}" font-size="11" text-anchor="middle" fill="var(--t2)">${new Date(t*1000).toISOString().slice(5,10)}</text>`}}else{for(let t=Math.ceil(a/3600/2)*7200;t<b;t+=7200){s+=`<text x="${X(t)}" y="${H-12}" font-size="11" text-anchor="middle" fill="var(--t2)">${new Date(t*1000).toISOString().slice(11,16)}</text>`}}
s+=`<text x="${L}" y="${H-BB+32}" font-size="11" fill="var(--t2)">traits orange : événements ; points verts : posts archivés (survol pour lire)</text>`;
c.innerHTML=s;c.querySelectorAll('.ev').forEach(n=>{n.onmousemove=e=>showTip(e,n.dataset.h);n.onmouseleave=hideTip})}
zoom.oninput=chart;chart();
const KIND={token_direct:['Transfert direct de DMAGA','--c2'],sol_direct:['Virement SOL direct','--c1'],funder_commun:['Financeur commun','--c3'],sink_commun:['Destination commune','--c4']};
const on={token_direct:1,sol_direct:1,funder_commun:0,sink_commun:0};const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
filters.innerHTML=Object.entries(KIND).map(([k,v])=>`<label><input type="checkbox" data-k="${k}" ${on[k]?'checked':''}> <span class="sw" style="background:var(${v[1]})"></span>${v[0]}</label>`).join('');
const N=D.nodes.map(n=>({...n,x:570+Math.random()*400-200,y:310+Math.random()*300-150,vx:0,vy:0}));const ctx=g.getContext('2d');let sel=null,alpha=1;
function active(){return D.links.filter(l=>on[l.k])}
function degree(){const d={};active().forEach(l=>{d[l.s]=(d[l.s]||0)+1;d[l.t]=(d[l.t]||0)+1});return d}
function step(){const A=active(),deg=degree();const vis=N.filter(n=>deg[n.id]);for(let i=0;i<vis.length;i++){const a=vis[i];for(let j=i+1;j<vis.length;j++){const b=vis[j];let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+30;if(d2>40000)continue;const f=420/d2*alpha;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f}}
A.forEach(l=>{const a=N[l.s],b=N[l.t];const dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-46)*.018*alpha;a.vx+=dx/d*f*d/40;a.vy+=dy/d*f*d/40;b.vx-=dx/d*f*d/40;b.vy-=dy/d*f*d/40});
vis.forEach(n=>{n.vx+=(570-n.x)*.002*alpha;n.vy+=(310-n.y)*.002*alpha;n.vx*=.82;n.vy*=.82;n.x=Math.max(10,Math.min(1130,n.x+n.vx));n.y=Math.max(10,Math.min(610,n.y+n.vy))});alpha=Math.max(alpha*.995,.02)}
function draw(){const deg=degree();ctx.clearRect(0,0,1140,620);active().forEach(l=>{const a=N[l.s],b=N[l.t];ctx.strokeStyle=css(KIND[l.k][1]);ctx.globalAlpha=(sel!==null&&l.s!==sel&&l.t!==sel)?.1:.75;ctx.lineWidth=l.k==='token_direct'?2:1;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()});ctx.globalAlpha=1;
N.forEach(n=>{if(!deg[n.id])return;const r=n.tag?7:Math.min(3+Math.sqrt(Math.max(n.net||0,0))/6,11);ctx.beginPath();ctx.arc(n.x,n.y,r,0,7);ctx.fillStyle=n.tag?css('--c5'):css('--t2');ctx.fill();ctx.lineWidth=2;ctx.strokeStyle=css('--s');ctx.stroke();if(n.tag||(n.net||0)>800){ctx.fillStyle=css('--t');ctx.font='11px sans-serif';ctx.fillText((n.tag?n.tag+' ':'')+n.a.slice(0,6),n.x+r+3,n.y+4)}})}
function loop(){step();draw();requestAnimationFrame(loop)}loop();
filters.querySelectorAll('input').forEach(i=>i.onchange=()=>{on[i.dataset.k]=+i.checked;alpha=.8;table()});
const pick=e=>{const r=g.getBoundingClientRect(),sx=1140/r.width,x=(e.clientX-r.left)*sx,y=(e.clientY-r.top)*sx;const deg=degree();let best=null,bd=144;N.forEach(n=>{if(!deg[n.id])return;const d=(n.x-x)**2+(n.y-y)**2;if(d<bd){bd=d;best=n}});return best};
g.onmousemove=e=>{const n=pick(e);if(n)showTip(e,`<code>${n.a}</code><br>net SOL : ${n.net??'n/d'} ; acheté : ${n.buy??'n/d'} SOL`);else hideTip()};g.onmouseleave=hideTip;
g.onclick=e=>{const n=pick(e);sel=n?n.id:null;detail.innerHTML=n?`<b>${n.tag||'wallet'}</b> <code>${n.a}</code> <a href="https://solscan.io/account/${n.a}" target="_blank" rel="noopener">Solscan</a><br>réalisé ${n.real??'n/d'} SOL ; flux net tous venues ${n.net??'n/d'} SOL ; acheté ${n.buy??'n/d'} SOL ; résiduel ${n.res??'n/d'} M ; premier achat ${n.fb?fmt(n.fb):'n/d'}`:'Cliquer un wallet pour voir ses chiffres.'};
function table(){const rows=active().slice().sort((a,b)=>(b.k==='token_direct')-(a.k==='token_direct')||b.amt-a.amt).slice(0,40);tb.innerHTML='<tr><th>De</th><th>Vers</th><th>Type</th><th>Montant</th><th>Tx</th><th>Première</th></tr>'+rows.map(l=>`<tr><td><code>${N[l.s].a}</code></td><td><code>${N[l.t].a}</code></td><td>${KIND[l.k][0]}</td><td>${l.amt.toLocaleString('fr-FR')}</td><td>${l.n}</td><td>${fmt(l.at)}</td></tr>`).join('')}table();
</script></body></html>"""
Path("viz").mkdir(exist_ok=True)
Path("viz/index.html").write_text(HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))
print("viz/index.html", Path("viz/index.html").stat().st_size // 1024, "Ko", "posts", len(posts), "noeuds", len(nodes), "arêtes", len(links))
