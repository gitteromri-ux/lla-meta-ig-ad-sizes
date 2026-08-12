#!/usr/bin/env python3
"""Render Meta / Instagram ad sizes to exact-pixel PNGs (deviceScaleFactor=1, no resampling)."""
import os, json, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SIZES = {
    '1x1':   (1080, 1080),
    '4x5':   (1080, 1350),
    '9x16':  (1080, 1920),
    '191x1': (1200, 628),
    '16x9':  (1920, 1080),
}
BANNERS = ['courtney', 'julie']
report = []

with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for b in BANNERS:
        for f, (w, h) in SIZES.items():
            for guide in (0, 1):
                page = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                url = f'file://{ROOT}/banner.html?b={b}&f={f}&guide={guide}'
                page.goto(url)
                page.wait_for_function('window.__ready===true', timeout=30000)
                page.wait_for_timeout(350)
                meta = page.evaluate('window.__meta')
                sub = 'guides' if guide else 'ads'
                name = f'LLA_{b.upper()}_{f}_{w}x{h}' + ('_SAFEZONE' if guide else '') + '.png'
                out = os.path.join(ROOT, sub, name)
                page.screenshot(path=out, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
                page.close()
                if not guide:
                    report.append({'banner': b, 'format': f, 'w': w, 'h': h,
                                   'file': f'{sub}/{name}', 'fits_safe_zone': meta['fits'],
                                   'card_scale': round(meta['sc'], 4)})
                print('rendered', name, 'safe_ok=' + str(meta['fits']))
    br.close()
json.dump(report, open(os.path.join(ROOT, 'render_report.json'), 'w'), indent=2)
print('done', len(report), 'ads +', len(report), 'guides')
