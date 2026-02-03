# -*- coding: utf-8 -*-
# 줄 번호로 직접 수정하는 스크립트

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i <= skip_until:
        continue

    # 1. CSS: bottom-nav grid 4->3 수정
    if 'repeat(4, 1fr)' in line:
        new_lines.append(line.replace('repeat(4, 1fr)', 'repeat(3, 1fr)'))
        print(f"CSS 수정: 줄 {i+1}")
        continue

    # 2. pages 배열 수정 - "const pages = [" 찾기
    if 'const pages = [' in line:
        new_lines.append(line)  # const pages = [ 그대로
        i_next = i + 1
        # 다음 줄들을 확인하면서 "];까지 건너뛰기
        j = i_next
        while j < len(lines) and '];' not in lines[j]:
            j += 1
        skip_until = j - 1  # ]; 직전까지 건너뛰기
        # 새 pages 추가
        new_lines.append("        { icon: '🏠', label: '홈', pageIndex: 0 },\n")
        new_lines.append("        { icon: '⛳', label: '라운드', pageIndex: 1 },\n")
        new_lines.append("        { icon: '⚙️', label: '설정', pageIndex: 4 }\n")
        print(f"pages 배열 수정: 줄 {i+1}")
        continue

    # 3. onclick 수정
    if 'appState.currentPage = index;' in line:
        new_lines.append(line.replace('appState.currentPage = index;', 'appState.currentPage = page.pageIndex;'))
        print(f"onclick 수정: 줄 {i+1}")
        continue

    new_lines.append(line)

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("완료! 홈, 라운드, 설정만 남겼습니다.")
