#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Tuesday 24 November 2026.

Draws a single 1024x1024 news image from scratch with Pillow.
Every story below was verified first-reported on Tuesday 24 November 2026
(UTC) against wire-grade sources; near-misses are listed in the DATE CHECK
box with their true dates. Deterministic: same input, same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
PAPER2 = (238, 231, 218)
INK = (22, 26, 38)
NAVY = (18, 32, 60)
NAVY2 = (28, 48, 88)
GOLD = (198, 158, 38)
GOLD_L = (232, 200, 110)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
SKY = (168, 196, 222)
CARD_BG = (255, 255, 255)
MUTED = (96, 96, 100)
LINE = (180, 172, 152)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SERIF_R = lambda s: font("DejaVuSerif.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def panel(d, x, y, w, h, fill=CARD_BG, shadow=True, outline=None):
    """Raised card: soft drop shadow + rounded body (3D depth)."""
    if shadow:
        d.rounded_rectangle([x + 3, y + 4, x + w + 3, y + h + 4],
                            radius=8, fill=(0, 0, 0, 42))
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fill,
                        outline=outline, width=1 if outline else 0)


def tag(d, x, y, text, bg, fg=(255, 255, 255)):
    """Small pill label; returns its width."""
    f = F_SANSB(10)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 12, y + 17], radius=8, fill=bg)
    d.text((x + 6, y + 2), text, font=f, fill=fg)
    return tw + 12


def label_chip(d, x, y, kind):
    """CONFIRMED / OFFICIAL / REPORTED / CLAIM chip."""
    cols = {"CONFIRMED": (24, 110, 54), "OFFICIAL": NAVY2,
            "REPORTED": (150, 96, 8), "CLAIM": RED}
    return tag(d, x, y, kind, cols[kind])


