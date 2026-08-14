#!/usr/bin/env python3
"""Render ONLY the six requested concepts (3e, 2a, 2b, 2c, 2d, 2e) from Omri's own
bundled source page, with:
  1. the real brand lockup (PRLOGO, blue/teal gradient, transparent PNG) swapped in
     for the old flat-white mark, scaled up and collision-checked,
  2. the giant ghost wordmark on the GHOST WORDMARK layouts moved out from behind the
     lockup and lifted off the bottom edge so it is fully visible.
No asset regeneration: same source page, same layout, same photography.
"""
import os, json, base64
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source-pages', 'LLA-Banner-Concepts.html')
LOGO = os.path.join(ROOT, 'assets', 'lla_logo_brand.png')
OUT = os.path.join(ROOT, 'six')
os.makedirs(OUT, exist_ok=True)
CHROME = '/home/user/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell'

WANT = ['3e', '2a', '2b', '2c', '2d', '2e']
LOGO_URI = 'data:image/png;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()

# ---- pass 1: swap the lockup asset + fix the ghost wordmark placement -------
PASS1 = r"""(a)=>{
  const [ids, uri] = a;
  const out=[];
  ids.forEach(id=>{
    const sec=document.getElementById(id); if(!sec) return;
    const lbl=sec.querySelector('span[style*="letter-spacing"]');
    const fr=[...sec.querySelectorAll('div')].find(d=>{
      const z=parseFloat(d.style.zoom||'0');
      return z>0 && z<1 && d.style.width && d.style.height;});
    if(!fr) return;
    fr.setAttribute('data-cap', id);
    const Z=parseFloat(fr.style.zoom||'1')||1;
    const frR=fr.getBoundingClientRect();
    const FW=frR.width/Z, FH=frR.height/Z;

    // --- brand lockup swap -------------------------------------------------
    [...fr.querySelectorAll('img')].forEach(im=>{
      const nw=im.naturalWidth||0, nh=im.naturalHeight||0;
      if(!nw||!nh) return;
      const nar=nw/nh, r0=im.getBoundingClientRect();
      // old flat-white lockup asset is 1314x596; Trustpilot stars are 512x96
      if(!(nw>900 && nar>1.9 && nar<2.6 && (r0.width/(frR.width||1))<0.5)) return;
      im.setAttribute('data-lla-logo','1');
      im.src=uri;
    });

    // --- ghost wordmark placement -----------------------------------------
    // Outlined display type ("Longevity" / "Life Academy") set behind the card.
    // Requirement: never sit under the lockup, never clipped by the frame edge.
    const ghosts=[...fr.querySelectorAll('div')].filter(d=>{
      const st=d.getAttribute('style')||'';
      return /text-stroke/.test(st) && (d.textContent||'').trim().length>3;});
    ghosts.forEach(g=>{
      const t=(g.textContent||'').trim();
      const st=g.getAttribute('style')||'';
      if(/top:\s*2?\dpx/.test(st) && /right:/.test(st)){
        // top ghost line: drop it clear of the lockup block
        g.style.top='268px';
        g.style.right='30px';
      }
      if(/bottom:/.test(st)){
        // bottom ghost line: lift it fully inside the frame
        g.style.bottom='30px';
        g.style.left='34px';
        const fs=parseFloat(getComputedStyle(g).fontSize)/Z;
        g.style.fontSize=Math.min(fs,132)+'px';
      }
      g.setAttribute('data-lla-ghost', t.slice(0,20));
    });
    out.push({id:id, label:lbl?lbl.textContent.trim():id,
              ghosts:ghosts.length,
              logos:fr.querySelectorAll('[data-lla-logo]').length});
  });
  document.body.style.background='#05070d';
  return out;}"""

