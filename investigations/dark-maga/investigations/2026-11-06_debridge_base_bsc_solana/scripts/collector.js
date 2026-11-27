// Collecteur Blockscout v2 exécuté dans l'onglet http://127.0.0.1:47391/recv.html (lecture cross-origin autorisée par Blockscout).
// Chaque page brute est postée à /save ; un marqueur _DONE n'est écrit qu'en fin de pagination.
window.__prog = window.__prog || {}; window.__jobs = window.__jobs || [];
window.__pullAll = async function(host, chain, A, kind, maxPages){
  const key=`${chain}_${A.toLowerCase()}_${kind}`; const st = window.__prog[key] = {pages:0, items:0, done:false, err:null};
  let params=null; maxPages = maxPages || 100000;
  while(st.pages < maxPages){
    const qs = params ? '?'+new URLSearchParams(Object.fromEntries(Object.entries(params).filter(([k,v])=>v!==null))).toString() : '';
    const url = `https://${host}/api/v2/addresses/${A}/${kind}${qs}`;
    let body=null, tries=0;
    while(true){
      try { const r = await fetch(url); if(r.status===200){ body=await r.text(); break; } st.err='HTTP '+r.status; if(r.status===404){ st.done=true; return st; } }
      catch(e){ st.err=String(e); }
      tries++; if(tries>10){ st.err='GAVE UP '+st.err; return st; } await new Promise(z=>setTimeout(z,2500*tries));
    }
    const j = JSON.parse(body);
    const s = await fetch('/save?name='+`${key}_p${String(st.pages).padStart(5,'0')}.json`,{method:'POST',body: JSON.stringify({url, fetched_at:new Date().toISOString(), response:j})});
    if(s.status!==200){ st.err='SAVE '+s.status; return st; }
    st.pages++; st.items += (j.items||[]).length; st.err=null;
    if(!j.next_page_params){ st.done=true; await fetch('/save?name='+key+'_DONE.json',{method:'POST',body:JSON.stringify({pages:st.pages,items:st.items})}); return st; }
    params=j.next_page_params; await new Promise(z=>setTimeout(z,300));
  }
  st.err='STOPPED at maxPages'; return st;
};
window.__getOne = async function(host, path, name){ // une ressource unique (adresse, tx, logs d'une tx)
  const url=`https://${host}/api/v2/${path}`; for(let i=0;i<8;i++){ try{ const r=await fetch(url); if(r.status===200){ const j=await r.json();
    await fetch('/save?name='+name,{method:'POST',body:JSON.stringify({url, fetched_at:new Date().toISOString(), response:j})}); return 'ok'; } if(r.status===404) return '404'; }catch(e){} await new Promise(z=>setTimeout(z,2000*(i+1))); } return 'fail'; };
window.__runQueue = async function(){ if(window.__qr) return; window.__qr=true; while(window.__jobs.length){ const j=window.__jobs.shift();
  if(j[0]==='one') await window.__getOne(j[1],j[2],j[3]); else await window.__pullAll(...j); } window.__qr=false; };
window.__add = function(host, chain, addrs, kinds, maxPages){ for(const a of addrs) for(const k of (kinds||['transactions','token-transfers','internal-transactions'])) window.__jobs.push([host,chain,a,k,maxPages]); window.__runQueue(); return window.__jobs.length; };
window.__status = function(){ return JSON.stringify({queue:window.__jobs.length, running:window.__qr, prog:Object.fromEntries(Object.entries(window.__prog).filter(([k,s])=>!s.done||s.err).map(([k,s])=>[k.slice(0,60),s])), done:Object.values(window.__prog).filter(s=>s.done).length}); };
