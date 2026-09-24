#!/usr/bin/env python3
"""Build adset-masterclass.html (separate tab) from ads-masterclass/*.png. Never touches adset-new.html."""
import os, re, zipfile
from PIL import Image
ROOT=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(ROOT,'ads-masterclass')
src=open(os.path.join(ROOT,'adset-new.html'),encoding='utf-8').read()
head=src.split('<body>')[0].replace('Adset New — Updated banners','Masterclass — banner set')
files=sorted(f for f in os.listdir(D) if f.lower().endswith('.png'))
LABEL={'1x1_1080x1080':('1:1 · 1080×1080','Square feed'),'1x1_1440x1440':('1:1 · 1440×1440','Hi-res square'),
 '4x5_1080x1350':('4:5 · 1080×1350','Feed'),'4x5_1440x1800_META-RECOMMENDED':('4:5 · 1440×1800','Meta recommended · Feed'),
 '9x16_MESSENGER-STORY_1080x1920':('9:16 · 1080×1920','Messenger Story'),'9x16_STORIES-REELS_1080x1920':('9:16 · 1080×1920','Stories + Reels'),
 '9x16_STORIES-REELS_1440x2560_META-RECOMMENDED':('9:16 · 1440×2560','Meta recommended · Stories/Reels'),
 '191x1_1200x628':('1.91:1 · 1200×628','Link banner'),'16x9_1920x1080':('16:9 · 1920×1080','Widest · in-stream')}
GROUPS=[('LLA_MASTERCLASS_7C_','Masterclass card · from Banner 7C (Blueprint layout) · same photo, same layout, masterclass copy'),
 ('LLA_MASTERCLASS_7B_','Masterclass headline · from Banner 7B (Julie layout) · same photo, same layout, masterclass copy'),
 ('LLA_MASTERCLASS_EVENT-ZOOM_','Masterclass event · Zoom room mockup (Julie + class + LLA logos)'),
 ('LLA_MASTERCLASS_EVENT-FOLD_','Masterclass event · Fold mockup')]
def card(f):
    im=Image.open(os.path.join(D,f)); w,h=im.size
    tag=next((k for k in LABEL if f.endswith(k+'.png')),None)
    lab,use=LABEL.get(tag,(f'{w}×{h}',''))
    return f'''<div class="card"><div class="frame"><img src="ads-masterclass/{f}" alt="{f}" loading="lazy"></div>
<div class="name">{lab}</div><div class="meta">{use} · actual {w}×{h}</div>
<div class="badges"><span class="badge">Masterclass copy</span><span class="badge g">From $49 · $79 VIP</span></div>
<a class="dl" href="ads-masterclass/{f}" download>⤓ Download</a></div>'''
secs=''
n=0
for pre,title in GROUPS:
    fs=[f for f in files if f.startswith(pre)]
    if not fs: continue
    n+=len(fs)
    secs+=f'<h2>{title} · {len(fs)} sizes</h2><div class="grid">'+''.join(card(f) for f in fs)+'</div>'
zp=os.path.join(ROOT,'MASTERCLASS_BANNERS.zip')
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files: z.write(os.path.join(D,f),f)
body=f'''<body>
<div class="wrap">
  <div class="hdr">
    <div class="kicker">Longevity Life Academy · The Longevity Masterclass of the Year</div>
    <h1>Masterclass banners — same designs, masterclass offer</h1>
    <div class="sub">Same photos, layouts, fonts and colors as the Blueprint set; only the copy changed to the live masterclass with Julie Gibson Clark: 60 minutes live on Zoom · Tue, Oct 27 · 7 PM ET or Sat, Nov 14 · 1 PM ET · From $49 ($49 Standard · $79 VIP, one payment). Plus new event banners built from the approved Zoom-room and fold mockups. Blueprint set unchanged at <a href="adset-new.html?v=12" style="color:#8ef5c1">adset-new</a>.</div>
    <div class="bar">
      <a class="btn btn-p" href="MASTERCLASS_BANNERS.zip" download>⤓ Download all {n} files (ZIP)</a>
      <a class="btn" href="adset-new.html?v=12">← Blueprint set (unchanged)</a>
      <a class="btn" href="https://www.longevitylifeacademy.com/julie-masterclass/#pricing">Masterclass pricing fold ↗</a>
    </div>
  </div>
  {secs}
</div></body></html>'''
open(os.path.join(ROOT,'adset-masterclass.html'),'w',encoding='utf-8').write(head+body)
print('page built with',n,'banners; zip',os.path.getsize(zp)//1024,'KB')
