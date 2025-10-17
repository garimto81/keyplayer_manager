# Apps Script 자동화 완전 가이드

**목적**: Python 완료 직후 Apps Script 자동 실행
**소요 시간**: 5분
**난이도**: 초급

---

## 🎯 목표

```
현재: Python (CSV 업로드) → [수동] Apps Script 실행
목표: Python (CSV 업로드) → [자동] Apps Script 실행
```

---

## 📋 사전 준비

1. ✅ Google 계정 (TARGET 시트 편집 권한)
2. ✅ `gs/keyplayer_api.gs` 파일
3. ✅ `gs/keyplayer.gs` 파일
4. ✅ TARGET 시트 접근 권한

---

## 🚀 배포 단계 (5분)

### 1단계: Apps Script 프로젝트 열기

1. **TARGET 시트 열기**:
   ```
   https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4
   ```

2. **Apps Script 편집기 열기**:
   - 메뉴: **확장 프로그램 → Apps Script**

3. **필요한 파일 확인**:
   - ✅ `keyplayer.gs` - 메인 로직 (updateAndCheckBoxes)
   - ✅ `keyplayer_api.gs` - Web App API (doGet)

   **없다면 추가**:
   - 좌측 **+** → 스크립트
   - 로컬 `gs/` 폴더에서 내용 복사

---

### 2단계: Web App 배포

1. **배포 버튼 클릭**:
   - 우측 상단 **배포 → 새 배포**

2. **유형 선택**:
   - 톱니바퀴 아이콘 ⚙️ 클릭
   - **웹 앱** 선택

3. **설정**:
   ```
   설명: WSOP Key Player API v1.0
   실행 사용자: 나
   액세스 권한: 모든 사용자
   ```

4. **배포 클릭**

5. **권한 승인** (처음만):
   - "권한 검토" 클릭
   - Google 계정 선택
   - "고급" → "{프로젝트 이름}(으)로 이동" 클릭
   - "허용" 클릭

6. **배포 URL 복사**:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```
   ⚠️ **메모장에 임시 저장**

---

### 3단계: .env 파일 설정

1. **프로젝트 루트의 .env 파일 열기**:
   ```
   d:\AI\claude01\keyplayer_manager\.env
   ```

2. **APPS_SCRIPT_URL 추가**:
   ```bash
   # WSOP 로그인 정보
   WSOP_USERNAME=dean.hong@ggproduction.net
   WSOP_PASSWORD=9311009aA
   WSOP_URL=https://staff.wsopplus.com/...

   # Google Sheets 설정
   SOURCE_SPREADSHEET_ID=1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg
   TARGET_SPREADSHEET_ID=19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4

   # Apps Script Web App URL (아래 줄 추가)
   APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycby.../exec

   # 다운로드 경로
   DOWNLOAD_PATH=downloads
   ```

3. **저장** (Ctrl+S)

---

### 4단계: 테스트

#### 테스트 1: 브라우저에서 Health Check

배포 URL을 브라우저에 입력:
```
https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?action=health
```

**예상 응답**:
```json
{
  "success": true,
  "message": "Apps Script API 정상 작동",
  "timestamp": "2025-10-17T12:00:00.000Z"
}
```

---

#### 테스트 2: Python에서 트리거

```bash
cd d:/AI/claude01/keyplayer_manager
python tests/test_trigger_apps_script.py
```

**예상 출력**:
```
============================================================
Apps Script 트리거 테스트
============================================================

Apps Script URL: https://script.google.com/macros/s/...
Google Sheets 인증 중...
✅ Google Sheets 인증 완료

Apps Script 실행 중...
(SOURCE Confirmed E열 → TARGET Type K열 매칭)
🚀 Apps Script 트리거 호출 중...
✅ Apps Script 실행 완료

✅ Apps Script 실행 완료!

결과 확인:
  - K열: Key Player 마킹 (TRUE)
  - L열: 짧은 이름 생성
