---
name: bazi-cover-generator
title: 八字公众号封面图生成器
description: 批量生成八字入门系列公众号封面图，椰子配色 + Noto Sans CJK字体 + 无条纹渐变
---

## 触发条件
用户需要为八字入门课程系列生成公众号封面图（多张或单张）

## 使用步骤
1. 读取 `~/命理学/docs/八字/` 下对应markdown文件，提取标题
2. 运行 `~/命理学/generate_all_covers.py`（已存在）
3. 输出到 `~/命理学/` 目录，文件名为 `第X课-标题.png`

## 修改特定封面
编辑 `~/命理学/generate_all_covers.py` 中 `covers` 列表，修改对应课的 title/subtitle/tag，然后重新运行

## 单张生成
使用 `~/命理学/make_cover_coconut.py` 命令行工具：
```bash
cd ~/命理学 && /usr/bin/python3 make_cover_coconut.py "标题" --sub "副标题" --tag "八字入门 · 第X课" --output "输出.png"
```

## 技术细节
- 分辨率: 2400×1256 (2x)
- 字体: Noto Sans CJK SC (index=2)，粗体用 Bold.ttc
- 配色: 暖白底色 + 椰壳棕文字 + 焦糖金点缀
- 渐变: 径向柔光（非逐行绘制，避免条纹）
- 纹理: 仅圆点，无横线
- Python依赖: Pillow, 系统python (/usr/bin/python3)

## 配色方案
- BG_TOP: (255, 248, 240) warm cream
- BG_BOT: (242, 232, 215) deeper cream
- TEXT_MAIN: (61, 43, 31) dark brown
- TEXT_SUB: (115, 88, 62) medium brown
- TEXT_BOTTOM: (155, 125, 95) lighter brown
- ACCENT: (193, 127, 78) caramel
- ACCENT_LIGHT: (210, 180, 140) tan

## 常见问题
- **条纹/横线问题**：使用 Image.alpha_composite 代替逐行 draw.rectangle
- **小字模糊**：升级到2x分辨率(2400×1256)，改用 Noto Sans CJK SC 字体
- **字体路径**：Noto Sans CJK SC 在 `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` (index=2)
- **Noto安装**：`sudo apt-get install -y fonts-noto-cjk`
