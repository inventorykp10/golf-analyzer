# -*- coding: utf-8 -*-
# index.html에 manifest 및 apple-touch-icon 추가

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 이미 추가되어 있으면 건너뛰기
if 'manifest.json' in content:
    print("이미 manifest가 추가되어 있습니다.")
else:
    # <meta name="theme-color"> 뒤에 추가
    manifest_tags = '''  <meta name="theme-color" content="#2d5016">
  <link rel="manifest" href="manifest.json">
  <link rel="apple-touch-icon" href="icon-192x192.png">'''

    content = content.replace(
        '  <meta name="theme-color" content="#2d5016">',
        manifest_tags
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("manifest.json 및 아이콘 링크 추가 완료!")
