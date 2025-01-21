# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox, QScrollArea
from PySide6.QtCore import Qt
from ui.home_page_ui import Ui_home_page
import os
import logging
from PySide6.QtGui import QFont
from config.config import PROJECT_ROOT  # 导入项目根目录配置

class HomePage(QWidget):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)
        self.ui = Ui_home_page()
        self.ui.setupUi(self)

        # 设置首页内容
        self.setup_content()

    def setup_content(self):
        """加载指定文件夹中的所有 TXT 文件，并在界面上显示其内容。"""
        txt_folder = os.path.join(PROJECT_ROOT, 'resources', 'home_page')
        
        if not os.path.exists(txt_folder):
            QMessageBox.critical(self, "错误", f"指定的文件夹不存在：{txt_folder}")
            return

        # 获取所有TXT文件
        txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

        if not txt_files:
            self.display_content("该文件夹中没有TXT文件。")
            return

        # 使用UI中预定义的布局
        content_layout = self.ui.contentLayout

        for txt_file in txt_files:
            file_path = os.path.join(txt_folder, txt_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception as e:
                logging.error(f"读取文件失败：{file_path}，错误：{e}")
                QMessageBox.critical(self, "读取错误", f"无法读取文件：{file_path}\n错误：{str(e)}")
                continue

            # 创建一个标签来显示文件内容
            content_label = QLabel(content)
            content_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            content_label.setWordWrap(True)
            
            # 使用样式表强制设置字体大小为18
            content_label.setStyleSheet("font-size: 18pt; font-family: 'Microsoft YaHei';")
            
            # 将标签添加到布局中
            content_layout.addWidget(content_label)

    def display_content(self, content):
        """显示默认内容"""
        label = QLabel(content)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setWordWrap(True)
        
        # 使用样式表强制设置字体大小为18
        label.setStyleSheet("font-size: 18pt; font-family: 'Microsoft YaHei';")

        # 使用UI中预定义的布局
        self.ui.contentLayout.addWidget(label)
