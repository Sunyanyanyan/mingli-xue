#!/usr/bin/env python3
"""八字四柱表 - 2x高清版"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 800*SCALE, 500*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

img = Image.new('RGBA', (W, H), (255, 248, 240, 255))
draw = ImageDraw.Draw(img)

ACCENT = (193, 127, 78)
TEXT_MAIN = (61, 43, 31)
TEXT_LIGHT = (130, 100, 75)
BG_CELL1 = (252, 245, 235)
BG_CELL2 = (248, 238, 225)
LINE = (180, 160, 140)
HIGHLIGHT = (230, 120, 80)

col_w = 125*SCALE
padding = 30*SCALE
table_x = 100*SCALE
table_y = 80*SCALE
row_h = 55*SCALE
cell_h = 52*SCALE

# Column headers
headers = ["年柱", "月柱", "日柱", "时柱"]
for i, h in enumerate(headers):
    cx = table_x + 20*SCALE + i*col_w
    cy = table_y + 5*SCALE
    draw.text((cx, cy), h, fill=TEXT_MAIN+(255,), font=f(24, bold=True))

# Down arrows
for i in range(4):
    cx = table_x + 45*SCALE + i*col_w
    cy = table_y + 38*SCALE
    draw.text((cx-6*SCALE, cy), "↓", fill=ACCENT+(255,), font=f(18))

# Grid
gy = table_y + 68*SCALE
row1_vals = ["甲", "丙", "乙", "丁"]
row2_vals = ["寅", "午", "丑", "亥"]

# Draw cells
for r in range(2):
    for c in range(4):
        x1 = table_x + padding + (c*col_w if c>0 else 0)
        y1 = gy + r*cell_h
        x2 = x1 + col_w
        y2 = y1 + cell_h
        fill_c = BG_CELL1 if r==0 else BG_CELL2
        draw.rectangle([x1+2*SCALE, y1+2*SCALE, x2-2*SCALE, y2-2*SCALE], fill=fill_c+(255,))
        draw.rectangle([x1, y1, x2, y2], outline=LINE+(180,), width=2*SCALE)

# Row labels
draw.text((table_x+5*SCALE, gy+12*SCALE), "天干", fill=ACCENT+(255,), font=f(18, bold=True))
draw.text((table_x+5*SCALE, gy+12*SCALE+cell_h), "地支", fill=ACCENT+(255,), font=f(18, bold=True))

# Row values
for i, v in enumerate(row1_vals):
    cx = table_x + padding + i*col_w + col_w//2 - 10*SCALE
    cy = gy + 8*SCALE
    color = HIGHLIGHT+(255,) if i==2 else TEXT_MAIN+(255,)
    draw.text((cx, cy), v, fill=color, font=f(26, bold=True))

for i, v in enumerate(row2_vals):
    cx = table_x + padding + i*col_w + col_w//2 - 10*SCALE
    cy = gy + cell_h + 8*SCALE
    draw.text((cx, cy), v, fill=TEXT_MAIN+(255,), font=f(26, bold=True))

# Highlight box
hx = table_x + padding + 2*col_w - 4*SCALE
hy = gy - 4*SCALE
hw = col_w + 8*SCALE
hh = cell_h*2 + 8*SCALE
draw.rectangle([hx, hy, hx+hw, hy+hh], outline=HIGHLIGHT+(220,), width=3*SCALE)

# 日主 annotation
draw.text((hx+20*SCALE, hy+hh+8*SCALE), "← 日主（你自己）", fill=HIGHLIGHT+(230,), font=f(18))

# Bottom text
draw.text((table_x+30*SCALE, hy+hh+48*SCALE), "上面是天干（表面性格）下面是她支（内在底色）", fill=TEXT_LIGHT+(200,), font=f(16))

out = "/home/ubuntu/命理学/第0课-四柱表-HD.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
