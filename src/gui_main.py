"""
GUI 진입점
FreeSimpleGUI 기반 데스크톱 애플리케이션
"""
import os
import sys
from pathlib import Path
import threading
import queue
from datetime import datetime

# 프로젝트 루트 경로 추가
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "src"))

import FreeSimpleGUI as sg
from gui.main_window import MainWindow
from main import KeyPlayerManager
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class GUIController:
    """GUI 컨트롤러 - GUI와 비즈니스 로직 연결"""

    def __init__(self):
        self.main_window = MainWindow()
        self.window = None
        self.manager = None
        self.running = False
        self.log_queue = queue.Queue()

        # 통계
        self.exec_count = 0
        self.csv_rows = 0
        self.key_players = 0

    def log(self, message):
        """로그 메시지를 큐에 추가 (스레드 안전)"""
        self.log_queue.put(message)

    def process_log_queue(self):
        """로그 큐 처리"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.main_window.append_log(message)
        except queue.Empty:
            pass

    def run_automation(self):
        """자동화 실행 (별도 스레드)"""
        self.running = True
        self.main_window.enable_run_button(False)
        self.main_window.enable_pause_button(True)
        self.main_window.update_status('실행 중...', 'green')
        self.main_window.update_progress(0)

        try:
            self.log("=" * 60)
            self.log("🚀 자동화 시작")
            self.log("=" * 60)

            # KeyPlayerManager 실행
            self.manager = KeyPlayerManager()

            # 진행 단계별 로그 및 진행바 업데이트
            self.log("📥 [1/3] WSOP CSV 다운로드 중...")
            self.main_window.update_progress(10)

            # 실제 실행 (main.py의 run 메서드 호출)
            # 로그를 GUI로 리다이렉트하기 위해 manager.log 메서드 오버라이드
            original_log = self.manager.log
            def gui_log(msg):
                self.log(msg)
                original_log(msg)
            self.manager.log = gui_log

            self.main_window.update_progress(30)

            # 스크래핑 실행
            from wsop_scraper import WSOPScraper
            scraper = WSOPScraper(download_path=os.getenv("DOWNLOAD_PATH", "downloads"))
            csv_file = scraper.run()

            self.log(f"✅ CSV 다운로드 완료: {csv_file}")
            self.main_window.update_progress(50)

            # CSV 행 수 카운트
            import pandas as pd
            df = pd.read_csv(csv_file)
            self.csv_rows = len(df)
            self.main_window.update_statistics(csv_rows=self.csv_rows)

            self.log("📤 [2/3] Google Sheets 업로드 중...")
            self.main_window.update_progress(60)

            # 시트 업로드
            from sheets_uploader import SheetsUploader
            uploader = SheetsUploader(credentials_path="credentials.json")
            uploader.upload_csv_to_type_sheet(csv_file)

            self.log("✅ Google Sheets 업로드 완료")
            self.main_window.update_progress(80)

            self.log("🔄 [3/3] Apps Script 트리거 대기")
            self.log("   → Time Trigger가 1분 이내 자동 실행합니다")
            self.main_window.update_progress(100)

            # 통계 업데이트
            self.exec_count += 1
            self.main_window.update_statistics(exec_count=self.exec_count)
            self.main_window.update_last_run(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            self.log("=" * 60)
            self.log("🎉 자동화 완료!")
            self.log("=" * 60)

            self.main_window.update_status('완료', 'cyan')

        except Exception as e:
            error_msg = f"❌ 오류 발생: {e}"
            self.log(error_msg)
            self.main_window.update_status('오류 발생', 'red')
            sg.popup_error(f'실행 오류\n\n{e}', title='오류')

        finally:
            self.running = False
            self.main_window.enable_run_button(True)
            self.main_window.enable_pause_button(False)
            self.main_window.update_status('대기 중', 'yellow')

    def handle_run_button(self):
        """실행 버튼 핸들러"""
        if not self.running:
            # 별도 스레드에서 실행 (GUI 블로킹 방지)
            thread = threading.Thread(target=self.run_automation, daemon=True)
            thread.start()

    def handle_wsop_config(self):
        """WSOP 설정 다이얼로그"""
        layout = [
            [sg.Text('WSOP 로그인 정보', font=('Arial', 12, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Text('Username:', size=(12, 1)),
             sg.Input(os.getenv('WSOP_USERNAME', ''), key='-USERNAME-', size=(30, 1))],
            [sg.Text('Password:', size=(12, 1)),
             sg.Input(os.getenv('WSOP_PASSWORD', ''), key='-PASSWORD-',
                     password_char='*', size=(30, 1))],
            [sg.Text('URL:', size=(12, 1)),
             sg.Input(os.getenv('WSOP_URL', ''), key='-URL-', size=(30, 1))],
            [sg.HorizontalSeparator()],
            [sg.Button('저장', key='-SAVE-'), sg.Button('취소', key='-CANCEL-')]
        ]

        dialog = sg.Window('WSOP 설정', layout, modal=True)

        while True:
            event, values = dialog.read()

            if event in (sg.WIN_CLOSED, '-CANCEL-'):
                break

            if event == '-SAVE-':
                # .env 파일 업데이트
                env_path = ROOT_DIR / '.env'

                # 기존 .env 읽기
                env_lines = []
                if env_path.exists():
                    with open(env_path, 'r', encoding='utf-8') as f:
                        env_lines = f.readlines()

                # WSOP 설정 업데이트
                wsop_keys = {
                    'WSOP_USERNAME': values['-USERNAME-'],
                    'WSOP_PASSWORD': values['-PASSWORD-'],
                    'WSOP_URL': values['-URL-']
                }

                # 새 env 내용 작성
                new_lines = []
                updated_keys = set()

                for line in env_lines:
                    key = line.split('=')[0] if '=' in line else None
                    if key in wsop_keys:
                        new_lines.append(f"{key}={wsop_keys[key]}\n")
                        updated_keys.add(key)
                    else:
                        new_lines.append(line)

                # 누락된 키 추가
                for key, value in wsop_keys.items():
                    if key not in updated_keys:
                        new_lines.append(f"{key}={value}\n")

                # 파일 쓰기
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

                sg.popup('설정이 저장되었습니다.', title='저장 완료')
                self.log('✅ WSOP 설정 업데이트 완료')
                break

        dialog.close()

    def handle_google_config(self):
        """Google API 설정 다이얼로그"""
        layout = [
            [sg.Text('Google API 설정', font=('Arial', 12, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Text('credentials.json 파일 선택:')],
            [sg.Input(str(ROOT_DIR / 'credentials.json'), key='-CREDS-', size=(40, 1)),
             sg.FileBrowse('찾아보기', file_types=(("JSON Files", "*.json"),))],
            [sg.HorizontalSeparator()],
            [sg.Text('SOURCE 스프레드시트 ID:', size=(20, 1))],
            [sg.Input(os.getenv('SOURCE_SPREADSHEET_ID', ''), key='-SOURCE-', size=(50, 1))],
            [sg.Text('TARGET 스프레드시트 ID:', size=(20, 1))],
            [sg.Input(os.getenv('TARGET_SPREADSHEET_ID', ''), key='-TARGET-', size=(50, 1))],
            [sg.HorizontalSeparator()],
            [sg.Button('저장', key='-SAVE-'), sg.Button('취소', key='-CANCEL-')]
        ]

        dialog = sg.Window('Google API 설정', layout, modal=True)

        while True:
            event, values = dialog.read()

            if event in (sg.WIN_CLOSED, '-CANCEL-'):
                break

            if event == '-SAVE-':
                # .env 업데이트
                env_path = ROOT_DIR / '.env'

                env_lines = []
                if env_path.exists():
                    with open(env_path, 'r', encoding='utf-8') as f:
                        env_lines = f.readlines()

                google_keys = {
                    'SOURCE_SPREADSHEET_ID': values['-SOURCE-'],
                    'TARGET_SPREADSHEET_ID': values['-TARGET-']
                }

                new_lines = []
                updated_keys = set()

                for line in env_lines:
                    key = line.split('=')[0] if '=' in line else None
                    if key in google_keys:
                        new_lines.append(f"{key}={google_keys[key]}\n")
                        updated_keys.add(key)
                    else:
                        new_lines.append(line)

                for key, value in google_keys.items():
                    if key not in updated_keys:
                        new_lines.append(f"{key}={value}\n")

                with open(env_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

                sg.popup('설정이 저장되었습니다.', title='저장 완료')
                self.log('✅ Google API 설정 업데이트 완료')
                break

        dialog.close()

    def handle_open_logs(self):
        """로그 폴더 열기"""
        logs_path = ROOT_DIR / 'logs'
        if not logs_path.exists():
            logs_path.mkdir(parents=True)

        import subprocess
        if sys.platform == 'win32':
            os.startfile(str(logs_path))
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', str(logs_path)])
        else:  # Linux
            subprocess.run(['xdg-open', str(logs_path)])

    def run(self):
        """메인 이벤트 루프"""
        self.window = self.main_window.create_window()
        self.main_window.append_log("🎰 Key Player Manager GUI v2.0 시작")
        self.main_window.append_log("=" * 60)

        while True:
            event, values = self.window.read(timeout=100)  # 100ms 타임아웃

            # 로그 큐 처리
            self.process_log_queue()

            if event in (sg.WIN_CLOSED, '-EXIT-'):
                if self.running:
                    response = sg.popup_yes_no(
                        '자동화가 실행 중입니다.\n정말 종료하시겠습니까?',
                        title='종료 확인'
                    )
                    if response == 'Yes':
                        break
                else:
                    break

            elif event == '-RUN-':
                self.handle_run_button()

            elif event == '-WSOP_CONFIG-':
                self.handle_wsop_config()

            elif event == '-GOOGLE_CONFIG-':
                self.handle_google_config()

            elif event == '-SCHEDULE_CONFIG-':
                sg.popup('스케줄 설정 기능은 곧 추가될 예정입니다.', title='개발 중')

            elif event == '-OPEN_LOGS-':
                self.handle_open_logs()

            elif event == '-VIEW_LOGS-':
                sg.popup('과거 로그 뷰어는 곧 추가될 예정입니다.', title='개발 중')

            elif event == '-AUTO-':
                if values['-AUTO-']:
                    sg.popup('자동 실행 기능은 곧 추가될 예정입니다.', title='개발 중')
                    self.window['-AUTO-'].update(False)

        self.window.close()


if __name__ == '__main__':
    controller = GUIController()
    controller.run()
