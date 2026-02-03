# -*- coding: utf-8 -*-
# 스코어카드 업로드를 카메라/갤러리 두 버튼으로 수정

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==================================================
# 1. 기존 숨김 input (갤러리용) 유지, 카메라용 input 추가
# ==================================================
# 기존: <input type="file" id="scorecard-upload" accept="image/*" ...>
# 카메라용 input 추가 (capture="environment")
OLD_INPUT = '<input type="file" id="scorecard-upload" accept="image/*" style="display:none" onchange="handleScoreCardUpload(event)">'
NEW_INPUT = """<input type="file" id="scorecard-upload" accept="image/*" style="display:none" onchange="handleScoreCardUpload(event)">
  <input type="file" id="scorecard-camera" accept="image/*" capture="environment" style="display:none" onchange="handleScoreCardUpload(event)">"""

content = content.replace(OLD_INPUT, NEW_INPUT)

# ==================================================
# 2. 기존 단일 버튼을 카메라 + 갤러리 두 버튼으로 수정
# ==================================================
# 기존 버튼 찾기
OLD_BTN = """<button class="secondary-btn" onclick="uploadScoreCard()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);">
            📸 스코어카드로 코스 등록
          </button>"""

NEW_BTN = """<button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);">
            📷 카메라로 찍기
          </button>
          <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;">
            🖼️ 갤러리에서 선택
          </button>"""

content = content.replace(OLD_BTN, NEW_BTN)

# ==================================================
# 3. JS 함수 수정: uploadCamera / uploadGallery 추가
# ==================================================
# 기존 uploadScoreCard 함수를 카메라/갤러리 두 함수로 교체
OLD_JS = """window.uploadScoreCard = function() {
      document.getElementById('scorecard-upload').click();
    };"""

NEW_JS = """window.uploadCamera = function() {
      document.getElementById('scorecard-camera').click();
    };

    window.uploadGallery = function() {
      document.getElementById('scorecard-upload').click();
    };"""

content = content.replace(OLD_JS, NEW_JS)

# ==================================================
# Save
# ==================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 카메라 + 갤러리 버튼 수정 완료!")
print("📱 카메라로 찍기 → capture='environment' (카메라 앱 직접 실행)")
print("🖼️ 갤러리에서 선택 → 기존과 동일")
