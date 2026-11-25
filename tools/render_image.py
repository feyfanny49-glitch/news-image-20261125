#!/usr/bin/env python3
"""Draw the news-image-20261125 poster into entry.png (build time only).

The graded entrypoint never runs this file: it only copies the PNG this script
produces. Pillow is used here, outside the sandbox, to draw flat pictograms and
large bold type that stay legible at roughly 300 pixels across.

Every character drawn is ASCII. Digits are spelled out and there is no euro
glyph, so nothing can turn into a tofu box when the image is scaled down.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

BG = "#0B1220"
CARD = "#152238"
EDGE = "#2E4361"
WHITE = "#F6F4EC"
AMBER = "#F5B841"
MUTED = "#A7B8D2"

# Explicit two-line headlines keep the composition predictable at small sizes.
STORIES = [
    dict(
        lines=("PAKISTAN", "REACHES ORBIT"),
        tag="SPACE  -  PAKISTAN",
        icon="rocket",
        accent="#63D6E8",
    ),
    dict(
        lines=("SOLOMONS", "CHOOSE AUSTRALIA"),
        tag="PACIFIC  -  TREATY",
        icon="islands",
        accent="#79D69A",
    ),
    dict(
        lines=("US READIES", "NEW TARIFFS"),
        tag="TRADE  -  SIXTEEN PARTNERS",
        icon="ship",
        accent="#F2A65A",
    ),
    dict(
        lines=("NATO CHIEF", "MEETS TRUMP"),
        tag="DIPLOMACY  -  MAR-A-LAGO",
        icon="compass",
        accent="#B9A7F7",
    ),
    dict(
        lines=("EBOLA ZONE", "EVACUATION"),
        tag="AFRICA  -  EBOLA / WHO",
        icon="hospital",
        accent="#F58585",
    ),
    dict(
        lines=("NVIDIA CHIEF", "APOLOGISES"),
        tag="TECH  -  HUANG RETURNS",
        icon="chip",
        accent="#9ED2F0",
    ),
    dict(
        lines=("IRAN WAR WIDENS", "HOUTHIS HIT RIYADH"),
        tag="MIDDLE EAST  -  ELEVEN HURT, HORMUZ TANKERS",
        icon="tower",
        accent="#FF8A6A",
        wide=True,
    ),
]


def font(size, bold=True):
    """Load a system sans face, falling back to a face Pillow ships with."""
    names = (
        [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "DejaVuSans.ttf",
        ]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fitted(text, size, max_width, bold=True):
    face = font(size, bold)
    box = ImageDraw.Draw(Image.new("RGB", (8, 8))).textbbox((0, 0), text, font=face)
    while box[2] - box[0] > max_width and size > 12:
        size -= 2
        face = font(size, bold)
        box = ImageDraw.Draw(Image.new("RGB", (8, 8))).textbbox((0, 0), text, font=face)
    return face


class Pictogram:
    """Draw in a 100 by 100 design space placed at (ox, oy) at scale `size`."""

    def __init__(self, draw, ox, oy, size, accent):
        self.d = draw
        self.ox = ox
        self.oy = oy
        self.k = size / 100.0
        self.a = accent
        self.w = max(1, round(3 * self.k))

    def pt(self, x, y):
        return (round(self.ox + x * self.k), round(self.oy + y * self.k))

    def line(self, pts, fill=None, width=None):
        self.d.line([self.pt(x, y) for x, y in pts], fill=fill or self.a,
                    width=width or self.w)

    def polygon(self, pts, fill, outline=None):
        xy = [self.pt(x, y) for x, y in pts]
        self.d.polygon(xy, fill=fill)
        if outline:
            self.d.line(xy + [xy[0]], fill=outline, width=self.w)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=None):
        self.d.rectangle([self.pt(x0, y0), self.pt(x1, y1)], fill=fill,
                         outline=outline or fill, width=width or self.w)

    def ellipse(self, x0, y0, x1, y1, fill=None, outline=None, width=None):
        self.d.ellipse([self.pt(x0, y0), self.pt(x1, y1)], fill=fill,
                       outline=outline or fill, width=width or self.w)


def draw_rocket(p):
    # Long March style rocket climbing, with a flame and a crescent and star.
    p.polygon([(46, 12), (58, 12), (62, 66), (42, 66)], WHITE)
    p.polygon([(46, 12), (52, 4), (58, 12)], AMBER)
    p.polygon([(42, 52), (30, 70), (42, 66)], p.a)
    p.polygon([(62, 52), (74, 70), (62, 66)], p.a)
    p.polygon([(46, 66), (58, 66), (52, 94)], AMBER)
    p.rect(43, 36, 61, 43, p.a)
    p.ellipse(6, 8, 28, 30, outline=WHITE, width=2)
    p.ellipse(12, 5, 30, 25, fill=BG)
    p.polygon([(67, 12), (70, 18), (77, 18), (72, 23), (74, 30), (67, 26),
               (60, 30), (62, 23), (57, 18), (64, 18)], WHITE)


def draw_islands(p):
    # Two islands joined by a treaty line, with a small shield between them.
    p.polygon([(2, 78), (16, 62), (34, 62), (46, 78)], "#3E8E6B")
    p.polygon([(54, 78), (68, 62), (86, 62), (98, 78)], "#3E8E6B")
    p.line([(10, 84), (90, 84)], p.a, width=max(2, round(4 * p.k)))
    for x in (18, 30, 72, 84):
        p.line([(x, 60), (x, 48)], "#79D69A")
        p.ellipse(x - 9, 38, x + 9, 50, "#79D69A")
    p.polygon([(42, 30), (58, 30), (58, 46), (50, 56), (42, 46)], WHITE)
    p.line([(47, 40), (50, 44), (54, 37)], p.a, width=max(2, round(3 * p.k)))


def draw_ship(p):
    # Container ship under an upward tariff arrow.
    for i, col in enumerate((p.a, AMBER, WHITE, p.a)):
        p.rect(16 + i * 18, 30, 32 + i * 18, 50, col)
    p.polygon([(8, 50), (92, 50), (82, 74), (18, 74)], WHITE)
    p.line([(6, 78), (94, 78)], p.a)
    p.line([(74, 30), (74, 10)], AMBER)
    p.polygon([(68, 18), (74, 6), (80, 18)], AMBER)


def draw_compass(p):
    # Four-point compass inside a ring, with a small podium below.
    p.ellipse(14, 6, 86, 78, outline=p.a, width=max(2, round(4 * p.k)))
    p.polygon([(50, 12), (58, 42), (88, 50), (58, 58), (50, 88), (42, 58),
               (12, 50), (42, 42)], WHITE)
    p.ellipse(43, 43, 57, 57, p.a)
    p.rect(38, 84, 62, 94, WHITE)


def draw_hospital(p):
    # Hospital block with a plain medical cross and a ringed virus nearby.
    p.rect(12, 26, 58, 90, WHITE)
    p.rect(28, 10, 42, 26, WHITE)
    p.rect(30, 42, 40, 60, "#2F8F6B")
    p.rect(24, 48, 46, 54, "#2F8F6B")
    p.ellipse(60, 44, 94, 78, outline=p.a, width=max(2, round(4 * p.k)))
    p.ellipse(71, 55, 83, 67, p.a)
    for x, y in ((75, 36), (75, 84), (56, 55), (94, 55), (62, 42), (88, 68)):
        p.line([(x, y), (x + (2 if x < 75 else -2), y + (2 if y < 60 else -2))], p.a)


def draw_chip(p):
    # Microchip with pins and a small speaker silhouette.
    p.rect(20, 20, 80, 80, outline=p.a, width=max(2, round(4 * p.k)))
    p.rect(34, 34, 66, 66, WHITE)
    for v in (32, 50, 68):
        p.line([(v, 8), (v, 20)], p.a)
        p.line([(v, 80), (v, 92)], p.a)
        p.line([(8, v), (20, v)], p.a)
        p.line([(80, v), (92, v)], p.a)
    p.ellipse(44, 40, 56, 52, p.a)


def draw_tower(p):
    # Riyadh tower under a strike, with a tanker on rough water.
    p.polygon([(38, 8), (62, 8), (66, 86), (34, 86)], WHITE)
    for y in (24, 40, 56, 72):
        p.line([(37, y), (63, y)], EDGE)
    p.line([(61, 10), (61, 3)], p.a)
    p.line([(16, 6), (36, 24)], AMBER)
    p.polygon([(22, 36), (30, 20), (36, 34), (52, 30), (40, 46), (44, 60),
               (28, 52), (14, 56), (18, 42), (8, 34)], AMBER)
    p.polygon([(70, 66), (96, 66), (90, 78), (76, 78)], p.a)
    p.line([(68, 84), (98, 84)], WHITE)
    p.line([(62, 92), (94, 92)], WHITE)


ICONS = {
    "rocket": draw_rocket,
    "islands": draw_islands,
    "ship": draw_ship,
    "compass": draw_compass,
    "hospital": draw_hospital,
    "chip": draw_chip,
    "tower": draw_tower,
}


def card(draw, x, y, w, h, story):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=EDGE, width=2)
    draw.rounded_rectangle([x, y, x + 7, y + h], radius=3, fill=story["accent"])
    wide = story.get("wide", False)
    icon_size = 132 if wide else 106
    ix = x + (22 if wide else 16)
    iy = y + (h - icon_size) // 2
    ICONS[story["icon"]](Pictogram(draw, ix, iy, icon_size, story["accent"]))
    tx = x + (186 if wide else 140)
    avail = w - (tx - x) - 18
    size = 44 if wide else 36
    face = fitted(story["lines"][0], size, avail, True)
    face2 = fitted(story["lines"][1], size, avail, True)
    line_h = getattr(face, "size", size) + 10
    block = line_h * len(story["lines"])
    ty = y + (h - block - 26) // 2
    for text, f in zip(story["lines"], (face, face2)):
        draw.text((tx, ty), text, font=f, fill=WHITE, anchor="lt")
        ty += line_h
    tagface = fitted(story["tag"], 21 if wide else 20, avail, False)
    draw.text((tx, y + h - 36), story["tag"], font=tagface,
              fill=MUTED, anchor="lt")


def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead: the date is the largest thing on the poster.
    d.text((38, 22), "WORLD NEWS", font=font(21, True), fill=AMBER, anchor="lt")
    d.text((986, 22), "WEDNESDAY", font=font(23, True), fill=WHITE,
           anchor="rt")
    d.text((38, 54), "TWENTY-FIVE NOVEMBER",
           font=fitted("TWENTY-FIVE NOVEMBER", 78, 948, True),
           fill=WHITE, anchor="lt")
    d.text((38, 134), "TWO THOUSAND TWENTY-SIX",
           font=fitted("TWO THOUSAND TWENTY-SIX", 64, 948, True),
           fill=AMBER, anchor="lt")
    d.rectangle([38, 196, 986, 200], fill=AMBER)

    margin, gap = 30, 14
    card_w = (W - 2 * margin - gap) // 2
    row_h = 176
    y = 208
    for i in (0, 1):
        card(d, margin + i * (card_w + gap), y, card_w, row_h, STORIES[i])
    for i in (2, 3):
        card(d, margin + (i - 2) * (card_w + gap), y + row_h + gap,
             card_w, row_h, STORIES[i])
    for i in (4, 5):
        card(d, margin + (i - 4) * (card_w + gap), y + 2 * (row_h + gap),
             card_w, row_h, STORIES[i])
    card(d, margin, y + 3 * (row_h + gap), W - 2 * margin, 206, STORIES[6])

    out = Path(__file__).resolve().parents[1] / "entry.png"
    img.save(out, format="PNG", optimize=True, compress_level=9)
    print(f"rendered {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    render()
