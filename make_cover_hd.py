#!/usr/bin/env python3
"""高分辨率封面 - 2x + Noto Sans CJK SC + 椰子配色"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 2400, 1256
random.seed(42)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# === 椰子配色方案 ===
BG_TOP = (255, 248, 240)
BG_BOT = (242, 232, 215)
TEXT_MAIN = (61, 43, 31)
TEXT_SUB = (115, 88, 62)
TEXT_BOTTOM = (155, 125, 95)
ACCENT = (193, 127, 78)
ACCENT_LIGHT = (210, 180, 140)
ACCENT_GLOW = (230, 210, 180)
SHADOW = (0, 0, 0, 20)

# === WARM CREAM GRADIENT (2x smooth) ===
for y in range(H):
    r = y / H
    rc = int(BG_TOP[0] + (BG_BOT[0]-BG_TOP[0]) * r)
    gc = int(BG_TOP[1] + (BG_BOT[1]-BG_TOP[1]) * r)
    bc = int(BG_TOP[2] + (BG_BOT[2]-BG_TOP[2]) * r)
    draw.rectangle([0, y, W, y], fill=(rc, gc, bc, 255))

# === SUBTLE STRUCTURED TEXTURE ===
# Small dots scattered
for _ in range(400):
    x, y = random.randint(0, W), random.randint(0, H)
    a = random.randint(8, 18)
    draw.ellipse([x, y, x+2, y+2], fill=(200, 180, 155, a))

# Fine grain noise pattern - tiny horizontal lines
for _ in range(60):
    x, y = random.randint(0, W), random.randint(0, H)
    w = random.randint(3, 8)
    a = random.randint(4, 10)
    draw.rectangle([x, y, x+w, y], fill=(200, 185, 160, a))

# === COCONUT SHELL DECORATIVE CIRCLES ===
draw.ellipse([W-350, -180, W+80, 300], outline=ACCENT_LIGHT + (25,), width=4)
draw.ellipse([-60, H-300, 140, H-60], outline=ACCENT_LIGHT + (18,), width=3)

# === GOLD ACCENT LINES (2x thicker) ===
draw.rectangle([160, 410, 400, 416], fill=ACCENT + (220,))
draw.rectangle([160, 428, 164, 680], fill=ACCENT + (180,))

# === TOP-RIGHT DECORATIVE DOTS (2x bigger) ===
for i, (x, y) in enumerate([(W-260, 140), (W-224, 140), (W-188, 140)]):
    c = ACCENT_LIGHT if i < 2 else ACCENT
    draw.ellipse([x, y, x+12, y+12], fill=c + (180,))

# === WAVY HORIZON LINE ===
pts = [(i, H-70+int(20*math.sin(i*0.01))+int(10*math.sin(i*0.025))) for i in range(0, W, 2)]
for i in range(len(pts)-1):
    draw.line([pts[i], pts[i+1]], fill=ACCENT_LIGHT + (30,), width=2)

# === MAIN TITLE - Noto Bold ===
title = "八字到底在说什么"
tf = f(128, bold=True)

# Shadow
for dx, dy in [(4,4),(5,5),(6,6)]:
    draw.text((160+dx, 450+dy), title, fill=SHADOW, font=tf)
# Main text
draw.text((160, 450), title, fill=TEXT_MAIN + (255,), font=tf)

# === SUBTITLE - bigger ===
sub = "先看地图，再谈命运"
sf = f(68)
draw.text((168, 600), sub, fill=TEXT_SUB + (245,), font=sf)

# === BOTTOM ACCENT BAR ===
draw.rectangle([160, H-180, 260, H-174], fill=ACCENT + (230,))

# === BOTTOM TEXT - much bigger ===
draw.text((160, H-150), "八字入门 · 第0课", fill=TEXT_BOTTOM + (240,), font=f(52))
draw.text((W-340, H-150), "@椰子", fill=TEXT_BOTTOM + (200,), font=f(48))

# === DECORATIVE: coconut leaf curve ===
for t in range(0, 100, 3):
    rad = math.radians(t)
    x = 200 + rad * 6
    y = 780 + rad * 3
    draw.ellipse([x-1, y-1, x+1, y+1], fill=ACCENT_LIGHT + (15,))

# === TOP-LEFT CORNER MINIMAL DECO ===
for t in range(0, 80, 2):
    rad = math.radians(t)
    x = 60 + rad * 6
    y = 60 + rad * 3
    draw.ellipse([x-1, y-1, x+1, y+1], fill=ACCENT + (12,))

# === RASTERIZE WITH STRONGER ANTI-ALIASING ===
# Save at full resolution
out = "/home/ubuntu/命理学/第0课-封面-椰子高清.png"
img.save(out, "PNG")
print(f"OK: {out}")
print(f"Size: {os.path.getsize(out) / 1024:.0f} KB")
print(f"Dimensions: {W}x{H}")
