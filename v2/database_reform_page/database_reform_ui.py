# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'database_reform.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_database_reform(object):
    def setupUi(self, database_reform):
        if not database_reform.objectName():
            database_reform.setObjectName(u"database_reform")
        database_reform.resize(800, 600)
        self.verticalLayout = QVBoxLayout(database_reform)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(database_reform)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit_db_path = QLineEdit(database_reform)
        self.lineEdit_db_path.setObjectName(u"lineEdit_db_path")
        self.lineEdit_db_path.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_db_path)

        self.pushButton_select_db = QPushButton(database_reform)
        self.pushButton_select_db.setObjectName(u"pushButton_select_db")

        self.horizontalLayout.addWidget(self.pushButton_select_db)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(database_reform)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label_db_name = QLabel(self.groupBox)
        self.label_db_name.setObjectName(u"label_db_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_db_name)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.comboBox_current_version = QComboBox(self.groupBox)
        self.comboBox_current_version.addItem("")
        self.comboBox_current_version.addItem("")
        self.comboBox_current_version.setObjectName(u"comboBox_current_version")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_current_version)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(database_reform)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.comboBox_target_version = QComboBox(self.groupBox_2)
        self.comboBox_target_version.addItem("")
        self.comboBox_target_version.addItem("")
        self.comboBox_target_version.setObjectName(u"comboBox_target_version")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comboBox_target_version)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_save_path = QLineEdit(self.groupBox_2)
        self.lineEdit_save_path.setObjectName(u"lineEdit_save_path")
        self.lineEdit_save_path.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_save_path)

        self.pushButton_select_save_path = QPushButton(self.groupBox_2)
        self.pushButton_select_save_path.setObjectName(u"pushButton_select_save_path")

        self.horizontalLayout_2.addWidget(self.pushButton_select_save_path)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.textEdit_log = QTextEdit(database_reform)
        self.textEdit_log.setObjectName(u"textEdit_log")
        self.textEdit_log.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit_log)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_start = QPushButton(database_reform)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.horizontalLayout_3.addWidget(self.pushButton_start)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(database_reform)

        QMetaObject.connectSlotsByName(database_reform)
    # setupUi

    def retranslateUi(self, database_reform):
        database_reform.setWindowTitle(QCoreApplication.translate("database_reform", u"\u6570\u636e\u5e93\u7248\u672c\u8f6c\u6362", None))
        self.label.setText(QCoreApplication.translate("database_reform", u"\u6570\u636e\u5e93\u6587\u4ef6\uff1a", None))
        self.lineEdit_db_path.setPlaceholderText(QCoreApplication.translate("database_reform", u"\u8bf7\u9009\u62e9\u8981\u8f6c\u6362\u7684\u6570\u636e\u5e93\u6587\u4ef6", None))
        self.pushButton_select_db.setText(QCoreApplication.translate("database_reform", u"\u9009\u62e9\u6587\u4ef6", None))
        self.groupBox.setTitle(QCoreApplication.translate("database_reform", u"\u6570\u636e\u5e93\u4fe1\u606f", None))
        self.label_2.setText(QCoreApplication.translate("database_reform", u"\u6570\u636e\u5e93\u540d\u79f0\uff1a", None))
        self.label_db_name.setText(QCoreApplication.translate("database_reform", u"\u672a\u9009\u62e9", None))
        self.label_3.setText(QCoreApplication.translate("database_reform", u"\u5f53\u524d\u7248\u672c\uff1a", None))
        self.comboBox_current_version.setItemText(0, "")
        self.comboBox_current_version.setItemText(1, "")

        self.groupBox_2.setTitle(QCoreApplication.translate("database_reform", u"\u8f6c\u6362\u8bbe\u7f6e", None))
        self.label_4.setText(QCoreApplication.translate("database_reform", u"\u76ee\u6807\u7248\u672c\uff1a", None))
        self.comboBox_target_version.setItemText(0, QCoreApplication.translate("database_reform", u"V2", None))
        self.comboBox_target_version.setItemText(1, QCoreApplication.translate("database_reform", u"V3", None))

        self.label_5.setText(QCoreApplication.translate("database_reform", u"\u4fdd\u5b58\u8def\u5f84\uff1a", None))
        self.lineEdit_save_path.setPlaceholderText(QCoreApplication.translate("database_reform", u"\u8bf7\u9009\u62e9\u4fdd\u5b58\u4f4d\u7f6e", None))
        self.pushButton_select_save_path.setText(QCoreApplication.translate("database_reform", u"\u9009\u62e9\u8def\u5f84", None))
        self.textEdit_log.setPlaceholderText(QCoreApplication.translate("database_reform", u"\u8f6c\u6362\u65e5\u5fd7\u5c06\u5728\u6b64\u663e\u793a...", None))
        self.pushButton_start.setText(QCoreApplication.translate("database_reform", u"\u5f00\u59cb\u8f6c\u6362", None))
    # retranslateUi

