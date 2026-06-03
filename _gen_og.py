#!/usr/bin/env python3
"""
Generate og-image.png and twitter-image.png for APICalculators.com
Design: "Terminal Precision" — Bloomberg Terminal meets Devtool
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys

# ── Brand palette ─────────────────────────────────────────────────────────────
BG     = (10,  12,  16)
LIME   = (184, 255, 46)
CYAN   = (77,  214, 255)
TEXT   = (232, 237, 241)
MUTED  = (139, 151, 164)
SURF   = (18,  22,  29)
BORDER = (29,  37,  48)

W, H = 1200, 630

# ── Font loader ───────────────────────────────────────────────────────────────
FDIR = r'C:\Windows\Fonts'
FMAP = {
    'black': 'ariblk.ttf',
    'bold':  'arialbd.ttf',
    'reg':   'arial.ttf',
    'mono':  'consola.ttf',
    'monob': 'consolab.ttf',
}
def F(name, size):
    try:    return ImageFont.truetype(os.path.join(FDIR, FMAP[name]), size)
    except: return ImageFont.load_default()

# ── Helpers ───────────────────────────────────────────────────────────────────
def new_canvas():
    return Image.new('RGBA', (W, H), (*BG, 255))

def glow_layer(cx, cy, r, color, alpha=85):
    g = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(g)
    for i in range(10, 0, -1):
        ri = int(r * i / 10)
        ai = int(alpha * (10-i) / 10 * 0.9)
        d.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(*color, ai))
    return g.filter(ImageFilter.GaussianBlur(r // 2.8))

def add_grid(img, sp=54, a=16):
    ov = Image.new('RGBA', (W, H), (0,0,0,0))
    d  = ImageDraw.Draw(ov)
    for x in range(0, W+sp, sp): d.line([(x,0),(x,H)], fill=(255,255,255,a))
    for y in range(0, H+sp, sp): d.line([(0,y),(W,y)], fill=(255,255,255,a))
    return Image.alpha_composite(img, ov)

def tw(draw, txt, fnt):
    bb = draw.textbbox((0,0), txt, font=fnt)
    return bb[2]-bb[0]

def rr(draw, box, radius=10, fill=None, outline=None, width=1):
    """Rounded rectangle helper."""
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def logo_mark(draw, x, y, size=38):
    """Draw lime-green square logo mark with 'A'."""
    rr(draw, [x, y, x+size, y+size], radius=8, fill=LIME)
    draw.text((x+size//2-9, y+size//2-13), "A", font=F('black', 24), fill=(*BG,255))

def draw_pill(draw, x, y, text, fnt, bg=(184,255,46,40), fg=LIME):
    tw_ = tw(draw, text, fnt)
    pad = 8
    rr(draw, [x, y, x+tw_+pad*2, y+22], radius=6, fill=bg)
    draw.text((x+pad, y+3), text, font=fnt, fill=fg)

# ─────────────────────────────────────────────────────────────────────────────
# OG IMAGE  1200 × 630
# ─────────────────────────────────────────────────────────────────────────────
def make_og():
    img = new_canvas()

    # Glows
    img = Image.alpha_composite(img, glow_layer(W-40,  55,  360, LIME, 80))
    img = Image.alpha_composite(img, glow_layer(60,    H-40, 180, CYAN, 45))

    # Grid
    img = add_grid(img, 54, 16)
    draw = ImageDraw.Draw(img)

    # ── Top accent lines
    draw.line([(0,0),(W,0)], fill=LIME, width=2)
    draw.line([(0,1),(W,1)], fill=(*LIME, 60), width=1)

    # ── Logo
    LX, LY = 48, 29
    logo_mark(draw, LX, LY, 38)
    draw.text((LX+50, LY+7),    "API",          font=F('black',22), fill=TEXT)
    draw.text((LX+50+46, LY+7), "Calculators",  font=F('bold', 22), fill=LIME)

    # ── Status badge (top-right)
    badge_font = F('mono', 12)
    badge = "· 2026 PRICING EDITION"
    bw = tw(draw, badge, badge_font)
    draw.text((W-bw-48, 39), badge, font=badge_font, fill=MUTED)
    draw.ellipse([W-bw-64, 43, W-bw-57, 50], fill=(*LIME,200))

    # ── Headline ─────────────────────────────────────────────────────────
    Y0   = 128
    f90  = F('black', 90)
    f78  = F('black', 78)

    # Line 1  "Know your"
    draw.text((48, Y0), "Know your", font=f90, fill=TEXT)

    # Line 2  "infra costs"  ← lime + underline glow
    IC = "infra costs"
    IC_Y = Y0 + 102
    draw.text((48, IC_Y), IC, font=f90, fill=LIME)
    icw = tw(draw, IC, f90)
    # underline
    draw.line([(48, IC_Y+96),(48+icw, IC_Y+96)], fill=(*LIME, 90), width=2)

    # Line 3  "before the invoice does."
    draw.text((48, IC_Y+104), "before the invoice does.", font=f78, fill=TEXT)

    # ── Divider
    HR_Y = Y0 + 302
    draw.line([(48, HR_Y),(560, HR_Y)], fill=BORDER, width=1)

    # ── Sub-line
    sub_font = F('reg', 19)
    draw.text((48, HR_Y+13), "No signup  ·  No server  ·  Prices from official docs",
              font=sub_font, fill=MUTED)

    # ── 4 Calculator Cards ───────────────────────────────────────────────
    cards = [("LLM Tokens","T"), ("Vector DB","V"), ("Image Gen","I"), ("Payment","$")]
    CW, CH = 240, 54
    CY     = H - CH - 44
    GAP    = (W - 2*48 - 4*CW) // 3
    f_cl   = F('bold', 14)
    f_ca   = F('monob', 13)

    for i, (lbl, acc) in enumerate(cards):
        cx = 48 + i*(CW+GAP)
        # Card bg
        rr(draw, [cx,CY,cx+CW,CY+CH], radius=9, fill=SURF, outline=BORDER, width=1)
        # Accent chip
        rr(draw, [cx+10, CY+CH//2-10, cx+32, CY+CH//2+10], radius=5, fill=(*LIME,55))
        draw.text((cx+14, CY+CH//2-10), acc, font=f_ca, fill=LIME)
        # Label
        draw.text((cx+44, CY+(CH-16)//2), lbl, font=f_cl, fill=TEXT)
        # Subtle right border between cards
        if i < 3:
            draw.line([(cx+CW+GAP//2, CY+8),(cx+CW+GAP//2, CY+CH-8)],
                      fill=BORDER, width=1)

    # ── Domain (bottom-right)
    dom_font = F('mono', 13)
    dom = "apicalculators.com"
    dw  = tw(draw, dom, dom_font)
    draw.text((W-dw-48, H-26), dom, font=dom_font, fill=MUTED)

    return img.convert('RGB')


# ─────────────────────────────────────────────────────────────────────────────
# TWITTER IMAGE  1200 × 630
# ─────────────────────────────────────────────────────────────────────────────
def make_twitter():
    img = new_canvas()

    # Glows — different placement for visual variety
    img = Image.alpha_composite(img, glow_layer(100,   H//2, 300, LIME, 70))
    img = Image.alpha_composite(img, glow_layer(W,     H,    240, CYAN, 40))
    img = Image.alpha_composite(img, glow_layer(W-100, 80,   180, LIME, 35))

    img = add_grid(img, 54, 14)
    draw = ImageDraw.Draw(img)

    # ── Accent bars
    draw.rectangle([0,0,3,H], fill=LIME)                    # left bar
    draw.line([(0,0),(W,0)], fill=LIME, width=2)            # top line
    draw.line([(0,H-1),(W,H-1)], fill=(*BORDER,180), width=1)  # bottom

    # ── Logo
    LX, LY = 48, 30
    logo_mark(draw, LX, LY, 36)
    draw.text((LX+48, LY+6),    "API",         font=F('black',21), fill=TEXT)
    draw.text((LX+48+43, LY+6), "Calculators", font=F('bold', 21), fill=LIME)

    # ── Tag right
    tag = "FREE · OPEN · 100% BROWSER"
    tf  = F('mono', 12)
    tw_ = tw(draw, tag, tf)
    draw.text((W-tw_-48, 39), tag, font=tf, fill=MUTED)

    # ── LEFT: large headline ─────────────────────────────────────────────
    Y0  = 108
    f84 = F('black', 84)
    f68 = F('black', 68)

    draw.text((48, Y0),       "Know your",      font=f84, fill=TEXT)
    draw.text((48, Y0+92),    "infra costs",    font=f84, fill=LIME)
    draw.text((48, Y0+184),   "before the",     font=f68, fill=TEXT)
    draw.text((48, Y0+258),   "invoice does.",  font=f68, fill=TEXT)

    # ── RIGHT: stat panel ────────────────────────────────────────────────
    RX    = 730
    stats = [
        ("12+",   "API providers",  LIME),
        ("10K+",  "developers",     TEXT),
        ("$0",    "to use",         LIME),
        ("100%",  "browser-based",  TEXT),
    ]
    f_val = F('black', 54)
    f_lbl = F('reg',   15)

    for i, (val, lbl, col) in enumerate(stats):
        sy = Y0 + i * 106
        draw.text((RX, sy),    val, font=f_val, fill=col)
        draw.text((RX, sy+60), lbl, font=f_lbl, fill=MUTED)
        if i < 3:
            draw.line([(RX, sy+90),(RX+420, sy+90)], fill=BORDER, width=1)

    # ── Bottom bar
    draw.line([(0, H-66),(W, H-66)], fill=BORDER, width=1)

    cats_font = F('bold', 14)
    cats = ["LLM Tokens", "Vector DB", "Image Gen", "Payment Fees"]
    cx2  = 48
    for cat in cats:
        draw.ellipse([cx2, H-44, cx2+7, H-37], fill=(*LIME,160))
        cx2 += 15
        draw.text((cx2, H-50), cat, font=cats_font, fill=MUTED)
        cx2 += tw(draw, cat, cats_font) + 28

    dom_font = F('mono', 13)
    dom      = "apicalculators.com"
    dw       = tw(draw, dom, dom_font)
    draw.text((W-dw-48, H-50), dom, font=dom_font, fill=MUTED)

    return img.convert('RGB')


# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────
OUT = r'C:\Users\muham\Desktop\APICalculators'

og = make_og()
og.save(os.path.join(OUT, 'og-image.png'), 'PNG', optimize=True)
print("OK og-image.png saved")

tw_img = make_twitter()
tw_img.save(os.path.join(OUT, 'twitter-image.png'), 'PNG', optimize=True)
print("OK twitter-image.png saved")
