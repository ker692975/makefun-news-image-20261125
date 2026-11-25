# News Image — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ker692975/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ker692975/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Built by an AI agent for make.fun's "Sum up 25 November's world news in one image" bounty, $100 in USDC.

make.fun bounty: https://make.fun/bounty/news-image-20261125

- Prize: $100 (50 places: 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Deadline: 2026-11-27 08:00 Asia/Shanghai
- Deliverable: a **program** that generates one image summing up 25 November 2026 world news.

## How it works (v3, current)

`main.py` is Python 3.13, standard library only (`zlib`, `struct`, `binascii`,
`os`, `pathlib`). No network, no randomness, no timestamps, no external files,
no Pillow, no photos. It renders a 1024×1024 newspaper front page with a
built-in 5×7 bitmap font and encodes it as a PNG with a hand-written encoder.
All illustrations are flat vector shapes drawn in code (rocket, line chart,
bar chart, small pictograms, simplified world map).

Run it:

```sh
python3 main.py            # writes /output/entry.png
OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
```

Verified 2026-11-26 (v3): two runs write byte-identical files —
SHA-256 `45c75e168b6e43ee5be79ff3607478b86bcaa2b1492227ee938b356c01c1fb94`,
26,479 bytes (limit 1 MiB), 1024×1024 (limit 1024×1024), valid PNG header.

## Layout (v3)

Cream paper (#f7f2e7), black masthead "WEDNESDAY 25 NOVEMBER 2026",
"33 STORIES - 7 REGIONS - ONE DAY", region count bar
(Asia 8, Middle East 6, Europe 6, Africa 3, Americas 5, Oceania 2, Global 3),
navy KPI band (-6.2% KOSPI, 1st astronaut, 14 economies, 26 trapped,
+36% wage), UTC timeline strip, 3 headline columns with vector illustrations
(rocket night launch; KOSPI -6.2% falling line chart to 4,697.51; tariff bar
chart China 20% / EU 15% / India 25% / Vietnam 35%), numbered cards 4–13
with small pictograms and region colour tags, bottom two-column numbered
list 14–33, simplified world map with numbered dots 1–13, footer
"DATE CHECK: ALL STORIES FIRST REPORTED WEDNESDAY 25 NOVEMBER 2026".

## The 33 stories (all 25 November 2026 unless noted)

Headlines 1–3: 1. Shenzhou-24 docks with Tiangong, Pakistan's first astronaut
Zeeshan Ali aboard. 2. KOSPI -6.16% to 4,697.51, Nikkei -2.78%, Nasdaq -1.5%
on AI doubts. 3. US proposes tariffs 15–35% on 14 economies incl. China,
EU, India.

Cards 4–13: 4. IRGC says two oil tankers struck naval mines in Hormuz, caught
fire. 5. Houthis hit Saudi Ras Tanura refinery; Riyadh tower strike hurt 11.
6. Odesa strike killed 2, hurt 3 incl. a child; Kyiv flat fire hurt 2; Ukraine
drones hit Rosneft Syzran and Kuibyshev. 7. Huawei convicted in US court on
trade secrets / bank fraud, not guilty of racketeering. 8. Cartagena
supermarket hostages freed, one captor killed. 9. Australia–Solomon Islands
treaty precluding foreign military base. 10. Sudan RSF drone strikes killed 19,
wounded 20 in Damazin. 11. Bangladesh garment wage +36% to Tk17,500.
12. Java gold mine flood, 9 dead, 26 trapped. 13. Australia CPI 4.9%.

List 14–33: 14. Coalition strikes Hodeidah port. 15. Ukraine drone hits
Samara refinery, 5 dead. 16. Dow first close above 50,000 at 50,018.70.
17. Ethiopia: 11.3m children polio vaccinated. 18. Gaza strikes continue.
19. UK Met Police race review. 20. Netanyahu trial continues. 21. London Tube
strike. 22. US House Democrats hold 259 seats. 23. Cairo tanker fire kills 30.
24. UK energy price cap +26%. 25. Taiex -4.8%. 26. 112 drones in overnight
Ukraine attacks. 27. Israel strikes Hamas targets. 28. 47,000 women killed by
partner or kin in 2025, UN says. 29. Vietnam tariff 35%. 30. Japan tariff 13%.
31. China tariff 20%; EU tariff 15%. 32. Pakistani astronaut first foreign
visitor to Tiangong (detail of story 1). 33. Shenzhou-24 lifts off 00:21 UTC,
docks 03:56 UTC (timeline detail of story 1).

Sources: Just Security, AP, Reuters, USTR, Principia, China Manned Space Agency.

## Earlier versions

- v1 (text-only, 10 stories): 14,686 bytes, SHA-256
  `d5247f08fbf108f24efe6e8c9921a109a682c50da74017cff779d5f85a96a4a4`.
- v2 (10 stories with embedded CC photo thumbnails, 144×104 each): 342,076
  bytes, SHA-256 `2cd1666041696a31f4971f9614327c39c96acda3434a2b955b615e4767eb60eb`.
  v2 was prepared and its submission form was filled, but the user chose
  "directly do v3, don't submit v2" (2026-11-26 06:36), so v2 was never submitted.
  Photo sources are documented in the v2 README history; v3 uses no photos.

## Files

- `main.py` — the entry program (root entry point)
- `README.md` — this file
- `LICENSE` — MIT License
- `TRANSCRIPT.md` — session transcript for this build
- `makefun-run.json` — run record (`makefun-run/1`) for the build record

## Status

Preparation only. Nothing was submitted to make.fun, no wallet was connected
or used to sign, no payment was made. The v3 GitHub repo update and submission
are separate steps for the user.

make.fun account: @er-kai — GitHub account: @ker692975
