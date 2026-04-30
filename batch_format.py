#!/usr/bin/env python3
"""
一键批量排版 — 将所有课程文章转成公众号可用的 HTML

用法:
  python3 batch_format.py

会扫描 docs/八字/ 下所有 .md 文件（排除 .wechat.md 和 00-开头的），
生成对应的 .wechat.html 文件。
"""

import os, sys, re, glob
from pathlib import Path
import markdown

def convert_to_wechat(md_path, out_path=None):
    md_path = Path(md_path).expanduser()
    if not md_path.exists():
        return None

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem
    
    # 判断是否为小贴士
    is_tip = '小贴士' in md_path.name or '口诀' in md_path.name

    # Markdown → HTML
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'attr_list', 'footnotes']
    )

    # 样式注入
    html_body = html_body.replace('<table>', '<table style="border-collapse:collapse;width:100%;margin:1em 0;font-size:15px;">')
    html_body = html_body.replace('<th>', '<th style="background:#efebe9;padding:10px 12px;border:1px solid #d7ccc8;text-align:center;font-weight:600;color:#3e2723;">')
    html_body = html_body.replace('<td>', '<td style="padding:8px 12px;border:1px solid #d7ccc8;text-align:center;color:#4e342e;">')
    html_body = html_body.replace('<pre><code', '<pre style="background:#2d2d2d;color:#f8f8f2;padding:16px;border-radius:6px;overflow-x:auto;font-size:14px;line-height:1.5;"><code')
    html_body = html_body.replace('<code>', '<code style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-size:14px;color:#c7254e;">')
    html_body = html_body.replace('<blockquote>', '<blockquote style="border-left:4px solid #e65100;background:#fff3e0;padding:12px 16px;margin:1em 0;border-radius:0 6px 6px 0;color:#5d4037;">')
    html_body = html_body.replace('<img ', '<img style="max-width:100%;border-radius:6px;margin:1em 0;" ')
    html_body = html_body.replace('<hr>', '<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e65100,transparent);margin:2em 0;">')
    html_body = html_body.replace('<h1>', '<h1 style="font-size:22px;color:#e65100;text-align:center;margin:1.5em 0 0.8em;">')
    html_body = html_body.replace('<h2>', '<h2 style="font-size:18px;color:#bf360c;margin:1.5em 0 0.5em;padding-bottom:6px;border-bottom:1px solid #fbe9e7;">')
    html_body = html_body.replace('<h3>', '<h3 style="font-size:16px;color:#5d4037;margin:1.2em 0 0.4em;">')

    # 构建完整 HTML
    badge = '📝 小贴士' if is_tip else '📖 课程'
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
</head>
<body style="max-width:640px;margin:0 auto;padding:20px 16px 30px;font-family:-apple-system,'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.9;color:#3e2723;background:#fff;">

<div style="text-align:center;padding:16px 0 8px;">
  <div style="font-size:32px;margin-bottom:4px;">🥥</div>
  <h1 style="font-size:22px;color:#e65100;margin:0;font-weight:700;">椰子要破壳</h1>
  <p style="color:#8d6e63;font-size:13px;margin:4px 0 0;letter-spacing:1px;">用生活讲八字 · {badge}</p>
</div>

<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e65100,transparent);margin:16px 0;">

{html_body}

<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e65100,transparent);margin:24px 0;">

<div style="text-align:center;color:#8d6e63;font-size:13px;padding:8px 0;line-height:1.6;">
  <p style="margin:4px 0;">📖 <a href="https://sunyanyanyan.github.io/mingli-xue/" style="color:#e65100;text-decoration:none;">椰子要破壳 · 八字入门</a></p>
  <p style="margin:4px 0;color:#bcaaa4;">原创文章 · 转载请联系作者</p>
</div>

</body>
</html>'''

    if out_path is None:
        out_path = md_path.with_suffix('.wechat.html')
    else:
        out_path = Path(out_path)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(out_path)


def batch_convert(course_dir='docs/八字'):
    course_dir = Path(course_dir).expanduser()
    if not course_dir.exists():
        print(f"❌ 目录不存在: {course_dir}")
        return
    
    # 找所有 .md 文件，排除 index.md、00-开头、和已生成的 .wechat.md
    md_files = sorted(course_dir.glob('*.md'))
    md_files = [f for f in md_files 
                if not f.name.startswith('00-') 
                and f.suffix == '.md'
                and not f.name.endswith('.wechat.md')]
    
    if not md_files:
        print(f"❌ 没有找到课程文件")
        return
    
    converted = []
    for md_file in md_files:
        result = convert_to_wechat(md_file)
        if result:
            converted.append(result)
            print(f"  ✓ {md_file.name} → {Path(result).name}")
    
    print(f"\n✅ 共转换 {len(converted)} 篇文章")
    print(f"📂 全部文件在: {course_dir}/")
    print(f"📋 打开任意 .wechat.html → Ctrl+A 全选 → Ctrl+C 复制 → 粘贴到公众号")
    return converted


if __name__ == '__main__':
    print("🥥 椰子要破壳 · 公众号排版工具")
    print("=" * 40)
    
    # 支持指定目录
    target = sys.argv[1] if len(sys.argv) > 1 else 'docs/八字'
    batch_convert(target)
