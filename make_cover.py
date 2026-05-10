#!/usr/bin/env python3
"""生成八字入门系列公众号封面图"""
from PIL import Image, ImageDraw, ImageFont
import math, os, sys, random

W, H = 1200, 628
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def f(sz):
    return ImageFont.truetype(FONT, sz)

def make_cover(title, subtitle, lesson_tag, author="椰子", output="cover.png"):
    random.seed(42 + hash(lesson_tag) % 1000)  # per-lesson texture variation
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background gradient
    for y in range(H):
        r = y / H
        draw.rectangle([0, y, W, y], fill=(int(15+r*8), int(18+r*12), int(30+r*20), 255))

    # Texture dots
    for _ in range(300):
        x, y = random.randint(0, W), random.randint(0, H)
        draw.ellipse([x, y, x+1, y+1], fill=(255, 255, 255, random.randint(5, 15)))

    # Decorations
    draw.ellipse([W-380, -150, W+50, 280], outline=(180, 150, 80, 18), width=2)
    draw.ellipse([-80, H-250, 120, H-130], outline=(180, 150, 80, 12), width=1)

    # Accent lines
    draw.rectangle([80, 210, 200, 212], fill=(200, 170, 90, 80))
    draw.rectangle([80, 220, 82, 380], fill=(200, 170, 90, 50))

    # Top-right dots
    for i, (x, y) in enumerate([(W-130, 70), (W-112, 70), (W-94, 70)]):
        draw.ellipse([x, y, x+5, y+5], fill=(180, 150, 80, 60 if i < 2 else 120))

    # Mountain line
    pts = [(i, H-30+int(15*math.sin(i*0.008))+int(8*math.sin(i*0.02))) for i in range(0, W, 2)]
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=(100, 95, 85, 18), width=1)

    # Title shadow + text
    tf = f(72)
    for dx, dy in [(2,2),(3,3)]:
        draw.text((82+dx, 230+dy), title, fill=(0,0,0,60), font=tf)
    draw.text((82, 230), title, fill=(235, 220, 185, 255), font=tf)

    # Subtitle
    draw.text((85, 315), subtitle, fill=(200, 185, 155, 255), font=f(38))

    # Bottom bar
    draw.rectangle([80, H-95, 130, H-91], fill=(200, 170, 90, 200))

    # Bottom text
    draw.text((80, H-80), lesson_tag, fill=(180, 170, 150, 230), font=f(26))
    draw.text((W-170, H-80), f"@{author}", fill=(160, 150, 130, 180), font=f(24))

    # Arc
    for t in range(0, 60, 2):
        rad = math.radians(t)
        draw.ellipse([30+rad*4-1, 30+rad*2-1, 30+rad*4+1, 30+rad*2+1], fill=(200, 170, 90, 18))

    img.save(output, "PNG")
    return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成八字封面图")
    parser.add_argument("title", help="主标题，如'十天干是什么'")
    parser.add_argument("--sub", default="一步一步，看懂命盘", help="副标题")
    parser.add_argument("--tag", default="八字入门 · 第1课", help="底部标签")
    parser.add_argument("--author", default="椰子", help="署名")
    parser.add_argument("--output", default="cover.png", help="输出路径")
    args = parser.parse_args()
    out = make_cover(args.title, args.sub, args.tag, args.author, args.output)
    print(f"✅ 封面已生成：{out}")
