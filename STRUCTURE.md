# 📁 프로젝트 파일 구조

**프로젝트**: Key Player Manager
**버전**: 1.0.0
**업데이트**: 2025-01-17

---

## 🎯 최적화된 구조

```
keyplayer_manager/
├── 📄 README.md                    ⭐ 메인 가이드 (343줄)
├── 📄 STRUCTURE.md                 📋 이 문서 (파일 구조 설명)
├── 📄 .env.example                 🔐 환경 변수 템플릿
├── 📄 .gitignore                   🚫 Git 제외 목록
├── 📄 requirements.txt             📦 Python 패키지
├── 📄 setup.py                     🔧 초기 설정 스크립트
│
├── 📂 docs/                        📚 모든 문서
│   ├── 📄 INDEX.md                 📚 문서 인덱스 (메인)
│   ├── 📄 APPS_SCRIPT_IMPROVEMENTS.md  🚀 Apps Script 개선 (440줄)
│   └── 📂 guides/                  📖 사용자 가이드
│       ├── 📄 QUICK_START.md       ⚡ 5분 빠른 시작 (143줄)
│       └── 📄 SESSION_GUIDE.md     🔐 세션 관리 상세 (289줄)
│
├── 📂 tasks/                       📋 PRD 및 작업 관리
│   └── 📂 prds/
│       ├── 📄 0001-prd-wsop-automation.md     📋 전체 PRD (368줄)
│       └── 📄 0001-prd-summary.md             📄 PRD 요약 (110줄)
│
├── 📂 src/                         💻 소스 코드
│   ├── 🐍 main.py                  ⭐ 메인 실행 스크립트
│   ├── 🐍 wsop_scraper.py          🌐 WSOP 스크래핑 (Selenium)
│   ├── 🐍 session_manager.py       🔐 세션 관리 (쿠키 저장/로드)
│   └── 🐍 sheets_uploader.py       📊 Google Sheets 업로드
│
├── 📂 gs/                          📜 Google Apps Script
│   ├── 📜 keyplayer.gs             📄 기존 Apps Script
│   ├── 📜 keyplayer_improved.gs    ✨ 개선된 버전 (75% 빠름)
│   └── 📜 keyplayer_api.gs         🔌 Web App API
│
├── 📂 scripts/                     🔧 유틸리티 스크립트
│   ├── 🐍 test_google_auth.py      🧪 Google API 테스트
│   ├── 🐍 test_wsop_login.py       🧪 WSOP 로그인 확인
│   ├── 📜 run_once.bat             ▶️ Windows 수동 실행
│   └── 📜 schedule_task_windows.bat ⏰ Windows 스케줄러 등록
│
├── 📂 tests/                       🧪 테스트 스크립트 (이동됨)
│   ├── 🐍 test_auto.py             ✅ 로그인 자동 테스트
│   ├── 🐍 test_csv_download.py     ✅ CSV 다운로드 테스트
│   ├── 🐍 test_session_reuse.py    ✅ 세션 재사용 테스트
│   └── 🐍 test_step_by_step.py     ✅ 단계별 대화형 테스트
│
├── 📂 downloads/                   📥 CSV 다운로드 폴더
├── 📂 logs/                        📝 실행 로그
│
├── 🔐 .env                         🚫 환경 변수 (Git 제외)
├── 🔐 credentials.json             🚫 Google API 키 (Git 제외)
└── 🔐 session_cookies.pkl          🚫 세션 쿠키 (Git 제외)
```

---

## 📊 파일 통계

### 문서 (Markdown)
| 파일 | 줄 수 | 용도 |
|------|-------|------|
| README.md | 343 | 메인 가이드 |
| APPS_SCRIPT_IMPROVEMENTS.md | 440 | Apps Script 개선 분석 |
| 0001-prd-wsop-automation.md | 368 | 전체 PRD |
| SESSION_GUIDE.md | 289 | 세션 관리 상세 |
| QUICK_START.md | 143 | 빠른 시작 |
| 0001-prd-summary.md | 110 | PRD 요약 |
| INDEX.md | ~200 | 문서 인덱스 |
| **합계** | **~1,900** | 7개 문서 |

