# -*- coding: utf-8 -*-
# ============================================================
# 전체 페이지 한 화면 적합화
# ============================================================
# ✅ 한 화면으로 수정할 페이지:
#   - 홈 페이지 (카메라/갤러리 2열 + 섹션 축소)
#   - 라운드 시작 (타입 선택) → 이미 짧음
#   - 코스 선택 / 티박스 선택 / 새 코스 입력 → 이미 짧음
#   - Par 입력 → CSS축소로 가능
#   - 퍼팅 입력 → CSS축소로 가능
#   - 통계 페이지 → CSS축소로 가능
#
# ❌ 스크롤 유지 (현상 유지):
#   - 샷 입력 → 조건에 따라 동적 섹션 많음
#   - 기록 페이지 → 라운드 수에 따라 길어짐
#   - 설정 페이지 → 코스목록 + 클럽목록 + 데이터
#   - 코스 등록 모달 → 18홀 입력폼
# ============================================================

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==================================================
# 1. CSS 전체 축소 (모든 페이지 공유)
# ==================================================

# .page-container
content = content.replace(
    """.page-container {
      flex: 1;
      padding: 24px;
      padding-bottom: 100px;
      overflow-y: auto;
    }""",
    """.page-container {
      flex: 1;
      padding: 12px 14px;
      padding-bottom: 70px;
      overflow-y: auto;
    }"""
)

# .page-title
content = content.replace(
    """.page-title {
      font-size: 28px;
      font-weight: 700;
      color: var(--green-primary);
      margin-bottom: 20px;
      font-family: 'Bebas Neue', cursive;
      letter-spacing: 1px;
      text-align: center;
    }""",
    """.page-title {
      font-size: 22px;
      font-weight: 700;
      color: var(--green-primary);
      margin-bottom: 10px;
      font-family: 'Bebas Neue', cursive;
      letter-spacing: 1px;
      text-align: center;
    }"""
)

# .section
content = content.replace(
    """.section {
      margin-bottom: 24px;
      background: white;
      padding: 20px;
      border-radius: 16px;
      box-shadow: var(--shadow);
    }""",
    """.section {
      margin-bottom: 8px;
      background: white;
      padding: 12px 14px;
      border-radius: 16px;
      box-shadow: var(--shadow);
    }"""
)

# .section-title
content = content.replace(
    """.section-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--green-primary);
      margin-bottom: 16px;
    }""",
    """.section-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--green-primary);
      margin-bottom: 8px;
    }"""
)

# .secondary-btn
content = content.replace(
    """.secondary-btn {
      width: 100%;
      padding: 16px;
      background: white;
      color: var(--green-primary);
      border: 2px solid var(--green-primary);
      border-radius: 12px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      margin-bottom: 12px;
    }""",
    """.secondary-btn {
      width: 100%;
      padding: 10px;
      background: white;
      color: var(--green-primary);
      border: 2px solid var(--green-primary);
      border-radius: 12px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      margin-bottom: 6px;
    }"""
)

# .primary-btn
content = content.replace(
    """.primary-btn {
      width: 100%;
      padding: 16px;
      background: var(--green-primary);
      color: white;
      border: none;
      border-radius: 12px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }""",
    """.primary-btn {
      width: 100%;
      padding: 12px;
      background: var(--green-primary);
      color: white;
      border: none;
      border-radius: 12px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }"""
)

# .input-section
content = content.replace(
    """/* Input Sections */
    .input-section {
      margin-bottom: 20px;
    }

    .input-section label {
      display: block;
      font-size: 15px;
      font-weight: 600;
      color: var(--brown);
      margin-bottom: 10px;
    }""",
    """/* Input Sections */
    .input-section {
      margin-bottom: 10px;
    }

    .input-section label {
      display: block;
      font-size: 14px;
      font-weight: 600;
      color: var(--brown);
      margin-bottom: 6px;
    }"""
)

# .text-input, .select-input padding
content = content.replace(
    """.text-input {
      width: 100%;
      padding: 12px;
      border: 2px solid var(--sand);
      border-radius: 8px;
      font-size: 16px;
      font-family: 'Noto Sans KR', sans-serif;
    }""",
    """.text-input {
      width: 100%;
      padding: 8px 10px;
      border: 2px solid var(--sand);
      border-radius: 8px;
      font-size: 15px;
      font-family: 'Noto Sans KR', sans-serif;
    }"""
)

