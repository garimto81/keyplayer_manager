# 📁 프로젝트 구조

**업데이트**: 2025-10-17

---

## 🎯 핵심 파일 (빠른 참조)

| 파일 | 용도 |
|------|------|
| **[AUTOMATION_COMPLETE.md](AUTOMATION_COMPLETE.md)** | 완전 자동화 설명 ⭐ |
| **[TIME_TRIGGER_SETUP.md](TIME_TRIGGER_SETUP.md)** | 2분 자동화 설정 ⚡ |
| **[gs/keyplayer.gs](gs/keyplayer.gs)** | Apps Script 메인 코드 |
| **[src/main.py](src/main.py)** | Python 메인 실행 |

---

## 📂 전체 구조

```
keyplayer_manager/
│
├── 📄 README.md                        # 프로젝트 메인 문서
├── 📄 AUTOMATION_COMPLETE.md           # 완전 자동화 설명 ⭐
├── 📄 TIME_TRIGGER_SETUP.md            # Time Trigger 설정 (2분) ⚡
├── 📄 PROJECT_STRUCTURE.md             # 이 문서
│
├── 🔧 .env                             # 환경 변수 (Spreadsheet ID, WSOP 로그인 등)
├── 🔧 .env.example                     # 환경 변수 템플릿
├── 🔐 credentials.json                 # Google Service Account 키 (필수)
├── 🔐 wsop-sheets-uploader.json        # 백업 키
├── 📦 requirements.txt                 # Python 패키지 목록
│
├── 📁 src/                             # Python 소스 코드
│   ├── main.py                         # 메인 실행 파일 ⭐
│   ├── wsop_scraper.py                 # WSOP 스크래핑 + CSV 다운로드
│   ├── sheets_uploader.py              # Google Sheets 업로드
│   └── session_manager.py              # 세션 관리 (쿠키 재사용)
│
├── 📁 gs/                              # Google Apps Script 코드
│   ├── keyplayer.gs                    # 메인 Apps Script ⭐
│   └── README.md                       # gs 폴더 사용법
│
├── 📁 tests/                           # 테스트 스크립트
│   ├── test_auto.py                    # 로그인 자동 테스트
│   ├── test_csv_download.py            # CSV 다운로드 테스트
│   ├── test_session_reuse.py           # 세션 재사용 테스트
│   ├── test_sheets_upload.py           # Sheets 업로드 테스트 (구버전)
│   ├── test_corrected_upload.py        # Sheets 업로드 테스트 (수정됨) ✅
│   ├── test_trigger_apps_script.py     # Apps Script 트리거 테스트
│   ├── test_find_export_button.py      # Export 버튼 탐색
│   └── test_manual_apps_script.md      # Apps Script 수동 실행 가이드
│
├── 📁 docs/                            # 문서
│   ├── INDEX.md                        # 전체 문서 인덱스
│   ├── SHEETS_ARCHITECTURE.md          # 2-Sheet 아키텍처 설명 ⭐
│   │
│   └── guides/                         # 상세 가이드
│       ├── QUICK_START.md              # 5분 빠른 시작
│       ├── SESSION_GUIDE.md            # 세션 관리 가이드
│       ├── TESTING_COMPLETE.md         # 테스트 현황
│       └── APPS_SCRIPT_AUTOMATION.md   # Apps Script 자동화 (Web App 방식)
│
├── 📁 tasks/                           # 작업 관리
│   └── prds/                           # PRD (Product Requirements Document)
│       ├── 0001-prd-wsop-automation.md # 전체 PRD (368줄)
│       └── 0001-prd-summary.md         # PRD 요약 (110줄)
│
├── 📁 downloads/                       # CSV 다운로드 경로
│   └── Seats.csv                       # 최신 다운로드 파일
│
├── 📁 logs/                            # 실행 로그
│   └── automation_YYYYMMDD.log         # 일별 로그
│
└── 🗃️ session_cookies.pkl              # 세션 쿠키 (24시간 유효)
```

---

## 🎯 역할별 파일 분류

### 1️⃣ 자동화 설정 (처음 1회)

```
필수 설정 파일:
├── .env                        # 환경 변수 설정
├── credentials.json            # Google API 키
└── TIME_TRIGGER_SETUP.md       # Trigger 설정 가이드

Apps Script 설정:
└── gs/keyplayer.gs             # Apps Script 편집기에 복사
```

---

### 2️⃣ 실행 파일 (자동 또는 수동)

```
메인 실행:
└── src/main.py                 # 전체 워크플로우 실행

단계별 실행:
├── src/wsop_scraper.py         # WSOP 스크래핑만
└── src/sheets_uploader.py      # Sheets 업로드만
```

---

### 3️⃣ 문서 (이해/참조)

```
빠른 시작:
├── AUTOMATION_COMPLETE.md      # 전체 워크플로우 이해 ⭐
├── TIME_TRIGGER_SETUP.md       # 2분 설정 가이드 ⚡
└── README.md                   # 프로젝트 개요

상세 가이드:
├── docs/SHEETS_ARCHITECTURE.md # 2-Sheet 설계 설명
├── docs/guides/SESSION_GUIDE.md # 세션 관리
└── docs/guides/TESTING_COMPLETE.md # 테스트 현황

PRD:
├── tasks/prds/0001-prd-summary.md # 빠른 참조 (110줄)
└── tasks/prds/0001-prd-wsop-automation.md # 전체 (368줄)
```

