#!/usr/bin/env python3
"""Render entry.png for news-image-20261124 V1 (ATM).

Written from scratch in this session (2026-11-25), same proven layout
family as our 23 Nov entry, all content new for Tuesday 24 Nov 2026:
  - DATE CHECK FIRST: a red proof strip directly under the masthead,
    before any story, naming 18 items left out because they happened
    or were first reported before Tuesday 24 Nov 2026.
  - THE DAY DECIDED: five verdict boxes (Huawei guilty 10/12, CAS
    restores Senegal, ECHR allows pushbacks, Denmark upholds the
    ghetto law, Zambia charges treason).
  - THE DAY IN EIGHT SCENES: eight illustrated top cards led by the
    courtroom verdict (Huawei) and the leaked 700,000 dead -- not the
    Hormuz/markets lead all five R1 leaders share. Each scene carries
    one big baked number.
  - TUESDAY'S MARKETS: a strip with Tuesday numbers only (Nvidia -7%,
    Anthropic under $83 IPO, TAIEX +9%, KOSPI +7.5%, Nikkei +3.9%).
  - THE REST OF THE DAY: 34 more stories in three region columns,
    12 px headlines + 11 px summaries, no tiny numbered list anywhere,
    no footer mini-map.
All drawings are procedural vector work in this file; no external assets.
Deterministic: no randomness, no clock, no network. Rendered at 2x then
downscaled with LANCZOS to 1024x1024.
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024 * S, 1024 * S
MX = 24                    # side margin
CW = 1024 - 2 * MX         # content width = 976

# ---------- palette ----------
PAPER    = (247, 242, 231)  # cream paper
INK      = (20, 20, 20)     # near-black
GREY     = (110, 108, 100)
FAINT    = (150, 148, 138)
RED      = (178, 34, 34)    # kept for the most urgent (W4)
DARKRED  = (140, 20, 20)
NAVY     = (16, 24, 48)     # night sky
DUSK     = (46, 52, 84)
SEA      = (28, 52, 76)
SEA2     = (18, 38, 60)
LAND     = (223, 217, 196)
WHITE    = (255, 255, 255)
CREAMBOX = (255, 246, 240)  # date-check fill
DARKBOX  = (24, 42, 60)
BAND     = (20, 20, 20)
GREEN    = (46, 125, 50)    # CONFIRMED
AMBER    = (176, 124, 0)    # REPORTED
ORANGE   = (230, 126, 34)
YELLOW   = (240, 196, 60)

# region colours (W1: same colour on verdict strip, panel chip, column disc)
REGION = {
    "EUROPE":   (31, 78, 121),
    "MIDEAST":  (179, 84, 30),
    "AMERICAS": (46, 125, 50),
    "ASIA-PAC": (106, 27, 154),
    "OCEANIA":  (0, 131, 143),
    "AFRICA":   (141, 110, 0),
    "WORLD":    (55, 71, 79),
}

# ---------- fonts ----------
FD = "/usr/share/fonts/truetype/noto/"


def F(name, size):
    return ImageFont.truetype(FD + name, size * S)


SERIF_B = lambda s: F("NotoSerif-Bold.ttf", s)
SERIF   = lambda s: F("NotoSerif-Regular.ttf", s)
SERIF_I = lambda s: F("NotoSerif-Italic.ttf", s)
SANS    = lambda s: F("NotoSans-Regular.ttf", s)
SANS_B  = lambda s: F("NotoSans-Bold.ttf", s)
SANS_I  = lambda s: F("NotoSans-Italic.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def X(v):
    return v * S


def Y(v):
    return v * S


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((X(x), Y(y)), s, font=font, fill=fill, anchor=anchor)


def text_w(s, font):
    return d.textlength(s, font=font) / S


def fit(s, font, maxw, label):
    """Assert a line fits; fail loudly instead of overflowing silently."""
    w = text_w(s, font)
    assert w <= maxw, f"OVERFLOW {label}: {w:.1f} > {maxw} :: {s!r}"
    return w


def wrap(s, font, maxw, max_lines, label):
    """Greedy word wrap; asserts the text fits in max_lines."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    assert len(lines) <= max_lines, \
        f"WRAP {label}: {len(lines)} lines > {max_lines} :: {s!r}"
    assert all(text_w(ln, font) <= maxw for ln in lines), \
        f"WRAP-WIDTH {label} :: {s!r}"
    return lines


def rrect(x0, y0, x1, y1, fill=None, outline=None, width=1, radius=0):
    d.rounded_rectangle([X(x0), Y(y0), X(x1), Y(y1)], radius=radius * S,
                        fill=fill, outline=outline, width=width * S)


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([X(x0), Y(y0), X(x1), Y(y1)], fill=fill,
                outline=outline, width=width * S)


