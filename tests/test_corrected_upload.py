"""
수정된 설계 테스트:
- CSV → TARGET 'type' 시트 업로드
- SOURCE 'Confirmed' 시트: Key Player 마스터 리스트 (수동 관리)
"""
import sys
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sheets_uploader import SheetsUploader


def main():
    print("=" * 60)
    print("수정된 설계 테스트: CSV → TARGET 'type' 시트")
    print("=" * 60)
    print()

    # 다운로드한 CSV 파일 경로
    csv_file = Path('downloads/Seats.csv')

    print(f"CSV 파일: {csv_file}")
    print(f"파일 존재: {csv_file.exists()}")
    print()

    if not csv_file.exists():
        print('❌ CSV 파일이 없습니다. 먼저 CSV 다운로드를 실행하세요.')
        print('   python src/wsop_scraper.py')
        return

    # Google Sheets 업로더 초기화
    print('Google Sheets 인증 중...')
    uploader = SheetsUploader('credentials.json')
    print()

    # TARGET 'type' 시트에 업로드
    print('TARGET "type" 시트에 업로드 중...')
    print('(SOURCE "Confirmed" 시트는 Key Player 마스터 리스트로 유지)')
    uploader.upload_csv_to_type_sheet(csv_file)

    print()
    print('✅ 업로드 완료!')
    print()
    print('시트 확인:')
    print('  - SOURCE (Key Player 마스터): https://docs.google.com/spreadsheets/d/1bGotri5sqcxt1H07QlU4lxV98m_he6i2NfZRHqfNaxg')
    print('  - TARGET (CSV 데이터 + 마킹): https://docs.google.com/spreadsheets/d/19e7eDjoZRFZooghZJF3XmOZzZcgmqsp9mFAfjvJWhj4')


if __name__ == '__main__':
    main()
