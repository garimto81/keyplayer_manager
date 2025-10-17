@echo off
REM Windows Task Scheduler 등록 스크립트
REM 관리자 권한으로 실행 필요

echo ========================================
echo   Windows 작업 스케줄러 등록
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%..\src\main.py
set TASK_NAME=KeyPlayerManager_Hourly

REM Python 경로 찾기
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i

echo [정보] Python 경로: %PYTHON_PATH%
echo [정보] 스크립트 경로: %PYTHON_SCRIPT%
echo.

REM 기존 작업 삭제
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo [정보] 기존 작업 삭제 중...
    schtasks /Delete /TN "%TASK_NAME%" /F
)

REM 새 작업 등록 (1시간마다)
echo [등록] 1시간마다 실행되는 작업 생성 중...
schtasks /Create /TN "%TASK_NAME%" ^
    /TR "\"%PYTHON_PATH%\" \"%PYTHON_SCRIPT%\"" ^
    /SC HOURLY ^
    /ST 00:00 ^
    /RU "%USERNAME%" ^
    /RL HIGHEST ^
    /F

if errorlevel 1 (
    echo [오류] 작업 등록 실패
    pause
    exit /b 1
)

echo.
echo ========================================
echo   등록 완료!
echo ========================================
echo   작업 이름: %TASK_NAME%
echo   실행 주기: 1시간마다
echo   다음 실행: 매시 정각
echo.
echo [확인] 작업 스케줄러에서 확인하세요
echo   1. Win + R 입력
echo   2. taskschd.msc 입력
echo   3. %TASK_NAME% 작업 확인
echo ========================================
pause