# Google Apps Script 파일

이 폴더에는 Google Apps Script로 실행할 코드가 포함되어 있습니다.

## 📁 파일

### keyplayer.gs (메인 파일)

**용도**:
- SOURCE (Confirmed) 시트에서 Key Player 마스터 리스트 읽기
- TARGET (Type) 시트에서 Key Player 마킹 (K열) + 이름 축약 (L열)
- Time Trigger를 통한 자동 실행

**주요 함수**:

| 함수 | 용도 | 실행 방법 |
|------|------|----------|
| **updateAndCheckBoxes** | Key Player 업데이트 (메인 로직) | 수동 실행 또는 Trigger 호출 |
| **setupTimeTrigger** | Time Trigger 설정 (코드용) | Python/API에서 호출 |
| **setupTimeTriggerWithUI** | Time Trigger 설정 (UI 포함) | Apps Script 에디터에서 수동 실행 |
| **autoRunIfUpdated** | 자동 실행 (변경 감지) | Trigger가 자동 호출 |
| **checkTriggerStatus** | Trigger 상태 반환 (코드용) | Python/API에서 호출 |
| **checkTriggerStatusWithUI** | Trigger 상태 확인 (UI 포함) | Apps Script 에디터에서 수동 실행 |
| **deleteTimeTrigger** | Trigger 중단 (코드용) | Python/API에서 호출 |
| **deleteTimeTriggerWithUI** | Trigger 중단 (UI 포함) | Apps Script 에디터에서 수동 실행 |

---

## 🚀 사용 방법

### 1단계: Apps Script 프로젝트에 추가

1. **TARGET 시트 열기**:
   ```
   https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4
   ```

2. **Apps Script 편집기 열기**:
   - 메뉴: 확장 프로그램 → Apps Script

3. **파일 추가**:
   - 좌측 **+** → 스크립트
   - 파일 이름: `keyplayer.gs`
   - 내용: 이 폴더의 `keyplayer.gs` 파일 전체 복사/붙여넣기
   - **Ctrl+S** 저장

---

### 2단계: Time Trigger 설정 (자동 실행)

1. 함수 선택: **`setupTimeTriggerWithUI`**
2. ▶ 실행 버튼 클릭
3. 권한 승인 (처음만):
   - "권한 검토" → Google 계정 선택
   - "고급" → "프로젝트 이름(으)로 이동" → "허용"
4. 완료 확인: "✅ 자동 실행 설정 완료!" 팝업

---

## 📊 전체 워크플로우

```
Python이 Type 시트에 CSV 업로드
    ↓
1분 이내
    ↓
Apps Script Time Trigger 감지 (autoRunIfUpdated)
    ↓
updateAndCheckBoxes() 자동 실행
    ↓
1. SOURCE Confirmed E열 읽기 (Key Player 마스터)
2. TARGET Type H열과 부분 일치 매칭
3. K열: Key Player 마킹 (TRUE)
4. L열: 이름 축약 생성
    ↓
완료!
```

---

## 🔍 변경 감지 로직

`autoRunIfUpdated()` 함수가 다음을 감지:

1. **행 수 변경**: 이전 67행 → 현재 80행 ✅
2. **A1 셀 값 변경**: Python의 `sheet.clear()` 후 재작성 ✅
3. **변경 없음**: 대기 (불필요한 실행 방지)

---

## ⚙️ 설정 값

파일 내부에 하드코딩된 Spreadsheet ID:

```javascript
const SOURCE_SPREADSHEET_ID = "1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg";
const TARGET_SPREADSHEET_ID = "19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4";
```

**변경 방법**: `keyplayer.gs` 파일 상단의 ID 수정

---

## 📖 상세 가이드

- [Time Trigger 설정 가이드](../TIME_TRIGGER_SETUP.md)
- [완전 자동화 설명](../AUTOMATION_COMPLETE.md)
- [Sheets 아키텍처](../docs/SHEETS_ARCHITECTURE.md)

---

## 🐛 문제 해결

### 오류: "Spreadsheet를 찾을 수 없습니다"
**원인**: Spreadsheet ID 불일치
**해결**: `keyplayer.gs` 파일 상단의 ID 확인

### 오류: "시트를 찾을 수 없습니다"
**원인**: 시트 이름 불일치
**해결**:
- SOURCE: `Confirmed` (정확히 일치)
- TARGET: `Type` (대문자 T)

### Trigger 작동 안 함
**확인**: `checkTriggerStatusWithUI` 실행
**해결**: `deleteTimeTriggerWithUI` → `setupTimeTriggerWithUI` 재실행

---

## 📝 버전 히스토리

- **v1.1.0** (2025-10-17):
  - **UI 함수 분리**: `setupTimeTriggerWithUI`, `checkTriggerStatusWithUI`, `deleteTimeTriggerWithUI` 추가
  - `SpreadsheetApp.getUi()` 오류 수정 (트리거 컨텍스트에서 사용 불가 문제 해결)
  - 코드용 함수와 UI용 함수 분리로 Python/API 호출 지원

- **v1.0.0** (2025-10-17):
  - Time Trigger 자동 실행 추가
  - 변경 감지 로직 구현
  - 부분 일치 매칭 적용
  - SOURCE/TARGET 2-Sheet 아키텍처