# ---- pass 2: scale the (now brand) lockup, collision aware ------------------
PASS2 = r"""(ids)=>{
  const rep=[];
  ids.forEach(id=>{
    const fr=document.querySelector('div[data-cap="'+id+'"]'); if(!fr) return;
    const Z=parseFloat(fr.style.zoom||'1')||1;
    const frR=fr.getBoundingClientRect();
    const FW=frR.width/Z, FH=frR.height/Z;
    fr.querySelectorAll('img[data-lla-logo]').forEach(im=>{
      const r0=im.getBoundingClientRect();
      const st=im.getAttribute('style')||'';
      const centered=/translateX\(-50%\)/.test(st);
      const abs=getComputedStyle(im).position==='absolute';
      const L=(r0.left-frR.left)/Z, T=(r0.top-frR.top)/Z;
      const W0=r0.width/Z, H0=r0.height/Z;
      const pad=26, gapMin=18, KMAX=1.5, KMIN=1.2;
      const parent=im.parentElement;
      const pR=parent?parent.getBoundingClientRect():null;
      const band=(parent&&pR&&pR.height/Z<FH*0.25&&getComputedStyle(parent).position!=='static')?parent:null;
      const bandH=band?pR.height/Z:null;
      const wideL=centered?L+W0/2-(W0*KMAX)/2:L, wideR=wideL+W0*KMAX;
      let obstacleTop=FH-pad;
      const consider=(o, minW, minH, skipGhost)=>{
        if(o===im||o.contains(im)||im.contains(o)) return;
        if(band&&(band===o||band.contains(o))) return;
        if(skipGhost&&o.hasAttribute('data-lla-ghost')) return;
        const r=o.getBoundingClientRect(), w=r.width/Z, h=r.height/Z;
        if(w<minW||h<minH) return;
        if(w>FW*0.9&&h>FH*0.9) return;
        const oT=(r.top-frR.top)/Z, oL=(r.left-frR.left)/Z, oR=oL+w;
        if(oT<T) return;
        if(oR<=wideL+1||oL>=wideR-1) return;
        if(oT<obstacleTop) obstacleTop=oT;
      };
      [...fr.querySelectorAll('img,div,span,p,a')].forEach(o=>{
        const isImg=o.tagName==='IMG';
        if(!isImg&&o.childElementCount>0) return;
        if(!isImg&&!(o.textContent||'').trim()) return;
        consider(o,4,4,true);                 // ghost type may sit behind the mark
      });
      [...fr.querySelectorAll('div')].forEach(o=>{
        const cs=getComputedStyle(o);
        const edge=cs.borderTopWidth!=='0px'||(cs.backgroundImage&&cs.backgroundImage!=='none')||
                   (cs.backgroundColor&&cs.backgroundColor!=='rgba(0, 0, 0, 0)');
        if(!edge) return;
        consider(o,40,40,true);
      });
      let newT=T;
      if(abs&&T>pad) newT=Math.max(pad, Math.min(T, T-(H0*KMAX-H0)));
      let K=Math.min(KMAX,(obstacleTop-gapMin-newT)/H0);
      if(centered) K=Math.min(K,(FW-2*pad)/W0); else K=Math.min(K,(FW-L-pad)/W0);
      if(K<KMIN) K=KMIN;
      if(abs&&newT!==T) im.style.top=newT+'px';
      im.style.transformOrigin = band?'center center':(centered?'center top':'left top');
      im.style.transform=(centered?'translateX(-50%) ':'')+'scale('+K+')';
      if(band){
        const want=Math.min(obstacleTop-16, H0*K+2*Math.max(16,(bandH-H0)/2));
        if(want>bandH) band.style.height=want+'px';
      }
      rep.push(id+':'+K.toFixed(2)+(band?'|band':''));
    });
  });
  return rep;}"""

report = []
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME,
                           args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for scale, w, h in ((1.0, 1080, 1080), (1440 / 1080, 1440, 1440)):
        page = br.new_page(viewport={'width': w + 60, 'height': h + 60}, device_scale_factor=1)
        page.goto('file://' + SRC)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(9000)
        found = page.evaluate(PASS1, [WANT, LOGO_URI])
        print('pass1:', found)
        page.wait_for_timeout(2500)                      # let the new lockup decode
        print('pass2:', page.evaluate(PASS2, WANT))
        page.evaluate("""(a)=>{const [ids,sc]=a; ids.forEach(id=>{
            const fr=document.querySelector('div[data-cap="'+id+'"]'); if(fr) fr.style.zoom=String(sc);});}""",
                      [WANT, scale])
        page.wait_for_timeout(2500)
        for meta in found:
            el = page.query_selector(f'div[data-cap="{meta["id"]}"]')
            if not el:
                print('MISS', meta['id']); continue
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(350)
            name = f"LLA_{meta['id'].upper()}_{meta['label'].replace(' · ','_').replace(' ','-')}_{w}x{h}.png"
            name = ''.join(c for c in name if c.isalnum() or c in '._-')
            el.screenshot(path=os.path.join(OUT, name))
            print('rendered', name)
            if scale == 1.0:
                report.append({'id': meta['id'], 'label': meta['label'],
                               'file_1080': 'six/' + name,
                               'file_1440': 'six/' + name.replace('1080x1080', '1440x1440')})
        page.close()
    br.close()
json.dump(report, open(os.path.join(ROOT, 'six_report.json'), 'w'), indent=2)
print('done', len(report))
