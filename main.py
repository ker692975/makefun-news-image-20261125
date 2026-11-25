#!/usr/bin/env python3
"""Generate the make.fun bounty entry: one image summing up 25 Nov 2026 world news.

Bounty: https://make.fun/bounty/news-image-20261125
Output: /output/entry.png  (or $OUTPUT_DIR/entry.png)
Size: 1024 x 1024 PNG, at most 1 MiB, deterministic.

Standard library only: zlib / struct / binascii / os / hashlib-free
rendering. No network, no randomness, no timestamps, no external files.
Text is rendered with a built-in 5x7 bitmap font (uppercase only),
so the program is fully self-contained and byte-identical on every run.
"""

import binascii
import os
import struct
import zlib
from pathlib import Path

WIDTH = 1024
HEIGHT = 1024

# ---------------------------------------------------------------------------
# 5x7 bitmap font. Each glyph is 7 rows; each row is a 5-bit integer,
# bit 4 = leftmost pixel. Only the characters used by the poster are defined.
# ---------------------------------------------------------------------------
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

# The 10 news items for 25 November 2026. Text is stored in plain ASCII
# and rendered in uppercase by the bitmap font.
ITEMS = [
    "Hormuz: two oil tankers hit mines and caught fire, Iran's guards say",
    "Houthis hit Saudi Ras Tanura refinery; Riyadh tower strike hurt 11",
    "Odesa strike killed 2 and hurt 3; Ukraine drones hit two Rosneft plants",
    "Huawei found guilty in US court on trade secrets and bank fraud",
    "US proposes tariffs on 14 economies, including China, the EU and India",
    "Markets slide: Kospi -6.16%, Nikkei -2.78%; Dow tops 50,000",
    "Colombia: Cartagena supermarket hostages freed; one captor killed",
    "Australia and Solomon Islands sign pact barring foreign bases",
    "Sudan: RSF drone strikes killed 19 and wounded 20, officials say",
    "Shenzhou-24 docks with Tiangong, carrying Pakistan's first astronaut",
]

TITLE = "WORLD NEWS"
SUBTITLE = "25 NOVEMBER 2026"
FOOTER = "SOURCES: JUST SECURITY, AP, REUTERS, USTR, PRINCIPIA, CMSA - 25 NOV 2026"

# Colours (R, G, B)
PAPER = (253, 252, 248)
NAVY = (18, 38, 66)
NAVY_LIGHT = (32, 58, 92)
RED = (178, 34, 34)
INK = (22, 22, 22)
GREY = (110, 110, 108)
CARD_A = (244, 243, 238)
CARD_B = (255, 255, 255)
WHITE = (255, 255, 255)
RULE = (200, 198, 190)


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


def render():
    c = Canvas(WIDTH, HEIGHT, PAPER)

    # Header band
    c.rect(0, 0, WIDTH, 168, NAVY)
    c.rect(0, 168, WIDTH, 6, RED)
    c.centred(34, TITLE, 8, WHITE)
    c.centred(118, SUBTITLE, 3, (200, 210, 225))
    c.text(48, 118, "10 STORIES", 2, (200, 210, 225))

    # Items: single-column list, alternating cards
    x0, x1 = 32, WIDTH - 32
    y = 196
    item_h = 74
    gap = 6
    for idx, item in enumerate(ITEMS, start=1):
        bg = CARD_A if idx % 2 == 1 else CARD_B
        c.rect(x0, y, x1 - x0, item_h, bg)
        # Number badge
        c.rect(x0 + 12, y + 13, 48, 48, RED if idx <= 3 else NAVY_LIGHT)
        num = str(idx)
        nw = c.text_width(num, 4 if len(num) == 1 else 3)
        c.text(x0 + 12 + (48 - nw) // 2, y + 13 + (48 - 7 * (4 if len(num) == 1 else 3)) // 2,
               num, 4 if len(num) == 1 else 3, WHITE)
        # Headline, wrapped to at most 2 lines
        lines = wrap(item, 62)[:2]
        ty = y + 16
        for line in lines:
            c.text(x0 + 76, ty, line, 2, INK)
            ty += 22
        y += item_h + gap

    # Footer
    fy = HEIGHT - 44
    c.rect(32, fy - 10, WIDTH - 64, 2, RULE)
    c.text(32, fy + 6, FOOTER, 1, GREY)
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
