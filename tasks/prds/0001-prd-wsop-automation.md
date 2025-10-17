# PRD-0001: WSOP 플레이어 자동 수집 및 키 플레이어 마킹 시스템

**작성일**: 2025-01-17
**버전**: 1.0.0
**상태**: ✅ 구현 완료
**담당자**: Dean Hong

---

## 1. 개요 (Overview)

### 1.1 프로젝트 목적
WSOP(World Series of Poker) 스태프 사이트에서 플레이어 리스트를 자동으로 다운로드하고, Google Sheets에 업로드한 후 키 플레이어를 자동으로 마킹하는 완전 자동화 시스템 구축.

### 1.2 배경
- 매번 수동으로 로그인하여 CSV 다운로드
- Google Sheets에 수동으로 복사/붙여넣기
- Apps Script를 수동으로 실행하여 키 플레이어 마킹
- 반복 작업으로 인한 시간 낭비 및 실수 가능성

### 1.3 비즈니스 가치
- **시간 절감**: 수동 작업 15분 → 자동화 2분 (87% 감소)
- **정확성 향상**: 수동 입력 오류 제거
- **확장성**: 1시간마다 자동 실행 가능
- **계정 안전**: 세션 재사용으로 로그인 횟수 최소화

---

## 2. 목표 및 성공 지표 (Goals & Metrics)

### 2.1 핵심 목표
1. ✅ WSOP 사이트 자동 로그인 및 CSV 다운로드
2. ✅ Google Sheets 자동 업로드
3. ✅ Apps Script 자동 트리거
4. ✅ 1시간마다 자동 실행
5. ✅ 세션 유지로 로그인 횟수 최소화

### 2.2 성공 지표
| 지표 | 목표 | 현재 상태 |
|------|------|----------|
| 자동화율 | 100% | ✅ 100% |
| 실행 시간 | <5분 | ✅ ~2분 |
| 에러율 | <5% | ✅ ~1% |
| 로그인 빈도 | 24시간당 1회 | ✅ 24시간당 1회 |

---

## 3. 사용자 스토리 (User Stories)

### 3.1 주요 사용자
- **스태프**: WSOP 토너먼트 관리자
- **분석가**: 플레이어 데이터 분석팀

### 3.2 사용자 스토리

**US-1: 자동 데이터 수집**
```
As a 스태프
I want to 플레이어 리스트가 자동으로 수집되길
So that 수동 작업 없이 최신 데이터를 확보할 수 있다
```

**US-2: 키 플레이어 식별**
```
As a 분석가
I want to 키 플레이어가 자동으로 마킹되길
So that 중요 플레이어를 빠르게 식별할 수 있다
```

**US-3: 오류 알림**
```
As a 시스템 관리자
I want to 오류 발생 시 알림을 받길
So that 문제를 신속하게 해결할 수 있다
```

---

## 4. 기능 요구사항 (Functional Requirements)

### 4.1 WSOP 스크래핑 (FR-1)

#### FR-1.1 로그인
- **필수**: Username/Password로 자동 로그인
- **필수**: 세션 쿠키 저장 (24시간 유효)
- **필수**: 세션 만료 시 자동 재로그인
- **선택**: 다중 계정 지원

#### FR-1.2 CSV 다운로드
- **필수**: "Export player list to csv" 버튼 자동 클릭
- **필수**: 다운로드 완료 대기 (최대 30초)
- **필수**: 다운로드 실패 시 재시도 (최대 3회)

### 4.2 Google Sheets 연동 (FR-2)

#### FR-2.1 데이터 업로드
- **필수**: CSV를 Confirmed 시트에 업로드
- **필수**: 기존 데이터 클리어 후 새 데이터 삽입
- **필수**: 헤더 유지

#### FR-2.2 Apps Script 트리거
- **선택**: Web App URL로 HTTP 요청
- **대안**: 수동 실행

### 4.3 Apps Script 로직 (FR-3)

#### FR-3.1 키 플레이어 마킹
- **필수**: Confirmed 시트 E열에서 키 플레이어 목록 수집
- **필수**: Type 시트 H열과 비교하여 매칭
- **필수**: Type 시트 K열에 TRUE/FALSE 마킹
- **필수**: Type 시트 L열에 축약 이름 생성

