#!/usr/bin/env python3
"""Render the gta6-meme-x-01 candidate memes with PIL.

Each candidate is a Leonida official document drawn flat on cream paper:
black header band, itemised joke lines, a stamp, and a magenta bottom band
where the make.fun ghost appears as a character next to the "paid by my AI
agent" line. The first family is a boarding pass, a pay stub and a hospital
discharge summary; the challenger family is a wanted poster, a university
diploma and a parking ticket.

Run:  python3 tools/make_meme.py
Out:  meme/candidate-a.png, meme/candidate-b.png, meme/candidate-c.png,
      meme/candidate-a2.png, meme/candidate-a3.png (revision rounds of A:
      a2 fixes the band ghost's prop and the DELAYED stamp placement;
      a3 is a2 plus an alligator passenger waiting in the band),
      meme/candidate-d.png, meme/candidate-e.png, meme/candidate-f.png
      (fresh challengers built to duel the standing champion),
      meme/candidate-g.png, meme/candidate-h.png, meme/candidate-i.png
      (round 3: an eviction notice, a marriage certificate and a lottery
      ticket, built to duel the wanted-poster champion)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "meme")

W = H = 1080
PAPER = (247, 240, 220)
INK = (24, 22, 26)
WHITE = (255, 255, 255)
MAGENTA = (214, 28, 143)
MAGENTA_DARK = (168, 18, 110)
STAMP_RED = (192, 32, 44)
GREY = (110, 104, 96)
CLIP_BROWN = (146, 96, 52)

FDIR = "/usr/share/fonts/truetype"
SANS_B = os.path.join(FDIR, "liberation", "LiberationSans-Bold.ttf")
SANS_R = os.path.join(FDIR, "liberation", "LiberationSans-Regular.ttf")
MONO_B = os.path.join(FDIR, "liberation", "LiberationMono-Bold.ttf")
MONO_R = os.path.join(FDIR, "liberation", "LiberationMono-Regular.ttf")
SERIF_B = os.path.join(FDIR, "liberation", "LiberationSerif-Bold.ttf")
SERIF_I = os.path.join(FDIR, "liberation", "LiberationSerif-Italic.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def fit_font(d, text, path, size, max_w):
    """Shrink a bold line until it fits max_w."""
    while size > 18 and tw(d, text, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def sparkle(d, cx, cy, r, fill):
    """Four-pointed sparkle (the ghost's eye shape)."""
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
    """The make.fun ghost: white blob, black outline, sparkle eyes.

    (x, y) is the top-left of the bounding box, w wide, h tall.
    Returns the centre of the coin position for prop drawing.
    """
    for expand, fill in ((ow, INK), (0, WHITE)):
        e = expand
        # dome (circle whose lower half is covered by the body rect)
        d.ellipse([x - e, y - e, x + w + e, y + w + e], fill=fill)
        # body
        d.rectangle([x - e, y + w * 0.45, x + w + e, y + h - w * 0.13 + e], fill=fill)
        # two feet bumps along the bottom
        fr = w * 0.34
        for fx in (x + w * 0.17, x + w * 0.60):
            d.ellipse([fx - e, y + h - fr + e, fx + fr + e, y + h + e], fill=fill)
    # sparkle eyes
    ey = y + w * 0.44
    er = w * 0.115
    sparkle(d, x + w * 0.33, ey, er, INK)
    sparkle(d, x + w * 0.67, ey, er, INK)
    return x + w, y + h * 0.52


def draw_coin(d, cx, cy, r, ow=9):
    """Magenta coin with a white star, as the ghost holds in the mark."""
    d.ellipse([cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA)
    star5(d, cx, cy, r * 0.58, WHITE)


def draw_hand(d, cx, cy, r, ow=8):
    d.ellipse([cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)


def stamp(img, text, cx, cy, size, color, angle=-9):
    """A rotated rubber-stamp imprint: rounded box + bold text."""
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
    """Draw text centred on cx at height y."""
    d.text((cx - tw(d, text, f) / 2, y), text, font=f, fill=fill)


def dotted_line(d, x0, x1, y, color=GREY):
    x = x0
    while x < x1:
        d.ellipse([x, y, x + 4, y + 4], fill=color)
        x += 13


def fee_rows(d, rows, x, y, right, size=40, gap=62, label_f=None, amt_f=None):
    """Itemised lines: label left, dotted leader, amount right."""
    lf = label_f or font(SANS_R, size)
    af = amt_f or font(SANS_B, size)
    for label, amount in rows:
        d.text((x, y), label, font=lf, fill=INK)
        aw = tw(d, amount, af)
        d.text((right - aw, y), amount, font=af, fill=INK)
        dotted_line(d, x + tw(d, label, lf) + 18, right - aw - 18, y + size - 8)
        y += gap
    return y


def field(d, x, y, label, value, lw=250, size=38, mono=False):
    lf = font(SANS_B, 26)
    vf = font(MONO_B if mono else SANS_B, size)
    d.text((x, y), label, font=lf, fill=GREY)
    d.text((x, y + 34), value, font=vf, fill=INK)
    return y + 34 + size + 26


def base_canvas():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)
    return img, d


def header(d, title, sub, right_top=None, right_big=None):
    d.rectangle([6, 6, W - 6, 172], fill=INK)
    tf = fit_font(d, title, SANS_B, 68, 800 if right_big else 1000)
    d.text((44, 34), title, font=tf, fill=WHITE)
    d.text((46, 116), sub, font=font(SANS_B, 30), fill=(255, 138, 199))
    if right_big:
        rf = font(SANS_B, 56)
        rw = tw(d, right_big, rf)
        d.text((W - 44 - rw, 62), right_big, font=rf, fill=WHITE)
        if right_top:
            sf = font(SANS_B, 24)
            sw = tw(d, right_top, sf)
            d.text((W - 44 - sw, 30), right_top, font=sf, fill=(200, 200, 200))


def band(img, headline, subline):
    """Magenta bottom band; returns the draw + ghost box for props."""
    d = ImageDraw.Draw(img)
    d.rectangle([6, 806, W - 6, H - 6], fill=MAGENTA)
    return d


def band_text(d, headline, subline, x=392):
    hf = fit_font(d, headline, SANS_B, 60, W - x - 36)
    d.text((x, 838), headline, font=hf, fill=WHITE)
    d.text((x, 916), subline, font=font(SANS_B, 35), fill=WHITE)
    # white pill with the make.fun wordmark
    pf = font(SANS_B, 54)
    pw = tw(d, "make.fun", pf)
    d.rounded_rectangle([x, 972, x + pw + 56, 1052], radius=40, fill=WHITE)
    d.text((x + 28, 984), "make.fun", font=pf, fill=INK)


# ---------------------------------------------------------------- candidate A
def candidate_a():
    img, d = base_canvas()
    header(d, "LEONIDA AIR", "BOARDING PASS - ONE WAY", right_top="FLIGHT", right_big="V > VI")

    # route
    rf = fit_font(d, "LOS SANTOS > VICE CITY", SANS_B, 66, 990)
    d.text((44, 196), "LOS SANTOS > VICE CITY", font=rf, fill=INK)

    lf = font(SANS_B, 26)
    vf = font(SANS_B, 38)
    d.text((44, 282), "PASSENGER", font=lf, fill=GREY)
    d.text((44, 316), "EVERY GTA FAN", font=vf, fill=INK)
    d.text((44, 388), "DEPARTED", font=lf, fill=GREY)
    d.text((44, 422), "SEP 17, 2013", font=vf, fill=INK)
    d.text((560, 388), "ARRIVES (FINALLY)", font=lf, fill=GREY)
    d.text((560, 422), "NOV 19, 2026", font=vf, fill=INK)

    stamp(img, "DELAYED 13 YEARS", 745, 325, 58, STAMP_RED, angle=-10)
    d = ImageDraw.Draw(img)

    rows = [
        ("Schedule changes: Fall 2025, then May 2026", "$26"),
        ("Checked baggage: one 214 GB download", "$214"),
        ("Window seat: 13 years of trailer-watching", "$0"),
        ("Unlisted passengers: Jason & Lucia", "$137"),
    ]
    y = fee_rows(d, rows, 44, 496, W - 44, gap=56)
    d.line([44, y + 10, W - 44, y + 10], fill=INK, width=3)
    tf = font(SANS_B, 44)
    d.text((44, y + 24), "TOTAL DUE", font=tf, fill=INK)
    tot = "$377"
    d.text((W - 44 - tw(d, tot, tf), y + 24), tot, font=tf, fill=INK)

    stamp(img, "NOW BOARDING", 700, 762, 34, MAGENTA_DARK, angle=-6)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # gate agent pressing its rubber stamp down beside it
    sx = edge + 30
    d.rounded_rectangle([sx - 47, gy + 198, sx + 47, gy + 218], radius=8, fill=INK)
    d.rectangle([sx - 10, gy + 166, sx + 10, gy + 200], fill=INK)
    d.ellipse([sx - 23, gy + 136, sx + 23, gy + 170], fill=INK)
    draw_hand(d, sx + 18, gy + 150, 25)
    band_text(d, "PAID BY MY AI AGENT", "with bounty money it earned on")
    return img


# ------------------------------------------------------- candidate A, revised
def draw_gator_on_suitcase(d):
    """A Leonida alligator passenger, flat ink silhouette with white
    sunglasses, sitting on a brown suitcase in the band's bottom-right
    corner. Drawn last so nothing covers it."""
    # suitcase: brown body, ink outline, two straps, a magenta luggage tag
    d.rounded_rectangle([882, 1006, 1034, 1066], radius=10, fill=CLIP_BROWN,
                        outline=INK, width=5)
    for sx in (918, 984):
        d.rectangle([sx, 1008, sx + 8, 1064], fill=INK)
    d.rounded_rectangle([1028, 1018, 1050, 1042], radius=5, fill=MAGENTA,
                        outline=INK, width=4)
    # handle ends peeking out from behind the gator
    d.rounded_rectangle([928, 990, 992, 1012], radius=8, outline=INK, width=6)
    # tail: a long triangle tapering to a point off the body's rear
    d.polygon([(916, 960), (868, 980), (916, 992)], fill=INK)
    for rx in (892, 902):
        d.polygon([(rx, 968), (rx + 5, 960), (rx + 10, 970)], fill=INK)
    # body
    d.rounded_rectangle([908, 954, 1022, 1000], radius=22, fill=INK)
    # back ridges
    for rx in (936, 962, 988):
        d.polygon([(rx, 956), (rx + 9, 944), (rx + 18, 956)], fill=INK)
    # head and snout, facing right
    d.polygon([(1006, 960), (1052, 964), (1062, 980), (1056, 992),
               (1008, 994)], fill=INK)
    d.line([1018, 984, 1056, 986], fill=MAGENTA, width=3)
    # white sunglasses on the head
    d.rounded_rectangle([1012, 964, 1030, 978], radius=4, fill=WHITE)
    d.rounded_rectangle([1034, 964, 1052, 978], radius=4, fill=WHITE)
    d.rectangle([1028, 968, 1036, 972], fill=WHITE)
    # front legs dangling over the suitcase
    for lx in (926, 978):
        d.rectangle([lx, 994, lx + 13, 1026], fill=INK)
        d.ellipse([lx - 3, 1020, lx + 17, 1032], fill=INK)


def _boarding_pass_v2(gator=False):
    """Candidate A revised: same pass, but the band ghost holds the magenta
    coin (as in candidate B) instead of the dark stamp prop, and the
    DELAYED 13 YEARS stamp sits lower and flatter so it clears the route
    line entirely."""
    img, d = base_canvas()
    header(d, "LEONIDA AIR", "BOARDING PASS - ONE WAY", right_top="FLIGHT", right_big="V > VI")

    # route
    rf = fit_font(d, "LOS SANTOS > VICE CITY", SANS_B, 66, 990)
    d.text((44, 196), "LOS SANTOS > VICE CITY", font=rf, fill=INK)

    lf = font(SANS_B, 26)
    vf = font(SANS_B, 38)
    d.text((44, 282), "PASSENGER", font=lf, fill=GREY)
    d.text((44, 316), "EVERY GTA FAN", font=vf, fill=INK)
    d.text((44, 388), "DEPARTED", font=lf, fill=GREY)
    d.text((44, 422), "SEP 17, 2013", font=vf, fill=INK)
    d.text((560, 388), "ARRIVES (FINALLY)", font=lf, fill=GREY)
    d.text((560, 422), "NOV 19, 2026", font=vf, fill=INK)

    stamp(img, "DELAYED 13 YEARS", 720, 330, 52, STAMP_RED, angle=-6)
    d = ImageDraw.Draw(img)

    rows = [
        ("Schedule changes: Fall 2025, then May 2026", "$26"),
        ("Checked baggage: one 214 GB download", "$214"),
        ("Window seat: 13 years of trailer-watching", "$0"),
        ("Unlisted passengers: Jason & Lucia", "$137"),
    ]
    y = fee_rows(d, rows, 44, 496, W - 44, gap=56)
    d.line([44, y + 10, W - 44, y + 10], fill=INK, width=3)
    tf = font(SANS_B, 44)
    d.text((44, y + 24), "TOTAL DUE", font=tf, fill=INK)
    tot = "$377"
    d.text((W - 44 - tw(d, tot, tf), y + 24), tot, font=tf, fill=INK)

    stamp(img, "NOW BOARDING", 700, 762, 34, MAGENTA_DARK, angle=-6)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # the ghost holds its magenta coin out, exactly as in candidate B
    draw_coin(d, edge + 40, gy + 118, 54)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "PAID BY MY AI AGENT", "with bounty money it earned on")
    if gator:
        draw_gator_on_suitcase(d)
    return img


def candidate_a2():
    return _boarding_pass_v2(gator=False)


def candidate_a3():
    return _boarding_pass_v2(gator=True)


# ---------------------------------------------------------------- candidate B
def candidate_b():
    img, d = base_canvas()
    header(d, "WAITING DEPT.", "EARNINGS STATEMENT - PAY STUB")

    rows = [
        ("EMPLOYEE", "GTA FAN"),
        ("JOB TITLE", "WAITING FOR GTA VI"),
        ("PAY PERIOD", "SEP 2013 - NOV 2026"),
        ("HOURS WORKED", "114,000"),
        ("HOURLY RATE", "$0.00"),
        ("GROSS PAY", "$0.00"),
        ("DEDUCTIONS", "13 YEARS OF YOUTH"),
    ]
    lf = font(MONO_B, 37)
    y = 214
    for label, value in rows:
        d.text((44, y), label, font=lf, fill=INK)
        vw = tw(d, value, lf)
        d.text((W - 44 - vw, y), value, font=lf, fill=INK)
        dotted_line(d, 44 + tw(d, label, lf) + 16, W - 44 - vw - 16, y + 30)
        y += 58
    d.line([44, y + 4, W - 44, y + 4], fill=INK, width=3)
    nf = font(MONO_B, 52)
    d.text((44, y + 20), "NET PAY", font=nf, fill=INK)
    net = "$0.00"
    d.text((W - 44 - tw(d, net, nf), y + 20), net, font=nf, fill=INK)

    tf = fit_font(d, "MY AI AGENT - SAME 13 YEARS, ON MAKE.FUN:", SANS_B, 41, 990)
    d.text((44, 700), "MY AI AGENT - SAME 13 YEARS, ON MAKE.FUN:", font=tf, fill=INK)
    d.text((44, 748), "PAID IN REAL MONEY", font=font(SANS_B, 50), fill=MAGENTA_DARK)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # payroll clerk handing the coin over to the right
    draw_coin(d, edge + 40, gy + 118, 54)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "MY AI AGENT GOT PAID", "real money from bounties on")
    return img


