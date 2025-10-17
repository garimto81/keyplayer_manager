"""
Export 버튼 찾기 대화형 테스트
페이지 소스를 분석하여 가능한 Export 버튼 찾기
"""
import os
import sys
import time
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

print("=" * 70)
print("  Export 버튼 찾기 테스트")
print("=" * 70)

username = os.getenv("WSOP_USERNAME")
password = os.getenv("WSOP_PASSWORD")
url = os.getenv("WSOP_URL")

driver = None

try:
    # Chrome 설정
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    print("\n[1/5] Chrome 드라이버 설정")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("  ✅ 준비 완료")

    # 로그인
    print("\n[2/5] WSOP 로그인")
    driver.get(url)
    time.sleep(2)

    username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)
    print(f"  ✅ 로그인 완료: {driver.current_url}")

    # 페이지 분석
    print("\n[3/5] 페이지 요소 분석")
    print("  ⏳ 페이지 로드 대기 중... (5초)")
    time.sleep(5)

    # 모든 버튼 찾기
    print("\n📋 페이지의 모든 버튼:")
    print("-" * 70)

    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\n총 <button> 태그: {len(buttons)}개")

    for i, btn in enumerate(buttons, 1):
        try:
            text = btn.text.strip()
            classes = btn.get_attribute("class")
            id_attr = btn.get_attribute("id")
            onclick = btn.get_attribute("onclick")
            is_visible = btn.is_displayed()

            if text or classes or id_attr:
                print(f"\n버튼 #{i}:")
                if text:
                    print(f"  텍스트: '{text}'")
                if id_attr:
                    print(f"  ID: {id_attr}")
                if classes:
                    print(f"  Class: {classes}")
                if onclick:
                    print(f"  onClick: {onclick[:50]}...")
                print(f"  표시 여부: {'✅ 보임' if is_visible else '❌ 숨김'}")

                # "export" 또는 "csv" 포함 시 하이라이트
                if text and ("export" in text.lower() or "csv" in text.lower()):
                    print("  🌟 *** Export/CSV 관련 버튼 발견! ***")

        except Exception as e:
            continue

    # 링크(a 태그)도 확인
    print("\n" + "=" * 70)
    print("\n📋 페이지의 모든 링크 (a 태그):")
    print("-" * 70)

    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\n총 <a> 태그: {len(links)}개")

    for i, link in enumerate(links, 1):
        try:
            text = link.text.strip()
            href = link.get_attribute("href")
            classes = link.get_attribute("class")
            is_visible = link.is_displayed()

            if text and ("export" in text.lower() or "csv" in text.lower()):
                print(f"\n링크 #{i}:")
                print(f"  텍스트: '{text}'")
                if href:
                    print(f"  Href: {href}")
                if classes:
                    print(f"  Class: {classes}")
                print(f"  표시 여부: {'✅ 보임' if is_visible else '❌ 숨김'}")
                print("  🌟 *** Export/CSV 관련 링크 발견! ***")

        except Exception as e:
            continue

    # 페이지 소스에서 검색
    print("\n" + "=" * 70)
    print("\n[4/5] 페이지 소스에서 'export' 키워드 검색")
    print("-" * 70)

    page_source = driver.page_source.lower()

    keywords = [
        "export player list",
        "export player",
        "export csv",
        "download csv",
        "export to csv"
    ]

    for keyword in keywords:
        if keyword in page_source:
            print(f"  ✅ '{keyword}' 발견!")

            # 주변 텍스트 추출
            idx = page_source.find(keyword)
            context_start = max(0, idx - 100)
            context_end = min(len(page_source), idx + 100)
            context = page_source[context_start:context_end]

            print(f"     주변 텍스트: ...{context}...")
        else:
            print(f"  ❌ '{keyword}' 없음")

    # 대기
    print("\n[5/5] 수동 확인")
    print("=" * 70)
    print("\n⏳ 브라우저를 60초간 열어둡니다")
    print("   → Export 버튼을 직접 찾아보세요")
    print("   → 버튼 우클릭 > 검사 > 정보 확인")
    print("   → 60초 후 자동 종료됩니다")
    print("\n" + "=" * 70)

    time.sleep(60)

    print("\n✅ 테스트 완료")

except Exception as e:
    print(f"\n❌ 오류: {e}")
    import traceback
    traceback.print_exc()

    if driver:
        print("\n⏳ 브라우저를 30초간 열어둡니다 (디버깅용)")
        time.sleep(30)

finally:
    if driver:
        driver.quit()
        print("\n✓ 브라우저 종료")