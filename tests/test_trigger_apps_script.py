"""
Apps Script 수동 트리거 테스트
- Python에서 Apps Script Web App 호출
- Web App 배포 후 .env에 URL 설정 필요
"""
import sys
import os
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sheets_uploader import SheetsUploader


def main():
    print("=" * 60)
    print("Apps Script 트리거 테스트")
    print("=" * 60)
    print()

    # .env 확인
    apps_script_url = os.getenv("APPS_SCRIPT_URL")

    if not apps_script_url:
        print("❌ APPS_SCRIPT_URL이 설정되지 않았습니다")
        print()
        print("Apps Script Web App 배포 필요:")
        print("  1. TARGET 시트 열기:")
        print("     https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4")
        print("  2. 확장 프로그램 → Apps Script")
        print("  3. 배포 → 새 배포 → 웹 앱")
        print("  4. 액세스: 모든 사용자")
        print("  5. 배포 URL 복사")
        print("  6. .env 파일에 추가:")
        print('     APPS_SCRIPT_URL=https://script.google.com/macros/s/.../exec')
        print()
        print("📖 상세 가이드: docs/guides/APPS_SCRIPT_DEPLOY.md")
        print()
        print("또는 수동 실행:")
        print("  1. Apps Script 편집기에서 updateAndCheckBoxes 선택")
        print("  2. ▶ 실행 버튼 클릭")
        return

    print(f"Apps Script URL: {apps_script_url[:50]}...")
    print()

    # Google Sheets 업로더 초기화
    print("Google Sheets 인증 중...")
    uploader = SheetsUploader('credentials.json')
    print()

    # Apps Script 트리거
    print("Apps Script 실행 중...")
    print("(SOURCE Confirmed E열 → TARGET Type K열 매칭)")
    success = uploader.trigger_apps_script()

    if success:
        print()
        print("✅ Apps Script 실행 완료!")
        print()
        print("결과 확인:")
        print("  - K열: Key Player 마킹 (TRUE)")
        print("  - L열: 짧은 이름 생성")
        print()
        print("시트 확인:")
        print("  https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4")
    else:
        print()
        print("❌ Apps Script 실행 실패")
        print("수동으로 실행하세요:")
        print("  1. TARGET 시트에서 확장 프로그램 → Apps Script")
        print("  2. updateAndCheckBoxes 실행")


if __name__ == '__main__':
    main()
