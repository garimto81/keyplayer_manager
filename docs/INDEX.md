# 📚 프로젝트 문서 인덱스

**프로젝트**: Key Player Manager
**버전**: 1.0.0
**업데이트**: 2025-01-17

---

## 🎯 시작하기

### 신규 사용자
1. **[README.md](../README.md)** ⭐ - 프로젝트 전체 개요 및 설치 가이드
2. **[guides/QUICK_START.md](guides/QUICK_START.md)** ⚡ - 5분 빠른 시작 가이드
3. **[PRD Summary](../tasks/prds/0001-prd-summary.md)** 📋 - 프로젝트 요약

### 기존 사용자
- **[guides/SESSION_GUIDE.md](guides/SESSION_GUIDE.md)** 🔐 - 세션 관리 심화
- **[APPS_SCRIPT_IMPROVEMENTS.md](APPS_SCRIPT_IMPROVEMENTS.md)** 🚀 - Apps Script 최적화

---

## 📂 문서 구조

```
keyplayer_manager/
├── README.md                        # ⭐ 메인 가이드
├── docs/
│   ├── INDEX.md                     # 📚 이 문서
│   ├── guides/
│   │   ├── QUICK_START.md           # ⚡ 빠른 시작
│   │   └── SESSION_GUIDE.md         # 🔐 세션 관리
│   └── APPS_SCRIPT_IMPROVEMENTS.md  # 🚀 Apps Script 개선
├── tasks/
│   └── prds/
│       ├── 0001-prd-wsop-automation.md  # 📋 전체 PRD
│       └── 0001-prd-summary.md           # 📄 PRD 요약
└── tests/
    ├── test_auto.py                 # 🧪 로그인 테스트
    ├── test_csv_download.py         # 🧪 CSV 다운로드 테스트
    ├── test_session_reuse.py        # 🧪 세션 재사용 테스트
    └── test_step_by_step.py         # 🧪 단계별 테스트
```

---

## 📖 문서별 용도

### 🎯 빠른 참조

| 문서 | 용도 | 대상 독자 | 소요 시간 |
|------|------|----------|----------|
| **README.md** | 전체 설치 및 사용법 | 모든 사용자 | 10분 |
| **QUICK_START.md** | 최소 설정으로 빠른 시작 | 신규 사용자 | 5분 |
| **PRD Summary** | 프로젝트 핵심 요약 | PM, 개발자 | 2분 |
| **SESSION_GUIDE.md** | 세션 관리 상세 설명 | 개발자 | 8분 |
| **APPS_SCRIPT_IMPROVEMENTS.md** | Apps Script 최적화 | 개발자 | 15분 |
| **PRD (전체)** | 완전한 요구사항 명세 | PM, Tech Lead | 30분 |

---

## 🔍 상황별 가이드

### 📦 설치 및 설정
1. [README.md - 설치](../README.md#설치) - Python 패키지 설치
2. [README.md - 환경 설정](../README.md#환경-설정) - `.env` 및 `credentials.json`
3. [QUICK_START.md - 빠른 설정](guides/QUICK_START.md) - 5분 완성
4. **[TESTING_COMPLETE.md - 테스트 현황](guides/TESTING_COMPLETE.md)** ⭐ - 완료/대기 단계

### 🚀 실행 및 사용
1. [README.md - 사용법](../README.md#사용법) - 수동 실행
2. [README.md - 자동 스케줄링](../README.md#자동-스케줄링) - Task Scheduler/Cron
3. [SESSION_GUIDE.md - 세션 관리](guides/SESSION_GUIDE.md) - 로그인 최소화

### 🐛 문제 해결
1. [README.md - 트러블슈팅](../README.md#트러블슈팅) - 일반적인 문제
2. [SESSION_GUIDE.md - FAQ](guides/SESSION_GUIDE.md#faq) - 세션 관련
3. [APPS_SCRIPT_IMPROVEMENTS.md - 문제 해결](APPS_SCRIPT_IMPROVEMENTS.md#문제-해결) - Apps Script

### 🔧 개발 및 커스터마이징
1. [PRD (전체)](../tasks/prds/0001-prd-wsop-automation.md) - 요구사항 명세
2. [APPS_SCRIPT_IMPROVEMENTS.md](APPS_SCRIPT_IMPROVEMENTS.md) - Apps Script 최적화
3. [README.md - 커스터마이징](../README.md#커스터마이징) - 설정 변경

---

## 🧪 테스트

### 단위 테스트
- **[tests/test_auto.py](../tests/test_auto.py)** - 로그인 자동 테스트
- **[tests/test_csv_download.py](../tests/test_csv_download.py)** - CSV 다운로드 테스트
- **[tests/test_session_reuse.py](../tests/test_session_reuse.py)** - 세션 재사용 테스트

### 수동 테스트
- **[scripts/test_google_auth.py](../scripts/test_google_auth.py)** - Google API 인증 테스트
- **[scripts/test_wsop_login.py](../scripts/test_wsop_login.py)** - WSOP 로그인 필드 확인

### 통합 테스트
- **[tests/test_step_by_step.py](../tests/test_step_by_step.py)** - 단계별 대화형 테스트

---

## 📊 PRD (Product Requirements Document)

### PRD 문서 구조
```
tasks/prds/
├── 0001-prd-wsop-automation.md    # 전체 PRD (368줄)
│   ├── 1. 개요
│   ├── 2. 목표 및 성공 지표
│   ├── 3. 사용자 스토리
│   ├── 4. 기능 요구사항
│   ├── 5. 비기능 요구사항
│   ├── 6-15. (기타 섹션)
│
└── 0001-prd-summary.md             # PRD 요약 (110줄)
    ├── 1줄 요약
    ├── 핵심 목표
    ├── 주요 기능
    ├── 성능 지표
    └── 빠른 시작
```

### PRD 읽기 가이드
- **빠른 이해**: [PRD Summary](../tasks/prds/0001-prd-summary.md) (2분)
- **상세 내용**: [전체 PRD](../tasks/prds/0001-prd-wsop-automation.md) (30분)

---

## 🔗 외부 참조

### 공식 문서
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Apps Script](https://developers.google.com/apps-script)

### 커뮤니티
- [Python Selenium Tutorial](https://selenium-python.readthedocs.io/)
- [gspread Documentation](https://docs.gspread.org/)

---

## 📝 문서 업데이트 가이드

### 문서 추가 시
1. 이 INDEX.md에 링크 추가
2. README.md에 필요시 참조 추가
3. PRD에 반영 (기능 변경 시)

### 문서 수정 시
- 파일 상단에 **업데이트 날짜** 명시
- 주요 변경사항은 **Version History** 섹션에 기록

---

## 🎯 다음 단계

### 신규 사용자
1. ✅ [README.md](../README.md) 읽기
2. ✅ [QUICK_START.md](guides/QUICK_START.md) 따라하기
3. ✅ 첫 실행 성공
4. ✅ [SESSION_GUIDE.md](guides/SESSION_GUIDE.md) 이해
5. ✅ 자동 스케줄러 등록

### 개발자
1. ✅ [PRD (전체)](../tasks/prds/0001-prd-wsop-automation.md) 읽기
2. ✅ 코드 구조 파악 (`src/`)
3. ✅ [APPS_SCRIPT_IMPROVEMENTS.md](APPS_SCRIPT_IMPROVEMENTS.md) 리뷰
4. ✅ 테스트 실행 (`tests/`)
5. ✅ 커스터마이징

---

## 📞 지원

- **이슈**: GitHub Issues
- **문의**: dean.hong@ggproduction.net

---

**버전**: 1.0.0 | **마지막 업데이트**: 2025-01-17