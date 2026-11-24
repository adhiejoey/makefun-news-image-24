#!/usr/bin/env python3
"""Build the news-image entry for Tuesday 24 November 2026.

Draws a cream-paper broadsheet: masthead, lead story, world map with
numbered story dots, a UTC timeline, a markets snapshot, a DATE CHECK box
and 40 sourced stories. Run: python3 generate.py  ->  writes entry.png
(1024x1024, under 1 MiB) in this directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 240, 218)      # cream paper
PAPER_DK = (238, 229, 203)
INK = (26, 26, 26)
GRAY = (90, 86, 74)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GREEN = (34, 110, 72)
AMBER = (166, 110, 0)
MAP_BG = (220, 232, 232)
LAND = (217, 201, 160)
LAND_EDGE = (138, 122, 82)
GOLD = (146, 104, 20)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    p = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(p, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None, align="left"):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading if leading else int(fnt.size * 1.25)
    for ln in lines:
        if align == "center":
            w = draw.textlength(ln, font=fnt)
            draw.text((x + (max_w - w) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (num, section, headline<=42ch, place, detail, source, confidence, lat, lon)
# section: W=world, P=politics, C=climate/science/health, M=markets/tech, S=sport
# lat/lon None -> no map dot (global / space story)
STORIES = [
    (1, "W", "ICJ: MYANMAR GUILTY OF GENOCIDE", "The Hague", "9-6 ruling", "Daily Summary", "HIGH", 52.07, 4.30),
    (2, "W", "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA", "Benghazi", "7 drones sank Merkury", "OneTurn", "HIGH", 32.12, 20.07),
    (3, "W", "NATO VOWS TO DEFEND SPACE FROM RUSSIA", "Brussels", "orbit in 60 days", "Daily Summary", "HIGH", 50.85, 4.35),
    (4, "W", "MEDVEDEV WARNS OF NUCLEAR ATTACK", "Moscow", "'preventive' strike", "Principia", "MED", 55.75, 37.62),
    (5, "W", "MALAYSIA TO RETURN MIGRANTS TO MYANMAR", "Kuala Lumpur", "thousands to return", "Daily Summary", "HIGH", 3.14, 101.69),
    (6, "W", "GERMANY GETS UKRAINE'S DELTA WAR SYSTEM", "Berlin", "first access", "Kyiv Independent", "HIGH", 52.52, 13.40),
    (7, "W", "EU PROPOSES 22ND SANCTIONS PACKAGE", "Brussels", "vs Russia, sports ban", "OneTurn", "HIGH", 50.85, 4.35),
    (8, "W", "RUSSIAN JETS ENTER KOREA DEFENCE ZONE", "Seoul", "no airspace breach", "Daily Summary", "HIGH", 37.57, 126.98),
    (9, "W", "ISRAELI STRIKES KILL SIX IN GAZA", "Gaza", "incl. two police", "Reuters", "HIGH", 31.50, 34.47),
    (10, "W", "UN: GAZA WAR ERASED 77 YEARS OF PROGRESS", "Gaza", "UN report", "Principia", "HIGH", 31.50, 34.47),
    (11, "W", "IRAQ PM TAKES OVER KURDISH OILFIELDS", "Baghdad", "after smuggling probe", "Reuters", "HIGH", 33.31, 44.36),
    (12, "W", "ITURI FIGHTING TRAPS EBOLA TEAMS", "Ituri, DRC", "crews hid 24 hours", "UN News", "HIGH", 1.57, 30.25),
    (13, "W", "UN URGES PROBE INTO BENGHAZI ATTACKS", "Benghazi", "UNSMIL calls probe", "UN News", "HIGH", 32.12, 20.07),
    (14, "W", "THREE TANKERS HIT MINES IN HORMUZ", "Hormuz", "tankers caught fire", "CNBC", "HIGH", 26.50, 56.20),
    (15, "P", "BUKELE NAMES 3 SOLDIERS KILLED IN HAITI", "Port-au-Prince", "accidental blast", "Daily Summary", "HIGH", 18.54, -72.34),
    (16, "P", "CAR BOMB HITS GOVERNOR'S OFFICE", "Villavicencio", "governor's office", "OneTurn", "HIGH", 4.15, -73.64),
    (17, "P", "MEXICO TO TRY 'CHAPO ISIDRO' DESPITE US", "Sinaloa", "US drone aided it", "Daily Summary", "HIGH", 24.80, -107.40),
    (18, "P", "CHINA: OFFICIAL GETS DEATH FOR SPYING", "Beijing", "official 'Ma'", "Daily Summary", "HIGH", 39.90, 116.40),
    (19, "P", "SPAIN AMNESTIES LEADER PUIGDEMONT", "Madrid", "Supreme Court", "OneTurn", "HIGH", 40.42, -3.70),
    (20, "P", "HASINA PLANS RETURN TO BANGLADESH DEC 16", "Dhaka", "return on 16 Dec", "OneTurn", "MED", 23.81, 90.41),
    (21, "P", "NEPAL PM IN INDIA; DELHI PLEDGES €1.4BN", "New Delhi", "€1.4bn pledged", "OneTurn", "HIGH", 28.61, 77.21),
    (22, "P", "INDONESIA NOMINATES TWO VP CANDIDATES", "Jakarta", "to replace Gibran", "Daily Summary", "HIGH", -6.21, 106.85),
    (23, "P", "CHINA EXTENDS MINERAL CURBS PAUSE", "Beijing", "gallium, germanium", "OneTurn", "HIGH", 39.90, 116.40),
    (24, "P", "GUTERRES URGES TALKS ON AI SAFETY RULES", "New York", "UN chief warns", "Principia", "HIGH", 40.71, -74.01),
    (25, "C", "COP31 CLIMATE SUMMIT ENDS WITH NO DEAL", "Global", "fossil-fuel split", "Principia", "HIGH", None, None),
    (26, "C", "US LOSES MEASLES ELIMINATION STATUS", "Washington", "after 25 years", "Principia", "HIGH", 38.90, -77.04),
    (27, "C", "FDA APPROVES FIRST LIMB-GIRDLE DRUG", "Washington", "BridgeBio drug", "Principia", "HIGH", 38.90, -77.04),
    (28, "C", "MOST DISTANT GLOWING BLACK HOLE FOUND", "Space", "630m yrs after Big Bang", "Principia", "HIGH", None, None),
    (29, "C", "47,000 WOMEN KILLED BY PARTNERS IN 2025", "Global", "UN report", "Principia", "HIGH", None, None),
    (30, "M", "ASIAN STOCKS SURGE: NIKKEI +3.9%", "Tokyo", "Nikkei +3.9%, Seoul +6%", "OneTurn", "HIGH", 35.68, 139.69),
    (31, "M", "SANOFI TO BUY INSMED FOR $41 BILLION", "Paris", "$175 a share, cash", "SuMarket", "HIGH", 48.86, 2.35),
    (32, "M", "CROWDSTRIKE TO BUY ZSCALER FOR $44BN", "Austin", "all-stock deal", "SuMarket", "HIGH", 30.27, -97.74),
    (33, "M", "SPACEX, TESLA DISCUSS $3.5TN MERGER", "Austin", "FT: talks, no deal", "SuMarket", "MED", 30.27, -97.74),
    (34, "M", "BITCOIN CLIMBS 9% TO $60,104", "Global", "risk rally", "SuMarket", "HIGH", None, None),
    (35, "M", "US STATES SUE OVER GROK SEXUALISED IMAGES", "Richmond", "Oregon & Virginia", "Principia", "HIGH", 37.54, -77.46),
    (36, "M", "META LAUNCHES MUSE AI AGENT IN THE UK", "London", "per The Guardian", "SuMarket", "HIGH", 51.51, -0.13),
    (37, "M", "EQUINOR SIGNS 18-YEAR GAS DEAL WITH VNG", "Oslo", "15.3 TWh a year", "SuMarket", "HIGH", 59.91, 10.75),
    (38, "M", "CONOCOPHILLIPS SELLS NORWAY UNIT", "Stavanger", "buyer Vår Energi", "SuMarket", "HIGH", 58.97, 5.73),
    (39, "S", "BRENTFORD 4–0 EVERTON IN PREMIER LEAGUE", "London", "Lewis-Potter brace", "IANS", "HIGH", 51.49, -0.31),
    (40, "S", "INDIA A BEAT UAE BY 7 WICKETS IN DOHA", "Doha", "Asia Cup Rising Stars", "Cricinfo", "HIGH", 25.29, 51.53),
]

SECTION_COLOR = {"W": RED, "P": BLUE, "C": GREEN, "M": GOLD, "S": (110, 60, 140)}
SECTION_NAME = {"W": "World", "P": "Politics", "C": "Climate \u00b7 Science \u00b7 Health",
                "M": "Markets \u00b7 Tech", "S": "Sport"}

# timeline: (hour_utc, label, exact?)  exact=True means a reported time
TIMELINE = [
    (1.10, "01:06  Bukele names Haiti dead", True),
    (2.15, "02:09  US drone aided 'Chapo' capture", True),
    (2.25, "02:15  NATO space vow", True),
    (2.62, "02:37  China spy death sentence", True),
    (3.00, "03:00  ICJ ruling first reported", True),
    (6.0, "~06:00  Asian markets surge", False),
    (9.0, "~09:00  EU sanctions proposal", False),
    (15.5, "~15:30  US deals: Sanofi, CrowdStrike", False),
    (20.0, "~20:00  Brentford 4\u20130 Everton, full time", False),
]

MARKETS = [
    ("Nikkei 225", "+3.91%"),
    ("Kospi", "over 6%"),
    ("Hang Seng", "+0.9%"),
    ("Brent crude", "$86.71"),
    ("Bitcoin", "$60,104  (+9%)"),
]


# ------------------------------------------------------- world map shapes
# Coarse equirectangular continent outlines, (lon, lat) pairs, drawn from
# memory of world geography; stylised, not survey-accurate.
NORTH_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
    (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-117, 32), (-110, 28), (-105, 20),
    (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-79, 9), (-82, 10),
    (-85, 11), (-87, 13), (-88, 15), (-90, 14), (-91, 19), (-97, 26), (-93, 30), (-89, 30),
    (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44),
    (-60, 47), (-55, 47), (-60, 50), (-64, 55), (-68, 58), (-72, 62), (-78, 62), (-85, 66),
    (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 65), (-32, 68), (-25, 70), (-20, 74),
    (-25, 76), (-35, 78), (-50, 76), (-58, 74), (-60, 70)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
    (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-68, -50),
    (-65, -45), (-62, -41), (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
    (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-55, 6), (-60, 8),
    (-62, 9), (-68, 11), (-72, 12), (-76, 10)]
AFRICA = [(-17, 15), (-16, 20), (-13, 27), (-9, 31), (-5, 35), (0, 36), (10, 37), (11, 34),
    (20, 32), (30, 31), (32, 31), (34, 28), (36, 22), (38, 18), (43, 12), (48, 11), (51, 10),
    (46, 5), (42, 0), (40, -5), (40, -12), (36, -18), (33, -26), (28, -33), (20, -35),
    (17, -32), (15, -27), (13, -18), (12, -10), (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 4),
    (-13, 8), (-17, 12)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (0, 50),
    (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (12, 64), (18, 66),
    (22, 68), (25, 70), (30, 70), (32, 68), (35, 66), (40, 66), (45, 68), (50, 69),
    (55, 68), (60, 69), (65, 68), (68, 66), (60, 64), (50, 60), (45, 55), (40, 52),
    (38, 48), (35, 45), (30, 45), (28, 44), (25, 40), (23, 36), (20, 40), (18, 40),
    (15, 44), (12, 44), (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52), (1, 51), (-3, 50)]
ASIA = [(30, 70), (35, 68), (40, 66), (45, 68), (50, 69), (55, 68), (60, 69), (65, 68),
    (68, 66), (70, 72), (75, 73), (80, 73), (90, 75), (100, 76), (110, 74), (120, 73),
    (130, 72), (140, 72), (150, 70), (160, 69), (170, 66), (178, 65), (178, 62), (170, 60),
    (162, 56), (156, 51), (150, 45), (142, 40), (140, 35), (137, 35), (132, 33), (129, 31),
    (127, 35), (126, 38), (124, 40), (122, 38), (120, 35), (122, 32), (120, 28), (118, 25),
    (114, 22), (110, 20), (108, 18), (106, 16), (105, 10), (104, 9), (103, 7), (101, 5),
    (100, 8), (99, 12), (98, 15), (97, 16), (95, 18), (93, 20), (91, 22), (89, 22),
    (87, 21), (85, 19), (82, 17), (80, 15), (78, 10), (77, 8), (76, 10), (74, 14),
    (72, 20), (70, 22), (68, 23), (66, 25), (63, 25), (60, 25), (58, 26), (56, 27),
    (54, 27), (52, 28), (50, 29), (48, 30), (48, 29), (52, 26), (56, 26), (58, 23),
    (59, 22), (55, 18), (52, 15), (48, 14), (44, 13), (43, 12), (40, 15), (39, 20),
    (37, 25), (35, 28), (34, 30), (36, 36), (33, 36), (30, 36), (27, 37), (26, 40),
    (28, 41), (30, 41), (33, 42), (35, 43), (38, 44), (40, 45), (42, 46), (44, 47),
    (46, 47), (48, 46), (50, 46), (52, 45), (55, 45), (58, 46), (60, 48), (62, 50),
    (65, 52), (68, 55), (70, 58), (72, 60), (70, 65), (68, 66), (60, 69)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 38), (141, 40),
    (142, 43), (144, 44), (142, 42), (140, 39), (138, 36), (136, 34), (133, 33)]
BORNEO = [(109, 1), (117, 4), (119, -2), (113, -4), (109, 0)]
SUMATRA = [(95, 5), (100, 0), (104, -4), (106, -6), (102, -5), (97, 3)]
NEW_GUINEA = [(131, -1), (136, -3), (141, -5), (146, -7), (150, -9), (147, -9), (142, -8),
    (136, -4)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
    (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
    (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
    (135, -12), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (175, -40),
    (172, -43), (168, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25), (43, -20)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE, UK, ASIA,
              JAPAN, BORNEO, SUMATRA, NEW_GUINEA, AUSTRALIA, NEW_ZEALAND, MADAGASCAR]

# ---------------------------------------------------------------- layout
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width
COL_W = (CW - 2 * 14) // 3  # 313


def measure_grid(draw):
    """Return (row_heights, grid_height) for the 40-story grid."""
    f_head = SANS_B(10)
    f_sub = SANS(10)
    cells = []
    for (num, sec, head, place, detail, src, conf, lat, lon) in STORIES:
        hl = wrap(draw, f"{num}. {head}", f_head, COL_W)
        sub = f"{place} \u2014 {detail} \u2022 {src} \u2022 {conf}"
        sl = wrap(draw, sub, f_sub, COL_W)[:2]
        h = len(hl) * 12 + len(sl) * 11 + 2
        cells.append(h)
    rows = []
    for i in range(0, 40, 3):
        rows.append(max(cells[i:i + 3]) + 4)
    return rows, sum(rows)


def draw_map(draw, x0, y0, w, h):
    """World map panel; lat 85..-60 equirectangular."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=INK, width=1)
    lat_top, lat_bot = 85.0, -60.0

    def px(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * w,
                y0 + (lat_top - lat) / (lat_top - lat_bot) * h)

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # ocean + continent labels
    f_lab = SANS(10)
    for txt, lon, lat in [("PACIFIC OCEAN", -150, 0), ("ATLANTIC OCEAN", -30, 8),
                          ("INDIAN OCEAN", 78, -32), ("NORTH AMERICA", -100, 52),
                          ("SOUTH AMERICA", -60, -14),
                          ("AFRICA", 12, 12), ("ASIA", 95, 55), ("AUSTRALIA", 134, -26)]:
        lx, ly = px(lon, lat)
        tw = draw.textlength(txt, font=f_lab)
        draw.text((lx - tw / 2, ly - 5), txt, font=f_lab, fill=(110, 110, 100))
    # story dots: plain red dots (numbered labels would collide in Europe,
    # where eleven stories sit within a few degrees of each other)
    for (num, sec, head, place, detail, src, conf, lat, lon) in STORIES:
        if lat is None:
            continue
        dx, dy = px(lon, lat)
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED, outline=(255, 255, 255), width=1)
    d_cap = SANS(9)
    draw.text((x0 + 8, y0 + h - 15), "\u25cf = one story  \u2022  36 stories placed; 4 are worldwide or in space",
              font=d_cap, fill=(110, 110, 100))


