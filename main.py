#!/usr/bin/env python3
"""Generate the make.fun bounty entry: one image summing up 25 Nov 2026 world news.

Bounty: https://make.fun/bounty/news-image-20261125
Output: /output/entry.png  (or $OUTPUT_DIR/entry.png)
Size: 1024 x 1024 PNG, at most 1 MiB, deterministic.
Version 3: newspaper front page, 33 stories, flat vector illustrations
drawn in code (no photos).

Standard library only: zlib / struct / binascii / os.
No network, no randomness, no timestamps, no external files.
Text is rendered with a built-in 5x7 bitmap font (uppercase only).
"""

import binascii
import os
import struct
import zlib
from pathlib import Path

_G = {
    "A": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "B": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    "C": [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
    "D": [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
    "E": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    "F": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    "G": [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
    "H": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "I": [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "J": [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
    "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    "M": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
    "O": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "P": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    "Q": [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    "R": [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    "S": [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
    "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
    "X": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    "Y": [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    "Z": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
    "0": [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
    "1": [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "2": [0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F],
    "3": [0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E],
    "4": [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    "5": [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
    "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    "7": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
    "8": [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    "9": [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C],
    ",": [0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08],
    "-": [0x00, 0x00, 0x00, 0x0E, 0x00, 0x00, 0x00],
    "%": [0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13],
    "(": [0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02],
    ")": [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
    "/": [0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10],
    "'": [0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00],
    ":": [0x00, 0x0C, 0x00, 0x00, 0x00, 0x0C, 0x00],
    ";": [0x00, 0x0C, 0x00, 0x0C, 0x04, 0x08, 0x00],
    "!": [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
    "?": [0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04],
    "+": [0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00],
    "=": [0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00],
    "$": [0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04],
}

def _chunk(data, name):
    return struct.pack(">I", len(data)) + name + data + struct.pack(
        ">I", binascii.crc32(name + data) & 0xFFFFFFFF
    )


def encode_png(rgb, width, height):
    """Encode raw RGB bytes as a deterministic PNG (colour type 2, no interlace)."""
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter: None
        raw.extend(rgb[y * stride:(y + 1) * stride])
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    comp = zlib.compress(bytes(raw), 9)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(ihdr, b"IHDR")
    png += _chunk(comp, b"IDAT")
    png += _chunk(b"", b"IEND")
    return png



class Canvas:
    def __init__(self, width, height, bg):
        self.width = width
        self.height = height
        self.pix = bytearray(bg * (width * height))

    def set(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pix[i:i + 3] = bytes(colour)

    def rect(self, x, y, w, h, colour):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        for yy in range(y0, y1):
            base = (yy * self.width + x0) * 3
            row = bytes(colour) * (x1 - x0)
            self.pix[base:base + (x1 - x0) * 3] = row


    def blit(self, x, y, rgb, w, h):
        """Copy a raw RGB thumbnail (bytes, w x h) onto the canvas."""
        for yy in range(h):
            base = ((y + yy) * self.width + x) * 3
            src = yy * w * 3
            self.pix[base:base + w * 3] = rgb[src:src + w * 3]

    def line(self, x0, y0, x1, y1, colour):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.set(x, y, colour)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def thick_line(self, x0, y0, x1, y1, w, colour):
        for i in range(w):
            self.line(x0, y0 + i, x1, y1 + i, colour)

    def disc(self, cx, cy, r, colour):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set(xx, yy, colour)

    def tri(self, cx, y_top, half, h, colour):
        for i in range(h):
            w = half * (h - i) // h
            if w < 1:
                w = 1
            self.rect(cx - w, y_top + i, 2 * w, 1, colour)

    def char(self, x, y, ch, scale, colour):
        glyph = _G.get(ch, _G[" "])
        for r, bits in enumerate(glyph):
            for c in range(5):
                if bits & (1 << (4 - c)):
                    px = x + c * scale
                    py = y + r * scale
                    self.rect(px, py, scale, scale, colour)

    def text(self, x, y, s, scale, colour):
        s = s.upper()
        cx = x
        for ch in s:
            self.char(cx, y, ch, scale, colour)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def centred(self, y, s, scale, colour):
        w = self.text_width(s, scale)
        self.text((self.width - w) // 2, y, s, scale, colour)



def wrap(text, max_chars):
    """Greedy word wrap; returns a list of lines, each <= max_chars."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        nxt = w if not cur else cur + " " + w
        if len(nxt) <= max_chars:
            cur = nxt
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines




# ---------------------------------------------------------------------------
# v3: newspaper front page, 33 stories, flat vector illustrations in code.
# No photos, no external files, no network. Deterministic.
# ---------------------------------------------------------------------------
WIDTH = 1024
HEIGHT = 1024

PAPER = (247, 242, 231)
CREAM = (247, 242, 231)
NAVY = (18, 38, 66)
NAVY_LIGHT = (32, 58, 92)
BLUE = (38, 84, 140)
RED = (178, 34, 34)
ORANGE = (214, 106, 32)
GOLD = (201, 162, 39)
GREEN = (46, 125, 72)
INK = (22, 22, 22)
GREY = (110, 110, 108)
WHITE = (255, 255, 255)
RULE = (200, 198, 190)
CARD = (255, 255, 255)
SKY = (16, 32, 58)

REGION_COL = {
    "ASIA": (38, 84, 140),
    "MIDDLE EAST": (178, 34, 34),
    "EUROPE": (46, 125, 72),
    "AFRICA": (201, 162, 39),
    "AMERICAS": (18, 38, 66),
    "OCEANIA": (120, 70, 140),
    "GLOBAL": (110, 110, 108),
}

# (number, region, headline) for cards 4-13
MID = [
    (4, "MIDDLE EAST", "TWO TANKERS HIT MINES IN HORMUZ, CATCH FIRE"),
    (5, "MIDDLE EAST", "HOUTHIS HIT RAS TANURA REFINERY; RIYADH TOWER HURT 11"),
    (6, "EUROPE", "ODESA STRIKE KILLS 2, HURTS 3; UKRAINE DRONES HIT TWO ROSNEFT PLANTS"),
    (7, "AMERICAS", "HUAWEI GUILTY IN US COURT ON TRADE SECRETS, BANK FRAUD"),
    (8, "AMERICAS", "CARTAGENA HOSTAGES FREED; ONE CAPTOR KILLED"),
    (9, "OCEANIA", "AUSTRALIA-SOLOMON PACT BARS FOREIGN BASES"),
    (10, "AFRICA", "SUDAN RSF DRONE STRIKES KILL 19, WOUND 20 IN DAMAZIN"),
    (11, "ASIA", "BANGLADESH GARMENT WAGE +36% TO TK17,500"),
    (12, "ASIA", "JAVA GOLD MINE FLOOD: 9 DEAD, 26 TRAPPED"),
    (13, "OCEANIA", "AUSTRALIA ANNUAL CPI 4.9%"),
]

# (number, text) for the bottom list 14-33
LIST = [
    (14, "COALITION STRIKES HODEIDAH PORT"),
    (15, "UKRAINE DRONE HITS SAMARA REFINERY; 5 DEAD"),
    (16, "DOW FIRST CLOSE ABOVE 50,000 AT 50,018.70"),
    (17, "ETHIOPIA: 11.3M CHILDREN GET POLIO VACCINE"),
    (18, "GAZA STRIKES CONTINUE"),
    (19, "UK MET POLICE RACE REVIEW"),
    (20, "NETANYAHU TRIAL CONTINUES"),
    (21, "LONDON TUBE STRIKE"),
    (22, "US HOUSE DEMOCRATS HOLD 259 SEATS"),
    (23, "CAIRO TANKER FIRE KILLS 30"),
    (24, "UK ENERGY PRICE CAP +26%"),
    (25, "TAIEX -4.8%"),
    (26, "112 DRONES IN OVERNIGHT UKRAINE ATTACKS"),
    (27, "ISRAEL STRIKES HAMAS TARGETS"),
    (28, "47,000 WOMEN KILLED BY PARTNER OR KIN IN 2025, UN SAYS"),
    (29, "VIETNAM TARIFF 35%"),
    (30, "JAPAN TARIFF 13%"),
    (31, "CHINA TARIFF 20%; EU TARIFF 15%"),
    (32, "PAKISTANI ASTRONAUT FIRST FOREIGN VISITOR TO TIANGONG"),
    (33, "SHENZHOU-24 LIFTS OFF 00:21 UTC; DOCKS 03:56"),
]

# Map dots for stories 1-13: (number, lon, lat)
DOTS = [
    (1, 116, 39), (2, 127, 37), (3, -88, 33), (4, 60, 30), (5, 48, 21),
    (6, 30, 46), (7, -74, 40), (8, -75, 10), (9, 160, -9), (10, 34, 11),
    (11, 90, 24), (12, 110, -7), (13, 149, -35),
]

FOOTER1 = "DATE CHECK: ALL STORIES FIRST REPORTED WEDNESDAY 25 NOVEMBER 2026"
FOOTER2 = "SOURCES: JUST SECURITY, AP, REUTERS, USTR, PRINCIPIA, CMSA - 25 NOV 2026"


def draw_icon(c, kind, x, y, w, h):
    """Small flat pictogram inside a card icon box (x,y,w,h)."""
    cx = x + w // 2
    cy = y + h // 2
    if kind == "tanker":
        c.rect(x, y + h - 12, w, 12, BLUE)
        c.rect(x + 30, y + 12, w - 70, 14, INK)
        c.rect(x + 44, y + 2, 16, 10, RED)
        c.tri(x + 60, y + 2, 7, 10, ORANGE)
        c.tri(x + 78, y + 6, 5, 8, GOLD)
    elif kind == "refinery":
        c.rect(x + 10, y + 12, 14, h - 12, GREY)
        c.rect(x + 30, y + 6, 14, h - 6, INK)
        c.rect(x + 50, y + 16, 16, h - 16, GREY)
        c.tri(x + 37, y, 6, 10, ORANGE)
        c.rect(x, y + h - 4, w, 4, RED)
    elif kind == "drone":
        c.line(x + 8, y + 8, x + w - 8, y + h - 8, INK)
        c.line(x + w - 8, y + 8, x + 8, y + h - 8, INK)
        c.disc(cx, cy, 7, RED)
        c.disc(cx, cy, 3, WHITE)
    elif kind == "court":
        c.tri(cx, y + 2, 30, 10, NAVY)
        c.rect(x + 6, y + 14, 8, h - 18, NAVY)
        c.rect(cx - 4, y + 14, 8, h - 18, NAVY)
        c.rect(x + w - 14, y + 14, 8, h - 18, NAVY)
        c.rect(x, y + h - 4, w, 4, NAVY)
    elif kind == "market":
        c.rect(x + 8, y + 12, w - 16, h - 12, BLUE)
        for i in range(5):
            col = RED if i % 2 == 0 else WHITE
            c.rect(x + 8 + i * (w - 16) // 5, y + 4, (w - 16) // 5, 8, col)
        c.rect(x + 22, y + 20, 20, 10, WHITE)
    elif kind == "treaty":
        c.rect(x + 30, y + 6, 52, 24, BLUE)
        c.rect(x + 90, y + 6, 52, 24, GREEN)
        c.rect(x + 36, y + 12, 40, 2, WHITE)
        c.rect(x + 96, y + 12, 40, 2, WHITE)
        c.rect(x + 36, y + 18, 28, 2, WHITE)
        c.rect(x + 96, y + 18, 28, 2, WHITE)
        c.disc(cx, y + h - 8, 9, RED)
        c.line(cx - 4, y + h - 8, cx - 1, y + h - 4, WHITE)
        c.line(cx - 1, y + h - 4, cx + 5, y + h - 12, WHITE)
    elif kind == "strike":
        for dx, dy in ((-14, -8), (0, -12), (14, -8), (-16, 6), (16, 6)):
            c.line(cx, cy, cx + dx, cy + dy, ORANGE)
        c.disc(cx, cy, 8, RED)
        c.disc(cx, cy, 4, GOLD)
    elif kind == "shirt":
        c.rect(cx - 22, y + 10, 44, h - 10, GREEN)
        c.rect(x + 8, y + 10, 22, 12, GREEN)
        c.rect(x + w - 30, y + 10, 22, 12, GREEN)
        c.rect(x + 28, y + 10, 4, 12, PAPER)
        c.rect(x + w - 32, y + 10, 4, 12, PAPER)
        c.tri(cx, y + 10, 7, 8, WHITE)
    elif kind == "mine":
        c.tri(cx, y + 2, 30, h - 2, (120, 90, 60))
        c.rect(cx - 8, y + h - 14, 16, 14, INK)
        c.disc(cx, y + 8, 4, GOLD)
    elif kind == "cpi":
        for i, bh in enumerate((10, 18, 14, 24)):
            c.rect(x + 10 + i * 16, y + h - 4 - bh, 10, bh, GREEN)
    else:
        c.rect(x, y, w, h, GREY)

ICON_KIND = {4: "tanker", 5: "refinery", 6: "drone", 7: "court",
             8: "market", 9: "treaty", 10: "strike", 11: "shirt",
             12: "mine", 13: "cpi"}


def draw_rocket(c, x, y, w, h):
    c.rect(x, y, w, h, SKY)
    for sx, sy in ((12, 10), (40, 26), (w - 20, 14), (w - 50, 34), (24, 48), (w - 30, 52)):
        c.rect(x + sx, y + sy, 2, 2, WHITE)
    cx = x + w // 2
    c.tri(cx, y + 12, 8, 14, RED)
    c.rect(cx - 8, y + 26, 16, 42, WHITE)
    c.rect(cx - 8, y + 40, 16, 4, BLUE)
    c.rect(cx - 16, y + 52, 8, 16, RED)
    c.rect(cx + 8, y + 52, 8, 16, RED)
    c.tri(cx, y + 68, 7, 16, ORANGE)
    c.tri(cx, y + 72, 4, 12, GOLD)
    c.disc(x + 26, y + 26, 9, (220, 220, 200))
    c.rect(x + w - 52, y + h - 16, 40, 4, GREY)


def draw_chart(c, x, y, w, h):
    c.rect(x, y, w, h, WHITE)
    for gy in range(4):
        yy = y + 12 + gy * 22
        c.rect(x + 8, yy, w - 16, 1, RULE)
    pts = [(x + 12, y + 30), (x + 60, y + 38), (x + 110, y + 36),
           (x + 160, y + 54), (x + 210, y + 66), (x + w - 14, y + 90)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.thick_line(ax, ay, bx, by, 3, RED)
    for px, py in pts:
        c.disc(px, py, 3, RED)
    c.text(x + 10, y + 4, "-6.2%", 3, RED)
    c.text(x + w - 76, y + h - 16, "4,697.51", 1, INK)


def draw_bars(c, x, y, w, h):
    c.rect(x, y, w, h, WHITE)
    data = [("CHINA", 20, NAVY), ("EU", 15, BLUE), ("INDIA", 25, RED), ("VIETNAM", 35, ORANGE)]
    bw = 52
    gap = (w - 4 * bw) // 5
    for i, (label, val, col) in enumerate(data):
        bx = x + gap + i * (bw + gap)
        bh = val * 2
        c.rect(bx, y + h - 22 - bh, bw, bh, col)
        c.text(bx + (bw - c.text_width(str(val) + "%", 1)) // 2, y + h - 18 - bh, str(val) + "%", 1, WHITE)
        c.text(bx + (bw - c.text_width(label, 1)) // 2, y + h - 16, label, 1, INK)
    c.rect(x + 8, y + h - 22, w - 16, 2, INK)


def render():
    c = Canvas(WIDTH, HEIGHT, PAPER)
    # --- Masthead ---
    c.centred(12, "WEDNESDAY 25 NOVEMBER 2026", 3, INK)
    c.centred(48, "33 STORIES - 7 REGIONS - ONE DAY", 2, RED)
    c.rect(20, 70, WIDTH - 40, 4, RED)
    # --- Region bar ---
    c.centred(82, "ASIA 8  MIDDLE EAST 6  EUROPE 6  AFRICA 3  AMERICAS 5  OCEANIA 2  GLOBAL 3", 1, INK)
    # --- KPI band ---
    c.rect(20, 100, WIDTH - 40, 30, NAVY)
    c.centred(108, "-6.2% KOSPI  -  1ST ASTRONAUT  -  14 ECONOMIES  -  26 TRAPPED  -  +36% WAGE", 2, WHITE)
    # --- UTC timeline ---
    c.centred(140, "00:21 SHENZHOU LIFTS OFF  -  03:56 CREW DOCKS  -  05:30 TAIEX -4.8%  -  06:30 KOSPI -6.2%  -  10:00 LONDON TUBE STRIKE", 1, GREY)
    # --- Headlines: 3 columns ---
    hx = [20, 352, 684]
    hw = 320
    hy = 158
    # 1 rocket
    draw_rocket(c, hx[0], hy, hw, 104)
    c.text(hx[0], hy + 112, "1. SHENZHOU-24 DOCKS", 2, INK)
    c.text(hx[0], hy + 134, "WITH TIANGONG", 2, INK)
    c.text(hx[0], hy + 156, "PAKISTAN'S FIRST ASTRONAUT, ZEESHAN ALI, ABOARD", 1, GREY)
    # 2 chart
    draw_chart(c, hx[1], hy, hw, 104)
    c.text(hx[1], hy + 112, "2. KOSPI -6.2% AS AI", 2, INK)
    c.text(hx[1], hy + 134, "DOUBTS HIT CHIP STOCKS", 2, INK)
    c.text(hx[1], hy + 156, "KOSPI 4,697.51 - NIKKEI -2.78% - NASDAQ -1.5%", 1, GREY)
    # 3 bars
    draw_bars(c, hx[2], hy, hw, 104)
    c.text(hx[2], hy + 112, "3. US PLANS TARIFFS", 2, INK)
    c.text(hx[2], hy + 134, "ON 14 ECONOMIES", 2, INK)
    c.text(hx[2], hy + 156, "CHINA 20% - EU 15% - INDIA 25% - VIETNAM 35%", 1, GREY)
    # --- Middle cards 4-13: 5 cols x 2 rows ---
    mw, mh = 188, 116
    for i, (num, region, text) in enumerate(MID):
        col, row = i % 5, i // 5
        x = 20 + col * (mw + 11)
        y = 340 + row * (mh + 10)
        c.rect(x, y, mw, mh, CARD)
        c.rect(x, y, mw, 2, REGION_COL[region])
        c.rect(x, y + 6, 24, 20, RED if num <= 3 else NAVY)
        c.text(x + (24 - c.text_width(str(num), 2)) // 2, y + 10, str(num), 2, WHITE)
        c.text(x + mw - 4 - c.text_width(region, 1), y + 10, region, 1, REGION_COL[region])
        draw_icon(c, ICON_KIND[num], x + 8, y + 32, mw - 16, 38)
        lines = wrap(text, 30)[:4]
        ly = y + 76
        for line in lines:
            c.text(x + 8, ly, line, 1, INK)
            ly += 10
    # --- Bottom: map (left) + list 14-33 (right, 2 cols) ---
    by = 596
    c.rect(20, by, 320, 340, CARD)
    c.rect(20, by, 320, 2, NAVY)
    c.text(32, by + 10, "WHERE IT HAPPENED", 2, NAVY)
    mx, my, mw2, mh2 = 32, by + 34, 296, 260
    c.rect(mx, my, mw2, mh2, (232, 238, 244))
    # rough continents
    c.rect(mx + 30, my + 40, 70, 60, (190, 200, 190))
    c.rect(mx + 110, my + 30, 60, 70, (190, 200, 190))
    c.rect(mx + 180, my + 50, 80, 60, (190, 200, 190))
    c.rect(mx + 200, my + 130, 50, 40, (190, 200, 190))
    c.rect(mx + 40, my + 130, 40, 50, (190, 200, 190))
    for num, lon, lat in DOTS:
        dx = mx + int((lon + 180) / 360.0 * mw2)
        dy = my + int((90 - lat) / 180.0 * mh2)
        c.rect(dx - 7, dy - 7, 14, 14, RED)
        c.text(dx - c.text_width(str(num), 1) // 2, dy - 4, str(num), 1, WHITE)
    c.text(32, by + 306, "DOTS 1-13 MARK THE TOP STORIES", 1, GREY)
    # list columns
    list_cols = [LIST[:10], LIST[10:]]
    list_x = [356, 688]
    for col_idx, items in enumerate(list_cols):
        x = list_x[col_idx]
        ly = by + 6
        for num, text in items:
            lines = wrap(str(num) + ". " + text, 50)
            for line in lines:
                c.text(x, ly, line, 1, INK)
                ly += 11
            ly += 6
    # --- Footer ---
    c.rect(20, 956, WIDTH - 40, 2, RULE)
    c.text(20, 970, FOOTER1, 1, RED)
    c.text(20, 988, FOOTER2, 1, GREY)
    return bytes(c.pix)


def main():
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    png = encode_png(render(), WIDTH, HEIGHT)
    out_path = out_dir / "entry.png"
    out_path.write_bytes(png)
    print(f"Wrote {len(png)} bytes to {out_path} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
