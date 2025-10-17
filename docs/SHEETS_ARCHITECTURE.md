# Google Sheets 아키텍처 설계

**버전**: 1.0.0
**업데이트**: 2025-10-17

---

## 📊 2-Sheet 시스템 개요

시스템은 **역할이 분리된 2개의 스프레드시트**를 사용합니다:

| 시트 | 역할 | 관리 방식 | 업데이트 주기 |
|------|------|----------|--------------|
| **SOURCE (Confirmed)** | Key Player 마스터 리스트 | 수동 | 필요 시 |
| **TARGET (Type)** | 실시간 플레이어 데이터 + 마킹 | 자동 | 매시간 |

---

## 1️⃣ SOURCE Spreadsheet: Key Player 마스터 리스트

### 기본 정보
- **ID**: `1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg`
- **시트 이름**: `Confirmed`
- **URL**: https://docs.google.com/spreadsheets/d/1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg

### 역할
- **Key Player 명단의 유일한 진실 공급원 (Single Source of Truth)**
- 수동으로 관리되는 마스터 리스트
- Apps Script가 이 리스트를 기준으로 TARGET 시트에서 Key Player를 탐지

### 구조

| 열 | 컬럼명 | 설명 | 예시 |
|----|--------|------|------|
| A | PokerRoom | 포커룸 | Main |
| B | 체크박스 | (사용 안 함) | - |
| C | TableName | 테이블 이름 | Black |
| D | TableId | 테이블 ID | 43822 |
| **E** | **PlayerName** | **Key Player 이름 (매칭 기준)** ⭐ | Beach |
| F | Nationality | 국적 | US |
| G | ChipCount | 칩 수 | 50000 |

### 중요 사항
1. **E열만 사용**: Apps Script는 오직 E열의 이름만 읽음
2. **부분 일치 매칭**: E열에 "Beach"만 있어도 "Lawrence Andrew Beach"가 매칭됨
3. **대소문자 무시**: 매칭 시 대소문자 구분 없음
4. **수동 업데이트**: Python 자동화는 이 시트를 **절대 수정하지 않음**

### 사용 예시

**E열에 저장된 이름**:
```
Beach
Ahmad
Cohen
```

**매칭되는 이름 (TARGET Type 시트)**:
```
Lawrence Andrew Beach  ← "Beach" 포함 → ✅ 매칭
Ahmad Abdelhadi        ← "Ahmad" 포함 → ✅ 매칭
Lucien Cohen           ← "Cohen" 포함 → ✅ 매칭
John Doe               ← 해당 없음   → ❌ 미매칭
```

---

## 2️⃣ TARGET Spreadsheet: 실시간 데이터 + Key Player 마킹

### 기본 정보
- **ID**: `19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4`
- **시트 이름**: `Type` (대문자 T 주의!)
- **URL**: https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4

### 역할
1. **WSOP CSV 데이터 저장**: Python이 매시간 최신 플레이어 목록 업로드
2. **Key Player 자동 마킹**: Apps Script가 SOURCE와 비교하여 K열에 `TRUE` 표시
3. **이름 축약**: L열에 화면 표시용 짧은 이름 생성

### 구조

| 열 | 컬럼명 | 설명 | 생성 방법 | 예시 |
|----|--------|------|----------|------|
| A-G | 기본 데이터 | WSOP CSV 원본 | Python | PokerRoom, TableName, ... |
| **H** | **PlayerName** | **전체 이름 (매칭 대상)** | Python | Lawrence Andrew Beach |
| I-J | 기타 | WSOP CSV 원본 | Python | - |
| **K** | **Key Player** | **Key Player 여부** | Apps Script | TRUE / 공백 |
| **L** | **짧은 이름** | **화면 표시용 축약 이름** | Apps Script | L. Beach |

### 업데이트 프로세스

#### 단계 0: 시트 초기화 (Python)
```python
sheet.clear()  # 기존 데이터 전체 삭제 (헤더 포함)
```

#### 단계 1: CSV 업로드 (Python)
```python
# WSOP에서 다운로드한 Seats.csv를 Type 시트에 업로드
sheet.update('A1', csv_data)
```

**업로드되는 컬럼** (WSOP CSV 원본):
- A: PokerRoom
- B: TableName
- C: TableId
- D: TableNo
- E: SeatId
- F: SeatNo
- G: PlayerId
- **H: PlayerName** ← 매칭 기준
- I: Nationality
- J: ChipCount