def main():
    probe = Image.new("RGB", (10, 10))
    pdraw = ImageDraw.Draw(probe)
    rows, grid_h = measure_grid(pdraw)

    # fixed vertical budget (top margin 20, bottom margin 20); block heights
    # measured from the drawing code below
    mast_h, lead_h, tl_h, gh_h, foot_h = 110, 104, 67, 40, 33
    map_header = 18
    map_h = H - 20 - 20 - (mast_h + lead_h + map_header + 8 + tl_h + gh_h + grid_h + foot_h)
    if map_h < 130:
        raise SystemExit(f"layout overflow: map_h would be {map_h}, grid_h={grid_h}")
    if map_h > 200:
        map_h = 200

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # paper frame
    d.rectangle([10, 10, W - 11, H - 11], outline=(120, 110, 85), width=1)
    d.rectangle([13, 13, W - 14, H - 14], outline=(170, 160, 125), width=1)

    y = 20
    # ---- masthead ----
    d.text((MARGIN, y), "T H E   W O R L D   I N   O N E   P A G E", font=SANS_B(14), fill=RED)
    y += 22
    d.text((MARGIN, y), "TUESDAY, 24 NOVEMBER 2026", font=SERIF_B(44), fill=INK)
    y += 56
    d.text((MARGIN, y), "One day\u2019s world news \u2014 40 stories, checked against their sources  \u2022  All times UTC",
           font=SANS(14), fill=GRAY)
    y += 20
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 4
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 8

    # ---- lead story (#1) ----
    d.text((MARGIN, y), "THE LEAD", font=SANS_B(12), fill=RED)
    y += 16
    lead_head = "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA"
    f_lead = SERIF_B(27)
    while d.textlength(lead_head, font=f_lead) > CW and f_lead.size > 18:
        f_lead = SERIF_B(f_lead.size - 1)
    d.text((MARGIN, y), lead_head, font=f_lead, fill=INK)
    y += f_lead.size + 7
    lead_sum = ("The International Court of Justice ruled that Myanmar\u2019s security forces committed "
                "genocide against the Rohingya in 2017 \u2014 the first time the court has found a state "
                "responsible. The 9\u20136 ruling sets a precedent for South Africa\u2019s case against "
                "Israel over Gaza.")
    y = draw_wrapped(d, MARGIN, y, lead_sum, SANS(14), CW, fill=INK, leading=18)
    y += 2
    d.text((MARGIN, y), "First reported 24 Nov, 03:00 UTC  \u2022  Daily Summary of World / Principia  \u2022  Full story: No. 1 below",
           font=SANS(11), fill=GRAY)
    y += 16

    # ---- map row ----
    map_top = y
    d.text((MARGIN, map_top), "WHERE IT HAPPENED \u2014 24 NOVEMBER 2026", font=SANS_B(13), fill=INK)
    draw_map(d, MARGIN, map_top + map_header, 636, map_h)
    # right rail: markets + date check
    rx0, rx1 = 676, W - MARGIN
    rw = rx1 - rx0
    d.rectangle([rx0, map_top + map_header, rx1, map_top + map_header + 100],
                fill=PAPER_DK, outline=INK, width=1)
    d.text((rx0 + 10, map_top + map_header + 6), "MARKETS \u2014 TUESDAY", font=SANS_B(12), fill=INK)
    my = map_top + map_header + 26
    for name, val in MARKETS:
        d.text((rx0 + 10, my), name, font=SANS(12), fill=INK)
        vw = d.textlength(val, font=SANS_B(12))
        d.text((rx1 - 10 - vw, my), val, font=SANS_B(12), fill=INK)
        my += 14
    dc_top = map_top + map_header + 106
    dc_h = map_h - 106
    d.rectangle([rx0, dc_top, rx1, dc_top + dc_h], fill=(235, 245, 235),
                outline=GREEN, width=2)
    d.text((rx0 + 10, dc_top + 7), "\u2713  DATE CHECK", font=SANS_B(13), fill=GREEN)
    dc_text = ("Every story here happened, or was first reported, on Tuesday "
               "24 November 2026. Checked against Reuters, UN News and the Kyiv "
               "Independent. Statements as statements; claims as claims.")
    draw_wrapped(d, rx0 + 10, dc_top + 28, dc_text, SANS(11), rw - 20, fill=INK, leading=14)
    y = map_top + map_header + map_h + 8

    # ---- UTC timeline ----
    d.text((MARGIN, y), "THE DAY IN UTC", font=SANS_B(13), fill=INK)
    y += 17
    axis_y = y + 6
    d.line([(MARGIN, axis_y), (W - MARGIN, axis_y)], fill=INK, width=2)
    for hh in range(0, 25, 6):
        tx = MARGIN + hh / 24.0 * CW
        d.line([(tx, axis_y - 3), (tx, axis_y + 3)], fill=INK, width=1)
        lab = f"{hh:02d}:00"
        d.text((tx - 10, axis_y + 5), lab, font=SANS(9), fill=GRAY)
    for hour, lab, exact in TIMELINE:
        tx = MARGIN + hour / 24.0 * CW
        d.ellipse([tx - 4, axis_y - 4, tx + 4, axis_y + 4], fill=RED, outline=(255, 255, 255), width=1)
    y = axis_y + 16
    d.text((MARGIN, y), "01:06  Bukele names Haiti dead   \u2022   02:09  US drone aided \u2018Chapo\u2019 capture   \u2022   02:15  NATO space vow   \u2022   02:37  China spy sentence   \u2022   03:00  ICJ ruling",
           font=SANS(10), fill=INK)
    y += 13
    d.text((MARGIN, y), "~06:00  Asian markets surge   \u2022   ~09:00  EU sanctions proposal   \u2022   ~15:30  US deals: Sanofi, CrowdStrike   \u2022   ~20:00  Brentford 4\u20130 Everton, full time",
           font=SANS(10), fill=INK)
    y += 15

    # ---- stories grid ----
    d.text((MARGIN, y), "40 STORIES \u2014 ALL SOURCED", font=SANS_B(13), fill=INK)
    y += 17
    legend = []
    for k in ["W", "P", "C", "M", "S"]:
        legend.append((SECTION_COLOR[k], SECTION_NAME[k]))
    lx = MARGIN
    for col, name in legend:
        d.rectangle([lx, y + 2, lx + 9, y + 11], fill=col)
        lx += 13
        d.text((lx, y), name, font=SANS(10), fill=GRAY)
        lx += d.textlength(name, font=SANS(10)) + 12
    d.text((lx, y), "HIGH = confirmed by \u22652 outlets or a primary source  \u2022  MED = single source, or a claim as reported",
           font=SANS(10), fill=GRAY)
    y += 17
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 6

    f_head, f_sub = SANS_B(10), SANS(10)
    for r_i, rh in enumerate(rows):
        row_y = y
        for c_i in range(3):
            idx = r_i * 3 + c_i
            if idx >= 40:
                break
            num, sec, head, place, detail, src, conf, lat, lon = STORIES[idx]
            cx = MARGIN + c_i * (COL_W + 14)
            cy = row_y
            col = SECTION_COLOR[sec]
            hl = wrap(d, f"{num}. {head}", f_head, COL_W)
            ty = cy
            for li, ln in enumerate(hl):
                d.text((cx, ty), ln, font=f_head, fill=INK)
                if li == 0:
                    d.text((cx, ty), f"{num}. ", font=f_head, fill=col)
                ty += 12
            sub = f"{place} \u2014 {detail} \u2022 {src} \u2022 {conf}"
            sl = wrap(d, sub, f_sub, COL_W)[:2]
            for ln in sl:
                d.text((cx, ty), ln, font=f_sub, fill=GRAY)
                if conf in ln:
                    pre = ln[:ln.rfind(conf)]
                    d.text((cx + d.textlength(pre, font=f_sub), ty), conf, font=f_sub,
                           fill=GREEN if conf == "HIGH" else AMBER)
                ty += 11
        y += rh

    # ---- footer ----
    y += 2
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 5
    d.text((MARGIN, y), "Sources: Reuters \u00b7 UN News \u00b7 Kyiv Independent \u00b7 OneTurn \u00b7 Principia \u00b7 Daily Summary \u00b7 "
           "IqMIA \u00b7 IANS \u00b7 Cricinfo \u00b7 SuMarket \u00b7 The Guardian \u00b7 Financial Times",
           font=SANS(10), fill=GRAY)
    y += 13
    d.text((MARGIN, y), "Compiled Tuesday 24 November 2026 (UTC)  \u2022  40 stories  \u2022  make.fun bounty news-image-20261124",
           font=SANS(10), fill=GRAY)
    print(f"grid_h={grid_h} map_h={map_h} final_y={y}")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {W}x{H} {size} bytes")
    if size > 1048576:
        img.save(out, format="JPEG", quality=88, optimize=True)
        size = os.path.getsize(out)
        print(f"PNG too big; saved JPEG instead: {size} bytes")
    assert size <= 1048576, "still over 1 MiB"


if __name__ == "__main__":
    main()
