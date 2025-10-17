# ⚡ 빠른 시작 가이드 (5분 완성)

## 1️⃣ Python 패키지 설치 (1분)

```bash
pip install -r requirements.txt
```

---

## 2️⃣ 환경 설정 (2분)

### `.env` 파일 생성

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### `.env` 파일 수정

```bash
WSOP_USERNAME=실제_아이디
WSOP_PASSWORD=실제_비밀번호
```

---

## 3️⃣ Google API 설정 (2분)

### 방법 1: 기존 프로젝트 사용

1. Google Cloud Console에서 기존 프로젝트의 서비스 계정 키 다운로드
2. `credentials.json`으로 저장

### 방법 2: 새 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/)
2. 프로젝트 생성 → Google Sheets API 활성화
3. 서비스 계정 생성 → JSON 키 다운로드
4. `credentials.json`으로 저장

### Google Sheets 권한 부여

```bash
# credentials.json에서 이메일 주소 확인
# (예: keyplayer-bot@xxx.iam.gserviceaccount.com)
```

**두 개의 Google Sheets에 모두 추가**:
- [Confirmed 시트](https://docs.google.com/spreadsheets/d/1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg)
- [Type 시트](https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4)

→ **공유** 버튼 클릭 → 이메일 추가 → **편집자** 권한

---

## 4️⃣ 테스트 실행

```bash
python src/main.py
```

**예상 출력**:
```
🚀 키 플레이어 자동화 시작
✅ Chrome 드라이버 설정 완료
🔑 로그인 시도...
✅ 로그인 성공
📥 CSV 다운로드 시작
✅ CSV 다운로드 완료
📤 Google Sheets에 데이터 업로드
✅ Sheets 업로드 완료
🎉 자동화 완료!
```

---

## 5️⃣ 자동 실행 설정 (선택)

### Windows

```bash
# 관리자 권한으로 실행
scripts\schedule_task_windows.bat
```

### Linux/Mac

```bash
crontab -e

# 1시간마다 실행
0 * * * * cd /path/to/keyplayer_manager && python3 src/main.py >> logs/cron.log 2>&1
```

---

## ✅ 체크리스트

- [ ] Python 3.8+ 설치됨
- [ ] Chrome 브라우저 설치됨
- [ ] `pip install -r requirements.txt` 완료
- [ ] `.env` 파일 생성 및 수정
- [ ] `credentials.json` 배치
- [ ] Google Sheets 권한 부여 (2개 시트)
- [ ] `python src/main.py` 테스트 성공

---

## 🆘 문제 발생 시

### 1. "No module named 'selenium'"

```bash
pip install selenium webdriver-manager
```

### 2. "Insufficient Permission" (Google Sheets)

→ `credentials.json`의 이메일 주소를 Google Sheets에 **편집자**로 추가

### 3. "Chrome driver not found"

→ Chrome 브라우저가 설치되어 있는지 확인

### 4. WSOP 로그인 실패

→ `.env`에서 `WSOP_USERNAME`, `WSOP_PASSWORD` 확인

---

## 📚 자세한 가이드

전체 문서는 [README.md](README.md) 참조

---

**준비 완료!** 🎉

이제 자동화 시스템이 1시간마다 실행됩니다.