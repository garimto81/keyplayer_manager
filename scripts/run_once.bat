@echo off
REM Windows에서 수동 실행용 스크립트

echo ========================================
echo   Key Player Manager - 수동 실행
echo ========================================
echo.

REM Python 경로 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다
    echo https://www.python.org/downloads/ 에서 설치하세요
    pause
    exit /b 1
)

REM 가상환경 활성화 (있는 경우)
if exist "..\venv\Scripts\activate.bat" (
    echo [정보] 가상환경 활성화 중...
    call ..\venv\Scripts\activate.bat
)

REM 메인 스크립트 실행
echo [실행] 자동화 시작...
echo.
python ..\src\main.py

echo.
echo ========================================
echo   실행 완료
echo ========================================
pause