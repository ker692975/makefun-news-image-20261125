# News Image — 25 November 2026

make.fun bounty: https://make.fun/bounty/news-image-20261125

- Prize: $100 (50 places: 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Deadline: 2026-11-27 08:00 Asia/Shanghai
- Deliverable: a **program** that generates one image summing up 25 November 2026 world news.

## How it works

`main.py` is Python 3.13, standard library only (`zlib`, `struct`, `binascii`,
`os`, `pathlib`). No network, no randomness, no timestamps, no external files,
no Pillow. It renders a 1024×1024 newspaper poster with a built-in 5×7 bitmap
font and encodes it as a PNG with a hand-written encoder.

Run it:

```sh
python3 main.py            # writes /output/entry.png
OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
```

Verified 2026-11-26: two runs write byte-identical files —
SHA-256 `d5247f08fbf108f24efe6e8c9921a109a682c50da74017cff779d5f85a96a4a4`,
14,686 bytes (limit 1 MiB), 1024×1024 (limit 1024×1024), valid PNG header.

## The 10 stories (all 25 November 2026 unless noted)

1. Hormuz: IRGC said two oil tankers struck naval mines, exploded/caught fire — Just Security / AP
2. Houthis attacked Saudi Ras Tanura refinery; earlier Riyadh skyscraper strike injured 11 — Just Security
3. Russia-Ukraine: Odesa strike killed 2, injured 3 incl. a child; Kyiv flat fire injured 2; Ukraine drones hit Rosneft Syzran & Kuibyshev — Just Security
4. Huawei convicted in US federal court: trade secrets / bank fraud, not guilty of racketeering (24–25 Nov) — AP / Just Security
5. US proposes tariffs on 14 economies incl. China, EU, India — OneTurn / USTR
6. Markets: KOSPI −6.16%, Nikkei −2.78%, Nasdaq −1.5%, Dow first close above 50,000 at 50,018.70 — AP / Reuters
7. Colombia: Cartagena supermarket hostages freed, one captor killed — Principia / AP
8. Australia–Solomon Islands treaty precluding foreign military base — Just Security
9. Sudan: RSF drone strikes killed 19, wounded 20 — Just Security
10. Shenzhou-24 docked with Tiangong, carrying Pakistan's first astronaut — China Manned Space Agency

Photos are deliberately not used: the program must be self-contained and
deterministic in a no-network sandbox, so the poster is typographic — title,
date, 10 numbered headlines, source line in the footer.

## Files

- `main.py` — the entry program (root entry point)
- `README.md` — this file
- `LICENSE` — MIT License
- `TRANSCRIPT.md` — session transcript for this build
- `makefun-run.json` — run record (`makefun-run/1`) for the build record

## Status

Preparation only. Nothing was submitted to make.fun, no wallet was connected
or used to sign, no payment was made, and nothing was pushed to GitHub yet.
Submission requires a public GitHub repo and a Solana wallet signature,
which are separate steps.

make.fun account: @er-kai — GitHub account: @ker692975
