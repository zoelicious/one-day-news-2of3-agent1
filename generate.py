# One-day newspaper front page: Saturday 21 November 2026.
# Built from a structured story list; flat vector illustrations drawn in code.
# Output: entry.png 1024x1024.
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (248, 242, 221)
PAPER = (255, 253, 244)
INK = (26, 26, 26)
MUTED = (107, 98, 82)
RED = (179, 35, 27)
DARKRED = (140, 26, 20)
RULE = (201, 191, 164)
TEAL = (31, 122, 110)
BLUE = (43, 90, 148)
GOLD = (201, 148, 32)
GREEN = (46, 125, 62)
AMBER = (176, 124, 16)

FD = "/usr/share/fonts/truetype/"
SERIF = FD + "noto/NotoSerif-Regular.ttf"
SERIFB = FD + "noto/NotoSerif-Bold.ttf"
SERIFI = FD + "noto/NotoSerif-Italic.ttf"
SERIFBI = FD + "noto/NotoSerif-BoldItalic.ttf"
SANS = FD + "dejavu/DejaVuSans.ttf"
SANSB = FD + "dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, width, lh, max_lines=None):
    lines = wrap(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# chip: (label, short, bg, fg)
CHIPS = {
    "OFFICIAL": ("OFFICIAL", (46, 125, 62), (255, 255, 255)),
    "CONFIRMED": ("CONFIRMED", (43, 90, 148), (255, 255, 255)),
    "REPORTED": ("REPORTED", (176, 124, 16), (255, 255, 255)),
    "CLAIM": ("CLAIM", (179, 35, 27), (255, 255, 255)),
}


def chip(d, x, y, level, size=9):
    label, bg, fg = CHIPS[level]
    f = F(SANSB, size)
    w = int(d.textlength(label, font=f)) + 10
    h = size + 7
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + 5, y + 3), label, font=f, fill=fg)
    return w


def badge(d, x, y, n, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    f = F(SANSB, 13)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x - tw / 2, y - 7), t, font=f, fill=(255, 255, 255))


# ---------------- story data ----------------
# region keys: EUrope, ASia, MIddle East, AFrica, AMe ricas, OC eania, GLobal
PANELS = [
    dict(n=2, hero=True, region="ME", chip="CONFIRMED", src="Saudi coalition",
         head="THREE MISSILES DOWNED OVER RIYADH",
         body="Saudi-led coalition intercepts three Houthi missiles over Riyadh; two blasts near 02:00; no casualties.",
         ill="riyadh"),
    dict(n=1, hero=True, region="GL", chip="CONFIRMED", src="Reuters / AP",
         head="CLIMATE TALKS RUN INTO OVERTIME",
         body="Day 13 in Antalya ends with no deal as a third draft without fossil fuels splits nearly 200 nations.",
         ill="cop31"),
    dict(n=3, hero=True, region="AM", chip="OFFICIAL", src="USGS",
         head="M6.7 QUAKE SHAKES PERU",
         body="Junin and Carhuamayo jolted at 00:09 UTC, 108 km deep; no deaths and no tsunami reported.",
         ill="peru"),
    dict(n=4, region="EU", chip="CONFIRMED", src="Reuters",
         head="RUSSIA HITS KRYVYI RIH \u2014 TWICE",
         body="Double-tap strike kills 2 and injures 42 in the Ukrainian city.",
         ill="kryvyi"),
    dict(n=5, region="EU", chip="REPORTED", src="NBC",
         head="\u2018THE BRIDGE WILL NOT STAY\u2019",
         body="Zelensky tells NBC the Crimea bridge is a target; Kyiv vows it will not stand.",
         ill="bridge"),
    dict(n=6, region="ME", chip="CLAIM", src="Iran state media",
         head="IRAN CLAIMS 58TH U.S. DRONE DOWN",
         body="Tehran says it shot down an MQ-9 over Hormuz; Washington has not confirmed.",
         ill="drone"),
    dict(n=7, region="ME", chip="REPORTED", src="AP",
         head="IRAN: URANIUM STAYS AT HOME",
         body="Tehran says its stockpile stays in Iran while seeking a \u2018fair solution\u2019.",
         ill="atom"),
    dict(n=8, region="AM", chip="REPORTED", src="Reuters",
         head="TRUMP VOWS TAX ON FOREIGN DATA CENTRES",
         body="Washington: new levy promised on overseas data centres; no details given.",
         ill="servers"),
    dict(n=9, region="AS", chip="CONFIRMED", src="AP / AFP",
         head="BEIJING TO TOKYO: \u2018CORRECT\u2019 TAIWAN WORDS",
         body="China demands Japan walk back Taiwan remarks; Tokyo says its stance is unchanged.",
         ill="taiwan"),
    dict(n=10, region="OC", chip="OFFICIAL", src="Air Niugini",
         head="146 WALK AWAY FROM EMERGENCY LANDING",
         body="Air Niugini 767 lands safely in Davao after trouble in the air; all aboard safe.",
         ill="plane"),
    dict(n=11, region="OC", chip="CONFIRMED", src="Reuters",
         head="CANBERRA AND BEIJING TO TALK AI",
         body="Australia and China agree AI talks as Albanese ends an 11-day trip.",
         ill="ai"),
    dict(n=12, region="AM", chip="OFFICIAL", src="Market data",
         head="BITCOIN SLIPS BELOW $59,000",
         body="$58,983 \u2014 down 3.9% in 24 hours as crypto slides with stocks.",
         ill="bitcoin"),
    dict(n=13, region="AM", chip="OFFICIAL", src="F1",
         head="RUSSELL FASTEST IN WET VEGAS PRACTICE",
         body="1:34.041 tops a rain-hit session; Verstappen takes pole for the Grand Prix.",
         ill="f1"),
]

