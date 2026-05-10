#!/usr/bin/env python3
"""高分辨率封面 - 椰子配色 + Noto Sans CJK 字体"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

# === 2x 分辨率 ===
W, H = 2400, 1256
SCALE = 2  # everything coordinates are 2x

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Bold.otf"

def check_font(fpath):
    if os.path.exists(fpath):
        print(f"  ✓ Found: {fpath}")
        return fpath
    # Try finding in truetype
    alt = fpath.replace("opentype", "truetype")
    if os.path.exists(alt):
        print(f"  ✓ Found: {alt}")
        return alt
    print(f"  ✗ Not found: {fpath}")
    return None

check_font(FONT)
check_font(FONT_BOLD)

# Let's find the actual path
import subprocess
r = subprocess.run(["fc-match", "-v", "Noto Sans CJK SC"], capture_output=True, text=True)
for line in r.stdout.split("\n"):
    if "file:" in line:
        print(f"Font file: {line.strip()}")

# Use the first found path
found = None
for f in [FONT, FONT_BOLD]:
    if os.path.exists(f):
        found = f
        break
# Search for it
import glob
candidates = glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK*")
print(f"Candidates: {candidates}")
candidates2 = glob.glob("/usr/share/fonts/truetype/noto/NotoSansCJK*")
print(f"TTF candidates: {candidates2}")
