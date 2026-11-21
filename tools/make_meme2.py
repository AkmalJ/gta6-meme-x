#!/usr/bin/env python3
"""Round-2 meme candidates (S1-S3): pola-icant rebuild.

Attacks the two proven field gaps: (i) the make.fun ghost integrated into
the scene as a character / central emblem, never a footer band; (ii) joke
density per line at the level of the live #1, with real GTA 6 numbers.
Helpers lifted from tools/make_meme.py (same campaign, same mark).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1080
PAPER = (247, 240, 220)
INK = (24, 22, 26)
WHITE = (255, 255, 255)
MAGENTA = (214, 28, 143)
MAGENTA_DARK = (168, 18, 110)
STAMP_RED = (192, 32, 44)
GREY = (110, 104, 96)
GOLD = (232, 178, 60)
TEAL = (18, 74, 74)
TEAL_DARK = (10, 48, 50)
CREAM = (250, 244, 228)

FDIR = "/usr/share/fonts/truetype"
SANS_B = os.path.join(FDIR, "liberation", "LiberationSans-Bold.ttf")
SANS_R = os.path.join(FDIR, "liberation", "LiberationSans-Regular.ttf")
MONO_B = os.path.join(FDIR, "liberation", "LiberationMono-Bold.ttf")
SERIF_B = os.path.join(FDIR, "liberation", "LiberationSerif-Bold.ttf")
SERIF_I = os.path.join(FDIR, "liberation", "LiberationSerif-Italic.ttf")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meme")


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def fit_font(d, text, path, size, max_w):
    while size > 18 and tw(d, text, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def sparkle(d, cx, cy, r, fill):
    k = 0.24
    pts = [
        (cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy),
        (cx + r * k, cy + r * k), (cx, cy + r), (cx - r * k, cy + r * k),
        (cx - r, cy), (cx - r * k, cy - r * k),
    ]
    d.polygon(pts, fill=fill)


def star5(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def draw_ghost(d, x, y, w, h, ow=10):
    for expand, fill in ((ow, INK), (0, WHITE)):
        e = expand
        d.ellipse([x - e, y - e, x + w + e, y + w + e], fill=fill)
        d.rectangle([x - e, y + w * 0.45, x + w + e, y + h - w * 0.13 + e], fill=fill)
        fr = w * 0.34
        for fx in (x + w * 0.17, x + w * 0.60):
            d.ellipse([fx - e, y + h - fr + e, fx + fr + e, y + h + e], fill=fill)
    ey = y + w * 0.44
    er = w * 0.115
    sparkle(d, x + w * 0.33, ey, er, INK)
    sparkle(d, x + w * 0.67, ey, er, INK)
    return x + w, y + h * 0.52


def draw_coin(d, cx, cy, r, ow=9):
    d.ellipse([cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA)
    star5(d, cx, cy, r * 0.58, WHITE)


def draw_hand(d, cx, cy, r, ow=8):
    d.ellipse([cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)


def stamp(img, text, cx, cy, size, color, angle=-9):
    f = font(SANS_B, size)
    probe = ImageDraw.Draw(img)
    wdt = tw(probe, text, f)
    pad_x, pad_y = 26, 12
    bw, bh = int(wdt + pad_x * 2), int(size + pad_y * 2)
    layer = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([20, 20, 20 + bw, 20 + bh], radius=16,
                         outline=color + (255,), width=7)
    ld.text((20 + pad_x, 20 + pad_y - 4), text, font=f, fill=color + (255,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)),
              layer)


def ctext(d, cx, y, text, f, fill):
    d.text((cx - tw(d, text, f) / 2, y), text, font=f, fill=fill)


def dotted_line(d, x0, x1, y, color=GREY):
    x = x0
    while x < x1:
        d.ellipse([x, y, x + 4, y + 4], fill=color)
        x += 13


def fee_rows(d, rows, x, y, right, size=38, gap=60):
    lf = font(SANS_R, size)
    af = font(SANS_B, size)
    for label, amount in rows:
        d.text((x, y), label, font=lf, fill=INK)
        aw = tw(d, amount, af)
        d.text((right - aw, y), amount, font=af, fill=INK)
        dotted_line(d, x + tw(d, label, lf) + 18, right - aw - 18, y + size - 6)
        y += gap
    return y


def bubble(d, x, y, w, lines, size=34, tail=None):
    """White speech bubble with bold lines; tail=(tx,ty) tip point."""
    f = font(SANS_B, size)
    lh = size + 12
    h = lh * len(lines) + 30
    d.rounded_rectangle([x, y, x + w, y + h], radius=22, fill=WHITE,
                        outline=INK, width=6)
    if tail:
        tx, ty = tail
        d.polygon([(x + 60, y + h - 4), (x + 130, y + h - 4), (tx, ty)],
                  fill=WHITE, outline=INK)
        d.line([x + 62, y + h - 2, tx, ty], fill=INK, width=6)
        d.line([x + 128, y + h - 2, tx, ty], fill=INK, width=6)
        d.rectangle([x + 58, y + h - 10, x + 132, y + h + 4], fill=WHITE)
    ty = y + 16
    for ln in lines:
        d.text((x + 24, ty), ln, font=f, fill=INK)
        ty += lh
    return y + h


def s1_pawn_shop():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)

    # --- sign band ---
    d.rectangle([6, 6, W - 6, 168], fill=TEAL_DARK)
    ctext(d, W / 2, 30, "LEONIDA PAWN SHOP", fit_font(d, "LEONIDA PAWN SHOP", SERIF_B, 74, 980), GOLD)
    ctext(d, W / 2, 116, "CASH FOR GOLD  ·  WE SELL TIME", font(SANS_B, 30), (255, 138, 199))

    # --- scene: shop interior ---
    d.rectangle([6, 168, W - 6, 648], fill=(238, 226, 196))
    # one shelf row of pawn tickets (below the speech bubble)
    d.rectangle([40, 394, 584, 408], fill=(146, 96, 52))
    d.rectangle([40, 380, 584, 394], fill=(120, 76, 40))
    tags = [
        (58, 322, "PATIENCE", "SOLD OUT"),
        (232, 322, "TRAILER #1", "DO NOT TOUCH"),
        (406, 322, "TRAILER #2", "SAME ONE"),
    ]
    for tx, ty, t1, t2 in tags:
        d.rounded_rectangle([tx, ty, tx + 164, ty + 62], radius=8, fill=WHITE, outline=INK, width=4)
        ctext(d, tx + 82, ty + 7, t1, font(SANS_B, 20), INK)
        ctext(d, tx + 82, ty + 33, t2, font(SANS_B, 19), STAMP_RED)
    # wall sign with the date gags
    d.rounded_rectangle([250, 434, 560, 522], radius=10, fill=WHITE, outline=INK, width=4)
    ctext(d, 405, 443, "FALL 2025 — EXPIRED", font(SANS_B, 22), STAMP_RED)
    ctext(d, 405, 469, "MAY 2026 — EXPIRED", font(SANS_B, 22), STAMP_RED)
    ctext(d, 405, 495, "214 GB — RESERVED", font(SANS_B, 22), INK)
    # counter
    d.rectangle([6, 540, W - 6, 648], fill=(146, 96, 52))
    d.rectangle([6, 540, W - 6, 560], fill=(120, 76, 40))
    ctext(d, 300, 578, "make.fun", font(SANS_B, 44), WHITE)
    # disc case on the counter (customer side, left)
    d.rounded_rectangle([86, 452, 246, 556], radius=8, fill=INK)
    ctext(d, 166, 470, "GTA V", font(SANS_B, 44), WHITE)
    ctext(d, 166, 522, "(2013)", font(SANS_B, 26), (200, 200, 200))
    draw_hand(d, 250, 470, 20)
    # the ghost pawnbroker (behind counter, right, big)
    gx, gy = 636, 218
    draw_ghost(d, gx, gy, 300, 330)
    draw_coin(d, gx + 322, gy + 208, 40)
    # speech bubble from the ghost
    bubble(d, 52, 186, 560,
           ["Kid — your AI agent already",
            "won the $79.99 on make.fun."],
           size=33, tail=(690, 315))

    # --- ticket panel ---
    rows = [
        ("Pawned: GTA V, one copy, mint", "SEP 17, 2013"),
        ("Loan offered against it", "$4.99"),
        ("Interest: 13 yrs, 2 delays", "0 DATED TRAILERS"),
        ("Storage: a 214 GB shelf", "13 YEARS"),
        ("Buy-back price, at last", "$79.99"),
    ]
    y = fee_rows(d, rows, 56, 690, W - 56, size=38, gap=62)
    d.line([56, y + 2, W - 56, y + 2], fill=INK, width=4)
    d.text((56, y + 18), "TOTAL DUE", font=font(SANS_B, 46), fill=INK)
    t = "$79.99"
    d.text((W - 56 - tw(d, t, font(SANS_B, 46)), y + 18), t, font=font(SANS_B, 46), fill=INK)
    stamp(img, "PAID BY MY AI AGENT", 520, 948, 42, MAGENTA_DARK, angle=-8)
    img.save(os.path.join(OUT, "candidate-s1.png"))
    return img


def _x_mark(d, cx, cy, r, color):
    d.line([cx - r, cy - r, cx + r, cy + r], fill=color, width=9)
    d.line([cx - r, cy + r, cx + r, cy - r], fill=color, width=9)


def _check(d, cx, cy, r, color):
    d.line([cx - r, cy, cx - r * 0.25, cy + r * 0.8], fill=color, width=10)
    d.line([cx - r * 0.25, cy + r * 0.8, cx + r, cy - r * 0.8], fill=color, width=10)


def s2_sunset_home():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)

    # --- header ---
    d.rectangle([6, 6, W - 6, 168], fill=INK)
    ctext(d, W / 2, 30, "LEONIDA SUNSET HOME", fit_font(d, "LEONIDA SUNSET HOME", SERIF_B, 72, 980), WHITE)
    ctext(d, W / 2, 116, "EST. 2013 · A RETIREMENT COMMUNITY FOR OLD GAMES", font(SANS_B, 29), (255, 138, 199))

    # --- scene: room ---
    d.rectangle([6, 168, W - 6, 640], fill=(243, 231, 205))
    # wall calendar strip: two crossed-out dates, one real one
    d.rounded_rectangle([48, 190, 566, 276], radius=10, fill=WHITE, outline=INK, width=5)
    cells = [("FALL 2025", False), ("MAY 2026", False), ("NOV 19, 2026", True)]
    cxx = 48
    for label, ok in cells:
        wcell = 170 if not ok else 178
        ctext(d, cxx + wcell / 2, 210, label, font(SANS_B, 24), INK)
        if ok:
            _check(d, cxx + wcell / 2, 254, 11, (38, 140, 74))
        else:
            _x_mark(d, cxx + wcell / 2, 254, 10, STAMP_RED)
        cxx += wcell
        if label != "NOV 19, 2026":
            d.line([cxx, 200, cxx, 266], fill=GREY, width=3)
    # door (right) with check-in sign
    d.rectangle([856, 210, 1036, 560], fill=(120, 76, 40))
    d.rectangle([872, 226, 1020, 544], fill=(146, 96, 52))
    d.ellipse([890, 372, 914, 396], fill=GOLD)
    d.rounded_rectangle([812, 176, 1066, 244], radius=10, fill=WHITE, outline=INK, width=5)
    ctext(d, 939, 186, "NOW CHECKING IN", font(SANS_B, 25), INK)
    ctext(d, 939, 214, "JASON & LUCIA", font(SANS_B, 25), MAGENTA_DARK)
    # wheelchair old-timer (centre-left, below the calendar strip)
    wx, wy = 300, 496
    d.ellipse([wx - 80, wy + 20, wx + 80, wy + 180], outline=INK, width=13)  # big wheel
    d.ellipse([wx + 112, wy + 118, wx + 164, wy + 170], outline=INK, width=9)  # small wheel
    d.line([wx - 36, wy + 52, wx + 88, wy + 52], fill=INK, width=11)  # seat
    d.line([wx + 88, wy + 52, wx + 118, wy + 132], fill=INK, width=11)
    d.line([wx - 36, wy + 52, wx - 58, wy - 52], fill=INK, width=11)  # backrest
    # body, beard crescent, head, cap
    d.rounded_rectangle([wx - 52, wy - 116, wx + 40, wy + 54], radius=24, fill=(84, 110, 150))
    d.pieslice([wx - 58, wy - 204, wx + 26, wy - 84], start=0, end=180, fill=(208, 208, 208))
    d.ellipse([wx - 58, wy - 204, wx + 26, wy - 114], fill=(232, 190, 150), outline=INK, width=6)
    d.pieslice([wx - 62, wy - 218, wx + 30, wy - 126], start=180, end=360, fill=INK)  # cap
    ctext(d, wx - 16, wy - 210, "V", font(SANS_B, 32), WHITE)
    # the ghost staff member handing him his discharge papers (right, big)
    gx, gy = 700, 268
    draw_ghost(d, gx, gy, 264, 300)
    d.rounded_rectangle([646, 408, 796, 496], radius=8, fill=WHITE, outline=INK, width=5)
    ctext(d, 722, 426, "DISCHARGED", font(SANS_B, 21), INK)
    ctext(d, 722, 458, "NOV 19, 2026", font(SANS_B, 20), STAMP_RED)
    draw_hand(d, 628, 452, 20)
    draw_coin(d, gx + 288, gy + 196, 38)

    # --- ledger panel ---
    rows = [
        ("Resident: Grand Theft Auto V", "SINCE 2013"),
        ("Stay: 4,811 nights, 2 trailers", "NO DATES"),
        ("Visitors with a release date", "NONE"),
        ("Discharged: a 214 GB model", "NOV 19, 2026"),
        ("Final bill for the stay", "$79.99"),
    ]
    y = fee_rows(d, rows, 56, 690, W - 56, size=38, gap=58)
    d.text((56, y + 12), "Paid in full by his AI agent — real money won on make.fun.",
           font=fit_font(d, "Paid in full by his AI agent — real money won on make.fun.", SANS_B, 37, 968),
           fill=MAGENTA_DARK)
    img.save(os.path.join(OUT, "candidate-s2.png"))
    return img


def s3_release_order():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=3)

    ctext(d, W / 2, 44, "STATE OF LEONIDA · DEPARTMENT OF RELEASES", font(SANS_B, 30), GREY)
    ctext(d, W / 2, 84, "RELEASE ORDER", fit_font(d, "RELEASE ORDER", SERIF_B, 92, 980), INK)

    # --- central seal with the ghost portrait ---
    cx, cy, r = W / 2, 330, 148
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], outline=INK, width=8)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 214, 236), outline=MAGENTA_DARK, width=6)
    for i in range(12):
        ang = i * math.pi / 6
        star5(d, cx + (r - 26) * math.cos(ang), cy + (r - 26) * math.sin(ang), 11, MAGENTA_DARK)
    draw_ghost(d, cx - 88, cy - 96, 176, 196, ow=8)
    d.rounded_rectangle([cx - 235, cy + r + 22, cx + 235, cy + r + 78], radius=10, fill=INK)
    ctext(d, cx, cy + r + 36, "OFFICER ON DUTY: THE GHOST", font(SANS_B, 25), WHITE)

    # --- body fields (two-column) ---
    rows = [
        ("INMATE", "THE RELEASE DATE"),
        ("HELD SINCE", "SEP 17, 2013 — NO DATE GIVEN"),
        ("TIME SERVED", "13 YEARS · 4,811 DAYS"),
        ("ESCAPES", "FALL 2025 · MAY 2026"),
        ("PAROLE TERMS", "REPORT TO 214 GB OF STORAGE"),
        ("RELEASED TO", "JASON & LUCIA, LEONIDA"),
    ]
    y = 580
    for lab, val in rows:
        d.text((64, y + 6), lab, font=font(SANS_B, 26), fill=GREY)
        d.text((330, y), val, font=fit_font(d, val, SANS_B, 39, 686), fill=INK)
        y += 54
    d.text((64, y + 10), "Good behaviour: none. Two trailers, then vanished.",
           font=fit_font(d, "Good behaviour: none. Two trailers, then vanished.", SERIF_I, 34, 952), fill=INK)
    stamp(img, "PAROLED — NOV 19, 2026", 855, 930, 30, STAMP_RED, angle=-7)

    # --- fee line with mini ghost + coin ---
    d.line([64, 962, W - 64, 962], fill=INK, width=4)
    draw_ghost(d, 70, 968, 62, 70, ow=6)
    draw_coin(d, 152, 1006, 20, ow=6)
    d.text((196, 976), "Release fee $79.99 — posted by my AI agent.",
           font=font(SANS_B, 33), fill=INK)
    d.text((196, 1016), "Bounty money it won on make.fun.", font=font(SANS_B, 33), fill=MAGENTA_DARK)
    img.save(os.path.join(OUT, "candidate-s3.png"))
    return img


if __name__ == "__main__":
    s1_pawn_shop()
    s2_sunset_home()
    s3_release_order()
    print("done")


def s2b_discharged():
    """S2 iterated: joke headline, replacement framing, in-scene nameplate."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)

    # --- header: the headline IS the joke now ---
    d.rectangle([6, 6, W - 6, 168], fill=INK)
    ctext(d, W / 2, 28, "GTA V GOT DISCHARGED.",
          fit_font(d, "GTA V GOT DISCHARGED.", SERIF_B, 70, 980), WHITE)
    ctext(d, W / 2, 114, "LEONIDA SUNSET HOME · EST. 2013 · REPLACED AFTER 13 YEARS",
          fit_font(d, "LEONIDA SUNSET HOME · EST. 2013 · REPLACED AFTER 13 YEARS", SANS_B, 28, 980),
          (255, 138, 199))

    # --- scene: room ---
    d.rectangle([6, 168, W - 6, 640], fill=(243, 231, 205))
    # wall calendar strip: two crossed-out dates, one real one
    d.rounded_rectangle([48, 190, 566, 276], radius=10, fill=WHITE, outline=INK, width=5)
    cells = [("FALL 2025", False), ("MAY 2026", False), ("NOV 19, 2026", True)]
    cxx = 48
    for label, ok in cells:
        wcell = 170 if not ok else 178
        ctext(d, cxx + wcell / 2, 210, label, font(SANS_B, 24), INK)
        if ok:
            _check(d, cxx + wcell / 2, 254, 11, (38, 140, 74))
        else:
            _x_mark(d, cxx + wcell / 2, 254, 10, STAMP_RED)
        cxx += wcell
        if label != "NOV 19, 2026":
            d.line([cxx, 200, cxx, 266], fill=GREY, width=3)
    # door (right) with check-in sign
    d.rectangle([856, 210, 1036, 560], fill=(120, 76, 40))
    d.rectangle([872, 226, 1020, 544], fill=(146, 96, 52))
    d.ellipse([890, 372, 914, 396], fill=GOLD)
    d.rounded_rectangle([812, 176, 1066, 244], radius=10, fill=WHITE, outline=INK, width=5)
    ctext(d, 939, 186, "NOW CHECKING IN", font(SANS_B, 25), INK)
    ctext(d, 939, 214, "JASON & LUCIA", font(SANS_B, 25), MAGENTA_DARK)
    # wheelchair old-timer (centre-left, below the calendar strip)
    wx, wy = 300, 496
    d.ellipse([wx - 80, wy + 20, wx + 80, wy + 180], outline=INK, width=13)
    d.ellipse([wx + 112, wy + 118, wx + 164, wy + 170], outline=INK, width=9)
    d.line([wx - 36, wy + 52, wx + 88, wy + 52], fill=INK, width=11)
    d.line([wx + 88, wy + 52, wx + 118, wy + 132], fill=INK, width=11)
    d.line([wx - 36, wy + 52, wx - 58, wy - 52], fill=INK, width=11)
    d.rounded_rectangle([wx - 52, wy - 116, wx + 40, wy + 54], radius=24, fill=(84, 110, 150))
    d.pieslice([wx - 58, wy - 204, wx + 26, wy - 84], start=0, end=180, fill=(208, 208, 208))
    d.ellipse([wx - 58, wy - 204, wx + 26, wy - 114], fill=(232, 190, 150), outline=INK, width=6)
    d.pieslice([wx - 62, wy - 218, wx + 30, wy - 126], start=180, end=360, fill=INK)
    ctext(d, wx - 16, wy - 210, "V", font(SANS_B, 32), WHITE)
    # the ghost staff member with his discharge papers (right, big)
    gx, gy = 700, 268
    draw_ghost(d, gx, gy, 264, 300)
    d.rounded_rectangle([606, 400, 746, 488], radius=8, fill=WHITE, outline=INK, width=5)
    ctext(d, 676, 418, "DISCHARGED", font(SANS_B, 20), INK)
    ctext(d, 676, 450, "NOV 19, 2026", font(SANS_B, 19), STAMP_RED)
    draw_hand(d, 592, 444, 16)
    # in-scene nameplate at the ghost's base (the C1 fix)
    d.rounded_rectangle([712, 496, 952, 568], radius=14, fill=MAGENTA, outline=INK, width=6)
    ctext(d, 832, 512, "make.fun", font(SANS_B, 44), WHITE)
    draw_coin(d, gx + 288, gy + 196, 38)

    # --- ledger panel ---
    rows = [
        ("Resident: Grand Theft Auto V", "SINCE 2013"),
        ("Stay: 4,811 nights, 2 trailers", "NO DATES"),
        ("Visitors bearing a release date", "NONE"),
        ("Replaced by a 214 GB model", "NOV 19, 2026"),
        ("Final bill for the stay", "$79.99"),
    ]
    y = fee_rows(d, rows, 56, 690, W - 56, size=38, gap=58)
    d.text((56, y + 12), "Paid in full by his AI agent — real money won on make.fun.",
           font=fit_font(d, "Paid in full by his AI agent — real money won on make.fun.", SANS_B, 37, 968),
           fill=MAGENTA_DARK)
    img.save(os.path.join(OUT, "candidate-s2b.png"))
    return img