content = content.replace(
    """.select-input {
      width: 100%;
      padding: 12px;
      border: 2px solid var(--sand);
      border-radius: 8px;
      font-size: 16px;
      font-family: 'Noto Sans KR', sans-serif;
      background: white;
    }""",
    """.select-input {
      width: 100%;
      padding: 8px 10px;
      border: 2px solid var(--sand);
      border-radius: 8px;
      font-size: 15px;
      font-family: 'Noto Sans KR', sans-serif;
      background: white;
    }"""
)

# .choice-btn
content = content.replace(
    """.choice-btn {
      padding: 12px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
      font-weight: 500;
    }""",
    """.choice-btn {
      padding: 8px 4px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
      font-weight: 500;
    }"""
)

# .checkbox-label
content = content.replace(
    """.checkbox-label {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
    }""",
    """.checkbox-label {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 7px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 13px;
    }"""
)

# .shot-header
content = content.replace(
    """/* Shot Info Header */
    .shot-header {
      background: white;
      padding: 16px;
      border-radius: 12px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
    }""",
    """/* Shot Info Header */
    .shot-header {
      background: white;
      padding: 10px 12px;
      border-radius: 12px;
      margin-bottom: 8px;
      box-shadow: var(--shadow);
    }"""
)

# .shot-number
content = content.replace(
    """.shot-number {
      font-size: 20px;
      font-weight: 700;
      color: var(--green-primary);
      margin-top: 8px;
    }""",
    """.shot-number {
      font-size: 16px;
      font-weight: 700;
      color: var(--green-primary);
      margin-top: 4px;
    }"""
)

# .previous-shots
content = content.replace(
    """/* Previous Shots */
    .previous-shots {
      background: var(--sand);
      padding: 12px;
      border-radius: 8px;
      margin-bottom: 20px;
      font-size: 14px;
    }""",
    """/* Previous Shots */
    .previous-shots {
      background: var(--sand);
      padding: 8px 10px;
      border-radius: 8px;
      margin-bottom: 8px;
      font-size: 13px;
    }"""
)

# .round-control-panel
content = content.replace(
    """/* Round Control */
    .round-control-panel {
      background: var(--sand);
      padding: 16px;
      border-radius: 12px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }""",
    """/* Round Control */
    .round-control-panel {
      background: var(--sand);
      padding: 8px 12px;
      border-radius: 12px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }"""
)

# .stats-grid
content = content.replace(
    """/* Stats */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }

    .stat-card {
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: var(--shadow);
      text-align: center;
    }

    .stat-icon {
      font-size: 32px;
      margin-bottom: 8px;
    }

    .stat-label {
      font-size: 13px;
      color: var(--brown);
      opacity: 0.7;
      margin-bottom: 8px;
    }

    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--green-primary);
    }""",
    """/* Stats */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-bottom: 10px;
    }

    .stat-card {
      background: white;
      padding: 10px 6px;
      border-radius: 12px;
      box-shadow: var(--shadow);
      text-align: center;
    }

    .stat-icon {
      font-size: 22px;
      margin-bottom: 2px;
    }

    .stat-label {
      font-size: 12px;
      color: var(--brown);
      opacity: 0.7;
      margin-bottom: 4px;
    }

    .stat-value {
      font-size: 22px;
      font-weight: 700;
      color: var(--green-primary);
    }"""
)

# .home-quick-actions
content = content.replace(
    """/* Home Layout Improvement */
    .home-quick-actions {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
    }""",
    """/* Home Layout Improvement */
    .home-quick-actions {
      display: flex;
      gap: 8px;
      margin-bottom: 6px;
    }"""
)

# .course-btn
content = content.replace(
    """/* Course Selection */
    .course-btn {
      width: 100%;
      padding: 16px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 12px;
      text-align: left;
      cursor: pointer;
      margin-bottom: 12px;
      transition: all 0.2s;
    }""",
    """/* Course Selection */
    .course-btn {
      width: 100%;
      padding: 10px 12px;
      background: white;
      border: 2px solid var(--sand);
      border-radius: 12px;
      text-align: left;
      cursor: pointer;
      margin-bottom: 6px;
      transition: all 0.2s;
    }"""
)

