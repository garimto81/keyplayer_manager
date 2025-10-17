"""
Google Sheets 업로더
- CSV 데이터를 Google Sheets에 업로드
- Apps Script 트리거 호출
"""
import os
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class SheetsUploader:
    """Google Sheets 업로드 클래스"""

    def __init__(self, credentials_path="credentials.json"):
        """
        초기화

        Args:
            credentials_path: Google Service Account JSON 파일 경로
        """
        self.source_spreadsheet_id = os.getenv("SOURCE_SPREADSHEET_ID")  # Confirmed (Key Player 마스터)
        self.target_spreadsheet_id = os.getenv("TARGET_SPREADSHEET_ID")  # type (CSV 업로드)
        self.credentials_path = Path(credentials_path)

        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"❌ Google credentials 파일이 없습니다: {self.credentials_path}\n"
                f"   생성 방법: https://console.cloud.google.com/iam-admin/serviceaccounts"
            )

        self.client = self._authenticate()
        print("✅ Google Sheets 인증 완료")

    def _authenticate(self):
        """Google Sheets API 인증"""
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(self.credentials_path), scope
        )
        return gspread.authorize(creds)

    def upload_csv_to_type_sheet(self, csv_file_path):
        """
        CSV 파일을 TARGET 'type' 시트에 업로드

        설계:
        - SOURCE (Confirmed): Key Player 마스터 리스트 (수동 관리)
        - TARGET (type): WSOP CSV 데이터 업로드 + Key Player 자동 마킹

        Args:
            csv_file_path: CSV 파일 경로

        Returns:
            업로드 성공 여부
        """
        try:
            csv_path = Path(csv_file_path)
            if not csv_path.exists():
                raise FileNotFoundError(f"❌ CSV 파일이 없습니다: {csv_path}")

            print(f"📤 CSV 업로드 시작: {csv_path.name}")

            # TARGET 스프레드시트 열기
            spreadsheet = self.client.open_by_key(self.target_spreadsheet_id)
            sheet = spreadsheet.worksheet("Type")  # 대문자 T

            # CSV 읽기
            with open(csv_path, 'r', encoding='utf-8-sig') as f:  # BOM 제거
                csv_data = list(csv.reader(f))

            if not csv_data:
                raise ValueError("❌ CSV 파일이 비어있습니다")

            print(f"📊 CSV 데이터: {len(csv_data)}행 × {len(csv_data[0])}열")

            # 기존 데이터 클리어 (전체 시트 클리어 후 재작성)
            print("🗑️ 기존 데이터 클리어 중...")
            sheet.clear()

            # 새 데이터 삽입 (헤더 포함)
            print("📝 새 데이터 삽입 중...")
            sheet.update('A1', csv_data, value_input_option='RAW')

            print(f"✅ 'type' 시트 업데이트 완료: {len(csv_data)}행")
            return True

        except Exception as e:
            print(f"❌ Sheets 업로드 오류: {e}")
            raise

    def trigger_apps_script(self, script_url=None):
        """
        Apps Script Web App 트리거

        Args:
            script_url: Apps Script Web App URL (배포 후 생성)

        Note:
            Apps Script를 Web App으로 배포해야 합니다:
            1. Apps Script 편집기에서 '배포' > '새 배포'
            2. 유형: 웹 앱
            3. 실행 사용자: 나
            4. 액세스 권한: 모든 사용자
            5. URL 복사 후 .env에 APPS_SCRIPT_URL로 저장
        """
        if not script_url:
            script_url = os.getenv("APPS_SCRIPT_URL")

        if not script_url:
            print("⚠️ APPS_SCRIPT_URL이 설정되지 않았습니다")
            print("   수동으로 Apps Script 실행: updateAndCheckBoxes()")
            return False

        try:
            import requests
            print("🚀 Apps Script 트리거 호출 중...")
            response = requests.get(script_url, timeout=60)

            if response.status_code == 200:
                print("✅ Apps Script 실행 완료")
                return True
            else:
                print(f"⚠️ Apps Script 응답 코드: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Apps Script 트리거 오류: {e}")
            return False


if __name__ == "__main__":
    # 테스트 실행
    import sys

    if len(sys.argv) < 2:
        print("사용법: python sheets_uploader.py <csv_file_path>")
        sys.exit(1)

    csv_file = sys.argv[1]
    uploader = SheetsUploader()
    uploader.upload_csv_to_type_sheet(csv_file)
    uploader.trigger_apps_script()