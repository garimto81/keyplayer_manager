# PRD-0001 Summary: WSOP 자동화 시스템

**버전**: 1.0.0 | **상태**: ✅ 완료 | **날짜**: 2025-01-17

---

## 📋 1줄 요약
WSOP 플레이어 리스트 자동 수집 → Google Sheets 업로드 → 키 플레이어 마킹을 완전 자동화하는 시스템

---

## 🎯 핵심 목표 (3가지)

1. **자동 데이터 수집**: WSOP 사이트 로그인 → CSV 다운로드
2. **자동 데이터 동기화**: Google Sheets 업로드 + Apps Script 트리거
3. **스케줄 자동화**: 1시간마다 무인 실행

---

## ✅ 주요 기능 (5가지)

| 기능 | 설명 | 상태 |
|------|------|------|
| **WSOP 스크래핑** | Selenium으로 로그인 + CSV 다운로드 | ✅ |
| **세션 관리** | 쿠키 저장/재사용 (24시간당 1회 로그인) | ✅ |
| **Sheets 연동** | gspread로 자동 업로드 | ✅ |
| **키 플레이어 마킹** | Apps Script로 자동 마킹 | ✅ |
| **스케줄링** | Task Scheduler/Cron 자동 실행 | ✅ |

---

## 📊 성능 지표

| 지표 | 목표 | 달성 |
|------|------|------|
| 실행 시간 | <5분 | ✅ ~2분 |
| 자동화율 | 100% | ✅ 100% |
| 로그인 빈도 | 24시간당 1회 | ✅ 1회 |
| 에러율 | <5% | ✅ ~1% |

---

## 🏗️ 아키텍처 (간단)

```
[Task Scheduler]
    ↓ 1시간마다
[main.py]
    ├─ wsop_scraper.py → WSOP 사이트 (CSV)
    └─ sheets_uploader.py → Google Sheets
                              ↓
                        Apps Script (키 플레이어 마킹)
```

---

## 🛠️ 기술 스택

- **언어**: Python 3.8+
- **주요 라이브러리**: Selenium, gspread, oauth2client
- **Apps Script**: JavaScript (Google)
- **스케줄러**: Windows Task Scheduler / Linux Cron

---

## 🚀 빠른 시작 (3단계)

```bash
# 1. 설치
pip install -r requirements.txt

# 2. 설정
cp .env.example .env  # 로그인 정보 입력
# credentials.json 배치

# 3. 실행
python src/main.py
```

---

## 📁 핵심 파일 (Top 5)

1. **[src/main.py](../../src/main.py)** - 메인 실행 스크립트
2. **[src/wsop_scraper.py](../../src/wsop_scraper.py)** - WSOP 자동화
3. **[src/session_manager.py](../../src/session_manager.py)** - 세션 관리
4. **[gs/keyplayer_improved.gs](../../gs/keyplayer_improved.gs)** - Apps Script (개선)
5. **[.env](../../.env.example)** - 환경 설정

---

## ⚠️ 주의사항

1. **보안**: `.env`, `credentials.json`, `session_cookies.pkl` Git 커밋 금지
2. **계정**: 세션 재사용으로 로그인 최소화 (24시간당 1회)
3. **에러**: 로그 파일 확인 (`logs/automation_*.log`)

---

## 🔗 문서 링크

| 문서 | 용도 |
|------|------|
| [전체 PRD](0001-prd-wsop-automation.md) | 상세 요구사항 |
| [README.md](../../README.md) | 설치 및 사용 가이드 |
| [QUICK_START.md](../../QUICK_START.md) | 5분 빠른 시작 |
| [SESSION_GUIDE.md](../../SESSION_GUIDE.md) | 세션 관리 설명 |

---

**업데이트**: 2025-01-17