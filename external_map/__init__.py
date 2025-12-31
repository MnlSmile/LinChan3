from PhiLia093.h import *

_NAME_QQID_MAP = {
    'SmileFlyOv': 986561577,
    'anhui25': 3265356703,
    'luoan25': 3265356703,
    'BaoHuSB': 3484868850,
    'HERRSC': 1590947611
}
NAME_QQID_MAP = defaultdict(lambda:-1)
for k, v in _NAME_QQID_MAP.items():
    NAME_QQID_MAP[k] = v

DIVIDER = b'/'

exsisting_player = set()
exsisting_player_data = defaultdict()


class MainGuiCard(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        ...


class Infinity:
    def __init__(self):
        pass
INFTY = INFINITY = Infinity()


class ExternalMapClient(QWebSocket):
    def __init__(self) -> None:
        super().__init__()
        self.binaryMessageReceived.connect(self.cuslot_on_binary_message_received)
        self.open(QUrl('ws://47.119.20.145:37370/external_map/receive/global'))
        self.emc_window = ExternalMapWindow()
        self.connected.connect(lambda:self.emc_window.setWindowTitle('PhiLia093 - Minecraft External Map (Connected)'))
        self.disconnected.connect(lambda:self.emc_window.setWindowTitle('PhiLia093 - Minecraft External Map (Disonnected)'))
        self.emc_window.show()
    def reconnect(self) -> None:
        self.close()
        self.open(QUrl('ws://47.119.20.145:37370/external_map/receive/global'))
    def cuslot_on_binary_message_received(self, msg:QByteArray) -> None:
        global exsisting_player, exsisting_player_data
        try:
            _bytes = bytes(msg)
        except Exception:
            _bytes = msg.data() if hasattr(msg, 'data') else bytes(msg)
        if len(_bytes) < 28:
            return
        t, _pdata = _bytes[0:4], _bytes[4:]
        
        temp = set()  # to store player names and their data existed in server package
        try:
            for ba in _pdata.split(DIVIDER):
                pn = ba[:-24].decode('utf-8', errors='ignore')
                print(pn)
                temp.add(pn)
                exsisting_player_data[pn] = struct.unpack('>6i', ba[-24:])
            for pn in temp - exsisting_player:  # 服务器来数据有，但历史数据没有的玩家 要创建 PlayerIcon
                x, y, z, i, j, k = exsisting_player_data[pn]
                self.emc_window.create_player_icon(pn)
                self.emc_window.update_player_icon(pn, (x, y, z), (i, j), k)
            for pn in exsisting_player - temp:  # 历史数据有，但服务器来数据没有的玩家 要删除 PlayerIcon
                self.emc_window.delete_player_icon(pn)
            for pn in temp & exsisting_player:
                x, y, z, i, j, k = exsisting_player_data[pn]
                self.emc_window.update_player_icon(pn, (x, y, z), (i, j), k)
        except Exception as e:
            print_exception(e)
        exsisting_player = temp


class ExternalMapWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PhiLia093 - Minecraft External Map')
        self.setGeometry((1920 - 1280) // 2, (1080 - 720) // 2, 1280, 720)
        self.setFixedSize(self.width(), self.height())

        self.player_name_playericon_map = defaultdict(lambda:None)
    def create_player_icon(self, name:str) -> 'PlayerIcon':
        self.player_name_playericon_map[name] = PlayerIcon(self, name, NAME_QQID_MAP[name])
    def delete_player_icon(self, name:str) -> None:
        del self.player_name_playericon_map[name]
    def update_player_icon(self, name:str, *args) -> None:
        p:PlayerIcon = self.player_name_playericon_map[name]
        if p:
            p.update_pos_pov(*args)
        else:
            self.player_name_playericon_map[name] = PlayerIcon(self, name, NAME_QQID_MAP[name])
            self.player_name_playericon_map[name].update_pos_pov(*args)
    def paintEvent(self, a0):
        return super().paintEvent(a0)

class PlayerIcon(QWidget):
    AVATAR_SIZE = 32
    def __init__(self, parent:QWidget, name:str='', qqid:int=-1):
        super().__init__(parent)
        self.player_name = name
        self.qqid = qqid

        a = 100
        self.setGeometry((self.parent().width() - a) // 2, (self.parent().height() - a) // 2, a, a) 
        self.pos:tuple[int, int, int] = (0, 0, 0)
        self.pov:tuple[int, int] = (0, 0)  # degrees: [yaw, pitch]
        self.dim = 0
        self.rot = 0

        self.icon = QLabel(self)
        self.icon.setGeometry(self.width() // 2 - 16, self.height() // 2 - 16, PlayerIcon.AVATAR_SIZE, PlayerIcon.AVATAR_SIZE)
        self.icon.setScaledContents(True)

        self.setMouseTracking(True)

        self.pos_detail = QLabel()
        self.pos_detail.setStyleSheet("""
QLabel {
    border-bottom-left-radius: 3px;
    border-bottom-right-radius: 3px;
    border-top-right-radius: 3px;
    border-color: black;
    background-color: black;
    font-family: "汉仪旗黑 75S";
    font-size: 12px;
    color:white;
}
""")
        self.pos_detail.setGeometry(a + 4, a + 4, 50, 200)
        self.pos_detail.setAlignment(Qt.AlignCenter)
        
        if self.qqid == -1:
            self.try_load_icon(usedefault=True)
        else:
            self.try_load_icon()
    def set_qqid(self, qqid:int) -> None:
        self.qqid = qqid
    def try_load_icon(self, usedefault=False) -> None:
        size = PlayerIcon.AVATAR_SIZE
        if usedefault:
            pix = QPixmap(size, size)
            pix.fill(QColor(255, 255, 255))
        else:
            try:
                path = f".\\cache\\{self.qqid}.jpg"
                with open(path, 'rb') as f:
                    pass
                pix = QPixmap(path).scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            except Exception:
                self.try_download_icon(_apply_after_finish=True)
                try:
                    pix = QPixmap(f".\\cache\\{self.qqid}.jpg").scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                except Exception as e:
                    print_exception(e)
                    return
        circ = QPixmap(size, size)
        circ.fill(Qt.transparent)
        painter = QPainter(circ)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pix)
        painter.end()
        self.icon.setPixmap(circ)
        self.icon.setScaledContents(True)
    def try_download_icon(self, _apply_after_finish=False) -> None:
        def _dl():
            for i in range(5):
                try:
                    resp = requests.get(f"http://q1.qlogo.cn/g?b=qq&nk={self.qqid}&s=40")
                    with open(f"./cache/{self.qqid}.jpg", 'wb') as f:
                        f.write(resp.content)
                    break
                except Exception:
                    continue
            if _apply_after_finish:
                self.try_load_icon()
        t = Thread(target=_dl, daemon=True)
        t.start()
    def update_pos_pov(self, pos:tuple[int, int, int], pov:tuple[int, int], dim:int) -> None:
        self.pos = pos
        x, y, z = pos
        self.pov = pov
        self.dim = dim
        if self.dim != 0:  # only deal with overworld now
            self.hide()
            return
        else:
            self.show()

        if not self.pos_detail.isHidden():
            self.pos_detail.setText(f"{self.player_name}({x}, {y}, {z})")
        self.move(round(x - self.width() / 2), round(z - self.height() / 2))
        self.update()
    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        #pen.setColor(CYRENE_PINK)
        pen.setColor(TEST_RED)
        pen.setWidth(4)
        painter.setPen(pen)

        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        R = 19
        rect = QRect(-R, -R, R * 2, R * 2)
        painter.drawEllipse(rect)
        painter.restore()

        TR = -2 + R + 8
        triangle = QPolygon([QPoint(0, TR + 12), QPoint(-6, TR + 2), QPoint(6, TR + 2)])
        i, j = self.pov
        self.rot = i
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.rot)
        painter.setPen(pen)
        painter.drawPolygon(triangle)
        painter.restore()

        return super().paintEvent(a0)
    def event(self, ev:QEvent):
        match ev.type():
            case QEvent.HoverEnter:
                self.pos_detail.show()
                return True
            case QEvent.HoverLeave:
                self.pos_detail.hide()
                return True
        return super().event(ev)