ALSO = [
    (14, "OC", "CONFIRMED", "Rahul 124* as India reach 344/2"),
    (15, "EU", "OFFICIAL", "BepiColombo reaches Mercury"),
    (16, "EU", "REPORTED", "NATO chief Rutte visits Warsaw"),
    (17, "AF", "REPORTED", "Bayelsa boat sinks; at least 4 dead"),
    (18, "ME", "REPORTED", "Israeli strikes on Gaza kill 6"),
    (19, "AS", "CONFIRMED", "Five of 21 wagons derail in Sejong"),
    (20, "ME", "REPORTED", "Houthis warn Jeddah is in range"),
    (21, "AM", "REPORTED", "Vance: Iran strike is Trump's call"),
    (22, "AM", "CONFIRMED", "$7.25bn Roundup verdict in Missouri"),
    (23, "AM", "CONFIRMED", "Texas execution lasts 63 minutes"),
    (24, "AM", "CONFIRMED", "Verdict in LA Palisades fire case"),
    (25, "AM", "REPORTED", "Youth climate case in Vancouver"),
    (26, "AS", "REPORTED", "Kim tours a factory in Pyongyang"),
    (27, "AS", "REPORTED", "Taipei passes its city budget"),
    (28, "AS", "REPORTED", "Bangkok plan to tackle arsenic"),
    (29, "AS", "REPORTED", "SCO forum meets in New Delhi"),
    (30, "AS", "CONFIRMED", "New sanctions hit Myanmar rulers"),
    (31, "AM", "OFFICIAL", "First U.S. measles death of 2026"),
    (32, "EU", "OFFICIAL", "Medvedev v Zverev in Turin semis"),
    (33, "EU", "CONFIRMED", "Denmark expels Russian attache"),
    (34, "OC", "OFFICIAL", "Starc 7/58 in Ashes opener, Perth"),
    (35, "AF", "CONFIRMED", "ANC polls 31%, worst since 1994"),
]

REGIONS = [
    ("Europe", "EU", (43, 90, 148)),
    ("Asia", "AS", (31, 122, 110)),
    ("Middle East", "ME", (176, 124, 16)),
    ("Africa", "AF", (201, 120, 32)),
    ("Americas", "AM", (140, 26, 20)),
    ("Oceania", "OC", (90, 90, 160)),
    ("Global", "GL", (107, 98, 82)),
]

STATS = [
    ("35", "STORIES"),
    ("7", "REGIONS"),
    ("3", "MISSILES DOWNED"),
    ("146", "SAVED IN DAVAO"),
    ("$58,983", "BITCOIN"),
    ("6.7", "PERU QUAKE"),
]

PIN_XY = {  # lon, lat per panel number
    1: (30.7, 36.9), 2: (46.7, 24.7), 3: (-75.2, -11.2), 4: (33.4, 47.9),
    5: (26.0, 52.0), 6: (56.5, 26.5), 7: (51.4, 38.8), 8: (-77.0, 38.9),
    9: (116.4, 39.9), 10: (125.6, 7.1), 11: (149.1, -35.3), 12: (-74.0, 40.7),
    13: (-115.1, 36.2),
}