def line(x0, y0, x1, y1, fill=INK, width=1):
    d.line([X(x0), Y(y0), X(x1), Y(y1)], fill=fill, width=width * S)


def section_header(y, label, right=""):
    text(MX, y, label, SANS_B(13), fill=INK)
    if right:
        text(1024 - MX, y, right, SANS(11), fill=GREY, anchor="ra")
    line(MX, y + 17, 1024 - MX, y + 17, fill=INK, width=1)


# =========================================================
# 0. TOP BAND  (y 0..24)
# =========================================================
rect(0, 0, 1024, 24, fill=BAND)
text(MX, 6, "THE WORLD IN ONE DAY", SANS_B(11), fill=WHITE)
text(1024 - MX, 6, "42 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED TUESDAY 24 NOVEMBER 2026",
     SANS_B(11), fill=WHITE, anchor="ra")

# =========================================================
# 1. MASTHEAD  (y 24..112)
# =========================================================
text(512, 24, "Tuesday 24 November 2026", SERIF_B(54), fill=INK, anchor="ma")
text(512, 90, "Huawei guilty on 10 of 12 counts  \u00b7  700,000 Russian dead, leaked  \u00b7  Three tankers ablaze in Hormuz",
     SERIF_I(16), fill=RED, anchor="ma")

# =========================================================
# 2. DATE CHECK FIRST  (y 114..206)
# =========================================================
rrect(MX, 114, 1024 - MX, 206, fill=CREAMBOX, outline=RED, width=2)
rect(MX, 114, 158, 206, fill=RED)
text(MX + 12, 122, "DATE CHECK", SANS_B(15), fill=WHITE)
text(MX + 12, 140, "READ THIS", SANS_B(11), fill=WHITE)
text(MX + 12, 156, "FIRST", SANS_B(11), fill=WHITE)
text(170, 118, "Every story below happened or was first reported Tuesday 24 Nov 2026 (UTC).",
     SANS_B(13), fill=INK)
DC_LINES = [
    "Left out \u2014 they happened earlier: COP31 no-deal itself (Sun/Mon) \u00b7 BepiColombo (Sat) \u00b7 Mariana volcanoes (Mon)",
    "Democrats win House (Sun) \u00b7 Nepal PM in India (Mon) \u00b7 Tajikistan leaves ICC (Mon) \u00b7 Walrus refuge (Mon)",
    "EU sanctions-22 proposed (Mon) \u00b7 Chapo Isidro caught (Sat) \u00b7 Cikande fire itself (Sat) \u00b7 ICE Seattle (Sun)",
    "Belgium march (Mon) \u00b7 Zanzibar hotel fire (Sat) \u00b7 Women\u2019s World Cup hosts (Mon) \u00b7 NATO space vow (Mon)",
    "UK heat deaths record (Mon) \u00b7 Puigdemont amnesty (Mon) \u00b7 School bomb threats (Mon)",
]
for j, ln in enumerate(DC_LINES):
    fit(ln, SANS(12), 1024 - MX - 170, f"datecheck-{j}")
    text(170, 135 + j * 14, ln, SANS(12), fill=INK)

# =========================================================
# 3. THE DAY DECIDED — five verdict boxes  (y 212..312)
# =========================================================
section_header(212, "THE DAY DECIDED \u2014 FIVE VERDICTS")
# (place, region, verdict, number, fact)
VERDICTS = [
    ("BROOKLYN \u00b7 JUSTICE", "AMERICAS", "HUAWEI GUILTY", "10/12", "Jury: 10 of 12 counts"),
    ("LAUSANNE \u00b7 SPORT",   "AFRICA",   "SENEGAL CHAMPIONS", "1\u20130", "CAS restores the title"),
    ("STRASBOURG \u00b7 RIGHTS", "EUROPE",  "PUSHBACKS OK", "3",    "Poland, Latvia, Lithuania faulted"),
    ("COPENHAGEN \u00b7 HOUSING", "EUROPE", "GHETTO LAW UPHELD", "1", "Mjolnerparken evictions stand"),
    ("LUSAKA \u00b7 POLITICS",  "AFRICA",   "TREASON CHARGE", "13", "Opposition leader + 12 others"),
]
VW, VGAP = 188, 8
VY0, VY1 = 230, 312
for i, (place, region, verdict, number, fact) in enumerate(VERDICTS):
    x0 = MX + i * (VW + VGAP)
    x1 = x0 + VW
    rrect(x0, VY0, x1, VY1, fill=WHITE, outline=GREY, width=1)
    rect(x0 + 1, VY0 + 1, x1 - 1, VY0 + 7, fill=REGION[region])
    text(x0 + 10, VY0 + 10, place, SANS_B(10), fill=GREY)
    fit(verdict, SANS_B(15), VW - 20, f"verdict-{i}")
    text(x0 + 10, VY0 + 24, verdict, SANS_B(15), fill=INK)
    fit(number, SANS_B(24), VW - 20, f"verdict-num-{i}")
    text(x0 + 10, VY0 + 42, number, SANS_B(24), fill=RED)
    fit(fact, SANS(11), VW - 20, f"verdict-fact-{i}")
    text(x0 + 10, VY0 + 66, fact, SANS(11), fill=INK)