---

### 4️⃣ 테스트 (디버깅/검증)

```
통합 테스트:
└── tests/test_corrected_upload.py  # 전체 업로드 테스트 ✅

단위 테스트:
├── tests/test_auto.py              # 로그인 테스트
├── tests/test_csv_download.py      # CSV 다운로드 테스트
└── tests/test_session_reuse.py     # 세션 재사용 테스트

Apps Script 테스트:
├── tests/test_trigger_apps_script.py # Python 트리거 테스트
└── tests/test_manual_apps_script.md  # 수동 실행 가이드
```

---

## 🗂️ 파일 상태

### ✅ 최신/활성

| 파일 | 상태 | 비고 |
|------|------|------|
| `src/main.py` | ✅ 최신 | Time Trigger 메시지 포함 |
| `src/wsop_scraper.py` | ✅ 최신 | JavaScript 클릭 방식 |
| `src/sheets_uploader.py` | ✅ 최신 | TARGET Type 시트 업로드 |
| `gs/keyplayer.gs` | ✅ 최신 | Time Trigger 로직 포함 |
| `AUTOMATION_COMPLETE.md` | ✅ 최신 | 전체 워크플로우 설명 |
| `TIME_TRIGGER_SETUP.md` | ✅ 최신 | 2분 설정 가이드 |
| `docs/SHEETS_ARCHITECTURE.md` | ✅ 최신 | 2-Sheet 설계 |

### ⚠️ 참조용 (구버전)

| 파일 | 용도 |
|------|------|
| `tests/test_sheets_upload.py` | SOURCE Confirmed 업로드 (구버전) |
| `docs/guides/APPS_SCRIPT_AUTOMATION.md` | Web App 방식 (대안) |

---

## 🚀 시작 가이드

### 신규 사용자 (처음 설정)

```
1. README.md 읽기 (5분)
   └─ 프로젝트 이해

2. TIME_TRIGGER_SETUP.md 따라하기 (2분)
   └─ Apps Script Time Trigger 설정

3. 테스트 실행
   └─ python src/main.py

4. 완료! ✅
```

### 기존 사용자 (일상 사용)

```
매시간 (또는 필요 시):
└─ python src/main.py

자동 실행 설정:
└─ Windows Task Scheduler 또는 Cron
```

---

## 📊 데이터 흐름

```
┌─────────────────────────────────────────────────┐
│  WSOP 사이트                                     │
│  https://staff.wsopplus.com                     │
└──────────────────┬──────────────────────────────┘
                   │ Python (Selenium)
                   │ src/wsop_scraper.py
                   ▼
┌─────────────────────────────────────────────────┐
│  downloads/Seats.csv                            │
│  (로컬 파일)                                     │
└──────────────────┬──────────────────────────────┘
                   │ Python (gspread)
                   │ src/sheets_uploader.py
                   ▼
┌─────────────────────────────────────────────────┐
│  TARGET Type 시트                               │
│  ID: 19e7e...Whj4                               │
└──────────────────┬──────────────────────────────┘
                   │ Apps Script (Time Trigger)
                   │ gs/keyplayer.gs
                   ▼
┌─────────────────────────────────────────────────┐
│  SOURCE Confirmed 시트                          │
│  ID: 1bGot...Naxg                               │
│  (Key Player 마스터 리스트)                      │
└──────────────────┬──────────────────────────────┘
                   │ Apps Script (매칭)
                   │ 부분 일치 비교
                   ▼
┌─────────────────────────────────────────────────┐
│  TARGET Type 시트 업데이트                       │
│  - K열: Key Player 마킹 (TRUE)                 │
│  - L열: 이름 축약 (L. Beach)                   │
└─────────────────────────────────────────────────┘
```

---

## 🔍 핵심 설정 파일

### .env (환경 변수)
```bash
WSOP_USERNAME=dean.hong@ggproduction.net
WSOP_PASSWORD=9311009aA
WSOP_URL=https://staff.wsopplus.com/...

SOURCE_SPREADSHEET_ID=1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg
TARGET_SPREADSHEET_ID=19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4

DOWNLOAD_PATH=downloads
```

### credentials.json (Google API)
- Service Account JSON 키
- Google Sheets API + Google Drive API 권한
- 양쪽 시트에 편집자 권한 부여 필요

---

## 🎯 다음 단계

1. ✅ 프로젝트 구조 이해 (이 문서)
2. ✅ [TIME_TRIGGER_SETUP.md](TIME_TRIGGER_SETUP.md) - Time Trigger 설정
3. ✅ [AUTOMATION_COMPLETE.md](AUTOMATION_COMPLETE.md) - 전체 워크플로우 이해
4. ✅ `python src/main.py` - 첫 실행
5. ✅ Windows Task Scheduler 등록 (매시간 자동)

---

**버전**: 1.0.0 | **마지막 업데이트**: 2025-10-17