# .club-item
content = content.replace(
    """.club-item {
      padding: 10px;
      background: var(--sand);
      border-radius: 8px;
      font-size: 14px;
    }""",
    """.club-item {
      padding: 6px 8px;
      background: var(--sand);
      border-radius: 8px;
      font-size: 13px;
    }"""
)

# .club-recommendation / .info-box
content = content.replace(
    """/* Club Recommendation */
    .club-recommendation {
      background: #e3f2fd;
      border-left: 4px solid var(--blue);
      padding: 12px;
      margin-bottom: 16px;
      border-radius: 4px;
      font-size: 14px;
    }

    .info-box {
      background: #e3f2fd;
      border-left: 4px solid var(--blue);
      padding: 12px;
      margin-bottom: 16px;
      border-radius: 4px;
      font-size: 14px;
    }""",
    """/* Club Recommendation */
    .club-recommendation {
      background: #e3f2fd;
      border-left: 4px solid var(--blue);
      padding: 8px 10px;
      margin-bottom: 8px;
      border-radius: 4px;
      font-size: 13px;
    }

    .info-box {
      background: #e3f2fd;
      border-left: 4px solid var(--blue);
      padding: 8px 10px;
      margin-bottom: 8px;
      border-radius: 4px;
      font-size: 13px;
    }"""
)

# bottom nav 약간 축소
content = content.replace(
    """.nav-btn {
      border: none;
      background: transparent;
      padding: 12px 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      transition: all 0.2s;
      color: var(--brown);
      opacity: 0.6;
    }""",
    """.nav-btn {
      border: none;
      background: transparent;
      padding: 8px 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      cursor: pointer;
      transition: all 0.2s;
      color: var(--brown);
      opacity: 0.6;
    }"""
)

content = content.replace(
    """.nav-btn-icon {
      font-size: 24px;
    }""",
    """.nav-btn-icon {
      font-size: 22px;
    }"""
)

# ==================================================
# 2. 홈 페이지 HTML: 카메라/갤러리 2열 + 섹션 통합
# ==================================================
OLD_HOME = """        <div class="section">
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
        </div>"""

NEW_HOME = """        <div class="section">
          <button class="primary-btn" onclick="goToPage(1)" style="margin-bottom:6px;">
            🏌️ 새 라운드 시작
          </button>
          <div class="home-quick-actions">
            <button class="secondary-btn" onclick="goToPage(2)" style="margin-bottom:0;">📊 통계</button>
            <button class="secondary-btn" onclick="goToPage(3)" style="margin-bottom:0;">📋 기록</button>
          </div>
          <div class="home-quick-actions">
            <button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);margin-bottom:0;">📷 카메라</button>
            <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;margin-bottom:0;">🖼️ 갤러리</button>
          </div>
          <button class="secondary-btn" onclick="openCourseRegistration()" style="margin-bottom:0;">
            ➕ 새 코스 등록
          </button>
        </div>

        <div class="section" style="text-align: center; padding: 8px;">
          <p style="opacity: 0.5; font-size: 12px;">v9.0.0 • Par 입력 개선</p>
        </div>"""

content = content.replace(OLD_HOME, NEW_HOME)

# ==================================================
# 3. 통계 페이지: 하단 문장 축소
# ==================================================
content = content.replace(
    """<p style="opacity: 0.7; margin-bottom: 24px;">최근 ${recentRounds.length}라운드</p>""",
    """<p style="opacity: 0.7; margin-bottom: 8px; font-size: 13px;">최근 ${recentRounds.length}라운드</p>"""
)

# ==================================================
# Save
# ==================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 전체 페이지 컴팩트 수정 완료!")
print()
print("📱 한 화면으로 수정된 페이지:")
print("  ✓ 홈 페이지 (섹션 통합 + 카메라/갤러리 2열)")
print("  ✓ 라운드 시작 / 코스 선택 / 티박스 선택")
print("  ✓ 새 코스 입력 / Par 입력 / 퍼팅 입력")
print("  ✓ 통계 페이지")
print()
print("📜 스크롤 유지 (현상 유지):")
print("  - 샷 입력 (동적 섹션이 많음)")
print("  - 기록 페이지 (라운드 수 증가시 길어짐)")
print("  - 설정 페이지 (코스+클럽+데이터)")
print("  - 코스 등록 모달 (18홀 입력폼)")
