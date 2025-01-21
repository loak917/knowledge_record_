# 目前是2.0版本，2025.1.19,美化版本

import sys
import os

from config.config import PROJECT_ROOT

import logging
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
import qtawesome as qta
import qdarkstyle

from src.gui.home_page.home_page import HomePage
from src.gui.knowledge_page.knowledge_page import KnowledgePage
from src.gui.modify_page.modify_page import ModifyPage
from src.gui.setting_page.setting_page import SettingPage
from src.gui.api_page.api_page import APIPage  
from src.tools.logger import logger
from src.core.database_manager import DatabaseManager


def excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.critical(None, "未捕获的异常", f"发生未捕获的异常：{exc_value}")

# 设置全局异常钩子
sys.excepthook = excepthook

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 修改 UI 文件加载方式
        ui_file_path = os.path.join(PROJECT_ROOT, "ui", "main.ui")
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"无法打开 UI 文件: {ui_file_path}")
            
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        if not self.ui:
            raise RuntimeError(loader.errorString())
            
        # 设置中央窗口
        self.setCentralWidget(self.ui)
        
        # 设置窗口初始大小和位置
        screen = QApplication.primaryScreen().geometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))
        self.move(int(screen.width() * 0.1), int(screen.height() * 0.1))
        
        # 初始化菜单页面
        self.menu_pages = {
            "首页": HomePage(),
            "知识点显示": KnowledgePage(),
            "知识点修改": ModifyPage(),
            "API": APIPage(),
            "设置": SettingPage(),
        }
        
        # 设置菜单按钮
        self.setup_menu_buttons()
        
        # 初始化堆叠窗口
        self.setup_stacked_widget()
        
        # 连接信号和槽
        self.ui.hide_button.clicked.connect(self.hide_menu)
        self.ui.show_button.clicked.connect(self.show_menu)
        self.ui.show_button.hide()
        
        # 设置样式
        self.setup_style()
        
        # 初始化时重置所有页面的状态
        self.reset_all_pages()

    def setup_menu_buttons(self):
        # 定义按钮样式和图标
        button_style = """
            QPushButton {
                text-align: left;
                padding: 8px 15px;
                font-size: 14px;
                border: none;
                background-color: #f0f0f0;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
        
        # 定义每个按钮的图标和文本
        menu_icons = {
            "首页": "fa5s.home",
            "知识点显示": "fa5s.book-open",
            "知识点修改": "fa5s.edit",
            "API": "fa5s.code",
            "设置": "fa5s.cog"
        }
        
        for name, page in self.menu_pages.items():
            btn = QPushButton(name)
            # 设置图标
            if name in menu_icons:
                icon = qta.icon(menu_icons[name], color='#333333')
                btn.setIcon(icon)
            btn.setStyleSheet(button_style)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda checked, p=page: self.switch_page(p))
            self.ui.menu_layout.addWidget(btn)
        
        self.ui.menu_layout.addStretch()

    def setup_stacked_widget(self):
        for page in self.menu_pages.values():
            self.ui.stacked_widget.addWidget(page)
        self.switch_page(self.menu_pages["首页"])

    def setup_style(self):
        # 设置主窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QWidget#menu_container {
                background-color: #f0f0f0;
                border-right: 1px solid #d0d0d0;
            }
            QPushButton#hide_button, QPushButton#show_button {
                background-color: #f0f0f0;
                border: none;
                color: #333333;
            }
            QPushButton#hide_button:hover, QPushButton#show_button:hover {
                background-color: #e0e0e0;
            }
            QStackedWidget {
                background-color: #ffffff;
            }
        """)
        
        # 设置隐藏/显示按钮的图标
        self.ui.hide_button.setIcon(qta.icon('fa5s.chevron-left', color='#333333'))
        self.ui.show_button.setIcon(qta.icon('fa5s.chevron-right', color='#333333'))
        
        # 移除之前的暗色主题
        # self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

    def switch_page(self, page):
        self.ui.stacked_widget.setCurrentWidget(page)

    def hide_menu(self):
        self.ui.menu_container.hide()
        self.ui.show_button.show()

    def show_menu(self):
        self.ui.menu_container.show()
        self.ui.show_button.hide()

    def reset_all_pages(self):
        """重置所有页面的状态"""
        for page in self.menu_pages.values():
            if hasattr(page, 'reset_state'):
                page.reset_state()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    app.setWindowIcon(qta.icon('fa5s.home'))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()