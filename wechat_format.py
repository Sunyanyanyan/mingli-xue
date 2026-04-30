#!/usr/bin/env python3
"""
公众号排版工具 — Markdown → 微信编辑器可直接粘贴的 HTML

用法:
  python3 wechat_format.py ~/命理学/docs/八字/第7课-十神-下.md

会输出一个 .wechat.html 文件，浏览器打开 → 全选复制 → 粘贴到公众号编辑器
"""

import sys, os, re
import markdown
from pathlib import Path

def convert_to_wechat(md_path):
    md_path = Path(md_path).expanduser()
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_path}")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取标题作为文章标题
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem

    # Markdown 转 HTML
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'attr_list', 'footnotes']
    )

    # 给表格加样式
    html_body = html_body.replace('<table>', '<table style="border-collapse:collapse;width:100%;margin:1em 0;font-size:15px;">')
    html_body = html_body.replace('<th>', '<th style="background:#efebe9;padding:10px 12px;border:1px solid #d7ccc8;text-align:center;font-weight:600;color:#3e2723;">')
    html_body = html_body.replace('<td>', '<td style="padding:8px 12px;border:1px solid #d7ccc8;text-align:center;color:#4e342e;">')
    
    # 给代码块加样式
    html_body = html_body.replace('<pre><code', '<pre style="background:#2d2d2d;color:#f8f8f2;padding:16px;border-radius:6px;overflow-x:auto;font-size:14px;line-height:1.5;"><code')
    html_body = html_body.replace('<code>', '<code style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-size:14px;color:#c7254e;">')
    
    # 给引用加样式
    html_body = html_body.replace('<blockquote>', '<blockquote style="border-left:4px solid #e65100;background:#fff3e0;padding:12px 16px;margin:1em 0;border-radius:0 6px 6px 0;color:#5d4037;">')

    # 给图片加样式
    html_body = html_body.replace('<img ', '<img style="max-width:100%;border-radius:6px;margin:1em 0;" ')

    # 给 hr 加样式
    html_body = html_body.replace('<hr>', '<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e65100,transparent);margin:2em 0;">')

    # 给段落和标题加样式
    html_body = html_body.replace('<h1>', '<h1 style="font-size:22px;color:#e65100;text-align:center;margin:1.5em 0 0.8em;">')
    html_body = html_body.replace('<h2>', '<h2 style="font-size:18px;color:#bf360c;margin:1.5em 0 0.5em;padding-bottom:6px;border-bottom:1px solid #fbe9e7;">')
    html_body = html_body.replace('<h3>', '<h3 style="font-size:16px;color:#5d4037;margin:1.2em 0 0.4em;">')
    
    # 构建完整 HTML
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
</head>
<body style="max-width:640px;margin:0 auto;padding:20px;font-family:-apple-system,'Noto Sans SC','PingFang SC',sans-serif;font-size:16px;line-height:1.8;color:#3e2723;background:#fff;">

<div style="text-align:center;padding:20px 0 10px;">
  <h1 style="font-size:24px;color:#e65100;margin:0;">🥥 椰子要破壳</h1>
  <p style="color:#8d6e63;font-size:14px;margin:4px 0 0;">八字入门 · 用生活讲八字</p>
</div>

<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e65100,transparent);margin:1em 0;">

{html_body}

<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e65100,transparent);margin:2em 0;">

<div style="text-align:center;color:#8d6e63;font-size:13px;padding:10px 0;">
  <p style="margin:4px 0;">📖 完整课程：<a href="https://sunyanyanyan.github.io/mingli-xue/" style="color:#e65100;">椰子要破壳 · 八字入门</a></p>
  <p style="margin:4px 0;">原创文章 · 转载请联系作者</p>
</div>

</body>
</html>'''

    # 输出文件
    out_path = md_path.with_suffix('.wechat.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 已生成: {out_path}")
    print(f"📋 浏览器打开 → Ctrl+A 全选 → Ctrl+C 复制 → 粘贴到公众号编辑器")
    return str(out_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 wechat_format.py <markdown文件路径>")
        sys.exit(1)
    convert_to_wechat(sys.argv[1])
