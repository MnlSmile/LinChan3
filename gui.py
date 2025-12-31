"""
素材来源
米哈游/文本 https://www.mihoyo.com
小熊猫/图片 https://space.bilibili.com/391634082
"""

from PhiLia093.h import *

import qq_bind, remote_copy, external_map

class MainWindow(QWidget): ...

class Fonts():
    @staticmethod
    def initialize():
        fontdb = QtGui.QFontDatabase()
        _hyqh_55s_font_id = fontdb.addApplicationFont('./font/HYQiHei_55S.ttf')
        _hyqh_75s_font_id = fontdb.addApplicationFont('./font/HYQiHei_75S.ttf')

game = game_container_widget = container = external_map_window = o_em_btn = None
gc_protected_vars = []

def main():
    global game, game_container_widget, container, afkmonitor, gc_protected_vars, external_map_window, o_em_btn
    if not os.path.exists('./cache'):
        os.mkdir('cache')

    app = QApplication(sys.argv)
    Fonts.initialize()

    window = MainWindow()
    window.setWindowTitle('PhiLia093')
    try:
        with open('./global.css', 'r', encoding='utf-8') as f:
            css = f.read()
        window.setStyleSheet(css)
    except Exception:
        pass
    
    rcc = remote_copy.RemoteCopyClient()

    afkmonitor = remote_copy.AFKMonitor()

    o_em_btn = QPushButton(window)
    o_em_btn.setGeometry(100, 100, 300, 50)
    o_em_btn.setText('(Test)External Map')
    o_em_btn.setFont(font_hyqh_75(18))
    def _start_em():
        global external_map_window
        if not external_map_window:
            external_map_window = external_map.ExternalMapClient()
        else:
            external_map_window.emc_window.show()
            external_map_window.reconnect()
    o_em_btn.clicked.connect(_start_em)

    o_mc_btn = QPushButton(window)
    o_mc_btn.setGeometry(100, 180, 300, 50)
    o_mc_btn.setText('(Test)启动 Minecraft')
    o_mc_btn.setFont(font_hyqh_75(18))
    def _start_mc():
        try:
            subprocess.Popen('"./_uproc.exe"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
    o_mc_btn.clicked.connect(_start_mc)

    window.show()
    
    #qq_bind.user_qq_local_bind_business_flow()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())