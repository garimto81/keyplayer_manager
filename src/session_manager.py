"""
세션 관리자
- 로그인 쿠키 저장/로드
- 세션 유효성 확인
- 필요시에만 재로그인
"""
import json
import pickle
from pathlib import Path
from datetime import datetime, timedelta


class SessionManager:
    """
    WSOP 세션 관리 클래스

    기능:
    1. 로그인 후 쿠키를 파일로 저장
    2. 다음 실행 시 쿠키 로드하여 로그인 생략
    3. 세션 만료 시 자동 재로그인
    """

    def __init__(self, session_file="session_cookies.pkl"):
        """
        초기화

        Args:
            session_file: 쿠키 저장 파일 경로
        """
        self.session_file = Path(session_file)
        self.cookies = None
        self.last_login = None

    def save_cookies(self, driver):
        """
        현재 드라이버의 쿠키를 파일로 저장

        Args:
            driver: Selenium WebDriver 인스턴스
        """
        try:
            cookies = driver.get_cookies()
            session_data = {
                "cookies": cookies,
                "last_login": datetime.now().isoformat(),
                "url": driver.current_url
            }

            with open(self.session_file, 'wb') as f:
                pickle.dump(session_data, f)

            print(f"✅ 세션 저장 완료: {self.session_file}")
            print(f"   쿠키 개수: {len(cookies)}")
            print(f"   저장 시간: {datetime.now():%Y-%m-%d %H:%M:%S}")

        except Exception as e:
            print(f"⚠️ 세션 저장 실패: {e}")

    def load_cookies(self, driver):
        """
        저장된 쿠키를 드라이버에 로드

        Args:
            driver: Selenium WebDriver 인스턴스

        Returns:
            bool: 로드 성공 여부
        """
        if not self.session_file.exists():
            print("ℹ️ 저장된 세션 없음 (첫 실행)")
            return False

        try:
            with open(self.session_file, 'rb') as f:
                session_data = pickle.load(f)

            cookies = session_data.get("cookies", [])
            last_login = datetime.fromisoformat(session_data.get("last_login"))

            # 세션 유효기간 확인 (24시간)
            age = datetime.now() - last_login
            if age > timedelta(hours=24):
                print(f"⚠️ 세션 만료 (경과: {age.total_seconds() / 3600:.1f}시간)")
                return False

            # 쿠키 로드
            for cookie in cookies:
                try:
                    # 'expiry' 필드는 과거 시간일 수 있으므로 제거
                    if 'expiry' in cookie:
                        del cookie['expiry']

                    driver.add_cookie(cookie)
                except Exception as e:
                    # 개별 쿠키 오류는 무시
                    pass

            print(f"✅ 세션 로드 완료")
            print(f"   쿠키 개수: {len(cookies)}")
            print(f"   저장 시간: {last_login:%Y-%m-%d %H:%M:%S}")
            print(f"   경과 시간: {age.total_seconds() / 3600:.1f}시간")

            return True

        except Exception as e:
            print(f"⚠️ 세션 로드 실패: {e}")
            return False

    def is_logged_in(self, driver, check_url_pattern="/series/", wait_time=5):
        """
        현재 로그인 상태 확인

        Args:
            driver: Selenium WebDriver 인스턴스
            check_url_pattern: 로그인 상태 확인용 URL 패턴
            wait_time: 페이지 로드 대기 시간

        Returns:
            bool: 로그인 여부
        """
        try:
            import time

            # 페이지 로드 대기
            time.sleep(wait_time)

            current_url = driver.current_url

            # 로그인 페이지로 리다이렉트되었는지 확인
            if "login" in current_url.lower():
                print("⚠️ 로그인 상태 확인: 로그인 페이지로 리다이렉트됨")
                return False

            # 목표 URL 패턴 확인
            if check_url_pattern in current_url:
                print("✅ 로그인 상태 확인: 세션 유효")
                return True

            # URL 패턴이 다른 경우 (예: 홈페이지)
            print(f"⚠️ 로그인 상태 불명확 (현재 URL: {current_url})")
            return False

        except Exception as e:
            print(f"⚠️ 로그인 상태 확인 실패: {e}")
            return False

    def clear_session(self):
        """저장된 세션 파일 삭제"""
        if self.session_file.exists():
            self.session_file.unlink()
            print("✅ 세션 파일 삭제")


if __name__ == "__main__":
    # 테스트 예시
    import os
    from dotenv import load_dotenv
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import time

    load_dotenv()

    print("=" * 60)
    print("  세션 관리자 테스트")
    print("=" * 60)

    # Chrome 설정
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    session_mgr = SessionManager()

    try:
        url = os.getenv("WSOP_URL")
        username = os.getenv("WSOP_USERNAME")
        password = os.getenv("WSOP_PASSWORD")

        # 먼저 페이지 접속 (쿠키 도메인 설정용)
        driver.get(url)
        time.sleep(2)

        # 세션 로드 시도
        print("\n[1] 저장된 세션 로드 시도")
        session_loaded = session_mgr.load_cookies(driver)

        if session_loaded:
            # 세션 유효성 확인
            driver.refresh()
            time.sleep(3)

            if session_mgr.is_logged_in(driver):
                print("\n✅ 기존 세션으로 로그인 성공!")
            else:
                print("\n⚠️ 세션 만료, 재로그인 필요")
                session_loaded = False

        # 세션이 없거나 만료된 경우 로그인
        if not session_loaded:
            print("\n[2] 새로 로그인")
            username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            time.sleep(5)

            if session_mgr.is_logged_in(driver):
                print("\n✅ 로그인 성공!")

                # 세션 저장
                print("\n[3] 세션 저장")
                session_mgr.save_cookies(driver)
            else:
                print("\n❌ 로그인 실패")

        print("\n⏳ 10초 대기 (결과 확인)")
        time.sleep(10)

    finally:
        driver.quit()
        print("\n✓ 브라우저 종료")