# ---------------- flat illustrations ----------------
def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 226))
    cx, cy, r = x + w * 0.32, y + h * 0.52, min(w, h) * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(31, 122, 110))
    d.ellipse([cx - r * 0.55, cy - r * 0.5, cx - r * 0.1, cy - r * 0.05], fill=(46, 160, 90))
    d.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.55], fill=(46, 160, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(255, 255, 255), width=2)
    d.line([x + w * 0.55, y + h * 0.75, x + w * 0.62, y + h * 0.35, x + w * 0.72, y + h * 0.75], fill=(179, 35, 27), width=3)
    d.ellipse([x + w * 0.66, y + h * 0.12, x + w * 0.80, y + h * 0.26], fill=(201, 148, 32))
    for i, xx in enumerate([0.60, 0.70, 0.80]):
        d.line([x + w * xx, y + h * 0.30, x + w * xx, y + h * 0.42], fill=(201, 148, 32), width=2)
    d.text((x + w * 0.56, y + h * 0.80), "DAY 13 \u00b7 NO DEAL", font=F(SANSB, 11), fill=(140, 26, 20))


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 38, 66))
    for sx, sy in [(0.12, 0.18), (0.30, 0.10), (0.55, 0.22), (0.75, 0.12), (0.90, 0.25), (0.45, 0.08)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(16, 24, 44))
    for bx, bh in [(0.05, 0.28), (0.18, 0.40), (0.34, 0.24), (0.50, 0.44), (0.68, 0.30), (0.82, 0.38)]:
        d.rectangle([x + w * bx, y + h * (1.0 - bh) - h * 0.0, x + w * bx + w * 0.10, y + h], fill=(10, 16, 32))
    for (ax, ay, bx, by) in [(0.08, 0.55, 0.42, 0.22), (0.30, 0.62, 0.62, 0.26), (0.55, 0.60, 0.88, 0.24)]:
        mx, my = (ax + bx) / 2, min(ay, by) - 0.18
        pts = []
        for t in [0, 0.25, 0.5, 0.75, 1.0]:
            px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * mx + t ** 2 * bx
            py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * my + t ** 2 * by
            pts.append((x + w * px, y + h * py))
        d.line(pts, fill=(255, 190, 60), width=3)
        ex, ey = x + w * bx, y + h * by
        for k in range(6):
            ang = k * math.pi / 3
            d.line([ex, ey, ex + 10 * math.cos(ang), ey + 10 * math.sin(ang)], fill=(255, 220, 120), width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 240, 180))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 190))
    d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.35), (x + w * 0.5, y + h), (x + w * 0.75, y + h * 0.45), (x + w, y + h)], fill=(120, 110, 88))
    d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.35), (x + w * 0.5, y + h)], fill=(96, 88, 70))
    d.line([x + w * 0.08, y + h * 0.88, x + w * 0.28, y + h * 0.70, x + w * 0.42, y + h * 0.90, x + w * 0.60, y + h * 0.68, x + w * 0.78, y + h * 0.88, x + w * 0.95, y + h * 0.72], fill=(140, 26, 20), width=3)
    d.rectangle([x + w * 0.62, y + h * 0.10, x + w * 0.95, y + h * 0.30], fill=(255, 253, 244))
    d.text((x + w * 0.65, y + h * 0.13), "M 6.7", font=F(SANSB, 13), fill=(140, 26, 20))
    d.text((x + w * 0.65, y + h * 0.13 + 16), "108 km deep", font=F(SANS, 9), fill=(26, 26, 26))


def ill_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 205))
    d.polygon([(x + w * 0.10, y + h), (x + w * 0.10, y + h * 0.42), (x + w * 0.20, y + h * 0.30), (x + w * 0.30, y + h * 0.44), (x + w * 0.42, y + h * 0.38), (x + w * 0.42, y + h)], fill=(90, 84, 74))
    d.rectangle([x + w * 0.55, y + h * 0.58, x + w * 0.85, y + h], fill=(70, 64, 56))
    for wy in [0.52, 0.66, 0.80]:
        for wx in [0.16, 0.28]:
            d.rectangle([x + w * wx, y + h * wy, x + w * wx + 8, y + h * wy + 7], fill=(255, 220, 120))
    d.ellipse([x + w * 0.55, y + h * 0.10, x + w * 0.75, y + h * 0.30], fill=(160, 150, 135))
    d.ellipse([x + w * 0.68, y + h * 0.05, x + w * 0.90, y + h * 0.28], fill=(140, 130, 115))


