#!/usr/bin/env python3
"""四柱表 - 高级深色版"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 800*SCALE, 500*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

# === 高级配色 ===
BG = (28, 24, 20)            # 深炭底
CARD_BG1 = (45, 40, 35)      # 卡片底色1
CARD_BG2 = (52, 47, 42)      # 卡片底色2
GOLD = (201, 169, 110)        # 古铜金
GOLD_DIM = (160, 140, 95)     # 暗金
TEXT_MAIN = (240, 230, 210)  # 暖白
TEXT_DIM = (180, 170, 150)   # 灰白
HIGHLIGHT = (212, 168, 88)   # 高亮金
LINE = (70, 65, 58)          # 分割线

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# === Subtle radial vignette ===
for y in range(H):
    ratio = y / H
    r = int(BG[0] + (35-BG[0]) * (1 - abs(ratio-0.4)*2)) if ratio < 0.4 else int(BG[0] + (35-BG[0]) * (1 - abs(ratio-0.4)))
    g = int(BG[1] + (30-BG[1]) * (1 - abs(ratio-0.4)*2)) if ratio < 0.4 else int(BG[1] + (30-BG[1]) * (1 - abs(ratio-0.4)))
    b = int(BG[2] + (26-BG[2]) * (1 - abs(ratio-0.4)*2)) if ratio < 0.4 else int(BG[2] + (26-BG[2]) * (1 - abs(ratio-0.4)))
    draw.rectangle([0, y, W, y], fill=(r, g, b, 15))

# === Column headers ===
col_w = 125*SCALE
table_x = 100*SCALE
table_y = 80*SCALE
padding = 30*SCALE
cell_h = 52*SCALE
gy = table_y + 68*SCALE

headers = ["年柱", "月柱", "日柱", "时柱"]
for i, h in enumerate(headers):
    cx = table_x + 20*SCALE + i*col_w
    cy = table_y + 5*SCALE
    draw.text((cx, cy), h, fill=GOLD+(255,), font=f(24, bold=True))

# === Decorative line under headers ===
draw.rectangle([table_x+10*SCALE, table_y+40*SCALE, table_x+padding+4*col_w-10*SCALE, table_y+42*SCALE], fill=GOLD_DIM+(120,))

# === Grid ===
row1_vals = ["甲", "丙", "乙", "丁"]
row2_vals = ["寅", "午", "丑", "亥"]

# Draw cells
for r in range(2):
    for c in range(4):
        x1 = table_x + padding + (c*col_w if c>0 else 0)
        y1 = gy + r*cell_h
        x2 = x1 + col_w
        y2 = y1 + cell_h
        fill_c = CARD_BG1 if r==0 else CARD_BG2
        # Rounded corners effect via multiple rectangles
        draw.rectangle([x1+4, y1+4, x2-4, y2-4], fill=fill_c+(255,))
        draw.rectangle([x1, y1, x2, y2], outline=LINE+(200,), width=2)

# Row labels
draw.text((table_x+8, gy+12*SCALE), "天干", fill=GOLD_DIM+(200,), font=f(18, bold=True))
draw.text((table_x+8, gy+12*SCALE+cell_h), "地支", fill=GOLD_DIM+(200,), font=f(18, bold=True))

# Row values - 天干
for i, v in enumerate(row1_vals):
    cx = table_x + padding + i*col_w + col_w//2 - 10*SCALE
    cy = gy + 8*SCALE
    color = HIGHLIGHT+(255,) if i==2 else TEXT_MAIN+(255,)
    draw.text((cx, cy), v, fill=color, font=f(28, bold=True))

# Row values - 地支
for i, v in enumerate(row2_vals):
    cx = table_x + padding + i*col_w + col_w//2 - 10*SCALE
    cy = gy + cell_h + 8*SCALE
    draw.text((cx, cy), v, fill=TEXT_MAIN+(255,), font=f(28, bold=True))

# Highlight box (日柱)
hx = table_x + padding + 2*col_w - 6*SCALE
hy = gy - 6*SCALE
hw = col_w + 12*SCALE
hh = cell_h*2 + 12*SCALE
draw.rectangle([hx, hy, hx+hw, hy+hh], outline=HIGHLIGHT+(200,), width=3)

# 日主 annotation
draw.text((hx+20*SCALE, hy+hh+10*SCALE), "← 日主（你自己）", fill=HIGHLIGHT+(230,), font=f(18))

# Bottom text
draw.text((table_x+30*SCALE, hy+hh+52*SCALE), "天干 = 你的表面性格    地支 = 你的内在底色", fill=TEXT_DIM+(200,), font=f(16))

# === Top-right decorative dots ===
for i, (dx, dy) in enumerate([(W-80, 50), (W-68, 50), (W-56, 50)]):
    alpha = 60 if i < 2 else 120
    draw.ellipse([dx, dy, dx+6, dy+6], fill=GOLD+(alpha,))

out = "/home/ubuntu/命理学/第0课-四柱表-pro.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