# =========================================================
# 4. THE DAY IN EIGHT SCENES — two rows of four  (y 318..606)
# =========================================================
section_header(318, "THE DAY IN EIGHT SCENES \u2014 LED BY THE VERDICT")
PW, PGAP = 236, 10
PH = 132
SCENE_H = 56


def badge2(x0, y0, s, size=22):
    """Big baked number, cream disc with red ring, top-right of a scene."""
    bw = text_w(s, SANS_B(size)) + 16
    bx1 = x0 + PW - 6
    bx0 = bx1 - bw
    by0, by1 = y0 + 6, y0 + 6 + 30
    d.ellipse([X(bx0), Y(by0), X(bx1), Y(by1)], fill=PAPER,
              outline=RED, width=2 * S)
    text((bx0 + bx1) / 2, by0 + 4, s, SANS_B(size), fill=RED, anchor="ma")


def panel2(row, col, story_no, place, region, status, headline, fact, num,
           draw_scene):
    x0 = MX + col * (PW + PGAP)
    y0 = 336 + row * (PH + 6)
    x1 = x0 + PW
    y1 = y0 + PH
    rrect(x0, y0, x1, y1, fill=WHITE, outline=GREY, width=1)
    draw_scene(x0, y0, x1, y0 + SCENE_H)
    badge2(x0, y0, num)
    # story number disc on the scene, top-left
    d.ellipse([X(x0 + 6), Y(y0 + 6), X(x0 + 26), Y(y0 + 26)],
              fill=REGION[region])
    text(x0 + 16, y0 + 9, str(story_no), SANS_B(11), fill=WHITE, anchor="ma")
    hy = y0 + SCENE_H + 6
    lines = wrap(headline, SANS_B(14), PW - 16, 2, f"scene-head-{story_no}")
    for j, ln in enumerate(lines):
        text(x0 + 8, hy + j * 14, ln, SANS_B(14), fill=INK)
    fy = hy + len(lines) * 14 + 2
    flines = wrap(fact, SANS(12), PW - 16, 2, f"scene-fact-{story_no}")
    for j, ln in enumerate(flines):
        text(x0 + 8, fy + j * 12, ln, SANS(12), fill=INK)
    # chips row at the bottom
    cy = y1 - 16
    text(x0 + 8, cy, place, SANS_B(10), fill=REGION[region])
    scol = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED}[status]
    sw = text_w(status, SANS_B(10)) + 12
    rrect(x1 - 8 - sw, cy - 2, x1 - 8, cy + 12, fill=scol, radius=2)
    text(x1 - 8 - sw / 2, cy, status, SANS_B(10), fill=WHITE, anchor="ma")


def scene_courtroom(x0, y0, x1, y1):
    # wood-panelled courtroom: bench, columns, gavel
    rect(x0, y0, x1, y1, fill=(94, 64, 40))
    rect(x0, y0, x1, y0 + 10, fill=(70, 46, 28))
    for cx in (18, 196):
        rect(x0 + cx, y0 + 10, x0 + cx + 14, y1, fill=(120, 88, 56))
        rect(x0 + cx - 3, y0 + 10, x0 + cx + 17, y0 + 16, fill=(140, 104, 66))
    # judge bench + gavel
    rect(x0 + 58, y0 + 30, x0 + 178, y1, fill=(52, 34, 20))
    rect(x0 + 58, y0 + 30, x0 + 178, y0 + 36, fill=(30, 20, 12))
    # gavel head + handle, angled
    d.polygon([(X(x0 + 96), Y(y0 + 20)), (X(x0 + 118), Y(y0 + 14)),
               (X(x0 + 122), Y(y0 + 22)), (X(x0 + 100), Y(y0 + 28))],
              fill=(210, 170, 110))
    line(x0 + 118, y0 + 22, x0 + 132, y0 + 30, fill=(210, 170, 110), width=3)
    d.ellipse([X(x0 + 132), Y(y0 + 26), X(x0 + 146), Y(y0 + 34)],
              fill=(180, 140, 90))
    # scales of justice, small, on the bench
    line(x0 + 160, y0 + 36, x0 + 160, y0 + 50, fill=YELLOW, width=2)
    line(x0 + 150, y0 + 38, x0 + 170, y0 + 38, fill=YELLOW, width=2)
    d.ellipse([X(x0 + 146), Y(y0 + 42), X(x0 + 154), Y(y0 + 48)], fill=YELLOW)
    d.ellipse([X(x0 + 166), Y(y0 + 42), X(x0 + 174), Y(y0 + 48)], fill=YELLOW)


