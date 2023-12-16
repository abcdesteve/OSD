from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui_gui import Ui_gui
import sys
import qdarkstyle
import keyboard

# KEY = ['win', 'ctrl', 'shift', 'alt', 'esc', 'enter', 'backspace', 'del','tab','caps lock','fn', 'up',
#        'down', 'left', 'right']+list(r'''abcdefghijklmnopqrstuvwxyz`-=[]\;',./''')
WIDTH = 100
HEIGHT = 30
ALLOW_REPEAT = False


class Main(QMainWindow, Ui_gui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.Drawer | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
                            Qt.WindowDoesNotAcceptFocus | Qt.WindowOverridesSystemGestures)
        self.setWindowOpacity(0.75)

        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(250)

        keyboard.on_press(self.add_key)

        QTimer.singleShot(500, lambda: QMetaObject.invokeMethod(
            self, "create_btn", Qt.QueuedConnection, Q_ARG(str, '神龙键盘显示已启动'), Q_ARG(int, 200)))
        self.show()
        self.timer_change = QTimer()
        self.timer_change.start(250)
        self.timer_change.timeout.connect(self.change_try)

    def change_try(self):
        cout = len(self.findChildren(QPushButton))
        # width = cout*WIDTH
        width=sum([i.width() for i in self.findChildren(QPushButton)])
        pos_x = self.screen().size().width()//2-width//2

        if cout:
            self.animation.setEasingCurve(QEasingCurve.OutBack)
            self.animation.setStartValue(
                QRect(self.x(), self.y(), self.width(), self.height()))
            self.animation.setEndValue(QRect(pos_x, 0, width, HEIGHT))
        else:
            self.animation.setEasingCurve(QEasingCurve.InBack)
            self.animation.setStartValue(
                QRect(self.x(), self.y(), self.width(), self.height()))
            self.animation.setEndValue(QRect(pos_x, -50, width, HEIGHT))
        self.animation.start()

    def add_key(self, key: keyboard._keyboard_event.KeyboardEvent):
        QMetaObject.invokeMethod(
            self, "create_btn", Qt.QueuedConnection, Q_ARG(str, key.name), Q_ARG(int, WIDTH))

    @Slot(str,int)
    def create_btn(self, txt: str, width: int):
        if (not [i for i in self.findChildren(QPushButton)if i.text() == txt]) or ALLOW_REPEAT:
            btn = QPushButton(txt, self)

            # btn.setGeometry((len(self.findChildren(QPushButton))-1)
            #                 * WIDTH, 0, WIDTH, HEIGHT)
            # btn.show()

            btn.setFixedSize(width, HEIGHT)
            btn.setFont(
                QFont(['Harmony OS Sans SC', 'Microsoft YaHei UI', 'Arial'], 15))
            self.btn_layout.addWidget(btn)
            QTimer.singleShot(2000, btn.deleteLater)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet('pyside6'))
    win = Main()
    sys.exit(app.exec())
