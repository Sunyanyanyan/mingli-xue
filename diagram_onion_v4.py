#!/usr/bin/env python3
"""五层洋葱图 - v4 修正版 加大字号"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 540*SCALE, 640*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (248, 246, 241)
TITLE = (48, 57, 66)
TEXT = (55, 60, 65)
TEXT_DIM = (150, 155, 160)
GOLD_LINE = (215, 205, 190)

card_colors = [
    (255, 255, 255),
    (252, 250, 247),
    (249, 246, 241),
    (245, 241, 235),
    (240, 235, 228),
]

bar_colors = [
    (180, 160, 140),
    (165, 145, 125),
    (150, 130, 110),
    (135, 115, 95),
    (120, 100, 80),
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

# === 标题 ===
draw.text((W//2-110*SCALE, 20*SCALE), "八字是一层一层剥开的", fill=TITLE+(255,), font=f(24, bold=True))
draw.text((W//2-110*SCALE, 55*SCALE), "从外到内，逐层深入", fill=TEXT_DIM+(160,), font=f(16))

# === 卡片 ===
start_y = 95*SCALE
box_h = 85*SCALE
gap = 10*SCALE

for i in range(5):
    width = 400*SCALE - i*30*SCALE
    x = (W - width)//2
    y = start_y + i*(box_h + gap)
    
    # Shadow
    draw.rectangle([x+5, y+5, x+width+5, y+box_h+5], fill=(0,0,0,10))
    
    # Card
    draw.rectangle([x, y, x+width, y+box_h], fill=card_colors[i]+(255,), outline=GOLD_LINE+(180,), width=2)
    
    # Left bar
    draw.rectangle([x+3, y+10, x+7, y+box_h-10], fill=bar_colors[i]+(200,))
    
    # Layer number
    draw.text((x+20, y+8), layers[i][0], fill=TEXT_DIM+(180,), font=f(15))
    
    # Title
    draw.text((x+20, y+32), layers[i][1], fill=TITLE+(255,), font=f(26, bold=True))
    
    # Description
    desc = layers[i][2]
    desc_w = draw.textlength(desc, font=f(17))
    draw.text((x+width-desc_w-18, y+38), desc, fill=TEXT+(180,), font=f(17))
    
    # Arrow
    if i < 4:
        ax = W//2
        ay = y + box_h + 1
        draw.text((ax-8, ay), "↓", fill=bar_colors[i]+(180,), font=f(22))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v4.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
