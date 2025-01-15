# 目前是2.0版本，2025.1.4

import sys
import logging
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from home_page.home_page import HomePage
from knowledge_page.knowledge_page import KnowledgePage
from modify_page.modify_page import ModifyPage
from setting_page.setting_page import SettingPage
from api_page.api_page import APIPage  # 新增 API 占位页面
from tools.logger import logger
from tools.database_manager import DatabaseManager

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
        self.resize(1024, 648)  # 设置窗口大小
        self.setWindowTitle("软件主界面")

        # 创建中央窗口部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 创建主布局（水平布局）
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # 去除外边距
        self.main_layout.setSpacing(0)  # 去除控件间距

        # 创建左侧菜单栏
        self.create_menu()

        # 创建右侧堆叠窗口
        self.create_stacked_widget()

        # 将菜单栏和堆叠窗口添加到主布局
        self.main_layout.addWidget(self.menu_container)
        self.main_layout.addWidget(self.stacked_widget, stretch=1)  # 右侧内容占用剩余空间

        # 初始化时重置所有页面的状态
        self.reset_all_pages()

    def create_menu(self):
        # 定义菜单项及对应的页面
        self.menu_pages = {
            "首页": HomePage(),
            "知识点显示": KnowledgePage(),
            "知识点修改": ModifyPage(),
            "API": APIPage(), 
            "设置": SettingPage(),
        }

        # 创建菜单布局（垂直布局）
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)  # 去除布局外边距
        menu_layout.setSpacing(0)  # 去除按钮间距

        # 创建"隐藏菜单"按钮（文本更改为<<<，放在顶部）
        self.hide_button = QPushButton("<<<")
        self.hide_button.setFixedHeight(40)
        self.hide_button.setStyleSheet(
            """
            QPushButton {
                text-align: center;
                padding-left: 10px;
                background-color: #f0f0f0;
                color: black;  /* 字体颜色设置为黑色 */
                border: none;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #dcdcdc;
            }
            """
        )
        self.hide_button.clicked.connect(self.hide_menu)
        menu_layout.addWidget(self.hide_button)

        # 创建菜单按钮
        for name, page in self.menu_pages.items():
            btn = QPushButton(name)
            btn.setFixedHeight(40)  # 设置按钮高度
            btn.setStyleSheet(
                """
                QPushButton {
                    text-align: left;
                    padding-left: 20px;
                    background-color: #f0f0f0;
                    color: black;  /* 菜单按钮字体颜色设置为黑色 */
                    border: none;
                    font-size: 12pt;
                }
                QPushButton:hover {
                    background-color: #dcdcdc;
                }
                """
            )
            btn.clicked.connect(lambda checked, p=page: self.switch_page(p))
            menu_layout.addWidget(btn)

        # 添加一个拉伸项，使按钮靠顶部排列
        menu_layout.addStretch()

        # 创建一个 QWidget 作为菜单内容，并设置布局
        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)

        # 创建 QScrollArea 并设置菜单内容
        self.menu_scroll_area = QScrollArea()
        self.menu_scroll_area.setWidgetResizable(True)
        self.menu_scroll_area.setWidget(menu_widget)
        self.menu_scroll_area.setFixedWidth(170)  # 设置固定宽度
        self.menu_scroll_area.setStyleSheet("background-color: #f0f0f0;")  # 设置背景颜色
        self.menu_scroll_area.setFrameShape(QScrollArea.NoFrame)  # 去除边框

        # 将 QScrollArea 包装在一个容器中，以便控制显示按钮
        self.menu_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.menu_scroll_area)
        self.menu_container.setLayout(container_layout)

        # 创建"显示菜单"按钮（初始隐藏，放在主布局的左侧边缘）
        self.show_button = QPushButton(">>>")
        self.show_button.setFixedWidth(60)  # 小按钮宽度
        self.show_button.setFixedHeight(40)
        self.show_button.setStyleSheet(
            """
            QPushButton {
                text-align: center;
                background-color: #f0f0f0;
                color: black;  /* 字体颜色设置为黑色 */
                border: none;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #dcdcdc;
            }
            """
        )
        self.show_button.clicked.connect(self.show_menu)
        self.show_button.setVisible(False)  # 初始隐藏
        self.main_layout.addWidget(self.show_button)  # 添加到主布局中

    def create_stacked_widget(self):
        self.stacked_widget = QStackedWidget()
        for name, page in self.menu_pages.items():
            self.stacked_widget.addWidget(page)
        # 设置首页为默认显示
        self.switch_page(self.menu_pages["首页"])

    def switch_page(self, page):
        self.stacked_widget.setCurrentWidget(page)

    def hide_menu(self):
        self.menu_container.hide()
        self.hide_button.setVisible(False)
        self.show_button.setVisible(True)

    def show_menu(self):
        self.menu_container.show()
        self.show_button.setVisible(False)
        self.hide_button.setVisible(True)

    def reset_all_pages(self):
        """重置所有页面的状态"""
        for name, page in self.menu_pages.items():
            if hasattr(page, 'reset_state'):
                page.reset_state()

def main():
    app = QApplication(sys.argv)
    
    # 加载统一样式表
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
            font-size: 10pt;
            background-color: #ffffff;
            color: #000000;
        }
        QPushButton {
            background-color: #f0f0f0; /* 默认背景色统一调整 */
            color: black;              /* 全局按钮字体颜色设置为黑色 */
            border: none;
            padding: 5px;
            border-radius: 4px;
            text-decoration: none;
        }
        QPushButton:hover {
            background-color: #dcdcdc;
        }
        QTableWidget {
            gridline-color: #D3D3D3;
            background-color: #f9f9f9;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            padding: 4px;
            border: 1px solid #D3D3D3;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()