# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QWidget)

class Ui_setting(object):
    def setupUi(self, setting):
        if not setting.objectName():
            setting.setObjectName(u"setting")
        setting.resize(800, 600)
        self.pushButton = QPushButton(setting)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(130, 40, 221, 101))
        font = QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(setting)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(450, 40, 221, 101))
        self.pushButton_2.setFont(font)
        self.pushButton_3 = QPushButton(setting)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(130, 190, 221, 101))
        self.pushButton_3.setFont(font)

        self.retranslateUi(setting)

        QMetaObject.connectSlotsByName(setting)
    # setupUi

    def retranslateUi(self, setting):
        setting.setWindowTitle(QCoreApplication.translate("setting", u"setting", None))
        self.pushButton.setText(QCoreApplication.translate("setting", u"\u5b57\u4f53\u8bbe\u7f6e", None))
        self.pushButton_2.setText(QCoreApplication.translate("setting", u"\u6570\u636e\u5e93\u7248\u672c\u8f6c\u6362", None))
        self.pushButton_3.setText(QCoreApplication.translate("setting", u"API\u5927\u6a21\u578b", None))
    # retranslateUi

