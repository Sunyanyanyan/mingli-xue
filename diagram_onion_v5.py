#!/usr/bin/env python3
"""五层洋葱图 - v5 居中+大字"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 520*SCALE, 620*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (248, 246, 241)
TITLE = (45, 50, 55)
TEXT = (50, 55, 60)

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
draw.text((W//2-120*SCALE, 18*SCALE), "八字是一层一层剥开的", fill=TITLE+(255,), font=ft(24, bold=True))
draw.text((W//2-120*SCALE, 52*SCALE), "从外到内，逐层深入", fill=(130,135,140)+(200,), font=ft(16))

# === 卡片 ===
start_y = 100*SCALE
box_h = 84*SCALE
gap = 10*SCALE

for i in range(5):
    width = 400*SCALE - i*30*SCALE
    x = (W - width)//2
    y = start_y + i*(box_h + gap)
    
    # 阴影
    draw.rectangle([x+4, y+4, x+width+4, y+box_h+4], fill=(0,0,0,10))
    
    # 卡片
    draw.rectangle([x, y, x+width, y+box_h], fill=card_colors[i]+(255,), outline=(215,210,200)+(180,), width=2)
    
    # 左侧色条
    draw.rectangle([x+3, y+8, x+7, y+box_h-8], fill=bar_colors[i]+(200,))
    
    # 层号
    draw.text((x+20, y+8), layers[i][0], fill=(130,135,140)+(180,), font=ft(15))
    
    # 标题
    draw.text((x+20, y+32), layers[i][1], fill=TITLE+(255,), font=ft(26, bold=True))
    
    # 描述
    desc = layers[i][2]
    desc_w = draw.textlength(desc, font=ft(17))
    draw.text((x+width-desc_w-18, y+38), desc, fill=TEXT+(200,), font=ft(17))
    
    # 箭头
    if i < 4:
        ay = y + box_h + 1
        draw.text((W//2-10*SCALE, ay), "↓", fill=bar_colors[i]+(180,), font=ft(22))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v5.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