#### 단계 2: Key Player 마킹 (Apps Script)
```javascript
// SOURCE Confirmed E열에서 Key Player 리스트 로드
const keyPlayersArray = ["Beach", "Ahmad", "Cohen"];

// TARGET Type H열과 부분 일치 비교
const isKeyPlayer = keyPlayersArray.some(keyName =>
  fullName.toLowerCase().includes(keyName.toLowerCase())
);

if (isKeyPlayer) {
  kValue = 'TRUE';  // K열에 TRUE 표시
}
```

**K열 결과**:
```
| H (PlayerName)         | K (Key Player) |
|------------------------|----------------|
| Lawrence Andrew Beach  | TRUE           |
| Ahmad Abdelhadi        | TRUE           |
| John Doe               |                |
```

#### 단계 3: 이름 축약 (Apps Script)
```javascript
// 10자 이하: 그대로
if (fullName.length <= 10) {
  lValue = fullName;  // "John Doe"
}
// 10자 초과: 이니셜 + 성
else {
  const firstName = parts[0];
  const lastName = parts[parts.length - 1];
  lValue = `${firstName.charAt(0)}. ${lastName}`;  // "L. Beach"
}
```

**L열 결과**:
```
| H (PlayerName)         | L (짧은 이름) |
|------------------------|---------------|
| Lawrence Andrew Beach  | L. Beach      |
| Ahmad Abdelhadi        | A. Abdelhadi  |
| John Doe               | John Doe      |
```

---

## 🔄 전체 데이터 흐름

```
┌──────────────────────────────────────────────────────┐
│  WSOP 사이트                                          │
│  https://staff.wsopplus.com                          │
│  "Export Player List To CSV" 버튼                    │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ ① Python (Selenium)
                   │    downloads/Seats.csv
                   ▼
┌──────────────────────────────────────────────────────┐
│  TARGET Spreadsheet (Type 시트)                      │
│  ID: 19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4   │
│                                                       │
│  ② Python 업로드:                                    │
│  ┌────┬─────────┬────────────────────┬──────┬────┐  │
│  │ A  │   B     │         H          │  I   │ J  │  │
│  ├────┼─────────┼────────────────────┼──────┼────┤  │
│  │Room│  Table  │ Lawrence A. Beach  │  US  │ 50k│  │
│  │Room│  Table  │ Ahmad Abdelhadi    │  CA  │ 50k│  │
│  │Room│  Table  │ John Doe           │  UK  │ 50k│  │
│  └────┴─────────┴────────────────────┴──────┴────┘  │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ ③ Apps Script 트리거
                   ▼
┌──────────────────────────────────────────────────────┐
│  SOURCE Spreadsheet (Confirmed 시트)                 │
│  ID: 1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg   │
│                                                       │
│  Key Player 마스터 리스트 (E열):                      │
│  ┌───────────────┐                                   │
│  │  E (Name)     │                                   │
│  ├───────────────┤                                   │
│  │  Beach        │  ← 부분 일치 매칭                 │
│  │  Ahmad        │                                   │
│  │  Cohen        │                                   │
│  └───────────────┘                                   │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ ④ Apps Script 매칭
                   │    부분 일치 (contains)
                   ▼
┌──────────────────────────────────────────────────────┐
│  TARGET Spreadsheet (Type 시트)                      │
│                                                       │
│  K열, L열 업데이트:                                   │
│  ┌────────────────────┬──────────┬──────────────┐   │
│  │  H (PlayerName)    │ K (Key)  │ L (짧은이름)  │   │
│  ├────────────────────┼──────────┼──────────────┤   │
│  │ Lawrence A. Beach  │  TRUE ⭐ │  L. Beach    │   │
│  │ Ahmad Abdelhadi    │  TRUE ⭐ │  A. Abdelhadi│   │
│  │ John Doe           │          │  John Doe    │   │
│  └────────────────────┴──────────┴──────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## 🔍 매칭 로직 상세

### Python → TARGET 업로드
```python
# src/sheets_uploader.py
def upload_csv_to_type_sheet(csv_file):
    spreadsheet = client.open_by_key(TARGET_SPREADSHEET_ID)
    sheet = spreadsheet.worksheet("Type")

    sheet.clear()  # 기존 데이터 삭제
    sheet.update('A1', csv_data)  # CSV 전체 업로드