# ---------------------------------------------------------------- scenes
def sky(d, box, top, bottom):
    """Vertical gradient sky inside box (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def smoke(cx, cy, box):
    """Soft smoke puffs, clipped inside box (x0, y0, x1, y1) so nothing
    spills over the panel edge. Drawn on a temp layer and composited."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", (max(1, x1 - x0), max(1, y1 - y0)),
                      (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i in range(3):
        r = 7 + i * 3
        ccx, ccy = cx - x0 + i * 4, cy - y0 - i * 5
        ld.ellipse([ccx - r, ccy - r, ccx + r, ccy + r],
                   fill=(120, 120, 125, 95))
    img.paste(layer, (x0, y0), layer)


def scene_zaporizhzhia(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (52, 58, 86), (120, 110, 108))
    d.ellipse([x + w - 34, y + 10, x + w - 12, y + 32], fill=(226, 190, 120))
    bx, by, bw, bh = x + 18, y + h - 78, 84, 78
    d.rectangle([bx, by, bx + bw, by + bh], fill=(74, 66, 62))
    for r in range(4):
        for c in range(4):
            wx, wy = bx + 8 + c * 19, by + 8 + r * 18
            broken = (r, c) in [(1, 1), (1, 2), (2, 1)]
            d.rectangle([wx, wy, wx + 12, wy + 11],
                        fill=(12, 10, 10) if broken else (214, 178, 96))
    d.polygon([(bx, by), (bx + 30, by - 16), (bx + 60, by)], fill=(52, 46, 44))
    d.polygon([(bx + 14, by + bh), (bx + 34, by + bh - 22),
               (bx + 54, by + bh), (bx + 70, by + bh)],
              fill=(58, 50, 46))
    smoke(bx + 52, by - 8, (x, y, x + w, y + h))
    d.polygon([(x + 120, y + h), (x + 150, y + h - 34), (x + 180, y + h)],
              fill=(58, 50, 46))
    d.rectangle([x + 150, y + h - 46, x + 156, y + h - 30], fill=(226, 120, 40))
    d.ellipse([x + 144, y + h - 58, x + 162, y + h - 40], fill=(240, 160, 60))


def scene_sanofi(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (232, 240, 248), (196, 214, 232))
    d.rectangle([x + 14, y + h - 46, x + 118, y + h - 10], fill=(255, 255, 255),
                outline=(150, 160, 175))
    bars = [(0, 22), (1, 34), (2, 30), (3, 52)]
    for i, bh in bars:
        bx = x + 24 + i * 24
        d.rectangle([bx, y + h - 18 - bh, bx + 16, y + h - 18],
                    fill=NAVY2 if i < 3 else GOLD)
    d.line([(x + 18, y + h - 18), (x + 116, y + h - 18)], fill=INK, width=2)
    d.line([(x + 24, y + h - 24), (x + 108, y + h - 66)], fill=RED, width=3)
    d.ellipse([x + 100, y + h - 74, x + 116, y + h - 58], fill=RED)
    cx, cy = x + w - 58, y + 34
    d.ellipse([cx - 30, cy - 13, cx + 30, cy + 13], fill=(220, 60, 60))
    d.ellipse([cx - 30, cy - 13, cx, cy + 13], fill=(245, 245, 245),
              outline=(180, 180, 180))
    d.ellipse([cx - 30, cy - 13, cx + 30, cy + 13], outline=(120, 120, 120))
    d.text((x + 14, y + 8), "$41bn", font=F_SANSB(26), fill=NAVY)


def scene_riyadh(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (10, 16, 40), (40, 58, 96))
    for sx, sy in [(x + 20, y + 12), (x + 60, y + 22), (x + 250, y + 14),
                   (x + 290, y + 30), (x + 150, y + 8)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([x + 8, y + h - 34, x + 60, y + h], fill=(16, 22, 44))
    d.rectangle([x + 252, y + h - 44, x + 300, y + h], fill=(16, 22, 44))
    tx, tw = x + 128, 56
    ty, th = y + 18, h - 18
    d.polygon([(tx, ty + th), (tx, ty + 22), (tx + tw, ty + 22),
               (tx + tw, ty + th)], fill=(30, 44, 78))
    d.polygon([(tx, ty + 22), (tx + tw // 2, ty), (tx + tw, ty + 22)],
              fill=(22, 34, 64))
    for r in range(6):
        for c in range(4):
            wx = tx + 6 + c * 13
            wy = ty + 30 + r * 11
            lit = (r + c) % 3 != 0
            d.rectangle([wx, wy, wx + 8, wy + 6],
                        fill=(240, 210, 120) if lit else (12, 18, 36))
    smoke(tx + tw // 2, ty + 6, (x, y, x + w, y + h))
    d.polygon([(tx + 18, ty + 6), (tx + 30, ty - 6), (tx + 42, ty + 6)],
              fill=(240, 140, 40))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(8, 12, 28))


def scene_gaza(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (214, 176, 130), (150, 120, 96))
    d.ellipse([x + w - 30, y + 8, x + w - 8, y + 30], fill=(240, 200, 120))
    for bx, bw, bh in [(x + 6, 26, 44), (x + 38, 20, 58), (x + 64, 30, 36),
                       (x + 100, 22, 50)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(70, 58, 50))
    smoke(x + 48, y + h - 56, (x, y, x + w, y + h))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(52, 44, 40))


def scene_quake(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (190, 210, 230), (150, 175, 200))
    d.polygon([(x, y + h), (x + 34, y + 26), (x + 68, y + h)], fill=(90, 110, 130))
    d.polygon([(x + 24, y + 40), (x + 34, y + 26), (x + 44, y + 40)],
              fill=(245, 245, 245))
    d.polygon([(x + 52, y + h), (x + 96, y + 14), (x + 140, y + h)],
              fill=(70, 92, 116))
    d.polygon([(x + 86, y + 30), (x + 96, y + 14), (x + 106, y + 30)],
              fill=(245, 245, 245))
    pts = [(x + 8, y + h - 22), (x + 26, y + h - 22), (x + 34, y + h - 40),
           (x + 44, y + h - 8), (x + 54, y + h - 34), (x + 64, y + h - 22),
           (x + 84, y + h - 22), (x + 92, y + h - 44), (x + 102, y + h - 10),
           (x + 112, y + h - 22), (x + 132, y + h - 22)]
    d.line(pts, fill=RED, width=2, joint="curve")
    d.ellipse([x + 14, y + 10, x + 28, y + 24], fill=RED)
    d.text((x + 16, y + 11), "*", font=F_SANSB(12), fill=(255, 255, 255))


def scene_fire(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (60, 58, 62), (120, 100, 88))
    fx, fy, fw, fh = x + 16, y + h - 52, 108, 52
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(96, 84, 72))
    for i in range(4):
        sx = fx + i * 28
        d.polygon([(sx, fy), (sx + 14, fy - 12), (sx + 28, fy)],
                  fill=(70, 60, 50))
    d.rectangle([fx + 12, fy + 16, fx + 26, fy + 30], fill=(240, 200, 90))
    d.rectangle([fx + 44, fy + 16, fx + 58, fy + 30], fill=(30, 26, 24))
    d.rectangle([fx + 76, fy + 16, fx + 90, fy + 30], fill=(240, 200, 90))
    for fx2, fy2, s in [(fx + 30, fy - 8, 1.0), (fx + 70, fy - 14, 1.3)]:
        d.polygon([(fx2 - 12 * s, fy2 + 8), (fx2, fy2 - 12 * s),
                   (fx2 + 12 * s, fy2 + 8)], fill=(240, 120, 30))
        d.polygon([(fx2 - 7 * s, fy2 + 8), (fx2, fy2 - 4 * s),
                   (fx2 + 7 * s, fy2 + 8)], fill=(250, 200, 60))
    smoke(fx + 54, fy - 16, (x, y, x + w, y + h))


def scene_jets(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (140, 180, 215), (200, 220, 235))
    d.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=(250, 240, 200))
    d.polygon([(x + 8, y + h - 18), (x + 44, y + h - 26), (x + 78, y + h - 14),
               (x + 108, y + h - 22), (x + 140, y + h - 10), (x + 140, y + h),
               (x + 8, y + h)], fill=(46, 110, 70))
    d.line([(x, y + h - 14), (x + w, y + h - 14)], fill=(40, 90, 140), width=2)
    jx, jy = x + 30, y + 22
    d.polygon([(jx, jy), (jx + 46, jy + 6), (jx + 46, jy + 10),
               (jx + 8, jy + 12), (jx + 18, jy + 20), (jx + 12, jy + 12),
               (jx, jy + 8)], fill=(40, 44, 54))
    d.polygon([(jx + 84, jy + 4), (jx + 118, jy + 10), (jx + 118, jy + 14),
               (jx + 88, jy + 14), (jx + 96, jy + 20), (jx + 88, jy + 12)],
              fill=(60, 64, 74))
    tx, ty = x + w - 26, y + 8
    d.polygon([(tx, ty + 16), (tx + 9, ty), (tx + 18, ty + 16)],
              fill=(240, 200, 60), outline=RED)
    d.text((tx + 7, ty + 6), "!", font=F_SANSB(11), fill=RED)


def scene_delta(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (24, 40, 66), (40, 66, 100))
    d.rounded_rectangle([x + 12, y + 10, x + w - 12, y + h - 10], radius=4,
                        fill=(12, 22, 40), outline=(90, 130, 180))
    pts = [(x + 30, y + 20), (x + 62, y + 30), (x + 96, y + 18),
           (x + 118, y + 32), (x + 44, y + 36), (x + 78, y + 28)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(90, 160, 220), width=1)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(240, 200, 60))
    d.text((x + 20, y + h - 20), "DELTA // LIVE MAP", font=F_SANSB(9),
           fill=(140, 190, 240))


