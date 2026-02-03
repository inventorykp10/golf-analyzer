# golf-analyzer폴더에서 실행
# 홈 페이지 메인 섹션에 grow 추가 + 간격 분배

$content = Get-Content -Path "index.html" -Encoding UTF8 -Raw

# 1. 홈 페이지 메인 섹션: "section" -> "section grow"
#    줄 969: <div class="section"> (버튼들이 들어있는 것)
#    이 섹션만 grow 추가하기 위해 바로 아래의 primary-btn과 세트로 매칭
$old1 = '<div class="section">
          <button class="primary-btn" onclick="goToPage(1)" style="margin-bottom:6px;">'

$new1 = '<div class="section grow" style="justify-content:space-between;">
          <button class="primary-btn" onclick="goToPage(1)" style="margin-bottom:6px;">'

$content = $content -replace [regex]::Escape($old1), $new1

# 2. version 섹션도 shrink:0 추가 (아래로 붙기)
$old2 = '<div class="section" style="text-align: center; padding: 8px;">'
$new2 = '<div style="text-align: center; padding: 6px; flex-shrink:0;">'

$content = $content -replace [regex]::Escape($old2), $new2

# Save
Set-Content -Path "index.html" -Value $content -Encoding UTF8

Write-Host "Done! index.html updated"
