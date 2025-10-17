"""
메인 자동화 스크립트
- WSOP 스크래핑 + Google Sheets 업로드 + Apps Script 트리거
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from wsop_scraper import WSOPScraper
from sheets_uploader import SheetsUploader
from dotenv import load_dotenv

# 프로젝트 루트 경로
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

load_dotenv()


class KeyPlayerManager:
    """키 플레이어 자동화 관리자"""

    def __init__(self):
        self.scraper = None
        self.uploader = None
        self.log_file = ROOT_DIR / "logs" / f"automation_{datetime.now():%Y%m%d}.log"
        self.log_file.parent.mkdir(exist_ok=True)

    def log(self, message):
        """로그 출력 및 저장"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def send_notification(self, subject, message, is_error=False):
        """이메일 알림 전송 (선택)"""
        notification_email = os.getenv("NOTIFICATION_EMAIL")

        if not notification_email:
            return

        try:
            import smtplib
            from email.mime.text import MIMEText

            # Gmail SMTP 예시 (실제 환경에 맞게 수정)
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_user = os.getenv("SMTP_USER")
            smtp_password = os.getenv("SMTP_PASSWORD")

            if not all([smtp_user, smtp_password]):
                return

            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = f"{'❌' if is_error else '✅'} {subject}"
            msg['From'] = smtp_user
            msg['To'] = notification_email

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            self.log(f"📧 알림 전송 완료: {notification_email}")

        except Exception as e:
            self.log(f"⚠️ 알림 전송 실패: {e}")

    def run(self):
        """전체 워크플로우 실행"""
        start_time = datetime.now()
        self.log("=" * 60)
        self.log("🚀 키 플레이어 자동화 시작")
        self.log("=" * 60)

        try:
            # 1. WSOP 스크래핑
            self.log("📥 [단계 1/3] WSOP 사이트에서 CSV 다운로드")
            self.scraper = WSOPScraper(download_path=os.getenv("DOWNLOAD_PATH", "downloads"))
            csv_file = self.scraper.run()
            self.log(f"✅ CSV 다운로드 완료: {csv_file}")

            # 2. Google Sheets 업로드 (TARGET 'type' 시트)
            self.log("📤 [단계 2/3] Google Sheets 'type' 시트에 CSV 업로드")
            self.uploader = SheetsUploader(credentials_path="credentials.json")
            self.uploader.upload_csv_to_type_sheet(csv_file)
            self.log("✅ 'type' 시트 업로드 완료")

            # 3. Apps Script 트리거 (Time Trigger 방식)
            self.log("🔄 [단계 3/3] Apps Script 실행 대기")
            self.log("   → Time Trigger가 1분 이내 자동 실행합니다")
            self.log("   → Type 시트 변경 감지 후 updateAndCheckBoxes() 자동 호출")

            # 완료
            elapsed = (datetime.now() - start_time).total_seconds()
            self.log("=" * 60)
            self.log(f"🎉 자동화 완료! (소요시간: {elapsed:.1f}초)")
            self.log("=" * 60)

            # 성공 알림
            self.send_notification(
                "Key Player 자동화 성공",
                f"소요시간: {elapsed:.1f}초\n"
                f"CSV 파일: {csv_file}\n"
                f"업데이트 시간: {datetime.now():%Y-%m-%d %H:%M:%S}"
            )

            return True

        except Exception as e:
            error_msg = f"❌ 자동화 실패: {e}"
            self.log(error_msg)
            self.log("=" * 60)

            # 에러 알림
            self.send_notification(
                "Key Player 자동화 실패",
                f"오류 내용: {e}\n"
                f"로그 파일: {self.log_file}\n"
                f"발생 시간: {datetime.now():%Y-%m-%d %H:%M:%S}",
                is_error=True
            )

            return False


if __name__ == "__main__":
    manager = KeyPlayerManager()
    success = manager.run()
    sys.exit(0 if success else 1)