# -*- coding: utf-8 -*-
# 결과를 Desktop에 저장

import os

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# 저장 경로: golf-analyzer폴더 상위 (Desktop이든 어디든)
save_path = os.path.join(os.path.dirname(os.path.abspath('index.html')), 'state.txt')

with open(save_path, 'w', encoding='utf-8') as out:
    out.write("=== CSS ===\n")
    for i, line in enumerate(lines):
        kw = ['page-container', '.section', 'grow', 'overflow', 'flex:', '--nav-h', 'scrollable', 'home-quick']
        if any(k in line for k in kw):
            for j in range(max(0,i-1), min(len(lines), i+3)):
                out.write(f"{'>>>' if j==i else '   '} {j+1:4d}: {lines[j]}\n")
            out.write("---\n")

    out.write("\n=== renderHomePage ===\n")
    in_func = False
    for i, line in enumerate(lines):
        if 'function renderHomePage' in line:
            in_func = True
        if in_func:
            out.write(f"{i+1:4d}: {line}\n")
            if 'window.goToPage' in line:
                break

# 저장된 경로 출력 (영문만)
print(f"Saved: {save_path}")