def scene_solomons(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (120, 190, 225), (190, 225, 240))
    d.ellipse([x + 16, y + 10, x + 34, y + 28], fill=(250, 235, 170))
    d.polygon([(x + 8, y + h - 16), (x + 52, y + h - 34), (x + 96, y + h - 20),
               (x + 132, y + h - 30), (x + 140, y + h - 16), (x + 140, y + h),
               (x + 8, y + h)], fill=(52, 130, 80))
    d.line([(x, y + h - 16), (x + w, y + h - 16)], fill=(30, 110, 160), width=3)
    px, py = x + 66, y + h - 34
    d.line([(px, py), (px, py - 22)], fill=(90, 60, 30), width=3)
    for dx, dy in [(-12, -8), (0, -14), (12, -8), (-8, -2), (8, -2)]:
        d.line([(px, py - 22), (px + dx, py - 22 + dy)], fill=(30, 110, 50),
               width=2)
    d.rectangle([x + w - 46, y + 14, x + w - 12, y + 44], fill=(255, 255, 255),
                outline=(120, 120, 120))
    d.line([(x + w - 42, y + 20), (x + w - 16, y + 20)], fill=INK, width=1)
    d.line([(x + w - 42, y + 26), (x + w - 16, y + 26)], fill=INK, width=1)
    d.line([(x + w - 42, y + 32), (x + w - 26, y + 32)], fill=INK, width=1)
    d.ellipse([x + w - 30, y + 36, x + w - 22, y + 44], outline=RED, width=2)


