# -*- coding: utf-8 -*-
# Gemini API로 스코어카드 이미지 읽기 기능 추가

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==================================================
# 1. CSS 추가
# ==================================================
NEW_CSS = """
    /* Scorecard Upload */
    .upload-loading-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.8);
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 3000;
      color: white;
      font-size: 18px;
      gap: 20px;
    }
    .upload-loading-overlay.active { display: flex; }
    .upload-spinner {
      width: 56px; height: 56px;
      border: 5px solid rgba(255,255,255,0.2);
      border-top-color: #7fb069;
      border-radius: 50%;
      animation: spinLoader 0.8s linear infinite;
    }
    @keyframes spinLoader { to { transform: rotate(360deg); } }
    .upload-loading-text { text-align: center; }
    .upload-loading-text p { margin: 4px 0; }
    .upload-loading-text .sub { opacity: 0.6; font-size: 14px; }
"""
content = content.replace('  </style>', NEW_CSS + '  </style>')

# ==================================================
# 2. Hidden input + Loading overlay HTML
# ==================================================
HIDDEN_HTML = """
  <input type="file" id="scorecard-upload" accept="image/*" style="display:none" onchange="handleScoreCardUpload(event)">
  <div id="upload-loading" class="upload-loading-overlay">
    <div class="upload-spinner"></div>
    <div class="upload-loading-text">
      <p style="font-size:22px;">🔍 스코어카드 분석 중...</p>
      <p class="sub">잠깐만 기다려주세요</p>
    </div>
  </div>
"""
content = content.replace('<div id="app"></div>', '<div id="app"></div>\n' + HIDDEN_HTML)

# ==================================================
# 3. 홈 페이지에 업로드 버튼 추가
# ==================================================
OLD_BTN = '<button class="secondary-btn" onclick="openCourseRegistration()">'
NEW_BTN = """<button class="secondary-btn" onclick="uploadScoreCard()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);">
            📸 스코어카드로 코스 등록
          </button>
          <button class="secondary-btn" onclick="openCourseRegistration()">"""
content = content.replace(OLD_BTN, NEW_BTN, 1)

# ==================================================
# 4. Gemini API KEY + 스코어카드 JS 함수 추가
# ==================================================
JS_CODE = """
    // ========================================
    // GEMINI API - SCORECARD UPLOAD
    // ========================================
    const GEMINI_API_KEY = 'GEMINI_KEY_PLACEHOLDER';

    window.uploadScoreCard = function() {
      document.getElementById('scorecard-upload').click();
    };

    window.handleScoreCardUpload = async function(event) {
      const file = event.target.files[0];
      if (!file) return;
      event.target.value = '';

      if (!GEMINI_API_KEY || GEMINI_API_KEY === 'GEMINI_KEY_PLACEHOLDER') {
        alert('❗ API 키가 설정되지 않았습니다.');
        return;
      }

      document.getElementById('upload-loading').classList.add('active');

      try {
        const base64Data = await fileToBase64(file);
        const mimeType = file.type;
        const extractedData = await callGeminiForScoreCard(base64Data, mimeType);
        fillCourseFromAI(extractedData);
      } catch (error) {
        console.error('Scorecard error:', error);
        alert('❌ 스코어카드 처리 실패:\\n' + error.message);
      } finally {
        document.getElementById('upload-loading').classList.remove('active');
      }
    };

    function fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    }

    async function callGeminiForScoreCard(base64Data, mimeType) {
      const URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + GEMINI_API_KEY;

      const prompt = [
        '이 스코어카드 이미지에서 골프 코스 정보를 추출하세요.',
        '반드시 아래 형식의 JSON만 응답하세요. 다른 텍스트, 설명, 마크다운 불가.',
        '{',
        '  "name": "코스 이름",',
        '  "location": "위치",',
        '  "holes": 홀수 (9 또는 18),',
        '  "par": [홀별 파 배열],',
        '  "distances_blue": [홀별 블루티 거리(미터) 배열],',
        '  "distances_white": [홀별 화이트티 거리(미터) 배열]',
        '}',
        '참고: 야드 단위면 미터로 변환(1야드=0.9144미터). 정보 없으면 거리는 0, 파는 4로 설정.'
      ].join('\\n');

      const body = {
        contents: [{
          parts: [
            {
              inlineData: {
                mimeType: mimeType,
                data: base64Data
              }
            },
            { text: prompt }
          ]
        }]
      };

      const response = await fetch(URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error('Gemini API 호출 실패: ' + response.status + ' ' + errText);
      }

      const data = await response.json();
      const text = data.candidates[0].content.parts[0].text.trim();

      const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);
      if (!jsonMatch) throw new Error('스코어카드에서 코스 정보를 찾을 수 없습니다.');

      return JSON.parse(jsonMatch[0]);
    }

    function fillCourseFromAI(data) {
      const holes = data.holes || 18;
      let par = data.par || [];
      let distBlue = data.distances_blue || [];
      let distWhite = data.distances_white || [];

      while (par.length < holes) par.push(4);
      while (distBlue.length < holes) distBlue.push(0);
      while (distWhite.length < holes) distWhite.push(0);

      appState.newCourse = {
        id: 'course_' + Date.now(),
        name: data.name || '',
        location: data.location || '',
        holes: holes,
        par: par.slice(0, holes),
        distances: {
          blue: distBlue.slice(0, holes),
          white: distWhite.slice(0, holes)
        }
      };
      appState.showCourseModal = true;
      render();
    }

"""

content = content.replace(
    '    // ========================================\n    // INIT\n    // ========================================',
    JS_CODE + '    // ========================================\n    // INIT\n    // ========================================'
)

# ==================================================
# Save
# ==================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Gemini 스코어카드 기능 추가 완료!")
print("⚠️  index.html에서 'GEMINI_KEY_PLACEHOLDER' 를 실제 키로 교체해주세요!")