def ill_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 226, 238))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(43, 90, 148))
    d.line([x, y + h * 0.72, x + w, y + h * 0.72], fill=(255, 255, 255), width=2)
    d.line([x + w * 0.10, y + h * 0.55, x + w * 0.90, y + h * 0.55], fill=(60, 60, 60), width=4)
    for px in [0.18, 0.38, 0.58, 0.78]:
        d.line([x + w * px, y + h * 0.55, x + w * px, y + h * 0.72], fill=(60, 60, 60), width=3)
    d.line([x + w * 0.10, y + h * 0.55, x + w * 0.50, y + h * 0.20], fill=(179, 35, 27), width=2)
    d.line([x + w * 0.90, y + h * 0.55, x + w * 0.50, y + h * 0.20], fill=(179, 35, 27), width=2)
    d.polygon([(x + w * 0.50, y + h * 0.20), (x + w * 0.50, y + h * 0.34), (x + w * 0.62, y + h * 0.27)], fill=(43, 90, 148))
    d.polygon([(x + w * 0.50, y + h * 0.34), (x + w * 0.50, y + h * 0.48), (x + w * 0.62, y + h * 0.41)], fill=(201, 148, 32))


def ill_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 228, 236))
    cx, cy = x + w * 0.5, y + h * 0.5
    for r in [10, 17, 24]:
        d.arc([cx - r, cy - r, cx + r, cy + r], -60, 60, fill=(43, 90, 148), width=2)
    d.ellipse([cx - 26, cy - 5, cx + 26, cy + 5], fill=(60, 60, 60))
    d.rectangle([cx - 4, cy - 12, cx + 4, cy + 12], fill=(60, 60, 60))
    d.ellipse([cx + 26, cy - 3, cx + 44, cy + 3], fill=(90, 90, 90))
    d.text((x + w * 0.06, y + h * 0.06), "CLAIM No. 58", font=F(SANSB, 10), fill=(179, 35, 27))


def ill_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 222))
    cx, cy = x + w * 0.5, y + h * 0.52
    rx, ry = w * 0.34, h * 0.22
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(31, 122, 110), width=2)
    d.ellipse([cx - w * 0.10, cy - h * 0.40, cx + w * 0.10, cy + h * 0.40], outline=(31, 122, 110), width=2)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(179, 35, 27))
    d.ellipse([cx + rx - 4, cy - 4, cx + rx + 4, cy + 4], fill=(43, 90, 148))
    d.ellipse([cx - rx * 0.5 - 4, cy + ry * 0.85 - 4, cx - rx * 0.5 + 4, cy + ry * 0.85 + 4], fill=(43, 90, 148))


def ill_servers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 226, 236))
    for i, sx in enumerate([0.10, 0.38, 0.66]):
        d.rectangle([x + w * sx, y + h * 0.18, x + w * sx + w * 0.22, y + h * 0.92], fill=(60, 66, 80))
        for j in range(4):
            yy = y + h * (0.26 + j * 0.16)
            d.rectangle([x + w * sx + 5, yy, x + w * sx + w * 0.22 - 5, yy + 8], fill=(90, 96, 112))
            d.ellipse([x + w * sx + w * 0.22 - 12, yy + 2, x + w * sx + w * 0.22 - 6, yy + 8], fill=(46, 200, 120))
    d.text((x + w * 0.06, y + h * 0.04), "TAX ?", font=F(SANSB, 12), fill=(140, 26, 20))


def ill_taiwan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 222))
    d.rectangle([x + w * 0.08, y + h * 0.18, x + w * 0.44, y + h * 0.82], fill=(179, 35, 27))
    d.ellipse([x + w * 0.16, y + h * 0.32, x + w * 0.36, y + h * 0.52], fill=(255, 255, 255))
    d.rectangle([x + w * 0.56, y + h * 0.18, x + w * 0.92, y + h * 0.82], fill=(255, 255, 255), outline=(179, 35, 27), width=2)
    d.ellipse([x + w * 0.66, y + h * 0.32, x + w * 0.82, y + h * 0.48], fill=(179, 35, 27))
    d.text((x + w * 0.60, y + h * 0.58), "TOKYO", font=F(SANSB, 10), fill=(26, 26, 26))
    d.text((x + w * 0.12, y + h * 0.58), "BEIJING", font=F(SANSB, 10), fill=(255, 255, 255))


