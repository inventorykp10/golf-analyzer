# golf-analyzer폴더에서 실행
# 현재 상태 먼저 확인 후 수정

$lines = Get-Content -Path "index.html" -Encoding UTF8

# 현재 홈 페이지 섹션 확인 (969줄 주변)
Write-Host "=== 현재 상태 (965~990) ==="
for ($i = 964; $i -le 989; $i++) {
    Write-Host "$($i+1): $($lines[$i])"
}

# 직접 줄번호로 수정
# 969줄: <div class="section"> -> <div class="section grow" style="justify-content:space-between;">
$lines[968] = '        <div class="section grow" style="justify-content:space-between;">'

# 986줄: version section -> div (section 제거)
$lines[985] = '        <div style="text-align: center; padding: 6px; flex-shrink:0;">'

Write-Host ""
Write-Host "=== 수정 후 ==="
for ($i = 964; $i -le 989; $i++) {
    Write-Host "$($i+1): $($lines[$i])"
}

# 저장
Set-Content -Path "index.html" -Value $lines -Encoding UTF8
Write-Host ""
Write-Host "Done! Saved."
