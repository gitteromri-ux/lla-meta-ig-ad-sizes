# LLA · Meta & Instagram Paid Media — Master Size Pack

Live download gallery: **https://gitteromri-ux.github.io/lla-meta-ig-ad-sizes/**

Three approved lead-card banners from *Lead Cards · Layout A Final*, each exported at **nine verified Meta-accepted pixel sizes** — 27 upload-ready files. The card artwork is pixel-identical across all ten files — identical fonts (Playfair Display, Playfair Display Italic, Inter), identical type sizes, identical neon geometry. Rendered at **card scale 1.000** on every export: nothing resampled, nothing reflowed, nothing cropped.

## Banners

| ID | Banner | Headline | Palette |
|---|---|---|---|
| 7C | Julie Gibson Clark | Master your tailored *Longevity Blueprint* | Blue card, gold Enroll now CTA |
| 7A | Courtney Donofrio | Decode Your Biomarkers. *Extend Your Life.* | Neon blue |
| 7B | Julie Gibson Clark | Make longevity *automatic.* | Warm gold |

## Sizes — every one verified against Meta's published specs (12 Aug 2026)

| Ratio | Pixels | Placements this file is for | Safe zone applied |
|---|---|---|---|
| 1:1 | **1080 × 1080** | FB Feed · IG Feed · Explore · Marketplace · Search | 54 px all edges |
| 1:1 | **1440 × 1440** | Same, at Meta's higher recommended resolution | 72 px all edges |
| 4:5 | **1080 × 1350** | IG Feed · FB Feed vertical — tallest ratio Feed accepts | 68 px top/bottom · 54 px sides |
| 4:5 | **1440 × 1800** | Same, at Meta's higher recommended resolution | 90 px top/bottom · 72 px sides |
| 9:16 | **1080 × 1920** *(Stories build)* | IG Stories · FB Stories | 250 px top · 340 px bottom · 64 px sides |
| 9:16 | **1080 × 1920** *(Reels build)* | IG Reels · FB Reels · Audience Network | 250 px top · **672 px bottom** · 64 px sides |
| 1.91:1 | **1200 × 628** | FB link ads · Right column · Messenger · Marketplace | 54 px top/bottom · 103 px sides |
| 16:9 | **1920 × 1080** | FB Feed landscape · In-stream · Instant Articles | 54 px top/bottom · 96 px sides |

Across all placements: **minimum width 600 px**, minimum height 600 px (1:1) or 750 px (4:5), **maximum file size 30 MB**, JPG or PNG. Sources: [Meta Ads Guide — image specifications](https://www.facebook.com/business/ads-guide/image), [Sprout Social](https://sproutsocial.com/insights/facebook-ad-sizes/), [Hootsuite 2026 cheat sheet](https://blog.hootsuite.com/facebook-ad-sizes/).

## The two rules that cause cropping

1. **Never put a 9:16 file into a Feed placement.** Feed accepts 1.91:1 down to 4:5 only — 4:5 is the tallest ratio it will show. A 1080 × 1920 file dropped into Feed is centre-cropped to 4:5 and loses the top and bottom of the card. Feed gets the 4:5 or 1:1 files; Stories and Reels get the 9:16 files.
2. **Stories and Reels do not share a safe zone.** Reels overlays the caption, engagement rail and CTA over roughly the bottom 672 px, versus about 340 px on Stories. A file safe on Stories can still be covered on Reels. This pack therefore ships them as **two separate files**, each built to its own reserve.

## Files

```
ads/      27 upload-ready PNGs        LLA_<BANNER>_<RATIO>_<W>x<H>.png
guides/   27 safe-zone overlay proofs LLA_<BANNER>_<RATIO>_<W>x<H>_SAFEZONE.png
LLA_META_IG_ALL_SIZES.zip             all 27 ads
LLA_SAFEZONE_GUIDES.zip               all 27 guides
banner.html                           parametric master for 7A / 7B
blueprint.html                        parametric master for 7C
render.py                             exact-pixel renderer (7A / 7B)
render_blueprint.py                   exact-pixel renderer (7C)
render_report.json                    per-file audit record
assets/                               original photography, logo, Trustpilot mark, fonts
```

Delivery files are **PNG · sRGB · 24-bit**, 0.8–4.5 MB each — well inside Meta's 30 MB per-image limit and lossless, so no JPEG artefacts around the neon glow or the serif type.

## Reproduce

```bash
pip install playwright pillow && python -m playwright install chromium
python render.py
```

`render.py` drives headless Chromium at `device_scale_factor=1` and clips to the exact output rectangle, so output pixels equal browser pixels with no interpolation step.

## Audit record

Every one of the 27 files was downloaded back from the live site and re-measured by **reading the raw PNG IHDR header bytes** — not by trusting the renderer that produced it, and not by trusting the filename. Dimensions, colour type and bit depth confirmed independently; all 27 matched. `render_report.json` records per file: output width, output height, safe-zone reserve in pixels on every edge, whether all copy falls inside it, and the card render scale. All 27: **safe zone pass**.

The 1440 files are true re-renders at higher resolution, not upscales of the 1080 files — every source photograph in this pack is 1600 px wide or larger.

---
Produced by **Gita Agency** for **Longevity Life Academy** (eTeacher Group).