def scene_rocket(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (8, 14, 36), (30, 48, 84))
    for sx, sy in [(x + 14, y + 10), (x + 40, y + 22), (x + 120, y + 12),
                   (x + 132, y + 30), (x + 90, y + 8)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    rx, ry = x + 56, y + 8
    d.polygon([(rx + 8, ry), (rx + 16, ry + 12), (rx, ry + 12)],
              fill=(200, 40, 40))
    d.rectangle([rx, ry + 12, rx + 16, ry + 44], fill=(240, 240, 240))
    d.rectangle([rx, ry + 12, rx + 16, ry + 20], fill=(40, 80, 160))
    d.polygon([(rx, ry + 44), (rx - 8, ry + 56), (rx, ry + 50)], fill=(200, 40, 40))
    d.polygon([(rx + 16, ry + 44), (rx + 24, ry + 56), (rx + 16, ry + 50)],
              fill=(200, 40, 40))
    d.polygon([(rx + 4, ry + 44), (rx + 8, ry + 62), (rx + 12, ry + 44)],
              fill=(250, 180, 40))
    d.ellipse([x + w - 40, y + 14, x + w - 12, y + 42], outline=(200, 210, 230),
              width=2)
    d.rectangle([x + w - 34, y + 24, x + w - 18, y + 32], fill=(200, 210, 230))


def scene_ship(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (150, 190, 220), (200, 220, 235))
    for i, yy in enumerate([y + h - 26, y + h - 18, y + h - 10]):
        d.line([(x, yy), (x + w, yy)], fill=(40, 100, 160), width=3)
    sx, sy = x + 18, y + h - 44
    d.polygon([(sx, sy + 16), (sx + 14, sy + 16), (sx + 96, sy + 16),
               (sx + 84, sy + 30), (sx + 10, sy + 30)], fill=(60, 64, 72))
    d.rectangle([sx + 24, sy, sx + 56, sy + 16], fill=(90, 94, 102))
    d.rectangle([sx + 30, sy - 10, sx + 38, sy], fill=(70, 74, 82))
    d.polygon([(sx + 96, sy + 8), (sx + 108, sy - 6), (sx + 114, sy + 8)],
              fill=(240, 140, 40))
    dx, dy = x + w - 34, y + 16
    d.line([(dx - 8, dy), (dx + 8, dy)], fill=INK, width=2)
    d.line([(dx, dy - 8), (dx, dy + 8)], fill=INK, width=2)
    for ox, oy in [(-8, -8), (8, -8), (-8, 8), (8, 8)]:
        d.ellipse([dx + ox - 3, dy + oy - 3, dx + ox + 3, dy + oy + 3],
                  fill=INK)


def scene_oil(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (232, 200, 140), (200, 160, 100))
    d.ellipse([x + w - 36, y + 8, x + w - 10, y + 34], fill=(250, 220, 130))
    dx, dy = x + 20, y + 12
    d.line([(dx, dy + 46), (dx + 16, dy), (dx + 32, dy + 46)], fill=(60, 50, 40),
           width=3)
    d.line([(dx + 4, dy + 30), (dx + 28, dy + 30)], fill=(60, 50, 40), width=2)
    d.line([(dx + 8, dy + 16), (dx + 24, dy + 16)], fill=(60, 50, 40), width=2)
    d.rectangle([dx + 46, y + h - 30, dx + 92, y + h - 14], fill=(80, 66, 50))
    d.ellipse([dx + 50, y + h - 40, dx + 58, y + h - 32], fill=(40, 40, 40))
    d.ellipse([dx + 78, y + h - 40, dx + 86, y + h - 32], fill=(40, 40, 40))
    d.rectangle([dx + 52, y + h - 44, dx + 84, y + h - 40], fill=(40, 40, 40))
    d.line([(dx + 100, y + h - 14), (dx + 100, y + h - 44)], fill=(60, 50, 40),
           width=3)
    d.ellipse([dx + 94, y + h - 52, dx + 106, y + h - 40], fill=(240, 120, 30))


def scene_hospital(d, x, y, w, h):
    sky(d, (x, y, x + w, y + h), (200, 225, 210), (170, 200, 185))
    hx, hy, hw, hh = x + 22, y + h - 54, 96, 54
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(245, 245, 240),
                outline=(140, 140, 140))
    d.rectangle([hx + 8, hy + 10, hx + 26, hy + 26], fill=(200, 40, 40))
    d.rectangle([hx + 14, hy + 14, hx + 20, hy + 22], fill=(255, 255, 255))
    d.rectangle([hx + 10, hy + 14, hx + 24, hy + 18], fill=(255, 255, 255))
    d.rectangle([hx + 14, hy + 10, hx + 18, hy + 26], fill=(255, 255, 255))
    d.rectangle([hx + 40, hy + 14, hx + 56, hy + 26], fill=(160, 200, 230))
    d.rectangle([hx + 66, hy + 14, hx + 82, hy + 26], fill=(160, 200, 230))
    d.rectangle([hx + 40, hy + 34, hx + 56, hy + hh], fill=(120, 90, 60))
    d.polygon([(x + 6, y + h - 8), (x + 30, y + h - 30), (x + 54, y + h - 8)],
              fill=(230, 225, 200))
    d.polygon([(x + 6, y + h - 8), (x + 30, y + h - 30), (x + 54, y + h - 8)],
              outline=(150, 140, 110))
    d.ellipse([x + w - 24, y + 10, x + w - 10, y + 24], fill=(90, 160, 90))
    d.rectangle([x + w - 19, y + 12, x + w - 15, y + 22], fill=(40, 90, 40))


