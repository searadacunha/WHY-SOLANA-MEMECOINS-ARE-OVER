"""Récepteur local (127.0.0.1 seulement) : la page Blockscout ouverte dans Chrome y poste les réponses brutes de l'API.
Chaque POST /save?name=<nom> est écrit tel quel dans raw/browser_dump/<nom>, avec son sha256 dans ledger.jsonl."""
import hashlib, json, os, re, time, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
OUT = Path(os.environ.get("DMAGA_NT_RAW", Path(__file__).resolve().parent.parent / "raw")) / "browser_dump"
# seule la page servie ici peut poster (même origine) ; un autre site ouvert dans le navigateur ne peut rien écrire
LOCAL = re.compile(r"http://(127\.0\.0\.1|localhost):\d+")

class H(BaseHTTPRequestHandler):
    def _cors(self):
        o = self.headers.get("Origin") or ""
        if LOCAL.fullmatch(o): self.send_header("Access-Control-Allow-Origin", o)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        name = parse_qs(urlparse(self.path).query).get("name", [""])[0]
        o = self.headers.get("Origin")
        if o is not None and not LOCAL.fullmatch(o):
            self.send_response(403); self.end_headers(); return
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,200}", name):
            self.send_response(400); self._cors(); self.end_headers(); return
        body = self.rfile.read(int(self.headers.get("content-length", 0)))
        (OUT / name).write_bytes(body)
        with open(OUT / "ledger.jsonl", "a") as f:
            f.write(json.dumps({"t": int(time.time()), "name": name, "n": len(body), "sha256": hashlib.sha256(body).hexdigest()}) + "\n")
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")
    def do_GET(self):
        if self.path.startswith("/collector.js"):
            js = (Path(__file__).resolve().parent / "collector.js").read_bytes()
            self.send_response(200); self.send_header("content-type", "application/javascript"); self.end_headers(); self.wfile.write(js); return  # page relais : reçoit les données par postMessage depuis l'onglet Blockscout, puis les poste ici (même origine)
        page = b"""<!doctype html><title>recv</title><pre id=o>ready</pre><script src="/collector.js"></script><script>
window.addEventListener('message', async e => { if(!/^https:\\/\\/[a-z0-9.-]+\\.blockscout\\.com$/.test(e.origin)) return; const m=e.data||{}; if(!m.name) return;
  const r = await fetch('/save?name='+encodeURIComponent(m.name), {method:'POST', body:m.body});
  document.getElementById('o').textContent += '\\n'+m.name+' '+r.status; e.source && e.source.postMessage({ack:m.name, status:r.status}, '*'); });
</script>"""
        self.send_response(200); self.send_header("content-type", "text/html"); self.end_headers(); self.wfile.write(page)
    def log_message(self, *a): pass

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
