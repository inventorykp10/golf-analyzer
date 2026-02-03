# -*- coding: utf-8 -*-
# 뒤로가기 버튼 추가 스크립트
# 홈(page 0)이 아닌 모든 페이지에 뒤로가기 버튼 표시

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. pageHistory 추가 (appState 안에)
old_state = "currentPage: 0,"
new_state = """currentPage: 0,
      pageHistory: [0],"""
content = content.replace(old_state, new_state, 1)

# 2. goToPage 함수 수정 - 히스토리 저장
old_goto = """window.goToPage = function(page) {
      appState.currentPage = page;
      render();
    };"""
new_goto = """window.goToPage = function(page) {
      appState.pageHistory.push(appState.currentPage);
      appState.currentPage = page;
      render();
    };"""
content = content.replace(old_goto, new_goto)

# 3. nav-btn onclick 수정 - 히스토리 저장
old_nav = "appState.currentPage = page.pageIndex;"
new_nav = """appState.pageHistory.push(appState.currentPage);
          appState.currentPage = page.pageIndex;"""
content = content.replace(old_nav, new_nav)

# 4. selectRoundType 히스토리 저장
old_select = """window.selectRoundType = function(type) {
      if (type === 'existing') {
        appState.currentPage = 10;
      } else {
        appState.currentPage = 11;
      }
      render();
    };"""
new_select = """window.selectRoundType = function(type) {
      appState.pageHistory.push(appState.currentPage);
      if (type === 'existing') {
        appState.currentPage = 10;
      } else {
        appState.currentPage = 11;
      }
      render();
    };"""
content = content.replace(old_select, new_select)

# 5. selectExistingCourse 히스토리 저장
old_existing = """window.selectExistingCourse = function(courseId) {
      appState.selectedCourseId = courseId;
      appState.currentPage = 12;
      render();
    };"""
new_existing = """window.selectExistingCourse = function(courseId) {
      appState.pageHistory.push(appState.currentPage);
      appState.selectedCourseId = courseId;
      appState.currentPage = 12;
      render();
    };"""
content = content.replace(old_existing, new_existing)

# 6. 일반 페이지 뒤로가기 함수 추가 + render에 백버튼 추가
# render 함수에서 activeRound가 아닐 때 백버튼 추가
old_render_nav = """      // 라운드 진행 중이 아닐 때만 하단 네비게이션 표시
      if (!appState.activeRound) {
        app.appendChild(renderBottomNav());
      }"""
new_render_nav = """      // 라운드 진행 중이 아닐 때만 하단 네비게이션 표시
      if (!appState.activeRound) {
        // 홈이 아닌 페이지에서 백버튼 표시
        if (appState.currentPage !== 0) {
          const backBtn = document.createElement('button');
          backBtn.className = 'back-button';
          backBtn.innerHTML = '&#8592;';
          backBtn.onclick = function() {
            if (appState.pageHistory.length > 0) {
              appState.currentPage = appState.pageHistory.pop();
            } else {
              appState.currentPage = 0;
            }
            render();
          };
          app.appendChild(backBtn);
        }
        app.appendChild(renderBottomNav());
      }"""
content = content.replace(old_render_nav, new_render_nav)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("뒤로가기 버튼 추가 완료!")
