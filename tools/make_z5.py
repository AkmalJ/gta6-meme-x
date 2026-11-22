"""Z5 — PERFORMANCE REVIEW (challenger champion, 22 Nov tournament).

The employee is the player's own patience, hired on GTA V's launch day and
reviewed by the release date itself. Every row is a straight-faced HR verdict
that is also the joke; the decision PROMOTED lands in the stamp slot, and the
closing pays the fantasy off: you start in Vice City.

Self-contained document build: layout helpers below, drawing primitives
from tools/make_meme2.py (same campaign kit).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_meme2 import (  # noqa: E402
    W, H, PAPER, INK, WHITE, MAGENTA, STAMP_RED, GREY,
    SANS_B, SANS_R, MONO_B, font, tw, fit_font, draw_ghost, dotted_line,
)
from PIL import Image, ImageDraw  # noqa: E402

MX = 56           # side margin
RIGHT = W - MX    # right edge for amounts


def base():
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img)


def header(d, brand, right_top, sub_left, sub_right, brand_size=64):
    d.rectangle([0, 0, W, 168], fill=INK)
    d.text((MX, 34), brand, font=fit_font(d, brand, SANS_B, brand_size,
                                          W - 2 * MX - 320), fill=WHITE)
    rt = fit_font(d, right_top, SANS_B, 40, 330)
    d.text((RIGHT - tw(d, right_top, rt), 30), right_top, font=rt, fill=WHITE)
    d.text((MX, 108), sub_left, font=font(SANS_R, 30), fill=(196, 190, 178))
    sr = font(SANS_R, 30)
    d.text((RIGHT - tw(d, sub_right, sr), 108), sub_right, font=sr,
           fill=(196, 190, 178))


def meta(d, rows, y, size=30, gap=42):
    f = font(MONO_B, size)
    for line in rows:
        d.text((MX, y), line, font=f, fill=INK)
        y += gap
    return y


def rule(d, y):
    d.line([MX, y, RIGHT, y], fill=INK, width=3)
    return y + 26


def rows_block(d, rows, y, size=34, gap=52):
    lf = font(SANS_R, size)
    af = font(SANS_B, size)
    for label, amount in rows:
        d.text((MX, y), label, font=lf, fill=INK)
        aw = tw(d, amount, af)
        d.text((RIGHT - aw, y), amount, font=af, fill=INK)
        dotted_line(d, MX + tw(d, label, lf) + 18, RIGHT - aw - 18,
                    y + size - 4)
        y += gap
    return y


def status_block(d, y, label, total, note):
    d.text((MX, y), label, font=font(SANS_B, 42), fill=INK)
    tf = font(SANS_B, 56)
    d.text((RIGHT - tw(d, total, tf), y - 8), total, font=tf,
           fill=STAMP_RED)
    d.text((MX, y + 54), note, font=font(SANS_R, 27), fill=GREY)
    return y + 96


def closing(d, y, line1, line2=None, size=47):
    d.text((MX, y), line1, font=fit_font(d, line1, SANS_B, size, W - 2 * MX),
           fill=INK)
    y += size + 10
    if line2:
        d.text((MX, y), line2,
               font=fit_font(d, line2, SANS_B, size, W - 2 * MX), fill=INK)
        y += size + 10
    return y


def paid_stamp(img, cx, cy, r=80):
    layer = Image.new("RGBA", (r * 2 + 30, r * 2 + 30), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    c = r + 15
    ld.ellipse([c - r, c - r, c + r, c + r], outline=MAGENTA + (255,),
               width=8)
    ld.ellipse([c - r + 13, c - r + 13, c + r - 13, c + r - 13],
               outline=MAGENTA + (255,), width=3)
    gw = int(r * 0.76)
    draw_ghost(ld, c - gw // 2, c - r + 15, gw, int(gw * 1.05), ow=6)
    f1 = font(SANS_B, 30)
    ld.text((c - tw(ld, "PAID", f1) / 2, c + 6), "PAID", font=f1,
            fill=MAGENTA + (255,))
    f2 = font(SANS_B, 21)
    ld.text((c - tw(ld, "IN FULL", f2) / 2, c + 40), "IN FULL", font=f2,
            fill=MAGENTA + (255,))
    layer = layer.rotate(-11, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)),
              layer)


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


def z5_review():
    img, d = base()
    header(d, "PERFORMANCE REVIEW", "CONFIDENTIAL",
           "DEPT. OF WAITING  •  EST. 2013", "ANNUAL — 13TH YEAR")
    y = meta(d, [
        "EMPLOYEE:  PATIENCE (YOURS)",
        "HIRED:  SEP 17, 2013",
        "ROLE:  WAITING",
        "REVIEWER:  THE RELEASE DATE",
    ], 190)
    y = rule(d, y + 4)
    y = rows_block(d, [
        ("Attendance (every rumor)", "PERFECT"),
        ("Overtime (nights, weekends)", "UNPAID"),
        ("Complaints filed (2 delays)", "NOTED"),
        ("Raises in 13 years", "0 — PAID IN TRAILERS"),
        ("Conduct under delays", "EXEMPLARY"),
        ("New title, from NOV 19", "PLAYER"),
    ], y)
    y = rule(d, y - 8)
    y = status_block(d, y, "DECISION", "PROMOTED",
                     "(BONUS PAID BY THE AGENT — SEE BELOW)")
    y = closing(d, y + 6, "CONGRATULATIONS.",
                "YOU START IN VICE CITY.", size=42)
    paid_stamp(img, 910, 862)
    footer(img, d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "meme", "candidate-z5.png")
    img.save(out)
    print(out)


if __name__ == "__main__":
    z5_review()
