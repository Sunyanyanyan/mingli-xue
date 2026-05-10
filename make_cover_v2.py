from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 1200, 628
random.seed(42)

img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# === DEEP GRADIENT BACKGROUND ===
for y in range(H):
    ratio = y / H
    r = int(15 + ratio * 8)
    g = int(18 + ratio * 12)
    b = int(30 + ratio * 20)
    draw.rectangle([0, y, W, y], fill=(r, g, b, 255))

# === SUBTLE TEXTURE: tiny dots ===
for _ in range(300):
    x = random.randint(0, W)
    y = random.randint(0, H)
    a = random.randint(5, 15)
    draw.ellipse([x, y, x+1, y+1], fill=(255, 255, 255, a))

# === DECORATIVE: Large faint circle top-right ===
draw.ellipse([W-380, -150, W+50, 280], outline=(180, 150, 80, 18), width=2)

# === DECORATIVE: Small circle bottom-left ===
draw.ellipse([-80, H-250, 120, H-130], outline=(180, 150, 80, 12), width=1)

# === DECORATIVE: Thin horizontal accent line ===
draw.rectangle([80, 240, 200, 242], fill=(200, 170, 90, 60))

# === DECORATIVE: Vertical accent line ===
draw.rectangle([80, 250, 82, 390], fill=(200, 170, 90, 40))

# === FONT ===
font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def f(sz):
    return ImageFont.truetype(font_path, sz)

# === MAIN TITLE ===
title = "八字到底在说什么"
tf = f(64)
for dx, dy in [(2,2),(3,3)]:
    draw.text((82+dx, 260+dy), title, fill=(0,0,0,60), font=tf)
draw.text((82, 260), title, fill=(230, 215, 180, 255), font=tf)

# === SUBTITLE ===
sub = "先看地图，再谈命运"
sf = f(30)
draw.text((85, 335), sub, fill=(180, 165, 140, 200), font=sf)

# === BOTTOM GOLD ACCENT BAR ===
draw.rectangle([80, H-90, 130, H-86], fill=(200, 170, 90, 180))

# === BOTTOM TEXT ===
draw.text((80, H-75), "八字入门 · 第0课", fill=(160, 150, 130, 180), font=f(22))
draw.text((W-160, H-75), "@椰子", fill=(160, 150, 130, 120), font=f(20))

# === TOP-RIGHT DECORATIVE DOTS ===
for i, (x, y) in enumerate([(W-120, 80), (W-105, 80), (W-90, 80)]):
    alpha = 60 if i < 2 else 120
    draw.ellipse([x, y, x+4, y+4], fill=(180, 150, 80, alpha))

# === SUBTLE MOUNTAIN/HORIZON LINE ===
pts = []
for i in range(0, W, 2):
    x = i
    y = H - 30 + int(15 * math.sin(i * 0.008)) + int(8 * math.sin(i * 0.02))
    pts.append((x, y))
for i in range(len(pts)-1):
    if i < len(pts) - 1:
        draw.line([pts[i], pts[i+1]], fill=(100, 95, 85, 15), width=1)

# === TOP-LEFT GOLD ARC ===
for t in range(0, 60, 2):
    rad = math.radians(t)
    x = 30 + rad * 4
    y = 30 + rad * 2
    draw.ellipse([x-1, y-1, x+1, y+1], fill=(200, 170, 90, 15))

out = "/home/ubuntu/命理学/第0课-封面-v2.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)} bytes)")