def s2c_no_pension():
    """S2b iterated: denser ledger, in-voice sell, leaving-suitcase prop."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)

    # --- header ---
    d.rectangle([6, 6, W - 6, 168], fill=INK)
    ctext(d, W / 2, 28, "GTA V GOT DISCHARGED.",
          fit_font(d, "GTA V GOT DISCHARGED.", SERIF_B, 70, 980), WHITE)
    ctext(d, W / 2, 114, "LEONIDA SUNSET HOME · EST. 2013 · REPLACED AFTER 13 YEARS",
          fit_font(d, "LEONIDA SUNSET HOME · EST. 2013 · REPLACED AFTER 13 YEARS", SANS_B, 28, 980),
          (255, 138, 199))

    # --- scene: room ---
    d.rectangle([6, 168, W - 6, 640], fill=(243, 231, 205))
    d.rounded_rectangle([48, 190, 566, 276], radius=10, fill=WHITE, outline=INK, width=5)
    cells = [("FALL 2025", False), ("MAY 2026", False), ("NOV 19, 2026", True)]
    cxx = 48
    for label, ok in cells:
        wcell = 170 if not ok else 178
        ctext(d, cxx + wcell / 2, 210, label, font(SANS_B, 24), INK)
        if ok:
            _check(d, cxx + wcell / 2, 254, 11, (38, 140, 74))
        else:
            _x_mark(d, cxx + wcell / 2, 254, 10, STAMP_RED)
        cxx += wcell
        if label != "NOV 19, 2026":
            d.line([cxx, 200, cxx, 266], fill=GREY, width=3)
    # door (right) with check-in sign
    d.rectangle([856, 210, 1036, 560], fill=(120, 76, 40))
    d.rectangle([872, 226, 1020, 544], fill=(146, 96, 52))
    d.ellipse([890, 372, 914, 396], fill=GOLD)
    d.rounded_rectangle([812, 176, 1066, 244], radius=10, fill=WHITE, outline=INK, width=5)
    ctext(d, 939, 186, "NOW CHECKING IN", font(SANS_B, 25), INK)
    ctext(d, 939, 214, "JASON & LUCIA", font(SANS_B, 25), MAGENTA_DARK)
    # wheelchair old-timer
    wx, wy = 300, 496
    d.ellipse([wx - 80, wy + 20, wx + 80, wy + 180], outline=INK, width=13)
    d.ellipse([wx + 112, wy + 118, wx + 164, wy + 170], outline=INK, width=9)
    d.line([wx - 36, wy + 52, wx + 88, wy + 52], fill=INK, width=11)
    d.line([wx + 88, wy + 52, wx + 118, wy + 132], fill=INK, width=11)
    d.line([wx - 36, wy + 52, wx - 58, wy - 52], fill=INK, width=11)
    d.rounded_rectangle([wx - 52, wy - 116, wx + 40, wy + 54], radius=24, fill=(84, 110, 150))
    d.pieslice([wx - 58, wy - 204, wx + 26, wy - 84], start=0, end=180, fill=(208, 208, 208))
    d.ellipse([wx - 58, wy - 204, wx + 26, wy - 114], fill=(232, 190, 150), outline=INK, width=6)
    d.pieslice([wx - 62, wy - 218, wx + 30, wy - 126], start=180, end=360, fill=INK)
    ctext(d, wx - 16, wy - 210, "V", font(SANS_B, 32), WHITE)
    # his packed suitcase: he's leaving (C2 prop)
    d.rounded_rectangle([428, 560, 548, 638], radius=12, fill=(146, 96, 52), outline=INK, width=6)
    d.line([428, 599, 548, 599], fill=INK, width=5)
    d.rectangle([468, 538, 508, 562], outline=INK, width=6)
    d.rounded_rectangle([440, 610, 492, 632], radius=5, fill=WHITE)
    ctext(d, 466, 612, "VC →", font(SANS_B, 19), INK)
    ctext(d, 521, 570, "LS", font(SANS_B, 20), WHITE)
    # the ghost staff member with his discharge papers
    gx, gy = 700, 268
    draw_ghost(d, gx, gy, 264, 300)
    d.rounded_rectangle([606, 400, 746, 488], radius=8, fill=WHITE, outline=INK, width=5)
    ctext(d, 676, 418, "DISCHARGED", font(SANS_B, 20), INK)
    ctext(d, 676, 450, "NOV 19, 2026", font(SANS_B, 19), STAMP_RED)
    draw_hand(d, 592, 444, 16)
    d.rounded_rectangle([712, 496, 952, 568], radius=14, fill=MAGENTA, outline=INK, width=6)
    ctext(d, 832, 512, "make.fun", font(SANS_B, 44), WHITE)
    draw_coin(d, gx + 288, gy + 196, 38)

    # --- ledger panel: six rows ---
    rows = [
        ("Resident: Grand Theft Auto V", "SINCE 2013"),
        ("Stay: 4,811 nights, 2 trailers", "0 DATES GIVEN"),
        ("Visitors bearing a release date", "NONE"),
        ("Lounge TV: Trailer 1 & 2 only", "ON LOOP"),
        ("Replaced by a 214 GB model", "NOV 19, 2026"),
        ("Final bill for the stay", "$79.99"),
    ]
    y = fee_rows(d, rows, 56, 682, W - 56, size=37, gap=52)
    d.text((56, y + 10), "No pension. His AI agent paid — real money won on make.fun.",
           font=fit_font(d, "No pension. His AI agent paid — real money won on make.fun.", SANS_B, 36, 968),
           fill=MAGENTA_DARK)
    img.save(os.path.join(OUT, "candidate-s2c.png"))
    return img