def scene_leak(x0, y0, x1, y1):
    # leaked pages + rising bar chart of the dead
    rect(x0, y0, x1, y1, fill=(226, 222, 210))
    rect(x0 + 14, y0 + 8, x0 + 92, y1 - 6, fill=WHITE)
    for ly in (16, 24, 32, 40):
        line(x0 + 20, y0 + ly, x0 + 86, y0 + ly, fill=(150, 148, 138), width=1)
    # red LEAKED stamp, tilted
    d.ellipse([X(x0 + 26), Y(y0 + 30), X(x0 + 80), Y(y0 + 50)],
              outline=RED, width=2 * S)
    text(x0 + 53, y0 + 35, "LEAK", SANS_B(11), fill=RED, anchor="ma")
    # bars climbing to the right
    for bi, bh in enumerate((10, 18, 26, 38)):
        bx = x0 + 108 + bi * 30
        rect(bx, y1 - 8 - bh, bx + 20, y1 - 8, fill=RED if bi == 3 else NAVY)


def scene_hormuz(x0, y0, x1, y1):
    # night strait: dark sky, darker sea, tanker under a missile arc
    rect(x0, y0, x1, y0 + 24, fill=NAVY)
    rect(x0, y0 + 24, x1, y1, fill=SEA2)
    for sx, sy in [(22, 8), (96, 12), (170, 6), (208, 14), (60, 18)]:
        d.ellipse([X(x0 + sx), Y(y0 + sy), X(x0 + sx + 3), Y(y0 + sy + 3)], fill=WHITE)
    # dotted missile arc diving onto the tanker
    for t in range(0, 9):
        px = x0 + 30 + t * 16
        py = y0 + 40 - int(26 * (1 - ((t - 4) / 4.0) ** 2))
        d.ellipse([X(px), Y(py), X(px + 4), Y(py + 4)], fill=WHITE)
    # tanker hull + bridge, low in the water
    rect(x0 + 52, y0 + 40, x0 + 188, y0 + 50, fill=(24, 30, 38))
    rect(x0 + 150, y0 + 32, x0 + 176, y0 + 40, fill=(40, 46, 56))
    # flame licking the deck + smoke
    d.polygon([(X(x0 + 84), Y(y0 + 40)), (X(x0 + 100), Y(y0 + 28)),
               (X(x0 + 116), Y(y0 + 40))], fill=ORANGE)
    d.polygon([(X(x0 + 90), Y(y0 + 40)), (X(x0 + 100), Y(y0 + 32)),
               (X(x0 + 110), Y(y0 + 40))], fill=YELLOW)
    d.ellipse([X(x0 + 88), Y(y0 + 16), X(x0 + 112), Y(y0 + 32)], fill=(90, 90, 96))
    # water lines
    for wy in (y0 + 52,):
        line(x0 + 8, wy, x1 - 8, wy, fill=(90, 120, 150), width=1)