# ---------------------------------------------------------------- candidate C
def candidate_c():
    img, d = base_canvas()
    header(d, "LEONIDA GENERAL HOSPITAL", "DISCHARGE SUMMARY")

    lf = font(SANS_B, 26)
    vf = font(SANS_B, 38)
    v36 = font(SANS_B, 36)
    d.text((44, 196), "PATIENT", font=lf, fill=GREY)
    d.text((44, 230), "EVERY GTA FAN", font=vf, fill=INK)
    d.text((560, 196), "ADMITTED", font=lf, fill=GREY)
    d.text((560, 230), "SEP 17, 2013", font=vf, fill=INK)
    d.text((44, 300), "DIAGNOSIS", font=lf, fill=GREY)
    d.text((44, 334), "CHRONIC WAITING (GTA DEFICIENCY)", font=v36, fill=INK)
    d.text((44, 398), "TREATMENT", font=lf, fill=GREY)
    d.text((44, 432), "ONE LAUNCH - 214 GB", font=v36, fill=INK)
    d.text((560, 398), "DISCHARGED", font=lf, fill=GREY)
    d.text((560, 432), "NOV 19, 2026", font=vf, fill=INK)

    stamp(img, "CURED", 884, 368, 66, MAGENTA_DARK, angle=-11)
    d = ImageDraw.Draw(img)

    rows = [
        ("Waiting-room chair (13 years)", "$313"),
        ("Trailer therapy, two sessions", "$26"),
        ("Launch-day medicine (one copy)", "$79.99"),
    ]
    y = fee_rows(d, rows, 44, 556, W - 44, size=38, gap=52)
    d.line([44, y + 6, W - 44, y + 6], fill=INK, width=3)
    tf = font(SANS_B, 42)
    d.text((44, y + 20), "TOTAL DUE", font=tf, fill=INK)
    tot = "$418.99"
    d.text((W - 44 - tw(d, tot, tf), y + 20), tot, font=tf, fill=INK)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # doctor's clipboard in hand
    cb = Image.new("RGBA", (124, 162), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cb)
    cd.rounded_rectangle([4, 4, 120, 158], radius=10, fill=CLIP_BROWN + (255,))
    cd.rectangle([17, 22, 107, 146], fill=WHITE + (255,))
    cd.rounded_rectangle([43, 0, 81, 22], radius=7, fill=INK + (255,))
    for i in range(3):
        cd.line([29, 52 + i * 28, 95, 52 + i * 28], fill=GREY + (255,), width=6)
    cb = cb.rotate(10, expand=True, resample=Image.BICUBIC)
    img.paste(cb, (int(edge - 8), int(gy + 62)), cb)
    d = ImageDraw.Draw(img)
    draw_hand(d, edge + 2, gy + 84, 26)
    band_text(d, "BILL PAID BY MY AI AGENT", "with its bounty winnings on")
    return img


