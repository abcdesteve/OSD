# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QSizePolicy,
    QWidget)

class Ui_gui(object):
    def setupUi(self, gui):
        if not gui.objectName():
            gui.setObjectName(u"gui")
        gui.resize(25, 25)
        self.centralwidget = QWidget(gui)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_layout = QGridLayout()
        self.btn_layout.setObjectName(u"btn_layout")

        self.gridLayout.addLayout(self.btn_layout, 0, 0, 1, 1)

        gui.setCentralWidget(self.centralwidget)

        self.retranslateUi(gui)

        QMetaObject.connectSlotsByName(gui)
    # setupUi

    def retranslateUi(self, gui):
        gui.setWindowTitle(QCoreApplication.translate("gui", u"MainWindow", None))
    # retranslateUi

