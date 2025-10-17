# Task List: GUI Application Conversion

**PRD**: [0002-prd-gui-app.md](prds/0002-prd-gui-app.md)
**생성일**: 2025-01-17
**예상 기간**: 2주

---

## Parent Tasks

### [x] T1: 개발 환경 준비 ✅
- [x] T1.1: FreeSimpleGUI 5.2.0 설치 (PySimpleGUI 대체)
- [x] T1.2: APScheduler 3.11.0 설치
- [x] T1.3: 프로젝트 구조 생성 (gui/, controllers/ 폴더)
- [x] T1.4: 의존성 requirements.txt 업데이트

### [x] T2: 기본 GUI 구조 (F1 - 기본 제어) ✅
- [x] T2.1: src/gui_main.py 진입점 생성 (338줄)
- [x] T2.2: src/gui/main_window.py 메인 윈도우 레이아웃 (159줄)
- [x] T2.3: "지금 실행" 버튼 + KeyPlayerManager 연동
- [x] T2.4: 실시간 로그 뷰어 (Multiline 위젯, queue 기반)
- [x] T2.5: 진행 바 (ProgressBar) 상태 표시
- [x] T2.6: 스레딩으로 GUI 블로킹 방지 (threading.Thread)

### [x] T3: 설정 관리 (F2 - 설정 관리) ✅
- [x] T3.1: gui_main.py에 설정 관리 통합
- [x] T3.2: WSOP 설정 다이얼로그 (ID/PW/URL 입력)
- [x] T3.3: Google API 설정 다이얼로그 (SOURCE/TARGET Sheets ID)
- [x] T3.4: .env 파일 읽기/쓰기 기능
- [x] T3.5: 설정 저장 완료 팝업

### [x] T4: 모니터링 대시보드 (F3 - 모니터링) ✅
- [x] T4.1: 상태 패널 레이아웃 (마지막 실행 시간, 다음 예정, 현재 상태)
- [x] T4.2: 실시간 통계 표시 (실행 횟수, CSV 행 수, Key Player 수)
- [x] T4.3: 로그 폴더 빠른 접근 (Windows/Mac/Linux 지원)
- [x] T4.4: 실행 중 에러 표시 (popup_error)

### [ ] T5: 자동 실행 스케줄러 (F2.3)
- [ ] T5.1: APScheduler BackgroundScheduler 통합
- [ ] T5.2: 스케줄 설정 UI (시간 간격 선택)
- [ ] T5.3: "자동 실행" 토글 스위치
- [ ] T5.4: 스케줄 상태 저장/로딩 (config.json)

### [ ] T6: 시스템 트레이 통합 (F4 - 알림)
- [ ] T6.1: pystray 라이브러리 추가
- [ ] T6.2: 시스템 트레이 아이콘 및 메뉴
- [ ] T6.3: 창 최소화 → 트레이로 전환
- [ ] T6.4: 데스크톱 알림 (성공/실패 메시지)

### [ ] T7: 고급 기능 (F5)
- [ ] T7.1: 멀티 프로필 관리 (여러 WSOP 계정)
- [ ] T7.2: Google Sheets 직접 접근 버튼
- [ ] T7.3: CSV 파일 미리보기 기능

### [ ] T8: 패키징 및 배포
- [ ] T8.1: PyInstaller spec 파일 생성
- [ ] T8.2: --onefile 빌드 테스트
- [ ] T8.3: credentials.json 번들링 처리
- [ ] T8.4: 아이콘 리소스 추가 (icon.ico)
- [ ] T8.5: Windows 7+ 테스트
- [ ] T8.6: 실행 파일 크기 최적화

### [ ] T9: 테스트 및 문서화
- [ ] T9.1: GUI 수동 테스트 체크리스트
- [ ] T9.2: 패키징 설치 가이드 작성
- [ ] T9.3: README.md 업데이트 (GUI 사용법)
- [ ] T9.4: 스크린샷 추가 (docs/screenshots/)

---

## 현재 진행 상황

**Phase**: ✅ Phase 1-3 완료 (기본 GUI, 설정, 모니터링)
**버전**: v2.0.0
**다음 단계**: T5 - 자동 실행 스케줄러 (선택 사항)

---

## 노트

- **기존 코드 재사용**: src/main.py의 KeyPlayerManager 클래스는 그대로 유지
- **Controller 패턴**: GUI ↔ Controllers ↔ Services 3-layer 구조
- **비동기 실행**: threading.Thread로 GUI 블로킹 방지 필수
- **설정 저장**: .env (민감 정보) + config.json (UI 상태)
