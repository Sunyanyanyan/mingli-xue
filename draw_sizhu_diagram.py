#!/usr/bin/env python3
"""四柱结构图精简版"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 780, 380
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

img = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

CREAM = (255, 248, 240)
PEACH = (251, 233, 231)
ORANGE = (230, 81, 0)
DARK = (61, 43, 31)
LIGHT_B = (141, 110, 99)

draw.rectangle([0, 0, W, H], fill=CREAM)

draw.text((W//2-140, 20), "四柱结构  —  天干在上，地支在下", fill=DARK, font=f(22, bold=True))

cols = [
    {"name": "年柱", "tg": "丙", "dz": "午", "x": 65},
    {"name": "月柱", "tg": "庚", "dz": "子", "x": 215},
    {"name": "日柱", "tg": "甲", "dz": "寅", "x": 365},
    {"name": "时柱", "tg": "戊", "dz": "辰", "x": 515},
]
CW = 100
CH = 65

for col in cols:
    x = col["x"]
    tw = draw.textlength(col["name"], font=f(18, bold=True))
    draw.text((x + (CW - tw)/2, 70), col["name"], fill=ORANGE, font=f(18, bold=True))

    if col["name"] == "日柱":
        draw.rectangle([x-5, 100, x+CW+5, 245], outline=ORANGE, width=3)
    draw.rectangle([x, 115, x+CW, 180], fill=CREAM, outline=ORANGE, width=2)
    tw = draw.textlength(col["tg"], font=f(30, bold=True))
    draw.text((x + (CW - tw)/2, 125), col["tg"], fill=DARK, font=f(30, bold=True))

    draw.rectangle([x, 180, x+CW, 245], fill=PEACH, outline=ORANGE, width=2)
    tw = draw.textlength(col["dz"], font=f(30, bold=True))
    draw.text((x + (CW - tw)/2, 190), col["dz"], fill=DARK, font=f(30, bold=True))

# 日干标注：从右边指进来
draw.line([(485, 145), (510, 145)], fill=ORANGE, width=3)
draw.polygon([(485, 140), (478, 145), (485, 150)], fill=ORANGE)
draw.text((515, 120), "日干", fill=ORANGE, font=f(20, bold=True))
draw.text((515, 148), "（= 你）", fill=ORANGE, font=f(16))

out = os.path.expanduser("~/命理学/四柱结构图.png")
img.save(out)
print(f"✅ {out}")
