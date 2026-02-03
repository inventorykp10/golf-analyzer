# golf-analyzer폴더에서 실행
# 홈 페이지 버튼 크기를 vh 단위로 크게 -> Ultra 화면 채우기

$lines = Get-Content -Path "index.html" -Encoding UTF8

# ===============================================
# 홈 페이지 innerHTML 통째로 교체 (969줄 주변)
# 전략:
#   - section grow + space-between (유지)
#   - primary-btn (새 라운드): padding 4vh
#   - secondary-btn 2열: padding 3.5vh
#   - 새 코스 등록: padding 3vh
#   - home-quick-actions gap 크게
# ===============================================

# 현재 홈 페이지 innerHTML 찾기 (969~984)
# 새로운 홈 페이지 innerHTML로 교체

$oldBlock = '        <div class="section grow" style="justify-content:space-between;">
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
        </div>'

$newBlock = '        <div class="section grow" style="justify-content:space-between; padding: 2vh 4vw;">
          <button class="primary-btn" onclick="goToPage(1)" style="padding: 4vh 16px; font-size: 18px;">
            🏌️ 새 라운드 시작
          </button>
          <div class="home-quick-actions" style="gap: 2vw;">
            <button class="secondary-btn" onclick="goToPage(2)" style="margin-bottom:0; padding: 3.2vh 8px; font-size: 16px;">📊 통계</button>
            <button class="secondary-btn" onclick="goToPage(3)" style="margin-bottom:0; padding: 3.2vh 8px; font-size: 16px;">📋 기록</button>
          </div>
          <div class="home-quick-actions" style="gap: 2vw;">
            <button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);margin-bottom:0; padding: 3.2vh 8px; font-size: 16px;">📷 카메라</button>
            <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;margin-bottom:0; padding: 3.2vh 8px; font-size: 16px;">🖼️ 갤러리</button>
          </div>
          <button class="secondary-btn" onclick="openCourseRegistration()" style="margin-bottom:0; padding: 3vh 16px; font-size: 16px;">
            ➕ 새 코스 등록
          </button>
        </div>'

$content = Get-Content -Path "index.html" -Encoding UTF8 -Raw
$content = $content -replace [regex]::Escape($oldBlock), $newBlock

Set-Content -Path "index.html" -Value $content -Encoding UTF8

Write-Host "Done! Button sizes updated with vh units."
