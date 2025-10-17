# ⚡ Apps Script Time Trigger 자동화 설정

**방식**: Apps Script가 1분마다 Type 시트 변경 감지 → 자동 실행
**장점**: Web App 배포 불필요, URL 관리 불필요, 가장 간단

---

## 🎯 작동 방식

```
Python이 Type 시트에 CSV 업로드
    ↓
1분 이내
    ↓
Apps Script Time Trigger 감지
    ↓
자동으로 updateAndCheckBoxes() 실행
    ↓
K열 Key Player 마킹 + L열 이름 축약 완료
```

---

## 📋 1회 설정 (2분)

### 1단계: Apps Script 편집기 열기

1. **TARGET 시트 열기**:
   ```
   https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4
   ```

2. **확장 프로그램 → Apps Script**

3. **keyplayer.gs 파일 확인**:
   - 파일이 있어야 함
   - 없다면 `d:\AI\claude01\keyplayer_manager\gs\keyplayer.gs` 내용 복사

---

### 2단계: Time Trigger 설정 (1회만!)

1. **함수 선택**:
   - 편집기 상단 드롭다운에서 **`setupTimeTrigger`** 선택

2. **실행 버튼 클릭**:
   - 재생 버튼(▶) 클릭

3. **권한 승인** (처음만):
   - "권한 검토" → Google 계정 선택
   - "고급" → "프로젝트 이름(으)로 이동"
   - "허용" 클릭

4. **완료 확인**:
   - 팝업 메시지: "✅ 자동 실행 설정 완료!"
   - 로그 확인: **보기 → 로그** (Ctrl+Enter)

---

## ✅ 설정 완료!

이제 **완전 자동**으로 작동합니다:

```
1. Python 실행 (매시간 또는 수동)
   python src/main.py

2. CSV 다운로드 + Type 시트 업로드 완료

3. 1분 이내 Apps Script 자동 실행
   - Type 시트 변경 감지
   - Key Player 마킹 자동 실행

4. 완료! (사용자 개입 0회)
```

---

## 🔍 상태 확인 방법

### 방법 1: Trigger 상태 확인

1. Apps Script 편집기에서 `checkTriggerStatus` 선택
2. ▶ 실행
3. 팝업 메시지 확인:
   - ✅ 자동 실행 활성화됨
   - 마지막 처리 시간

### 방법 2: 실행 로그 확인

1. Apps Script 편집기 → **보기 → 실행 로그**
2. 최근 실행 내역 확인:
   ```
   ℹ️ Type 시트 변경 없음. 대기 중...
   또는
   🔄 Type 시트 변경 감지!
   🚀 updateAndCheckBoxes() 자동 실행 시작...
   ✅ 자동 실행 완료!
   ```

---

## 🛠️ 관리 기능

### Trigger 중단하기

자동 실행을 중단하려면:
1. `deleteTimeTrigger` 선택
2. ▶ 실행
3. 확인: "✅ 자동 실행 중단 완료!"

### Trigger 재활성화

다시 활성화하려면:
1. `setupTimeTrigger` 선택
2. ▶ 실행

---

## 📊 변경 감지 로직

Apps Script가 다음을 감지하면 자동 실행:

1. **행 수 변경**:
   - 이전: 50행 → 현재: 67행 ✅ 실행

2. **A1 셀 값 변경**:
   - Python이 `sheet.clear()` 후 새 데이터 업로드 ✅ 실행

3. **변경 없음**:
   - 로그: "ℹ️ Type 시트 변경 없음. 대기 중..."
   - 실행 안 함 (불필요한 실행 방지)

---

## ⚠️ 주의사항

### 1. 최대 1분 지연
- Python 완료 후 최대 1분 후 Apps Script 실행
- 즉시 실행이 필요하면 수동 실행:
  - `updateAndCheckBoxes` 선택 → ▶ 실행

### 2. Apps Script 6분 실행 시간 제한
- 일반적으로 수백 행 처리 가능
- 수천 행 이상이면 최적화 필요

### 3. 하루 실행 횟수 제한
- 무료 계정: 90분/일 Apps Script 실행 시간
- 1분마다 체크 → 하루 1440회 체크 (각 체크는 1초 미만)
- 실제 업데이트는 하루 24회 (매시간) → 문제 없음

---

## 🧪 테스트 방법

### 전체 워크플로우 테스트

1. **Python 실행**:
   ```bash
   cd d:/AI/claude01/keyplayer_manager
   python src/main.py
   ```

2. **로그 확인** (Python):
   ```
   [단계 1/3] CSV 다운로드 ✅
   [단계 2/3] Type 시트 업로드 ✅
   [단계 3/3] Apps Script 실행
   ⚠️ Apps Script 자동 트리거 실패 (수동 실행 필요)  ← 정상!
      → Google Apps Script에서 updateAndCheckBoxes() 실행
   ```
   ⚠️ 이 메시지는 정상입니다. Time Trigger 방식에서는 Python이 직접 호출하지 않습니다.

3. **1분 대기**

4. **Apps Script 로그 확인**:
   - Apps Script 편집기 → 보기 → 실행 로그
   - 최근 로그에서 "🔄 Type 시트 변경 감지!" 확인

5. **결과 확인**:
   - TARGET Type 시트 열기
   - K열: Key Player `TRUE` 표시
   - L열: 짧은 이름 생성

---

## 📈 성능

| 항목 | 값 |
|------|-----|
| 체크 주기 | 1분 |
| 평균 지연 시간 | 30초 |
| 최대 지연 시간 | 1분 |
| 실행 시간 (Apps Script) | 2~5초 |
| 하루 최대 자동 실행 | 무제한 (변경 감지 시) |

---

## 🎉 완료!

이제 완전 자동화가 설정되었습니다:

```
매시간 (또는 수동):
  Python 실행 → CSV 업로드 → 1분 이내 → Apps Script 자동 실행 → 완료

사용자 개입: 0회
설정 필요: 1회 (setupTimeTrigger)
```

---

## 🔗 관련 문서

- **Apps Script 코드**: [gs/keyplayer.gs](gs/keyplayer.gs)
- **Python 메인**: [src/main.py](src/main.py)
- **아키텍처**: [docs/SHEETS_ARCHITECTURE.md](docs/SHEETS_ARCHITECTURE.md)

---

## 📞 지원

**Trigger 작동 안 함?**
1. `checkTriggerStatus` 실행 → Trigger 활성화 확인
2. Apps Script 실행 로그 확인
3. 필요시 `deleteTimeTrigger` → `setupTimeTrigger` 재설정