def ill_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    d.ellipse([x + w * 0.08, y + h * 0.10, x + w * 0.28, y + h * 0.30], fill=(255, 255, 255))
    d.ellipse([x + w * 0.55, y + h * 0.18, x + w * 0.80, y + h * 0.42], fill=(255, 255, 255))
    d.polygon([(x + w * 0.15, y + h * 0.62), (x + w * 0.75, y + h * 0.50), (x + w * 0.92, y + h * 0.55), (x + w * 0.80, y + h * 0.62), (x + w * 0.30, y + h * 0.72)], fill=(43, 90, 148))
    d.polygon([(x + w * 0.30, y + h * 0.55), (x + w * 0.45, y + h * 0.40), (x + w * 0.52, y + h * 0.55)], fill=(31, 122, 110))
    d.line([x, y + h * 0.88, x + w, y + h * 0.88], fill=(60, 60, 60), width=3)
    for i in range(6):
        xx = x + w * (0.08 + i * 0.16)
        d.line([xx, y + h * 0.88, xx + 8, y + h * 0.88], fill=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.84, y + h * 0.06, x + w * 0.97, y + h * 0.19], fill=(46, 125, 62))
    d.text((x + w * 0.875, y + h * 0.075), "\u2713", font=F(SANSB, 11), fill=(255, 255, 255))


def ill_ai(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 230, 244))
    d.rounded_rectangle([x + w * 0.30, y + h * 0.18, x + w * 0.70, y + h * 0.78], radius=8, fill=(90, 90, 160))
    d.ellipse([x + w * 0.40, y + h * 0.34, x + w * 0.47, y + h * 0.44], fill=(255, 255, 255))
    d.ellipse([x + w * 0.53, y + h * 0.34, x + w * 0.60, y + h * 0.44], fill=(255, 255, 255))
    d.line([x + w * 0.42, y + h * 0.58, x + w * 0.58, y + h * 0.58], fill=(255, 255, 255), width=3)
    d.rectangle([x + w * 0.06, y + h * 0.70, x + w * 0.24, y + h * 0.86], fill=(43, 90, 148))
    d.rectangle([x + w * 0.76, y + h * 0.70, x + w * 0.94, y + h * 0.86], fill=(179, 35, 27))
    d.text((x + w * 0.08, y + h * 0.72), "AU", font=F(SANSB, 9), fill=(255, 255, 255))
    d.text((x + w * 0.78, y + h * 0.72), "CN", font=F(SANSB, 9), fill=(255, 255, 255))


def ill_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 200))
    cx, cy, r = x + w * 0.32, y + h * 0.50, min(w, h) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(201, 148, 32), outline=(140, 100, 20), width=2)
    d.text((cx - 7, cy - 12), "B", font=F(SANSB, 20), fill=(255, 255, 255))
    d.line([cx - 2, cy - 14, cx - 2, cy + 13], fill=(255, 255, 255), width=2)
    d.line([cx + 3, cy - 14, cx + 3, cy + 13], fill=(255, 255, 255), width=2)
    pts = [(0.52, 0.28), (0.64, 0.45), (0.74, 0.36), (0.86, 0.60), (0.95, 0.72)]
    for i in range(len(pts) - 1):
        d.line([x + w * pts[i][0], y + h * pts[i][1], x + w * pts[i + 1][0], y + h * pts[i + 1][1]], fill=(179, 35, 27), width=3)
    d.polygon([(x + w * 0.95, y + h * 0.72), (x + w * 0.89, y + h * 0.66), (x + w * 0.95, y + h * 0.60)], fill=(179, 35, 27))
    d.text((x + w * 0.52, y + h * 0.78), "-3.9%", font=F(SANSB, 11), fill=(179, 35, 27))


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 228, 232))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(60, 60, 66))
    d.line([x, y + h * 0.70, x + w, y + h * 0.70], fill=(255, 255, 255), width=2)
    d.polygon([(x + w * 0.12, y + h * 0.55), (x + w * 0.30, y + h * 0.42), (x + w * 0.62, y + h * 0.42), (x + w * 0.78, y + h * 0.55), (x + w * 0.72, y + h * 0.62), (x + w * 0.18, y + h * 0.62)], fill=(179, 35, 27))
    d.ellipse([x + w * 0.24, y + h * 0.58, x + w * 0.34, y + h * 0.68], fill=(26, 26, 26))
    d.ellipse([x + w * 0.62, y + h * 0.58, x + w * 0.72, y + h * 0.68], fill=(26, 26, 26))
    for i in range(4):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + w * (0.84 + i * 0.035), y + h * (0.12 + j * 0.09), x + w * (0.875 + i * 0.035), y + h * (0.21 + j * 0.09)], fill=(26, 26, 26))
    d.line([x + w * 0.84, y + h * 0.12, x + w * 0.84, y + h * 0.34], fill=(26, 26, 26), width=2)
    d.text((x + w * 0.06, y + h * 0.08), "1:34.041", font=F(SANSB, 12), fill=(26, 26, 26))


