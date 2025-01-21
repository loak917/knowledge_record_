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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

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
"QPushButton:disabled {\n"
"    background-color: #cccccc;\n"
"    color: #666666;\n"
"}\n"
"\n"
"/* \u53f3\u4fa7\u529f\u80fd\u6309\u94ae\u7ec4\u7684\u7279\u6b8a\u6837\u5f0f */\n"
"#pushButton, #pushButton_2, #pushButton_6, #pushButton_9, #pushButton_10 {\n"
"    background-c"
                        "olor: #67c23a;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#pushButton:hover, #pushButton_2:hover, #pushButton_6:hover, #pushButton_9:hover, #pushButton_10:hover {\n"
"    background-color: #5daf34;\n"
"}\n"
"\n"
"#pushButton:pressed, #pushButton_2:pressed, #pushButton_6:pressed, #pushButton_9:pressed, #pushButton_10:pressed {\n"
"    background-color: #529d2e;\n"
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
"    border: 1px solid #d0d0d0;\n"
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
""
                        "    border: none;\n"
"    border-right: 1px solid #d0d0d0;\n"
"    border-bottom: 1px solid #d0d0d0;\n"
"    font-weight: bold;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: #333333;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    border: 2px solid #d0d0d0;\n"
"    border-radius: 9px;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid #4a9eff;\n"
"    border-radius: 9px;\n"
"    background-color: #4a9eff;\n"
"}\n"
"\n"
"/* \u64cd\u4f5c\u6309\u94ae\u7ec4\u7684\u7279\u6b8a\u6837\u5f0f */\n"
"#pushButton_4, #pushButton_7, #pushButton_8 {\n"
"    background-color: #f56c6c;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"#pushButton_4:hover, #pushButton_7:hover, #pushButton_8:hover {\n"
"    background-color: #e45c5c;\n"
"}\n"
"\n"
"#pushButton_4:pressed, #pushButton_7:pressed, #pushButton_8:pressed {\n"
"    background-colo"
                        "r: #d44c4c;\n"
"}\n"
"\n"
"/* \u786e\u8ba4\u6309\u94ae\u7684\u7279\u6b8a\u6837\u5f0f */\n"
"#pushButton_3 {\n"
"    background-color: #409eff;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#pushButton_3:hover {\n"
"    background-color: #3d8ee6;\n"
"}\n"
"\n"
"#pushButton_3:pressed {\n"
"    background-color: #2d7ed6;\n"
"}\n"
"\n"
"/* \u67e5\u8be2\u6309\u94ae\u7684\u7279\u6b8a\u6837\u5f0f */\n"
"#pushButton_5 {\n"
"    background-color: #909399;\n"
"}\n"
"\n"
"#pushButton_5:hover {\n"
"    background-color: #808285;\n"
"}\n"
"\n"
"#pushButton_5:pressed {\n"
"    background-color: #707275;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(dataloader)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.topWidget = QWidget(dataloader)
        self.topWidget.setObjectName(u"topWidget")
        self.verticalLayout_2 = QVBoxLayout(self.topWidget)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton = QRadioButton(self.topWidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setMinimumSize(QSize(60, 35))

        self.horizontalLayout.addWidget(self.radioButton)

        self.label_3 = QLabel(self.topWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 35))

        self.horizontalLayout.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.topWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(200, 35))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton_5 = QPushButton(self.topWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(80, 35))

        self.horizontalLayout.addWidget(self.pushButton_5)

        self.comboBox = QComboBox(self.topWidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(120, 35))

        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_8 = QPushButton(self.topWidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setMinimumSize(QSize(100, 35))

        self.horizontalLayout.addWidget(self.pushButton_8)

        self.pushButton_7 = QPushButton(self.topWidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(100, 35))

        self.horizontalLayout.addWidget(self.pushButton_7)

        self.pushButton_4 = QPushButton(self.topWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(100, 35))

        self.horizontalLayout.addWidget(self.pushButton_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.topWidget)

        self.contentWidget = QWidget(dataloader)
        self.contentWidget.setObjectName(u"contentWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.contentWidget)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.contentWidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        self.horizontalLayout_3.addWidget(self.tableWidget)

        self.rightButtonLayout = QVBoxLayout()
        self.rightButtonLayout.setSpacing(10)
        self.rightButtonLayout.setObjectName(u"rightButtonLayout")
        self.pushButton = QPushButton(self.contentWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(120, 80))

        self.rightButtonLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.contentWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(120, 80))

        self.rightButtonLayout.addWidget(self.pushButton_2)

        self.pushButton_6 = QPushButton(self.contentWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(120, 80))

        self.rightButtonLayout.addWidget(self.pushButton_6)

        self.pushButton_9 = QPushButton(self.contentWidget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setMinimumSize(QSize(120, 80))

        self.rightButtonLayout.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.contentWidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setMinimumSize(QSize(120, 80))

        self.rightButtonLayout.addWidget(self.pushButton_10)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightButtonLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.rightButtonLayout)


        self.verticalLayout.addWidget(self.contentWidget)

        self.bottomWidget = QWidget(dataloader)
        self.bottomWidget.setObjectName(u"bottomWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.bottomWidget)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.bottomWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.pushButton_3 = QPushButton(self.bottomWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(100, 35))
        self.pushButton_3.setMaximumSize(QSize(100, 35))

        self.horizontalLayout_4.addWidget(self.pushButton_3)


        self.verticalLayout.addWidget(self.bottomWidget)


        self.retranslateUi(dataloader)

        QMetaObject.connectSlotsByName(dataloader)
    # setupUi

    def retranslateUi(self, dataloader):
        dataloader.setWindowTitle(QCoreApplication.translate("dataloader", u"\u77e5\u8bc6\u5e93\u4fee\u6539", None))
        self.radioButton.setText(QCoreApplication.translate("dataloader", u"\u5168\u9009", None))
        self.label_3.setText(QCoreApplication.translate("dataloader", u"\u5173\u952e\u5b57\u641c\u7d22", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("dataloader", u"\u8bf7\u8f93\u5165\u5173\u952e\u5b57", None))
        self.pushButton_5.setText(QCoreApplication.translate("dataloader", u"\u67e5\u8be2", None))
        self.pushButton_8.setText(QCoreApplication.translate("dataloader", u"\u6dfb\u52a0", None))
        self.pushButton_7.setText(QCoreApplication.translate("dataloader", u"\u5220\u9664\u9009\u4e2d", None))
        self.pushButton_4.setText(QCoreApplication.translate("dataloader", u"\u64a4\u9500\u64cd\u4f5c", None))
        self.pushButton.setText(QCoreApplication.translate("dataloader", u"\u6570\u636e\u5e93\u9009\u62e9", None))
        self.pushButton_2.setText(QCoreApplication.translate("dataloader", u"\u65b0\u5efa\u6570\u636e\u5e93", None))
        self.pushButton_6.setText(QCoreApplication.translate("dataloader", u"\u6dfb\u52a0\u5f52\u7c7b", None))
        self.pushButton_9.setText(QCoreApplication.translate("dataloader", u"\u79fb\u52a8\u81f3", None))
        self.pushButton_10.setText(QCoreApplication.translate("dataloader", u"\u5f52\u7c7b\u7ba1\u7406", None))
        self.label.setText(QCoreApplication.translate("dataloader", u"\u5f53\u524d\u9009\u62e9\u6570\u636e\u5e93\uff1a", None))
        self.pushButton_3.setText(QCoreApplication.translate("dataloader", u"\u786e\u8ba4", None))
    # retranslateUi

