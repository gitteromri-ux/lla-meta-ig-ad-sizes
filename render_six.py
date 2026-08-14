#!/usr/bin/env python3
"""Re-render ONLY the six requested concepts (3e, 2a, 2b, 2c, 2d, 2e) straight out of
Omri's own bundled source page, with the LLA wordmark enlarged and its spacing corrected.
No asset regeneration: same source, same layout, only logo scale + breathing room change.
"""
import os, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source-pages', 'LLA-Banner-Concepts.html')
OUT = os.path.join(ROOT, 'six')
os.makedirs(OUT, exist_ok=True)

WANT = ['3e', '2a', '2b', '2c', '2d', '2e']

FIX = """(ids)=>{
  const out=[];
  ids.forEach(id=>{
    const sec=document.getElementById(id); if(!sec) return;
    const lbl=sec.querySelector('span[style*="letter-spacing"]');
    const fr=[...sec.querySelectorAll('div')].find(d=>{
      const z=parseFloat(d.style.zoom||'0');
      return z>0 && z<1 && d.style.width && d.style.height;});
    if(!fr) return;
    fr.setAttribute('data-cap', id);
    // --- LOGO / WORDMARK FIX -------------------------------------------
    // Same asset, same layout. The lockup is scaled up (and lifted / its band
    // grown where needed) so it never collides with existing artwork.
    const frR=fr.getBoundingClientRect();
    const Z=parseFloat(fr.style.zoom||'1')||1;
    const imgs=[...fr.querySelectorAll('img')];
    imgs.forEach(im=>{
      const nw=im.naturalWidth||0, nh=im.naturalHeight||0;
      if(!nw||!nh) return;
      const nar=nw/nh, r0=im.getBoundingClientRect();
      if(!(nw>900 && nar>1.9 && nar<2.6 && (r0.width/(frR.width||1))<0.5)) return;
      const st=im.getAttribute('style')||'';
      const centered=/translateX\(-50%\)/.test(st);
      const abs=getComputedStyle(im).position==='absolute';
      // frame-space geometry (undo the preview zoom)
      const L=(r0.left-frR.left)/Z, T=(r0.top-frR.top)/Z;
      const W0=r0.width/Z, H0=r0.height/Z;
      const FW=frR.width/Z, FH=frR.height/Z;
      const pad=26, gapMin=18, KMAX=1.5, KMIN=1.2;
      const parent=im.parentElement;
      const pR=parent?parent.getBoundingClientRect():null;
      const band = (parent && pR && pR.height/Z < FH*0.25 &&
                    getComputedStyle(parent).position!=='static') ? parent : null;
      const bandT = band ? (pR.top-frR.top)/Z : null;
      const bandH = band ? pR.height/Z : null;
      // widest possible footprint, used for the horizontal overlap test
      const wideL = centered ? L+W0/2-(W0*KMAX)/2 : L;
      const wideR = wideL + W0*KMAX;
      let obstacleTop = FH - pad;
      [...fr.querySelectorAll('img,div,span,p,a')].forEach(o=>{
        if(o===im||o.contains(im)||im.contains(o)) return;
        if(band && band.contains(o)) return;
        const isImg=o.tagName==='IMG';
        if(!isImg && o.childElementCount>0) return;
        if(!isImg && !(o.textContent||'').trim()) return;
        const r=o.getBoundingClientRect();
        const w=r.width/Z, h=r.height/Z;
        if(w<4||h<4) return;
        if(w>FW*0.9 && h>FH*0.9) return;                 // full-bleed background
        const oT=(r.top-frR.top)/Z, oL=(r.left-frR.left)/Z, oR=oL+w;
        if(oT < T) return;                               // above the lockup
        if(oR<=wideL+1 || oL>=wideR-1) return;           // clears it horizontally
        if(oT < obstacleTop) obstacleTop = oT;
      });
      // structural boxes (arch frame, panels) below the lockup also matter
      [...fr.querySelectorAll('div')].forEach(o=>{
        if(o===im||o.contains(im)) return;
        if(band && (band.contains(o)||o===band)) return;
        const cs=getComputedStyle(o);
        const hasEdge = cs.borderTopWidth!=='0px' || (cs.backgroundImage&&cs.backgroundImage!=='none') ||
                        (cs.backgroundColor&&cs.backgroundColor!=='rgba(0, 0, 0, 0)');
        if(!hasEdge) return;
        const r=o.getBoundingClientRect();
        const w=r.width/Z, h=r.height/Z;
        if(w<40||h<40) return;
        if(w>FW*0.9 && h>FH*0.9) return;
        const oT=(r.top-frR.top)/Z, oL=(r.left-frR.left)/Z, oR=oL+w;
        if(oT < T) return;
        if(oR<=wideL+1 || oL>=wideR-1) return;
        if(oT < obstacleTop) obstacleTop = oT;
      });
      // lift the lockup toward the top safe margin to buy vertical room
      let newT=T;
      if(abs && T>pad) newT=Math.max(pad, Math.min(T, T-(H0*KMAX-H0)));
      let K=Math.min(KMAX, (obstacleTop-gapMin-newT)/H0);
      if(centered) K=Math.min(K,(FW-2*pad)/W0); else K=Math.min(K,(FW-L-pad)/W0);
      if(K<KMIN) K=KMIN;
      if(abs && newT!==T) im.style.top=newT+'px';
      // inside a flex band the mark is vertically centred, so scale about its
      // own centre and grow the band symmetrically - never past the band edge
      im.style.transformOrigin = band ? 'center center' : (centered ? 'center top' : 'left top');
      im.style.transform = (centered?'translateX(-50%) ':'') + 'scale('+K+')';
      // grow the dark lockup band so the bigger mark keeps even breathing room
      if(band){
        const want = Math.min(obstacleTop-16, H0*K + 2*Math.max(16, (bandH-H0)/2));
        if(want > bandH) band.style.height = want+'px';
      }
      im.setAttribute('data-lla-logo', K.toFixed(3)+(band?'|band':''));
    });
    const r=fr.getBoundingClientRect();
    out.push({id:id, label:lbl?lbl.textContent.trim():id,
              logos:[...fr.querySelectorAll('[data-lla-logo]')].map(e=>e.getAttribute('data-lla-logo'))});
  });
  document.body.style.background='#05070d';
  return out;}"""

report = []
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/home/user/.cache/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell', args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for scale, w, h in ((1.0, 1080, 1080), (1440 / 1080, 1440, 1440)):
        page = br.new_page(viewport={'width': w + 60, 'height': h + 60}, device_scale_factor=1)
        page.goto('file://' + SRC)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(9000)
        found = page.evaluate(FIX, WANT)
        print('sections:', found)
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
            print('rendered', name, 'logos:', meta['logos'])
            if scale == 1.0:
                report.append({'id': meta['id'], 'label': meta['label'],
                               'file_1080': 'six/' + name,
                               'file_1440': 'six/' + name.replace('1080x1080', '1440x1440')})
        page.close()
    br.close()
json.dump(report, open(os.path.join(ROOT, 'six_report.json'), 'w'), indent=2)
print('done', len(report))