### 소스 코드 (Python)
| 파일 | 역할 | 줄 수 |
|------|------|-------|
| main.py | 메인 실행 | ~110 |
| wsop_scraper.py | WSOP 자동화 | ~270 |
| session_manager.py | 세션 관리 | ~230 |
| sheets_uploader.py | Sheets 업로드 | ~120 |
| **합계** | 4개 모듈 | **~730** |

### Apps Script (JavaScript)
| 파일 | 역할 | 줄 수 |
|------|------|-------|
| keyplayer.gs | 기존 로직 | 97 |
| keyplayer_improved.gs | 개선 버전 | 220 |
| keyplayer_api.gs | Web App API | 80 |
| **합계** | 3개 스크립트 | **~400** |

### 테스트 (Python)
| 파일 | 역할 | 줄 수 |
|------|------|-------|
| test_auto.py | 로그인 테스트 | ~210 |
| test_csv_download.py | CSV 다운로드 | ~170 |
| test_session_reuse.py | 세션 재사용 | ~90 |
| test_step_by_step.py | 대화형 테스트 | ~360 |
| test_google_auth.py | Google API | ~60 |
| test_wsop_login.py | WSOP 로그인 | ~100 |
| **합계** | 6개 테스트 | **~990** |

---

## 🎯 핵심 파일 Top 10

### 실행 & 자동화
1. **[src/main.py](src/main.py)** ⭐ - 메인 실행 스크립트
2. **[src/wsop_scraper.py](src/wsop_scraper.py)** 🌐 - WSOP 자동화
3. **[src/session_manager.py](src/session_manager.py)** 🔐 - 세션 관리
4. **[gs/keyplayer_improved.gs](gs/keyplayer_improved.gs)** ✨ - Apps Script (개선)

### 문서
5. **[README.md](README.md)** 📖 - 메인 가이드
6. **[docs/INDEX.md](docs/INDEX.md)** 📚 - 문서 인덱스
7. **[docs/guides/QUICK_START.md](docs/guides/QUICK_START.md)** ⚡ - 빠른 시작
8. **[tasks/prds/0001-prd-summary.md](tasks/prds/0001-prd-summary.md)** 📋 - PRD 요약

### 설정
9. **[.env.example](.env.example)** 🔐 - 환경 변수 템플릿
10. **[requirements.txt](requirements.txt)** 📦 - 패키지 목록

---

## 📂 디렉토리별 설명

### 📚 docs/ (문서)
**목적**: 모든 사용자 문서 중앙 집중화

**구조**:
- `INDEX.md` - 문서 메인 허브
- `guides/` - 사용자 가이드
  - `QUICK_START.md` - 신규 사용자용
  - `SESSION_GUIDE.md` - 세션 관리 심화
- `APPS_SCRIPT_IMPROVEMENTS.md` - 개발자용

**장점**:
- 찾기 쉬움
- 계층 구조 명확
- 문서 간 링크 관리 용이

### 📋 tasks/prds/ (PRD)
**목적**: 제품 요구사항 문서 관리

**구조**:
- `####-prd-feature-name.md` - 전체 PRD
- `####-prd-summary.md` - 요약 버전

**규칙**:
- 번호: 0001부터 시작
- 이름: 케밥-케이스 (kebab-case)
- 버전: PRD 내부에 버전 히스토리

### 💻 src/ (소스 코드)
**목적**: 실행 가능한 Python 모듈

**구조**:
- `main.py` - 진입점 (Entry Point)
- 나머지 - 모듈 (독립 클래스)

**원칙**:
- 한 파일 = 한 책임
- 모든 클래스 독립 테스트 가능
- 순환 의존성 없음

### 🧪 tests/ (테스트)
**목적**: 단위/통합 테스트 스크립트

**구조**:
- `test_*.py` - pytest 규칙 따름
- 각 모듈별 테스트 파일

