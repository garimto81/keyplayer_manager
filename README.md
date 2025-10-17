# Key Player Manager 🎰

**버전**: 2.0.0 | **상태**: ✅ 프로덕션 | **업데이트**: 2025-01-17

WSOP 플레이어 리스트 자동 수집 및 Google Sheets 동기화 시스템

## 🆕 v2.0 신규 기능: GUI 데스크톱 애플리케이션

이제 명령줄 없이 **GUI 인터페이스**로 쉽게 사용할 수 있습니다!

```bash
# GUI 앱 실행
python src/gui_main.py
```

**주요 기능**:
- ▶️ 원클릭 실행 버튼
- 📊 실시간 진행 상태 및 로그
- ⚙️ 비주얼 설정 다이얼로그 (WSOP, Google API)
- 📈 통계 대시보드 (실행 횟수, CSV 행 수, Key Player 수)
- 🔔 자동 실행 스케줄러 (개발 중)
- 📂 로그 폴더 빠른 접근

📚 **[GUI 사용 가이드](tasks/prds/0002-prd-gui-app.md)** - 상세 설명 및 스크린샷

## 📋 기능

1. **WSOP 사이트 자동 로그인** - Selenium 기반 브라우저 자동화
2. **CSV 다운로드** - "Export player list to csv" 버튼 자동 클릭
3. **Google Sheets 업로드** - Confirmed 시트에 자동 붙여넣기
4. **Apps Script 트리거** - 키 플레이어 자동 마킹
5. **스케줄링** - 1시간마다 자동 실행
6. **세션 관리** - 24시간 쿠키 재사용으로 로그인 최소화

---

## 📚 문서

### ⚡ 빠른 시작
- **[완전 자동화 설정](AUTOMATION_COMPLETE.md)** 🎉 - 전체 워크플로우 이해
- **[Time Trigger 설정](TIME_TRIGGER_SETUP.md)** ⚡ - 2분 자동화 (추천)
- **[빠른 시작](docs/guides/QUICK_START.md)** 🚀 - 5분 완성 가이드

### 📖 상세 가이드
- **[세션 관리](docs/guides/SESSION_GUIDE.md)** 🔐 - 로그인 최적화
- **[Sheets 아키텍처](docs/SHEETS_ARCHITECTURE.md)** 📊 - 2-Sheet 설계 설명
- **[테스트 현황](docs/guides/TESTING_COMPLETE.md)** ✅ - 완료/대기 현황

### 📋 기타
- **[PRD Summary](tasks/prds/0001-prd-summary.md)** 📋 - 프로젝트 요약
- **[전체 문서 인덱스](docs/INDEX.md)** 📚 - 모든 문서 목록

---

## 🚀 빠른 시작

### 1. 사전 요구사항

