#!/usr/bin/env python3
"""五层洋葱图 - v9 竖排剥开"""
from PIL import Image, ImageDraw, ImageFont
import os, math

SCALE = 2
W, H = 520*SCALE, 600*SCALE

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def ft(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz*SCALE, index=2)

BG = (255, 243, 224)
TITLE = (62, 39, 35)
TEXT = (93, 64, 55)

# 层色: 从外到内 浅→深
colors = [
    (242, 210, 175),   # 第1层 天干
    (230, 190, 150),   # 第2层 地支
    (215, 170, 130),   # 第3层 藏干
    (195, 150, 110),   # 第4层 五行
    (170, 125, 85),    # 第5层 十神
]

# 翻起 flap 色 (各层稍亮)
flap_colors = [
    (250, 220, 190),
    (240, 205, 170),
    (228, 188, 150),
    (210, 170, 130),
    None,
]

text_colors = [
    (62, 39, 35),
    (62, 39, 35),
    (62, 39, 35),
    (255, 243, 224),
    (255, 243, 224),
]

layers = [
    ("第1层", "天干", "表面的你"),
    ("第2层", "地支", "骨子里的你"),
    ("第3层", "藏干", "你藏着的那面"),
    ("第4层", "五行生克", "力量怎么互动"),
    ("第5层", "十神", "谁帮你·谁压你"),
]

img = Image.new('RGBA', (W, H), BG + (255,))
draw = ImageDraw.Draw(img)

# 标题
draw.text((W//2-110*SCALE, 15*SCALE), "八字是一层一层剥开的", fill=TITLE+(255,), font=ft(24, bold=True))

# === 竖排洋葱截面 ===
# 总卡片高度 ≈ 420, 顶部留80, 底部留100
start_y = 80*SCALE
end_y = H - 40*SCALE
total_h = end_y - start_y  # ≈ 440

# 5层, 每层高度递增 (外层高, 内层矮)
layer_heights = [95, 88, 82, 75, 68]  # *SCALE
layer_gaps = [0, 6, 6, 6, 6]  # *SCALE

# 宽度: 外层宽, 内层窄
layer_widths = [420, 360, 300, 240, 180]  # *SCALE

# 偏移: 让每层稍微错开 (剥开效果)
offsets = [0, 8, 16, 24, 32]  # *SCALE, 向右偏移

# 从最外层画起 (天干, 最外面)
for i in range(5):
    w = layer_widths[i] * SCALE
    h = layer_heights[i] * SCALE
    offset_x = offsets[i] * SCALE
    
    # y位置 = start_y + 之前所有层顶部之和
    y_pos = start_y + sum(layer_heights[:i]) * SCALE + sum(layer_gaps[:i]) * SCALE
    
    x1 = (W - w) // 2 + offset_x - 10*SCALE  # 稍微偏右错开
    x2 = x1 + w
    y1 = y_pos
    y2 = y1 + h
    
    # 圆角半径 (外层大, 内层小)
    rad = (20 - i*2) * SCALE
    
    # 画主层
    draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=colors[i]+(255,))
    
    if i < 4:
        # === 剥开 flap: 右上角翻起 ===
        flap_w = int(w * 0.2)
        flap_h = int(h * 0.25)
        
        # 在右上角画 flap (翻起的皮)
        # flap 顶点: 从右上角向上翻
        fx = x2 - 2
        fy = y1 + 2
        # 画 flap (菱形/三角)
        f_points = [
            (fx, fy),
            (fx + flap_w, fy),
            (fx + flap_w + 10*SCALE, fy - flap_h),
            (fx + 10*SCALE, fy - flap_h + 10*SCALE),
        ]
        draw.polygon(f_points, fill=flap_colors[i]+(255,), outline=(180,140,100)+(150,), width=2)
        
        # flap 下面的阴影 (露出内层的颜色)
        inner_color = colors[i+1]
        shadow_points = [
            (fx, fy+4),
            (fx + flap_w, fy+4),
            (fx + flap_w + 8*SCALE, fy - flap_h + 8*SCALE),
            (fx + 8*SCALE, fy - flap_h + 12*SCALE),
        ]
        draw.polygon(shadow_points, fill=inner_color+(180,))
        
        # 沿剥开边缘画一个小白点虚线
        for t in range(0, flap_w, 12):
            px = fx + t
            py = fy + int((flap_h / flap_w) * t * 0.5)
            draw.ellipse([px-2, py-2, px+2, py+2], fill=(255,255,255,150))
        
        # 剥开处显示内层边缘
        inner_w = layer_widths[i+1] * SCALE
        inner_x1 = (W - inner_w) // 2 + offsets[i+1] * SCALE - 10*SCALE
        inner_x2 = inner_x1 + inner_w
        inner_y1 = y1 + int(h * 0.5)  # 内层顶部
        draw.arc([inner_x1, inner_y1, inner_x2, y2], start=0, end=180, fill=inner_color+(200,), width=2)
    
    # === 标签 ===
    tc = text_colors[i]
    lx = x1 + 12*SCALE
    ly = y1 + 8*SCALE
    
    draw.text((lx, ly), layers[i][0], fill=tc+(180,), font=ft(13))
    draw.text((lx, ly+24*SCALE), layers[i][1], fill=tc+(255,), font=ft(22, bold=True))
    draw.text((lx, ly+48*SCALE), layers[i][2], fill=tc+(200,), font=ft(14))

# 右侧标注
draw.text((W-140*SCALE, H-60*SCALE), "⇠ 从外到内\n   逐层剥开", fill=TEXT+(150,), font=ft(15))

out = "/home/ubuntu/命理学/第0课-五层洋葱-v9.png"
img.save(out, "PNG")
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
