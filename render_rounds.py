#!/usr/bin/env python3
"""Render every remaining round from the All Banners export: the live 3D glass card frames
(7A/7B/7C/6A/6B at each authored format) plus the original 18-banner campaign export."""
import os, re, json, unicodedata
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source-pages', 'LLA-All-Banners.html')
OUT = os.path.join(ROOT, 'rounds')
os.makedirs(OUT, exist_ok=True)


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'-{2,}', '-', re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-')).upper()[:56]


report = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])

    # ---- 1. live frames, rendered at native authored pixels and at 1.3333x ----
    for scale, tagsuffix in ((1.0, ''), (1440 / 1080, '_HI')):
        page = br.new_page(viewport={'width': 2100, 'height': 1400}, device_scale_factor=1)
        page.goto('file://' + SRC)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(15000)
        hid = page.evaluate("""()=>{
          let n=0;
          document.querySelectorAll('div,span,p').forEach(x=>{
            if(x.childElementCount>0) return;
            const t=(x.textContent||'').replace(/[\\s\\u00a0]/g,'');
            if(/^\\d{1,2}[:x.]\\d{1,2}$/.test(t)){x.style.visibility='hidden';n++;}
          });
          return n;}""")
        print('  hid', hid, 'proof labels')
        frames = page.evaluate("""(sc)=>{
          const out=[]; let n=0;
          const secs=[...document.querySelectorAll('div[id]')].filter(d=>/^[0-9]?[a-z]$/i.test(d.id));
          document.querySelectorAll('div').forEach(d=>{
            const z=parseFloat(d.style.zoom||'0');
            if(!(z>0&&z<1&&d.style.width&&d.style.height)) return;
            let sec=d.closest('div[id]'); let sid='x';
            let e=d; while(e){ if(e.id && /^[0-9]?[a-z]$/i.test(e.id)){sid=e.id;break;} e=e.parentElement; }
            const lbl=d.querySelector('div[style*="bottom:6px"]');
            const w=parseInt(d.style.width), h=parseInt(d.style.height);
            d.style.zoom=String(sc);
            // strip the dev proof label ("1:1", "4:5") so upload files are clean
            d.querySelectorAll('div[style]').forEach(x=>{
              const st=x.getAttribute('style')||'';
              if(st.includes('bottom:6px') && st.includes('left:16px')) x.style.display='none';
              const t=(x.textContent||'').replace(/\s|\u00a0/g,'');
              if(/^\d+:\d+$/.test(t) && x.childElementCount===0) x.style.display='none';});
            const cap='cap'+(n++);
            d.setAttribute('data-cap',cap);
            out.push({cap:cap,sid:sid,w:Math.round(w*sc),h:Math.round(h*sc),
                      label:lbl?lbl.textContent.trim():''});
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
          document.body.style.background='#05070d';
          return out;}""", scale)
        page.wait_for_timeout(3000)
        for f in frames:
            el = page.query_selector(f'div[data-cap="{f["cap"]}"]')
            if not el:
                continue
            el.scroll_into_view_if_needed(); page.wait_for_timeout(260)
            ratio = (f['label'] or '').replace(':', 'x') or f"{f['w']}x{f['h']}"
            name = f"LLA_ROUND_{f['sid'].upper()}_{slug(ratio)}_{f['w']}x{f['h']}{tagsuffix}.png"
            el.screenshot(path=os.path.join(OUT, name))
            if scale == 1.0:
                report.append({'kind': 'live-frame', 'section': f['sid'], 'ratio': f['label'],
                               'w': f['w'], 'h': f['h'], 'file': f'rounds/{name}',
                               'file_hi': f"rounds/{name.replace('.png', '_HI.png')}"})
            print('frame', name)
        page.close()

    LIVE_ONLY=os.environ.get('LIVE_ONLY')=='1'
    if LIVE_ONLY:
        json.dump(report, open(os.path.join(ROOT,'rounds_report_live.json'),'w'), indent=2)
        br.close(); raise SystemExit(0)
    # ---- 2. the original 18-banner campaign export, saved at native resolution ----
    page = br.new_page(viewport={'width': 1700, 'height': 1200}, device_scale_factor=1)
    page.goto('file://' + SRC)
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(15000)
    shots = page.evaluate("""()=>{
      const gal=[...document.querySelectorAll('img')].filter(i=>{
        const a=i.alt||''; const r=i.getBoundingClientRect();
        return i.naturalWidth>=1000 && r.width>200 && /\\u00b7/.test(a);});
      let n=0; const out=[];
      gal.forEach(i=>{const c='img'+(n++); i.setAttribute('data-cap',c);
        out.push({cap:c,alt:i.alt,w:i.naturalWidth,h:i.naturalHeight});});
      return out;}""")
    for s in shots:
        el = page.query_selector(f'img[data-cap="{s["cap"]}"]')
        if not el:
            continue
        el.scroll_into_view_if_needed(); page.wait_for_timeout(180)
        name = f"LLA_CAMPAIGN_{slug(s['alt'])}_{s['w']}x{s['h']}.png"
        # capture the element at its native pixel size, not the shrunken layout size
        page.evaluate("""(cap)=>{const i=document.querySelector(`img[data-cap="${cap}"]`);
            i.style.width=i.naturalWidth+'px'; i.style.height=i.naturalHeight+'px';
            i.style.maxWidth='none'; i.style.borderRadius='0';}""", s['cap'])
        page.wait_for_timeout(150)
        el.screenshot(path=os.path.join(OUT, name))
        report.append({'kind': 'campaign', 'label': s['alt'], 'w': s['w'], 'h': s['h'],
                       'file': f'rounds/{name}'})
        print('campaign', name)
    page.close()
    br.close()

json.dump(report, open(os.path.join(ROOT, 'rounds_report.json'), 'w'), indent=2)
print('done', len(report), 'items')
