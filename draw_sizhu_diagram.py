#!/usr/bin/env python3
"""绘制四柱结构图：天干在上，地支在下"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 800, 480
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

img = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# === Colors ===
CREAM = (255, 248, 240)
PEACH = (251, 233, 231)
ORANGE = (230, 81, 0)
DARK_BROWN = (61, 43, 31)
MED_BROWN = (93, 64, 55)
LIGHT_BROWN = (141, 110, 99)
RED_BROWN = (191, 54, 12)

# Background
draw.rectangle([0, 0, W, H], fill=CREAM)

# === Title ===
draw.text((280, 25), "四柱结构 — 天干在上，地支在下", fill=DARK_BROWN, font=f(24, bold=True))

# === Column positions ===
cols = [
    {"name": "年柱", "tg": "丙", "dz": "午", "x": 100, "label": "↑ 年份"},
    {"name": "月柱", "tg": "庚", "dz": "子", "x": 260, "label": "↑ 月份"},
    {"name": "日柱", "tg": "甲", "dz": "寅", "x": 420, "label": "↑ 你自己（核心）"},
    {"name": "时柱", "tg": "戊", "dz": "辰", "x": 580, "label": "↑ 时辰"},
]
CW = 100  # column width
CH = 65   # cell height

# === Left labels ===
draw.text((15, 148), "天干", fill=RED_BROWN, font=f(20, bold=True))
draw.text((10, 180), "像天气", fill=LIGHT_BROWN, font=f(16))
draw.text((20, 205), "外面看到的", fill=LIGHT_BROWN, font=f(16))
draw.text((15, 255), "地支", fill=RED_BROWN, font=f(20, bold=True))
draw.text((10, 288), "像地基", fill=LIGHT_BROWN, font=f(16))
draw.text((20, 313), "骨子里的底色", fill=LIGHT_BROWN, font=f(16))

# === Arrows from labels to columns ===
# Arrow from 天干 to top row
draw.line([(90, 165), (100, 165)], fill=ORANGE, width=2)
draw.polygon([(100, 162), (107, 165), (100, 168)], fill=ORANGE)
# Arrow from 地支 to bottom row
draw.line([(90, 275), (100, 275)], fill=ORANGE, width=2)
draw.polygon([(100, 272), (107, 275), (100, 278)], fill=ORANGE)

for col in cols:
    x = col["x"]

    # === Column header ===
    tw = draw.textlength(col["name"], font=f(20, bold=True))
    draw.text((x + (CW - tw)/2, 80), col["name"], fill=ORANGE, font=f(20, bold=True))

    # === Top cell (天干) ===
    if col["name"] == "日柱":
        # Highlight with dashed border
        draw.rectangle([x-5, 115, x+CW+5, 265], outline=ORANGE, width=3)
    draw.rectangle([x, 130, x+CW, 195], fill=CREAM, outline=ORANGE, width=2)
    tw = draw.textlength(col["tg"], font=f(32, bold=True))
    draw.text((x + (CW - tw)/2, 140), col["tg"], fill=DARK_BROWN, font=f(32, bold=True))

    # === Bottom cell (地支) ===
    draw.rectangle([x, 195, x+CW, 260], fill=PEACH, outline=ORANGE, width=2)
    tw = draw.textlength(col["dz"], font=f(32, bold=True))
    draw.text((x + (CW - tw)/2, 205), col["dz"], fill=DARK_BROWN, font=f(32, bold=True))

    # === Bottom label ===
    color = ORANGE if "核心" in col["label"] else LIGHT_BROWN
    tw = draw.textlength(col["label"], font=f(16))
    draw.text((x + (CW - tw)/2, 272), col["label"], fill=color, font=f(16))

# === 日干标注 ===
# Arrow pointing to 日柱的天干 (甲)
draw.line([(530, 165), (555, 165)], fill=ORANGE, width=3)
draw.polygon([(530, 160), (522, 165), (530, 170)], fill=ORANGE)

# "日干" label
draw.text((558, 143), "日干", fill=ORANGE, font=f(20, bold=True))
draw.text((558, 168), "（日柱上面的天干=你）", fill=ORANGE, font=f(14))

# === Bottom note ===
note = "每个柱分上下两个字：上面叫天干，下面叫地支"
tw = draw.textlength(note, font=f(16))
draw.text(((W - tw)/2, 350), note, fill=MED_BROWN, font=f(16))

detail = "天干 = 外面看到的（像天气），地支 = 骨子里的底色（像地基）"
tw = draw.textlength(detail, font=f(14))
draw.text(((W - tw)/2, 380), detail, fill=LIGHT_BROWN, font=f(14))

out = os.path.expanduser("~/命理学/四柱结构图.png")
img.save(out)
print(f"✅ {out}")
