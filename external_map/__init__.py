from PhiLia093.h import *

NAME_QQID_MAP = {
    'SmileFlyOv': 986561577,
    'anhui25': 3265356703,
    'luoan25': 3265356703,
    'BaoHuSB': 3484868850,
    'HERRSC': 1590947611
}

class Infinity:
    def __init__(self):
        pass
INFTY = INFINITY = Infinity()

class ExternalMapClient(QWebSocket):
    def __init__(self) -> None:
        super().__init__()
        self.binaryMessageReceived.connect(self.cuslot_on_binary_message_received)
        self.open(QUrl('ws://127.0.0.1:37370/external_map/receive/global'))
        self.emc_window = ExternalMapWindow()
        self.emc_window.show()
    def cuslot_on_binary_message_received(self, msg:QByteArray) -> None:
        try:
            _bytes = bytes(msg)
        except Exception:
            _bytes = msg.data() if hasattr(msg, 'data') else bytes(msg)
        if len(_bytes) < 24:
            return
        x, y, z, i, j, k = struct.unpack('>6i', _bytes[-24:])
        #name = _bytes[:-24].decode('utf-8', errors='ignore')
        #print(name)
        self.emc_window.update_test_player((x, y, z), (i, j, k))

class ExternalMapWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PhiLia093 - Minecraft External Map')
        self.setGeometry((1920 - 1280) // 2, (1080 - 720) // 2, 1280, 720)

        self.playericon = PlayerIcon(self, 'MnlSmile', 986561577)
        self.playericon.update_pos_pov((100, 100, 100), (100, 100, 100))
    def paintEvent(self, a0):
        return super().paintEvent(a0)
    def update_test_player(self, pos, pov):
        self.playericon.update_pos_pov(pos, pov)
    

class PlayerIcon(QWidget):
    def __init__(self, parent:QWidget, name:str='', qqid:int=0):
        super().__init__(parent)
        self.name = name
        self.qqid = qqid

        self.setGeometry(self.parent().width() // 2 - 35, self.parent().height() // 2 - 35, 70, 70) 
        self.pos:tuple[int, int, int] = (0, 0, 0)
        self.pov:tuple[int, int, int] = (0, 0, 1)
        self.rot = 0
    def update_pos_pov(self, pos:tuple[int, int, int], pov:tuple[int, int, int]) -> None:
        self.pos = pos
        x, _, z = pos
        self.pov = pov
        #self.move(round(x - self.width() / 2), round(z - self.height() / 2))
        self.move(round(x - self.width() / 2), round(z - self.height() / 2))
        self.update()
    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        pen.setColor(CYRENE_PINK)
        pen.setWidth(4)
        painter.setPen(pen)

        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        R = 16
        rect = QRect(-R, -R, R * 2, R * 2)
        painter.drawEllipse(rect)
        painter.restore()

        TR = -2 + 22
        triangle = QPolygon([QPoint(0, TR + 12), QPoint(-6, TR + 2), QPoint(6, TR + 2)])
        i, _, k = self.pov
        print(i, _, k)
        pov_length = math.hypot(i, k)
        if pov_length == 0:
            self.rot = 0.0# + 180
        else:
            self.rot = math.degrees(math.atan2(k, i))# + 180
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.rot)
        painter.setPen(pen)
        painter.drawPolygon(triangle)
        painter.restore()

        return super().paintEvent(a0)