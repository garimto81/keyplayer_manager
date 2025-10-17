"""
초기 설정 도우미 스크립트
"""
import os
import sys
import shutil
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass


def setup_project():
    """프로젝트 초기 설정"""
    print("=" * 60)
    print("  Key Player Manager - 초기 설정")
    print("=" * 60)
    print()

    root = Path(__file__).parent

    # 1. .env 파일 생성
    env_file = root / ".env"
    env_example = root / ".env.example"

    if not env_file.exists() and env_example.exists():
        print("📝 [1/4] .env 파일 생성 중...")
        shutil.copy(env_example, env_file)
        print("✅ .env 파일 생성 완료")
        print("   ⚠️ .env 파일을 열어 실제 값으로 수정하세요!")
    else:
        print("✅ [1/4] .env 파일이 이미 존재합니다")

    # 2. 디렉토리 생성
    print("\n📁 [2/4] 필요한 디렉토리 생성 중...")
    dirs = ["downloads", "logs"]
    for dir_name in dirs:
        dir_path = root / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/ 생성")

    # 3. credentials.json 확인
    print("\n🔑 [3/4] Google API credentials 확인 중...")
    creds_file = root / "credentials.json"
    if not creds_file.exists():
        print("   ⚠️ credentials.json이 없습니다!")
        print("   📖 생성 방법:")
        print("      1. https://console.cloud.google.com/")
        print("      2. 프로젝트 생성 > API 및 서비스 > 사용 설정")
        print("      3. Google Sheets API, Google Drive API 활성화")
        print("      4. 서비스 계정 생성 > 키 생성 (JSON)")
        print("      5. 다운로드한 JSON 파일을 credentials.json으로 저장")
        print()
    else:
        print("   ✅ credentials.json 존재")

    # 4. 패키지 설치 안내
    print("\n📦 [4/4] Python 패키지 설치 안내")
    print("   다음 명령어를 실행하세요:")
    print("   ")
    print("   pip install -r requirements.txt")
    print()

    # 완료
    print("=" * 60)
    print("  초기 설정 완료!")
    print("=" * 60)
    print()
    print("📋 다음 단계:")
    print("   1. .env 파일 수정 (WSOP 로그인 정보)")
    print("   2. credentials.json 배치 (Google API)")
    print("   3. pip install -r requirements.txt")
    print("   4. python src/main.py 테스트")
    print()


if __name__ == "__main__":
    setup_project()