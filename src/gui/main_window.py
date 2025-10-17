"""
메인 윈도우 GUI 레이아웃
FreeSimpleGUI를 사용한 사용자 인터페이스
"""
import FreeSimpleGUI as sg
from datetime import datetime


class MainWindow:
    """메인 GUI 윈도우"""

    def __init__(self):
        # 테마 설정 (PySimpleGUI 5.0+)
        try:
            sg.theme('DarkBlue3')
        except AttributeError:
            # PySimpleGUI 5.0+에서는 테마 시스템이 변경됨
            pass

        # 윈도우 레이아웃
        self.layout = [
            # 타이틀
            [sg.Text('🎰 Key Player Manager', font=('Arial', 16, 'bold'),
                    justification='center', expand_x=True)],

            [sg.HorizontalSeparator()],

            # 상태 패널
            [sg.Frame('📊 상태', [
                [sg.Text('현재 상태:', size=(12, 1)),
                 sg.Text('대기 중', key='-STATUS-', size=(30, 1),
                        text_color='yellow')],
                [sg.Text('마지막 실행:', size=(12, 1)),
                 sg.Text('없음', key='-LAST_RUN-', size=(30, 1))],
                [sg.Text('다음 예정:', size=(12, 1)),
                 sg.Text('수동 실행 대기', key='-NEXT_RUN-', size=(30, 1))],
                [sg.ProgressBar(100, orientation='h', size=(50, 20),
                              key='-PROGRESS-', bar_color=('green', 'white'))]
            ], expand_x=True)],

            [sg.HorizontalSeparator()],

            # 제어 버튼
            [sg.Frame('⚙️ 제어', [
                [sg.Button('▶️ 지금 실행', key='-RUN-', size=(15, 1),
                          button_color=('white', 'green')),
                 sg.Button('⏸️ 일시정지', key='-PAUSE-', size=(15, 1),
                          disabled=True),
                 sg.Checkbox('🔄 자동 실행', key='-AUTO-',
                            enable_events=True, tooltip='자동 스케줄링 활성화')],
                [sg.Button('🔧 WSOP 설정', key='-WSOP_CONFIG-', size=(15, 1)),
                 sg.Button('📊 Google API 설정', key='-GOOGLE_CONFIG-', size=(15, 1)),
                 sg.Button('⏰ 스케줄 설정', key='-SCHEDULE_CONFIG-', size=(15, 1))]
            ], expand_x=True)],

            [sg.HorizontalSeparator()],

            # 로그 뷰어
            [sg.Frame('📝 실시간 로그', [
                [sg.Multiline('', size=(80, 15), key='-LOG-',
                             autoscroll=True, disabled=True,
                             background_color='black', text_color='white',
                             font=('Courier', 9))]
            ], expand_x=True, expand_y=True)],

            [sg.HorizontalSeparator()],

            # 통계 대시보드
            [sg.Frame('📈 오늘의 통계', [
                [sg.Text('실행 횟수:', size=(12, 1)),
                 sg.Text('0회', key='-EXEC_COUNT-', size=(10, 1)),
                 sg.Text('CSV 행 수:', size=(12, 1)),
                 sg.Text('0행', key='-CSV_ROWS-', size=(10, 1)),
                 sg.Text('Key Player:', size=(12, 1)),
                 sg.Text('0명', key='-KEY_PLAYERS-', size=(10, 1))]
            ], expand_x=True)],

            [sg.HorizontalSeparator()],

            # 하단 버튼
            [sg.Button('📂 로그 폴더 열기', key='-OPEN_LOGS-'),
             sg.Button('📄 과거 로그 보기', key='-VIEW_LOGS-'),
             sg.Push(),
             sg.Button('❌ 종료', key='-EXIT-', button_color=('white', 'red'))]
        ]

        self.window = None

    def create_window(self):
        """윈도우 생성"""
        self.window = sg.Window(
            'Key Player Manager v2.0',
            self.layout,
            size=(700, 750),
            resizable=True,
            finalize=True
        )
        return self.window

    def update_status(self, status, color='yellow'):
        """상태 업데이트"""
        if self.window:
            self.window['-STATUS-'].update(status, text_color=color)

    def update_last_run(self, timestamp):
        """마지막 실행 시간 업데이트"""
        if self.window:
            self.window['-LAST_RUN-'].update(timestamp)

    def update_next_run(self, next_time):
        """다음 예정 시간 업데이트"""
        if self.window:
            self.window['-NEXT_RUN-'].update(next_time)

    def update_progress(self, percent):
        """진행바 업데이트"""
        if self.window:
            self.window['-PROGRESS-'].update(percent)

    def append_log(self, message):
        """로그 추가"""
        if self.window:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            self.window['-LOG-'].print(log_message, end='')

    def update_statistics(self, exec_count=None, csv_rows=None, key_players=None):
        """통계 업데이트"""
        if self.window:
            if exec_count is not None:
                self.window['-EXEC_COUNT-'].update(f'{exec_count}회')
            if csv_rows is not None:
                self.window['-CSV_ROWS-'].update(f'{csv_rows}행')
            if key_players is not None:
                self.window['-KEY_PLAYERS-'].update(f'{key_players}명')

    def enable_pause_button(self, enable=True):
        """일시정지 버튼 활성화/비활성화"""
        if self.window:
            self.window['-PAUSE-'].update(disabled=not enable)

    def enable_run_button(self, enable=True):
        """실행 버튼 활성화/비활성화"""
        if self.window:
            self.window['-RUN-'].update(disabled=not enable)