# ---------------------------------------------------------------- data
# All items verified first-reported Tue 24 Nov 2026 (UTC). Labels:
# CONFIRMED = 2+ outlets, OFFICIAL = on the record, REPORTED = one outlet,
# CLAIM = single-sided claim, attribution named.

LEADS = [
    dict(tag="ZAPORIZHZHIA", label="CONFIRMED", src="Reuters",
         head="Russian strike kills 2 in Zaporizhzhia",
         sub="Overnight strike tears apart a 5-storey block; 41+ hurt, incl. children.",
         scene=scene_zaporizhzhia),
    dict(tag="PHARMA", label="OFFICIAL", src="Sanofi / WSJ",
         head="Sanofi buys Insmed for $41bn in cash",
         sub="$175 a share, a 17% premium - the year's biggest pharma deal.",
         scene=scene_sanofi),
    dict(tag="RIYADH", label="CLAIM", src="Reuters / AFP",
         head="Riyadh tower hit again; 11 hurt",
         sub="Second strike on the PIF Tower in a week; no group claims it.",
         scene=scene_riyadh),
]

CARDS = [
    dict(n=1, tag="GAZA", label="CONFIRMED", src="Reuters",
         head="Hamas security chief killed in Gaza strike",
         scene=scene_gaza, lat=31.5, lon=34.5),
    dict(n=2, tag="NEPAL", label="CONFIRMED", src="USGS",
         head="M5.3 quake shakes Nepal at 01:32 UTC",
         scene=scene_quake, lat=27.8, lon=88.0),
    dict(n=3, tag="INDONESIA", label="CONFIRMED", src="AP",
         head="Banten fire toll hits 26; probe opened",
         scene=scene_fire, lat=-6.2, lon=106.2),
    dict(n=4, tag="KOREA", label="CONFIRMED", src="Reuters",
         head="Russian jets near Seoul island; alert",
         scene=scene_jets, lat=37.5, lon=130.9),
    dict(n=5, tag="GERMANY", label="OFFICIAL", src="Ukraine MoD",
         head="Berlin first to get Ukraine's DELTA",
         scene=scene_delta, lat=52.5, lon=13.4),
    dict(n=6, tag="PACIFIC", label="REPORTED", src="Reuters",
         head="Solomons to end China security pact",
         scene=scene_solomons, lat=-9.4, lon=160.0),
    dict(n=7, tag="SPACE", label="OFFICIAL", src="Xinhua",
         head="Shenzhou-24 crew unveiled; first foreigner",
         scene=scene_rocket, lat=40.0, lon=99.0),
    dict(n=8, tag="LIBYA", label="CONFIRMED", src="Reuters",
         head="Kyiv defends Benghazi ship strikes",
         scene=scene_ship, lat=32.1, lon=20.1),
    dict(n=9, tag="IRAQ", label="CONFIRMED", src="Reuters",
         head="Baghdad orders Kurdish oil takeover",
         scene=scene_oil, lat=33.3, lon=44.4),
    dict(n=10, tag="CONGO", label="CONFIRMED", src="UN News",
         head="Ebola teams trapped in Congo hospital",
         scene=scene_hospital, lat=1.5, lon=30.0),
]

