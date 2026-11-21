# The World Today — 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Azet17/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Azet17/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A 1024x1024 newspaper front page summing up Saturday 21 November 2026's
world news in a single image. Six stories in a 2x3 grid, each with a tag,
headline, short summary, and a pictogram drawn entirely in code with Pillow —
no photos, no copied artwork.

## The six stories

1. **Markets** — US stocks plunge in a deepening AI sell-off: Nasdaq falls
   5.28%, Nvidia drops about 14% in Friday's rout.
2. **Weather** — Cyclone Akvan crosses the Odisha coast near Gopalpur,
   bringing strong winds and heavy rainfall.
3. **Ukraine** — Russian missile and drone strikes hit Kryvyi Rih: 2 dead,
   42 injured, including 4 children.
4. **Brazil** — Imprisoned ex-president Jair Bolsonaro taken to hospital
   with severe abdominal pain.
5. **Pakistan** — Suicide car bombing at a security checkpoint kills 5,
   injures 13.
6. **Sport** — India fight back against New Zealand in the Wellington Test:
   159/1 at stumps on Day 2, trailing by 209.

## How to run

```sh
python3 draw.py          # regenerates entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

`main.py` uses only the Python standard library, performs no network access,
and verifies the copied file with sha256. Two runs write identical bytes.
