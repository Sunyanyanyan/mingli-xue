#!/usr/bin/env python3
"""四柱表 - 专业版 重新设计"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 840*SCALE, 520*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

# === 专业配色 ===
BG = (248, 246, 241)          # 暖白纸色
CARD = (255, 255, 255)        # 白色卡片
ROW1_BG = (252, 250, 247)     # 天干行底色
ROW2_BG = (247, 244, 239)     # 地支行底色
TITLE = (48, 57, 66)          # 深灰蓝 (标题)
TEXT = (55, 60, 65)           # 深灰 (正文)
TEXT_DIM = (140, 145, 150)    # 灰 (辅助)
ACCENT = (140, 110, 80)       # 暖褐 (装饰色)
HIGHLIGHT = (200, 70, 50)     # 朱红 (日主高亮)
BORDER = (220, 215, 208)      # 边框色

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# === 布局参数 ===
col_w = 130*SCALE
table_x = 60*SCALE
table_y = 70*SCALE
gy = table_y + 60*SCALE     # grid start y
cell_h = 55*SCALE

# === 顶部标题 ===
draw.text((table_x+10*SCALE, 15*SCALE), "八字 = 四柱 × 2", fill=TITLE+(255,), font=f(26, bold=True))
draw.text((table_x+10*SCALE, 44*SCALE), "八个字，四个柱子，每个分上下两层", fill=TEXT_DIM+(200,), font=f(16))

# === 列标题 ===
headers = ["年柱", "月柱", "日柱", "时柱"]
for i, h in enumerate(headers):
    cx = table_x + 65*SCALE + i*col_w
    draw.text((cx, table_y+5*SCALE), h, fill=TITLE+(255,), font=f(22, bold=True))
    # 下箭头
    draw.text((cx+20*SCALE, table_y+30*SCALE), "↓", fill=ACCENT+(200,), font=f(16))

# === 画表格 ===
# 行1: 天干
r1_y = gy
draw.rectangle([table_x, r1_y, table_x+4*col_w+55*SCALE, r1_y+cell_h], fill=ROW1_BG+(255,), outline=BORDER+(200,), width=2)
# 行2: 地支
r2_y = gy + cell_h
draw.rectangle([table_x, r2_y, table_x+4*col_w+55*SCALE, r2_y+cell_h], fill=ROW2_BG+(255,), outline=BORDER+(200,), width=2)

# 列分隔线
for i in range(1, 5):
    lx = table_x + 60*SCALE + i*col_w
    draw.line([(lx, gy), (lx, gy+2*cell_h)], fill=BORDER+(180,), width=2)

# 水平分隔线
draw.line([(table_x, gy+cell_h), (table_x+4*col_w+55*SCALE, gy+cell_h)], fill=BORDER+(200,), width=2)

# === 行标签 ===
draw.text((table_x+15*SCALE, gy+14*SCALE), "天干", fill=TITLE+(255,), font=f(18, bold=True))
draw.text((table_x+15*SCALE, gy+14*SCALE+cell_h), "地支", fill=TITLE+(255,), font=f(18, bold=True))
# 小提示
draw.text((table_x+15*SCALE, gy+35*SCALE), "表面性格", fill=TEXT_DIM+(150,), font=f(13))
draw.text((table_x+15*SCALE, gy+35*SCALE+cell_h), "内在底色", fill=TEXT_DIM+(150,), font=f(13))

# === 单元格数值 ===
row1_vals = ["甲", "丙", "乙", "丁"]
row2_vals = ["寅", "午", "丑", "亥"]

for i, v in enumerate(row1_vals):
    cx = table_x + 65*SCALE + i*col_w + col_w//2 - 16*SCALE
    if i == 2:
        draw.text((cx, gy+8*SCALE), v, fill=HIGHLIGHT+(255,), font=f(28, bold=True))
    else:
        draw.text((cx, gy+8*SCALE), v, fill=TEXT+(255,), font=f(26))

for i, v in enumerate(row2_vals):
    cx = table_x + 65*SCALE + i*col_w + col_w//2 - 16*SCALE
    draw.text((cx, gy+8*SCALE+cell_h), v, fill=TEXT+(255,), font=f(26))

# === 日柱高亮框 ===
hx = table_x + 62*SCALE + 2*col_w - 8*SCALE
hy = gy - 6*SCALE
hw = col_w + 16*SCALE
hh = 2*cell_h + 12*SCALE
draw.rectangle([hx, hy, hx+hw, hy+hh], outline=HIGHLIGHT+(220,), width=3*SCALE)

# 日主标注
draw.text((hx+20*SCALE, hy+hh+10*SCALE), "← 日主（= 你自己）", fill=HIGHLIGHT+(230,), font=f(17))

# === 底部说明 ===
draw.text((table_x+10*SCALE, hy+hh+48*SCALE), "整个八字以日主为中心展开，其他三柱是你的环境", fill=TEXT_DIM+(180,), font=f(16))

out = "/home/ubuntu/命理学/第0课-四柱表-v3.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
