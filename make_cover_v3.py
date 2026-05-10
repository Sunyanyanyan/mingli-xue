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

# === FONT ===
font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def f(sz):
    return ImageFont.truetype(font_path, sz)

# === DECORATIVE: Thin horizontal accent line ===
draw.rectangle([80, 210, 200, 212], fill=(200, 170, 90, 80))
# === DECORATIVE: Vertical accent line ===
draw.rectangle([80, 220, 82, 380], fill=(200, 170, 90, 50))

# === MAIN TITLE ===
title = "八字到底在说什么"
tf = f(72)
for dx, dy in [(2,2),(3,3)]:
    draw.text((82+dx, 230+dy), title, fill=(0,0,0,60), font=tf)
draw.text((82, 230), title, fill=(235, 220, 185, 255), font=tf)

# === SUBTITLE (bigger, bolder) ===
sub = "先看地图，再谈命运"
sf = f(38)
draw.text((85, 315), sub, fill=(200, 185, 155, 255), font=sf)

# === BOTTOM GOLD ACCENT BAR ===
draw.rectangle([80, H-95, 130, H-91], fill=(200, 170, 90, 200))

# === BOTTOM TEXT (bigger) ===
draw.text((80, H-80), "八字入门 · 第0课", fill=(180, 170, 150, 230), font=f(26))
draw.text((W-170, H-80), "@椰子", fill=(160, 150, 130, 180), font=f(24))

# === TOP-RIGHT DECORATIVE DOTS ===
for i, (x, y) in enumerate([(W-130, 70), (W-112, 70), (W-94, 70)]):
    alpha = 60 if i < 2 else 120
    draw.ellipse([x, y, x+5, y+5], fill=(180, 150, 80, alpha))

# === SUBTLE MOUNTAIN/HORIZON LINE ===
pts = []
for i in range(0, W, 2):
    x = i
    y = H - 30 + int(15 * math.sin(i * 0.008)) + int(8 * math.sin(i * 0.02))
    pts.append((x, y))
for i in range(len(pts)-1):
    draw.line([pts[i], pts[i+1]], fill=(100, 95, 85, 18), width=1)

# === TOP-LEFT GOLD ARC ===
for t in range(0, 60, 2):
    rad = math.radians(t)
    x = 30 + rad * 4
    y = 30 + rad * 2
    draw.ellipse([x-1, y-1, x+1, y+1], fill=(200, 170, 90, 18))

out = "/home/ubuntu/命理学/第0课-封面-v3.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)} bytes)")
