# The World in One Day — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/adhiejoey/makefun-news-image-24/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/adhiejoey/makefun-news-image-24/reward.svg)](https://make.fun/bounty/news-image-20261124)

A single 1024×1024 image summing up Tuesday 24 November 2026's world news —
35 stories from 7 regions, every one verified first-reported on that Tuesday
(UTC) against wire-grade sources. This is a resubmission: the first entry
scored low in round 2, so this build was made fresh with illustrated story
panels and a full date audit.

## What's on the page

- **Masthead** — "TUESDAY 24 NOVEMBER 2026", 35 stories · 7 regions, and the
  day in numbers (2 killed · $41bn · 11 hurt · M5.3 · 26 dead · 23 hurt).
- **Timeline** — the day in UTC, 01:32 → 14:50.
- **3 illustrated leads** — Russian strike kills 2 in Zaporizhzhia
  (CONFIRMED, Reuters); Sanofi buys Insmed for $41bn in cash (OFFICIAL,
  Sanofi/WSJ); Riyadh tower hit again, 11 hurt (CLAIM, Reuters/AFP).
- **10 illustrated cards** — Gaza, Nepal quake, Banten fire, Seoul jets,
  Berlin DELTA, Solomons pact, Shenzhou-24 crew, Benghazi, Baghdad, Congo Ebola.
- **ALSO TODAY** — 22 more one-liners, numbered 14–35, so the count is auditable.
- **Dot world map** — numbered pins for the 13 lead/card stories + region counts
  (Europe 13, Middle East 7, Asia 9, Oceania 2, Africa 2, S. America 1,
  N. America 1).
- **DATE CHECK** — 15 excluded near-misses with their true dates (ICJ Myanmar
  ruling Thu 19 Nov; COP31 Sun 22 Nov; Merkury sinking Sun 22 Nov; US measles
  status Mon 17 Nov; and 11 Monday 23 Nov items), plus 3 "not yet" items.
- **Footer** — sources (Reuters · AP · AFP · UN News · Xinhua · USGS · Sanofi ·
  Ukraine MoD) and the CONFIRMED / OFFICIAL / REPORTED / CLAIM legend.

## How it is built

`gen.py` (Python 3 + Pillow, no network) draws the whole page from scratch:
serif masthead, gradient skies, custom scene drawings for every lead and card
(a damaged apartment block, a $41bn chart, the PIF Tower at night, a
seismograph, a rocket, a hospital, and more), drop shadows and a raised
DATE CHECK box for depth. Run it with `python3 gen.py`; it writes `entry.png`
next to itself, deterministically.

`main.ts` (Node 22, standard library only) copies that `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`. Run it twice and
the output bytes are identical.

## Verification

- Every story's first-reported UTC date was checked against its source with
  web search during the build; the 7 wrong dates from the first entry
  (including the lead) are excluded and named in the DATE CHECK box.
- Legibility was checked at 300px wide: masthead, lead headlines and all
  illustrated panels still carry the page.
