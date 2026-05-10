#!/usr/bin/env python3
"""五层洋葱图 v11 - 简洁切片"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 520*SCALE, 560*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (255, 243, 224)
TITLE = (62, 39, 35)

# 从外到内 5层 暖色渐变 (浅→深)
ring_colors = [
    (255, 235, 210),
    (252, 222, 192),
    (245, 208, 175),
    (235, 192, 155),
    (220, 172, 130),
]
inner_borders = [
    (235, 210, 185),
    (228, 198, 170),
    (218, 188, 155),
    (205, 170, 135),
    (195, 150, 110),
]

layers = [
    ("第1层", "天干"),
    ("第2层", "地支"),
    ("第3层", "藏干"),
    ("第4层", "五行"),
    ("第5层", "十神"),
]

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# 标题
draw.text((W//2-115*SCALE, 15*SCALE), "八字五层结构", fill=TITLE+(255,), font=ft(24, bold=True))

# === 洋葱切片：每层是一个弧顶矩形 ===
# 从外到内画
cx = W // 2
top_y = 85 * SCALE
bot_y = H - 50 * SCALE

widths = [440, 380, 320, 260, 190]  # *SCALE
heights = [390, 340, 285, 225, 155]  # *SCALE
# 每层向右偏移 8px (剥开偏移)
x_off = [0, 8, 16, 24, 32]

for i in range(5):
    w = widths[i] * SCALE
    h = heights[i] * SCALE
    xo = x_off[i] * SCALE
    
    # 弧顶: 矩形+半圆顶
    x1 = cx - w//2 + xo
    x2 = cx + w//2 + xo
    y1 = top_y + (heights[0] - heights[i]) // 2 * SCALE  # 顶部对齐
    y2 = y1 + h
    
    # 圆角半径
    rad = (20 - i*2) * SCALE
    
    if i < 4:
        # === 外层：右上角剥开 ===
        # 画主矩形 (带圆角)
        draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=ring_colors[i]+(255,),
                               outline=inner_borders[i]+(180,), width=3)
        
        # 右上角剥开 flap (翻起)
        fw = int(w * 0.15)
        fh = int(h * 0.1)
        # flap 三角
        fp = [(x2-1, y1+1), (x2-1-fw, y1+1), (x2-1-fw-8*SCALE, y1-1-fh)]
        draw.polygon(fp, fill=(255,242,225,255), outline=(200,170,140,150), width=1)
        
        # flap 阴影下方露出下一层颜色
        sp = [(x2-1, y1+3), (x2-1-fw+4, y1+3), (x2-1-fw-4, y1-1-fh+4)]
        draw.polygon(sp, fill=ring_colors[i+1]+(200,))
        
        # 沿剥开边缘画白点
        for t in range(0, fw, 15):
            px = x2 - 1 - t
            py = y1 + 1 + int((fh/fw) * t * 0.3)
            draw.ellipse([px-2, py-2, px+2, py+2], fill=(255,255,255,160))
        
        # 右下角标注"从外到内"
        if i == 0:
            draw.text((x2-120*SCALE, y2+15*SCALE), "从外到内  一层一层剥开 →", fill=TITLE+(150,), font=ft(16))
        
    else:
        # === 最内层 ===
        draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=ring_colors[i]+(255,),
                               outline=inner_borders[i]+(200,), width=3)
    
    # 标号 (左上角)
    tc = (62,39,35) if i < 4 else (255,243,224)
    draw.text((x1+12*SCALE, y1+10*SCALE), layers[i][0], fill=tc+(200,), font=ft(15))
    draw.text((x1+12*SCALE, y1+35*SCALE), layers[i][1], fill=tc+(255,), font=ft(24, bold=True))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v11.png"
img.save(out, "PNG")
print("OK")