**장점**:
- 루트 디렉토리 깔끔
- 테스트 자동 발견 (pytest)
- CI/CD 통합 용이

---

## 🔄 구조 변경 사항

### v1.0.0 (2025-01-17)

#### ✅ 추가됨
```diff
+ docs/INDEX.md                      # 문서 인덱스
+ docs/guides/                       # 가이드 디렉토리
+ tasks/prds/                        # PRD 디렉토리
+ tests/                             # 테스트 디렉토리
+ STRUCTURE.md                       # 이 문서
```

#### 🔄 이동됨
```diff
- QUICK_START.md              → docs/guides/QUICK_START.md
- SESSION_GUIDE.md            → docs/guides/SESSION_GUIDE.md
- test_*.py                   → tests/test_*.py
```

#### 🎯 유지됨
```
README.md                     # 루트에 유지 (메인 진입점)
src/                          # 소스 코드
gs/                           # Apps Script
scripts/                      # 유틸리티
```

---

## 📖 문서 읽기 순서

### �� 신규 사용자
1. **[README.md](README.md)** - 전체 개요
2. **[docs/guides/QUICK_START.md](docs/guides/QUICK_START.md)** - 빠른 시작
3. **[tasks/prds/0001-prd-summary.md](tasks/prds/0001-prd-summary.md)** - 프로젝트 이해

### 👨‍💻 개발자
1. **[tasks/prds/0001-prd-wsop-automation.md](tasks/prds/0001-prd-wsop-automation.md)** - 요구사항
2. **[docs/INDEX.md](docs/INDEX.md)** - 문서 맵
3. **[docs/APPS_SCRIPT_IMPROVEMENTS.md](docs/APPS_SCRIPT_IMPROVEMENTS.md)** - 최적화

### 🔧 유지보수
1. **[docs/guides/SESSION_GUIDE.md](docs/guides/SESSION_GUIDE.md)** - 세션 관리
2. **[README.md#트러블슈팅](README.md#트러블슈팅)** - 문제 해결
3. **[logs/](logs/)** - 실행 로그

---

## 🎯 디자인 원칙

### 1. **SSOT (Single Source of Truth)**
- 각 정보는 한 곳에만 정의
- 중복 없음
- 참조는 링크 사용

### 2. **레이어 분리**
```
사용자 문서 (docs/)
    ↓
요구사항 (tasks/prds/)
    ↓
소스 코드 (src/)
    ↓
테스트 (tests/)
```

### 3. **발견 가능성 (Discoverability)**
- `docs/INDEX.md` - 모든 문서 링크
- `README.md` - 메인 진입점
- 파일명 명확 (`test_`, `prd-`)

### 4. **확장성 (Scalability)**
```
tasks/prds/
├── 0001-prd-wsop-automation.md
├── 0002-prd-slack-integration.md    # 향후
└── 0003-prd-web-dashboard.md        # 향후
```

---

## 🔍 파일 찾기 가이드

### "빠르게 시작하고 싶어요"
→ [docs/guides/QUICK_START.md](docs/guides/QUICK_START.md)

### "세션 관리가 궁금해요"
→ [docs/guides/SESSION_GUIDE.md](docs/guides/SESSION_GUIDE.md)

### "Apps Script를 개선하고 싶어요"
→ [docs/APPS_SCRIPT_IMPROVEMENTS.md](docs/APPS_SCRIPT_IMPROVEMENTS.md)

### "전체 요구사항이 궁금해요"
→ [tasks/prds/0001-prd-wsop-automation.md](tasks/prds/0001-prd-wsop-automation.md)

### "모든 문서 목록이 필요해요"
→ [docs/INDEX.md](docs/INDEX.md)

### "소스 코드를 보고 싶어요"
→ [src/](src/)

### "테스트를 실행하고 싶어요"
→ [tests/](tests/)

---

## 📞 지원

- **이슈**: GitHub Issues
- **문의**: dean.hong@ggproduction.net
- **문서**: [docs/INDEX.md](docs/INDEX.md)

---

**v1.0.0** | **마지막 업데이트**: 2025-01-17