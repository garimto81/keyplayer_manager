"""
CSV 다운로드 테스트
로그인 → CSV Export 버튼 클릭 → 다운로드 확인
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
print("  CSV 다운로드 테스트")
print("=" * 70)

username = os.getenv("WSOP_USERNAME")
password = os.getenv("WSOP_PASSWORD")
url = os.getenv("WSOP_URL")
download_path = Path(os.getenv("DOWNLOAD_PATH", "downloads")).absolute()
download_path.mkdir(exist_ok=True)

print(f"\n다운로드 경로: {download_path}")

driver = None

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    # Chrome 설정
    chrome_options = Options()
    prefs = {
        "download.default_directory": str(download_path),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    print("\n[1/4] Chrome 드라이버 설정")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("  ✅ 준비 완료")

    # 로그인
    print("\n[2/4] WSOP 로그인")
    driver.get(url)
    time.sleep(2)

    username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)
    print(f"  ✅ 로그인 완료: {driver.current_url}")

    # Export 버튼 찾기
    print("\n[3/4] Export 버튼 탐색")

    export_selectors = [
        (By.XPATH, "//button[contains(text(), 'Export player list to csv')]"),
        (By.XPATH, "//button[contains(text(), 'Export player list')]"),
        (By.XPATH, "//button[contains(text(), 'Export')]"),
        (By.XPATH, "//a[contains(text(), 'Export player list to csv')]"),
        (By.XPATH, "//a[contains(text(), 'Export')]"),
        (By.CSS_SELECTOR, "button.export"),
        (By.CSS_SELECTOR, "a.export"),
        (By.CSS_SELECTOR, "[href*='export']"),
    ]

    export_button = None
    for selector_type, selector_value in export_selectors:
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.presence_of_element_located((selector_type, selector_value)))

            # 요소가 보이는지 확인
            if element.is_displayed():
                export_button = element
                print(f"  ✅ Export 버튼 발견!")
                print(f"     셀렉터: {selector_type}")
                print(f"     텍스트: '{element.text}'")
                break
        except Exception as e:
            continue

    if not export_button:
        print("  ❌ Export 버튼을 찾을 수 없습니다!")
        print("\n⏳ 브라우저를 30초간 열어둡니다 (수동 확인용)")
        print("   → Export 버튼을 직접 찾아보세요")
        print("   → 버튼 우클릭 > 검사 > id/class/text 확인")
        time.sleep(30)
        sys.exit(1)

    # 기존 CSV 파일 삭제
    print("\n  기존 CSV 파일 삭제...")
    for old_csv in download_path.glob("*.csv"):
        old_csv.unlink()
        print(f"    삭제: {old_csv.name}")

    # Export 버튼 클릭
    print("\n[4/4] CSV 다운로드 시도")

    # 버튼이 화면에 보이도록 스크롤
    driver.execute_script("arguments[0].scrollIntoView(true);", export_button)
    time.sleep(1)

    # 클릭 시도
    try:
        export_button.click()
        print("  ✅ Export 버튼 클릭 (일반 클릭)")
    except:
        # JavaScript 클릭 시도
        driver.execute_script("arguments[0].click();", export_button)
        print("  ✅ Export 버튼 클릭 (JavaScript)")

    # 다운로드 대기
    print("\n  ⏳ 다운로드 대기 중 (최대 30초)...")

    csv_file = None
    for i in range(30):
        time.sleep(1)

        # CSV 파일 확인 (.crdownload 제외)
        csv_files = [f for f in download_path.glob("*.csv") if not f.name.endswith('.crdownload')]

        if csv_files:
            csv_file = max(csv_files, key=lambda f: f.stat().st_mtime)
            print(f"\n  ✅ CSV 파일 다운로드 완료! ({i+1}초)")
            break

        # 진행 표시
        if (i + 1) % 5 == 0:
            print(f"    {i+1}초 경과...")

    if not csv_file:
        print("\n  ❌ CSV 파일 다운로드 실패 (타임아웃)")
        print("\n⏳ 브라우저를 20초간 열어둡니다")
        time.sleep(20)
        sys.exit(1)

    # 파일 정보
    print("\n" + "=" * 70)
    print("✅✅✅ CSV 다운로드 성공! ✅✅✅")
    print("=" * 70)
    print(f"\n파일 정보:")
    print(f"  - 파일명: {csv_file.name}")
    print(f"  - 경로: {csv_file}")
    print(f"  - 크기: {csv_file.stat().st_size:,} bytes")

    # CSV 내용 미리보기
    print(f"\n파일 내용 미리보기 (처음 5줄):")
    with open(csv_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            print(f"  {line.rstrip()}")

    print("\n⏳ 브라우저를 10초간 열어둡니다")
    time.sleep(10)

    print("\n🎉 테스트 완료!")
    sys.exit(0)

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