#!/usr/bin/env python3
"""五层洋葱图 - v10 简洁同心"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 520*SCALE, 540*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (255, 243, 224)
TITLE = (62, 39, 35)

cx, cy = W//2, H//2 + 15*SCALE  # 中心

# 五层同心圆角矩形 (从外到内)
rings = [
    {"r": 220, "rad": 28, "color": (255, 230, 200), "text": (62,39,35), "label": "第1层 天干", "sub": "表面的你"},
    {"r": 175, "rad": 22, "color": (250, 215, 180), "text": (62,39,35), "label": "第2层 地支", "sub": "骨子里的你"},
    {"r": 132, "rad": 18, "color": (240, 198, 158), "text": (62,39,35), "label": "第3层 藏干", "sub": "你藏着的那面"},
    {"r": 92,  "rad": 14, "color": (225, 175, 132), "text": (62,39,35), "label": "第4层 五行生克", "sub": "力量怎么互动"},
    {"r": 54,  "rad": 10, "color": (200, 148, 102), "text": (255,240,220), "label": "第5层 十神", "sub": "谁帮你·谁压你"},
]

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# 标题
draw.text((cx-120*SCALE, 12*SCALE), "八字是一层一层剥开的", fill=TITLE+(255,), font=ft(24, bold=True))

# 从外到内画
for i, ring in enumerate(rings):
    r = ring["r"] * SCALE
    rad = ring["rad"] * SCALE
    color = ring["color"]
    tc = ring["text"]
    
    x1 = cx - r
    y1 = cy - r
    x2 = cx + r
    y2 = cy + r
    
    # 画圆角矩形
    draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=color+(255,), 
                           outline=(180,150,120)+(120,), width=2)
    
    # 左上角标号
    draw.text((x1+12*SCALE, y1+8*SCALE), ring["label"], fill=tc+(200,), font=ft(15, bold=True))
    draw.text((x1+12*SCALE, y1+30*SCALE), ring["sub"], fill=tc+(160,), font=ft(14))
    
    # 如果不是最内层，在右上角画"剥开"翻边
    if i < 4:
        next_r = rings[i+1]["r"] * SCALE
        # 右上角剥开的 flap
        flap_w = int(r * 0.18)
        flap_h = int(r * 0.15)
        flap_x = x2 - 2
        flap_y = y1 + 2
        
        # 翻起的瓣 (右上)
        fpts = [
            (flap_x, flap_y),
            (flap_x + flap_w, flap_y),
            (flap_x + flap_w + 8*SCALE, flap_y - flap_h),
            (flap_x + 8*SCALE, flap_y - flap_h + 10*SCALE),
        ]
        # flap 亮色
        lighter = tuple(min(c+30, 255) for c in color)
        draw.polygon(fpts, fill=lighter+(255,), outline=(180,150,120)+(120,), width=1)
        
        # 剥开后露出的下一层颜色
        inner_color = rings[i+1]["color"]
        inner_x1 = cx - next_r
        shdw = [
            (flap_x, flap_y+4),
            (flap_x + flap_w-4, flap_y+4),
            (flap_x + flap_w+6, flap_y - flap_h+8),
            (flap_x + 6, flap_y - flap_h+12),
        ]
        draw.polygon(shdw, fill=inner_color+(200,))
        
        # 从剥开处画一个弧形箭头指向内层
        arrow_x = flap_x + flap_w//2
        arrow_y = flap_y + 20*SCALE
        draw.text((arrow_x-10*SCALE, arrow_y), "➘", fill=(200,120,80)+(200,), font=ft(20))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v10.png"
img.save(out, "PNG")
print(f"OK: {out}")
