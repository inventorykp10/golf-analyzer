# -*- coding: utf-8 -*-
# ============================================================
# Galaxy S Ultra (6.8~6.9") 기준 Full Screen 적합화
# ============================================================
# Galaxy Ultra viewport (PWA mode):
#   - 화면 높이 (CSS px): ~830px
#   - status bar: ~24px
#   - Android 제스처 nav: ~4px
#   - 사용 가능: ~800px
#   - bottom nav (~60px) 제외: ~740px 유효 영역
#
# 전략:
#   1. page-container = calc(100vh - 60px), flex column
#   2. 홈/라운드시작/코스선택/티박스/새코스/Par입력/퍼팅/통계
#      → overflow: hidden (스크롤 없음), 섹션이 flex grow
#   3. 샷입력/기록/설정 → overflow-y: auto (스크롤 유지)
#   4. 버튼/섹션 크기를 vh 단위로 → 폰 크기에 맞게 자동 조정
# ============================================================

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==================================================
# 1. CSS 전체 교체 (style 안의 내용)
# ==================================================
# <style> ~ </style> 사이의 내용을 통째로 교체

import re

NEW_CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Bebas+Neue&display=swap');

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    :root {
      --green-primary: #2d5016;
      --green-secondary: #4a7c23;
      --green-light: #7fb069;
      --cream: #fffbf3;
      --sand: #e5dcc5;
      --brown: #5c4a3a;
      --red: #c44536;
      --blue: #4a90e2;
      --shadow: 0 4px 12px rgba(0,0,0,0.1);
      --nav-h: 60px; /* bottom nav 높이 */
    }

    body {
      font-family: 'Noto Sans KR', sans-serif;
      background: linear-gradient(to bottom, var(--cream) 0%, var(--sand) 100%);
      color: var(--brown);
      -webkit-font-smoothing: antialiased;
      margin: 0;
      padding: 0;
      height: 100vh;
      overflow: hidden;
    }

    #app {
      max-width: 600px;
      margin: 0 auto;
      height: 100vh;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* ========== PAGE CONTAINER ========== */
    .page-container {
      height: calc(100vh - var(--nav-h));
      display: flex;
      flex-direction: column;
      padding: 2vh 4vw;
      overflow: hidden; /* 기본: 스크롤 없음 */
    }

    /* 스크롤이 필요한 페이지용 */
    .page-container.scrollable {
      overflow-y: auto;
      padding-bottom: 2vh;
    }

    /* ========== BACK BUTTON ========== */
    .back-button {
      position: fixed;
      top: 16px;
      left: 16px;
      width: 36px;
      height: 36px;
      background: white;
      border: 2px solid var(--green-primary);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: var(--shadow);
      z-index: 999;
      font-size: 18px;
      color: var(--green-primary);
      transition: all 0.2s;
    }

    .back-button:hover {
      background: var(--green-primary);
      color: white;
    }

    /* ========== PAGE TITLE ========== */
    .page-title {
      font-size: clamp(20px, 3vh, 28px);
      font-weight: 700;
      color: var(--green-primary);
      margin-bottom: 1.5vh;
      font-family: 'Bebas Neue', cursive;
      letter-spacing: 1px;
      text-align: center;
      flex-shrink: 0;
    }

    /* ========== SECTION ========== */
    .section {
      background: white;
      padding: clamp(12px, 2vh, 20px) clamp(14px, 3vw, 20px);
      border-radius: 16px;
      box-shadow: var(--shadow);
      margin-bottom: 1.5vh;
      flex-shrink: 0;
    }

    /* 홈 페이지의 메인 섹션 (flex grow로 남은 공간 채움) */
    .section.grow {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 0;
    }

    .section-title {
      font-size: clamp(14px, 2vh, 18px);
      font-weight: 600;
      color: var(--green-primary);
      margin-bottom: 1vh;
      flex-shrink: 0;
    }

    /* ========== SHOT HEADER ========== */
    .shot-header {
      background: white;
      padding: clamp(8px, 1.2vh, 14px) clamp(10px, 2vw, 16px);
      border-radius: 12px;
      margin-bottom: 1vh;
      box-shadow: var(--shadow);
      flex-shrink: 0;
    }

    .shot-info {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 4px;
    }

    .hole-num {
      font-size: clamp(14px, 2vh, 16px);
      font-weight: 600;
      color: var(--green-primary);
    }

    .tee-badge {
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      background: var(--blue);
      color: white;
    }

    .tee-badge.white {
      background: #888;
    }

    .distance-badge {
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 12px;
      background: var(--sand);
      color: var(--brown);
    }

    .shot-number {
      font-size: clamp(15px, 2vh, 18px);
      font-weight: 700;
      color: var(--green-primary);
      margin-top: 2px;
    }

    /* ========== PREVIOUS SHOTS ========== */
    .previous-shots {
      background: var(--sand);
      padding: clamp(6px, 1vh, 10px) clamp(8px, 1.5vw, 12px);
      border-radius: 8px;
      margin-bottom: 1vh;
      font-size: 13px;
      flex-shrink: 0;
    }

    .prev-shot { margin-bottom: 3px; opacity: 0.8; }
    .prev-shot:last-child { margin-bottom: 0; }

    /* ========== INPUT SECTIONS ========== */
    .input-section {
      margin-bottom: clamp(6px, 1.2vh, 14px);
    }

    .input-section label {
      display: block;
      font-size: clamp(13px, 1.8vh, 15px);
      font-weight: 600;
      color: var(--brown);
      margin-bottom: clamp(4px, 0.7vh, 8px);
    }

    .optional-label {
      font-size: 12px;
      font-weight: 400;
      opacity: 0.6;
    }

    .text-input {
      width: 100%;
      padding: clamp(8px, 1.3vh, 12px);
      border: 2px solid var(--sand);
      border-radius: 8px;
      font-size: 16px;
      font-family: 'Noto Sans KR', sans-serif;
    }

    .text-input:focus {
      outline: none;
      border-color: var(--green-primary);
    }

    /* 거리 입력 화살표 제거 */
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    input[type="number"] { -moz-appearance: textfield; }

    .select-input {
      width: 100%;
      padding: clamp(8px, 1.3vh, 12px);
      border: 2px solid var(--sand);
      border-radius: 8px;
      font-size: 16px;
      font-family: 'Noto Sans KR', sans-serif;
      background: white;
    }

    /* ========== BUTTONS ========== */
    .primary-btn {
      width: 100%;
      padding: clamp(12px, 2vh, 18px);
      background: var(--green-primary);
      color: white;
      border: none;
      border-radius: 12px;
      font-size: clamp(15px, 2vh, 17px);
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      flex-shrink: 0;
    }

    .primary-btn:hover { background: var(--green-secondary); }
    .primary-btn:disabled { background: #ccc; cursor: not-allowed; }

    .secondary-btn {
      width: 100%;
      padding: clamp(10px, 1.6vh, 16px);
      background: white;
      color: var(--green-primary);
      border: 2px solid var(--green-primary);
      border-radius: 12px;
      font-size: clamp(14px, 1.9vh, 16px);
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      margin-bottom: 0;
      flex-shrink: 0;
    }

    .secondary-btn:hover {
      background: var(--green-light);
      color: white;
    }

    .button-group {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(6px, 1vh, 10px);
    }

    .button-group-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: clamp(6px, 1vh, 10px);
    }

    .choice-btn {
      padding: clamp(8px, 1.3vh, 12px) 4px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
      font-weight: 500;
    }

    .choice-btn:hover { border-color: var(--green-light); }

    .choice-btn.selected {
      background: var(--green-primary);
      color: white;
      border-color: var(--green-primary);
    }

    /* ========== CHECKBOX GROUP ========== */
    .checkbox-group {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(5px, 0.8vh, 8px);
    }

    .checkbox-label {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: clamp(6px, 1vh, 10px);
      background: white;
      border: 2px solid var(--sand);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 13px;
    }

    .checkbox-label:hover { border-color: var(--green-light); }

    .checkbox-label.selected {
      background: var(--green-primary);
      color: white;
      border-color: var(--green-primary);
    }

    .checkbox-label input[type="checkbox"] { display: none; }

    /* ========== INFO BOXES ========== */
    .club-recommendation {
      background: #e3f2fd;
      border-left: 4px solid var(--blue);
      padding: clamp(6px, 1vh, 10px) clamp(8px, 1.5vw, 12px);
      margin-bottom: 1vh;
      border-radius: 4px;
      font-size: 13px;
    }

    .info-box {
      background: #e3f2fd;
      border-left: 4px solid var(--blue);
      padding: clamp(6px, 1vh, 10px) clamp(8px, 1.5vw, 12px);
      margin-bottom: 1vh;
      border-radius: 4px;
      font-size: 13px;
    }

    /* ========== BOTTOM NAVIGATION ========== */
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      max-width: 600px;
      margin: 0 auto;
      height: var(--nav-h);
      background: white;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      border-top: 1px solid var(--sand);
      box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
      z-index: 1000;
    }

    .nav-btn {
      border: none;
      background: transparent;
      padding: 10px 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      cursor: pointer;
      transition: all 0.2s;
      color: var(--brown);
      opacity: 0.6;
    }

    .nav-btn.active { color: var(--green-primary); opacity: 1; }
    .nav-btn-icon { font-size: 22px; }
    .nav-btn-label { font-size: 11px; font-weight: 500; }

    /* ========== STATS ========== */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(8px, 1.5vh, 14px);
      flex: 1;
      min-height: 0;
    }

    .stat-card {
      background: white;
      padding: clamp(10px, 1.8vh, 18px) 8px;
      border-radius: 12px;
      box-shadow: var(--shadow);
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .stat-icon { font-size: clamp(22px, 3.5vh, 30px); margin-bottom: 4px; }
    .stat-label { font-size: 12px; color: var(--brown); opacity: 0.7; margin-bottom: 4px; }
    .stat-value { font-size: clamp(20px, 3vh, 26px); font-weight: 700; color: var(--green-primary); }

    .empty-state {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      opacity: 0.6;
    }

    .empty-state p { margin-bottom: 8px; }

    /* ========== ROUNDS LIST ========== */
    .rounds-list {
      display: flex;
      flex-direction: column;
      gap: clamp(8px, 1.2vh, 12px);
    }

    .round-card {
      background: white;
      padding: clamp(10px, 1.5vh, 16px);
      border-radius: 12px;
      box-shadow: var(--shadow);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .round-header-info h3 { font-size: 15px; color: var(--green-primary); margin-bottom: 3px; }
    .round-date { font-size: 12px; opacity: 0.6; }
    .round-score-info { text-align: right; }
    .total-score { font-size: clamp(22px, 3vh, 28px); font-weight: 700; color: var(--green-primary); }

    /* ========== CLUB LIST ========== */
    .club-list {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(5px, 0.8vh, 8px);
    }

    .club-item {
      padding: clamp(6px, 1vh, 10px) 8px;
      background: var(--sand);
      border-radius: 8px;
      font-size: 13px;
    }

    /* ========== MODAL ========== */
    .modal {
      display: none;
      position: fixed;
      z-index: 2000;
      left: 0; top: 0;
      width: 100%; height: 100%;
      background-color: rgba(0,0,0,0.5);
      align-items: center;
      justify-content: center;
    }

    .modal.active { display: flex; }

    .modal-content {
      background: white;
      padding: 16px;
      border-radius: 16px;
      max-width: 480px;
      width: 94%;
      max-height: 90vh;
      overflow-y: auto;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .modal-title { font-size: 20px; font-weight: 700; color: var(--green-primary); }

    .close-btn {
      font-size: 26px;
      font-weight: bold;
      color: var(--brown);
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
      width: 32px;
      height: 32px;
    }

    /* ========== COURSE SELECTION ========== */
    .course-btn {
      width: 100%;
      padding: clamp(10px, 1.5vh, 16px);
      background: white;
      border: 2px solid var(--sand);
      border-radius: 12px;
      text-align: left;
      cursor: pointer;
      margin-bottom: clamp(6px, 1vh, 12px);
      transition: all 0.2s;
    }

    .course-btn:hover { border-color: var(--green-primary); }
    .course-name { font-size: 15px; font-weight: 600; color: var(--green-primary); margin-bottom: 3px; }
    .course-details { font-size: 13px; opacity: 0.7; }

    /* ========== COURSE MANAGEMENT BUTTONS ========== */
    .btn-group { display: flex; gap: 6px; }

    .edit-btn, .delete-btn {
      padding: 6px 12px;
      border: none;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      font-family: 'Noto Sans KR', sans-serif;
    }

    .edit-btn { background: var(--blue); color: white; }
    .edit-btn:hover { background: var(--green-secondary); }
    .delete-btn { background: var(--red); color: white; }
    .delete-btn:hover { background: #a03028; }
    .course-info { flex: 1; }

    /* ========== ROUND CONTROL ========== */
    .round-control-panel {
      background: var(--sand);
      padding: clamp(8px, 1.2vh, 14px) clamp(10px, 2vw, 16px);
      border-radius: 12px;
      margin-bottom: 1vh;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }

    .round-info { font-size: 14px; opacity: 0.8; }

    .finish-round-btn {
      padding: 8px 14px;
      background: var(--red);
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
    }

    /* ========== COURSE REGISTRATION (modal) ========== */
    .hole-row {
      display: grid;
      grid-template-columns: 30px 55px 80px 80px;
      gap: 5px;
      margin-bottom: 6px;
      align-items: center;
    }

    .hole-number { text-align: center; font-weight: 600; color: var(--green-primary); font-size: 13px; }

    .hole-row select,
    .hole-row input[type="number"] {
      padding: 6px 3px;
      border: 2px solid var(--sand);
      border-radius: 6px;
      font-size: 13px;
      width: 100%;
    }

    .par-summary {
      background: var(--sand);
      padding: 10px;
      border-radius: 8px;
      margin-bottom: 12px;
    }

    .par-summary-row { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 13px; }
    .par-summary-row:last-child { margin-bottom: 0; }
    .par-summary-row.total { font-weight: 600; padding-top: 5px; border-top: 1px solid var(--brown); opacity: 0.3; }

    .section-divider { border-top: 2px solid var(--sand); margin: 12px 0; padding-top: 10px; }

    .subsection-title { font-size: 14px; font-weight: 600; color: var(--green-primary); margin-bottom: 10px; }

    .holes-header {
      display: grid;
      grid-template-columns: 30px 55px 80px 80px;
      gap: 5px;
      margin-bottom: 6px;
      font-weight: 600;
      font-size: 11px;
      color: var(--green-primary);
      text-align: center;
    }

    /* ========== HOME QUICK ACTIONS (2열) ========== */
    .home-quick-actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: clamp(6px, 1vh, 10px);
    }

    .home-quick-actions .secondary-btn { margin-bottom: 0; }

    /* ========== SCORECARD UPLOAD OVERLAY ========== */
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

# style 내용 교체
content = re.sub(
    r'(<style>)(.*?)(</style>)',
    r'\g<1>' + NEW_CSS + r'\n  \g<3>',
    content,
    flags=re.DOTALL
)

# ==================================================
# 2. 홈 페이지 HTML 수정
#    - 섹션 하나로 통합 + class="section grow"
#    - 카메라/갤러리 2열 (home-quick-actions)
#    - 버튼 사이 간격을 flexbox space-between으로 분배
# ==================================================

# 홈 페이지 innerHTML 교체
# renderHomePage 함수 안의 container.innerHTML 부분 교체
OLD_HOME_TEMPLATE = """container.innerHTML = `
        <h1 class="page-title">⛳ Golf Round Analyzer</h1>

        ${inProgressRound ? `
          <div class="section">
            <h2 class="section-title">진행 중인 라운드</h2>
            <p style="margin-bottom: 12px;">
              ${inProgressRound.course} • ${inProgressRound.holes.length}/18 홀 완료
            </p>
            <button class="primary-btn" onclick="resumeRound()">
              라운드 계속하기
            </button>
          </div>
        ` : ''}

        <div class="section">
          <h2 class="section-title">새 라운드</h2>
          <button class="primary-btn" onclick="goToPage(1)">
            🏌️ 새 라운드 시작
          </button>
        </div>

        <div class="section">
          <h2 class="section-title">빠른 메뉴</h2>
          <div class="home-quick-actions">
            <button class="secondary-btn" onclick="goToPage(2)">
              📊 통계
            </button>
            <button class="secondary-btn" onclick="goToPage(3)">
              📋 기록
            </button>
          </div>
          <button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);">
            📷 카메라로 찍기
          </button>
          <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;">
            🖼️ 갤러리에서 선택
          </button>
          <button class="secondary-btn" onclick="openCourseRegistration()">
            ➕ 새 코스 등록
          </button>
        </div>

        <div class="section" style="text-align: center;">
          <p style="opacity: 0.6; font-size: 14px;">Version 9.0.0</p>
          <p style="opacity: 0.6; font-size: 12px; margin-top: 4px;">
            테스트2 피드백 반영 • Par 입력 개선
          </p>
        </div>
      `;"""

NEW_HOME_TEMPLATE = """container.innerHTML = `
        <h1 class="page-title">⛳ Golf Round Analyzer</h1>

        ${inProgressRound ? `
          <div class="section" style="padding: 1.5vh 3vw;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
              <div>
                <div style="font-weight:600; color:var(--green-primary); font-size:15px;">${inProgressRound.course}</div>
                <div style="font-size:13px; opacity:0.7;">${inProgressRound.holes.length}/18 홀 완료</div>
              </div>
              <button class="primary-btn" onclick="resumeRound()" style="width:auto; padding:10px 18px; flex-shrink:0;">
                계속하기 →
              </button>
            </div>
          </div>
        ` : ''}

        <div class="section grow">
          <button class="primary-btn" onclick="goToPage(1)">
            🏌️ 새 라운드 시작
          </button>

          <div class="home-quick-actions">
            <button class="secondary-btn" onclick="goToPage(2)">📊 통계</button>
            <button class="secondary-btn" onclick="goToPage(3)">📋 기록</button>
          </div>

          <div class="home-quick-actions">
            <button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);">📷 카메라</button>
            <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;">🖼️ 갤러리</button>
          </div>

          <button class="secondary-btn" onclick="openCourseRegistration()">
            ➕ 새 코스 등록
          </button>
        </div>

        <div style="text-align:center; padding: 0.8vh 0; flex-shrink:0;">
          <p style="opacity: 0.5; font-size: 12px;">v9.0.0 • Par 입력 개선</p>
        </div>
      `;"""

content = content.replace(OLD_HOME_TEMPLATE, NEW_HOME_TEMPLATE)

# ==================================================
# 3. 통계 페이지: stats-grid를 flex grow로
# ==================================================
# renderStatsPage의 innerHTML에 클럽목록 섹션에 grow 추가
# 통계 페이지는: title + "최근 N라운드" + stats-grid(4장카드) + 클럽목록
# stats-grid가 flex grow하면 카드가 남은 공간 채움

OLD_STATS = """<p style="opacity: 0.7; margin-bottom: 24px;">최근 ${recentRounds.length}라운드</p>"""
NEW_STATS = """<p style="opacity: 0.7; margin-bottom: 1vh; font-size:13px;">최근 ${recentRounds.length}라운드</p>"""
content = content.replace(OLD_STATS, NEW_STATS)

# 클럽목록 섹션에 grow 클래스 추가
OLD_CLUB_SECTION = """<div class="section">
          <h2 class="section-title">클럽별 평균 거리</h2>"""
NEW_CLUB_SECTION = """<div class="section grow">
          <h2 class="section-title">클럽별 평균 거리</h2>"""
content = content.replace(OLD_CLUB_SECTION, NEW_CLUB_SECTION)

# ==================================================
# 4. 스크롤이 필요한 페이지에 scrollable 클래스 추가
#    - 샷 입력 (renderShotInput)
#    - 기록 페이지 (renderHistoryPage)
#    - 설정 페이지 (renderSettingsPage)
# ==================================================
# 각 render 함수 시작에 container.classList 추가

# renderShotInput 안에 scrollable 추가
OLD_SHOT = """    function renderShotInput(container) {
      const shot = appState.currentShot;"""
NEW_SHOT = """    function renderShotInput(container) {
      container.classList.add('scrollable');
      const shot = appState.currentShot;"""
content = content.replace(OLD_SHOT, NEW_SHOT)

# renderHistoryPage
OLD_HIST = """    function renderHistoryPage(container) {
      const completedRounds = appState.data.rounds.filter(r => r.status === 'completed');"""
NEW_HIST = """    function renderHistoryPage(container) {
      container.classList.add('scrollable');
      const completedRounds = appState.data.rounds.filter(r => r.status === 'completed');"""
content = content.replace(OLD_HIST, NEW_HIST)

# renderSettingsPage
OLD_SET = """    function renderSettingsPage(container) {
      container.innerHTML = `
        <h1 class="page-title">⚙️ 설정</h1>"""
NEW_SET = """    function renderSettingsPage(container) {
      container.classList.add('scrollable');
      container.innerHTML = `
        <h1 class="page-title">⚙️ 설정</h1>"""
content = content.replace(OLD_SET, NEW_SET)

# ==================================================
# 5. Par 입력 & 퍼팅 페이지: section grow로 하여
#    남은 공간에 버튼이 아래로 내려가도록
# ==================================================
# Par 입력의 main section에 grow 추가
OLD_PAR_SECTION = """<div class="section">
          <h2 class="section-title">홀 정보</h2>"""
NEW_PAR_SECTION = """<div class="section grow">
          <h2 class="section-title">홀 정보</h2>"""
content = content.replace(OLD_PAR_SECTION, NEW_PAR_SECTION)

# ==================================================
# 6. 라운드시작 / 코스선택 / 티박스 / 새코스 페이지:
#    단일 섹션이므로 grow로 하면 자동 centering
# ==================================================

# 라운드 시작 페이지 - 타입 선택 섹션 grow
OLD_RS = """<div class="section">
          <h2 class="section-title">라운드 방식 선택</h2>"""
NEW_RS = """<div class="section grow" style="justify-content:center;">
          <h2 class="section-title">라운드 방식 선택</h2>"""
content = content.replace(OLD_RS, NEW_RS)

# 코스 선택 페이지
OLD_CS = """<div class="section">
          <h2 class="section-title">등록된 코스</h2>"""
NEW_CS = """<div class="section grow" style="justify-content:center;">
          <h2 class="section-title">등록된 코스</h2>"""
content = content.replace(OLD_CS, NEW_CS)

# 티박스 선택 - section grow + center
OLD_TB = """<div class="section">
          <h2 class="section-title">${course.name}</h2>

          <div class="button-group">
            <button class="choice-btn ${appState.selectedTeeBox === 'blue' ? 'selected' : ''}"
              onclick="selectTeeBoxAndStart('blue')">
              🔵 Blue
            </button>
            <button class="choice-btn ${appState.selectedTeeBox === 'white' ? 'selected' : ''}"
              onclick="selectTeeBoxAndStart('white')">
              ⚪ White
            </button>
          </div>
        </div>"""
NEW_TB = """<div class="section grow" style="justify-content:center;">
          <h2 class="section-title" style="text-align:center;">${course.name}</h2>

          <div class="button-group">
            <button class="choice-btn ${appState.selectedTeeBox === 'blue' ? 'selected' : ''}"
              onclick="selectTeeBoxAndStart('blue')">
              🔵 Blue
            </button>
            <button class="choice-btn ${appState.selectedTeeBox === 'white' ? 'selected' : ''}"
              onclick="selectTeeBoxAndStart('white')">
              ⚪ White
            </button>
          </div>
        </div>"""
content = content.replace(OLD_TB, NEW_TB)

# 새 코스 입력 페이지
OLD_NC = """<div class="section">
          <h2 class="section-title">코스 정보</h2>"""
NEW_NC = """<div class="section grow" style="justify-content:center;">
          <h2 class="section-title">코스 정보</h2>"""
content = content.replace(OLD_NC, NEW_NC)

# ==================================================
# Save
# ==================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Galaxy Ultra Full Screen 적합화 완료!")
print()
print("📐 기준:")
print("  • Galaxy S22~S25 Ultra (6.8~6.9\")")
print("  • vh/vw 단위 사용 → 폰 크기에 자동 적응")
print("  • clamp() → 최소/최대 크기 제한")
print()
print("📱 Full screen (스크롤 없음):")
print("  ✓ 홈 / 라운드 시작 / 코스 선택 / 티박스")
print("  ✓ 새 코스 입력 / Par 입력 / 퍼팅 / 통계")
print()
print("📜 스크롤 유지:")
print("  • 샷 입력 / 기록 / 설정")
