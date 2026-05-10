#!/usr/bin/env python3
"""生成八字四柱表框架图 - PNG"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 800, 500
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

img = Image.new('RGBA', (W, H), (255, 248, 240, 255))
draw = ImageDraw.Draw(img)

# Colors
ACCENT = (193, 127, 78)
ACCENT_LIGHT = (210, 180, 140)
TEXT_MAIN = (61, 43, 31)
BG_CELL = (245, 235, 220)
BG_HEADER = (230, 215, 195)
LINE = (180, 160, 140)

# === Table layout ===
# Header row: 年柱  月柱  日柱  时柱
# Sub header: ↓      ↓     ↓     ↓
# Row 1: 天干 | 甲 | 丙 | 乙 | 丁
# Row 2: 地支 | 寅 | 午 | 丑 | 亥

cols = [100, 175, 300, 425, 550]  # x positions for each column
col_w = 125
table_x = 100
table_y = 80
row_h = 55
padding_left = 30

# Column headers
headers = ["年柱", "月柱", "日柱", "时柱"]
for i, h in enumerate(headers):
    cx = table_x + 20 + i * col_w
    cy = table_y + 5
    draw.text((cx, cy), h, fill=TEXT_MAIN + (255,), font=f(24, bold=True))

# Down arrows
arrows_y = table_y + 38
for i in range(4):
    cx = table_x + 45 + i * col_w
    draw.text((cx-6, arrows_y), "↓", fill=ACCENT + (255,), font=f(18))

# Table grid
grid_y_start = table_y + 68
cell_h = 52

# Draw table cells
# Row 1: labels + 天干 values
row1_label = "天干"
row1_vals = ["甲", "丙", "乙", "丁"]
# Row 2: labels + 地支 values
row2_label = "地支"
row2_vals = ["寅", "午", "丑", "亥"]

# Draw cell backgrounds
for r in range(2):
    for c in range(4):
        x1 = table_x + padding_left + (c * col_w if c > 0 else 0)
        y1 = grid_y_start + r * cell_h
        x2 = x1 + col_w
        y2 = y1 + cell_h
        if r == 0:
            fill_cell = (252, 245, 235)  # lighter for 天干
        else:
            fill_cell = (248, 238, 225)  # slightly darker for 地支
        
        draw.rectangle([x1+2, y1+2, x2-2, y2-2], fill=fill_cell + (255,))
        draw.rectangle([x1, y1, x2, y2], outline=LINE + (180,), width=2)

# Row labels
draw.text((table_x+5, grid_y_start+12), "天干", fill=ACCENT + (255,), font=f(18, bold=True))
draw.text((table_x+5, grid_y_start+12+cell_h), "地支", fill=ACCENT + (255,), font=f(18, bold=True))

# Row 1 values (天干)
for i, v in enumerate(row1_vals):
    cx = table_x + padding_left + i * col_w + col_w//2 - 10
    cy = grid_y_start + 8
    color = (200, 80, 50) if i == 2 else TEXT_MAIN  # highlight 日柱
    draw.text((cx, cy), v, fill=color + (255,), font=f(26, bold=True))

# Row 2 values (地支)
for i, v in enumerate(row2_vals):
    cx = table_x + padding_left + i * col_w + col_w//2 - 10
    cy = grid_y_start + cell_h + 8
    draw.text((cx, cy), v, fill=TEXT_MAIN + (255,), font=f(26, bold=True))

# === Highlight box around 日柱 ===
hx = table_x + padding_left + 2 * col_w - 4
hy = grid_y_start - 4
hw = col_w + 8
hh = cell_h * 2 + 8
draw.rectangle([hx, hy, hx+hw, hy+hh], outline=(230, 120, 80, 200), width=3)

# === Annotation: 日主 ===
draw.text((hx+20, hy+hh+8), "← 日主（你自己）", fill=(200, 80, 50, 230), font=f(18))

# === Bottom annotation ===
draw.text((table_x + 30, hy+hh+48), "上面是天干（表面性格） 下面是地支（内在底色）", fill=TEXT_MAIN + (180,), font=f(16))

out = "/home/ubuntu/命理学/第0课-四柱表.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
