# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 648)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_layout = QHBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_container = QWidget(self.centralwidget)
        self.menu_container.setObjectName(u"menu_container")
        self.menu_container.setStyleSheet(u"background-color: #f0f0f0;")
        self.container_layout = QVBoxLayout(self.menu_container)
        self.container_layout.setSpacing(0)
        self.container_layout.setObjectName(u"container_layout")
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_scroll_area = QScrollArea(self.menu_container)
        self.menu_scroll_area.setObjectName(u"menu_scroll_area")
        self.menu_scroll_area.setMinimumSize(QSize(170, 0))
        self.menu_scroll_area.setMaximumSize(QSize(170, 16777215))
        self.menu_scroll_area.setFrameShape(QFrame.NoFrame)
        self.menu_scroll_area.setWidgetResizable(True)
        self.menu_widget = QWidget()
        self.menu_widget.setObjectName(u"menu_widget")
        self.menu_layout = QVBoxLayout(self.menu_widget)
        self.menu_layout.setSpacing(0)
        self.menu_layout.setObjectName(u"menu_layout")
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.hide_button = QPushButton(self.menu_widget)
        self.hide_button.setObjectName(u"hide_button")
        self.hide_button.setMinimumSize(QSize(0, 40))
        self.hide_button.setMaximumSize(QSize(16777215, 40))

        self.menu_layout.addWidget(self.hide_button)

        self.menu_scroll_area.setWidget(self.menu_widget)

        self.container_layout.addWidget(self.menu_scroll_area)


        self.main_layout.addWidget(self.menu_container)

        self.show_button = QPushButton(self.centralwidget)
        self.show_button.setObjectName(u"show_button")
        self.show_button.setMinimumSize(QSize(60, 40))
        self.show_button.setMaximumSize(QSize(60, 40))

        self.main_layout.addWidget(self.show_button)

        self.stacked_widget = QStackedWidget(self.centralwidget)
        self.stacked_widget.setObjectName(u"stacked_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stacked_widget.sizePolicy().hasHeightForWidth())
        self.stacked_widget.setSizePolicy(sizePolicy)

        self.main_layout.addWidget(self.stacked_widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8f6f\u4ef6\u4e3b\u754c\u9762", None))
        self.hide_button.setText(QCoreApplication.translate("MainWindow", u"<<<", None))
        self.show_button.setText(QCoreApplication.translate("MainWindow", u">>>", None))
    # retranslateUi

