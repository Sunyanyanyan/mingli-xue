#!/usr/bin/env python3
"""五层洋葱图 - v7 垂直居中 压短"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 520*SCALE, 520*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (255, 243, 224)
TITLE = (62, 39, 35)
TEXT = (93, 64, 55)

card_colors = [
    (255, 255, 255),
    (255, 250, 242),
    (255, 247, 237),
    (255, 243, 230),
    (255, 238, 224),
]

bar_colors = [
    (230, 81, 0),
    (220, 75, 10),
    (210, 68, 18),
    (200, 62, 26),
    (191, 54, 12),
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

# === 垂直居中: 总内容高≈400, 图像520, 偏移=(520-400)/2≈60 ===
yo = 60*SCALE

# === 标题 ===
draw.text((W//2-120*SCALE, yo+5*SCALE), "八字是一层一层剥开的", fill=TITLE+(255,), font=ft(24, bold=True))

# === 卡片 ===
start_y = 50*SCALE + yo
box_h = 78*SCALE
gap = 8*SCALE

for i in range(5):
    width = 400*SCALE - i*28*SCALE
    x = (W - width)//2
    y = start_y + i*(box_h + gap)
    
    # 阴影
    draw.rectangle([x+4, y+4, x+width+4, y+box_h+4], fill=(0,0,0,8))
    
    # 卡片
    draw.rectangle([x, y, x+width, y+box_h], fill=card_colors[i]+(255,), outline=(232,225,220)+(180,), width=2)
    
    # 橙色色条
    draw.rectangle([x+3, y+6, x+7, y+box_h-6], fill=bar_colors[i]+(200,))
    
    # 层号
    draw.text((x+20, y+6), layers[i][0], fill=(141,110,99)+(180,), font=ft(15))
    
    # 标题
    draw.text((x+20, y+28), layers[i][1], fill=TITLE+(255,), font=ft(26, bold=True))
    
    # 描述
    desc = layers[i][2]
    desc_w = draw.textlength(desc, font=ft(17))
    draw.text((x+width-desc_w-18, y+34), desc, fill=TEXT+(200,), font=ft(17))
    
    # 箭头
    if i < 4:
        ay = y + box_h + 1
        draw.text((W//2-10*SCALE, ay), "↓", fill=bar_colors[i]+(180,), font=ft(22))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v7.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
