#!/usr/bin/env python3
"""五层洋葱图 - v8 真洋葱型 剥开效果"""
from PIL import Image, ImageDraw, ImageFont
import os, math

SCALE = 2
W, H = 560*SCALE, 580*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (255, 243, 224)
TITLE = (62, 39, 35)
TEXT = (93, 64, 55)

# 从外到内 - 层颜色越来越深
outer_colors = [
    (255, 210, 170),   # 天干 - 最浅
    (245, 195, 150),   # 地支
    (235, 175, 130),   # 藏干
    (220, 155, 110),   # 五行
    (200, 130, 85),    # 十神 - 最深
]

# 剥开翻起的"瓣"颜色（稍亮）
peel_colors = [
    (255, 220, 185),
    (250, 210, 170),
    (240, 195, 155),
    (230, 175, 135),
    None,  # 最内层无剥开
]

# 文字颜色 - 外层文字深色，内层文字浅色
text_colors = [
    (62, 39, 35),      # 深棕
    (62, 39, 35),
    (62, 39, 35),
    (62, 39, 35),
    (255, 243, 224),   # 最内层用浅色
]

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# === 标题 ===
draw.text((W//2-130*SCALE, 15*SCALE), "八字五层结构", fill=TITLE+(255,), font=ft(24, bold=True))

# === 同心圆角矩形（洋葱截面） ===
# 从最外层到最内层
cx, cy = W//2, H//2 + 10*SCALE  # 中心点

# 各层半径 (宽度一半)
radii = [240, 190, 145, 100, 58]  # 从外到内 *SCALE

# 各层圆角
roundness = [30, 25, 20, 15, 10]  # *SCALE

labels = [
    ("第1层", "天干", "表面的你"),
    ("第2层", "地支", "骨子里的你"),
    ("第3层", "藏干", "你藏着的那面"),
    ("第4层", "五行生克", "力量怎么互动"),
    ("第5层", "十神", "谁帮你·谁压你"),
]

# 从最外层开始画
for i in range(5):
    r = radii[i] * SCALE
    rad = roundness[i] * SCALE
    
    x1 = cx - r
    y1 = cy - r
    x2 = cx + r
    y2 = cy + r
    
    if i < 4:
        # === 外层：画"剥开"效果 ===
        # 剥开的 flap 在右上角
        flap_w = int(r * 0.3)
        flap_h = int(r * 0.25)
        
        # 主层（去掉右上角）
        # 用路径近似：画主圆角矩形后，右上角盖一个白色三角（剥开效果）
        # 先画完整的圆角矩形
        draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=outer_colors[i]+(255,), outline=(200,170,140)+(180,), width=3)
        
        # 右上角剥开 flap - 三角形翻起
        # flap 顶点（翻起前的位置，在右上角）
        fx1 = x2 - flap_w
        fy1 = y1
        fx2 = x2
        fy2 = y1 + flap_h
        
        # 盖一个背景色的三角（剥掉）
        draw.polygon([(fx1, fy1), (fx2, fy1), (fx2, fy2)], fill=BG+(255,))
        
        # 画翻起的 flap（在右上角外侧）
        peel_x = x2
        peel_y = y1 - int(flap_h * 0.3)
        peel_w = flap_w
        peel_h = flap_h + int(flap_h * 0.3)
        
        # 翻起的瓣 - 带阴影
        draw.polygon([(fx2+8, fy1-8), (fx2+flap_w+8, fy1-8), (fx2+8, fy1-flap_h-8)], fill=(0,0,0,15))
        draw.polygon([(fx2, fy1), (fx2+flap_w, fy1), (fx2, fy1-flap_h)], fill=peel_colors[i]+(255,), outline=(200,170,140)+(160,), width=2)
        
        # 剥开边缘的虚线效果 - 用短线模拟
        for t in range(0, flap_w, 10):
            px = x2 - flap_w + t
            py = y1 + int((flap_h / flap_w) * t)
            draw.ellipse([px-2, py-2, px+2, py+2], fill=(255,255,255,120))
        
        # 在内层边缘画"露出"的层次线
        inner_r = radii[i+1] * SCALE
        ix1 = cx - inner_r
        iy1 = cy - inner_r
        ix2 = cx + inner_r
        iy2 = cy + inner_r
        draw.rounded_rectangle([ix1, iy1, ix2, iy2], radius=roundness[i+1]*SCALE, outline=outer_colors[i+1]+(200,), width=4)
        
    else:
        # === 最内层：实心 ===
        draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=outer_colors[i]+(255,), outline=(180,110,70)+(200,), width=3)
    
    # === 标签 ===
    # 标签在每层的左侧区域
    label_x = x1 + 12*SCALE
    label_y = y1 + 8*SCALE
    
    if i == 4:
        tc = text_colors[i]
        draw.text((label_x, label_y), labels[i][0], fill=tc+(200,), font=ft(14))
        draw.text((label_x, label_y+22*SCALE), labels[i][1], fill=tc+(255,), font=ft(22, bold=True))
        draw.text((label_x, label_y+48*SCALE), labels[i][2], fill=tc+(200,), font=ft(14))
    else:
        tc = text_colors[i]
        draw.text((label_x, label_y), labels[i][0], fill=tc+(180,), font=ft(14))
        draw.text((label_x, label_y+22*SCALE), labels[i][1], fill=tc+(255,), font=ft(22, bold=True))
        draw.text((label_x, label_y+48*SCALE), labels[i][2], fill=tc+(200,), font=ft(14))

# === 右侧标注"从外到内" ===
# 画一个弧形箭头从外指向内
draw.text((cx+radii[4]*SCALE+20*SCALE, cy-10*SCALE), "→ 一层一层\n   剥开", fill=TEXT+(180,), font=ft(16))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v8.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
