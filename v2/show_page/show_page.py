# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QWidget, QLabel, QTextEdit, QMessageBox, QVBoxLayout,
    QScrollArea, QDialog, QApplication, QSpinBox, QPushButton,
    QHBoxLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from .show_ui import Ui_show
from image_viewer.image_viewer import ImageViewer
from .config_manager import ConfigManager
import sqlite3
import os
import logging

class ImagePreviewLabel(QLabel):
    """可点击的图片预览标签"""
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setScaledContents(True)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(150, 150)
        self.setCursor(Qt.PointingHandCursor)
        self.viewer = None  # 添加图片查看器引用
        
        # 加载并设置缩略图
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                150, 150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.show_full_image()

    def show_full_image(self):
        """显示完整图片"""
        try:
            # 如果已经有打开的查看器，就先关闭它
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            
            # 创建新的查看器
            self.viewer = ImageViewer(self.image_path)
            # 设置窗口模态
            self.viewer.setWindowModality(Qt.ApplicationModal)
            # 连接关闭信号
            self.viewer.destroyed.connect(self.on_viewer_closed)
            # 显示窗口
            self.viewer.show()
            
        except Exception as e:
            logging.error(f"显示图片失败：{e}")
            QMessageBox.critical(None, "错误", f"显示图片失败：{str(e)}")

    def on_viewer_closed(self):
        """图片查看器关闭时的处理"""
        self.viewer = None

class SettingsDialog(QDialog):
    """设置对话框"""
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("设置")
        layout = QVBoxLayout(self)
        
        # 字体大小设置
        font_layout = QHBoxLayout()
        font_label = QLabel("字体大小：")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(self.config_manager.get('font_size', 14))
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_size_spin)
        layout.addLayout(font_layout)
        
        # 确定取消按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

class ShowPage(QWidget):
    def __init__(self, parent=None):
        super(ShowPage, self).__init__(parent)
        self.ui = Ui_show()
        self.ui.setupUi(self)
        
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        
        # 设置窗口标题
        self.setWindowTitle("知识点详情")
        
        # 初始化变量
        self.db_manager = None
        self.db_path = None
        self.current_item = None
        
        # 设置右侧文本框属性
        self.setup_text_area()
        
        # 连接设置按钮信号
        self.ui.settingsButton.clicked.connect(self.show_settings)
        
        # 连接信号槽
        self.ui.pushButton.clicked.connect(self.invoke_large_model)
        
        # 应用保存的字体大小
        self.apply_font_size()

    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            # 保存新的字体大小
            new_font_size = dialog.font_size_spin.value()
            self.config_manager.set('font_size', new_font_size)
            # 应用新的字体大小
            self.apply_font_size()

    def apply_font_size(self):
        """应用字体大小设置"""
        font_size = self.config_manager.get('font_size', 14)
        font = QFont()
        font.setPointSize(font_size)
        self.ui.textEdit.setFont(font)

    def setup_text_area(self):
        """设置右侧文本显示区域"""
        # 设置文本框为只读
        self.ui.textEdit.setReadOnly(True)
        # 设置自动换行
        self.ui.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)

    def display_knowledge_details_by_id(self, record_id):
        """通过ID显示知识点的详细信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT title, description, category, images FROM knowledge WHERE id = ?', (record_id,))
            record = cursor.fetchone()
            conn.close()

            if record:
                self.current_item = record_id
                title, description, category, images = record

                # 设置窗口标题
                self.setWindowTitle(f"知识点：{title}")

                # 清除原有布局中的所有控件
                while self.ui.scrollLayout.count():
                    child = self.ui.scrollLayout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

                # 显示图片预览
                if images:
                    image_list = images.split(',')
                    for img_name in image_list:
                        if img_name:
                            img_path = os.path.join(
                                os.path.dirname(self.db_path),
                                'images',
                                img_name
                            )
                            if os.path.exists(img_path):
                                preview = ImagePreviewLabel(img_path, self)
                                self.ui.scrollLayout.addWidget(preview)

                # 添加弹簧
                self.ui.scrollLayout.addStretch()

                # 显示描述文本
                self.ui.textEdit.setText(description)
                
                logging.info(f"显示记录ID={record_id}的详细信息")
                
        except sqlite3.Error as e:
            logging.error(f"显示知识点详情失败：{e}")
            QMessageBox.critical(self, "数据库错误", f"显示知识点详情失败：{str(e)}")

    def invoke_large_model(self):
        """调用大模型进行处理"""
        QMessageBox.information(self, "提示", "大模型处理功能正在开发中，敬请期待！")
