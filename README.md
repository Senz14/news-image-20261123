# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Senz14/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Senz14/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**The world in one day — Monday, 23 November 2026.** One original front page summing up the day's world news in six panels: the stories that happened, or were first reported, around 23 November 2026.

## The six stories

1. **COP31 ends with no deal** — UN climate talks in Antalya close without an agreement, the first failure since 2009, as nearly 200 nations split over fossil fuels (Reuters, AFP, UN News).
2. **Ukraine sinks Russian warship in Libya** — President Zelenskyy says seven sea drones sank the corvette Merkury at Benghazi, taking the war to a new sea (Reuters, AP).
3. **Nvidia brings back its chief** — Jensen Huang returns as CEO 11 days after resigning; shares jump about 33% and the S&P 500 climbs 4.8% (Reuters).
4. **AI sell-off hits Asia** — South Korea's Kospi falls 3.3% to its lowest close since January as doubts over AI spending spread (Reuters, AP).
5. **Strike kills 11 in Dymer** — A Russian drone strike on an apartment block near Kyiv kills 11 people, rescuers say (AP, Reuters).
6. **Coalition talks collapse** — Netanyahu's Likud and Eisenkot's Yashar end unity talks without a deal, leaving Israel's next government uncertain (Al Jazeera, Reuters).

## The image

`entry.png` (1024×1024) is an original illustration drawn for this bounty by `draw.py` — no news-agency photographs, no copied artwork. Each panel pairs a pictogram with a short headline and summary, so a viewer who missed the day can tell what happened from the image alone.

## Run it

No build step, no network. `main.ts` (Node 22, standard library only) copies `entry.png` to the output directory, then verifies the copy byte-for-byte (SHA-256) and reports the image's dimensions from its PNG header:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png
```

To redraw the image from scratch: `python3 draw.py` (needs Pillow).

## Files

- `entry.png` — the entry image (1024×1024 PNG).
- `draw.py` — the program that draws `entry.png` (Pillow, standard fonts).
- `main.ts` — the entry program: copies `entry.png` to `/output/entry.png` and verifies the copy.

<sub>Entered on [make.fun](https://make.fun/?ref=jkmc4mts&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
