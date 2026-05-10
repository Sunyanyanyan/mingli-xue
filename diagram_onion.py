#!/usr/bin/env python3
"""生成五层洋葱图"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 500, 600
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

img = Image.new('RGBA', (W, H), (255, 248, 240, 255))
draw = ImageDraw.Draw(img)

ACCENT = (193, 127, 78)
TEXT_MAIN = (61, 43, 31)

# 5 layers, each wider than the previous (onion effect)
# colors: from outer to inner, getting warmer
colors = [
    (252, 235, 220),  # 天干 - light cream
    (248, 225, 200),  # 地支 - warm cream
    (240, 215, 185),  # 藏干 - tan
    (230, 200, 165),  # 五行 - deeper tan
    (220, 185, 145),  # 十神 - deepest
]

layers = [
    ("第1层", "天干", "表面的你"),
    ("第2层", "地支", "骨子里的你"),
    ("第3层", "藏干", "你藏着的那面"),
    ("第4层", "五行生克", "力量怎么互动"),
    ("第5层", "十神", "谁帮你·谁压你"),
]

# From outer to inner (wider rectangles first)
start_y = 40
box_h = 80
gap = 12

for i in range(5):
    # Widest at top, narrowest at bottom
    width = 380 - i * 45
    x = (W - width) // 2
    y = start_y + i * (box_h + gap)
    
    # Background
    draw.rectangle([x, y, x+width, y+box_h], fill=colors[i] + (255,), outline=ACCENT + (160,), width=2)
    
    # Layer number
    draw.text((x+15, y+10), layers[i][0], fill=ACCENT + (200,), font=f(16))
    
    # Title
    draw.text((x+15, y+32), layers[i][1], fill=TEXT_MAIN + (255,), font=f(24, bold=True))
    
    # Description
    desc_w = draw.textlength(layers[i][2], font=f(16))
    draw.text((x+width-desc_w-15, y+35), layers[i][2], fill=TEXT_MAIN + (170,), font=f(16))
    
    # Arrow down (except last)
    if i < 4:
        ax = W // 2
        ay = y + box_h + 2
        draw.text((ax-6, ay), "↓", fill=ACCENT + (200,), font=f(20))

out = "/home/ubuntu/命理学/第0课-五层洋葱.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
