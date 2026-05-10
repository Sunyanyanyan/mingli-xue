#!/usr/bin/env python3
"""五层洋葱图 - 2x高清版"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 500*SCALE, 600*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

img = Image.new('RGBA', (W, H), (255, 248, 240, 255))
draw = ImageDraw.Draw(img)

ACCENT = (193, 127, 78)
TEXT_MAIN = (61, 43, 31)

colors = [
    (252, 235, 220),
    (248, 225, 200),
    (240, 215, 185),
    (230, 200, 165),
    (220, 185, 145),
]

layers = [
    ("第1层", "天干", "表面的你"),
    ("第2层", "地支", "骨子里的你"),
    ("第3层", "藏干", "你藏着的那面"),
    ("第4层", "五行生克", "力量怎么互动"),
    ("第5层", "十神", "谁帮你·谁压你"),
]

start_y = 40*SCALE
box_h = 80*SCALE
gap = 12*SCALE

for i in range(5):
    width = 380*SCALE - i*45*SCALE
    x = (W - width)//2
    y = start_y + i*(box_h + gap)
    
    # Background box
    draw.rectangle([x, y, x+width, y+box_h], fill=colors[i]+(255,), outline=ACCENT+(160,), width=2*SCALE)
    
    # 第X层
    draw.text((x+15*SCALE, y+10*SCALE), layers[i][0], fill=ACCENT+(200,), font=f(16))
    
    # Title
    draw.text((x+15*SCALE, y+32*SCALE), layers[i][1], fill=TEXT_MAIN+(255,), font=f(24, bold=True))
    
    # Description (right-aligned)
    desc = layers[i][2]
    desc_w = draw.textlength(desc, font=f(16))
    draw.text((x+width-desc_w-15*SCALE, y+35*SCALE), desc, fill=TEXT_MAIN+(170,), font=f(16))
    
    # Down arrow
    if i < 4:
        ax = W//2
        ay = y + box_h + 2*SCALE
        draw.text((ax-6*SCALE, ay), "↓", fill=ACCENT+(200,), font=f(20))

out = "/home/ubuntu/命理学/第0课-五层洋葱-HD.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
