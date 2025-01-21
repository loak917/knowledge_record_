# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QInputDialog, QComboBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from ui.setting_ui import Ui_setting  # 导入自动生成的UI类
from src.gui.database_reform_page.database_reform_page import DatabaseReformPage
import os
import logging

# 设置日志记录
log_dir = os.path.join('resources', 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.DEBUG,  # 更改为 DEBUG 级别以捕获更多日志信息
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class SettingPage(QWidget):
    def __init__(self, parent=None, app=None):
        super(SettingPage, self).__init__(parent)
        self.ui = Ui_setting()
        self.ui.setupUi(self)
        self.app = app  # 引用主应用以便应用设置

        # 连接信号槽
        try:
            self.ui.pushButton.clicked.connect(self.font_settings)                     # 字体设置
            self.ui.pushButton_2.clicked.connect(self.database_version_conversion)      # 数据库版本转换
            self.ui.pushButton_3.clicked.connect(self.api_large_model_settings)         # API大模型
        except AttributeError as e:
            logging.error(f"UI 元素连接失败：{e}")
            QMessageBox.critical(
                self, "界面错误", f"未找到必要的按钮，请检查 UI 文件。\n详细错误：{str(e)}"
            )

    def font_settings(self):
        """打开输入对话框，允许用户输入字体大小并应用"""
        QMessageBox.information(self, "功能未实现", "字体设置功能尚未实现。")

    def database_version_conversion(self):
        """数据库版本转换功能（暂不实现）"""
        self.database_reform_page = DatabaseReformPage()
        self.database_reform_page.show()
        logging.info("数据库版本转换功能尚未实现。")

    def api_large_model_settings(self):
        """
        API大模型设置。
        示例：配置API密钥和选择模型。
        """
        # 输入API密钥
        QMessageBox.information(self, "暂时未实现", "API大模型设置功能暂时未实现。")
        pass
