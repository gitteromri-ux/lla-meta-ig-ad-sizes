#!/usr/bin/env python3
"""Render masterclass-event.html (zoom + fold concepts) to exact-pixel PNGs in ads-masterclass/.
Pattern of render.py: viewport = exact size, deviceScaleFactor=1, wait for window.__ready, screenshot clip."""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
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
CONCEPTS = ['zoom']
GUIDES = '--guides' in sys.argv
OUT = os.path.join(ROOT, 'ads-masterclass')
os.makedirs(OUT, exist_ok=True)
report = []

with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for c in CONCEPTS:
        for f, (w, h, tag) in SIZES.items():
            for guide in ((0, 1) if GUIDES else (0,)):
                page = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                page.goto(f'file://{ROOT}/masterclass-event.html?c={c}&f={f}&guide={guide}')
                page.wait_for_function('window.__ready===true', timeout=30000)
                page.wait_for_timeout(350)
                m = page.evaluate('window.__meta')
                name = f'LLA_MASTERCLASS_EVENT-{c.upper()}_{tag}' + ('_SAFEZONE' if guide else '') + '.png'
                page.screenshot(path=os.path.join(OUT, name), clip={'x': 0, 'y': 0, 'width': w, 'height': h})
                page.close()
                if not guide:
                    report.append({'concept': c, 'format_key': f, 'file': f'ads-masterclass/{name}',
                                   'output_w': w, 'output_h': h, 'layout': m['layout'],
                                   'comp_scale': m['sc'], 'safe_top': m['safeTop'], 'safe_bottom': m['safeBottom'],
                                   'safe_side': m['insetX'], 'mock_src': m['mockSrc'],
                                   'mock_render_px': m['mockRenderPx'], 'mock_full_uncropped': m['mockContainFull'],
                                   'fits': m['fits']})
                print('rendered', name, 'fits=' + str(m['fits']), 'sc=' + str(m['sc']),
                      'mock=' + str(m['mockRenderPx']), 'box=' + str(m['box']), 'over=' + str(m['textOverflow']) + str(m['cardOverflow']))
    br.close()
json.dump(report, open(os.path.join(ROOT, 'render_masterclass_event_report.json'), 'w'), indent=2)
print('done', len(report), 'ads')
