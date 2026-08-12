#!/usr/bin/env python3
"""Render Meta / Instagram ad sizes to exact-pixel PNGs (deviceScaleFactor=1, no resampling)."""
import os, json
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
BANNERS = ['courtney', 'julie']
report = []

with sync_playwright() as p:
    br = p.chromium.launch(args=['--force-color-profile=srgb', '--disable-lcd-text'])
    for b in BANNERS:
        for f, (w, h, tag) in SIZES.items():
            for guide in (0, 1):
                page = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                page.goto(f'file://{ROOT}/banner.html?b={b}&f={f}&guide={guide}')
                page.wait_for_function('window.__ready===true', timeout=30000)
                page.wait_for_timeout(350)
                m = page.evaluate('window.__meta')
                sub = 'guides' if guide else 'ads'
                name = f'LLA_{b.upper()}_{tag}' + ('_SAFEZONE' if guide else '') + '.png'
                page.screenshot(path=os.path.join(ROOT, sub, name),
                                clip={'x': 0, 'y': 0, 'width': w, 'height': h})
                page.close()
                if not guide:
                    report.append({
                        'banner': b, 'format_key': f, 'file': f'{sub}/{name}',
                        'output_w': w, 'output_h': h, 'aspect': round(w / h, 4),
                        'safe_reserve_top_px': m['safeTop'], 'safe_reserve_bottom_px': m['safeBottom'],
                        'safe_reserve_side_px': m['insetX'],
                        'all_copy_inside_safe_zone': m['fits'],
                        'card_render_scale': round(m['sc'] * m['S'], 4),
                        'source_photo': m['photoSrc'], 'source_photo_px': f"{m['photoW']}x{m['photoH']}",
                        'photo_cover_scale': m['photoUpscale'],
                    })
                print('rendered', name, 'safe=' + str(m['fits']),
                      'card_sc=' + str(round(m['sc'], 3)), 'photo_x=' + str(m['photoUpscale']))
    br.close()
json.dump(report, open(os.path.join(ROOT, 'render_report.json'), 'w'), indent=2)
print('done', len(report), 'ads +', len(report), 'guides')