```

---

#### 테스트 3: 전체 워크플로우

```bash
python src/main.py
```

**예상 로그**:
```
[2025-10-17 12:00:00] 🚀 키 플레이어 자동화 시작
[2025-10-17 12:00:07] ✅ CSV 다운로드 완료
[2025-10-17 12:00:09] ✅ 'type' 시트 업로드 완료
[2025-10-17 12:00:09] 🔄 [단계 3/3] Apps Script 실행
[2025-10-17 12:00:10] ✅ Apps Script 실행 완료  ← 자동 실행!
[2025-10-17 12:00:10] 🎉 자동화 완료! (소요시간: 10초)
```

---

## 🔧 트러블슈팅

### 오류 1: "404 Not Found"
**원인**: 배포 URL이 잘못됨
**해결**:
1. Apps Script 편집기 → 배포 → 배포 관리
2. 최신 배포 URL 복사
3. `.env` 파일 업데이트

---

### 오류 2: "권한이 필요합니다"
**원인**: 브라우저에서 권한 승인 필요
**해결**:
1. 브라우저에서 배포 URL 직접 접속
2. 권한 검토 → 허용
3. Python 스크립트 재실행

---

### 오류 3: "액세스 거부됨"
**원인**: 실행 권한 설정 오류
**해결**:
1. 배포 → 배포 관리 → 편집 (연필 아이콘)
2. 액세스 권한: "모든 사용자"로 변경
3. 배포 업데이트

---

### 오류 4: Python에서 타임아웃
**원인**: Apps Script 실행 시간 초과 (6분 제한)
**해결**:
1. `keyplayer.gs` 최적화 필요
2. 또는 timeout 값 증가:
   ```python
   # src/sheets_uploader.py
   response = requests.get(script_url, timeout=300)  # 60 → 300
   ```

---

## 📊 API 엔드포인트

### Health Check
```
GET {APPS_SCRIPT_URL}?action=health
```
- 용도: API 정상 작동 확인
- 응답: `{"success": true, "message": "Apps Script API 정상 작동"}`

### Key Player 업데이트 (기본)
```
GET {APPS_SCRIPT_URL}
또는
GET {APPS_SCRIPT_URL}?action=updateKeyPlayers
```
- 용도: updateAndCheckBoxes() 실행
- 응답: `{"success": true, "message": "키 플레이어 업데이트 완료"}`

---

## 🔄 배포 업데이트

코드 수정 후 재배포 방법:

1. **Apps Script 편집기에서 코드 수정**
2. **저장** (Ctrl+S)
3. **배포 → 배포 관리**
4. **편집 아이콘 (연필)** 클릭
5. **버전: 새 버전** 선택
6. **배포 업데이트** 클릭

⚠️ URL은 변경되지 않으므로 `.env` 수정 불필요

---

## ✅ 자동화 검증 체크리스트

- [ ] Apps Script 프로젝트에 `keyplayer.gs`, `keyplayer_api.gs` 존재
- [ ] Web App 배포 완료 (액세스: 모든 사용자)
- [ ] 배포 URL 복사
- [ ] `.env`에 `APPS_SCRIPT_URL` 추가
- [ ] 브라우저 Health Check 성공 (JSON 응답)
- [ ] Python 트리거 테스트 성공
- [ ] 전체 워크플로우 테스트 성공
- [ ] TARGET Type 시트 K열, L열 자동 업데이트 확인

---

## 🎯 자동화 완료 후 워크플로우

```
┌─────────────────────────────────────────────────┐
│  Python 자동화 (매시간 실행)                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  [1] WSOP CSV 다운로드 (Selenium)               │
│       ↓                                          │
│  [2] TARGET Type 시트 업로드 (gspread)          │
│       ↓                                          │
│  [3] Apps Script HTTP 트리거 (requests) ← 자동! │
│       ↓                                          │
│  [4] Apps Script 실행                            │
│       - SOURCE Confirmed E열 읽기                │
│       - TARGET Type H열과 부분 일치 매칭         │
│       - K열 Key Player 마킹                      │
│       - L열 이름 축약                            │
│       ↓                                          │
│  [5] 완료!                                       │
│                                                  │
└─────────────────────────────────────────────────┘

총 소요 시간: ~15초 (로그인 재사용 시)
사용자 개입: 0회 (완전 자동)
```

---

## 📞 지원

**문제 발생 시**:
1. Apps Script 실행 로그 확인: 보기 → 로그
2. Python 로그 확인: `logs/automation_YYYYMMDD.log`
3. 이슈 리포트: GitHub Issues

---

**완료!** 이제 Python 실행만으로 전체 워크플로우가 자동으로 실행됩니다. 🎉
