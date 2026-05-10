#!/usr/bin/env python3
"""五层洋葱图 - 专业版 重新设计"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 500*SCALE, 620*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

# === 专业配色 ===
BG = (248, 246, 241)
GOLD = (160, 130, 95)         # 暖褐
GOLD_LIGHT = (215, 205, 190)  # 浅褐
TITLE = (48, 57, 66)
TEXT = (55, 60, 65)
TEXT_DIM = (140, 145, 150)

# 卡片色 - 从浅到深 (外到内)
card_colors = [
    (255, 255, 255),   # 第1层 - 白
    (252, 250, 247),   # 第2层
    (249, 246, 241),   # 第3层
    (245, 241, 235),   # 第4层
    (240, 235, 228),   # 第5层 - 最深
]

# 左侧色条
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
draw.text((W//2-100*SCALE, 20*SCALE), "八字是一层一层剥开的", fill=TITLE+(255,), font=f(22, bold=True))

# === 五层卡片 ===
start_y = 70*SCALE
box_h = 85*SCALE
gap = 10*SCALE

for i in range(5):
    width = 380*SCALE - i*30*SCALE  # 380 → 260, each step 30 narrower
    x = (W - width)//2
    y = start_y + i*(box_h + gap)
    
    # Card shadow
    draw.rectangle([x+4, y+4, x+width+4, y+box_h+4], fill=(0,0,0,12))
    
    # Card bg
    draw.rectangle([x, y, x+width, y+box_h], fill=card_colors[i]+(255,), outline=GOLD_LIGHT+(180,), width=2)
    
    # Left color bar
    draw.rectangle([x+2, y+8, x+6, y+box_h-8], fill=bar_colors[i]+(200,))
    
    # Layer number (small, top)
    draw.text((x+18, y+8), layers[i][0], fill=TEXT_DIM+(180,), font=f(14))
    
    # Title (bigger, middle)
    draw.text((x+18, y+30), layers[i][1], fill=TITLE+(255,), font=f(24, bold=True))
    
    # Description (right side)
    desc = layers[i][2]
    desc_w = draw.textlength(desc, font=f(16))
    draw.text((x+width-desc_w-15, y+38), desc, fill=TEXT+(180,), font=f(16))
    
    # Arrow down
    if i < 4:
        ax = W//2
        ay = y + box_h + 1
        draw.text((ax-6, ay), "↓", fill=GOLD+(150,), font=f(18))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v3.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
