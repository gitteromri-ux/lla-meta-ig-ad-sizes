# Masterclass banner brief (shared by all agents) — 2026-09-24

Repo: /home/user/workspace/masterclass-handover/launch-materials/lla-meta-ig-ad-sizes (git, GitHub Pages: https://gitteromri-ux.github.io/lla-meta-ig-ad-sizes/)
DO NOT modify: adset-new.html, blueprint.html, banner.html, ads/, six-v4/, rounds/, concepts/ (the existing tab must stay exactly as is).
All new output goes to: ads-masterclass/  (PNG, exact pixel sizes, deviceScaleFactor=1) and new HTML templates named masterclass-*.html.
Renderer: python3 + playwright chromium (installed by the orchestrator; wait until `grep -q PLAYWRIGHT_DONE /tmp/pw_install.log`). Copy the pattern of render.py (viewport = exact size, wait for window.__ready, screenshot clip). Use `--force-color-profile=srgb`.
Fonts: ONLY assets/fonts/PlayfairDisplay.ttf, PlayfairDisplay-Italic.ttf, Inter.ttf (already referenced in templates). Display/italic line = Playfair Italic. No other fonts.
Logo: assets/lla_logo_oneline.png (in-card) — never restyle, recolor, stretch or crop the logo. Masterclass assets logo: ../lla-masterclass-assets/parts/lla-logo-transparent.png (1314x596, RGBA) if a standalone logo is needed.
Images: never distort (object-fit: cover with sensible object-position only), never let text overlap Julie's face, never let anything be cut by the safe zone. Keep the SAME background photos as today (julie_couch_a_web.jpg, zoom_class_web.jpg) in the converted banners.

## Exact masterclass copy (use verbatim, nothing invented)
- Headline line 1 (Playfair regular/bold, white): `The Longevity`
- Headline line 2 (Playfair ITALIC, gold/blue gradient like today): `Masterclass of the Year`
- Sub line: `Learn to age slower, live on Zoom with Julie Gibson Clark.`
- Format line: `60 minutes live · Tue, Oct 27 · 7 PM ET  or  Sat, Nov 14 · 1 PM ET`
- Bullets (max 3, exactly these):
  1. `60 minutes live with Julie on Zoom`
  2. `Her full daily protocol`
  3. `VIP: private 30-minute Q&A + $249 Blueprint credit`
- Price block: `From $49` (big, gold gradient) · `$49 Standard · $79 VIP` · `one payment`  — NO strikethrough price, NO "% off", NO "/ mo", NO promo label.
- CTA: `Enroll now` (unchanged). Trustpilot `4.6 on Trustpilot` + stars (unchanged).
- Byline chip (unchanged): `Julie Gibson Clark` / `2nd Slowest-Aging Person on Earth`
- Optional small kicker: `Live on Zoom · No replay`  (only if the layout has an existing slot for a kicker; do not add new elements otherwise)

## FORBIDDEN words/claims
PDF, certificate, "limited to N seats", "50 people", replay included, Q&A for the $49 tier, any discount, "35% off", "$445", "$289", "/ mo", "18 live sessions", "Small groups", "Six Pillars", "Make longevity automatic", "Blueprint" as the product (only inside the VIP bullet as "$249 Blueprint credit").

## Sizes (same keys/tags as render.py SIZES)
1x1 1080x1080 · 1x1hi 1440x1440 · 4x5 1080x1350 · 4x5hi 1440x1800_META-RECOMMENDED · 9x16m MESSENGER-STORY 1080x1920 · 9x16 STORIES-REELS 1080x1920 · 9x16hi STORIES-REELS 1440x2560_META-RECOMMENDED · 191x1 1200x628 · 16x9 1920x1080

## Quality gate before you report
Open every PNG you rendered (PIL thumbnail + `read` the image) and check: nothing clipped, no text over Julie's face, text contrast readable, logo intact, no forbidden words, exact pixel size. Report the list of files with sizes. Do not commit/push — the orchestrator does.
