"""
WSOP 사이트 자동화 스크레이퍼
- 로그인 (세션 유지)
- CSV 다운로드
"""
import os
import sys
import time
import glob
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from session_manager import SessionManager

load_dotenv()


class WSOPScraper:
    """WSOP 사이트 자동화 클래스 (세션 유지 지원)"""

    def __init__(self, download_path="downloads", session_file="session_cookies.pkl"):
        """
        초기화

        Args:
            download_path: CSV 다운로드 경로
            session_file: 세션 쿠키 저장 파일
        """
        self.username = os.getenv("WSOP_USERNAME")
        self.password = os.getenv("WSOP_PASSWORD")
        self.url = os.getenv("WSOP_URL")
        self.download_path = Path(download_path).absolute()
        self.download_path.mkdir(exist_ok=True)

        self.driver = None
        self.session_manager = SessionManager(session_file)

    def _setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()

        # 다운로드 경로 설정
        prefs = {
            "download.default_directory": str(self.download_path),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # 헤드리스 모드 (백그라운드 실행)
        # chrome_options.add_argument("--headless")  # 디버깅 시 주석 처리
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # User-Agent 설정 (봇 감지 방지)
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

        print("✅ Chrome 드라이버 설정 완료")

    def _do_login(self):
        """실제 로그인 수행 (내부 메서드)"""
        print("🔑 새 로그인 수행 중...")

        # 로그인 폼 찾기
        wait = WebDriverWait(self.driver, 15)

        # Username 필드
        username_field = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        username_field.clear()
        username_field.send_keys(self.username)
        print(f"✅ Username 입력: {self.username}")

        # Password 필드
        password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        password_field.send_keys(self.password)
        print("✅ Password 입력 완료")

        # Enter 키로 로그인
        password_field.send_keys(Keys.RETURN)
        print("✅ 로그인 제출")

        time.sleep(5)  # 로그인 처리 대기

        # 로그인 성공 확인
        if "login" in self.driver.current_url.lower():
            raise Exception("❌ 로그인 실패")

        print("✅ 새 로그인 성공")

    def login(self):
        """
        WSOP 사이트 로그인 (세션 재사용)

        세션이 있으면 재사용, 없거나 만료되면 새로 로그인
        """
        try:
            print(f"\n🔐 로그인 프로세스 시작")
            print(f"   URL: {self.url}")

            # 1. 페이지 접속 (쿠키 도메인 설정용)
            print("\n[1/3] 페이지 접속 중...")
            self.driver.get(self.url)
            time.sleep(2)

            # 2. 저장된 세션 로드 시도
            print("\n[2/3] 저장된 세션 확인...")
            session_loaded = self.session_manager.load_cookies(self.driver)

            if session_loaded:
                # 세션 유효성 확인
                self.driver.refresh()
                time.sleep(3)

                if self.session_manager.is_logged_in(self.driver, "/series/"):
                    print("\n✅ 기존 세션으로 로그인 완료 (새 로그인 불필요)")
                    return True
                else:
                    print("\n⚠️ 세션 만료됨, 새로 로그인 필요")

            # 3. 새 로그인 수행
            print("\n[3/3] 새 로그인 수행...")
            self._do_login()

            # 4. 세션 저장
            print("\n[세션 저장] 다음 실행을 위해 쿠키 저장 중...")
            self.session_manager.save_cookies(self.driver)

            print("\n✅ 로그인 프로세스 완료")
            return True

        except Exception as e:
            print(f"\n❌ 로그인 오류: {e}")
            raise

    def download_csv(self):
        """CSV 파일 다운로드"""
        try:
            print("📥 CSV 다운로드 시작")

            # 기존 CSV 파일 삭제 (최신 파일 구분용)
            for old_file in self.download_path.glob("*.csv"):
                old_file.unlink()

            # "Export player list to csv" 버튼 찾기
            wait = WebDriverWait(self.driver, 15)

            export_button_selectors = [
                # 실제 WSOP 사이트 버튼 (텍스트 기반)
                (By.XPATH, "//button[contains(text(), 'Export Player List')]"),
                (By.XPATH, "//button[contains(., 'Export Player List To CSV')]"),
                (By.XPATH, "//span[contains(text(), 'Export Player List')]/ancestor::button"),
                # Class 기반 (bg-primary는 WSOP 주요 버튼)
                (By.CSS_SELECTOR, "button.bg-primary[class*='q-btn']"),
                # 일반적인 패턴
                (By.XPATH, "//button[contains(text(), 'Export')]"),
                (By.XPATH, "//button[contains(text(), 'export')]"),
                (By.XPATH, "//button[contains(text(), 'CSV')]"),
                (By.CSS_SELECTOR, "button.export-csv"),
            ]

            export_button = None
            for selector_type, selector_value in export_button_selectors:
                try:
                    export_button = wait.until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    print(f"✅ Export 버튼 발견: {selector_type}={selector_value}")
                    break
                except:
                    continue

            if not export_button:
                raise Exception("❌ Export 버튼을 찾을 수 없습니다")

            # 버튼 클릭 (JavaScript로 직접 클릭 - 오버레이 우회)
            print("🖱️ Export 버튼 클릭 시도...")

            # 방법 1: JavaScript 클릭 (오버레이 무시)
            try:
                self.driver.execute_script("arguments[0].click();", export_button)
                print("✅ Export 버튼 클릭 (JavaScript)")
            except Exception as e1:
                print(f"⚠️ JavaScript 클릭 실패, 대체 방법 시도... ({e1})")

                # 방법 2: 스크롤 후 일반 클릭
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_button)
                    time.sleep(2)
                    export_button.click()
                    print("✅ Export 버튼 클릭 (스크롤 후)")
                except Exception as e2:
                    print(f"⚠️ 스크롤 클릭 실패, ActionChains 시도... ({e2})")

                    # 방법 3: ActionChains
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(export_button).click().perform()
                    print("✅ Export 버튼 클릭 (ActionChains)")

            # 다운로드 완료 대기 (최대 30초)
            print("⏳ 다운로드 완료 대기 중...")
            download_wait = 30
            csv_file = None

            for _ in range(download_wait):
                csv_files = list(self.download_path.glob("*.csv"))
                # .crdownload 파일 제외
                csv_files = [f for f in csv_files if not f.name.endswith('.crdownload')]

                if csv_files:
                    csv_file = max(csv_files, key=lambda f: f.stat().st_mtime)
                    break
                time.sleep(1)

            if not csv_file:
                raise Exception("❌ CSV 파일 다운로드 실패 (타임아웃)")

            print(f"✅ CSV 다운로드 완료: {csv_file.name}")
            return csv_file

        except Exception as e:
            print(f"❌ CSV 다운로드 오류: {e}")
            raise

    def run(self):
        """전체 스크래핑 실행"""
        try:
            self._setup_driver()
            self.login()
            csv_file = self.download_csv()
            return csv_file

        except Exception as e:
            print(f"❌ 스크래핑 실패: {e}")
            raise

        finally:
            if self.driver:
                self.driver.quit()
                print("✅ 브라우저 종료")


if __name__ == "__main__":
    # 테스트 실행
    scraper = WSOPScraper()
    csv_path = scraper.run()
    print(f"✅ 최종 CSV 파일: {csv_path}")