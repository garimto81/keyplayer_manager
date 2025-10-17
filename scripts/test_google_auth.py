"""
Google Sheets 인증 테스트 스크립트
credentials.json 파일이 올바른지 확인
"""
import sys
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.sheets_uploader import SheetsUploader

    print("=" * 60)
    print("  Google Sheets 인증 테스트")
    print("=" * 60)
    print()

    print("1. credentials.json 확인 중...")
    creds_path = Path(__file__).parent.parent / "credentials.json"

    if not creds_path.exists():
        print("❌ credentials.json이 없습니다!")
        print()
        print("생성 방법:")
        print("1. https://console.cloud.google.com/ 접속")
        print("2. 프로젝트 생성 또는 선택")
        print("3. API 및 서비스 > 사용자 인증 정보")
        print("4. 서비스 계정 만들기")
        print("5. 키 추가 > JSON 다운로드")
        print("6. 다운로드한 파일을 credentials.json으로 저장")
        sys.exit(1)

    print(f"✅ credentials.json 존재: {creds_path}")
    print()

    print("2. Google Sheets API 인증 시도...")
    uploader = SheetsUploader(credentials_path=str(creds_path))
    print("✅ Google Sheets API 인증 성공!")
    print()

    print("3. Spreadsheet 접근 테스트...")
    try:
        spreadsheet = uploader.client.open_by_key(
            "1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg"
        )
        print(f"✅ Spreadsheet 접근 성공: {spreadsheet.title}")

        sheet = spreadsheet.worksheet("Confirmed")
        print(f"✅ 'Confirmed' 시트 접근 성공")
        print(f"   - 행 수: {sheet.row_count}")
        print(f"   - 열 수: {sheet.col_count}")

    except Exception as e:
        print(f"❌ Spreadsheet 접근 실패: {e}")
        print()
        print("해결 방법:")
        print("1. credentials.json에서 client_email 확인")
        print("2. Google Sheets에서 공유 버튼 클릭")
        print("3. 위 이메일 주소 추가 (편집자 권한)")
        sys.exit(1)

    print()
    print("=" * 60)
    print("  ✅ 모든 테스트 통과!")
    print("=" * 60)

except ImportError as e:
    print(f"❌ 모듈 import 실패: {e}")
    print()
    print("해결 방법:")
    print("pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ 예상치 못한 오류: {e}")
    sys.exit(1)