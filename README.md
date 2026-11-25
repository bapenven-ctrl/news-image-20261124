# news-image-20261124 — The World in One Day (V1, ATM)

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bapenven-ctrl/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bapenven-ctrl/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

![Tuesday 24 November 2026](entry.png)

**Sum up Tuesday 24 November 2026 in one image.** 42 stories, 7 regions,
every one dated Tuesday 24 November 2026 (UTC).

## What the picture shows

- **DATE CHECK first:** 18 items left out because they happened or were
  first reported before Tuesday — COP31's no-deal itself (Sun/Mon),
  BepiColombo (Sat), the Democrats' House win (Sun), the Nepal PM's India
  visit (Mon), Tajikistan leaving the ICC (Mon), the Chapo Isidro capture
  (Sat), the Cikande fire itself (Sat), ICE Seattle (Sun), and more.
- **THE DAY DECIDED — five verdicts:** Huawei guilty on 10 of 12 counts
  (Brooklyn jury) · Senegal champions again (CAS restores the AFCON title)
  · ECHR allows pushbacks · Denmark upholds the ghetto law · Zambia
  charges its opposition leader with treason.
- **THE DAY IN EIGHT SCENES, led by the verdict:** the courtroom (Huawei),
  the leaked 700,000 Russian dead, three tankers ablaze in Hormuz, the
  Riyadh tower hit a second time in five days, Nvidia down 7%, 96 drones
  in a night over Ukraine, Poland's deliberate drone incursion, Senegal's
  trophy.
- **TUESDAY'S MARKETS:** Nvidia −7% · Anthropic under its $83 IPO ·
  TAIEX +9% · KOSPI +7.5% · Nikkei +3.9% · Sanofi $41bn.
- **THE REST OF THE DAY:** 34 more stories in three region columns.

## How it is made

`render.py` draws the whole front page procedurally with Pillow — no
external assets, no network, no clock, no randomness. `main.py` copies the
rendered `entry.png` to the output directory the grader names, so two runs
write identical bytes.

```sh
python3 render.py entry.png   # draw the picture (1024x1024, < 1 MiB)
python3 main.py               # place it in $MAKEFUN_OUTPUT_DIR/entry.png
```

## Sources

Reuters, BBC, AFP, AP, Al Jazeera, The Guardian, SCMP, CNBC, France 24 —
wires read to 00:15 UTC Wed 25 Nov 2026. Scenes are drawn illustrations of
reported events, not photographs. Story list: OneTurn day page for
24 Nov 2026 (133 stories from 925 headlines), cross-checked by web search
for the overnight 96-drone barrage.
