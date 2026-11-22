"""GG1v2 — boarding pass for a 13-year layover, funny layer strengthened.

Same winning frame as GG1 (cream pass, perforated stub, ghost passenger,
LAYOVER 4,811 DAYS instant gag, all anchors). Changes per duel evidence:
a stack of deadpan S2c-style gags added (gate / pilot / snacks / aged),
a big red "13 YEARS LATE" stamp (the #1 receipt's proven visual gag),
and the closing pitch strengthened to #1's explicit wording (agent +
bounty earned on make.fun), woven into the pass. Footer last.

Self-contained build: drawing primitives from tools/make_meme2.py (same
campaign kit); the footer is replicated here verbatim, as in make_z5.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_meme2 import (  # noqa: E402
    W, H, PAPER, INK, WHITE, MAGENTA, MAGENTA_DARK, STAMP_RED, GREY, GOLD,
    SANS_B, SANS_R, font, tw, fit_font, draw_ghost, draw_coin, sparkle,
    ctext, stamp,
)
from PIL import Image, ImageDraw  # noqa: E402

MX = 56
RIGHT = W - MX
USED = []  # (label, actual px size) for the report


def footer(img, d):
    d.rectangle([0, H - 140, W, H], fill=MAGENTA)
    draw_ghost(d, MX + 6, H - 124, 104, 116, ow=8)
    d.text((MX + 146, H - 116), "PAID BY MY AI AGENT",
           font=font(SANS_B, 44), fill=WHITE)
    d.text((MX + 146, H - 64), "with real money it earned on",
           font=font(SANS_R, 33), fill=WHITE)
    pill_w, pill_h = 252, 62
    px, py = MX + 146 + tw(d, "with real money it earned on ",
                           font(SANS_R, 33)) + 6, H - 74
    d.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=31,
                        fill=WHITE)
    pf = font(SANS_B, 40)
    d.text((px + (pill_w - tw(d, "make.fun", pf)) / 2, py + 8), "make.fun",
           font=pf, fill=INK)


def F(label, text, size, max_w, path=SANS_B):
    """fit_font wrapper that records the actual size used."""
    f = fit_font(_d, text, path, size, max_w)
    USED.append((label, f.size))
    return f


def build():
    global _d
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    _d = d
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)

    # --- header band ---
    d.rectangle([6, 6, W - 6, 104], fill=INK)
    d.text((MX, 30), "LEONIDA AIR", font=F("brand", "LEONIDA AIR", 50, 560),
           fill=WHITE)
    bp = F("band-right", "BOARDING PASS", 44, 400)
    d.text((RIGHT - tw(d, "BOARDING PASS", bp), 36), "BOARDING PASS",
           font=bp, fill=(255, 138, 199))

    # --- passenger + route (full width) ---
    d.text((MX, 116), "PASSENGER: A GTA FAN",
           font=F("passenger", "PASSENGER: A GTA FAN", 46, 968), fill=INK)
    d.text((MX, 166), "LOS SANTOS → LEONIDA",
           font=F("route", "LOS SANTOS → LEONIDA", 84, 968), fill=INK)
    d.line([MX, 238, RIGHT, 238], fill=INK, width=3)

    # --- perforated stub edge (right) ---
    for yy in range(258, 600, 18):
        d.ellipse([668, yy, 673, yy + 5], fill=GREY)

    # --- left column: flight facts + first deadpan gags ---
    col_w = 664 - MX  # 56..664
    d.text((MX, 252), "DEPARTED SEP 17, 2013",
           font=F("departed", "DEPARTED SEP 17, 2013", 48, col_w), fill=INK)
    d.text((MX, 306), "LAYOVER 4,811 DAYS",
           font=F("layover", "LAYOVER 4,811 DAYS", 54, col_w), fill=MAGENTA)
    d.text((MX, 366), "ARRIVED: NOV 19, 2026",
           font=F("arrived", "ARRIVED: NOV 19, 2026", 48, col_w), fill=INK)
    d.text((MX, 418), "SEAT 13A: JASON & LUCIA",
           font=F("seat", "SEAT 13A: JASON & LUCIA", 46, col_w), fill=INK)
    d.text((MX, 466), "BAGGAGE: 214 GB",
           font=F("baggage", "BAGGAGE: 214 GB", 46, col_w), fill=INK)
    d.text((MX, 514), "PILOT: RETIRED. TWICE.",
           font=F("pilot", "PILOT: RETIRED. TWICE.", 46, col_w), fill=INK)
    d.text((MX, 562), "SNACKS: EXPIRED 2019",
           font=F("snacks", "SNACKS: EXPIRED 2019", 46, col_w), fill=INK)

    # --- the ghost passenger in the stub, holding coin + make.fun sign ---
    gx, gy, gw, gh = 700, 250, 290, 330
    draw_ghost(d, gx, gy, gw, gh)
    draw_coin(d, gx + gw - 8, gy + int(gh * 0.52) + 10, 33)
    sparkle(d, 694, 264, 11, GOLD)
    sparkle(d, 1008, 260, 9, GOLD)
    d.rounded_rectangle([716, 422, 940, 494], radius=14, fill=WHITE,
                        outline=INK, width=6)
    ctext(d, 828, 436, "make.fun", F("sign", "make.fun", 44, 200), INK)

    # --- the visual gag: big red 13 YEARS LATE stamp over the stub base ---
    stamp(img, "13 YEARS LATE", 810, 568, 46, STAMP_RED, angle=-10)
    USED.append(("stamp", 46))
    d = ImageDraw.Draw(img)
    _d = d

    d.line([MX, 642, RIGHT, 642], fill=INK, width=3)

    # --- bottom stack: delays + trailer anchors, remaining gags, pitch ---
    d.text((MX, 654), "FALL 2025, MAY 2026 — SURVIVED BOTH",
           font=F("delays", "FALL 2025, MAY 2026 — SURVIVED BOTH",
                  48, 968), fill=INK)
    d.text((MX, 702), "MOVIE: SAME TRAILER FOR 13 YEARS",
           font=F("movie", "MOVIE: SAME TRAILER FOR 13 YEARS",
                  46, 968), fill=INK)
    d.text((MX, 750), "GATE CHANGED: 214 TIMES",
           font=F("gate", "GATE CHANGED: 214 TIMES", 46, 968), fill=INK)
    d.text((MX, 798), "PASSENGER AGED: 13 YEARS",
           font=F("aged", "PASSENGER AGED: 13 YEARS", 46, 968), fill=INK)
    d.text((MX, 846), "TICKET $79.99 — PAID BY HIS AI AGENT",
           font=F("pitch1", "TICKET $79.99 — PAID BY HIS AI AGENT",
                  48, 968), fill=MAGENTA_DARK)
    d.text((MX, 894), "WITH A BOUNTY IT EARNED ON MAKE.FUN",
           font=F("pitch2", "WITH A BOUNTY IT EARNED ON MAKE.FUN",
                  46, 968), fill=MAGENTA_DARK)

    footer(img, d)
    return img


if __name__ == "__main__":
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "meme", "candidate-gg1v2.png")
    img.save(out)
    print(out)
    for label, size in USED:
        print(f"{label}: {size}px")
