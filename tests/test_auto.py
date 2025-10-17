"""
자동 WSOP 로그인 테스트 (input() 없음)
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

print("=" * 70)
print("  WSOP 로그인 자동 테스트")
print("=" * 70)

# Step 1: 환경 변수
print("\n[1/6] 환경 변수 확인")
username = os.getenv("WSOP_USERNAME")
password = os.getenv("WSOP_PASSWORD")
url = os.getenv("WSOP_URL")

print(f"  Username: {username}")
print(f"  Password: {'*' * len(password)}")
print(f"  URL: {url}")

if not username or username == "your_username":
    print("\n❌ .env 파일을 확인하세요!")
    sys.exit(1)

driver = None

try:
    # Step 2: Selenium 설정
    print("\n[2/6] Selenium Chrome 드라이버 설정")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # 브라우저 표시
    # chrome_options.add_argument("--headless")

    print("  Chrome 드라이버 다운로드 중...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"  ✅ Chrome {driver.capabilities['browserVersion']} 준비 완료")

    # Step 3: 사이트 접속
    print("\n[3/6] WSOP 사이트 접속")
    print(f"  접속: {url}")
    driver.get(url)
    time.sleep(3)

    print(f"  ✅ 페이지 로드 완료")
    print(f"     제목: {driver.title}")
    print(f"     URL: {driver.current_url}")

    # Step 4: 로그인 폼 찾기
    print("\n[4/6] 로그인 폼 요소 찾기")

    username_selectors = [
        (By.ID, "username"),
        (By.NAME, "username"),
        (By.ID, "email"),
        (By.NAME, "email"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.CSS_SELECTOR, "input[type='email']"),
    ]

    password_selectors = [
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]

    # Username 필드
    username_field = None
    print("  Username 필드 탐색...")
    for selector_type, selector_value in username_selectors:
        try:
            element = driver.find_element(selector_type, selector_value)
            if element.is_displayed():
                username_field = element
                print(f"  ✅ Username 필드 발견: {selector_type}={selector_value}")
                break
        except:
            continue

    if not username_field:
        print("  ❌ Username 필드를 찾을 수 없습니다!")
        print("\n브라우저 창을 20초간 열어둡니다 (수동 확인용)")
        time.sleep(20)
        sys.exit(1)

    # Password 필드
    password_field = None
    print("  Password 필드 탐색...")
    for selector_type, selector_value in password_selectors:
        try:
            element = driver.find_element(selector_type, selector_value)
            if element.is_displayed():
                password_field = element
                print(f"  ✅ Password 필드 발견: {selector_type}={selector_value}")
                break
        except:
            continue

    if not password_field:
        print("  ❌ Password 필드를 찾을 수 없습니다!")
        time.sleep(20)
        sys.exit(1)

    # Login 버튼
    login_button_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign in') or contains(text(), 'Log in')]"),
        (By.CSS_SELECTOR, "input[type='submit']"),
    ]

    login_button = None
    print("  Login 버튼 탐색...")
    for selector_type, selector_value in login_button_selectors:
        try:
            element = driver.find_element(selector_type, selector_value)
            if element.is_displayed():
                login_button = element
                print(f"  ✅ Login 버튼 발견: {selector_type}={selector_value}")
                break
        except:
            continue

    if not login_button:
        print("  ⚠️ Login 버튼 없음 (Enter 키 사용)")

    # Step 5: 로그인 시도
    print("\n[5/6] 로그인 시도")
    before_url = driver.current_url

    username_field.clear()
    username_field.send_keys(username)
    print(f"  ✅ Username 입력: {username}")

    password_field.clear()
    password_field.send_keys(password)
    print(f"  ✅ Password 입력: {'*' * len(password)}")

    if login_button:
        login_button.click()
        print("  ✅ Login 버튼 클릭")
    else:
        password_field.send_keys(Keys.RETURN)
        print("  ✅ Enter 키 입력")

    print("  ⏳ 로그인 처리 대기 (5초)...")
    time.sleep(5)

    after_url = driver.current_url
    print(f"  로그인 전: {before_url}")
    print(f"  로그인 후: {after_url}")

    # Step 6: 로그인 검증
    print("\n[6/6] 로그인 성공 여부 확인")

    # 에러 메시지 확인
    error_selectors = [
        (By.CSS_SELECTOR, ".error"),
        (By.CSS_SELECTOR, ".alert-danger"),
        (By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'incorrect')]"),
    ]

    error_found = False
    for selector_type, selector_value in error_selectors:
        try:
            error_element = driver.find_element(selector_type, selector_value)
            if error_element.is_displayed():
                print(f"  ❌ 에러: {error_element.text}")
                error_found = True
                break
        except:
            continue

    if not error_found:
        print("  ✅ 에러 메시지 없음")

    # 로그아웃 버튼 확인
    logout_selectors = [
        (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Log out')]"),
        (By.CSS_SELECTOR, "a[href*='logout']"),
    ]

    logout_found = False
    for selector_type, selector_value in logout_selectors:
        try:
            logout_element = driver.find_element(selector_type, selector_value)
            if logout_element.is_displayed():
                print(f"  ✅ 로그아웃 버튼 발견: '{logout_element.text}'")
                logout_found = True
                break
        except:
            continue

    # 최종 판단
    print("\n" + "=" * 70)
    if logout_found or (not error_found and "login" not in after_url.lower()):
        print("✅✅✅ 로그인 성공! ✅✅✅")
        success = True
    else:
        print("❌ 로그인 실패")
        success = False

    print("=" * 70)

    # 결과 확인
    print("\n⏳ 브라우저를 20초간 열어둡니다 (결과 확인용)")
    print("   브라우저 창을 확인하세요!")
    time.sleep(20)

    if success:
        print("\n🎉 테스트 완료: 로그인 성공!")
        sys.exit(0)
    else:
        print("\n🔍 테스트 완료: 로그인 실패 (수동 확인 필요)")
        sys.exit(1)

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()

    if driver:
        print("\n⏳ 브라우저를 20초간 열어둡니다 (디버깅용)")
        time.sleep(20)

    sys.exit(1)

finally:
    if driver:
        driver.quit()
        print("\n✓ 브라우저 종료")