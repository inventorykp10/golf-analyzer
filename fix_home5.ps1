# golf-analyzer폴더에서 실행
# 줄번호로 직접 교체 (no matching)

$lines = Get-Content -Path "index.html" -Encoding UTF8

# 줄 969 (인덱스 968): <div class="section"> -> <div class="section grow" style="justify-content:space-between;">
$lines[968] = '        <div class="section grow" style="justify-content:space-between;">'

# 줄 970 (인덱스 969): primary-btn padding 크게
$lines[969] = '          <button class="primary-btn" onclick="goToPage(1)" style="padding:4vh 16px; font-size:18px;">'

# 줄 974 (인덱스 973): 통계 버튼
$lines[973] = '            <button class="secondary-btn" onclick="goToPage(2)" style="margin-bottom:0; padding:3.2vh 8px; font-size:16px;">📊 통계</button>'

# 줄 975 (인덱스 974): 기록 버튼
$lines[974] = '            <button class="secondary-btn" onclick="goToPage(3)" style="margin-bottom:0; padding:3.2vh 8px; font-size:16px;">📋 기록</button>'

# 줄 978 (인덱스 977): 카메라 버튼
$lines[977] = '            <button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);margin-bottom:0; padding:3.2vh 8px; font-size:16px;">📷 카메라</button>'

# 줄 979 (인덱스 978): 갤러리 버튼
$lines[978] = '            <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;margin-bottom:0; padding:3.2vh 8px; font-size:16px;">🖼️ 갤러리</button>'

# 줄 981 (인덱스 980): 새 코스 등록
$lines[980] = '          <button class="secondary-btn" onclick="openCourseRegistration()" style="margin-bottom:0; padding:3vh 16px; font-size:16px;">'

# 저장
Set-Content -Path "index.html" -Value $lines -Encoding UTF8

# 수정 후 확인
Write-Host "=== AFTER (968~985) ==="
for ($i = 967; $i -le 984; $i++) {
    Write-Host "$($i+1): $($lines[$i])"
}
Write-Host ""
Write-Host "Done!"