ILLS = {"cop31": ill_cop31, "riyadh": ill_riyadh, "peru": ill_peru, "kryvyi": ill_kryvyi,
        "bridge": ill_bridge, "drone": ill_drone, "atom": ill_atom, "servers": ill_servers,
        "taiwan": ill_taiwan, "plane": ill_plane, "ai": ill_ai, "bitcoin": ill_bitcoin, "f1": ill_f1}


# ---------------- world map ----------------
LAND = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-100, 20), (-105, 23), (-110, 28), (-115, 32), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 5), (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -40), (-72, -20), (-78, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (28, -33), (18, -35), (12, -18), (8, -2), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68), (55, 69), (70, 72), (80, 73), (100, 77), (110, 74), (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 32), (115, 22), (108, 18), (105, 10), (100, 8), (98, 12), (95, 16), (90, 22), (85, 20), (80, 15), (77, 8), (72, 20), (66, 25), (60, 25), (57, 26), (52, 28), (48, 29), (44, 29), (40, 31), (36, 36), (30, 36), (26, 38), (22, 37), (18, 40), (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32), (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-40, 80), (-55, 76), (-58, 70), (-52, 64)],
    [(18, -17), (20, -25), (16, -28), (14, -22)],
    [(95, 5), (98, 8), (100, 5), (102, 2), (104, -2), (100, -5), (97, 0)],
    [(105, -6), (110, -7), (114, -8), (112, -9), (107, -8)],
    [(130, -2), (136, -3), (141, -4), (138, -8), (132, -7)],
    [(122, 24), (121, 22), (120, 23), (121, 25)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 42), (143, 44), (140, 44), (138, 40), (136, 37), (133, 35), (130, 33)],
    [(-3, 54), (-5, 56), (-2, 58), (0, 53), (1, 51), (-4, 50)],
    [(167, -41), (170, -43), (174, -39), (177, -38), (174, -41), (168, -45)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 236, 240))
    for lon in range(-150, 181, 30):
        px = x + (lon + 180) / 360 * w
        d.line([px, y, px, y + h], fill=(210, 220, 226), width=1)
    for lat in [-60, -30, 0, 30, 60]:
        py = y + (90 - lat) / 180 * h
        d.line([x, py, x + w, py], fill=(210, 220, 226), width=1)
    for poly in LAND:
        pts = [(x + (lo + 180) / 360 * w, y + (90 - la) / 180 * h) for lo, la in poly]
        d.polygon(pts, fill=(168, 190, 158), outline=(120, 145, 115))
    for n, (lo, la) in PIN_XY.items():
        px = x + (lo + 180) / 360 * w
        py = y + (90 - la) / 180 * h
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=2)
        f = F(SANSB, 10)
        t = str(n)
        d.text((px - d.textlength(t, font=f) / 2, py - 6), t, font=f, fill=(255, 255, 255))


# ---------------- panels ----------------
def hero_panel(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=RULE, width=1)
    ih = 88
    ILLS[s["ill"]](d, x + 1, y + 1, w - 2, ih)
    badge(d, x + 20, y + ih + 16, s["n"])
    tx = x + 38
    hy = y + ih + 6
    hy = para(d, tx, hy, s["head"], F(SERIFB, 17), INK, w - 48, 20, max_lines=2)
    hy = para(d, x + 10, hy + 3, s["body"], F(SERIF, 12), (58, 58, 58), w - 20, 15, max_lines=2)
    chip(d, x + 10, y + h - 20, s["chip"])
    sf = F(SERIFI, 10)
    d.text((x + 10 + chip_w(s["chip"]) + 8, y + h - 18), s["src"], font=sf, fill=MUTED)


