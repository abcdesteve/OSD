from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from gui_ui import Ui_gui
import sys
import os
import json
import qdarkstyle
import keyboard

WIDTH = 12
HEIGHT = 30


class QActionCheckBox(QAction):
    def __init__(self, txt: str, parent, func=None):
        super().__init__(
            txt, parent, triggered=(lambda: func(self.text()) if func else None)
        )
        self.setCheckable(True)


class QMenuWithRadioButtons(QMenu):
    def __init__(self, title: str, btns: list[str]):
        super().__init__(title)
        self.init_title = title
        self.items: dict[str, QAction] = {}
        for i in btns:
            self.items[i] = QActionCheckBox(i, self, func=self.update_check_state)
            self.addAction(self.items[i])
        self.setCurrentIndex(0)

    def update_check_state(self, item: str):
        if self.items[item].isChecked():
            for i in self.items.keys():
                if self.items[i].text() == item:
                    self.setTitle(f"{self.init_title}：{item}")
                    # self.items[i].setChecked(True)
                else:
                    self.items[i].setChecked(False)

    def currentIndex(self):
        for i in range(len(self.items)):
            text, item = list(self.items.keys())[i], list(self.items.values())[i]
            if item.isChecked():
                return list(self.items.keys()).index(text)

    def currentText(self):
        for i in range(len(self.items)):
            text, item = list(self.items.keys())[i], list(self.items.values())[i]
            if item.isChecked():
                return text

    def setCurrentIndex(self, index: int):
        key, value = list(self.items.items())[index]
        value.setChecked(True)
        self.update_check_state(key)

    def setCurrentText(self, text: str):
        self.items[text].setChecked(True)
        self.update_check_state(text)


class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icon.svg")))
        self.setup()
        self.read_settings()
        self.show()

    def setup(self):
        self.menu = QMenu()

        self.allow_repeat = QActionCheckBox("允许重复", self)
        self.menu.addAction(self.allow_repeat)

        self.animation_menu = QMenu("消失动画")
        self.animation_pos = QMenuWithRadioButtons("贴靠位置", ["上边缘", "下边缘", "左边缘", "右边缘"])
        self.animation_style = QMenuWithRadioButtons("动画效果", ["贴边隐藏", "渐隐"])
        self.animation_menu.addMenu(self.animation_pos)
        self.animation_menu.addMenu(self.animation_style)

        self.menu.addMenu(self.animation_menu)

        self.menu.addAction(QAction("退出", self, triggered=self.exit))
        self.setContextMenu(self.menu)

    def read_settings(self):
        path = os.path.expandvars(r"%appdata%/Avoconal/神龙OSD/settings.json")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.allow_repeat.setChecked(data["allow_repeat"])
                self.animation_pos.setCurrentText(data["animation"]["pos"])
                self.animation_style.setCurrentText(data["animation"]["style"])
        else:
            try:
                os.mkdir(os.path.expandvars(r"%appdata%/Avoconal"))
            except:
                pass
            try:
                os.mkdir(os.path.expandvars(r"%appdata%/Avoconal/神龙OSD"))
            except:
                pass
            self.save_settings()
            print("successfully created settings file")

    def save_settings(self):
        with open(
            os.path.expandvars(r"%appdata%/Avoconal/神龙OSD/settings.json"),
            "w",
            encoding="utf-8",
        ) as file:
            data = {
                "allow_repeat": self.allow_repeat.isChecked(),
                "animation": {
                    "pos": self.animation_pos.currentText(),
                    "style": self.animation_style.currentText(),
                },
            }
            json.dump(data, file)

    def exit(self):
        self.save_settings()
        app.exit()


