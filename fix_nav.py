# -*- coding: utf-8 -*-
# index.html 하단 메뉴 수정 스크립트
# 홈, 라운드, 설정만 남기기

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    # 1. CSS: repeat(4, 1fr) -> repeat(3, 1fr) (bottom-nav 부분만)
    if 'grid-template-columns: repeat(4, 1fr);' in lines[i] and i > 0 and 'bottom-nav' in ''.join(lines[max(0,i-10):i]):
        new_lines.append(lines[i].replace('repeat(4, 1fr)', 'repeat(3, 1fr)'))
        i += 1
        continue

    # 2. pages 배열 수정
    if "{ icon: '\U0001f3e0', label: '\ud604' }," in lines[i]:
        new_lines.append("        { icon: '\U0001f3e0', label: '\ud604', pageIndex: 0 },\n")
        i += 1
        new_lines.append("        { icon: '\u26f3', label: '\ub77c\uc6e8\ub4dc', pageIndex: 1 },\n")
        i += 1
        i += 1  # 통계 건너뛰기
        i += 1  # 기록 건너뛰기
        new_lines.append("        { icon: '\u2699\ufe0f', label: '\uc11c\uc815', pageIndex: 4 }\n")
        i += 1
        continue

    # 3. onclick: appState.currentPage = index -> page.pageIndex
    if 'appState.currentPage = index;' in lines[i]:
        new_lines.append(lines[i].replace('appState.currentPage = index;', 'appState.currentPage = page.pageIndex;'))
        i += 1
        continue

    new_lines.append(lines[i])
    i += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("수정 완료! 홈, 라운드, 설정만 남겼습니다.")
