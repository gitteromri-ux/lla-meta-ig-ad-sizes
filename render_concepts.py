#!/usr/bin/env python3
"""Render every banner concept from the uploaded LLA Banner Concepts export at native
and 1440 resolution, straight out of Omri's own file so the design is exact."""
import os, json, re, unicodedata
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source-pages', 'LLA-Banner-Concepts.html')
OUT = os.path.join(ROOT, 'concepts')
os.makedirs(OUT, exist_ok=True)

# Curated order: strongest concepts first, per Omri's "nicest ones first" note.
PRIORITY = ['j6', 'j7', 'g1', 'g2', 'g3', 'e2', 'e3', 'e1', 'w2', 'w1', 'w3',
            'b4', 'b3', 'b2', 'b1', 'b5', 'c5', 'j5', 'c3', 'j3', 'c1', 'j1',
            'c2', 'j2', 'c4', 'j4', 'z2', 'z1', 'z4', 'z3', '5b', '5a',
            '4e', '4d', '4f', '4b', '4a', '4c', '3a', '3b', '3c', '3d', '3e',
            '2a', '2b', '2c', '2d', '2e', '1a', '1b', '1c', '1d', '1e']


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').upper()
    return re.sub(r'-{2,}', '-', s)[:58]


report = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for scale, w, h in ((1.0, 1080, 1080), (1440 / 1080, 1440, 1440)):
        page = br.new_page(viewport={'width': w + 40, 'height': h + 40}, device_scale_factor=1)
        page.goto('file://' + SRC)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(9000)
        # Strip preview chrome so each frame renders alone at true size.
        ids = page.evaluate("""(sc)=>{
          const found=[];
          document.querySelectorAll('div[id]').forEach(sec=>{
            if(!/^[0-9a-z]{1,4}$/.test(sec.id)) return;
            const lbl=sec.querySelector('span[style*="letter-spacing"]');
            const fr=[...sec.querySelectorAll('div')].find(d=>{
              const z=parseFloat(d.style.zoom||'0');
              return z>0 && z<1 && d.style.width && d.style.height;});
            if(!fr) return;
            fr.style.zoom=String(sc);
            fr.setAttribute('data-cap',sec.id);
            found.push({id:sec.id,label:lbl?lbl.textContent.trim():sec.id,
                        w:parseInt(fr.style.width),h:parseInt(fr.style.height)});
          });


  const NAMES=/Julie Gibson Clark|Courtney Donofrio|Slowest[- ]Aging|Slowest Ager|Longevity Life Academy Instructor|Founding Faculty/i;
  // Enlarge the credit block with a TRANSFORM, not font-size: siblings never reflow,
  // so the CTA row and everything else stay exactly where the design put them.
  const seen=new Set();
  document.querySelectorAll('div,span,p').forEach(x=>{
    if(x.childElementCount>0) return;
    const t=(x.textContent||'').trim(); if(!t||!NAMES.test(t)) return;
    let blk=x;
    for(let i=0;i<3 && blk.parentElement;i++){
      const pt=(blk.parentElement.textContent||'').trim();
      if(pt.length<=t.length+64 && NAMES.test(pt)) blk=blk.parentElement; else break;
    }
    if(seen.has(blk)) return; seen.add(blk);
    const fr=blk.closest('div[style*="zoom"]')||blk.offsetParent||document.body;
    const fw=fr.clientWidth||1080, fh=fr.clientHeight||1080;
    const r=blk.getBoundingClientRect(), pr=fr.getBoundingClientRect();
    const left=r.left-pr.left, top=r.top-pr.top;
    let k=2;
    // never let the enlarged block leave the frame
    k=Math.min(k, (fw-left-4)/Math.max(r.width,1), (fh-top-4)/Math.max(r.height,1));
    if(k<1.15) k=1.15;
    const bottomAnchored = (top + r.height) > fh*0.72;
    if(bottomAnchored){
      k=Math.min(2,(fw-left-4)/Math.max(r.width,1),(top+r.height-4)/Math.max(r.height,1));
      if(k<1.15) k=1.15;
      blk.style.transformOrigin='left bottom';
    } else {
      blk.style.transformOrigin='left top';
    }
    blk.style.transform='scale('+k+')';
  });
          // Enlarge the 'Make longevity' / 'automatic.' headline on the 3A-3E Julie set.
          // These layouts absolutely-position the sub-line 'Taught live by ...' just below
          // the italic word, so we (1) size up the headline safely, (2) shrink to fit,
          // and (3) shift 'Taught live by ...' downward by the extra descender height.
          document.querySelectorAll('div[data-cap]').forEach(fr=>{
            const id=fr.getAttribute('data-cap');
            if(!/^3[a-e]$/.test(id)) return;
            const Z=parseFloat(fr.style.zoom||'1')||1;
            const frR=fr.getBoundingClientRect();
            const FW=frR.width/Z;
            let deltaAuto=0;
            [...fr.querySelectorAll('div,span,p')].forEach(el=>{
              if(el.childElementCount>0) return;
              const t=(el.textContent||'').trim();
              if(t!=='Make longevity'&&t!=='automatic.') return;
              const fs=parseFloat(getComputedStyle(el).fontSize);
              let nf=Math.round(fs*1.32);
              el.style.fontSize=nf+'px';
              el.style.lineHeight='1.02';
              el.style.whiteSpace='nowrap';
              for(let g=0;g<12;g++){
                const w=el.getBoundingClientRect().width/Z;
                if(w<=FW*0.88) break;
                nf=Math.max(fs, nf-4);
                el.style.fontSize=nf+'px';
                if(nf===fs) break;
              }
              if(t==='automatic.') deltaAuto=Math.max(deltaAuto, nf-fs);
            });
            // Push the 'Taught live by ...' sub-headline down by the descender delta so
            // it isn't overlapped by the enlarged italic 'automatic.'.
            if(deltaAuto>0){
              [...fr.querySelectorAll('div,span,p')].forEach(el=>{
                if(el.childElementCount>0) return;
                const t=(el.textContent||'').trim();
                if(!/^Taught live by /.test(t)) return;
                el.style.transform='translateY('+Math.round(deltaAuto*0.9)+'px)';
              });
            }
          });
          document.body.style.background='#05070d';
          return found;}""", scale)
        page.wait_for_timeout(2500)
        for meta in ids:
            el = page.query_selector(f'div[data-cap="{meta["id"]}"]')
            if not el:
                print('MISS', meta['id']); continue
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(280)
            order = PRIORITY.index(meta['id']) if meta['id'] in PRIORITY else 99
            name = f"LLA_CONCEPT_{order:02d}_{meta['id'].upper()}_{slug(meta['label'])}_{w}x{h}.png"
            el.screenshot(path=os.path.join(OUT, name))
            if scale == 1.0:
                report.append({'id': meta['id'], 'label': meta['label'], 'order': order,
                               'file_1080': f'concepts/{name}',
                               'file_1440': f"concepts/{name.replace('1080x1080', '1440x1440')}"})
            print('rendered', name)
        page.close()
    br.close()
report.sort(key=lambda r: r['order'])
json.dump(report, open(os.path.join(ROOT, 'concepts_report.json'), 'w'), indent=2)
print('done', len(report), 'concepts x 2 sizes')
