"""
단계별 WSOP 로그인 테스트
각 단계를 확인하며 진행
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

load_dotenv()


def step1_check_env():
    """Step 1: 환경 변수 확인"""
    print("\n" + "=" * 60)
    print("STEP 1: 환경 변수 확인")
    print("=" * 60)

    username = os.getenv("WSOP_USERNAME")
    password = os.getenv("WSOP_PASSWORD")
    url = os.getenv("WSOP_URL")

    print(f"✓ WSOP_USERNAME: {username}")
    print(f"✓ WSOP_PASSWORD: {'*' * len(password) if password else 'None'}")
    print(f"✓ WSOP_URL: {url}")

    if not username or username == "your_username":
        print("\n❌ .env 파일을 확인하세요!")
        return False

    print("\n✅ Step 1 통과: 환경 변수 설정 완료")
    return True


def step2_selenium_setup():
    """Step 2: Selenium 및 Chrome 드라이버 설정"""
    print("\n" + "=" * 60)
    print("STEP 2: Selenium Chrome 드라이버 설정")
    print("=" * 60)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        print("✓ Selenium 모듈 import 성공")

        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        # 브라우저 표시 (디버깅용)
        # chrome_options.add_argument("--headless")

        print("✓ Chrome 옵션 설정 완료")

        # 드라이버 설치
        print("✓ Chrome 드라이버 다운로드 중...")
        service = Service(ChromeDriverManager().install())

        print("✓ Chrome 드라이버 생성 중...")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("✓ Chrome 버전:", driver.capabilities['browserVersion'])
        print("✓ ChromeDriver 버전:", driver.capabilities['chrome']['chromedriverVersion'].split()[0])

        print("\n✅ Step 2 통과: Selenium 준비 완료")
        return driver

    except Exception as e:
        print(f"\n❌ Step 2 실패: {e}")
        import traceback
        traceback.print_exc()
        return None


def step3_access_site(driver):
    """Step 3: WSOP 사이트 접속"""
    print("\n" + "=" * 60)
    print("STEP 3: WSOP 사이트 접속")
    print("=" * 60)

    url = os.getenv("WSOP_URL")

    try:
        print(f"✓ 접속 중: {url}")
        driver.get(url)

        time.sleep(3)  # 페이지 로딩 대기

        print(f"✓ 현재 URL: {driver.current_url}")
        print(f"✓ 페이지 제목: {driver.title}")
        print(f"✓ 페이지 소스 길이: {len(driver.page_source)} bytes")

        print("\n✅ Step 3 통과: 사이트 접속 성공")
        return True

    except Exception as e:
        print(f"\n❌ Step 3 실패: {e}")
        return False


def step4_find_login_form(driver):
    """Step 4: 로그인 폼 요소 찾기"""
    print("\n" + "=" * 60)
    print("STEP 4: 로그인 폼 요소 찾기")
    print("=" * 60)

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # 가능한 셀렉터들
    username_selectors = [
        (By.ID, "username", "ID: username"),
        (By.NAME, "username", "NAME: username"),
        (By.ID, "email", "ID: email"),
        (By.NAME, "email", "NAME: email"),
        (By.CSS_SELECTOR, "input[type='text']", "CSS: input[type='text']"),
        (By.CSS_SELECTOR, "input[type='email']", "CSS: input[type='email']"),
        (By.XPATH, "//input[@placeholder='Username' or @placeholder='Email']", "XPATH: placeholder"),
    ]

    password_selectors = [
        (By.ID, "password", "ID: password"),
        (By.NAME, "password", "NAME: password"),
        (By.CSS_SELECTOR, "input[type='password']", "CSS: input[type='password']"),
    ]

    # Username 필드 찾기
    username_field = None
    username_selector_info = None

    print("\n🔍 Username/Email 필드 탐색 중...")
    for selector_type, selector_value, description in username_selectors:
        try:
            element = driver.find_element(selector_type, selector_value)
            if element.is_displayed():
                username_field = element
                username_selector_info = (selector_type, selector_value, description)
                print(f"✓ Username 필드 발견: {description}")
                break
        except:
            print(f"  ✗ {description} - 없음")
            continue

    if not username_field:
        print("\n❌ Username 필드를 찾을 수 없습니다!")
        print("\n수동 확인 필요:")
        print("1. 브라우저 창에서 F12 (개발자 도구)")
        print("2. 로그인 필드 우클릭 > 검사")
        print("3. id, name, class 속성 확인")
        return None, None, None

    # Password 필드 찾기
    password_field = None
    password_selector_info = None

    print("\n🔍 Password 필드 탐색 중...")
    for selector_type, selector_value, description in password_selectors:
        try:
            element = driver.find_element(selector_type, selector_value)
            if element.is_displayed():
                password_field = element
                password_selector_info = (selector_type, selector_value, description)
                print(f"✓ Password 필드 발견: {description}")
                break
        except:
            print(f"  ✗ {description} - 없음")
            continue

    if not password_field:
        print("\n❌ Password 필드를 찾을 수 없습니다!")
        return None, None, None

    # Login 버튼 찾기
    login_button_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']", "CSS: button[type='submit']"),
        (By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign in') or contains(text(), 'Log in')]", "XPATH: 텍스트 포함"),
        (By.CSS_SELECTOR, "input[type='submit']", "CSS: input[type='submit']"),
        (By.CSS_SELECTOR, "button.btn-primary", "CSS: button.btn-primary"),
    ]

    login_button = None
    login_button_info = None

    print("\n🔍 Login 버튼 탐색 중...")
    for selector_type, selector_value, description in login_button_selectors:
        try:
            element = driver.find_element(selector_type, selector_value)
            if element.is_displayed():
                login_button = element
                login_button_info = (selector_type, selector_value, description)
                print(f"✓ Login 버튼 발견: {description}")
                break
        except:
            print(f"  ✗ {description} - 없음")
            continue

    if not login_button:
        print("\n⚠️ Login 버튼을 찾을 수 없습니다 (Enter로 로그인 시도 가능)")

    print("\n✅ Step 4 통과: 로그인 폼 발견")
    return username_field, password_field, login_button


def step5_login(driver, username_field, password_field, login_button):
    """Step 5: 로그인 시도"""
    print("\n" + "=" * 60)
    print("STEP 5: 로그인 시도")
    print("=" * 60)

    username = os.getenv("WSOP_USERNAME")
    password = os.getenv("WSOP_PASSWORD")

    try:
        # Username 입력
        print(f"✓ Username 입력 중: {username}")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(0.5)

        # Password 입력
        print(f"✓ Password 입력 중: {'*' * len(password)}")
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)

        # 현재 URL 저장 (로그인 후 변경 확인용)
        before_url = driver.current_url

        # 로그인 버튼 클릭 또는 Enter
        if login_button:
            print("✓ Login 버튼 클릭")
            login_button.click()
        else:
            print("✓ Enter 키 입력 (버튼 없음)")
            from selenium.webdriver.common.keys import Keys
            password_field.send_keys(Keys.RETURN)

        # 로그인 처리 대기
        print("⏳ 로그인 처리 중... (5초 대기)")
        time.sleep(5)

        after_url = driver.current_url

        print(f"\n✓ 로그인 전 URL: {before_url}")
        print(f"✓ 로그인 후 URL: {after_url}")

        print("\n✅ Step 5 통과: 로그인 시도 완료")
        return True

    except Exception as e:
        print(f"\n❌ Step 5 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def step6_verify_login(driver):
    """Step 6: 로그인 성공 여부 확인"""
    print("\n" + "=" * 60)
    print("STEP 6: 로그인 성공 여부 확인")
    print("=" * 60)

    from selenium.webdriver.common.by import By

    current_url = driver.current_url
    page_title = driver.title

    print(f"✓ 현재 URL: {current_url}")
    print(f"✓ 페이지 제목: {page_title}")

    # 로그인 실패 징후 확인
    error_selectors = [
        (By.CSS_SELECTOR, ".error"),
        (By.CSS_SELECTOR, ".alert-danger"),
        (By.CSS_SELECTOR, ".alert-error"),
        (By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'incorrect') or contains(text(), 'failed')]"),
    ]

    print("\n🔍 에러 메시지 확인 중...")
    error_found = False
    for selector_type, selector_value in error_selectors:
        try:
            error_element = driver.find_element(selector_type, selector_value)
            if error_element.is_displayed():
                print(f"❌ 에러 메시지 발견: {error_element.text}")
                error_found = True
                break
        except:
            continue

    if not error_found:
        print("✓ 에러 메시지 없음")

    # URL 변경 확인
    if "login" in current_url.lower():
        print("\n⚠️ 경고: URL에 여전히 'login'이 포함됨")
        print("   → 로그인이 실패했을 가능성")
    else:
        print("\n✓ URL이 로그인 페이지가 아님 (성공 가능성)")

    # 로그아웃 버튼 확인 (로그인 성공 시 보통 존재)
    print("\n🔍 로그아웃 버튼 확인 중...")
    logout_selectors = [
        (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Log out') or contains(text(), 'Sign out')]"),
        (By.CSS_SELECTOR, "a[href*='logout']"),
        (By.CSS_SELECTOR, ".logout"),
    ]

    logout_found = False
    for selector_type, selector_value in logout_selectors:
        try:
            logout_element = driver.find_element(selector_type, selector_value)
            if logout_element.is_displayed():
                print(f"✓ 로그아웃 버튼 발견: {logout_element.text}")
                logout_found = True
                break
        except:
            continue

    if not logout_found:
        print("  ✗ 로그아웃 버튼 없음")

    # 최종 판단
    print("\n" + "=" * 60)
    if logout_found or (not error_found and "login" not in current_url.lower()):
        print("✅✅✅ 로그인 성공! ✅✅✅")
        print("=" * 60)
        return True
    else:
        print("❌ 로그인 실패 가능성")
        print("=" * 60)
        return False


def main():
    """메인 실행"""
    print("\n" + "=" * 70)
    print("  WSOP 로그인 단계별 테스트")
    print("=" * 70)

    driver = None

    try:
        # Step 1: 환경 변수 확인
        if not step1_check_env():
            return

        input("\n계속하려면 Enter를 누르세요...")

        # Step 2: Selenium 설정
        driver = step2_selenium_setup()
        if not driver:
            return

        input("\n계속하려면 Enter를 누르세요...")

        # Step 3: 사이트 접속
        if not step3_access_site(driver):
            return

        input("\n브라우저 창을 확인한 후 Enter를 누르세요...")

        # Step 4: 로그인 폼 찾기
        username_field, password_field, login_button = step4_find_login_form(driver)
        if not username_field or not password_field:
            print("\n⏳ 브라우저를 30초간 열어둡니다 (수동 확인용)")
            time.sleep(30)
            return

        input("\n로그인을 시도하려면 Enter를 누르세요...")

        # Step 5: 로그인
        if not step5_login(driver, username_field, password_field, login_button):
            return

        # Step 6: 로그인 검증
        success = step6_verify_login(driver)

        # 결과 확인 시간
        print("\n⏳ 결과 확인을 위해 브라우저를 30초간 열어둡니다...")
        print("   브라우저 창을 확인하세요!")
        time.sleep(30)

        if success:
            print("\n🎉 테스트 성공!")
        else:
            print("\n🔍 수동 확인 필요")

    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단됨")

    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            input("\n브라우저를 닫으려면 Enter를 누르세요...")
            driver.quit()
            print("✓ 브라우저 종료")


if __name__ == "__main__":
    main()