#### FR-3.2 체크박스 업데이트
- **필수**: Confirmed 시트 B열 체크박스 자동 체크

### 4.4 스케줄링 (FR-4)

#### FR-4.1 주기적 실행
- **필수**: Windows Task Scheduler 지원
- **선택**: Linux Cron 지원
- **설정 가능**: 실행 주기 (기본 1시간)

---

## 5. 비기능 요구사항 (Non-Functional Requirements)

### 5.1 성능 (Performance)
- **응답 시간**: 전체 실행 < 5분
- **동시 사용자**: 단일 계정 (동시 로그인 불가)
- **데이터 크기**: 최대 10,000행 지원

### 5.2 안정성 (Reliability)
- **가용성**: 99% (트리거 기반)
- **에러 처리**: 모든 단계에서 try-catch
- **복구**: 실패 시 다음 주기에 자동 재시도

### 5.3 보안 (Security)
- **인증**: .env 파일로 비밀번호 관리
- **쿠키**: 로컬 파일로만 저장 (세션 재사용)
- **API 키**: credentials.json (Service Account)
- **.gitignore**: 모든 비밀 정보 제외

### 5.4 확장성 (Scalability)
- **다중 이벤트**: URL만 변경하면 다른 토너먼트 지원
- **다중 시트**: 여러 Google Sheets 동시 관리 가능

### 5.5 유지보수성 (Maintainability)
- **모듈화**: 각 기능을 독립 클래스로 분리
- **로그**: 모든 작업 로그 기록
- **문서화**: README, QUICK_START, SESSION_GUIDE

---

## 6. 제외 사항 (Out of Scope)

### 6.1 현재 버전에서 제외
- ❌ 다중 사용자 동시 접근
- ❌ 실시간 모니터링 대시보드
- ❌ 데이터 히스토리 관리 (버전 관리)
- ❌ AI 기반 플레이어 분석
- ❌ 모바일 앱

### 6.2 향후 고려 사항
- 🔮 Slack/Discord 알림 연동
- 🔮 웹 UI (Flask/Streamlit)
- 🔮 플레이어 통계 분석
- 🔮 CSV 히스토리 관리

---

## 7. 기술 스택 (Technical Stack)

### 7.1 백엔드
- **언어**: Python 3.8+
- **프레임워크**: Selenium 4.27.1
- **라이브러리**:
  - `webdriver-manager`: Chrome 드라이버 자동 관리
  - `gspread`: Google Sheets API
  - `oauth2client`: Google 인증
  - `python-dotenv`: 환경 변수 관리

### 7.2 Apps Script
- **언어**: JavaScript (Google Apps Script)
- **API**: Spreadsheet Service

### 7.3 인프라
- **스케줄러**: Windows Task Scheduler / Linux Cron
- **스토리지**: 로컬 파일 시스템
- **로그**: 파일 기반 (logs/)

---

## 8. 시스템 아키텍처 (Architecture)

### 8.1 컴포넌트 다이어그램

```
┌─────────────────────────────────────────────────────────┐
│                   Task Scheduler                        │
│              (매 1시간마다 실행)                          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   main.py                               │
│              (KeyPlayerManager)                         │
└───────┬─────────────────────┬───────────────────────────┘
        │                     │
        ▼                     ▼
┌──────────────────┐  ┌──────────────────────────┐
│  wsop_scraper.py │  │  sheets_uploader.py      │
│  (WSOPScraper)   │  │  (SheetsUploader)        │
│                  │  │                          │
│  - login()       │  │  - upload_csv()          │
│  - download_csv()│  │  - trigger_apps_script() │
└────────┬─────────┘  └───────────┬──────────────┘
         │                        │
         │                        │
┌────────┴────────┐      ┌────────┴──────────┐
│ session_manager │      │  Google Sheets    │
│ (SessionManager)│      │  API              │
│                 │      │                   │
│ - save_cookies()│      │  - Confirmed 시트 │
│ - load_cookies()│      │  - Type 시트      │
└─────────────────┘      └────────┬──────────┘
                                  │
                                  ▼
                         ┌────────────────────┐
                         │  Apps Script       │
                         │  (keyplayer.gs)    │
                         │                    │
                         │  - updateAndCheck  │
                         │    Boxes()         │
                         └────────────────────┘
```

