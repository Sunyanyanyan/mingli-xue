#!/usr/bin/env python3
"""高分辨率封面 v5 - 无条纹渐变 + 椰子配色 + Noto Sans"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 2400, 1256
random.seed(42)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

# === BUILD SMOOTH GRADIENT USING BLENDED LAYERS ===
# Instead of per-row rectangles, use a large gradient image
base = Image.new('RGBA', (W, H), (255, 248, 240, 255))   # warm cream top

# Create radial gradient overlay for depth (soft spotlight)
grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gdraw = ImageDraw.Draw(grad)

# Soft vignette - darker at edges, lighter in center
# Use multiple overlay circles for smooth transition
cx, cy = W//2, H//3  # center slightly above middle
max_r = int(math.sqrt(W*W + H*H))

# Radial gradient using concentric circles
for r in range(max_r, 0, -4):
    alpha = max(0, min(15, int(15 * (1 - r / max_r))))
    if alpha > 0:
        gdraw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(242, 232, 215, alpha))

# Blend gradient overlay onto base
img = Image.alpha_composite(base, grad)
draw = ImageDraw.Draw(img)

# === SUBTLE TEXTURE: tiny dots only (no lines!) ===
for _ in range(500):
    x, y = random.randint(0, W), random.randint(0, H)
    a = random.randint(6, 16)
    draw.ellipse([x, y, x+2, y+2], fill=(200, 185, 165, a))

# === COCONUT SHELL DECORATIVE CIRCLES ===
draw.ellipse([W-350, -180, W+80, 300], outline=(210, 180, 140, 28), width=4)
draw.ellipse([-60, H-300, 140, H-60], outline=(210, 180, 140, 20), width=3)

# === GOLD ACCENT LINES ===
draw.rectangle([160, 410, 400, 416], fill=(193, 127, 78, 220))
draw.rectangle([160, 428, 164, 680], fill=(193, 127, 78, 180))

# === TOP-RIGHT DECORATIVE DOTS ===
for i, (x, y) in enumerate([(W-260, 140), (W-224, 140), (W-188, 140)]):
    c = (210, 180, 140) if i < 2 else (193, 127, 78)
    a = 180
    draw.ellipse([x, y, x+12, y+12], fill=c + (a,))

# === WAVY HORIZON LINE (subtle) ===
pts = [(i, H-70+int(20*math.sin(i*0.01))+int(10*math.sin(i*0.025))) for i in range(0, W, 4)]
for i in range(len(pts)-1):
    draw.line([pts[i], pts[i+1]], fill=(210, 180, 140, 35), width=2)

# === MAIN TITLE - Noto Bold ===
title = "八字到底在说什么"
tf = f(128, bold=True)

# Shadow
draw.text((162, 452), title, fill=(0, 0, 0, 22), font=tf)
# Main text
draw.text((160, 450), title, fill=(61, 43, 31, 255), font=tf)

# === SUBTITLE ===
sub = "先看地图，再谈命运"
draw.text((168, 600), sub, fill=(115, 88, 62, 245), font=f(68))

# === BOTTOM ACCENT BAR ===
draw.rectangle([160, H-180, 260, H-174], fill=(193, 127, 78, 230))

# === BOTTOM TEXT ===
draw.text((160, H-150), "八字入门 · 第0课", fill=(155, 125, 95, 240), font=f(52))
draw.text((W-340, H-150), "@椰子", fill=(155, 125, 95, 200), font=f(48))

# === DECORATIVE: coconut leaf curve ===
for t in range(0, 100, 3):
    rad = math.radians(t)
    x = 200 + rad * 6
    y = 780 + rad * 3
    draw.ellipse([x-1, y-1, x+1, y+1], fill=(210, 180, 140, 18))

# === TOP-LEFT minimal deco ===
for t in range(0, 80, 2):
    rad = math.radians(t)
    x = 60 + rad * 6
    y = 60 + rad * 3
    draw.ellipse([x-1, y-1, x+1, y+1], fill=(193, 127, 78, 14))

out = "/home/ubuntu/命理学/第0课-封面-v5.png"
img.save(out, "PNG")
print(f"OK: {out}")
print(f"Size: {os.path.getsize(out) / 1024:.0f} KB")
