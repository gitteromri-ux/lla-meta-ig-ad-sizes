# LLA · Meta & Instagram Paid Media — Master Size Pack

Live download gallery: **https://gitteromri-ux.github.io/lla-meta-ig-ad-sizes/**

Two approved lead-card banners from *Lead Cards · Layout A Final*, each exported at **five exact Meta-accepted pixel sizes**. The card artwork is pixel-identical across all ten files — identical fonts (Playfair Display, Playfair Display Italic, Inter), identical type sizes, identical neon geometry. Rendered at **card scale 1.000** on every export: nothing resampled, nothing reflowed, nothing cropped.

## Banners

| ID | Banner | Headline | Palette |
|---|---|---|---|
| 7A | Courtney Donofrio | Decode Your Biomarkers. *Extend Your Life.* | Neon blue |
| 7B | Julie Gibson Clark | Make longevity *automatic.* | Warm gold |

## Sizes — all five are native Meta Ads Manager accepted dimensions

| Ratio | Pixels | Placements | Safe zone applied |
|---|---|---|---|
| 1:1 | **1080 × 1080** | FB Feed · IG Feed · Explore · Marketplace · Search | 5% all edges |
| 4:5 | **1080 × 1350** | IG Feed (recommended) · FB Feed vertical | 5% all edges |
| 9:16 | **1080 × 1920** | IG Stories · Reels · FB Stories · Audience Network | 250 px top · 340 px bottom · 5.5% sides |
| 1.91:1 | **1200 × 628** | FB link ads · Right column · Messenger inbox · Marketplace | 5% all edges |
| 16:9 | **1920 × 1080** | FB Feed landscape · In-stream · Instant Articles | 5% all edges |

Specifications per the [Meta Ads Guide — image ad specifications](https://www.facebook.com/business/ads-guide/image).

### Why 250 / 340 px on 9:16
Instagram and Facebook overlay the profile row at the top and the caption, CTA button and audio bar at the bottom of every Story and Reel — roughly the top 250 px and bottom 340 px of a 1080 × 1920 frame. All headline, price, logo and Trustpilot copy in the 9:16 exports sits inside the surviving centre band. The card artwork was **repositioned, never resized**, to achieve this.

## Files

```
ads/      10 upload-ready PNGs        LLA_<BANNER>_<RATIO>_<W>x<H>.png
guides/   10 safe-zone overlay proofs LLA_<BANNER>_<RATIO>_<W>x<H>_SAFEZONE.png
LLA_META_IG_ALL_SIZES.zip             all 10 ads
LLA_SAFEZONE_GUIDES.zip               all 10 guides
banner.html                           parametric master (source of truth)
render.py                             exact-pixel renderer
render_report.json                    per-file audit record
assets/                               original photography, logo, Trustpilot mark, fonts
```

Delivery files are **PNG · sRGB · 24-bit**, 0.8–2.6 MB each — well inside Meta's 30 MB per-image limit and lossless, so no JPEG artefacts around the neon glow or the serif type.

## Reproduce

```bash
pip install playwright pillow && python -m playwright install chromium
python render.py
```

`render.py` drives headless Chromium at `device_scale_factor=1` and clips to the exact output rectangle, so output pixels equal browser pixels with no interpolation step.

## Audit record

Every PNG was opened and dimension-verified after render. `render_report.json` records, per file: output width, output height, safe-zone pass/fail, and card render scale. All ten: **safe zone pass, card scale 1.000**.

---
Produced by **Gita Agency** for **Longevity Life Academy** (eTeacher Group).
