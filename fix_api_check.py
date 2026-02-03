# -*- coding: utf-8 -*-
# API 키 검증 코드 수정

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 검증 코드에서 실제 키 비교 제거
old_check = """if (!GEMINI_API_KEY || GEMINI_API_KEY === 'AIzaSyDq99TUnFbwa_hWewjE4HqCzzWgsR_nNoY') {
        alert('❗ API 키가 설정되지 않았습니다.');
        return;
      }"""

new_check = """if (!GEMINI_API_KEY) {
        alert('❗ API 키가 설정되지 않았습니다.');
        return;
      }"""

content = content.replace(old_check, new_check)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ API 키 검증 코드 수정 완료!")
