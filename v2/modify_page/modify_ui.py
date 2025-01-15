# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modify.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHeaderView,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_dataloader(object):
    def setupUi(self, dataloader):
        if not dataloader.objectName():
            dataloader.setObjectName(u"dataloader")
        dataloader.resize(800, 600)
        self.scrollArea = QScrollArea(dataloader)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(20, 20, 771, 571))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 769, 569))
        self.pushButton_4 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(400, 90, 111, 31))
        font = QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.tableWidget = QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 130, 571, 381))
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.radioButton = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(30, 20, 71, 31))
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(110, 20, 91, 31))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_3.setFont(font1)
        self.lineEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(210, 20, 301, 31))
        self.pushButton_5 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(530, 20, 93, 28))
        self.comboBox = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(650, 20, 83, 25))
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(620, 70, 121, 81))
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(620, 160, 121, 81))
        self.pushButton_2.setFont(font)
        self.pushButton_6 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(620, 250, 121, 81))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setKerning(True)
        self.pushButton_6.setFont(font2)
        self.pushButton_6.setAcceptDrops(False)
        self.pushButton_6.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_6.setAutoFillBackground(False)
        self.pushButton_3 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(170, 520, 251, 31))
        self.pushButton_3.setFont(font)
        self.pushButton_7 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(220, 90, 101, 31))
        self.pushButton_7.setFont(font)
        self.pushButton_8 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(40, 90, 101, 31))
        self.pushButton_8.setFont(font)
        self.pushButton_9 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(620, 340, 121, 81))
        self.pushButton_9.setFont(font2)
        self.pushButton_9.setAcceptDrops(False)
        self.pushButton_9.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_9.setAutoFillBackground(False)
        self.pushButton_10 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(620, 430, 121, 81))
        self.pushButton_10.setFont(font2)
        self.pushButton_10.setAcceptDrops(False)
        self.pushButton_10.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_10.setAutoFillBackground(False)
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(460, 520, 121, 31))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(dataloader)

        QMetaObject.connectSlotsByName(dataloader)
    # setupUi

    def retranslateUi(self, dataloader):
        dataloader.setWindowTitle(QCoreApplication.translate("dataloader", u"dataloader", None))
        self.pushButton_4.setText(QCoreApplication.translate("dataloader", u"\u64a4\u9500\u64cd\u4f5c", None))
        self.radioButton.setText(QCoreApplication.translate("dataloader", u"\u5168\u9009", None))
        self.label_3.setText(QCoreApplication.translate("dataloader", u"\u5173\u952e\u5b57\u641c\u7d22", None))
        self.pushButton_5.setText(QCoreApplication.translate("dataloader", u"\u67e5\u8be2", None))
        self.pushButton.setText(QCoreApplication.translate("dataloader", u"\u6570\u636e\u5e93\u9009\u62e9", None))
        self.pushButton_2.setText(QCoreApplication.translate("dataloader", u"\u65b0\u5efa\u6570\u636e\u5e93", None))
        self.pushButton_6.setText(QCoreApplication.translate("dataloader", u"\u6dfb\u52a0\u5f52\u7c7b", None))
        self.pushButton_3.setText(QCoreApplication.translate("dataloader", u"\u786e\u8ba4", None))
        self.pushButton_7.setText(QCoreApplication.translate("dataloader", u"\u5220\u9664\u9009\u4e2d", None))
        self.pushButton_8.setText(QCoreApplication.translate("dataloader", u"\u6dfb\u52a0", None))
        self.pushButton_9.setText(QCoreApplication.translate("dataloader", u"\u79fb\u52a8\u81f3", None))
        self.pushButton_10.setText(QCoreApplication.translate("dataloader", u"\u5f52\u7c7b\u7ba1\u7406", None))
        self.label.setText(QCoreApplication.translate("dataloader", u"\u5f53\u524d\u9009\u62e9\u6570\u636e\u5e93\uff1a", None))
    # retranslateUi

