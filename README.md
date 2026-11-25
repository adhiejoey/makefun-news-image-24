# The World in One Day — Tuesday 24 November 2026 (resubmission)

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/adhiejoey/makefun-news-image-24/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/adhiejoey/makefun-news-image-24/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image summing up the world's news of **Tuesday 24 November 2026** — a cream-paper broadsheet drawn by `gen.py` from 35 stories, every one verified first-reported on Tuesday 24 November 2026 (UTC).

## What is on the page

- **Masthead** — TUESDAY 24 NOVEMBER 2026, 35 stories, 7 regions.
- **UTC timeline** — the day from the 01:32 UTC Nepal quake to the evening FIFA announcement.
- **The day in numbers** — 96 drones over Ukraine, the $41bn Sanofi–Insmed deal, 26 dead in Banten, 11,613 Ebola cases, the M5.3 quake, 36 Kuiper satellites.
- **Three illustrated leads** — the Russian strike on Zaporizhzhia (2 killed), Sanofi's $41bn Insmed buy, and the Riyadh tower targeted in a Houthi attack — each drawn as a custom scene, with a CONFIRMED/CLAIM label and source.
- **Ten illustrated cards** — Nepal quake, Banten toll, Ebola teams trapped, Lukashenko's Moscow offer, the EU sanctions package, FIFA's 2031 hosts, Gaza strikes, Huang's apology, the Solomons pact swap, Seoul scrambling jets — each with its own drawing.
- **ALSO ON TUESDAY** — 22 more one-line stories, numbered so the count is auditable.
- **World map** — the 13 illustrated stories pinned and numbered; region counts below.
- **DATE CHECK box** — 14 near-misses left out on purpose with their true dates (ICJ Myanmar ruling Thu 19 Nov, COP31 Sun 22 Nov, the Merkury sinking Sun 22 Nov, Nvidia's Huang reinstatement Mon 23 Nov, the Ahmadi flogging Mon 23 Nov, and more), plus two "not yet" items.

## How it is built

`gen.py` (Python 3 + Pillow, run at build time only) draws `entry.png` at 1024×1024 from the verified story list embedded in the script — no network access, no external assets. Every story was checked against wire reporting (Reuters, AP, WSJ, CNN, BBC, UN News, Anadolu) before drawing, and re-checked over the finished image. `main.ts` (Node 22, standard library only) copies that image to the grader's output directory — the program runs twice and writes the same bytes both times.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Competition: [news-image-20261124](https://make.fun/bounty/news-image-20261124) — "Sum up 24 November's world news in one image"
- Prize: $100 shared by the top 50 entries (1st $20)
- Deadline: Thursday 26 November 2026, 07:00 WIB (2026-11-26T00:00:00Z)
- This is an improved resubmission: the first entry ranked 4,782/9,063 in round 2 with no illustrated panels and 7 wrong dates; this version fixes both.
