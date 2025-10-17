# 🔐 세션 관리 가이드

WSOP 자동화 시스템의 세션 유지 기능 설명

---

## 🎯 목적

**매번 로그인하면 계정이 의심받거나 차단될 수 있습니다.**

세션 관리를 통해:
- ✅ 첫 로그인 후 쿠키 저장
- ✅ 다음 실행 시 쿠키 재사용
- ✅ 로그인 횟수 최소화 (24시간마다 1회)
- ✅ 자동 감지 및 재로그인

---

## 🚀 사용법

### 자동 사용 (기본 동작)

아무 설정 없이 `main.py`를 실행하면 자동으로 세션 관리가 적용됩니다:

```bash
# 첫 실행: 로그인 + 세션 저장
python src/main.py

# 두 번째 실행부터: 세션 재사용 (로그인 생략!)
python src/main.py
```

---

## 📁 저장 위치

```
keyplayer_manager/
└── session_cookies.pkl    # 쿠키 저장 파일 (자동 생성)
```

**중요:** `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.

---

## 🔄 동작 원리

### 첫 실행
```
1. WSOP 사이트 접속
2. 로그인 (Username/Password 입력)
3. 쿠키를 session_cookies.pkl에 저장
4. CSV 다운로드
```

### 두 번째 실행부터
```
1. WSOP 사이트 접속
2. session_cookies.pkl에서 쿠키 로드
3. 페이지 리프레시
4. 로그인 상태 확인
   ├─ ✅ 유효: CSV 다운로드 (로그인 생략!)
   └─ ❌ 만료: 재로그인 후 쿠키 업데이트
```

---

## ⏰ 세션 유효기간

- **24시간**: 쿠키 저장 후 24시간 이내에는 재사용 가능
- **24시간 초과**: 자동으로 재로그인 (쿠키 갱신)

---

## 🛠️ 수동 관리

### 세션 상태 확인

```python
import pickle
from datetime import datetime
from pathlib import Path

session_file = Path("session_cookies.pkl")

if session_file.exists():
    with open(session_file, 'rb') as f:
        data = pickle.load(f)
        last_login = datetime.fromisoformat(data['last_login'])
        age_hours = (datetime.now() - last_login).total_seconds() / 3600

        print(f"저장 시간: {last_login:%Y-%m-%d %H:%M:%S}")
        print(f"경과 시간: {age_hours:.1f}시간")
        print(f"상태: {'유효' if age_hours < 24 else '만료'}")
else:
    print("세션 파일 없음")
```

### 세션 강제 삭제 (재로그인 강제)

```bash
# Windows
del session_cookies.pkl

# Linux/Mac
rm session_cookies.pkl
```

또는 Python으로:

```python
from pathlib import Path
Path("session_cookies.pkl").unlink(missing_ok=True)
```

---

## 📊 로그 예시

### 첫 실행 (새 로그인)

```
🔐 로그인 프로세스 시작
   URL: https://staff.wsopplus.com/...

[1/3] 페이지 접속 중...

[2/3] 저장된 세션 확인...
ℹ️ 저장된 세션 없음 (첫 실행)

[3/3] 새 로그인 수행...
🔑 새 로그인 수행 중...
✅ Username 입력: dean.hong@ggproduction.net
✅ Password 입력 완료
✅ 로그인 제출
✅ 새 로그인 성공

[세션 저장] 다음 실행을 위해 쿠키 저장 중...
✅ 세션 저장 완료: session_cookies.pkl
   쿠키 개수: 1
   저장 시간: 2025-10-17 11:23:29

✅ 로그인 프로세스 완료
```

### 재실행 (세션 재사용)

```
🔐 로그인 프로세스 시작
   URL: https://staff.wsopplus.com/...

[1/3] 페이지 접속 중...

[2/3] 저장된 세션 확인...
✅ 세션 로드 완료
   쿠키 개수: 1
   저장 시간: 2025-10-17 11:23:29
   경과 시간: 0.5시간
✅ 로그인 상태 확인: 세션 유효

✅ 기존 세션으로 로그인 완료 (새 로그인 불필요)

✅ 로그인 프로세스 완료
```

---

## 🔒 보안

### ✅ 안전한 점
- 쿠키는 로컬 파일로만 저장 (외부 전송 없음)
- `.gitignore`로 Git 커밋 차단
- 비밀번호는 `.env`에만 저장 (쿠키 파일에 없음)

### ⚠️ 주의사항
- `session_cookies.pkl`을 다른 사람과 공유하지 마세요
- 다른 PC에서는 사용할 수 없습니다 (IP/브라우저 정보 포함)

---

## 🧪 테스트

### 세션 재사용 테스트

```bash
# 첫 실행 (로그인 + 저장)
python test_session_reuse.py
선택: 1

# 두 번째 실행 (세션 재사용)
python test_session_reuse.py
선택: 2

# 세션 삭제 후 재실행
python test_session_reuse.py
선택: 3
```

---

## 💡 FAQ

### Q1: 세션이 왜 재사용되지 않나요?

**원인:**
- 24시간이 지났음
- WSOP 사이트가 쿠키를 무효화함
- IP 주소가 변경됨

**해결:**
- 자동으로 재로그인됩니다 (추가 조치 불필요)

### Q2: 매번 로그인하면 밴 당하나요?

**가능성:**
- 짧은 시간에 여러 번 로그인: 위험
- 하루 1~2회 로그인: 안전
- **세션 사용 시 (추천):** 24시간마다 1회만 로그인

### Q3: 다른 PC에서도 사용 가능한가요?

**불가능:**
- 쿠키는 IP 주소와 브라우저 정보를 포함
- PC마다 별도로 로그인 필요

### Q4: 세션 파일을 수동으로 복사하면?

**비추천:**
- 대부분의 경우 작동하지 않음
- 각 PC에서 자동으로 관리하는 것이 안전

---

## 🎯 권장 사용 시나리오

### 시나리오 1: 개발/테스트 (로컬 PC)
```bash
# 첫 실행
python src/main.py

# 이후 계속 실행 (세션 재사용)
python src/main.py
python src/main.py
python src/main.py
# → 24시간 동안 로그인 1회만!
```

### 시나리오 2: 자동화 (1시간마다)
```bash
# Windows Task Scheduler 또는 Cron 등록
0 * * * * python /path/to/src/main.py

# 24시간 = 24회 실행
# → 로그인은 1회만! (세션 재사용)
```

### 시나리오 3: 서버 배포
```bash
# 서버에서 첫 실행 (로그인 + 세션 저장)
python src/main.py

# 이후 스케줄러가 자동 실행
# → 세션 유효기간 동안 로그인 생략
```

---

## 📋 체크리스트

자동화 전 확인사항:

- [ ] `.env` 파일에 로그인 정보 설정
- [ ] 첫 실행 시 수동으로 테스트 (`python src/main.py`)
- [ ] `session_cookies.pkl` 파일 생성 확인
- [ ] 두 번째 실행 시 로그인 생략 확인
- [ ] 스케줄러 등록 (선택)

---

## 🚀 다음 단계

세션 관리가 정상 작동하면:

1. **스케줄러 설정**: [README.md](README.md#자동-스케줄링) 참조
2. **Google Sheets 연동**: `credentials.json` 설정
3. **전체 자동화 테스트**: `python src/main.py`

---

**v1.0.0** | 작성일: 2025-01-17