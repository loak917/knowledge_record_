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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_dataloader(object):
    def setupUi(self, dataloader):
        if not dataloader.objectName():
            dataloader.setObjectName(u"dataloader")
        dataloader.resize(800, 600)
        dataloader.setStyleSheet(u"QWidget {\n"
"    background-color: #ffffff;\n"
"    font-family: \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #333333;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    padding: 5px 10px;\n"
"    border: 1px solid #d0d0d0;\n"
"    border-radius: 4px;\n"
"    background-color: #ffffff;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4a9eff;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #4a9eff;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 5px 15px;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d8ee6;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2d7ed6;\n"
"}\n"
"\n"
"QComboBox {\n"
"    padding: 5px 10px;\n"
"    border: 1px solid #d0d0d0;\n"
"    border-radius: 4px;\n"
"    background-color: #ffffff;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #4a9eff;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    border:"
                        " 1px solid #d0d0d0;\n"
"    background-color: #ffffff;\n"
"    gridline-color: #e0e0e0;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #e6f3ff;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #f5f5f5;\n"
"    padding: 5px;\n"
"    border: none;\n"
"    border-right: 1px solid #d0d0d0;\n"
"    border-bottom: 1px solid #d0d0d0;\n"
"    font-weight: bold;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #f0f0f0;\n"
"    width: 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #c0c0c0;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #a0a0a0;\n"
"}")
        self.verticalLayout = QVBoxLayout(dataloader)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.topWidget = QWidget(dataloader)
        self.topWidget.setObjectName(u"topWidget")
        self.topWidget.setMinimumSize(QSize(0, 50))
        self.topWidget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.topWidget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.topWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.topWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(250, 35))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton_search = QPushButton(self.topWidget)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setMinimumSize(QSize(80, 35))

        self.horizontalLayout.addWidget(self.pushButton_search)

        self.comboBox = QComboBox(self.topWidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(120, 35))

        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_import = QPushButton(self.topWidget)
        self.pushButton_import.setObjectName(u"pushButton_import")
        self.pushButton_import.setMinimumSize(QSize(120, 35))

        self.horizontalLayout.addWidget(self.pushButton_import)

        self.pushButton_export = QPushButton(self.topWidget)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setMinimumSize(QSize(120, 35))
        self.pushButton_export.setStyleSheet(u"QPushButton {\n"
"    background-color: #67c23a;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #5daf34;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #529d2e;\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_export)


        self.verticalLayout.addWidget(self.topWidget)

        self.keywordsContainer = QWidget(dataloader)
        self.keywordsContainer.setObjectName(u"keywordsContainer")
        self.keywordsContainer.setMinimumSize(QSize(0, 30))
        self.keywordsContainer.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_2 = QHBoxLayout(self.keywordsContainer)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 2, 5, 2)

        self.verticalLayout.addWidget(self.keywordsContainer)

        self.tableWidget = QTableWidget(dataloader)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(dataloader)

        QMetaObject.connectSlotsByName(dataloader)
    # setupUi

    def retranslateUi(self, dataloader):
        dataloader.setWindowTitle(QCoreApplication.translate("dataloader", u"\u77e5\u8bc6\u5e93\u7ba1\u7406", None))
        self.label_3.setText(QCoreApplication.translate("dataloader", u"\u5173\u952e\u5b57\u641c\u7d22", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("dataloader", u"\u8bf7\u8f93\u5165\u5173\u952e\u5b57", None))
        self.pushButton_search.setText(QCoreApplication.translate("dataloader", u"\u67e5\u8be2", None))
        self.pushButton_import.setText(QCoreApplication.translate("dataloader", u"\u5bfc\u5165\u6570\u636e\u5e93", None))
        self.pushButton_export.setText(QCoreApplication.translate("dataloader", u"\u5bfc\u51fa\u6570\u636e", None))
    # retranslateUi

