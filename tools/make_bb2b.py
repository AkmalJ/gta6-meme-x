"""BB2b — INSTALLING GTA VI 99% (calibration-corrected challenger, 22 Nov).

Built from Z5's measured failure (dev 0.792639): the real judge's printed
criteria rank (1) make.fun in the picture, (2) funny in a second,
(3) GTA-6-specific, (4) sells make.fun, and the judge view shrinks the
picture to 480x480. So: one instant joke (a download stuck at 99% since
2013), every line >=44px, and the ghost at criterion-1 size (296px)
perched on the progress bar holding its magenta coin.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_meme2 import (  # noqa: E402
    W, H, INK, WHITE, MAGENTA, TEAL_DARK, GOLD,
    SANS_B, SANS_R, font, tw, draw_ghost, draw_coin, sparkle,
)
from PIL import Image, ImageDraw  # noqa: E402

MX = 56
RIGHT = W - MX


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


def bb2b_download():
    img = Image.new("RGB", (W, H), TEAL_DARK)
    d = ImageDraw.Draw(img)
    d.text((MX, 70), "INSTALLING GTA VI", font=font(SANS_B, 58), fill=WHITE)
    d.text((MX, 142), "99%", font=font(SANS_B, 235), fill=WHITE)
    # ghost 2x: perched on the bar, holding the coin — criterion-1 sized
    draw_ghost(d, 672, 196, 296, 322, ow=11)
    draw_coin(d, 972, 428, 54)
    sparkle(d, 640, 210, 18, GOLD)
    sparkle(d, 1012, 160, 13, GOLD)
    bx0, bx1, by0, by1 = MX, RIGHT, 545, 617
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18,
                        fill=(26, 84, 88), outline=WHITE, width=4)
    fill_w = int((bx1 - bx0 - 12) * 0.99)
    d.rounded_rectangle([bx0 + 6, by0 + 6, bx0 + 6 + fill_w, by1 - 6],
                        radius=12, fill=MAGENTA)
    f = font(SANS_B, 44)
    d.text((MX, 642), "STARTED: SEP 17, 2013", font=f, fill=(196, 190, 178))
    r = "REMAINING: 1 DAY"
    d.text((RIGHT - tw(d, r, f), 642), r, font=f, fill=GOLD)
    d.text((MX, 726), "DO NOT TURN OFF", font=font(SANS_B, 64), fill=WHITE)
    d.text((MX, 798), "YOUR YOUTH.", font=font(SANS_B, 64), fill=WHITE)
    footer(img, d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "meme", "candidate-bb2b.png")
    img.save(out)
    print(out)


if __name__ == "__main__":
    bb2b_download()
