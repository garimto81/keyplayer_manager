"""
세션 재사용 테스트
1차 실행: 로그인 + 세션 저장
2차 실행: 세션 재사용 (새 로그인 없음)
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent / "src"))

# UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

from dotenv import load_dotenv
from wsop_scraper import WSOPScraper

load_dotenv()

print("=" * 70)
print("  세션 재사용 테스트")
print("=" * 70)

# 세션 파일 경로
session_file = Path("session_cookies.pkl")

print(f"\n📁 세션 파일: {session_file}")
print(f"   존재 여부: {'✅ 있음' if session_file.exists() else '❌ 없음'}")

if session_file.exists():
    import pickle
    from datetime import datetime

    with open(session_file, 'rb') as f:
        data = pickle.load(f)
        last_login = datetime.fromisoformat(data['last_login'])
        age_hours = (datetime.now() - last_login).total_seconds() / 3600

    print(f"   저장 시간: {last_login:%Y-%m-%d %H:%M:%S}")
    print(f"   경과 시간: {age_hours:.1f}시간")

print("\n" + "-" * 70)

# 테스트 선택
print("\n테스트 옵션:")
print("  1. 첫 실행 (새 로그인 + 세션 저장)")
print("  2. 재실행 (세션 재사용, 로그인 생략)")
print("  3. 세션 삭제 후 재실행")

choice = input("\n선택 (1/2/3): ").strip()

if choice == "3":
    if session_file.exists():
        session_file.unlink()
        print("\n✅ 세션 파일 삭제 완료")
    else:
        print("\n⚠️ 삭제할 세션 파일이 없습니다")
    choice = "1"

print("\n" + "=" * 70)

# 스크래퍼 실행
try:
    scraper = WSOPScraper(download_path="downloads", session_file=str(session_file))

    print("\n[실행 시작]")
    scraper._setup_driver()

    print("\n[로그인 단계]")
    scraper.login()

    print("\n" + "=" * 70)
    if choice == "1":
        print("✅ 첫 실행 완료!")
        print("   → 세션이 저장되었습니다")
        print("   → 다음 실행 시 로그인 생략됩니다")
    else:
        print("✅ 재실행 완료!")
        print("   → 세션이 재사용되었는지 확인하세요")

    print("\n⏳ 브라우저를 10초간 열어둡니다 (결과 확인)")
    import time
    time.sleep(10)

except Exception as e:
    print(f"\n❌ 오류: {e}")
    import traceback
    traceback.print_exc()

finally:
    if scraper and scraper.driver:
        scraper.driver.quit()
        print("\n✓ 브라우저 종료")

print("\n" + "=" * 70)
print("테스트 완료")
print("=" * 70)