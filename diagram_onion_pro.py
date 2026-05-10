#!/usr/bin/env python3
"""五层洋葱图 - 高级深色版"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 500*SCALE, 600*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

# === 高级配色 ===
BG = (28, 24, 20)
GOLD = (201, 169, 110)
GOLD_DIM = (160, 140, 95)
TEXT_MAIN = (240, 230, 210)
TEXT_DIM = (180, 170, 150)

# Layer card colors - dark but subtly layered
card_colors = [
    (55, 48, 40),    # 第1层 - slightly lighter
    (50, 44, 37),    # 第2层
    (46, 40, 34),    # 第3层
    (42, 37, 31),    # 第4层
    (38, 33, 28),    # 第5层 - darkest (innermost)
]

layers = [
    ("第1层", "天干", "表面的你"),
    ("第2层", "地支", "骨子里的你"),
    ("第3层", "藏干", "你藏着的那面"),
    ("第4层", "五行生克", "力量怎么互动"),
    ("第5层", "十神", "谁帮你·谁压你"),
]

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# === Subtle vignette ===
for y in range(H):
    ratio = y / H
    r = min(35, BG[0] + int(8 * (1 - abs(ratio-0.4)*2))) if ratio < 0.4 else BG[0]
    g = min(30, BG[1] + int(6 * (1 - abs(ratio-0.4)*2))) if ratio < 0.4 else BG[1]
    b = min(26, BG[2] + int(6 * (1 - abs(ratio-0.4)*2))) if ratio < 0.4 else BG[2]
    draw.rectangle([0, y, W, y], fill=(r, g, b, 15))

# === Title ===
draw.text((W//2-80*SCALE, 20*SCALE), "八字五层结构", fill=GOLD+(220,), font=f(22, bold=True))
draw.text((W//2-80*SCALE, 50*SCALE), "从外到内，逐层剥开", fill=TEXT_DIM+(150,), font=f(14))

# === Layers ===
start_y = 90*SCALE
box_h = 80*SCALE
gap = 12*SCALE

for i in range(5):
    width = 380*SCALE - i*45*SCALE
    x = (W - width)//2
    y = start_y + i*(box_h + gap)
    
    # Card background with subtle gold border
    draw.rectangle([x, y, x+width, y+box_h], fill=card_colors[i]+(255,), outline=GOLD+(80,), width=2)
    
    # Small left accent bar
    draw.rectangle([x, y+8, x+4, y+box_h-8], fill=GOLD+(160,))
    
    # Layer number
    draw.text((x+18, y+10), layers[i][0], fill=GOLD_DIM+(200,), font=f(16))
    
    # Title
    draw.text((x+18, y+32), layers[i][1], fill=TEXT_MAIN+(255,), font=f(24, bold=True))
    
    # Description
    desc = layers[i][2]
    desc_w = draw.textlength(desc, font=f(16))
    draw.text((x+width-desc_w-15, y+35), desc, fill=TEXT_DIM+(180,), font=f(16))
    
    # Arrow
    if i < 4:
        ax = W//2
        ay = y + box_h + 2
        draw.text((ax-6, ay), "↓", fill=GOLD+(150,), font=f(20))

out = "/home/ubuntu/命理学/第0课-五层洋葱-pro.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
