# Apps Script Web App 배포 가이드

**목적**: Python에서 HTTP 요청으로 Apps Script를 자동 트리거
**소요 시간**: 5분

---

## 📋 사전 준비

1. Google Apps Script 접근 권한
2. `gs/keyplayer_api.gs` 파일 내용
3. TARGET Spreadsheet 접근 권한 (ID: `19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4`)

---

## 🚀 배포 단계

### 1단계: Apps Script 프로젝트 생성

1. **Google Sheets 열기**
   ```
   https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4
   ```

2. **Apps Script 편집기 열기**
   - 메뉴: **확장 프로그램 → Apps Script**

3. **새 스크립트 파일 생성**
   - 파일 이름: `keyplayer_api.gs`
   - 내용: `gs/keyplayer_api.gs` 파일 전체 복사/붙여넣기

4. **저장**
   - Ctrl+S 또는 디스크 아이콘 클릭

---

### 2단계: Web App 배포

1. **배포 메뉴 열기**
   - 우측 상단 **배포 → 새 배포** 클릭

2. **웹 앱 선택**
   - 유형 선택: **웹 앱** (톱니바퀴 아이콘 클릭)

3. **배포 설정**
   ```
   설명: WSOP Key Player API v1
   실행 사용자: 나 (본인 이메일)
   액세스 권한: 모든 사용자
   ```

4. **배포 클릭**
   - 권한 승인 필요 시:
     1. **권한 검토** 클릭
     2. Google 계정 선택
     3. **고급** → **{프로젝트 이름}(으)로 이동** 클릭
     4. **허용** 클릭

5. **배포 URL 복사**
   ```
   형식: https://script.google.com/macros/s/AKfycby.../exec
   ```
   ⚠️ 이 URL을 **메모장에 임시 저장**

---

### 3단계: .env 파일 설정

1. **프로젝트 루트의 .env 파일 열기**
   ```
   d:\AI\claude01\keyplayer_manager\.env
   ```

2. **APPS_SCRIPT_URL 추가**
   ```bash
   # Apps Script Web App URL
   APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycby.../exec
   ```

3. **저장**

---

## ✅ 배포 테스트

### 테스트 1: 브라우저에서 Health Check

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

### 테스트 2: Python에서 트리거

```bash
cd d:/AI/claude01/keyplayer_manager
python -c "
from src.sheets_uploader import SheetsUploader
uploader = SheetsUploader()
uploader.trigger_apps_script()
"
```

**예상 출력**:
```
🚀 Apps Script 트리거 호출 중...
✅ Apps Script 실행 완료
```

---

### 테스트 3: 전체 워크플로우

```bash
python src/main.py
```

**예상 로그**:
```
[단계 1/3] WSOP 사이트에서 CSV 다운로드
✅ CSV 다운로드 완료
[단계 2/3] Google Sheets에 데이터 업로드
✅ Sheets 업로드 완료
[단계 3/3] Apps Script 실행
✅ Apps Script 실행 완료
🎉 자동화 완료!
```

---

## 🔧 트러블슈팅

### 오류 1: "권한이 필요합니다"
**원인**: Google 계정 권한 승인 필요
**해결**:
1. Apps Script 편집기에서 `doGet` 함수 선택
2. **실행** 버튼 클릭
3. 권한 검토 → 허용

---

### 오류 2: "404 Not Found"
**원인**: 배포 URL이 잘못됨
**해결**:
1. Apps Script 편집기 → **배포 → 배포 관리**
2. 최신 배포 URL 복사
3. `.env` 파일의 `APPS_SCRIPT_URL` 업데이트

---

### 오류 3: "액세스 거부됨"
**원인**: 실행 권한 설정 오류
**해결**:
1. **배포 → 배포 관리 → 편집 (연필 아이콘)**
2. **액세스 권한**: "모든 사용자"로 변경
3. **배포 업데이트**

---

### 오류 4: "ReferenceError: updateAndCheckBoxes is not defined"
**원인**: `keyplayer.gs` 파일이 프로젝트에 없음
**해결**:
1. Apps Script 프로젝트에 `keyplayer.gs` 파일 추가
2. `gs/keyplayer.gs` 내용 복사/붙여넣기
3. 저장 후 재배포

---

## 📊 Apps Script API 사용법

### 사용 가능한 Action

#### 1. updateKeyPlayers (기본)
```
GET {APPS_SCRIPT_URL}?action=updateKeyPlayers
또는
GET {APPS_SCRIPT_URL}
```
- Confirmed 시트에서 Key Player 탐지
- Type 시트에서 체크박스 업데이트

#### 2. health (상태 확인)
```
GET {APPS_SCRIPT_URL}?action=health
```
- API 정상 작동 여부 확인

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

## 📝 배포 체크리스트

- [ ] Apps Script 프로젝트 생성
- [ ] `keyplayer_api.gs` 코드 복사
- [ ] `keyplayer.gs` 코드 추가 (필수)
- [ ] Web App 배포 (액세스: 모든 사용자)
- [ ] 배포 URL 복사
- [ ] `.env`에 `APPS_SCRIPT_URL` 추가
- [ ] Health Check 테스트 (브라우저)
- [ ] Python 트리거 테스트
- [ ] 전체 워크플로우 테스트

---

## 🎯 다음 단계

배포 완료 후:
1. ✅ [전체 워크플로우 테스트](TESTING_COMPLETE.md)
2. ✅ [자동 스케줄러 설정](../../README.md#자동-스케줄링)
3. ✅ 프로덕션 모니터링

---

**참조**:
- [Google Apps Script 공식 문서](https://developers.google.com/apps-script)
- [Web Apps 가이드](https://developers.google.com/apps-script/guides/web)