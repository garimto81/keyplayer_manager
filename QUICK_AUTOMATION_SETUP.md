# ⚡ 5분 자동화 설정

**현재 상태**: CSV 업로드까지 자동 ✅ → Apps Script 수동 실행 ❌
**목표**: 전체 자동화 ✅✅✅

---

## 🎯 해야 할 일 (5분)

### 1️⃣ Apps Script 편집기 열기 (1분)

1. 이 링크 클릭: https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4
2. **확장 프로그램 → Apps Script**

---

### 2️⃣ Web App 배포 (2분)

1. **배포 → 새 배포**
2. ⚙️ 톱니바퀴 → **웹 앱**
3. 설정:
   - 실행 계정: **나**
   - 액세스: **모든 사용자**
4. **배포** 클릭
5. 권한 승인 (처음만)
6. **URL 복사** ← 중요!

---

### 3️⃣ .env 파일 수정 (1분)

`d:\AI\claude01\keyplayer_manager\.env` 파일 열기

마지막 줄에 추가:
```bash
APPS_SCRIPT_URL=복사한_URL_여기_붙여넣기
```

예시:
```bash
APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbyXXX.../exec
```

저장 (Ctrl+S)

---

### 4️⃣ 테스트 (1분)

```bash
cd d:/AI/claude01/keyplayer_manager
python tests/test_trigger_apps_script.py
```

**성공 시**: `✅ Apps Script 실행 완료!`
**실패 시**: URL 다시 확인

---

## 🎉 완료!

이제 전체 자동화:
```bash
python src/main.py
```

**결과**:
```
[단계 1/3] CSV 다운로드 ✅
[단계 2/3] Sheets 업로드 ✅
[단계 3/3] Apps Script 실행 ✅ ← 자동!
🎉 자동화 완료!
```

---

## 📖 상세 가이드

더 자세한 내용: [docs/guides/APPS_SCRIPT_AUTOMATION.md](docs/guides/APPS_SCRIPT_AUTOMATION.md)
