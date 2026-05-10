#!/usr/bin/env python3
"""四柱表 - v4 修正版"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 900*SCALE, 560*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (248, 246, 241)
ROW1_BG = (252, 250, 247)
ROW2_BG = (247, 244, 239)
TITLE = (48, 57, 66)
TEXT = (55, 60, 65)
TEXT_DIM = (150, 155, 160)
ACCENT = (140, 110, 80)
HIGHLIGHT = (200, 70, 50)
BORDER = (220, 215, 208)

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# === 标题 ===
draw.text((60*SCALE, 20*SCALE), "八字 = 四柱 × 2", fill=TITLE+(255,), font=f(28, bold=True))
draw.text((60*SCALE, 55*SCALE), "八个字，四个柱子，每个柱子分上下两层", fill=TEXT_DIM+(200,), font=f(18))

# === 表格布局 ===
col_w = 130*SCALE
# 表格区域
tx = 65*SCALE      # 表左
ty = 95*SCALE      # 表上
label_w = 90*SCALE  # 左侧标签宽度
cell_h = 62*SCALE

# 列标题
headers = ["年柱", "月柱", "日柱", "时柱"]
for i, h in enumerate(headers):
    cx = tx + label_w + i*col_w
    draw.text((cx, ty+2*SCALE), h, fill=TITLE+(255,), font=f(26, bold=True))
    # 箭头
    ax = cx + col_w//2 - 12*SCALE
    draw.text((ax, ty+34*SCALE), "↓", fill=ACCENT+(200,), font=f(22))

# 表体
r1_y = ty + 70*SCALE
r2_y = r1_y + cell_h
row_right = tx + label_w + 4*col_w

# 行背景
draw.rectangle([tx, r1_y, row_right, r1_y+cell_h], fill=ROW1_BG+(255,), outline=BORDER+(200,), width=2)
draw.rectangle([tx, r2_y, row_right, r2_y+cell_h], fill=ROW2_BG+(255,), outline=BORDER+(200,), width=2)

# 列分隔线
for i in range(1, 5):
    lx = tx + label_w + i*col_w
    draw.line([(lx, r1_y), (lx, r2_y+cell_h)], fill=BORDER+(180,), width=2)

# 行分隔线
draw.line([(tx, r1_y+cell_h), (row_right, r1_y+cell_h)], fill=BORDER+(200,), width=2)

# === 行标签 ===
draw.text((tx+12*SCALE, r1_y+12*SCALE), "天干", fill=TITLE+(255,), font=f(20, bold=True))
draw.text((tx+12*SCALE, r1_y+36*SCALE), "（表面性格）", fill=TEXT_DIM+(150,), font=f(14))

draw.text((tx+12*SCALE, r2_y+12*SCALE), "地支", fill=TITLE+(255,), font=f(20, bold=True))
draw.text((tx+12*SCALE, r2_y+36*SCALE), "（内在底色）", fill=TEXT_DIM+(150,), font=f(14))

# === 单元格值 ===
row1_vals = ["甲", "丙", "乙", "丁"]
row2_vals = ["寅", "午", "丑", "亥"]

for i, v in enumerate(row1_vals):
    cx = tx + label_w + i*col_w + col_w//2 - 16*SCALE
    if i == 2:
        draw.text((cx, r1_y+10*SCALE), v, fill=HIGHLIGHT+(255,), font=f(32, bold=True))
    else:
        draw.text((cx, r1_y+10*SCALE), v, fill=TEXT+(255,), font=f(28))

for i, v in enumerate(row2_vals):
    cx = tx + label_w + i*col_w + col_w//2 - 16*SCALE
    draw.text((cx, r2_y+10*SCALE), v, fill=TEXT+(255,), font=f(28))

# === 日柱高亮框 (正确位置: 第3列) ===
hx = tx + label_w + 2*col_w - 8*SCALE
hy = r1_y - 8*SCALE
hw = col_w + 16*SCALE
hh = 2*cell_h + 16*SCALE
draw.rectangle([hx, hy, hx+hw, hy+hh], outline=HIGHLIGHT+(220,), width=4*SCALE)

# 日主标注 - 从右侧箭头
anno_x = hx + hw + 15*SCALE
anno_y = hy + hh//2 - 14*SCALE
# 箭头线
draw.line([(hx+hw+4*SCALE, anno_y+14*SCALE), (anno_x+5*SCALE, anno_y+14*SCALE)], fill=HIGHLIGHT+(200,), width=3*SCALE)
draw.text((anno_x+12*SCALE, anno_y), "→ 日主（= 你自己）", fill=HIGHLIGHT+(230,), font=f(20))

# === 底部说明 ===
draw.text((tx, hy+hh+20*SCALE), "整个八字以日主为中心展开，其他三柱是你的环境背景", fill=TEXT_DIM+(180,), font=f(18))

out = "/home/ubuntu/命理学/第0课-四柱表-v4.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
