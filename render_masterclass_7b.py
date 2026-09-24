#!/usr/bin/env python3
"""Render Masterclass 7B (Julie, gold theme) to exact-pixel PNGs in ads-masterclass/ (deviceScaleFactor=1)."""
import os, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'ads-masterclass')
os.makedirs(OUT, exist_ok=True)
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
report = []

with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for f, (w, h, tag) in SIZES.items():
        page = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        page.goto(f'file://{ROOT}/masterclass-7b.html?b=julie&f={f}')
        page.wait_for_function('window.__ready===true', timeout=30000)
        page.wait_for_timeout(350)
        m = page.evaluate('window.__meta')
        name = f'LLA_MASTERCLASS_7B_{tag}.png'
        page.screenshot(path=os.path.join(OUT, name),
                        clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        page.close()
        report.append({
            'format_key': f, 'file': f'ads-masterclass/{name}',
            'output_w': w, 'output_h': h,
            'all_copy_inside_safe_zone': m['fits'],
            'card_render_scale': round(m['sc'] * m['S'], 4),
            'text_overflow': m.get('overflow'),
        })
        print('rendered', name, 'fits=' + str(m['fits']),
              'card_sc=' + str(round(m['sc'], 3)), 'overflow=' + str(m.get('overflow')))
    br.close()
json.dump(report, open(os.path.join(ROOT, 'render_masterclass_7b_report.json'), 'w'), indent=2)
print('done', len(report), 'ads')
