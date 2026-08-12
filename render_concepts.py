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
