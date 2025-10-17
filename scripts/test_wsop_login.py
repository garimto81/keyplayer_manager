"""
WSOP 로그인 테스트 스크립트
Selenium 동작 확인 (헤드리스 모드 OFF)
"""
import sys
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import os
    from dotenv import load_dotenv
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    load_dotenv()

    print("=" * 60)
    print("  WSOP 로그인 테스트")
    print("=" * 60)
    print()

    # .env 확인
    username = os.getenv("WSOP_USERNAME")
    password = os.getenv("WSOP_PASSWORD")
    url = os.getenv("WSOP_URL")

    if username == "your_username" or not username:
        print("❌ .env 파일을 수정하세요!")
        print("   WSOP_USERNAME=실제_아이디")
        print("   WSOP_PASSWORD=실제_비밀번호")
        sys.exit(1)

    print(f"✅ .env 설정 확인")
    print(f"   - Username: {username}")
    print(f"   - URL: {url}")
    print()

    # Chrome 드라이버 설정
    print("🔧 Chrome 드라이버 설정 중...")
    chrome_options = Options()
    # 헤드리스 모드 OFF (브라우저 표시)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ Chrome 드라이버 준비 완료")
    print()

    try:
        print("🌐 WSOP 사이트 접속 중...")
        driver.get(url)
        print(f"✅ 페이지 로드 완료: {driver.title}")
        print()

        print("⏳ 10초간 대기 (로그인 필드 확인용)")
        print("   → 브라우저 창을 확인하세요!")
        print("   → 로그인 필드의 ID, name, class를 확인하세요")
        print()

        import time
        time.sleep(10)

        # 페이지 소스 일부 출력
        print("📄 페이지 정보:")
        print(f"   - 현재 URL: {driver.current_url}")
        print(f"   - Title: {driver.title}")

        # 로그인 폼 찾기 시도
        try:
            # 가능한 셀렉터들
            username_selectors = [
                (By.ID, "username"),
                (By.NAME, "username"),
                (By.ID, "email"),
                (By.NAME, "email"),
            ]

            found = False
            for selector_type, selector_value in username_selectors:
                try:
                    element = driver.find_element(selector_type, selector_value)
                    print(f"✅ Username 필드 발견: {selector_type}={selector_value}")
                    found = True
                    break
                except:
                    continue

            if not found:
                print("⚠️ Username 필드를 자동으로 찾지 못했습니다")
                print("   → 브라우저에서 직접 확인하고 src/wsop_scraper.py 수정 필요")

        except Exception as e:
            print(f"⚠️ 로그인 폼 감지 오류: {e}")

        print()
        print("🔍 브라우저를 닫기 전에 확인하세요:")
        print("   1. 로그인 필드가 보이나요?")
        print("   2. Username/Email 필드의 'id' 또는 'name' 속성은?")
        print("   3. Password 필드의 'id' 또는 'name' 속성은?")
        print()
        print("⏳ 20초 후 자동 종료됩니다...")

        time.sleep(20)

    finally:
        driver.quit()
        print("✅ 브라우저 종료")

    print()
    print("=" * 60)
    print("  테스트 완료")
    print("=" * 60)
    print()
    print("다음 단계:")
    print("1. 로그인 필드 정보를 확인했다면")
    print("2. src/wsop_scraper.py의 login_selectors 수정")
    print("3. python scripts/test_wsop_login.py 재실행")

except ImportError as e:
    print(f"❌ 모듈 import 실패: {e}")
    print()
    print("해결 방법:")
    print("pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ 예상치 못한 오류: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)