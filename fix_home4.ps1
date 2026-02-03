# golf-analyzer폴더에서 실행
# 줄번호로 직접 확인 후 수정

$lines = Get-Content -Path "index.html" -Encoding UTF8

# 먼저 현재 상태 출력 (960~995)
Write-Host "=== BEFORE (960~995) ==="
for ($i = 959; $i -le 994; $i++) {
    Write-Host "$($i+1): $($lines[$i])"
}

# renderHomePage 안에서 "section grow" 있는 줄 찾기
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match "section grow" -and $lines[$i] -match "space-between") {
        Write-Host ""
        Write-Host "Found 'section grow space-between' at line $($i+1)"
        
        # 이 줄부터 </div> 까지 찾아서 통째로 새 코드로 교체
        # 새 라운드 버튼 줄 찾기 (i+1)
        $lines[$i+1] = '          <button class="primary-btn" onclick="goToPage(1)" style="padding:4vh 16px; font-size:18px;">'
        
        # 통계/기록 줄 찾기
        for ($j = $i; $j -lt $i + 20; $j++) {
            if ($lines[$j] -match "goToPage\(2\)") {
                $lines[$j] = '            <button class="secondary-btn" onclick="goToPage(2)" style="margin-bottom:0; padding:3.2vh 8px; font-size:16px;">📊 통계</button>'
            }
            if ($lines[$j] -match "goToPage\(3\)") {
                $lines[$j] = '            <button class="secondary-btn" onclick="goToPage(3)" style="margin-bottom:0; padding:3.2vh 8px; font-size:16px;">📋 기록</button>'
            }
            if ($lines[$j] -match "uploadCamera") {
                $lines[$j] = '            <button class="secondary-btn" onclick="uploadCamera()" style="background:var(--green-primary);color:white;border-color:var(--green-primary);margin-bottom:0; padding:3.2vh 8px; font-size:16px;">📷 카메라</button>'
            }
            if ($lines[$j] -match "uploadGallery") {
                $lines[$j] = '            <button class="secondary-btn" onclick="uploadGallery()" style="background:#5a9e4b;color:white;border-color:#5a9e4b;margin-bottom:0; padding:3.2vh 8px; font-size:16px;">🖼️ 갤러리</button>'
            }
            if ($lines[$j] -match "openCourseRegistration") {
                $lines[$j] = '          <button class="secondary-btn" onclick="openCourseRegistration()" style="margin-bottom:0; padding:3vh 16px; font-size:16px;">'
            }
        }
        break
    }
}

# 저장
Set-Content -Path "index.html" -Value $lines -Encoding UTF8

# 수정 후 확인
Write-Host ""
Write-Host "=== AFTER (960~995) ==="
for ($i = 959; $i -le 994; $i++) {
    Write-Host "$($i+1): $($lines[$i])"
}

Write-Host ""
Write-Host "Done!"
