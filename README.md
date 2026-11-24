# One day's world news — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/adhiejoey/makefun-news-image-24/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/adhiejoey/makefun-news-image-24/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for make.fun's **"Sum up 24 November's world news in one image"**
([news-image-20261124](https://make.fun/bounty/news-image-20261124)): one
1024×1024 broadsheet that sums up Tuesday 24 November 2026.

## The image

A cream-paper broadsheet, drawn from scratch:

- **Masthead** naming the day: Tuesday, 24 November 2026.
- **The lead**: the International Court of Justice finding Myanmar guilty of
  genocide against the Rohingya — first reported 24 Nov, 03:00 UTC.
- **A world map** with a dot for each of the 36 stories that has a place
  (4 stories are worldwide or in space).
- **A UTC timeline** of the day, from the overnight burst (01:06–03:00) to
  Brentford 4–0 Everton at full time.
- **40 stories, all sourced**, across world news, politics, climate, science,
  health, markets, tech and sport — each with its place, its source and a
  confidence tag (HIGH = confirmed by ≥2 outlets or a primary source,
  MED = single source, or a claim as reported).
- **A DATE CHECK box**: every story happened, or was first reported, on
  Tuesday 24 November 2026 — checked against Reuters, UN News, the Kyiv
  Independent and the day's live briefings.

## How it was made

`generate.py` (Python + Pillow, run locally while building) draws
`entry.png` from the 40 researched stories. `main.ts` (Node 22, standard
library only) copies that image to `/output/entry.png`. It takes no input,
reaches for no network and writes identical bytes on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs write byte-identical output (sha256
`d11e40e0a5822267438c5e911b7b3421cdacfbd190ce34ed41b9c53ece9afa9a`).
The image is a whole PNG, 1024×1024, 203,436 bytes — inside the gate's
1 MiB cap. Every story's date was checked a second time against its source
before this was finished: all 40 happened, or were first reported, on
Tuesday 24 November 2026.

## Sources

Reuters · UN News · Kyiv Independent · OneTurn · Principia · Daily Summary
of World · IqMIA · IANS · Cricinfo · SuMarket · The Guardian ·
Financial Times.