def scene_tower(x0, y0, x1, y1):
    # dusk skyline, one very tall tower, blast near its crown
    rect(x0, y0, x1, y0 + 34, fill=(214, 132, 74))
    d.ellipse([X(x0 + 170), Y(y0 + 4), X(x0 + 196), Y(y0 + 30)], fill=(240, 196, 110))
    rect(x0, y0 + 34, x1, y1, fill=(40, 44, 60))
    # low blocks
    for bx, bw, bh in [(8, 34, 12), (48, 26, 18), (180, 30, 14), (214, 16, 10)]:
        rect(x0 + bx, y1 - bh, x0 + bx + bw, y1, fill=(24, 28, 40))
    # the tower: tapering shaft + crown
    d.polygon([(X(x0 + 104), Y(y1)), (X(x0 + 112), Y(y0 + 6)),
               (X(x0 + 124), Y(y0 + 6)), (X(x0 + 132), Y(y1))], fill=(16, 24, 48))
    for wy in range(y0 + 14, y1 - 4, 8):
        line(x0 + 110, wy, x0 + 126, wy, fill=(240, 196, 110), width=1)
    # blast starburst at the crown
    ex, ey = x0 + 118, y0 + 10
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        r = 14 if (ang // 30) % 2 == 0 else 8
        line(ex, ey, ex + r * math.cos(a), ey + r * math.sin(a),
             fill=ORANGE, width=2)
    d.ellipse([X(ex - 6), Y(ey - 6), X(ex + 6), Y(ey + 6)], fill=YELLOW)


def scene_chart(x0, y0, x1, y1):
    # falling market chart: red line down, bars shrinking
    rect(x0, y0, x1, y1, fill=WHITE)
    line(x0 + 10, y0 + 8, x0 + 10, y1 - 8, fill=GREY, width=1)
    line(x0 + 10, y1 - 8, x1 - 8, y1 - 8, fill=GREY, width=1)
    # bars, tall to short
    for bi, bh in enumerate((34, 30, 24, 16, 10)):
        bx = x0 + 20 + bi * 36
        rect(bx, y1 - 8 - bh, bx + 22, y1 - 8, fill=(176, 34, 34) if bi >= 3 else NAVY)
    # falling red line across the bars
    pts = [(x0 + 20, y0 + 12), (x0 + 70, y0 + 20), (x0 + 120, y0 + 30),
           (x0 + 170, y0 + 42), (x0 + 214, y0 + 50)]
    for a, b in zip(pts, pts[1:]):
        line(a[0], a[1], b[0], b[1], fill=RED, width=3)
    # arrowhead at the end
    d.polygon([(X(x0 + 214), Y(y0 + 50)), (X(x0 + 204), Y(y0 + 44)),
               (X(x0 + 206), Y(y0 + 52))], fill=RED)


def scene_drones(x0, y0, x1, y1):
    # night sky, drone swarm dots, two impact flashes over a city
    rect(x0, y0, x1, y0 + 38, fill=NAVY)
    rect(x0, y0 + 38, x1, y1, fill=(30, 30, 40))
    for sx, sy in [(20, 8), (70, 14), (130, 6), (180, 12), (210, 20), (100, 22)]:
        d.ellipse([X(x0 + sx), Y(y0 + sy), X(x0 + sx + 3), Y(y0 + sy + 3)], fill=WHITE)
    # drone crosses
    for dx, dy in [(44, 12), (96, 20), (150, 10), (196, 24)]:
        line(x0 + dx - 4, y0 + dy, x0 + dx + 4, y0 + dy, fill=(205, 205, 215), width=2)
        line(x0 + dx, y0 + dy - 4, x0 + dx, y0 + dy + 4, fill=(205, 205, 215), width=2)
    # dotted trails
    for tx in range(0, 5):
        d.ellipse([X(x0 + 30 + tx * 8), Y(y0 + 30), X(x0 + 34 + tx * 8), Y(y0 + 34)],
                  fill=(150, 150, 160))
    # city blocks + two impact flashes
    for bx, bw, bh in [(10, 40, 10), (60, 30, 14), (150, 36, 12), (196, 30, 9)]:
        rect(x0 + bx, y1 - bh, x0 + bx + bw, y1, fill=(16, 18, 26))
    for ix in (75, 168):
        d.polygon([(X(x0 + ix), Y(y1 - 14)), (X(x0 + ix + 5), Y(y1 - 26)),
                   (X(x0 + ix + 10), Y(y1 - 14))], fill=ORANGE)


def scene_poland(x0, y0, x1, y1):
    # night border: radar sweep, one drone crossing, jet overhead
    rect(x0, y0, x1, y0 + 36, fill=NAVY)
    rect(x0, y0 + 36, x1, y1, fill=(34, 44, 34))
    for sx, sy in [(20, 8), (80, 14), (150, 6), (200, 16), (120, 22)]:
        d.ellipse([X(x0 + sx), Y(y0 + sy), X(x0 + sx + 3), Y(y0 + sy + 3)], fill=WHITE)
    # radar dish + sweep
    line(x0 + 30, y1 - 8, x0 + 30, y0 + 26, fill=(90, 120, 150), width=3)
    d.ellipse([X(x0 + 18), Y(y0 + 20), X(x0 + 42), Y(y0 + 32)], fill=(90, 120, 150))
    line(x0 + 30, y0 + 26, x0 + 90, y0 + 12, fill=GREEN, width=2)
    # the intruding drone, dotted trail behind it
    for t in range(0, 6):
        d.ellipse([X(x0 + 96 + t * 8), Y(y0 + 14), X(x0 + 100 + t * 8), Y(y0 + 18)],
                  fill=(205, 205, 215))
    d.polygon([(X(x0 + 150), Y(y0 + 16)), (X(x0 + 166), Y(y0 + 12)),
               (X(x0 + 166), Y(y0 + 20))], fill=(150, 154, 160))
    # treeline + NATO jet silhouette
    for tx in range(0, PW, 26):
        d.polygon([(X(x0 + tx), Y(y0 + 36)), (X(x0 + tx + 9), Y(y0 + 26)),
                   (X(x0 + tx + 18), Y(y0 + 36))], fill=(20, 28, 20))
    d.polygon([(X(x0 + 176), Y(y0 + 30)), (X(x0 + 196), Y(y0 + 34)),
               (X(x0 + 176), Y(y0 + 38)), (X(x0 + 184), Y(y0 + 34))],
              fill=(150, 154, 160))


def scene_trophy(x0, y0, x1, y1):
    # green pitch, gold cup, ball, confetti
    rect(x0, y0, x1, y0 + 14, fill=(247, 242, 231))
    rect(x0, y0 + 14, x1, y1, fill=(46, 125, 50))
    line(x0, y0 + 34, x1, y0 + 34, fill=WHITE, width=2)
    d.ellipse([X(x0 + 100), Y(y0 + 36), X(x0 + 136), Y(y0 + 54)],
              outline=WHITE, width=2 * S)
    # the cup: bowl, stem, base
    d.polygon([(X(x0 + 96), Y(y0 + 10)), (X(x0 + 140), Y(y0 + 10)),
               (X(x0 + 132), Y(y0 + 34)), (X(x0 + 104), Y(y0 + 34))],
              fill=(240, 196, 60))
    line(x0 + 118, y0 + 34, x0 + 118, y0 + 44, fill=(240, 196, 60), width=4)
    rect(x0 + 104, y0 + 44, x0 + 132, y0 + 50, fill=(240, 196, 60))
    # handles
    d.arc([X(x0 + 82), Y(y0 + 8), X(x0 + 100), Y(y0 + 28)], 90, 270,
          fill=(240, 196, 60), width=3 * S)
    d.arc([X(x0 + 136), Y(y0 + 8), X(x0 + 154), Y(y0 + 28)], -90, 90,
          fill=(240, 196, 60), width=3 * S)
    # ball + confetti
    d.ellipse([X(x0 + 170), Y(y0 + 40), X(x0 + 184), Y(y0 + 52)], fill=WHITE)
    for cx, cy, cc in [(30, 20, RED), (60, 44, YELLOW), (200, 18, WHITE),
                       (160, 46, YELLOW), (40, 48, WHITE)]:
        d.ellipse([X(x0 + cx), Y(y0 + cy), X(x0 + cx + 4), Y(y0 + cy + 4)], fill=cc)


panel2(0, 0, 1, "BROOKLYN, US", "AMERICAS", "CONFIRMED",
       "Huawei guilty on 10 of 12 counts",
       "Trade-secret conspiracy + bank fraud; 7-year case ends. (BBC)",
       "10/12", scene_courtroom)
panel2(0, 1, 2, "LEAKED DATA", "WORLD", "REPORTED",
       "Leaked data: 700,000 Russian dead",
       "At least 490,000 dead; Meduza counts the missing. (France 24)",
       "700K", scene_leak)
panel2(0, 2, 3, "HORMUZ, IRAN", "MIDEAST", "CLAIM",
       "Iran: mines set 3 tankers ablaze",
       "Ships burn in the strait; talks stalled on 7 terms. (Euronews)",
       "3", scene_hormuz)
panel2(0, 3, 4, "RIYADH, SAUDI", "MIDEAST", "REPORTED",
       "Houthis hit Riyadh\u2019s tallest tower",
       "Second strike in five days; 11 injured. (MEE)",
       "11", scene_tower)
panel2(1, 0, 5, "SANTA CLARA, US", "AMERICAS", "CONFIRMED",
       "Nvidia slides 7% as rally fades",
       "AI stocks fall; Anthropic below its $83 IPO. (CNBC)",
       "\u22127%", scene_chart)
panel2(1, 1, 6, "ZAPORIZHZHIA, UKRAINE", "EUROPE", "REPORTED",
       "96 drones in a night over Ukraine",
       "73 downed; 2 killed in Zaporizhzhia. (Al Jazeera)",
       "96", scene_drones)
panel2(1, 2, 7, "WARSAW, POLAND", "EUROPE", "CONFIRMED",
       "Poland: drone incursion deliberate",
       "NATO jet cleared to shoot a missile down. (NPR)",
       "1", scene_poland)
panel2(1, 3, 8, "LAUSANNE, SWITZERLAND", "AFRICA", "CONFIRMED",
       "Senegal champions again",
       "CAS restores the AFCON title; Morocco stunned. (France 24)",
       "1\u20130", scene_trophy)

# =========================================================
# 5. TUESDAY'S MARKETS — Tuesday numbers only  (y 612..638)
# =========================================================
rect(MX, 612, 1024 - MX, 638, fill=BAND)
MARKETS = [
    ("NVIDIA", "\u22127%", RED),
    ("ANTHROPIC", "< $83", WHITE),
    ("TAIEX", "+9%", GREEN),
    ("KOSPI", "+7.5%", GREEN),
    ("NIKKEI", "+3.9%", GREEN),
    ("SANOFI", "$41BN", WHITE),
]
MW = CW // 6
for i, (label, value, col) in enumerate(MARKETS):
    cx0 = MX + i * MW
    fit(label, SANS_B(10), MW - 12, f"mkt-label-{i}")
    text(cx0 + 6, 613, label, SANS_B(10), fill=GREY)
    fit(value, SANS_B(16), MW - 12, f"mkt-value-{i}")
    text(cx0 + 6, 622, value, SANS_B(16), fill=col)

# =========================================================
# 6. THE REST OF THE DAY — three region columns  (y 644..974)
# =========================================================
section_header(644, "THE REST OF THE DAY \u2014 34 MORE STORIES, BY REGION")

# (story_no, region, headline, summary) -- headlines 1 line, summaries 1 line
COLUMNS = [
    ("EUROPE \u00b7 MIDEAST \u2014 12", [
        (9,  "EUROPE",  "Russia warns Estonia of war",
         "Tallinn to shut crossings Dec 1 (CNBC)"),
        (10, "EUROPE",  "COP31 ends; EU seeks rule change",
         "Longest talks fail on fossil fuels (BBC)"),
        (11, "EUROPE",  "EU to cap Chinese hybrid imports",
         "Temporary quotas from next month (Guardian)"),
        (12, "EUROPE",  "Rights court allows pushbacks",
         "When migration is used as pressure (Le Monde)"),
        (13, "EUROPE",  "Sarkozy, Bruni to stand trial",
         "2027 trial over witness tampering (BBC)"),
        (14, "EUROPE",  "Sanofi to buy Insmed",
         "Biggest pharma deal since 2023 (CNBC)"),
        (15, "EUROPE",  "Denmark backs ghetto-law evictions",
         "Top court rules for removal (Al Jazeera)"),
        (16, "MIDEAST", "Houthis close in on Aden",
         "Fighters 60 km from the capital (France 24)"),
        (17, "MIDEAST", "Yemen bus strikes kill about 25",
         "Buses, trucks hit; most active front (Hindu)"),
        (18, "MIDEAST", "Katz: Iran builds chemical arms",
         "Pre-emptive strike left open (CBS)"),
        (19, "MIDEAST", "Eisenkot signs first coalition deal",
         "Lieberman party in; left pauses (Aawsat)"),
        (20, "MIDEAST", "Israel kills Hamas security chief",
         "Naeem Abu Nahel dead; 7 killed (BBC)"),
    ]),
    ("MIDEAST \u00b7 AMERICAS \u00b7 ASIA \u2014 11", [
        (21, "MIDEAST", "Gaza meningitis epidemic alert",
         "272 cases in Oct, 8x normal (Guardian)"),
        (22, "MIDEAST", "Kyiv: two Russian ships hit off Libya",
         "Italy protests; Haftar visits Turkey (Guardian)"),
        (23, "AMERICAS", "Trump to announce new tariffs",
         "China, EU and dozens more targeted (Folha)"),
        (24, "AMERICAS", "Fed's Williams: rates higher",
         "Inflation near 2% in 2027 (CNBC)"),
        (25, "AMERICAS", "Car bomb wounds 25 in Colombia",
         "100 kg blast wrecks state HQ (Al Jazeera)"),
        (26, "AMERICAS", "El Salvador troops push in Haiti",
         "Gangs fight back; locals welcome (France 24)"),
        (27, "AMERICAS", "Cuba life expectancy falls",
         "78.8 to 74.4, first fall since 1950 (Guardian)"),
        (28, "AMERICAS", "California braces for floods",
         "High tides, El Ni\u00f1o hit travel week (BBC)"),
        (29, "ASIA-PAC", "China probes Politburo member",
         "Chen Jining, 4th of 24 probed (El Pa\u00eds)"),
        (30, "ASIA-PAC", "US blacklists Megaspeed",
         "Chip diversion; Nvidia scandal link (CNBC)"),
        (31, "ASIA-PAC", "China extends mineral pause",
         "Gallium, germanium curbs eased 2 months (SCMP)"),
    ]),
    ("ASIA \u00b7 AFRICA \u00b7 OCEANIA \u00b7 WORLD \u2014 11", [
        (32, "ASIA-PAC", "Hasina to return Dec 16",
         "Faces death sentence back home (BBC)"),
        (33, "ASIA-PAC", "Pakistan's first astronaut named",
         "Zeeshan Ali to fly Shenzhou-24 (BBC)"),
        (34, "ASIA-PAC", "Sooryavanshi, 15, hits 204",
         "53 balls, List A record (ABC)"),
        (35, "ASIA-PAC", "S. Korea shelter alert",
         "Russian jets near Ulleungdo (Al Jazeera)"),
        (36, "AFRICA",  "DR Congo plane missing",
         "Rebels claim shootdown; pilot aboard (BBC)"),
        (37, "AFRICA",  "Ebola responders trapped",
         "Fighting pins WHO staff in Ituri (UN News)"),
        (38, "AFRICA",  "Zambia charges opposition leader",
         "Treason indictment, 12 others (RFI)"),
        (39, "OCEANIA", "Australia: sue the tech giants",
         "Online safety fines up to 5% (Guardian)"),
        (40, "WORLD",   "UK sanctions Myanmar generals",
         "Malaysia to return 6,803 nationals (BBC)"),
        (41, "WORLD",   "UN chief: AI safety rules in a year",
         "Guterres warns of power shift (UN News)"),
        (42, "WORLD",   "Armenia proposes new constitution",
         "Drops Karabakh claim for peace (El Pa\u00eds)"),
    ]),
]
COLW, CGAP = 317, 12
CY0, CY1 = 666, 974
for ci, (chead, stories) in enumerate(COLUMNS):
    cx0 = MX + ci * (COLW + CGAP)
    cx1 = cx0 + COLW
    # column header: colour bar + title
    rect(cx0, CY0, cx1, CY0 + 4, fill=INK)
    fit(chead, SANS_B(13), COLW, f"colhead-{ci}")
    text(cx0, CY0 + 8, chead, SANS_B(13), fill=INK)
    line(cx0, CY0 + 24, cx1, CY0 + 24, fill=GREY, width=1)
    n = len(stories)
    row_h = (CY1 - (CY0 + 30)) / n
    for ri, (no, region, head, summ) in enumerate(stories):
        ry = CY0 + 30 + ri * row_h
        # number disc
        d.ellipse([X(cx0), Y(ry + 1), X(cx0 + 15), Y(ry + 16)],
                  fill=REGION[region])
        text(cx0 + 7, ry + 3, str(no), SANS_B(10), fill=WHITE, anchor="ma")
        tx = cx0 + 21
        tw = COLW - 21
        fit(head, SANS_B(12), tw, f"col-head-{no}")
        text(tx, ry, head, SANS_B(12), fill=INK)
        sy = ry + 13
        fit(summ, SANS(11), tw, f"col-sum-{no}")
        text(tx, sy, summ, SANS(11), fill=(60, 60, 58))
        assert sy + 11 <= ry + row_h + 1, \
            f"ROW OVERFLOW story {no}: sy {sy:.1f} row ends {ry + row_h:.1f}"
        if ri < n - 1:
            line(cx0, ry + row_h - 4, cx1, ry + row_h - 4,
                 fill=(214, 210, 198), width=1)

# =========================================================
# 7. FOOTER  (y 978..1024)
# =========================================================
foot = ("Sources: Reuters, BBC, AFP, AP, Al Jazeera, The Guardian, SCMP, CNBC, France 24 \u2014 "
        "wires read to 00:15 UTC Wed 25 Nov 2026. Scenes are drawn illustrations of reported events, not photographs.")
flines = wrap(foot, SANS(11), 1024 - 2 * MX, 2, "footer")
for j, ln in enumerate(flines):
    text(MX, 978 + j * 13, ln, SANS(11), fill=GREY)
rect(0, 1000, 1024, 1024, fill=BAND)
text(MX, 1007, "THE WORLD IN ONE DAY", SANS_B(11), fill=WHITE)
text(1024 - MX, 1007, "TUESDAY 24 NOVEMBER 2026 \u00b7 ONE PAGE",
     SANS_B(11), fill=WHITE, anchor="ra")

# =========================================================
# SAVE — deterministic downscale
# =========================================================
out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
small = img.resize((1024, 1024), Image.LANCZOS)
small.save(out_path, "PNG", optimize=True)
print("wrote", out_path, small.size)