```

### Apps Script → 부분 일치 매칭
```javascript
// gs/keyplayer.gs
function updateAndCheckBoxes() {
  // 1. SOURCE에서 Key Player 마스터 리스트 로드
  const sourceSpreadsheet = SpreadsheetApp.openById(SOURCE_SPREADSHEET_ID);
  const confirmedSheet = sourceSpreadsheet.getSheetByName('Confirmed');
  const keyPlayersArray = confirmedSheet.getRange("E2:E").getValues()
    .map(row => row[0].trim())
    .filter(name => name);

  // 2. TARGET에서 플레이어 데이터 로드
  const targetSpreadsheet = SpreadsheetApp.openById(TARGET_SPREADSHEET_ID);
  const typeSheet = targetSpreadsheet.getSheetByName('Type');
  const typeValues = typeSheet.getDataRange().getValues();

  // 3. 부분 일치 매칭
  const newValues = typeValues.map((row, index) => {
    if (index === 0) return [row[10], row[11]];  // 헤더

    const fullName = row[7];  // H열
    let kValue = '', lValue = '';

    // 부분 일치 (contains, case-insensitive)
    const isKeyPlayer = keyPlayersArray.some(keyName =>
      fullName.toLowerCase().includes(keyName.toLowerCase())
    );

    if (isKeyPlayer) {
      kValue = 'TRUE';
    }

    // 이름 축약 로직
    lValue = abbreviateName(fullName);

    return [kValue, lValue];
  });

  // 4. K열, L열 업데이트
  typeSheet.getRange(1, 11, newValues.length, 2).setValues(newValues);
}
```

---

## 🎯 설계 원칙

### 1. 역할 분리 (Separation of Concerns)
- **SOURCE**: 마스터 데이터 (수동 관리)
- **TARGET**: 트랜잭션 데이터 (자동 업데이트)

### 2. Single Source of Truth
- Key Player 명단은 오직 SOURCE Confirmed E열에만 존재
- TARGET은 SOURCE를 참조만 하고 수정하지 않음

### 3. 부분 일치 매칭
- **장점**: 유연한 매칭 (이름 변형 대응 가능)
- **예시**: "Beach" 하나로 "Lawrence Beach", "Andrew Beach" 모두 매칭

### 4. 멱등성 (Idempotency)
- Python 업로드: `clear()` 후 전체 재작성
- Apps Script: K열, L열 전체 재계산
- 여러 번 실행해도 동일한 결과

---

## ⚠️ 주의사항

### 1. 시트 이름 대소문자
- **TARGET 시트**: `Type` (대문자 T)
- **SOURCE 시트**: `Confirmed` (대문자 C)
- 코드에서 정확히 일치시켜야 함

### 2. 컬럼 위치 고정
- **H열**: PlayerName (매칭 기준)
- **K열**: Key Player 마킹
- **L열**: 짧은 이름
- Apps Script는 컬럼 번호로 접근하므로 변경 시 주의

### 3. 부분 일치의 함정
- "Lee" 검색 시 "Freeman Lee"도 매칭됨
- 고유한 키워드 사용 권장 (예: 성 전체)

### 4. 성능
- 현재: O(n*m) (n=TARGET 행 수, m=SOURCE Key Player 수)
- 최적화 가능: Set 기반 전처리

---

## 📝 유지보수 가이드

### Key Player 추가
1. SOURCE Confirmed 시트 열기
2. E열에 새 이름 추가 (부분 이름도 가능)
3. 저장 (자동으로 다음 실행 시 반영)

### 시트 초기화
```bash
# TARGET Type 시트만 초기화 (SOURCE는 유지)
python tests/test_corrected_upload.py
```

### 매칭 테스트
```javascript
// Apps Script 편집기에서 직접 실행
function testMatching() {
  updateAndCheckBoxes();
  Logger.log("실행 로그 확인: 보기 > 로그");
}
```

---

## 🔗 참조

- **Python 코드**: [src/sheets_uploader.py](../src/sheets_uploader.py)
- **Apps Script**: [gs/keyplayer.gs](../gs/keyplayer.gs)
- **테스트**: [tests/test_corrected_upload.py](../tests/test_corrected_upload.py)
- **전체 워크플로우**: [README.md](../README.md)

---

**버전 히스토리**:
- v1.0.0 (2025-10-17): 초기 문서 작성 - 2-Sheet 아키텍처 확정
