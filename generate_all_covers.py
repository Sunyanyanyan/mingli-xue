#!/usr/bin/env python3
"""批量生成八字入门系列封面图 - 椰子配色 + Noto Sans + 无条纹渐变"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H = 2400, 1256
random.seed(42)

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def f(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, sz, index=2)

# === 椰子配色 ===
BG_TOP = (255, 248, 240)
BG_MID = (248, 240, 228)
BG_BOT = (242, 232, 215)
TEXT_MAIN = (61, 43, 31)
TEXT_SUB = (115, 88, 62)
TEXT_BOTTOM = (155, 125, 95)
ACCENT = (193, 127, 78)
ACCENT_LIGHT = (210, 180, 140)
SHADOW = (0, 0, 0, 22)

def make_cover(title, subtitle, tag, output):
    """Generate one cover image"""
    # === BUILD SMOOTH GRADIENT ===
    base = Image.new('RGBA', (W, H), BG_TOP + (255,))

    # Radial vignette
    grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    cx, cy = W//2, H//3
    max_r = int(math.sqrt(W*W + H*H))
    for r in range(max_r, 0, -4):
        alpha = max(0, min(15, int(15 * (1 - r / max_r))))
        if alpha > 0:
            gdraw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BG_MID + (alpha,))

    img = Image.alpha_composite(base, grad)
    draw = ImageDraw.Draw(img)

    # === TEXTURE: tiny dots ===
    for _ in range(500):
        x, y = random.randint(0, W), random.randint(0, H)
        a = random.randint(6, 16)
        draw.ellipse([x, y, x+2, y+2], fill=(200, 185, 165, a))

    # === DECORATIVE CIRCLES ===
    draw.ellipse([W-350, -180, W+80, 300], outline=ACCENT_LIGHT + (28,), width=4)
    draw.ellipse([-60, H-300, 140, H-60], outline=ACCENT_LIGHT + (20,), width=3)

    # === ACCENT LINES ===
    draw.rectangle([160, 410, 400, 416], fill=ACCENT + (220,))
    draw.rectangle([160, 428, 164, 680], fill=ACCENT + (180,))

    # === TOP-RIGHT DOTS ===
    for i, (x, y) in enumerate([(W-260, 140), (W-224, 140), (W-188, 140)]):
        c = ACCENT_LIGHT if i < 2 else ACCENT
        draw.ellipse([x, y, x+12, y+12], fill=c + (180,))

    # === WAVY HORIZON ===
    pts = [(i, H-70+int(20*math.sin(i*0.01))+int(10*math.sin(i*0.025))) for i in range(0, W, 4)]
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=ACCENT_LIGHT + (35,), width=2)

    # === MAIN TITLE ===
    tf = f(128, bold=True)
    draw.text((162, 452), title, fill=SHADOW, font=tf)
    draw.text((160, 450), title, fill=TEXT_MAIN + (255,), font=tf)

    # === SUBTITLE ===
    draw.text((168, 630), subtitle, fill=TEXT_SUB + (245,), font=f(68))

    # === BOTTOM BAR ===
    draw.rectangle([160, H-180, 260, H-174], fill=ACCENT + (230,))

    # === BOTTOM TEXT ===
    draw.text((160, H-150), tag, fill=TEXT_BOTTOM + (240,), font=f(52))
    draw.text((W-340, H-150), "@椰子", fill=TEXT_BOTTOM + (200,), font=f(48))

    # === LEAF CURVE ===
    for t in range(0, 100, 3):
        rad = math.radians(t)
        draw.ellipse([200+rad*6-1, 780+rad*3-1, 200+rad*6+1, 780+rad*3+1], fill=ACCENT_LIGHT + (18,))

    # === TOP-LEFT DECO ===
    for t in range(0, 80, 2):
        rad = math.radians(t)
        draw.ellipse([60+rad*6-1, 60+rad*3-1, 60+rad*6+1, 60+rad*3+1], fill=ACCENT + (14,))

    img.save(output, "PNG")
    return output

# === ALL LESSONS ===
covers = [
    ("什么是八字？", "先看出厂设置，再谈命运怎么走", "八字入门 · 第1课", "第1课-什么是八字.png"),
    ("天干", "十个天干，十种性格能量", "八字入门 · 第2课", "第2课-天干.png"),
    ("地支", "你的起点，决定你的姿势", "八字入门 · 第3课", "第3课-地支.png"),
    ("五行关系", "生克之间，全是生活", "八字入门 · 第4课", "第4课-五行关系.png"),
    ("藏干", "看不到的，才是真相", "八字入门 · 第5课", "第5课-藏干.png"),
    ("十神（上）", "谁在管你，谁在帮你", "八字入门 · 第6课", "第6课-十神-上.png"),
    ("十神（下）", "才华、财富、朋友怎么看", "八字入门 · 第7课", "第7课-十神-下.png"),
    ("十神组合看性格", "单味不成菜，组合才是你", "八字入门 · 第8课", "第8课-十神组合看性格.png"),
    ("大运", "十年磨一剑，好运何时来", "八字入门 · 第9课（上）", "第9课-大运-上.png"),
    ("大运怎么看", "一步大运，十年风景", "八字入门 · 第9课（下）", "第9课-大运-下.png"),
    ("流年怎么看", "今年刮什么风", "八字入门 · 第10课", "第10课-流年.png"),
    ("旺衰强弱", "你电池多大，能量多足", "八字入门 · 第11课", "第11课-旺衰强弱.png"),
    ("用神忌神", "充电器和耗电器", "八字入门 · 第12课", "第12课-用神忌神.png"),
    ("格局入门", "八字的主线剧情", "八字入门 · 第13课", "第13课-格局入门.png"),
    ("神煞", "八字里的标点符号", "八字入门 · 第15课", "第15课-神煞.png"),
]

output_dir = "/home/ubuntu/命理学"
for title, subtitle, tag, fname in covers:
    path = os.path.join(output_dir, fname)
    print(f"生成: {fname} ... ", end="", flush=True)
    make_cover(title, subtitle, tag, path)
    size = os.path.getsize(path)
    print(f"OK ({size//1024} KB)")

print("\n全部完成！")