- **Python 3.8+** ([다운로드](https://www.python.org/downloads/))
- **Chrome 브라우저** (Selenium용)
- **Google Cloud 프로젝트** (Sheets API용)

### 2. 설치

```bash
# 1. 저장소 클론 또는 다운로드
git clone <repository_url>
cd keyplayer_manager

# 2. 초기 설정 스크립트 실행
python setup.py

# 3. Python 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 설정

#### 3.1 `.env` 파일 설정

`.env.example`을 복사하여 `.env` 생성 후 실제 값으로 수정:

```bash
# WSOP 로그인 정보
WSOP_USERNAME=your_username
WSOP_PASSWORD=your_password
WSOP_URL=https://staff.wsopplus.com/series/13/tournaments/management/event-flight/1675/tables/seats

# Google Sheets ID
SOURCE_SPREADSHEET_ID=1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg
TARGET_SPREADSHEET_ID=19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4

# Apps Script Web App URL (선택)
APPS_SCRIPT_URL=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?action=updateKeyPlayers

# 이메일 알림 (선택)
NOTIFICATION_EMAIL=your_email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

#### 3.2 Google API 설정

**Step 1: Google Cloud Console 설정**

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (예: "KeyPlayerManager")
3. **API 및 서비스** > **라이브러리**에서 다음 활성화:
   - Google Sheets API
   - Google Drive API

**Step 2: 서비스 계정 생성**

1. **IAM 및 관리자** > **서비스 계정** 클릭
2. **서비스 계정 만들기**
   - 이름: `keyplayer-bot`
   - 역할: `편집자`
3. 생성된 계정 클릭 > **키** 탭 > **키 추가** > **JSON**
4. 다운로드한 JSON 파일을 `credentials.json`으로 저장

**Step 3: Google Sheets 권한 부여**

1. `credentials.json`에서 `client_email` 복사 (예: `keyplayer-bot@xxx.iam.gserviceaccount.com`)
2. Google Sheets 열기:
   - [Confirmed 시트](https://docs.google.com/spreadsheets/d/1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg)
   - [Type 시트](https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4)
3. **공유** 버튼 클릭 > 위 이메일 추가 > **편집자** 권한 부여

#### 3.3 Apps Script 설정 (선택)

Apps Script를 Web App으로 배포하면 Python에서 자동 트리거 가능합니다.

1. Google Sheets > **확장 프로그램** > **Apps Script**
2. `gs/keyplayer.gs`와 `gs/keyplayer_api.gs` 내용 복사
3. **배포** > **새 배포**
   - 유형: **웹 앱**
   - 실행 사용자: **나**
   - 액세스 권한: **모든 사용자**
4. 생성된 **웹 앱 URL** 복사
5. `.env` 파일에 `APPS_SCRIPT_URL`로 저장

---

## 🎮 사용법

### 🖥️ GUI 모드 (권장)

```bash
# GUI 애플리케이션 실행
python src/gui_main.py
```

**GUI 사용법**:
1. ▶️ **"지금 실행"** 버튼 클릭 → 자동화 즉시 시작
2. 📝 **실시간 로그** 창에서 진행 상황 확인
3. ⚙️ **설정 버튼**으로 WSOP/Google API 정보 편집
4. 📊 **통계 대시보드**에서 실행 결과 확인

### 📟 CLI 모드 (기존 방식)

```bash
# Python으로 직접 실행
python src/main.py

# Windows 배치 파일 (더블클릭)
scripts\run_once.bat
```

### 자동 스케줄링

#### Windows (Task Scheduler)

```bash
# 관리자 권한으로 실행
scripts\schedule_task_windows.bat
```

- **작업 이름**: `KeyPlayerManager_Hourly`
- **실행 주기**: 1시간마다 (매시 정각)
- **확인 방법**: Win + R → `taskschd.msc`

#### Linux/Mac (Cron)

```bash
# Cron 편집기 열기
crontab -e

# 1시간마다 실행 (매시 정각)
0 * * * * cd /path/to/keyplayer_manager && /usr/bin/python3 src/main.py >> logs/cron.log 2>&1

# 30분마다 실행
*/30 * * * * cd /path/to/keyplayer_manager && /usr/bin/python3 src/main.py >> logs/cron.log 2>&1
```

---

## 📂 프로젝트 구조

```
keyplayer_manager/
├── src/
│   ├── gui_main.py          # 🆕 GUI 진입점
│   ├── gui/                 # 🆕 GUI 컴포넌트
│   │   └── main_window.py   # 메인 윈도우 레이아웃
│   ├── controllers/         # 🆕 Controller 레이어
│   ├── main.py              # CLI 메인 스크립트
│   ├── wsop_scraper.py      # WSOP 스크래핑 (Selenium)
│   └── sheets_uploader.py   # Google Sheets 업로드
├── gs/
│   └── keyplayer.gs         # Apps Script (Time Trigger)
├── scripts/
│   ├── run_once.bat         # Windows 수동 실행
│   └── schedule_task_windows.bat  # Windows 스케줄러 등록
├── downloads/               # CSV 다운로드 폴더
├── logs/                    # 실행 로그
├── requirements.txt         # Python 패키지 (FreeSimpleGUI 포함)
├── .env                     # 환경 변수 (비밀)
├── credentials.json         # Google API 키 (비밀)
└── README.md
```

---

## 🔧 동작 원리

```
┌─────────────────┐
│  1. WSOP 로그인  │  ← Selenium (Chrome)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. CSV 다운로드 │  ← "Export player list" 버튼 클릭
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Sheets 업로드│  ← Google Sheets API
│   (Confirmed)    │     기존 데이터 클리어 → 새 데이터 삽입
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Apps Script  │  ← HTTP 요청 or 수동 실행
│   트리거         │     updateAndCheckBoxes() 실행
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. 키 플레이어  │  ← Type 시트 K/L열 업데이트
│     마킹 완료    │     Confirmed 시트 체크박스 업데이트
└─────────────────┘
```

---

## 🐛 트러블슈팅

### 1. Selenium 오류: "Chrome driver not found"

**원인**: Chrome 버전과 드라이버 불일치

**해결**:
```bash
pip install --upgrade webdriver-manager
```

### 2. Google Sheets API 오류: "Insufficient Permission"

**원인**: 서비스 계정이 시트에 접근 권한 없음

**해결**:
1. `credentials.json`에서 `client_email` 확인
2. Google Sheets에서 해당 이메일에 **편집자** 권한 부여

### 3. WSOP 로그인 실패

**원인**: 사이트 구조 변경 또는 잘못된 셀렉터

**해결**:
1. Chrome 개발자 도구 (F12) 열기
2. 로그인 필드 우클릭 > **검사**
3. `id`, `name`, `class` 확인
4. `src/wsop_scraper.py`의 `login_selectors` 수정

### 4. CSV 다운로드 실패

**원인**: "Export" 버튼 셀렉터 변경

**해결**:
1. 브라우저에서 버튼 우클릭 > **검사**
2. XPath 복사: 우클릭 > **Copy** > **Copy XPath**
3. `src/wsop_scraper.py`의 `export_button_selectors`에 추가

### 5. Apps Script 트리거 실패

**원인**: Web App URL 미설정 또는 배포 권한 문제

**해결**:
1. Apps Script > **배포** > **배포 관리**
2. 액세스 권한: **모든 사용자**로 변경
3. 새 URL 복사 후 `.env` 업데이트

---

## 🔒 보안 주의사항

1. **절대 커밋 금지**:
   - `.env` (WSOP 비밀번호)
   - `credentials.json` (Google API 키)

2. **Git에 추가됨 확인**:
   ```bash
   git status
   # .env, credentials.json이 보이면 안 됨
   ```

3. **비밀번호 관리**:
   - WSOP 비밀번호는 정기적으로 변경
   - Google 서비스 계정 키는 만료일 설정 권장

---

## 📊 로그 확인

```bash
# 최신 로그 보기
tail -f logs/automation_20250117.log

# Windows (PowerShell)
Get-Content logs\automation_20250117.log -Wait
```

**로그 예시**:
```
[2025-01-17 10:00:00] 🚀 키 플레이어 자동화 시작
[2025-01-17 10:00:05] ✅ Chrome 드라이버 설정 완료
[2025-01-17 10:00:12] ✅ 로그인 성공
[2025-01-17 10:00:18] ✅ CSV 다운로드 완료: player_list.csv
[2025-01-17 10:00:25] ✅ Sheets 업로드 완료
[2025-01-17 10:00:30] ✅ Apps Script 실행 완료
[2025-01-17 10:00:30] 🎉 자동화 완료! (소요시간: 30.5초)
```

---

## 🎯 커스터마이징

### 실행 주기 변경

**Windows Task Scheduler**:
1. `taskschd.msc` 실행
2. `KeyPlayerManager_Hourly` 우클릭 > **속성**
3. **트리거** 탭에서 시간 수정

**Linux Cron**:
```bash
# 15분마다
*/15 * * * * python3 /path/to/src/main.py

# 매일 오전 9시
0 9 * * * python3 /path/to/src/main.py
```

### WSOP URL 변경

`.env` 파일에서 수정:
```bash
WSOP_URL=https://staff.wsopplus.com/series/NEW_ID/tournaments/...
```

### 알림 추가

`.env`에 SMTP 설정 추가 후 자동 이메일 알림:
- ✅ 성공 시: 실행 시간, CSV 파일명
- ❌ 실패 시: 오류 메시지, 로그 위치

---

## 🤝 기여

이슈 및 개선 제안은 GitHub Issues로 제출해 주세요.

---

## 📄 라이선스

MIT License

---

## 📞 문의

프로젝트 관련 문의: [이메일 또는 연락처]

---

## 📋 버전 히스토리

### v2.0.0 (2025-01-17)
- 🆕 **GUI 데스크톱 애플리케이션** 추가 (FreeSimpleGUI 기반)
- 🆕 실시간 로그 뷰어 및 진행 바
- 🆕 비주얼 설정 다이얼로그 (WSOP/Google API)
- 🆕 통계 대시보드 (실행 횟수, CSV 행 수, Key Player 수)
- 📚 GUI PRD 문서 추가 ([0002-prd-gui-app.md](tasks/prds/0002-prd-gui-app.md))

### v1.0.0 (2025-01-17)
- ✅ WSOP 자동 로그인 및 CSV 다운로드
- ✅ Google Sheets 업로드 (TARGET Type 시트)
- ✅ Apps Script Time Trigger (1분 간격)
- ✅ 세션 관리 (24시간 쿠키 재사용)
- ✅ 완전 자동화 문서 작성

---

**v2.0.0** | 마지막 업데이트: 2025-01-17