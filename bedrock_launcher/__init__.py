from PhiLia093.h import *
import winreg as reg
import os

STARTMENU_PATH = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Minecraft.lnk'

REG_PARENT_KEY = 'SOFTWARE\\WOW6432Node\\Microsoft\\SecurityManager\\CapAuthz\\ApplicationsEx'
REG_GAME_SUBKEY = 'MICROSOFT.MINECRAFTUWP_1.21.13101.0_x64__8wekyb3d8bbwe'

def is_regkey_exist(pkey:str, subkey:str='', hkey=reg.HKEY_LOCAL_MACHINE) -> bool:
    try:
        parent_key = reg.OpenKey(hkey, pkey)
        
        if not subkey: return True

        try:
            i = 0
            while True:
                name = reg.EnumKey(parent_key, i)
                if name == subkey:
                    reg.CloseKey(parent_key)
                    return True
                i += 1
        except OSError:
            reg.CloseKey(parent_key)
            return False
            
    except WindowsError:
        return False

def launching_flow(launch_patched:bool=False, use_new_qapp:bool=False) -> None:
    global gc_protected
    if use_new_qapp:
        app = QApplication(sys.argv)

    window = QWidget()
    gc_protect(window)
    screen_size = QGuiApplication.primaryScreen().size()

    window.setFixedSize(screen_size)
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    o_bg_lb = QLabel(window)
    o_bg_lb.setFixedSize(screen_size)
    pix = QPixmap(screen_size)
    pix.fill(CYRENE_PINK)
    o_bg_lb.setPixmap(pix)

    sw, sh = screen_size.width(), screen_size.height()
    o_process_tip_lb = QLabel(window)
    o_process_tip_lb.setGeometry(0, int(sh * 0.7), sw, int(sh * 0.15))
    o_process_tip_lb.setAlignment(Qt.AlignCenter)
    o_process_tip_lb.setFont(font_hyqh_75())

    window.showFullScreen()

    def _flow():
        nonlocal window, o_process_tip_lb

        def update_tip(tip:str):
            o_process_tip_lb.setText(tip)
        is_game_installed = False
        update_tip('伙伴安装好游戏了没有?')
        if os.path.exists(STARTMENU_PATH):
            is_game_installed = True
        elif is_regkey_exist(REG_PARENT_KEY, REG_GAME_SUBKEY):
            is_game_installed = True
        qel_sleep(2500)
        if is_game_installed:
            update_tip('找到了!')
        else:
            update_tip('好像...没有?')
        """
        else:
            window.close()
            cancle_gc_protect(window)
            alw = AlarmWindow('Cound not find a valid Minecraft Bedrock Edition installation.')
            gc_protect(alw)
            def _rm_gcp(ev:QEvent):
                cancle_gc_protect(alw)
                return ev.accept()
            alw.alarm_window.closeEvent = _rm_gcp
        """
        qel_sleep(1000)
        update_tip('尝试联系 Prev 分桃...')
        is_prev_exist = False
        qel_sleep(1500)
        update_tip('嗨, PhiLia Prev, 你在吗?')
        if is_regkey_exist('mcappx-minecraft', hkey=reg.HKEY_CLASSES_ROOT):
            for i in range(ord('C'), ord('Z') + 1):
                path = f"{chr(i)}:\\PhiLia093Prev\\PhiLia093TemporaryLauncher.exe"
                if os.path.exists(path):
                    is_prev_exist = True
                    break
                else:
                    continue
        else:
            is_prev_exist = False
        qel_sleep(1500)
        if is_prev_exist:
            update_tip('PhiLia093 Prev: 我在!')
            qel_sleep(1000)
            update_tip('PhiLia093 Prev: 接下来就交给我吧!')
            qel_sleep(500)
            try:
                subprocess.Popen(f"{path}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                for check_cnt in range(120):
                    if game := FindWindow(None, 'Minecraft'):
                        update_tip('PhiLia093 Prev: 好啦~')
                        break
                    qel_sleep(1000)
                qel_sleep(3000)
                window.close()
                cancle_gc_protect(window)
            except:
                update_tip('好像不太顺利呢...我只能帮你到这里了哦, 伙伴?')
        else:
            update_tip('PhiLia Prev 不在呢...只能试试强行开启了?')
            try:
                subprocess.Popen(f"open mcappx-minecraft://?", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                update_tip('盲启也失败了...我只能帮你到这里了哦, 伙伴?')
            finally:
                qel_sleep(3000)
                window.close()
                cancle_gc_protect(window)

    if use_new_qapp:
        _t = Thread(target=_flow, daemon=True)
        _t.start()
        sys.exit(app.exec())
    else:
        _flow()