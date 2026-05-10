#!/usr/bin/env python3
"""生成八字入门系列公众号封面图 - 椰子配色主题"""
from PIL import Image, ImageDraw, ImageFont
import math, os, sys, random

W, H = 1200, 628
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def f(sz):
    return ImageFont.truetype(FONT, sz)

def make_cover(title, subtitle, lesson_tag, author="椰子", output="cover.png"):
    random.seed(42)

    # === 椰子配色方案 ===
    BG_TOP = (255, 248, 240)       # warm cream
    BG_BOT = (245, 235, 220)       # slightly deeper cream
    TEXT_MAIN = (61, 43, 31)       # dark brown
    TEXT_SUB = (130, 100, 75)      # medium brown
    TEXT_BOTTOM = (160, 130, 100)  # lighter brown
    ACCENT = (193, 127, 78)        # caramel/golden brown
    ACCENT_LIGHT = (210, 180, 140) # tan
    ACCENT_GLOW = (230, 210, 180)  # very light gold
    SHADOW = (0, 0, 0, 25)

    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # === WARM CREAM GRADIENT ===
    for y in range(H):
        r = y / H
        rc = int(BG_TOP[0] + (BG_BOT[0]-BG_TOP[0]) * r)
        gc = int(BG_TOP[1] + (BG_BOT[1]-BG_TOP[1]) * r)
        bc = int(BG_TOP[2] + (BG_BOT[2]-BG_TOP[2]) * r)
        draw.rectangle([0, y, W, y], fill=(rc, gc, bc, 255))

    # === TEXTURE: tiny warm dots ===
    for _ in range(200):
        x, y = random.randint(0, W), random.randint(0, H)
        draw.ellipse([x, y, x+1, y+1], fill=(200, 180, 155, random.randint(8, 20)))

    # === COCONUT SHELL HINT: subtle half-circle top-right ===
    draw.ellipse([W-350, -180, W+80, 300], outline=ACCENT_LIGHT + (20,), width=3)

    # === COCONUT SHELL HINT: subtle arc bottom-left ===
    draw.ellipse([-60, H-300, 140, H-60], outline=ACCENT_LIGHT + (15,), width=2)

    # === ACCENT LINES ===
    # Gold accent line
    draw.rectangle([80, 210, 200, 214], fill=ACCENT + (200,))
    # Vertical accent
    draw.rectangle([80, 222, 83, 380], fill=ACCENT + (160,))

    # === TOP-RIGHT DOTS ===
    for i, (x, y) in enumerate([(W-130, 70), (W-112, 70), (W-94, 70)]):
        c = ACCENT_LIGHT if i < 2 else ACCENT
        draw.ellipse([x, y, x+6, y+6], fill=c + (160,))

    # === DECORATIVE: coconut leaf hint - gentle curve ===
    for t in range(0, 100, 3):
        rad = math.radians(t)
        x = 100 + rad * 3
        y = 400 + rad * 1.5
        draw.ellipse([x-1, y-1, x+1, y+1], fill=ACCENT_LIGHT + (12,))

    # === WAVY HORIZON LINE (subtle) ===
    pts = [(i, H-35+int(10*math.sin(i*0.01))+int(5*math.sin(i*0.025))) for i in range(0, W, 2)]
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=ACCENT_LIGHT + (25,), width=1)

    # === SHADOW BEHIND TITLE ===
    tf = f(72)
    draw.text((84, 232), title, fill=SHADOW, font=tf)
    draw.text((83, 231), title, fill=SHADOW, font=tf)

    # === MAIN TITLE ===
    draw.text((82, 230), title, fill=TEXT_MAIN + (255,), font=tf)

    # === SUBTITLE ===
    draw.text((85, 340), subtitle, fill=TEXT_SUB + (230,), font=f(38))

    # === BOTTOM ACCENT BAR ===
    draw.rectangle([80, H-95, 130, H-91], fill=ACCENT + (220,))

    # === BOTTOM TEXT ===
    draw.text((80, H-80), lesson_tag, fill=TEXT_BOTTOM + (220,), font=f(26))
    draw.text((W-170, H-80), f"@{author}", fill=TEXT_BOTTOM + (180,), font=f(24))

    img.save(output, "PNG")
    return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成八字封面图")
    parser.add_argument("title", help="主标题")
    parser.add_argument("--sub", default="一步一步，看懂命盘", help="副标题")
    parser.add_argument("--tag", default="八字入门 · 第1课", help="底部标签")
    parser.add_argument("--author", default="椰子", help="署名")
    parser.add_argument("--output", default="cover.png", help="输出路径")
    args = parser.parse_args()
    out = make_cover(args.title, args.sub, args.tag, args.author, args.output)
    print(f"✅ {out}")
