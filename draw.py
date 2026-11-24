#!/usr/bin/env python3
"""Draw the 24 November 2026 one-day world news poster (1024x1024).

Original line-art illustrations only: every picture is drawn with Pillow
primitives (rectangles, ellipses, polygons, lines, arcs). No external
images, no network, no fonts beyond the system DejaVu family.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (246, 241, 231)
NAVY = (22, 35, 60)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
INK = (26, 26, 26)
GREY = (74, 74, 68)
BORDER = (217, 210, 194)
LIGHT_GREY = (120, 118, 110)


def font(name, size):
    return ImageFont.truetype(name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(draw, cx, y, text, fnt, fill, spacing=6):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


# ---------------------------------------------------------------- scenes
def scene_estonia(d, x, y, w, h):
    """Border fence, warning triangle, Estonian tricolour flag."""
    d.rectangle([x, y, x + w, y + h], fill=(223, 232, 238))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(170, 190, 170))
    # flag pole + tricolour (blue / black / white)
    px = x + 26
    d.rectangle([px, y + 8, px + 4, y + h - 26], fill=(60, 60, 60))
    fx, fy = px + 4, y + 10
    for i, col in enumerate([(0, 114, 206), (20, 20, 20), (255, 255, 255)]):
        d.rectangle([fx, fy + i * 11, fx + 52, fy + i * 11 + 11], fill=col)
        d.rectangle([fx, fy + i * 11, fx + 52, fy + i * 11 + 11],
                    outline=(120, 120, 120))
    # fence posts and rails
    for i in range(5):
        fx2 = x + 110 + i * 62
        d.rectangle([fx2, y + 34, fx2 + 7, y + h - 26], fill=(90, 70, 50))
    d.rectangle([x + 100, y + 44, x + w - 12, y + 50], fill=(90, 70, 50))
    d.rectangle([x + 100, y + 62, x + w - 12, y + 68], fill=(90, 70, 50))
    # barbed wire zigzag
    pts = []
    for i in range(9):
        pts.append((x + 100 + i * 38, y + 30 if i % 2 == 0 else y + 40))
    d.line(pts, fill=(70, 70, 70), width=2)
    # warning triangle
    cx, cy = x + w - 62, y + 52
    d.polygon([(cx, cy - 26), (cx - 26, cy + 18), (cx + 26, cy + 18)],
              fill=(214, 48, 49), outline=(140, 20, 20))
    d.polygon([(cx, cy - 18), (cx - 19, cy + 13), (cx + 19, cy + 13)],
              fill=(255, 255, 255))
    d.rectangle([cx - 2, cy - 10, cx + 2, cy + 2], fill=(214, 48, 49))
    d.ellipse([cx - 2, cy + 6, cx + 2, cy + 10], fill=(214, 48, 49))


def scene_iran(d, x, y, w, h):
    """Missile on a dashed arc over a stylised map, target star."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 58, 74))
    # stars
    for sx, sy in [(30, 14), (90, 26), (160, 10), (250, 22), (330, 12),
                   (400, 26), (60, 52), (200, 40)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(200, 220, 230))
    # ground silhouette
    d.polygon([(x, y + h), (x, y + h - 18), (x + 90, y + h - 30),
               (x + 200, y + h - 16), (x + 320, y + h - 26),
               (x + w, y + h - 14), (x + w, y + h)],
              fill=(10, 38, 50))
    # dashed trajectory arc
    prev = None
    for t in range(0, 101, 4):
        ax = x + 60 + t * 3.4
        ay = y + h - 24 - (t / 100.0) ** 1.6 * (h - 34)
        if prev and (t // 4) % 2 == 0:
            d.line([prev, (ax, ay)], fill=(255, 214, 90), width=3)
        prev = (ax, ay)
    # target star at arc end
    tx, ty = x + 60 + 340, y + h - 24 - (h - 34)
    for k in range(5):
        import math
        a1 = math.radians(-90 + k * 72)
        a2 = math.radians(-90 + k * 72 + 36)
        d.polygon([(tx + 13 * math.cos(a1), ty + 13 * math.sin(a1)),
                   (tx + 5 * math.cos(a2), ty + 5 * math.sin(a2)),
                   (tx + 13 * math.cos(a1 + math.radians(72)),
                    ty + 13 * math.sin(a1 + math.radians(72)))],
                  fill=(255, 214, 90))
    # missile body along the arc, nose up-right
    mx, my = x + 120, y + h - 52
    d.polygon([(mx, my - 26), (mx + 12, my - 6), (mx + 8, my + 16),
               (mx - 8, my + 16), (mx - 12, my - 6)], fill=(230, 230, 230))
    d.polygon([(mx, my - 26), (mx + 7, my - 10), (mx - 7, my - 10)],
              fill=(214, 48, 49))
    d.rectangle([mx - 14, my + 10, mx - 6, my + 18], fill=(150, 150, 150))
    d.rectangle([mx + 6, my + 10, mx + 14, my + 18], fill=(150, 150, 150))
    d.polygon([(mx - 6, my + 18), (mx + 6, my + 18), (mx + 2, my + 34),
               (mx - 2, my + 34)], fill=(255, 140, 0))
    d.polygon([(mx - 3, my + 18), (mx + 3, my + 18), (mx, my + 28)],
              fill=(255, 214, 90))


def scene_china(d, x, y, w, h):
    """Sealed document, red stamp, judge's gavel."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    # document
    dx, dy = x + 24, y + 10
    d.rectangle([dx, dy, dx + 210, dy + h - 20], fill=WHITE,
                outline=(150, 140, 120), width=2)
    d.rectangle([dx + 14, dy + 12, dx + 120, dy + 22], fill=(40, 40, 40))
    for i in range(5):
        ly = dy + 34 + i * 11
        d.line([(dx + 14, ly), (dx + 196, ly)], fill=(170, 165, 150), width=2)
    # red seal over the document corner
    sx, sy = dx + 168, dy + h - 52
    d.ellipse([sx - 24, sy - 24, sx + 24, sy + 24], outline=(178, 34, 34),
              width=4)
    d.ellipse([sx - 17, sy - 17, sx + 17, sy + 17], outline=(178, 34, 34),
              width=2)
    d.polygon([(sx, sy - 10), (sx + 3, sy - 3), (sx + 10, sy - 3),
               (sx + 5, sy + 2), (sx + 7, sy + 9), (sx, sy + 5),
               (sx - 7, sy + 9), (sx - 5, sy + 2), (sx - 10, sy - 3),
               (sx - 3, sy - 3)], fill=(178, 34, 34))
    # gavel: short thick head on a handle, lower right
    gx, gy = x + 300, y + 30
    d.polygon([(gx, gy), (gx + 62, gy - 16), (gx + 70, gy + 8),
               (gx + 8, gy + 24)], fill=(120, 72, 32))
    d.polygon([(gx + 62, gy - 16), (gx + 70, gy + 8), (gx + 78, gy + 2),
               (gx + 70, gy - 22)], fill=(90, 52, 22))
    d.rectangle([gx + 28, gy + 14, gx + 40, gy + 62], fill=(150, 100, 50))
    d.rectangle([gx + 16, gy + 58, gx + 126, gy + 66], fill=(90, 52, 22))


def scene_indonesia(d, x, y, w, h):
    """Factory with sawtooth roof, flames and smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 200))
    # smoke
    for cx, cy, r in [(120, 26, 14), (150, 16, 18), (185, 28, 13),
                      (330, 20, 16), (360, 32, 12)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(150, 148, 142))
    # factory block
    d.rectangle([x + 60, y + 46, x + w - 60, y + h - 8], fill=(96, 96, 100))
    # sawtooth roof
    d.polygon([(x + 60, y + 46), (x + 130, y + 18), (x + 200, y + 46),
               (x + 270, y + 18), (x + 340, y + 46), (x + w - 60, y + 46)],
              fill=(70, 70, 74))
    # windows
    for i in range(4):
        wx = x + 84 + i * 78
        d.rectangle([wx, y + 60, wx + 44, y + 78], fill=(255, 214, 90))
    # door
    d.rectangle([x + w // 2 - 20, y + h - 34, x + w // 2 + 20, y + h - 8],
                fill=(50, 50, 54))
    # chimney
    d.rectangle([x + w - 96, y + 8, x + w - 78, y + 46], fill=(80, 80, 84))
    # flames
    fx = x + 110
    for i, (fw, fh, col) in enumerate([(70, 42, (255, 120, 0)),
                                       (46, 30, (255, 170, 0)),
                                       (26, 20, (255, 220, 90))]):
        d.polygon([(fx - fw // 2, y + h - 8), (fx - fw // 4, y + h - 8 - fh),
                   (fx, y + h - 8 - fh - 12), (fx + fw // 4, y + h - 8 - fh),
                   (fx + fw // 2, y + h - 8)], fill=col)
        fx += 120


def scene_korea(d, x, y, w, h):
    """Government hall with columns and the Taegeuk flag."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 234, 244))
    # flag pole + Taegeukgi (simplified: white field, red/blue circle)
    px = x + 30
    d.rectangle([px, y + 8, px + 4, y + h - 10], fill=(60, 60, 60))
    fx, fy = px + 4, y + 10
    d.rectangle([fx, fy, fx + 62, fy + 40], fill=WHITE,
                outline=(150, 150, 150))
    d.pieslice([fx + 20, fy + 8, fx + 42, fy + 32], 90, 270, fill=(205, 46, 58))
    d.pieslice([fx + 20, fy + 8, fx + 42, fy + 32], 270, 90, fill=(0, 71, 160))
    d.ellipse([fx + 25, fy + 13, fx + 37, fy + 27], fill=(205, 46, 58))
    # hall: pediment + columns + steps
    hx = x + 130
    d.polygon([(hx, y + 22), (hx + 140, y + 22), (hx + 70, y + 2)],
              fill=(120, 120, 126))
    d.rectangle([hx, y + 22, hx + 140, y + 30], fill=(90, 90, 96))
    for i in range(4):
        cx = hx + 16 + i * 36
        d.rectangle([cx, y + 30, cx + 14, y + h - 26], fill=(240, 240, 236),
                    outline=(150, 150, 150))
    d.rectangle([hx - 8, y + h - 26, hx + 148, y + h - 18], fill=(90, 90, 96))
    d.rectangle([hx - 16, y + h - 18, hx + 156, y + h - 10], fill=(70, 70, 74))
    # sun
    d.ellipse([x + w - 66, y + 10, x + w - 34, y + 42], fill=(255, 200, 60))
    # small trees
    for tx in (x + w - 96, x + 120):
        d.polygon([(tx, y + h - 44), (tx - 12, y + h - 18),
                   (tx + 12, y + h - 18)], fill=(46, 120, 70))


def scene_un_ai(d, x, y, w, h):
    """Globe with circuit nodes and a shield."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    cx, cy, r = x + w // 2 - 40, y + h // 2, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 180),
              outline=(20, 60, 110), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=2)
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=WHITE, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=WHITE, width=2)
    # circuit nodes around the globe
    nodes = [(x + 40, y + 18), (x + 70, y + h - 20), (x + w - 120, y + 16),
             (x + w - 44, y + h - 24), (x + w - 70, y + h // 2)]
    for nx, ny in nodes:
        d.line([(nx, ny), (cx, cy)], fill=(90, 130, 90), width=2)
        d.rectangle([nx - 6, ny - 6, nx + 6, ny + 6], fill=(46, 120, 70),
                    outline=(20, 70, 30))
    # shield, lower right
    sx, sy = x + w - 78, y + h - 58
    d.polygon([(sx, sy), (sx + 34, sy), (sx + 34, sy + 20),
               (sx + 17, sy + 38), (sx, sy + 20)], fill=(255, 255, 255),
              outline=(46, 120, 70), width=3)
    d.line([(sx + 10, sy + 18), (sx + 15, sy + 24), (sx + 25, sy + 10)],
           fill=(46, 120, 70), width=3)


SCENES = {
    "estonia": scene_estonia,
    "iran": scene_iran,
    "china": scene_china,
    "indonesia": scene_indonesia,
    "korea": scene_korea,
    "un_ai": scene_un_ai,
}

STORIES = [
    {
        "tag": "EUROPE",
        "accent": (176, 42, 48),
        "scene": "estonia",
        "head": "Russia warns Estonia of \u201copen war\u201d",
        "body": "Moscow summons Tallinn\u2019s envoy over claims Kyiv uses its airspace; Estonia denies it. Its border shuts Dec. 1.",
    },
    {
        "tag": "MIDDLE EAST",
        "accent": (122, 31, 31),
        "scene": "iran",
        "head": "Iran: missiles can now reach Europe",
        "body": "A lawmaker says the range rose to 4,500 km; a Tehran paper maps \u201call of Europe within range.\u201d",
    },
    {
        "tag": "ASIA",
        "accent": (140, 29, 24),
        "scene": "china",
        "head": "China: death sentence for spying",
        "body": "An official known only as Ma is convicted of passing 35 state secrets to a foreign agency for over 1m yuan.",
    },
    {
        "tag": "ASIA",
        "accent": (217, 108, 0),
        "scene": "indonesia",
        "head": "24 dead in Indonesia factory fire",
        "body": "A blaze at a sweets plant near Jakarta; about 30 people are still missing as rescuers search the wreckage.",
    },
    {
        "tag": "ASIA",
        "accent": (31, 78, 121),
        "scene": "korea",
        "head": "Seoul shuffles its top security team",
        "body": "Lee Jae Myung names a new foreign minister and the first woman to lead the spy agency.",
    },
    {
        "tag": "WORLD",
        "accent": (46, 107, 52),
        "scene": "un_ai",
        "head": "UN chief: agree AI safety rules in a year",
        "body": "Guterres calls for a global AI risk framework at a summit in Barbados.",
    },
]


def draw_card(d, x, y, w, h, story):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BORDER, width=2)
    d.rectangle([x + 2, y + 2, x + w - 2, y + 8], fill=story["accent"])
    pad = 16
    inner_w = w - 2 * pad
    # tag chip
    tag_f = font(SANS_B, 13)
    tag_w = d.textlength(story["tag"], font=tag_f) + 18
    ty = y + 16
    d.rectangle([x + pad, ty, x + pad + tag_w, ty + 22], fill=story["accent"])
    d.text((x + pad + 9, ty + 4), story["tag"], font=tag_f, fill=WHITE)
    # illustration band
    iy = ty + 30
    ih = 96
    SCENES[story["scene"]](d, x + pad, iy, inner_w, ih)
    d.rectangle([x + pad, iy, x + pad + inner_w, iy + ih], outline=BORDER)
    # headline (max 2 lines)
    hf = font(SANS_B, 22)
    lines = wrap(d, story["head"], hf, inner_w)[:2]
    hy = iy + ih + 10
    for ln in lines:
        d.text((x + pad, hy), ln, font=hf, fill=INK)
        hy += 27
    # summary (max 3 lines)
    bf = font(SANS, 15)
    blines = wrap(d, story["body"], bf, inner_w)[:3]
    by = hy + 4
    for ln in blines:
        d.text((x + pad, by), ln, font=bf, fill=GREY)
        by += 20


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 120], fill=GOLD)
    title_f = font(SERIF_B, 48)
    d.text((W // 2, 12), "THE WORLD TODAY", font=title_f, fill=WHITE,
           anchor="ma")
    date_f = font(SANS_B, 25)
    draw_spaced(d, W // 2, 72, "TUESDAY  24  NOVEMBER  2026", date_f, GOLD,
                spacing=4)
    # grid of six stories
    margin, gap = 20, 14
    card_w = (W - 2 * margin - gap) // 2
    top = 132
    row_h = (994 - top - 2 * gap) // 3
    for i, story in enumerate(STORIES):
        cx = margin + (i % 2) * (card_w + gap)
        cy = top + (i // 2) * (row_h + gap)
        draw_card(d, cx, cy, card_w, row_h, story)
    # footer
    foot_f = font(SANS, 13)
    d.text((W // 2, 1002),
           "Sources: Reuters  ·  AP  ·  UN News  ·  Iran International  ·  "
           "Korea JoongAng Daily   —   stories first reported 23\u201324 November 2026",
           font=foot_f, fill=LIGHT_GREY, anchor="ma")
    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