ALSO = [
    "Air defences down 73 of 96 drones overnight - Kyiv",
    "US envoy doubts Israel military aid will end this year - Reuters",
    "Russia's 2026 troop losses hit record 432,519 - General Staff",
    "Norway joins Germany in testing DELTA - Nov 24",
    "Ukraine-Norway expand DESNA defence; $7bn Oslo aid 2027",
    "UK warns firms over Russian sabotage threat",
    "~100 civilians trapped on Kinburn Spit, short of food and medicine",
    "Sanofi shares +5.6% at open; Insmed +14%",
    "Nepal quake: no casualties reported - PTI",
    "Funeral held in Gaza for Hamas security chief - i24",
    "Seoul summons Russian defence attache - Reuters",
    "KRG rejects Baghdad order: 'in no way acceptable' - Reuters",
    "Zaporizhzhia block torn apart; 41+ hurt incl. children",
    "Sanofi pays $175/share, 17% premium; gains 2 drugs",
    "Solomons treaty: no foreign base; China pact ends Apr 2027",
    "DELTA: Germany gets no access to Ukraine's combat data - MoD",
    "Shenzhou: Ali returns aboard Shenzhou 23 after a week - Xinhua",
    "Doha urges US-Iran talks + Hormuz reopening - Anadolu",
    "Banten: police open criminal negligence probe - AP",
    "Nepal quake felt in Sikkim, N. Bengal, Bhutan, China - USGS",
    "Riyadh: coalition calls tower attack 'cowardly terrorist attack' - SPA",
    "Car bomb in Villavicencio injures 23; president visits Tue - AP",
]

TIMELINE = [
    ("01:32", "M5.3 quake strikes Nepal"),
    ("03:12", "Seoul scrambles jets"),
    ("06:30", "Sanofi $41bn deal"),
    ("09:16", "Shenzhou-24 crew named"),
    ("10:12", "DELTA for Germany"),
    ("14:50", "Banten toll hits 26"),
]

EXCLUDED = [
    ("ICJ Myanmar genocide ruling", "Thu 19 Nov"),
    ("COP31 ends without a pact", "Sun 22 Nov"),
    ("Ukraine sinks Russian corvette Merkury", "Sun 22 Nov"),
    ("US loses measles elimination status", "Mon 17 Nov"),
    ("Indonesia VP nominations", "Mon 23 Nov"),
    ("CrowdStrike-Zscaler $43.9bn deal", "Mon 23 Nov"),
    ("Brentford 4-0 Everton", "Sun 23 Nov"),
    ("EU 22nd sanctions package", "Mon 23 Nov"),
    ("Nepal PM's Delhi visit", "Mon 23 Nov"),
    ("Lukoil refinery + Tatarstan strikes", "Mon 23 Nov"),
    ("Medvedev nuclear-warning article", "Mon 23 Nov"),
    ("OpenAI-Cisco Shirudo launch", "Mon 23 Nov"),
    ("Virginia + Oregon sue SpaceX over Grok", "Mon 23 Nov"),
    ("Parastoo Ahmadi flogged 74 times", "Mon 23 Nov"),
    ("Mexico to try 'El Chapo Isidro'", "Mon 23 Nov"),
]

NOT_YET = [
    "Shenzhou-24 launch - Wed 25 Nov, 00:18 UTC",
    "Solomons-Australia treaty signing - Wed 25 Nov",
    "EU sanctions: Council vote still to come",
]

REGIONS = [("Europe", 13), ("Middle East", 7), ("Asia", 9),
           ("Oceania", 2), ("Africa", 2), ("S. America", 1),
           ("N. America", 1)]

# Simplified continent outlines (lon, lat) for the dot map.
CONTINENTS = {
    "N America": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73),
                  (-60, 62), (-55, 47), (-70, 42), (-80, 32), (-84, 30),
                  (-97, 26), (-105, 20), (-95, 16), (-86, 12), (-92, 15),
                  (-105, 22), (-120, 34), (-125, 48), (-150, 60)],
    "S America": [(-78, 8), (-72, 12), (-62, 10), (-52, 5), (-44, -3),
                  (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45),
                  (-68, -52), (-72, -42), (-73, -30), (-77, -18), (-81, -6),
                  (-80, 0)],
    "Europe": [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 57), (10, 59),
               (18, 56), (21, 55), (24, 60), (30, 62), (32, 70), (40, 68),
               (44, 60), (40, 52), (38, 46), (30, 46), (28, 41), (23, 36),
               (19, 42), (12, 44), (8, 44), (3, 42), (0, 39)],
    "Africa": [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
               (51, 11), (48, 0), (40, -10), (36, -18), (32, -28), (26, -34),
               (18, -32), (14, -22), (12, -12), (9, -2), (9, 4), (-8, 4),
               (-16, 12), (-17, 20), (-15, 28)],
    "Asia": [(40, 68), (50, 70), (70, 72), (90, 75), (110, 76), (130, 72),
             (160, 70), (178, 66), (170, 60), (160, 58), (142, 52),
             (140, 40), (130, 35), (122, 30), (120, 22), (110, 20),
             (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 13),
             (75, 8), (70, 24), (60, 25), (55, 26), (50, 29), (48, 30),
             (44, 30), (40, 36), (36, 36), (38, 44), (40, 52), (44, 60)],
    "Oceania": [(113, -22), (120, -34), (130, -32), (140, -38), (150, -37),
                (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
                (130, -13), (122, -17), (114, -30)],
}

