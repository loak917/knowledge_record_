# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_modify.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QTextEdit, QWidget)

class Ui_show_modify(object):
    def setupUi(self, show_modify):
        if not show_modify.objectName():
            show_modify.setObjectName(u"show_modify")
        show_modify.resize(800, 600)
        self.scrollArea = QScrollArea(show_modify)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 20, 131, 351))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 129, 349))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.title_edit = QLineEdit(show_modify)
        self.title_edit.setObjectName(u"title_edit")
        self.title_edit.setGeometry(QRect(150, 20, 641, 30))
        font = QFont()
        font.setPointSize(12)
        self.title_edit.setFont(font)
        self.category_combo = QComboBox(show_modify)
        self.category_combo.setObjectName(u"category_combo")
        self.category_combo.setGeometry(QRect(150, 60, 641, 30))
        self.category_combo.setFont(font)
        self.description_edit = QTextEdit(show_modify)
        self.description_edit.setObjectName(u"description_edit")
        self.description_edit.setGeometry(QRect(150, 100, 641, 481))
        self.description_edit.setFont(font)
        self.pushButton_3 = QPushButton(show_modify)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(20, 390, 101, 31))
        self.pushButton_3.setFont(font)
        self.pushButton_4 = QPushButton(show_modify)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 440, 101, 31))
        self.pushButton_4.setFont(font)
        self.pushButton = QPushButton(show_modify)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 500, 101, 31))
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(show_modify)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 550, 101, 31))
        self.pushButton_2.setFont(font)

        self.retranslateUi(show_modify)

        QMetaObject.connectSlotsByName(show_modify)
    # setupUi

    def retranslateUi(self, show_modify):
        show_modify.setWindowTitle(QCoreApplication.translate("show_modify", u"\u4fee\u6539\u8bb0\u5f55", None))
        self.title_edit.setPlaceholderText(QCoreApplication.translate("show_modify", u"\u8bf7\u8f93\u5165\u6807\u9898", None))
        self.description_edit.setPlaceholderText(QCoreApplication.translate("show_modify", u"\u8bf7\u8f93\u5165\u63cf\u8ff0", None))
        self.pushButton_3.setText(QCoreApplication.translate("show_modify", u"\u6dfb\u52a0\u56fe\u7247", None))
        self.pushButton_4.setText(QCoreApplication.translate("show_modify", u"\u5220\u9664\u56fe\u7247", None))
        self.pushButton.setText(QCoreApplication.translate("show_modify", u"\u4fdd\u5b58", None))
        self.pushButton_2.setText(QCoreApplication.translate("show_modify", u"\u5927\u6a21\u578b", None))
    # retranslateUi

