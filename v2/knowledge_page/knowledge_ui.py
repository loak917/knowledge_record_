# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'knowledge.ui'
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
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_dataloader(object):
    def setupUi(self, dataloader):
        if not dataloader.objectName():
            dataloader.setObjectName(u"dataloader")
        dataloader.resize(800, 600)
        self.scrollArea = QScrollArea(dataloader)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 10, 781, 591))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 779, 589))
        self.tableWidget = QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 90, 761, 491))
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 20, 91, 31))
        font = QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.lineEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(100, 20, 301, 31))
        self.pushButton_search = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setGeometry(QRect(410, 20, 93, 28))
        self.comboBox = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(530, 20, 83, 25))
        self.pushButton_import = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_import.setObjectName(u"pushButton_import")
        self.pushButton_import.setGeometry(QRect(630, 0, 121, 41))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setKerning(True)
        self.pushButton_import.setFont(font1)
        self.pushButton_import.setAcceptDrops(False)
        self.pushButton_import.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_import.setAutoFillBackground(False)
        self.pushButton_export = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setGeometry(QRect(630, 50, 121, 31))
        font2 = QFont()
        font2.setPointSize(12)
        self.pushButton_export.setFont(font2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(dataloader)

        QMetaObject.connectSlotsByName(dataloader)
    # setupUi

    def retranslateUi(self, dataloader):
        dataloader.setWindowTitle(QCoreApplication.translate("dataloader", u"dataloader", None))
        self.label_3.setText(QCoreApplication.translate("dataloader", u"\u5173\u952e\u5b57\u641c\u7d22", None))
        self.pushButton_search.setText(QCoreApplication.translate("dataloader", u"\u67e5\u8be2", None))
        self.pushButton_import.setText(QCoreApplication.translate("dataloader", u"\u5bfc\u5165\u6570\u636e\u5e93", None))
        self.pushButton_export.setText(QCoreApplication.translate("dataloader", u"\u5bfc\u51fa", None))
    # retranslateUi

