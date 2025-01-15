# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QScrollArea, QApplication, QSizePolicy,
    QToolBar
)
from PySide6.QtGui import (
    QPixmap, QWheelEvent, QIcon, QPalette, QMouseEvent,
    QAction
)
from PySide6.QtCore import Qt, QSize, QPoint


class ImageViewer(QMainWindow):
    def __init__(self, image_path, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.setWindowTitle("图片查看器")
        self.resize(800, 600)

        # 初始化变量
        self.scale_factor = 1.0
        self.last_mouse_pos = None  # 用于记录上一次鼠标位置

        # 创建工具栏
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)  # 禁止工具栏移动
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # 创建 QAction 动作
        self.create_actions()

        # 创建 QLabel 用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        # 创建 QScrollArea 并设置其属性
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.scroll_area)

        # 安装事件过滤器到 QScrollArea
        self.scroll_area.viewport().installEventFilter(self)

        # 加载图片
        self.load_image(image_path)

    def create_actions(self):
        """创建工具栏按钮"""
        # 放大按钮
        self.zoom_in_act = QAction(QIcon(), "放大(+)", self)
        self.zoom_in_act.setShortcut("Ctrl++")
        self.zoom_in_act.triggered.connect(self.zoom_in)
        self.toolbar.addAction(self.zoom_in_act)

        # 缩小按钮
        self.zoom_out_act = QAction(QIcon(), "缩小(-)", self)
        self.zoom_out_act.setShortcut("Ctrl+-")
        self.zoom_out_act.triggered.connect(self.zoom_out)
        self.toolbar.addAction(self.zoom_out_act)

        # 原始大小按钮
        self.normal_size_act = QAction(QIcon(), "原始大小(S)", self)
        self.normal_size_act.setShortcut("Ctrl+S")
        self.normal_size_act.triggered.connect(self.normal_size)
        self.toolbar.addAction(self.normal_size_act)

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        if self.pixmap.isNull():
            self.image_label.setText("无法加载图片")
        else:
            self.image_label.setPixmap(self.pixmap)
            self.scale_factor = 1.0
            self.image_label.adjustSize()

    def eventFilter(self, source, event):
        """事件过滤器，用于处理滚轮事件"""
        if source == self.scroll_area.viewport() and isinstance(event, QWheelEvent):
            # 只处理垂直滚轮事件
            if event.angleDelta().y() != 0:
                factor = 1.1 if event.angleDelta().y() > 0 else 0.9
                self.scale_image(factor)
                return True  # 事件已经被处理，不再传播
        return super().eventFilter(source, event)

    def wheelEvent(self, event: QWheelEvent):
        """处理滚轮事件用于缩放图片（辅助）"""
        # 事件过滤器已经处理了滚轮事件，这里直接忽略
        event.ignore()

    def mousePressEvent(self, event: QMouseEvent):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """处理鼠标移动事件"""
        if self.last_mouse_pos is not None:
            # 计算移动距离
            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            
            # 移动滚动条
            hbar = self.scroll_area.horizontalScrollBar()
            vbar = self.scroll_area.verticalScrollBar()
            hbar.setValue(hbar.value() - delta.x())
            vbar.setValue(vbar.value() - delta.y())
            
            event.accept()

    def zoom_in(self):
        """放大图片"""
        self.scale_image(1.1)

    def zoom_out(self):
        """缩小图片"""
        self.scale_image(0.9)

    def normal_size(self):
        """恢复图片原始大小"""
        self.scale_factor = 1.0
        self.image_label.setPixmap(self.pixmap)
        self.image_label.adjustSize()
        self.setWindowTitle("图片查看器")

    def scale_image(self, factor):
        """缩放图片"""
        new_scale = self.scale_factor * factor
        if new_scale < 0.1 or new_scale > 10:
            return  # 不进行缩放，超出限制

        self.scale_factor = new_scale
        new_size = self.scale_factor * self.pixmap.size()
        self.image_label.setPixmap(self.pixmap.scaled(
            new_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.image_label.adjustSize()
        
        # 更新窗口标题以显示缩放比例
        self.setWindowTitle(f"图片查看器 - {self.scale_factor * 100:.0f}%")
