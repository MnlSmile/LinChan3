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
        self.emc_window.update_test_player((x, y, z), (i, j), k)

class ExternalMapWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PhiLia093 - Minecraft External Map')
        self.setGeometry((1920 - 1280) // 2, (1080 - 720) // 2, 1280, 720)

        self.playericon = PlayerIcon(self, 'MnlSmile', 986561577)
        self.playericon.update_pos_pov((100, 100, 100), (100, 100), 0)
    def paintEvent(self, a0):
        return super().paintEvent(a0)
    def update_test_player(self, pos, pov, dim):
        self.playericon.update_pos_pov(pos, pov, dim)
    

class PlayerIcon(QWidget):
    def __init__(self, parent:QWidget, name:str='', qqid:int=0):
        super().__init__(parent)
        self.name = name
        self.qqid = qqid

        a = 100
        self.setGeometry((self.parent().width() - a) // 2, (self.parent().height() - a) // 2, a, a) 
        self.pos:tuple[int, int, int] = (0, 0, 0)
        self.pov:tuple[int, int] = (0, 0)  # degrees: [yaw, pitch]
        self.dim = 0
        self.rot = 0

        self.setObjectName("PlayerIcon")
        self.icon = QLabel(self)
        self.icon.setGeometry(self.width() // 2 - 16, self.height() // 2 - 16, 32, 32)
        self.icon.setScaledContents(True)
        img_path = 'D:\\python_works\\PhiLia093\\cache\\g.jpg'
        pix = QPixmap(str(img_path)).scaled(32, 32, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        size = 32
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
    def update_pos_pov(self, pos:tuple[int, int, int], pov:tuple[int, int], dim:int) -> None:
        self.pos = pos
        x, _, z = pos
        self.pov = pov
        self.dim = dim
        if self.dim != 0:  # only deal with overworld now
            self.hide()
            return
        else:
            self.show()
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
        R = 18
        rect = QRect(-R, -R, R * 2, R * 2)
        painter.drawEllipse(rect)
        painter.restore()

        TR = -2 + R + 8
        triangle = QPolygon([QPoint(0, TR + 12), QPoint(-6, TR + 2), QPoint(6, TR + 2)])
        i, j = self.pov
        #print(i, j, self.dim)
        self.rot = i
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.rot)
        painter.setPen(pen)
        painter.drawPolygon(triangle)
        painter.restore()

        return super().paintEvent(a0)