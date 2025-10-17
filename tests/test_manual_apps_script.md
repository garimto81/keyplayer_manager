# Apps Script 수동 실행 가이드

TARGET Type 시트에 CSV 업로드는 완료되었지만, Key Player 마킹(K열)과 이름 축약(L열)은 Apps Script를 실행해야 합니다.

## 🚀 즉시 실행 방법

### 1단계: Google Apps Script 편집기 열기

1. **TARGET 시트 열기**:
   ```
   https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4
   ```

2. **Apps Script 편집기 열기**:
   - 메뉴: **확장 프로그램 → Apps Script**

---

### 2단계: 스크립트 파일 확인/추가

Apps Script 프로젝트에 다음 파일이 있는지 확인:
- `keyplayer.gs` ← 메인 로직

**없다면**:
1. 좌측 **+** 버튼 → **스크립트** 클릭
2. 파일 이름: `keyplayer.gs`
3. 내용: `d:\AI\claude01\keyplayer_manager\gs\keyplayer.gs` 파일 전체 복사/붙여넣기
4. **Ctrl+S** 저장

---

### 3단계: 함수 실행

1. **함수 선택**:
   - 편집기 상단 드롭다운에서 `updateAndCheckBoxes` 선택

2. **실행 버튼 클릭**:
   - 재생 버튼(▶) 클릭

3. **권한 승인** (처음 실행 시):
   - "권한 검토" → Google 계정 선택
   - "고급" → "프로젝트 이름(으)로 이동" → "허용"

---

### 4단계: 실행 로그 확인

1. **로그 보기**:
   - 메뉴: **보기 → 로그** 또는 **Ctrl+Enter**

2. **예상 로그**:
   ```
   🚀 스크립트 실행 시작
   ➡️ [단계 1/3] SOURCE 스프레드시트 열기...
   ➡️ [단계 2/3] Key Player 마스터 리스트 생성 중...
   ✅ Key Player 마스터 리스트: 총 X명 로드 완료
   ➡️ [단계 3/3] TARGET 스프레드시트에서 데이터 읽기...
   ✅ 'Type' 시트에서 총 XX 행의 데이터를 읽었습니다.
   ➡️ 'Type' 시트 H열(PlayerName)과 Key Player 마스터 리스트 매칭 중...
   ✅ 'Type' 시트 K열(Key Player), L열(짧은이름) 업데이트 완료!
      → 총 X명의 Key Player 마킹 완료
   🎉 모든 작업이 성공적으로 완료되었습니다.
   ```

---

### 5단계: 결과 확인

**TARGET Type 시트**로 돌아가서 확인:
- **K열**: Key Player는 `TRUE` 표시
- **L열**: 모든 플레이어에 짧은 이름 생성

---

## ⚠️ 문제 해결

### 오류 1: "SOURCE 시트에서 'Confirmed' 탭을 찾을 수 없습니다"
**원인**: SOURCE 스프레드시트에 Confirmed 시트가 없음
**해결**:
1. SOURCE 시트 열기: https://docs.google.com/spreadsheets/d/1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg
2. 시트 이름이 정확히 `Confirmed`인지 확인 (대소문자 일치)
3. 없다면 시트 생성 후 E열에 Key Player 이름 입력

---

### 오류 2: "TARGET 시트에서 'Type' 탭을 찾을 수 없습니다"
**원인**: TARGET 스프레드시트에 Type 시트가 없거나 이름 불일치
**해결**:
1. 시트 이름이 정확히 `Type` (대문자 T)인지 확인
2. 다른 이름이면 `keyplayer.gs` 파일에서 시트 이름 수정

---

### 오류 3: "권한 오류"
**원인**: Apps Script가 스프레드시트 접근 권한 없음
**해결**:
1. 실행 시 나타나는 권한 요청 승인
2. Google 계정이 두 스프레드시트 모두에 접근 가능한지 확인

---

### 오류 4: "Key Player 마킹이 0명"
**원인**: SOURCE Confirmed E열에 Key Player 이름이 없거나 매칭 실패
**해결**:
1. SOURCE Confirmed 시트 E열 확인
2. E열에 Key Player 이름 입력 (예: "Beach", "Ahmad")
3. 다시 `updateAndCheckBoxes` 실행

---

## 🎯 매칭 테스트

### SOURCE Confirmed E열에 입력:
```
Beach
Ahmad
Cohen
```

### TARGET Type H열 (PlayerName):
```
Lawrence Andrew Beach  ← "Beach" 포함 → ✅ K열 TRUE
Ahmad Abdelhadi        ← "Ahmad" 포함 → ✅ K열 TRUE
Lucien Cohen           ← "Cohen" 포함 → ✅ K열 TRUE
John Doe               ← 해당 없음   → ❌ K열 공백
```

---

## 📝 다음 단계

수동 실행이 성공하면:
1. [Apps Script Web App 배포](../docs/guides/APPS_SCRIPT_DEPLOY.md)
2. `.env`에 `APPS_SCRIPT_URL` 추가
3. Python에서 자동 트리거 가능
