#!/usr/bin/env python3
"""Render 'THE WORLD TODAY' newspaper front page, 21 November 2026.

Deterministic: fixed layout, fixed fonts, no randomness, no network.
Output: entry.png (1024x1024) in this directory.
"""

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
W, H = 1024, 1024
MARGIN = 34
GAP = 16
BG = (250, 246, 236)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (158, 28, 28)
MUTED = (90, 84, 76)
PANEL = (255, 253, 248)
PANEL_ALT = (244, 238, 226)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=4):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def pictogram(draw, x, y, w, h, kind):
    """Simple geometric pictogram for a story, drawn in code."""
    cx, cy = x + w // 2, y + h // 2
    if kind == "markets":
        # falling chart: axes + descending red line
        draw.line([(x + 8, y + h - 8), (x + w - 8, y + h - 8)], fill=INK, width=3)
        draw.line([(x + 8, y + h - 8), (x + 8, y + 8)], fill=INK, width=3)
        pts = [(x + 14, y + 14), (x + 34, y + 26), (x + 54, y + 22),
               (x + 74, y + 44), (x + 94, y + 40), (x + 114, y + 62)]
        draw.line(pts, fill=ACCENT, width=5, joint="curve")
        draw.polygon([(x + 114, y + 62), (x + 104, y + 56), (x + 106, y + 70)],
                     fill=ACCENT)
    elif kind == "weather":
        # cyclone spiral: concentric arcs
        for r, col in [(52, INK), (40, ACCENT), (28, INK), (16, ACCENT)]:
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=5)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=ACCENT)
    elif kind == "ukraine":
        # explosion burst: radiating triangles
        for ang in range(0, 360, 30):
            import math
            a = math.radians(ang)
            x1 = cx + int(14 * math.cos(a))
            y1 = cy + int(14 * math.sin(a))
            x2 = cx + int(52 * math.cos(a))
            y2 = cy + int(52 * math.sin(a))
            draw.line([(x1, y1), (x2, y2)], fill=ACCENT, width=5)
        draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=ACCENT)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 220, 90))
    elif kind == "brazil":
        # hospital cross in a circle
        draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=INK, width=4)
        draw.rectangle([cx - 12, cy - 34, cx + 12, cy + 34], fill=ACCENT)
        draw.rectangle([cx - 34, cy - 12, cx + 34, cy + 12], fill=ACCENT)
    elif kind == "pakistan":
        # warning triangle with exclamation
        draw.polygon([(cx, cy - 50), (cx - 52, cy + 42), (cx + 52, cy + 42)],
                     outline=INK, width=4)
        draw.rectangle([cx - 5, cy - 28, cx + 5, cy + 8], fill=ACCENT)
        draw.ellipse([cx - 5, cy + 18, cx + 5, cy + 28], fill=ACCENT)
    elif kind == "sport":
        # cricket bat and ball
        draw.rounded_rectangle([cx - 54, cy - 16, cx + 34, cy + 16],
                               radius=8, fill=(210, 170, 110), outline=INK, width=3)
        draw.rectangle([cx + 34, cy - 7, cx + 58, cy + 7], fill=(120, 80, 40))
        draw.ellipse([cx + 28, cy - 56, cx + 58, cy - 26], fill=ACCENT,
                     outline=INK, width=2)


STORIES = [
    ("MARKETS", "US stocks plunge in deepening AI sell-off",
     "Nasdaq falls 5.28% and Nvidia drops about 14% in Friday's rout.",
     "markets"),
    ("WEATHER", "Cyclone Akvan strikes Odisha coast",
     "The storm crosses near Gopalpur, bringing strong winds and heavy rain.",
     "weather"),
    ("UKRAINE", "Strikes hit Kryvyi Rih",
     "Russian missile and drone attacks kill 2 and injure 42, including 4 children.",
     "ukraine"),
    ("BRAZIL", "Bolsonaro taken to hospital",
     "The imprisoned ex-president is moved for treatment of severe abdominal pain.",
     "brazil"),
    ("PAKISTAN", "Suicide bombing kills 5 at checkpoint",
     "A car bomb at a security post kills 5 and injures 13.",
     "pakistan"),
    ("SPORT", "India fight back in Wellington Test",
     "India reach 159/1 at stumps on Day 2, trailing New Zealand by 209.",
     "sport"),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead
    title_f = font("DejaVuSerif-Bold.ttf", 74)
    d.text((W // 2, 30), "THE WORLD TODAY", font=title_f, fill=INK, anchor="mt")
    d.line([(MARGIN, 118), (W - MARGIN, 118)], fill=RULE, width=4)
    sub_f = font("DejaVuSans-Bold.ttf", 24)
    d.text((MARGIN, 132), "SATURDAY 21 NOVEMBER 2026", font=sub_f, fill=ACCENT)
    d.text((W - MARGIN, 132), "ONE IMAGE  •  SIX STORIES", font=sub_f,
           fill=MUTED, anchor="rt")
    d.line([(MARGIN, 168), (W - MARGIN, 168)], fill=RULE, width=2)

    # 2x3 grid of stories
    top = 186
    cell_w = (W - 2 * MARGIN - GAP) // 2
    cell_h = (H - top - MARGIN - 2 * GAP - 26) // 3
    tag_f = font("DejaVuSans-Bold.ttf", 20)
    head_f = font("DejaVuSerif-Bold.ttf", 27)
    body_f = font("DejaVuSans.ttf", 21)

    for i, (tag, headline, summary, kind) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = MARGIN + col * (cell_w + GAP)
        y = top + row * (cell_h + GAP)
        fill = PANEL if (row + col) % 2 == 0 else PANEL_ALT
        d.rectangle([x, y, x + cell_w, y + cell_h], fill=fill,
                    outline=RULE, width=2)
        # pictogram on the left
        px, py, pw, ph = x + 14, y + 14, 130, 130
        d.rectangle([px, py, px + pw, py + ph], fill=BG, outline=MUTED, width=1)
        pictogram(d, px, py, pw, ph, kind)
        tx = x + 158
        tw = cell_w - 158 - 14
        d.text((tx, y + 16), tag, font=tag_f, fill=ACCENT)
        y2 = draw_wrapped(d, tx, y + 48, headline, head_f, tw, leading=2)
        draw_wrapped(d, tx, y2 + 6, summary, body_f, tw, fill=MUTED, leading=3)

    # Footer
    d.line([(MARGIN, H - MARGIN - 4), (W - MARGIN, H - MARGIN - 4)],
           fill=RULE, width=2)
    foot_f = font("DejaVuSans.ttf", 16)
    d.text((W // 2, H - MARGIN + 4),
           "Compiled from reporting published Saturday 21 November 2026.",
           font=foot_f, fill=MUTED, anchor="mt")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