# ---------------------------------------------------------------- build
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")
MX = 28  # side margin

# --- masthead: navy band, extruded serif title, gold date line
d.rectangle([0, 0, W, 88], fill=NAVY)
d.rectangle([0, 86, W, 88], fill=GOLD)
d.text((MX + 2, 8), "THE WORLD IN ONE DAY", font=F_SERIF(40),
       fill=(10, 18, 36))
d.text((MX, 6), "THE WORLD IN ONE DAY", font=F_SERIF(40), fill=(255, 255, 255))
d.text((MX, 50), "TUESDAY  24  NOVEMBER  2026", font=F_SANSB(17), fill=GOLD_L)
d.text((W - MX - 330, 52), "35 STORIES  \u00b7  7 REGIONS  \u00b7  ALL FROM THIS TUESDAY",
       font=F_SANSB(11), fill=(200, 210, 230))
d.text((MX, 70), "DAY IN NUMBERS:  2 killed \u00b7 $41bn \u00b7 11 hurt \u00b7 M5.3 \u00b7 26 dead \u00b7 23 hurt",
       font=F_SANSB(10), fill=(160, 175, 205))

y = 96
# --- timeline strip
d.text((MX, y), "THE DAY  \u2014  ALL TIMES UTC", font=F_SANSB(11), fill=NAVY)
y += 18
d.line([(MX, y + 6), (W - MX, y + 6)], fill=LINE, width=2)
seg = (W - 2 * MX) / len(TIMELINE)
for i, (t, txt) in enumerate(TIMELINE):
    cx = MX + seg * i + seg / 2
    d.ellipse([cx - 5, y + 1, cx + 5, y + 11], fill=NAVY, outline=GOLD, width=2)
    d.text((cx - 16, y + 14), t, font=F_SANSB(10), fill=RED)
    for ln, line in enumerate(wrap(d, txt, F_SANS(9), seg - 10)):
        d.text((cx - seg / 2 + 5, y + 27 + ln * 11), line, font=F_SANS(9),
               fill=INK)
y += 44

# --- leads: 3 illustrated panels
lw, lh, gap = (W - 2 * MX - 2 * 12) // 3, 196, 12
for i, lead in enumerate(LEADS):
    x = MX + i * (lw + gap)
    panel(d, x, y, lw, lh)
    lead["scene"](d, x + 6, y + 6, lw - 12, 92)
    ty = y + 104
    label_chip(d, x + 10, ty, lead["label"])
    tag(d, x + 10 + 92, ty, lead["tag"], NAVY2)
    d.text((x + 10, ty + 22), lead["head"], font=F_SANSB(15), fill=INK)
    for ln, line in enumerate(wrap(d, lead["sub"], F_SANS(10), lw - 20)):
        d.text((x + 10, ty + 42 + ln * 13), line, font=F_SANS(10), fill=MUTED)
    d.text((x + 10, y + lh - 18), lead["src"], font=F_SANSB(9), fill=NAVY2)
y += lh + 8

# --- story cards: 2 rows x 5
cw, chh = (W - 2 * MX - 4 * 8) // 5, 138
for row in range(2):
    for col in range(5):
        c = CARDS[row * 5 + col]
        x = MX + col * (cw + 8)
        cy = y + row * (chh + 8)
        panel(d, x, cy, cw, chh)
        c["scene"](d, x + 5, cy + 5, cw - 10, 62)
        d.ellipse([x + cw - 24, cy + 8, x + cw - 6, cy + 26], fill=RED)
        d.text((x + cw - 19, cy + 10), str(c["n"]), font=F_SANSB(11),
               fill=(255, 255, 255))
        d.text((x + 7, cy + 71), c["tag"], font=F_SANSB(9), fill=RED)
        for ln, line in enumerate(wrap(d, c["head"], F_SANSB(11), cw - 14)):
            d.text((x + 7, cy + 84 + ln * 13), line, font=F_SANSB(11), fill=INK)
        d.text((x + 7, cy + chh - 15), c["label"] + " \u00b7 " + c["src"],
               font=F_SANS(8), fill=MUTED)
y += 2 * chh + 6 + 8

