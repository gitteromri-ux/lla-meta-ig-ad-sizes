#!/usr/bin/env python3
"""Render the Masterclass 7C card banner (masterclass-7c.html) to exact-pixel PNGs
(deviceScaleFactor=1, no resampling). Modelled on render.py."""
import os, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'ads-masterclass')
SIZES = {
    '1x1':    (1080, 1080, '1x1_1080x1080'),
    '1x1hi':  (1440, 1440, '1x1_1440x1440'),
    '4x5':    (1080, 1350, '4x5_1080x1350'),
    '4x5hi':  (1440, 1800, '4x5_1440x1800_META-RECOMMENDED'),
    '9x16m':  (1080, 1920, '9x16_MESSENGER-STORY_1080x1920'),
    '9x16':   (1080, 1920, '9x16_STORIES-REELS_1080x1920'),
    '9x16hi': (1440, 2560, '9x16_STORIES-REELS_1440x2560_META-RECOMMENDED'),
    '191x1':  (1200, 628,  '191x1_1200x628'),
    '16x9':   (1920, 1080, '16x9_1920x1080'),
}
# in-card overflow check: every nowrap line must fit inside the card's content box
OVERFLOW_JS = """() => {
  const card = document.getElementById('card');
  const cs = getComputedStyle(card);
  const inner = card.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  const rows = {};
  for (const id of ['h1','h2','pl','sp']) {
    const el = document.getElementById(id);
    rows[id] = Math.round(el.scrollWidth);
  }
  const bul = document.getElementById('bul');
  if (bul) rows.bul = Math.max(...[...bul.children].map(c => Math.round(c.scrollWidth)));
  const price = document.getElementById('po').parentElement;
  rows.price = Math.round(price.scrollWidth);
  const cta = price.nextElementSibling;
  rows.cta = Math.round(cta.scrollWidth);
  const over = Object.entries(rows).filter(([k,v]) => v > inner + 0.5).map(([k]) => k);
  return {inner: Math.round(inner), rows, over};
}"""
os.makedirs(OUT, exist_ok=True)
report = []

with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for f, (w, h, tag) in SIZES.items():
        page = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        page.goto(f'file://{ROOT}/masterclass-7c.html?f={f}')
        page.wait_for_function('window.__ready===true', timeout=30000)
        page.wait_for_timeout(350)
        m = page.evaluate('window.__meta')
        ov = page.evaluate(OVERFLOW_JS)
        name = f'LLA_MASTERCLASS_7C_{tag}.png'
        page.screenshot(path=os.path.join(OUT, name),
                        clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        page.close()
        report.append({
            'format_key': f, 'file': f'ads-masterclass/{name}',
            'output_w': w, 'output_h': h,
            'fits': m['fits'], 'card_sc': round(m['sc'], 4),
            'safe_top': m['safeTop'], 'safe_bottom': m['safeBottom'], 'inset_x': m['insetX'],
            'card_inner_w': ov['inner'], 'row_widths': ov['rows'], 'card_overflow': ov['over'],
        })
        print('rendered', name, f'{w}x{h}', 'fits=' + str(m['fits']),
              'card_sc=' + str(round(m['sc'], 3)),
              'overflow=' + (','.join(ov['over']) or 'none'), ov['rows'], 'inner=' + str(ov['inner']))
    br.close()
json.dump(report, open(os.path.join(ROOT, 'render_masterclass_7c_report.json'), 'w'), indent=2)
print('done', len(report), 'ads')
