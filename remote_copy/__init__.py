from PhiLia093.h import *

global_timers = []

def restore_and_activate_window(hwnd):
    SW_RESTORE = 9
    windll.user32.ShowWindow(hwnd, SW_RESTORE)
    windll.user32.SetForegroundWindow(hwnd)

def set_cursor_pos(x, y):
    windll.user32.SetCursorPos(x, y)

def block_input(block:bool):
    windll.user32.BlockInput(block)

def lmb_click(hwnd:int, x:int, y:int) -> None:
    PostMessage(hwnd, WM_LBUTTONDOWN, 0, (y << 16) | x)
    PostMessage(hwnd, WM_LBUTTONUP, 0, (y << 16) | x)

class RemoteCopyClient(QWebSocket):
    def __init__(self) -> None:
        super().__init__()
        self.current_code:str = ''
        self.window = RemoteCopyWindow(self.current_code)
        self.textMessageReceived.connect(self.cuslot_on_text_message_received)
        self.open(QUrl('ws://47.119.20.145:52520/remote_copy'))
    def cuslot_on_text_message_received(self, msg:str) -> None:
        if self.window.is_angry_resize:
            self.window.o_btn.show()
            self.window.o_tip.setText(RECOVER_FROM_ANGER_TIP)
            self.window.o_code.move(20, 80)
            self.window.is_angry_resize = False
        elif self.window.o_tip.text()[0:2] == RECOVER_FROM_ANGER_TIP[0:2]:
            self.window.o_tip.setText(DEFAULT_TIP)
        def _set_code(code:str):
            game = FindWindow(None, 'Draw&Guess')
            if game:
                self.current_code = code
                self.window.code = code
                self.window.o_code.setText(code)
                self.window.show()
        with mccmd.Parser(msg) as parser:
            parser.resolve_overload_and_bind(
                {
                    ('/join', str): _set_code
                }
            )

class RemoteCopyWindow(QWidget):
    def __init__(self, code:str) -> None:
        super().__init__()      
        self.code = code
        self.is_angry_resize = False

        self.setGeometry(1920 - 400 - 20, 1080 - 200 - 70, 400, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('PhiLia093 - Draw & Guess Remote Copy')

        self.o_code = QLabel(self)
        self.o_code.setGeometry(20, 80, 400, 50)
        self.o_code.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.o_code.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.o_code.setFont(QFont('汉仪旗黑 75S', 27))
        self.o_code.setText(code)

        self.o_btn = QPushButton(self)
        self.o_btn.setGeometry(20, 75 + 50 + 10, 120, 50)
        self.o_btn.setFont(QFont('汉仪旗黑 55S', 18))
        self.o_btn.setText('拜托了!')
        self.o_btn.clicked.connect(self.code_inputing_flow)

        self.o_cyrene = QLabel(self)
        self.o_cyrene.setStyleSheet(
            "border-image: url(./cyrene_small_handback.png); background-color: transparent;"
        )
        self.o_cyrene.setGeometry(self.width() - 200 *2// 3, self.height() - 283 *2// 3, 200 *2// 3, 283 *2// 3)

        self.o_tip = QLabel(self)
        self.o_tip.setGeometry(20, 15, 400, 100)
        self.o_tip.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.o_tip.setFont(font_hyqh_55(18))
        self.o_tip.setText(DEFAULT_TIP)
    def resizeEvent(self, a0):
        global global_timers
        if (a0.oldSize().width(), a0.oldSize().height()) != (-1, -1) and (a0.size().width(), a0.size().height()) != (400, 200):
            if not self.is_angry_resize:
                self.o_tip.setText(ANGRY_1_TIP)
                self.o_code.move(self.o_btn.pos())
                self.o_btn.hide()
            self.is_angry_resize = True
            recover_size_timer = QTimer(self)
            global_timers += [recover_size_timer]
            def _recover():
                nonlocal recover_size_timer
                self.resize(400, 200)
                recover_size_timer.stop()
                if recover_size_timer in global_timers:
                    global_timers.remove(recover_size_timer)
                del recover_size_timer
            recover_size_timer.timeout.connect(_recover)
            recover_size_timer.setSingleShot(True)
            recover_size_timer.start(1000)
        return super().resizeEvent(a0)
    def code_inputing_flow(self) -> None:
        def _thread():
            block_input(True)
            try:
                game = FindWindow(None, 'Draw&Guess')
                if game:
                    restore_and_activate_window(game)
                    if re.search(r'^[a-zA-Z]{4}$', self.code):
                        op1 = (476, 320)
                        op2 = (784, 480)
                        x1, y1, x2, y2 = GetWindowRect(game)
                        dx = abs(x2 - x1)
                        dy = abs(y2 - y1)
                        p1 = (int(dx * (op1[0] / 1280)), int(dy * (op1[1] / 720)))
                        p2 = (int(dx * (op2[0] / 1280)), int(dy * (op2[1] / 720)))
                        p1_lparam = (p1[1] << 16) | p1[0]
                        p2_lparam = (p2[1] << 16) | p2[0]
                        
                        set_cursor_pos(x1 + p1[0], y1 + p1[1])
                        PostMessage(game, WM_LBUTTONDOWN, 0, p1_lparam)
                        PostMessage(game, WM_LBUTTONUP, 0, p1_lparam)
                        time.sleep(0.1)
                        PostMessage(game, WM_LBUTTONDOWN, 0, p1_lparam)
                        PostMessage(game, WM_LBUTTONUP, 0, p1_lparam)
                        time.sleep(0.5)

                        set_cursor_pos(x1 + p2[0], y1 + p2[1])
                        PostMessage(game, WM_LBUTTONDOWN, 0, p2_lparam)
                        PostMessage(game, WM_LBUTTONUP, 0, p2_lparam)
                        time.sleep(0.5)
                        PostMessage(game, WM_LBUTTONDOWN, 0, p2_lparam)
                        PostMessage(game, WM_LBUTTONUP, 0, p2_lparam)
                        time.sleep(0.1)
                        
                        for char in self.code:
                            PostMessage(game, WM_CHAR, ord(char.upper()), 0)
                        time.sleep(0.2)
                        SendMessage(game, WM_KEYDOWN, VK_RETURN, 0)
                        SendMessage(game, WM_KEYUP, VK_RETURN, 0)
            finally:
                block_input(False)
        Thread(target=_thread).start()

class AFKMonitor(QFile):
    def __init__(self) -> None:
        super().__init__(LOG_PATH)
        if not self.open(QIODevice.ReadOnly | QIODevice.Text):
            print('File open failed')
            return
        self.seek(self.size())
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_latest_line)
        self.timer.setInterval(250)
        self.timer.start()

        self.alarm_window = NormalAlarmWindow('伙伴, 该回来猜词了!')
    def check_latest_line(self) -> None:
        game = FindWindow(None, 'Draw&Guess')
        if game:
            self.timer.setInterval(250)
            example = "[22:06:09.368][DG][MnlSmile][Debug] [Round 1] Transitioning from 'Drawing' to 'Guessing'\n"
            line = self.readLine().data().decode('utf-8')
            if re.search(r"^\[\d{2}:\d{2}:\d{2}\.\d{3}\]\[DG\]\[.*\]\[Debug\] \[Round \d+\] Transitioning from 'Drawing' to 'Guessing'\n*$", line):
                if GetForegroundWindow() != game:
                    self.alarm_window.show()
                    SetForegroundWindow(game)
        else:
            self.timer.setInterval(2500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RemoteCopyWindow('ABCD')
    window.show()
    app.exec()