# --- ALSO list: 22 numbered one-liners, 3 columns
d.text((MX, y), "ALSO TODAY", font=F_SANSB(12), fill=NAVY)
y += 16
col_w = (W - 2 * MX - 2 * 16) // 3
for i, item in enumerate(ALSO):
    col = i // 8
    row = i % 8
    x = MX + col * (col_w + 16)
    yy = y + row * 12
    d.text((x, yy), f"{i + 14:>2}.", font=F_SANSB(9), fill=RED)
    d.text((x + 22, yy), item, font=F_SANS(9), fill=INK)
y += 8 * 12 + 6

# --- dot world map with numbered pins + region legend
map_y = y
map_h = 72
map_x0, map_x1 = MX, W - MX - 210
panel(d, MX, map_y, W - 2 * MX, map_h + 14, fill=(232, 238, 246))
for name, poly in CONTINENTS.items():
    pts = []
    for lon, lat in poly:
        px = map_x0 + 8 + (lon + 180) / 360 * (map_x1 - map_x0 - 16)
        py = map_y + 6 + (90 - lat) / 180 * (map_h - 8)
        pts.append((px, py))
    d.polygon(pts, fill=(196, 206, 190), outline=(150, 160, 145))
pins = [(c["lat"], c["lon"], c["n"]) for c in CARDS]
pins += [(47.8, 35.2, "L1"), (48.9, 2.3, "L2"), (24.7, 46.7, "L3")]
for lat, lon, num in pins:
    px = map_x0 + 8 + (lon + 180) / 360 * (map_x1 - map_x0 - 16)
    py = map_y + 6 + (90 - lat) / 180 * (map_h - 8)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((px - 3 if isinstance(num, int) and num < 10 else px - 5, py - 5),
           str(num), font=F_SANSB(7), fill=(255, 255, 255))
lx = map_x1 + 14
d.text((lx, map_y + 2), "REGIONS - L1-3 = leads", font=F_SANSB(9), fill=NAVY)
for i, (name, cnt) in enumerate(REGIONS):
    yy = map_y + 16 + i * 10
    d.text((lx, yy), f"{name}", font=F_SANS(9), fill=INK)
    d.text((lx + 82, yy), str(cnt), font=F_SANSB(9), fill=RED)
y = map_y + map_h + 14 + 4

# --- DATE CHECK box (raised, gold border)
dc_h = 124
panel(d, MX, y, W - 2 * MX, dc_h, fill=(255, 250, 230), outline=GOLD)
d.text((MX + 10, y + 6), "DATE CHECK \u2014 EXCLUDED: THESE DID NOT HAPPEN ON TUESDAY 24 NOV",
       font=F_SANSB(11), fill=RED)
d.text((MX + 10, y + 22), "Checked against first-reported dates. Anything here was a near-miss.",
       font=F_SANS(9), fill=MUTED)
half = (len(EXCLUDED) + 1) // 2
for i, (what, when) in enumerate(EXCLUDED):
    col = 0 if i < half else 1
    row = i if i < half else i - half
    x = MX + 12 + col * ((W - 2 * MX) // 2)
    yy = y + 38 + row * 9
    d.text((x, yy), "\u2717", font=F_SANSB(9), fill=RED)
    d.text((x + 12, yy), what, font=F_SANS(9), fill=INK)
    d.text((x + 300, yy), when, font=F_SANSB(9), fill=RED)
ny_x = MX + 12
ny_y = y + 38 + half * 9 + 2
d.text((ny_x, ny_y), "NOT YET:  " + "  \u00b7  ".join(NOT_YET),
       font=F_SANSB(9), fill=NAVY2)
y += dc_h + 4

# --- footer
d.line([(MX, y + 2), (W - MX, y + 2)], fill=LINE, width=1)
d.text((MX, y + 8),
       "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 UN News \u00b7 Xinhua \u00b7 USGS \u00b7 Sanofi \u00b7 Ukraine MoD",
       font=F_SANS(9), fill=MUTED)
d.text((MX, y + 20),
       "CONFIRMED = 2+ outlets   OFFICIAL = on the record   REPORTED = one outlet   CLAIM = single-sided, named",
       font=F_SANS(9), fill=MUTED)
d.text((W - MX - 210, y + 8), "Compiled Tue 24 Nov 2026 \u00b7 All times UTC",
       font=F_SANS(9), fill=MUTED)

assert y + 34 <= H, f"layout overflow: footer ends at {y + 34} > {H}"
img.save(OUT)
print("saved", OUT, img.size)
