#!/usr/bin/env python3
"""四柱表 - v7 垂直居中"""
from PIL import Image, ImageDraw, ImageFont
import os, math

SCALE = 2
W, H = 780*SCALE, 420*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (255, 243, 224)
CARD1 = (255, 255, 255)
CARD2 = (255, 248, 238)
TITLE = (62, 39, 35)
TEXT = (93, 64, 55)
ACCENT = (230, 81, 0)
BORDER = (232, 225, 220)
HIGHLIGHT = (191, 54, 12)

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# === 内容区高度 ≈ 380*SCALE, 垂直居中 ===
# 总内容高: 标题(38) + 间距 + 列表头(42) + 间距 + 表(2*58=116) + 标注(24) + 间距 + 底文(18) ≈ 380
# 图像高 420, 偏移 = (420-380)/2 ≈ 20
yo = 20*SCALE

# === 居中表格 ===
col_w = 120*SCALE
label_w = 80*SCALE
table_w = label_w + 4*col_w
tx = (W - table_w) // 2
ty = 70*SCALE + yo
cell_h = 58*SCALE

# === 标题 ===
draw.text((tx, yo), "八字 = 四柱 × 2", fill=TITLE+(255,), font=ft(26, bold=True))

# === 列标题 ===
for i, h in enumerate(["年柱", "月柱", "日柱", "时柱"]):
    cx = tx + label_w + i*col_w + col_w//2
    draw.text((cx-26*SCALE, ty), h, fill=TITLE+(255,), font=ft(22, bold=True))
    ax = cx - 8*SCALE
    draw.text((ax, ty+28*SCALE), "↓", fill=ACCENT+(200,), font=ft(18))

# === 行 ===
r1_top = ty + 58*SCALE
r2_top = r1_top + cell_h
right = tx + table_w

draw.rectangle([tx, r1_top, right, r1_top+cell_h], fill=CARD1+(255,), outline=BORDER+(200,), width=2)
draw.rectangle([tx, r2_top, right, r2_top+cell_h], fill=CARD2+(255,), outline=BORDER+(200,), width=2)

for i in range(1, 5):
    lx = tx + label_w + i*col_w
    draw.line([(lx, r1_top), (lx, r2_top+cell_h)], fill=BORDER+(180,), width=2)

draw.line([(tx, r1_top+cell_h), (right, r1_top+cell_h)], fill=BORDER+(200,), width=2)

# === 标签 ===
draw.text((tx+12*SCALE, r1_top+6*SCALE), "天干", fill=TITLE+(255,), font=ft(20, bold=True))
draw.text((tx+12*SCALE, r1_top+33*SCALE), "表面性格", fill=TEXT+(200,), font=ft(15))

draw.text((tx+12*SCALE, r2_top+6*SCALE), "地支", fill=TITLE+(255,), font=ft(20, bold=True))
draw.text((tx+12*SCALE, r2_top+33*SCALE), "内在底色", fill=TEXT+(200,), font=ft(15))

# === 格值 ===
for i, v in enumerate(["甲", "丙", "乙", "丁"]):
    cx = tx + label_w + i*col_w + col_w//2
    if i == 2:
        draw.text((cx-16*SCALE, r1_top+8*SCALE), v, fill=HIGHLIGHT+(255,), font=ft(30, bold=True))
    else:
        draw.text((cx-14*SCALE, r1_top+8*SCALE), v, fill=TEXT+(255,), font=ft(26))

for i, v in enumerate(["寅", "午", "丑", "亥"]):
    cx = tx + label_w + i*col_w + col_w//2
    draw.text((cx-14*SCALE, r2_top+8*SCALE), v, fill=TEXT+(255,), font=ft(26))

# === 日柱高亮 ===
hx = tx + label_w + 2*col_w - 8*SCALE
hy = r1_top - 8*SCALE
hw = col_w + 16*SCALE
hh = 2*cell_h + 16*SCALE
draw.rectangle([hx, hy, hx+hw, hy+hh], outline=HIGHLIGHT+(220,), width=3*SCALE)

ax2 = hx + hw + 10*SCALE
ay2 = hy + hh//2 - 12*SCALE
draw.line([(hx+hw+4*SCALE, ay2+14*SCALE), (ax2+6*SCALE, ay2+14*SCALE)], fill=HIGHLIGHT+(200,), width=3*SCALE)
draw.text((ax2+14*SCALE, ay2), "→ 日主（你自己）", fill=HIGHLIGHT+(230,), font=ft(20))

out = "/home/ubuntu/命理学/第0课-四柱表-v7.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