class Main(QMainWindow, Ui_gui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            Qt.Drawer
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowDoesNotAcceptFocus
            | Qt.WindowOverridesSystemGestures
        )
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowOpacity(0.75)

        # animation init
        self.animation_pos = QPropertyAnimation(self, b"geometry")
        self.animation_pos.setDuration(500)
        self.animation_opacity = QPropertyAnimation(self, b"windowOpacity")
        self.animation_opacity.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation_opacity.setDuration(250)
        # hook init
        keyboard.on_press(self.add_key)

        # menu init
        self.tray = Tray()

        # show init notice
        QTimer.singleShot(
            500,
            lambda: QMetaObject.invokeMethod(
                self, "create_btn", Qt.QueuedConnection, Q_ARG(str, "神龙键盘显示已启动")
            ),
        )
        self.show()
        self.timer_change = QTimer()
        self.timer_change.start(250)
        self.timer_change.timeout.connect(self.change_try)

    def change_try(self):
        items = self.findChildren(QPushButton)
        cout = len(items)

        # pos animation
        if self.tray.animation_style.currentText() == "贴边隐藏":
            match self.tray.animation_pos.currentText():
                case "上边缘":
                    move_x, move_y = 0, -self.height()
                case "下边缘":
                    move_x, move_y = 0, self.height()
                case "左边缘":
                    move_x, move_y = -self.width(), 0
                case "右边缘":
                    move_x, move_y = self.width(), 0
        else:
            move_x, move_y = 0, 0

        if self.tray.animation_style.currentText() == "渐隐":
            # opacity animation
            self.animation_opacity.setStartValue(self.windowOpacity())
            self.animation_opacity.setEndValue(0.75 if cout else 0)
            self.animation_opacity.start()

        # move to side without hide
        screen_width = self.screen().size().width()
        screen_height = self.screen().size().height()
        self.animation_pos.setStartValue(
            QRect(self.x(), self.y(), self.width(), self.height())
        )
        match self.tray.animation_pos.currentText():
            case "上边缘":
                width = screen_width // 2 - self.width() // 2
                height = 0
            case "下边缘":
                width = screen_width // 2 - self.width() // 2
                height = screen_height - self.height()
            case "左边缘":
                width = 0
                height = screen_height // 2 - self.height() // 2
            case "右边缘":
                width = screen_width - self.width()
                height = screen_height // 2 - self.height() // 2
        is_x, is_y = self.tray.animation_pos.currentText() in [
            "上边缘",
            "下边缘",
        ], self.tray.animation_pos.currentText() in ["左边缘", "右边缘"]
        if cout:
            self.animation_pos.setEasingCurve(QEasingCurve.OutBack)
            self.animation_pos.setEndValue(
                QRect(
                    width,
                    height,
                    sum([i.width() for i in items] + [(WIDTH + 80) * (cout == 0)])
                    if is_x
                    else max([i.width() for i in items] + [WIDTH + 80]),
                    sum([i.height() for i in items] + [(HEIGHT) * (cout == 0)])
                    if is_y
                    else max([i.height() for i in items] + [HEIGHT]),
                )
            )
            # +[0] 防止列表为空sum报错
            # +[100] 使动画更明显
        else:
            self.animation_pos.setEasingCurve(QEasingCurve.InBack)
            self.animation_pos.setEndValue(
                QRect(
                    width + move_x,
                    height + move_y,
                    sum([i.width() for i in items] + [(WIDTH + 80) * (cout == 0)])
                    if is_x
                    else max([i.width() for i in items] + [WIDTH + 80]),
                    sum([i.height() for i in items] + [(HEIGHT) * (cout == 0)])
                    if is_y
                    else max([i.height() for i in items] + [HEIGHT]),
                )
            )
        self.animation_pos.start()

    def add_key(self, key: keyboard._keyboard_event.KeyboardEvent):
        QMetaObject.invokeMethod(
            self, "create_btn", Qt.QueuedConnection, Q_ARG(str, key.name)
        )

    @Slot(str)
    def create_btn(self, txt: str):
        if (
            not [i for i in self.findChildren(QPushButton) if i.text() == txt]
        ) or self.tray.allow_repeat.isChecked():
            btn = QPushButton(txt, self)

            # btn.setGeometry((len(self.findChildren(QPushButton))-1)
            #                 * WIDTH, 0, WIDTH, HEIGHT)
            # btn.show()

            btn.setFixedSize(WIDTH * len(txt) + 80, HEIGHT)
            btn.setFont(
                QFont(["Harmony OS Sans SC", "Microsoft YaHei UI", "Arial"], 15)
            )
            if self.tray.animation_pos.currentText() in ["上边缘", "下边缘"]:
                self.btn_layout_h.addWidget(btn)
            else:
                self.btn_layout_v.addWidget(btn)
            QTimer.singleShot(2000, btn.deleteLater)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet("pyside6"))
    win = Main()
    sys.exit(app.exec())
