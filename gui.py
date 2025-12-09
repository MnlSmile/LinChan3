"""
素材来源
米哈游/文本 https://www.mihoyo.com
小熊猫/图片 https://space.bilibili.com/391634082
"""

from PhiLia093.h import *

import qq_bind, remote_copy, picocat_keyoverride, external_map

class MainWindow(QWidget): ...

class Fonts():
    @staticmethod
    def initialize():
        fontdb = QtGui.QFontDatabase()
        _hyqh_55s_font_id = fontdb.addApplicationFont('./font/HYQiHei_55S.ttf')
        _hyqh_75s_font_id = fontdb.addApplicationFont('./font/HYQiHei_75S.ttf')

game = game_container_widget = container = external_map_window = None
gc_protected_vars = []

def main():
    global game, game_container_widget, container, afkmonitor, gc_protected_vars
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

    window.show()

    afkmonitor = remote_copy.AFKMonitor()

    gc_protected_vars += [picocat_keyoverride.start()]

    external_map_client = external_map.ExternalMapClient()
    
    #qq_bind.user_qq_local_bind_business_flow()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())