### 8.2 데이터 플로우

```
[1] WSOP 사이트
    ↓ (Selenium)
[2] CSV 파일 (downloads/)
    ↓ (gspread)
[3] Google Sheets (Confirmed)
    ↓ (Apps Script)
[4] Google Sheets (Type) - K열, L열 업데이트
    ↓
[5] Google Sheets (Confirmed) - B열 체크박스 업데이트
```

---

## 9. 테스트 계획 (Testing Plan)

### 9.1 단위 테스트
- ✅ `test_auto.py` - 로그인 테스트
- ✅ `test_csv_download.py` - CSV 다운로드 테스트
- ✅ `test_session_reuse.py` - 세션 재사용 테스트
- ✅ `test_google_auth.py` - Google API 인증 테스트

### 9.2 통합 테스트
- ✅ `main.py` - 전체 워크플로우 테스트

### 9.3 수동 테스트
- ✅ 로그인 필드 확인 (`test_wsop_login.py`)
- ✅ Export 버튼 위치 확인
- ✅ Apps Script 수동 실행

### 9.4 부하 테스트
- 🔄 1시간 주기 24시간 연속 실행
- 🔄 1000행 데이터 처리 시간

---

## 10. 배포 계획 (Deployment Plan)

### 10.1 환경 설정
1. Python 3.8+ 설치
2. `pip install -r requirements.txt`
3. `.env` 파일 설정 (WSOP 로그인 정보)
4. `credentials.json` 배치 (Google Service Account)
5. Google Sheets 권한 부여

### 10.2 초기 실행
```bash
python setup.py
python src/main.py
```

### 10.3 스케줄러 등록
```bash
# Windows
scripts\schedule_task_windows.bat

# Linux
crontab -e
0 * * * * cd /path/to/keyplayer_manager && python3 src/main.py
```

---

## 11. 모니터링 및 알림 (Monitoring & Alerts)

### 11.1 로그
- **경로**: `logs/automation_YYYYMMDD.log`
- **로테이션**: 일별 (자동)
- **보존**: 30일

### 11.2 알림 (선택)
- **이메일**: 실패 시 SMTP 알림
- **Slack**: 웹훅 연동 (향후)

---

## 12. 위험 관리 (Risk Management)

### 12.1 식별된 위험

| 위험 | 영향 | 가능성 | 완화 방안 |
|------|------|--------|----------|
| WSOP 사이트 구조 변경 | 높음 | 중간 | 셀렉터 배열로 여러 패턴 시도 |
| 계정 차단 | 높음 | 낮음 | 세션 재사용 (24시간당 1회 로그인) |
| Google API 할당량 초과 | 중간 | 낮음 | 배치 업데이트, 캐싱 |
| Chrome 버전 불일치 | 중간 | 낮음 | webdriver-manager 자동 업데이트 |

### 12.2 비상 계획
- **자동 복구**: 다음 주기에 재시도
- **수동 개입**: 로그 확인 후 수동 실행
- **롤백**: 백업 데이터 복원 (수동)

---

## 13. 버전 히스토리 (Version History)

| 버전 | 날짜 | 변경 사항 |
|------|------|----------|
| 1.0.0 | 2025-01-17 | 초기 릴리스 |
|       |            | - WSOP 스크래핑 |
|       |            | - Google Sheets 연동 |
|       |            | - 세션 관리 |
|       |            | - Apps Script 개선 |

---

## 14. 참고 자료 (References)

### 14.1 외부 문서
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Apps Script Reference](https://developers.google.com/apps-script/reference)

### 14.2 내부 문서
- [README.md](../../README.md) - 전체 가이드
- [QUICK_START.md](../../QUICK_START.md) - 5분 빠른 시작
- [SESSION_GUIDE.md](../../SESSION_GUIDE.md) - 세션 관리 가이드
- [APPS_SCRIPT_IMPROVEMENTS.md](../../docs/APPS_SCRIPT_IMPROVEMENTS.md) - Apps Script 개선

---

## 15. 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Product Owner | Dean Hong | ✅ | 2025-01-17 |
| Tech Lead | Dean Hong | ✅ | 2025-01-17 |

---

**문서 종료**