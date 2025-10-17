# 완전한 워크플로우 테스트 가이드

**버전**: 1.0.0
**업데이트**: 2025-10-17

---

## ✅ 완료된 테스트

### 1. WSOP 로그인 ✅
- **상태**: 성공
- **세션 관리**: 작동 중 (24시간 쿠키 유효)
- **테스트 파일**: `tests/test_auto.py`, `tests/test_session_reuse.py`

### 2. CSV 다운로드 ✅
- **상태**: 성공
- **파일**: `downloads/Seats.csv` (67행)
- **컬럼**: PlayerName, Nationality, ChipCount 등 10개
- **해결 사항**: ElementClickInterceptedException → JavaScript 클릭으로 해결

**다운로드 로직 (3단계 폴백)**:
```python
# 1. JavaScript 클릭 (오버레이 무시) ← 현재 작동
self.driver.execute_script("arguments[0].click();", export_button)

# 2. 중앙 스크롤 후 클릭 (폴백 1)
self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_button)
export_button.click()

# 3. ActionChains (폴백 2)
ActionChains(self.driver).move_to_element(export_button).click().perform()
```

---

## 🔄 다음 테스트 단계

### 3. Google Sheets 업로드 ✅
- **상태**: 성공
- **업로드된 데이터**: 67행
- **시트**: Confirmed (SOURCE_SPREADSHEET_ID)
- **소요 시간**: ~2초
- **테스트 파일**: `tests/test_sheets_upload.py`

**참고**: Service Account 키 파일(`credentials.json`)이 이미 설정되어 있어 즉시 작동

#### 3.1. Service Account 생성
1. [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts) 접속
2. 프로젝트 생성 (예: "WSOP-Automation")
3. Service Account 생성:
   - 이름: `wsop-sheets-uploader`
   - 역할: **Editor**
4. JSON 키 생성 → `credentials.json` 다운로드
5. 프로젝트 루트에 `credentials.json` 복사

#### 3.2. Google Sheets API 활성화
1. [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) 활성화
2. [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) 활성화

#### 3.3. Spreadsheet 권한 부여
1. Google Sheets 열기:
   - **SOURCE**: `1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg` (Confirmed 시트)
   - **TARGET**: `19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4` (type 시트)
2. 각 시트의 **공유 → Service Account 이메일 추가** (편집자 권한)
   - Service Account 이메일: `credentials.json`의 `client_email` 필드 확인

#### 3.4. 테스트 실행
```bash
# Google Sheets 업로드 테스트
python src/sheets_uploader.py

# 또는 전체 워크플로우
python src/main.py
```

---

### 4. Apps Script 트리거 ⏳
**파일**: `gs/keyplayer_api.gs`

#### 4.1. Web App 배포
1. [Google Apps Script](https://script.google.com) 열기
2. 프로젝트 선택 또는 새로 만들기
3. `gs/keyplayer_api.gs` 코드 복사
4. **배포 → 새 배포**:
   - 유형: **웹 앱**
   - 실행 계정: **나**
   - 액세스 권한: **모든 사용자**
5. 배포 URL 복사 → `.env`의 `APPS_SCRIPT_URL` 설정

#### 4.2. 테스트
```bash
curl -X POST "https://script.google.com/macros/s/.../exec"
```

---

### 5. 스케줄러 설정 ⏳
**목표**: 매시간 자동 실행

#### Windows (Task Scheduler)
```bash
# 1. Task Scheduler 열기
taskschd.msc

# 2. 작업 만들기
- 이름: WSOP-Hourly-Automation
- 트리거: 매일 매시간 반복
- 작업: python.exe
- 인수: d:\AI\claude01\keyplayer_manager\src\main.py
```

#### Linux (Cron)
```bash
# 매시간 실행
crontab -e
0 * * * * cd /path/to/keyplayer_manager && python src/main.py >> logs/automation.log 2>&1
```

---

## 📊 테스트 결과 요약

| 단계 | 상태 | 소요 시간 | 비고 |
|------|------|-----------|------|
| 1. 로그인 | ✅ 성공 | 7초 | 세션 재사용 시 0.1초 |
| 2. CSV 다운로드 | ✅ 성공 | 3초 | JavaScript 클릭 방식 |
| 3. Sheets 업로드 | ✅ 성공 | 2초 | 67행 업로드 완료 |
| 4. Apps Script | ⏳ 대기 | - | Web App 배포 필요 |
| 5. 스케줄러 | ⏳ 대기 | - | 단계 4 완료 후 |

---

## 🐛 해결된 이슈

### Issue #1: ElementClickInterceptedException
**문제**: Export 버튼 클릭 시 time-zone div 오버레이가 클릭 차단
**원인**: Selenium의 일반 click()은 실제 마우스 좌표 클릭 시뮬레이션
**해결**: JavaScript `element.click()` 사용으로 DOM 직접 조작
**파일**: [wsop_scraper.py:210](../../src/wsop_scraper.py#L210)

### Issue #2: UnicodeEncodeError (Windows Console)
**문제**: 한글/이모지 출력 시 `cp949` 인코딩 오류
**원인**: Windows 기본 콘솔 인코딩
**해결**: UTF-8 wrapper 추가
**파일**: [wsop_scraper.py:12-18](../../src/wsop_scraper.py#L12)

---

## 🔧 트러블슈팅

### CSV 다운로드 실패 시
```bash
# 1. 버튼 위치 확인
python tests/test_find_export_button.py

# 2. 수동 대기 시간 증가
# wsop_scraper.py:212 수정
download_wait = 60  # 30 → 60초
```

### 세션 만료 시
```bash
# 세션 파일 삭제 후 재로그인
rm session_cookies.pkl
python src/wsop_scraper.py
```

### Google Sheets 업로드 실패 시
```bash
# 1. credentials.json 경로 확인
ls credentials.json

# 2. Service Account 이메일 권한 확인
# Google Sheets → 공유 → [Service Account 이메일] 편집자 권한

# 3. API 활성화 확인
# https://console.cloud.google.com/apis/dashboard
```

---

## 📈 성능 지표

**현재 (단계 1-3 완료)**:
- 초기 로그인: ~7초
- 세션 재사용: ~0.1초 (로그인 생략)
- CSV 다운로드: ~3초
- Google Sheets 업로드: ~2초
- **총 실행 시간**: ~12초 (초기) / ~5초 (재사용)

**예상 (전체 완료 시)**:
- Apps Script 실행: ~5초
- **총 실행 시간**: ~17초 (초기) / ~10초 (재사용)

---

## 🎯 다음 액션

1. ✅ ~~Google Service Account 생성~~ (완료)
2. ✅ ~~Google Sheets 업로드 테스트~~ (완료)
3. **다음**: Apps Script Web App 배포 ([배포 가이드](APPS_SCRIPT_DEPLOY.md) 참조)
4. **마지막**: 스케줄러 설정

---

**참조 문서**:
- [Quick Start](QUICK_START.md)
- [Session Guide](SESSION_GUIDE.md)
- [PRD Summary](../../tasks/prds/0001-prd-summary.md)