# draw.py — draws entry.png for the news-image-20261123 bounty.
#
# A newspaper-style front page, 1024x1024, summarising the world news of
# Monday 23 November 2026 in six panels. Every shape and every word is drawn
# here with Pillow, from the story list below — no photographs, no copied
# artwork, no network. Run:  python3 draw.py   (writes entry.png next to it)

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
GREY = (74, 74, 66)
NAVY = (27, 42, 74)
GOLD = (242, 193, 78)
CARD = (255, 255, 255)
CARD_EDGE = (216, 210, 196)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# --- The six stories of Monday 23 November 2026 -------------------------
# Headlines and summaries follow what Reuters, AP, AFP, UN News and
# Al Jazeera reported on the day. Each panel: (colour, kicker, headline,
# summary, glyph).
STORIES = [
    (
        (178, 34, 24),  # red
        "CLIMATE · ANTALYA",
        "COP31 ends with no deal",
        "UN climate talks close without an agreement — the first failure "
        "since 2009 — as nearly 200 nations split over fossil fuels.",
        "sun",
    ),
    (
        (14, 90, 120),  # deep teal
        "CONFLICT · LIBYA",
        "Ukraine sinks Russian warship in Libya",
        "President Zelenskyy says seven sea drones sank the corvette "
        "Merkury at Benghazi — the war reaches a new sea.",
        "ship",
    ),
    (
        (46, 94, 140),  # steel blue
        "MARKETS · NEW YORK",
        "Nvidia brings back its chief",
        "Jensen Huang returns as CEO 11 days after resigning; shares jump "
        "about 33% and the S&P 500 climbs 4.8%.",
        "chip",
    ),
    (
        (122, 63, 154),  # purple
        "MARKETS · SEOUL",
        "AI sell-off hits Asia",
        "South Korea's Kospi falls 3.3% to its lowest close since January "
        "as doubts over AI spending spread.",
        "chart",
    ),
    (
        (176, 96, 0),  # amber
        "WAR · UKRAINE",
        "Strike kills 11 in Dymer",
        "A Russian drone strike on an apartment block near Kyiv kills 11 "
        "people, rescuers say.",
        "building",
    ),
    (
        (46, 125, 50),  # green
        "POLITICS · ISRAEL",
        "Coalition talks collapse",
        "Netanyahu's Likud and Eisenkot's Yashar end unity talks without a "
        "deal, leaving Israel's next government uncertain.",
        "columns",
    ),
]


def glyph(draw, kind, cx, cy, r, colour):
    """A small white pictogram inside a coloured disc."""
    white = (255, 255, 255)
    if kind == "sun":  # a sun: disc with rays
        draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                     fill=white)
        for i in range(8):
            a = math.pi * i / 4
            x1 = cx + int(math.cos(a) * (r // 2 + 4))
            y1 = cy + int(math.sin(a) * (r // 2 + 4))
            x2 = cx + int(math.cos(a) * (r // 2 + 13))
            y2 = cy + int(math.sin(a) * (r // 2 + 13))
            draw.line([x1, y1, x2, y2], fill=white, width=4)
    elif kind == "ship":  # hull, mast and flag
        draw.polygon([(cx - 26, cy + 2), (cx + 26, cy + 2),
                      (cx + 18, cy + 18), (cx - 18, cy + 18)], fill=white)
        draw.line([cx, cy - 26, cx, cy + 2], fill=white, width=4)
        draw.polygon([(cx, cy - 26), (cx + 16, cy - 20), (cx, cy - 14)],
                     fill=white)
        draw.line([cx - 26, cy - 4, cx + 26, cy - 4], fill=white, width=3)
    elif kind == "chip":  # a processor: square, core, pins
        draw.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20],
                               radius=5, outline=white, width=4)
        draw.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=white)
        for dx in (-26, 26):
            for dy in (-12, 0, 12):
                draw.line([cx + dx, cy + dy, cx + dx + (6 if dx < 0 else -6),
                           cy + dy], fill=white, width=3)
        for dy in (-26, 26):
            for dx in (-12, 0, 12):
                draw.line([cx + dx, cy + dy, cx + dx,
                           cy + dy + (6 if dy < 0 else -6)], fill=white,
                          width=3)
    elif kind == "chart":  # falling market line with an arrow
        draw.line([cx - 26, cy + 22, cx - 26, cy - 24], fill=white, width=4)
        draw.line([cx - 26, cy + 22, cx + 26, cy + 22], fill=white, width=4)
        draw.line([cx - 22, cy - 16, cx - 8, cy - 2, cx + 4, cy - 10,
                   cx + 22, cy + 14], fill=white, width=4)
        draw.polygon([(cx + 22, cy + 14), (cx + 22, cy + 4),
                      (cx + 12, cy + 14)], fill=white)
    elif kind == "building":  # a block with windows
        draw.rectangle([cx - 20, cy - 24, cx + 20, cy + 24], fill=white)
        for row in (-14, -2, 10):
            for col in (-12, 0, 12):
                draw.rectangle([cx + col - 4, cy + row - 4,
                                cx + col + 4, cy + row + 4], fill=colour)
    elif kind == "columns":  # a parliament front: pediment, pillars, base
        draw.polygon([(cx - 26, cy - 8), (cx + 26, cy - 8), (cx, cy - 24)],
                     fill=white)
        for dx in (-18, 0, 18):
            draw.rectangle([cx + dx - 4, cy - 4, cx + dx + 4, cy + 18],
                           fill=white)
        draw.rectangle([cx - 28, cy + 18, cx + 28, cy + 24], fill=white)


def draw_panel(img, x, y, w, h, story):
    colour, kicker, headline, summary, kind = story
    d = ImageDraw.Draw(img)
    # card
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CARD,
                        outline=CARD_EDGE, width=1)
    d.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=colour)
    d.rectangle([x, y + 5, x + w, y + 10], fill=colour)
    # pictogram disc
    cx, cy, r = x + 60, y + 64, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    glyph(d, kind, cx, cy, r, colour)
    # kicker + headline, right of the disc
    tx = x + 116
    d.text((tx, y + 26), kicker, font=font(SANS_BOLD, 17), fill=colour)
    hl = wrap(d, headline, font(SANS_BOLD, 27), w - 136)
    yy = y + 52
    for line in hl[:3]:
        d.text((tx, yy), line, font=font(SANS_BOLD, 27), fill=INK)
        yy += 32
    # summary across the full width, under the disc
    sy = y + 148
    for line in wrap(d, summary, font(SANS, 20), w - 40)[:3]:
        d.text((x + 20, sy), line, font=font(SANS, 20), fill=GREY)
        sy += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((W // 2, 22), "THE WORLD IN ONE DAY",
           font=font(SERIF_BOLD, 52), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 88), "MONDAY, 23 NOVEMBER 2026",
           font=font(SANS_BOLD, 30), fill=GOLD, anchor="ma")
    d.text((W // 2, 126), "Six stories that shaped the day — as reported around the world",
           font=font(SANS, 17), fill=(200, 208, 224), anchor="ma")

    # --- six panels: 2 columns x 3 rows -------------------------------
    margin, gap = 24, 10
    pw = (W - 2 * margin - gap) // 2
    ph = 262
    top = 162
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        draw_panel(img, x, y, pw, ph, story)

    # --- footer --------------------------------------------------------
    d.text((W // 2, 978),
           "Sources: Reuters · AP · AFP · UN News · Al Jazeera — as reported on 23 November 2026",
           font=font(SANS, 16), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