def chip_w(level):
    f = F(SANSB, 9)
    return int(f.getlength(CHIPS[level][0])) + 10


def small_panel(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=RULE, width=1)
    ih = 48
    ILLS[s["ill"]](d, x + 1, y + 1, w - 2, ih)
    badge(d, x + 16, y + ih + 13, s["n"], r=10)
    tx = x + 31
    hy = y + ih + 4
    hy = para(d, tx, hy, s["head"], F(SERIFB, 11.5), INK, w - 38, 13.5, max_lines=2)
    hy = para(d, x + 8, hy + 2, s["body"], F(SERIF, 10), (58, 58, 58), w - 16, 12.5, max_lines=3)
    chip(d, x + 8, y + h - 17, s["chip"], size=8)


# ---------------- build ----------------
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 22
    CW = W - 2 * MX  # 980

    # masthead
    d.line([MX, 12, W - MX, 12], fill=INK, width=2)
    t = "THE WORLD IN ONE DAY"
    f = F(SERIFB, 40)
    d.text(((W - d.textlength(t, font=f)) / 2, 16), t, font=f, fill=RED)
    t2 = "Saturday 21 November 2026"
    f2 = F(SERIFB, 44)
    d.text(((W - d.textlength(t2, font=f2)) / 2, 58), t2, font=f2, fill=INK)
    sub = "COP31 talks run into overtime  \u00b7  Three missiles downed over Riyadh  \u00b7  Peru shaken by M6.7 quake"
    fs = F(SERIFI, 15)
    d.text(((W - d.textlength(sub, font=fs)) / 2, 106), sub, font=fs, fill=MUTED)
    d.line([MX, 128, W - MX, 128], fill=INK, width=1)

    # stats strip
    y0 = 134
    bw = CW / 6
    for i, (num, lab) in enumerate(STATS):
        cx = MX + bw * i + bw / 2
        fn = F(SERIFB, 20)
        d.text((cx - d.textlength(num, font=fn) / 2, y0), num, font=fn, fill=RED)
        fl = F(SANSB, 8.5)
        d.text((cx - d.textlength(lab, font=fl) / 2, y0 + 24), lab, font=fl, fill=MUTED)
        if i:
            d.line([MX + bw * i, y0 + 2, MX + bw * i, y0 + 34], fill=RULE, width=1)
    d.line([MX, 170, W - MX, 170], fill=INK, width=1)

    # region bar (counts computed from data; must sum to 35)
    counts = {}
    for s in PANELS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for n, r, c, _t in ALSO:
        counts[r] = counts.get(r, 0) + 1
    total = sum(counts.values())
    assert total == 35, total
    yb = 178
    bx, bw_tot = MX, CW
    xcur = bx
    for name, key, col in REGIONS:
        c = counts.get(key, 0)
        seg = bw_tot * c / total
        d.rectangle([xcur, yb, xcur + seg, yb + 14], fill=col)
        xcur += seg
    d.rectangle([bx, yb, bx + bw_tot, yb + 14], outline=INK, width=1)
    fl = F(SANSB, 9)
    lab_y = yb + 18
    lx = MX
    for name, key, col in REGIONS:
        c = counts.get(key, 0)
        d.rectangle([lx, lab_y + 1, lx + 9, lab_y + 10], fill=col)
        t = "%s %d" % (name, c)
        d.text((lx + 12, lab_y), t, font=fl, fill=INK)
        lx += 12 + d.textlength(t, font=fl) + 16
    d.text((W - MX - d.textlength("35 STORIES IN ALL", font=fl), lab_y), "35 STORIES IN ALL", font=fl, fill=RED)

    # hero row: Riyadh (#2), COP31 (#1), Peru (#3)
    hy, hh = 214, 190
    hw = (CW - 2 * 11) / 3
    order = [PANELS[0], PANELS[1], PANELS[2]]
    for i, s in enumerate(order):
        hero_panel(d, MX + i * (hw + 11), hy, hw, hh, s)

    # small panels: 2 rows x 5
    sy1, sh = 412, 136
    sw = (CW - 4 * 10) / 5
    smalls = PANELS[3:]
    for i, s in enumerate(smalls):
        row, col = divmod(i, 5)
        small_panel(d, MX + col * (sw + 10), sy1 + row * (sh + 8), sw, sh, s)

    # bottom section
    by = 700
    bh = 228
    # map
    mw = 330
    d.rectangle([MX, by, MX + mw, by + bh], fill=PAPER, outline=RULE, width=1)
    fm = F(SANSB, 11)
    d.text((MX + 10, by + 6), "WHERE IT HAPPENED", font=fm, fill=INK)
    d.text((MX + mw - 10 - d.textlength("pins 1\u201313", font=F(SERIFI, 10)), by + 7), "pins 1\u201313", font=F(SERIFI, 10), fill=MUTED)
    draw_map(d, MX + 6, by + 24, mw - 12, bh - 30)

    # ALSO list (2 columns, one line per story)
    ax = MX + mw + 12
    aw = 426
    d.rectangle([ax, by, ax + aw, by + bh], fill=PAPER, outline=RULE, width=1)
    d.text((ax + 10, by + 6), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES", font=fm, fill=INK)
    d.line([ax + 10, by + 24, ax + aw - 10, by + 24], fill=RULE, width=1)
    fa = F(SERIF, 9.5)
    fn = F(SANSB, 9)
    col_w = (aw - 20 - 8) / 2
    for i, (n, r, clev, txt) in enumerate(ALSO):
        col, row = divmod(i, 11)
        lx = ax + 10 + col * (col_w + 8)
        ly = by + 30 + row * 18
        d.text((lx, ly), "%d." % n, font=fn, fill=RED)
        _, bg, _ = CHIPS[clev]
        d.rectangle([lx + 20, ly + 3, lx + 26, ly + 9], fill=bg)
        d.text((lx + 30, ly), txt, font=fa, fill=INK)

    # THE VERDICT sidebar
    vx = ax + aw + 12
    vw = W - MX - vx
    d.rectangle([vx, by, vx + vw, by + bh], fill=(255, 250, 235), outline=RED, width=2)
    d.text((vx + 10, by + 6), "THE VERDICT", font=F(SERIFB, 13), fill=RED)
    d.line([vx + 10, by + 26, vx + vw - 10, by + 26], fill=RED, width=1)
    verdict = ("Climate talks stalled while missiles flew. The day's deadliest numbers: Kryvyi Rih "
               "(2 killed, 42 hurt) and Gaza (6 killed). Markets slid as Bitcoin fell below $59,000 \u2014 "
               "but 146 people walked away from a runway in Davao.")
    para(d, vx + 10, by + 32, verdict, F(SERIF, 11.5), INK, vw - 20, 15)
    d.text((vx + 10, by + bh - 22), "Checked story by story.", font=F(SERIFI, 10), fill=MUTED)
    d.text((vx + 10, by + bh - 36), "See HOW WE CHECKED below.", font=F(SERIFI, 10), fill=MUTED)

    # DATE CHECK
    dy = 936
    dh = 48
    d.rectangle([MX, dy, W - MX, dy + dh], fill=(255, 250, 235), outline=RED, width=2)
    d.text((MX + 10, dy + 5), "DATE CHECK", font=F(SERIFB, 11), fill=RED)
    dc = ("Left out on purpose \u2014 they belong to other days: Wall Street's slide into correction; Russia's strike on a Kyiv bridge; "
          "a missile landing in Poland; the UK\u2013EU reset deal; Cyclone Akvan's landfall (all Friday 20 Nov); Voyager 1 passing "
          "one light-day (18 Nov). Not yet confirmed when drawn: BepiColombo's Mercury orbit insertion; the final COP31 text.")
    para(d, MX + 96, dy + 5, dc, F(SERIF, 10.5), INK, W - MX - 106, 13.5, max_lines=4)

    # footer
    fy = 990
    d.line([MX, fy, W - MX, fy], fill=INK, width=1)
    d.text((MX, fy + 5), "Every story here happened, or was first reported, on Saturday 21 November 2026.",
           font=F(SERIFI, 11), fill=INK)
    leg = "HOW WE CHECKED:  OFFICIAL = authority statement  \u00b7  CONFIRMED = 2+ outlets  \u00b7  REPORTED = one outlet  \u00b7  CLAIM = unverified claim"
    d.text((MX, fy + 20), leg, font=F(SANS, 9), fill=MUTED)
    d.text((MX, fy + 20 + 0), "", font=F(SANS, 9), fill=MUTED)
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    print("saved entry.png", im.size)