# ---------------------------------------------------------------- candidate D
def candidate_d():
    """Wanted poster: the release date as a fugitive, finally apprehended."""
    img, d = base_canvas()
    header(d, "LEONIDA SHERIFF'S OFFICE", "WANTED POSTER - VICE CITY DIVISION",
           right_top="CASE NO.", right_big="VI-13")

    ctext(d, W // 2, 190, "WANTED", font(SANS_B, 112), INK)
    ctext(d, W // 2, 318, "THE RELEASE DATE", font(SANS_B, 54), INK)
    ctext(d, W // 2, 386, "DEAD OR DELAYED", font(SANS_B, 32), MAGENTA_DARK)
    d.line([210, 442, W - 210, 442], fill=INK, width=3)

    lf = font(SANS_B, 26)
    d.text((44, 460), "CHARGES", font=lf, fill=GREY)
    rows = [
        ("Stood up 40 million fans", "COUNT 1"),
        ("Escaped custody: Fall 2025", "COUNT 2"),
        ("Escaped again: May 2026", "COUNT 3"),
        ("Accomplice: total silence", "COUNT 4"),
    ]
    fee_rows(d, rows, 44, 498, W - 44, size=37, gap=48)

    vf = font(SANS_B, 36)
    d.text((44, 700), "LAST SEEN:", font=vf, fill=GREY)
    lw = tw(d, "LAST SEEN:", vf)
    d.text((44 + lw + 18, 700), "IN TWO TRAILERS", font=vf, fill=INK)
    d.text((44, 752), "STATUS:", font=vf, fill=GREY)
    sw = tw(d, "STATUS:", vf)
    d.text((44 + sw + 18, 752), "APPREHENDED - NOV 19, 2026",
           font=vf, fill=STAMP_RED)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # sheriff's star badge on the ghost's left chest, clear of eyes and feet
    bcx, bcy = gx + 54, gy + 142
    d.ellipse([bcx - 26, bcy - 26, bcx + 26, bcy + 26], fill=INK)
    d.ellipse([bcx - 20, bcy - 20, bcx + 20, bcy + 20], fill=MAGENTA)
    star5(d, bcx, bcy, 12, WHITE)
    # the reward coin, held out as always
    draw_coin(d, edge + 40, gy + 118, 54)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "REWARD PAID BY MY AI AGENT", "from bounties it won on")
    return img


# ---------------------------------------------------------------- candidate E
def candidate_e():
    """University diploma: a doctorate in waiting, conferred at launch."""
    img, d = base_canvas()
    header(d, "UNIVERSITY OF LEONIDA", "DIPLOMA - OFFICE OF THE REGISTRAR")

    ctext(d, W // 2, 200, "This certifies that", font(SERIF_I, 36), GREY)
    ctext(d, W // 2, 250, "EVERY GTA FAN", font(SERIF_B, 64), INK)
    ctext(d, W // 2, 336, "has satisfied every requirement for the degree of",
          font(SANS_R, 28), INK)
    ctext(d, W // 2, 376, "DOCTORATE IN WAITING", font(SERIF_B, 54), INK)
    ctext(d, W // 2, 450, "SUMMA CUM LAUDE - HE WAITED THE LONGEST",
          font(SANS_B, 30), MAGENTA_DARK)

    lf = font(SANS_B, 26)
    vf = font(SANS_B, 32)
    d.text((44, 502), "ENROLLED", font=lf, fill=GREY)
    d.text((44, 536), "SEP 17, 2013", font=vf, fill=INK)
    d.text((400, 502), "GRADUATED", font=lf, fill=GREY)
    d.text((400, 536), "NOV 19, 2026", font=vf, fill=INK)
    # the university seal is the magenta coin itself, ribbons and all
    draw_coin(d, 948, 532, 44)
    d.polygon([(922, 566), (946, 570), (934, 616), (912, 574)], fill=MAGENTA_DARK)
    d.polygon([(950, 570), (974, 566), (984, 574), (962, 616)], fill=MAGENTA_DARK)

    d.text((44, 592), "COURSE OF STUDY - FINAL GRADES", font=lf, fill=GREY)
    rows = [
        ("Trailer Analysis I & II", "A+"),
        ("Delay Endurance (13 years)", "A+"),
        ("Download Management, 214 GB", "A"),
        ("Advanced Hopium Studies", "A+"),
    ]
    fee_rows(d, rows, 44, 628, W - 44, size=33, gap=42)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # mortarboard: a wide flat board on the dome, a skull band under its
    # centre, and a tassel with a magenta bobble at the right corner
    d.polygon([(48, 836), (268, 836), (312, 808), (92, 808)], fill=INK)
    d.rounded_rectangle([102, 830, 214, 858], radius=8, fill=INK)
    d.line([312, 808, 312, 850], fill=INK, width=7)
    d.ellipse([302, 850, 322, 870], fill=MAGENTA)
    # the graduate's diploma scroll: one long tube held across the body's
    # front, magenta ribbon around its middle, hand gripping its left half
    sc = Image.new("RGBA", (280, 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sc)
    sd.rounded_rectangle([15, 30, 245, 90], radius=28, fill=WHITE + (255,),
                         outline=INK + (255,), width=6)
    sd.ellipse([226, 34, 252, 86], fill=PAPER + (255,), outline=INK + (255,),
               width=5)
    sd.rectangle([168, 30, 190, 90], fill=MAGENTA + (255,))
    sc = sc.rotate(-8, expand=True, resample=Image.BICUBIC)
    img.paste(sc, (int(215 - sc.width / 2), int(gy + 172 - sc.height / 2)), sc)
    d = ImageDraw.Draw(img)
    draw_hand(d, 150, gy + 148, 25)
    band_text(d, "TUITION PAID BY MY AI AGENT", "with its bounty winnings on")
    return img


# ---------------------------------------------------------------- candidate F
def candidate_f():
    """Parking ticket: thirteen years in a loading zone, fined at last."""
    img, d = base_canvas()
    header(d, "LEONIDA POLICE DEPT.", "PARKING VIOLATION - NOTICE OF FINE",
           right_top="TICKET NO.", right_big="13-YRS")

    lf = font(SANS_B, 26)
    v34 = font(SANS_B, 34)
    d.text((44, 192), "VEHICLE", font=lf, fill=GREY)
    d.text((44, 226), "ONE FAN, CAMPED OUTSIDE THE GAME STORE", font=v34, fill=INK)
    d.text((44, 288), "LOCATION", font=lf, fill=GREY)
    d.text((44, 322), "LOADING ZONE, VICE CITY", font=v34, fill=INK)
    d.text((560, 288), "PARKED SINCE", font=lf, fill=GREY)
    d.text((560, 322), "SEP 17, 2013", font=v34, fill=INK)
    d.text((44, 384), "STATUS", font=lf, fill=GREY)
    d.text((44, 418), "13 YEARS OVERDUE - DO NOT IGNORE",
           font=v34, fill=STAMP_RED)

    d.text((44, 480), "VIOLATIONS", font=lf, fill=GREY)
    rows = [
        ("13 years in a loading zone", "$44.99"),
        ("False alarm: Fall 2025", "$15.00"),
        ("False alarm: May 2026", "$20.00"),
        ("Engine off, hopes on", "$0.00"),
    ]
    y = fee_rows(d, rows, 44, 516, W - 44, size=34, gap=44)
    d.line([44, y + 8, W - 44, y + 8], fill=INK, width=3)
    tf = font(SANS_B, 42)
    d.text((44, y + 22), "TOTAL FINE DUE", font=tf, fill=INK)
    tot = "$79.99"
    d.text((W - 44 - tw(d, tot, tf), y + 22), tot, font=tf, fill=INK)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # traffic cop's cap: a band across the dome and a brim, badge star on it
    d.rounded_rectangle([gx + 28, gy + 22, gx + 172, gy + 52], radius=12,
                        fill=INK)
    d.ellipse([gx + 10, gy + 42, gx + 190, gy + 72], fill=INK)
    star5(d, gx + 100, gy + 37, 9, WHITE)
    draw_coin(d, edge + 40, gy + 118, 54)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "FINE PAID BY MY AI AGENT", "with bounty money it earned on")
    return img


def draw_key(d, cx, cy):
    """A front-door key held out flat: cream bow with a magenta hole,
    ink shaft running right with two teeth hanging near the tip."""
    d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=INK)
    d.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=PAPER)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=MAGENTA)
    d.line([cx + 26, cy, cx + 76, cy], fill=INK, width=13)
    d.rectangle([cx + 46, cy, cx + 56, cy + 16], fill=INK)
    d.rectangle([cx + 62, cy, cx + 72, cy + 22], fill=INK)


def draw_suitcase(d, x, y, w=96, h=56):
    """A brown moving suitcase: straps, ink outline, handle on top."""
    d.rounded_rectangle([x + w * 0.35, y - 15, x + w * 0.65, y + 2],
                        radius=7, outline=INK, width=6)
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CLIP_BROWN,
                        outline=INK, width=5)
    for sx in (x + w * 0.28, x + w * 0.68):
        d.rectangle([sx, y + 3, sx + 8, y + h - 3], fill=INK)


def draw_ball(d, cx, cy, r, text, fill, tcol, fsize):
    """A lottery ball: ink rim, coloured face, bold number centred."""
    d.ellipse([cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    f = fit_font(d, text, SANS_B, fsize, 2 * r - 14)
    d.text((cx - tw(d, text, f) / 2, cy - f.size * 0.58), text, font=f,
           fill=tcol)


# ---------------------------------------------------------------- candidate G
def candidate_g():
    """Eviction notice: GTA V is ordered off the SSD; the ghost moves in."""
    img, d = base_canvas()
    header(d, "LEONIDA COUNTY COURT", "NOTICE TO VACATE - EVICTION ORDER")

    ctext(d, W // 2, 192, "NOTICE TO VACATE", font(SANS_B, 58), INK)
    ctext(d, W // 2, 264, "THE TENANT BELOW MUST LEAVE THE PREMISES",
          font(SANS_B, 27), MAGENTA_DARK)

    lf = font(SANS_B, 26)
    v34 = font(SANS_B, 34)
    d.text((44, 316), "TENANT", font=lf, fill=GREY)
    d.text((44, 350), "GRAND THEFT AUTO V", font=v34, fill=INK)
    d.text((560, 316), "VACATE BY", font=lf, fill=GREY)
    d.text((560, 350), "NOV 19, 2026", font=v34, fill=INK)
    d.text((44, 414), "PREMISES", font=lf, fill=GREY)
    d.text((44, 448), "THE SSD - EVERY CONSOLE & PC", font=v34, fill=INK)

    stamp(img, "VACATED", 850, 468, 38, MAGENTA_DARK, angle=-8)
    d = ImageDraw.Draw(img)

    d.text((44, 524), "GROUNDS FOR EVICTION", font=lf, fill=GREY)
    rows = [
        ("Squatting on the drive since 2013", "13 YEARS"),
        ("Rent paid in nostalgia - expired", "EXPIRED"),
        ("New tenant needs the room", "214 GB"),
    ]
    fee_rows(d, rows, 44, 560, W - 44, size=35, gap=46)
    d.text((44, 712), "THE NEW TENANT WAITED 13 YEARS TO MOVE IN",
           font=font(SANS_B, 30), fill=INK)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # the new tenant, moved in: suitcase at its feet, front-door key in hand
    draw_suitcase(d, 176, 1000)
    draw_key(d, 292, gy + 118)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "MOVING COSTS PAID BY MY AI AGENT",
              "with bounty money it earned on")
    return img


# ---------------------------------------------------------------- candidate H
def candidate_h():
    """Marriage certificate: the fan and the release date, finally wed."""
    img, d = base_canvas()
    header(d, "LEONIDA REGISTRY OF MARRIAGES", "CERTIFICATE OF MARRIAGE")

    ctext(d, W // 2, 198, "This certifies that", font(SERIF_I, 36), GREY)
    ctext(d, W // 2, 246, "EVERY GTA FAN", font(SERIF_B, 62), INK)
    ctext(d, W // 2, 322, "and", font(SERIF_I, 34), MAGENTA_DARK)
    ctext(d, W // 2, 356, "THE RELEASE DATE", font(SERIF_B, 62), INK)
    ctext(d, W // 2, 442, "were joined in marriage on", font(SANS_R, 28), INK)
    ctext(d, W // 2, 476, "NOV 19, 2026", font(SANS_B, 42), INK)

    stamp(img, "FINALLY", 875, 478, 36, MAGENTA_DARK, angle=-8)
    d = ImageDraw.Draw(img)

    lf = font(SANS_B, 26)
    d.text((44, 536), "ENGAGEMENT RECORD", font=lf, fill=GREY)
    rows = [
        ("Engaged", "SEP 17, 2013"),
        ("Wedding postponed", "FALL 2025"),
        ("Postponed a second time", "MAY 2026"),
        ("Vows exchanged in", "TWO TRAILERS"),
    ]
    fee_rows(d, rows, 44, 570, W - 44, size=34, gap=44)
    d.text((44, 748), "WITNESSED BY: JASON & LUCIA",
           font=font(SANS_B, 28), fill=INK)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # the officiant's bowtie, worn low on the body, clear of the eyes
    ncx, ncy = gx + 100, gy + 130
    d.polygon([(ncx, ncy), (ncx - 42, ncy - 17), (ncx - 42, ncy + 17)],
              fill=INK)
    d.polygon([(ncx, ncy), (ncx + 42, ncy - 17), (ncx + 42, ncy + 17)],
              fill=INK)
    d.ellipse([ncx - 9, ncy - 9, ncx + 9, ncy + 9], fill=INK)
    # and the ring it holds out is the magenta coin itself
    draw_coin(d, edge + 40, gy + 118, 54)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "WEDDING PAID FOR BY MY AI AGENT",
              "with its bounty winnings on")
    return img


# ---------------------------------------------------------------- candidate I
def candidate_i():
    """Lottery ticket: one draw that took thirteen years to come up."""
    img, d = base_canvas()
    header(d, "LEONIDA STATE LOTTERY", "MEGA DRAW - OFFICIAL TICKET",
           right_top="DRAW NO.", right_big="13")

    lf = font(SANS_B, 26)
    v32 = font(SANS_B, 32)
    d.text((44, 192), "PLAYER", font=lf, fill=GREY)
    d.text((44, 226), "EVERY GTA FAN", font=v32, fill=INK)
    d.text((400, 192), "BOUGHT", font=lf, fill=GREY)
    d.text((400, 226), "SEP 17, 2013", font=v32, fill=INK)
    d.text((736, 192), "DRAWN", font=lf, fill=GREY)
    d.text((736, 226), "NOV 19, 2026", font=v32, fill=INK)

    d.text((44, 292), "YOUR NUMBERS", font=lf, fill=GREY)
    balls = [("13", WHITE, INK, 46), ("2", WHITE, INK, 46),
             ("2", WHITE, INK, 46), ("214", WHITE, INK, 38),
             ("79.99", MAGENTA, WHITE, 30)]
    for (num, fill, tcol, fs), cx in zip(balls, (96, 318, 540, 762, 984)):
        draw_ball(d, cx, 376, 54, num, fill, tcol, fs)

    rows = [
        ("Years waited for a single draw", "13"),
        ("Trailers along the way", "2"),
        ("Delays survived", "2"),
        ("Download size, in gigabytes", "214"),
    ]
    fee_rows(d, rows, 44, 462, W - 44, size=33, gap=42)
    d.line([44, 648, W - 44, 648], fill=INK, width=3)
    pf = font(SANS_B, 40)
    d.text((44, 664), "GRAND PRIZE: ONE GAME", font=pf, fill=INK)
    tot = "$79.99"
    d.text((W - 44 - tw(d, tot, pf), 664), tot, font=pf, fill=INK)

    stamp(img, "JACKPOT", 845, 742, 34, STAMP_RED, angle=-7)

    d = band(img, None, None)
    gx, gy = 58, 820
    edge, _ey = draw_ghost(d, gx, gy, 200, 230)
    # the host holds up the winning ball: the magenta coin, star and all
    draw_coin(d, edge + 40, gy + 118, 54)
    draw_hand(d, edge - 2, gy + 140, 29)
    band_text(d, "TICKET PAID FOR BY MY AI AGENT",
              "with bounty money it earned on")
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in (("candidate-a", candidate_a),
                     ("candidate-b", candidate_b),
                     ("candidate-c", candidate_c),
                     ("candidate-a2", candidate_a2),
                     ("candidate-a3", candidate_a3),
                     ("candidate-d", candidate_d),
                     ("candidate-e", candidate_e),
                     ("candidate-f", candidate_f),
                     ("candidate-g", candidate_g),
                     ("candidate-h", candidate_h),
                     ("candidate-i", candidate_i)):
        img = fn()
        path = os.path.join(OUT_DIR, name + ".png")
        img.save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
