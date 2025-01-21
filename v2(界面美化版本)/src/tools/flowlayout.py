from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, 
                             QWidget, QFileDialog, QMessageBox, QTableWidgetItem,
                             QLabel, QHBoxLayout, QVBoxLayout, QLayout)
from PySide6.QtCore import Qt, Signal, QSize, QRect, QPoint
from PySide6.QtGui import QMouseEvent

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margin = self.contentsMargins()
        size += QSize(2 * margin.left(), 2 * margin.top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing()
            spaceY = self.spacing()
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

class CloseButton(QLabel):
    """关闭按钮类"""
    clicked = Signal(str)  

    def __init__(self, keyword, parent=None):
        super().__init__("✕", parent)
        self.keyword = keyword
        self.setStyleSheet("""
            QLabel {
                color: #666;
                padding: 0px 5px;
            }
            QLabel:hover {
                color: #000;
                background-color: #ccc;
                border-radius: 3px;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.keyword)  # 直接发出信号，不再查找父窗口

class KeywordLabel(QWidget):
    """关键字标签类"""
    remove_clicked = Signal(str)

    def __init__(self, keyword, parent=None):
        super().__init__(parent)
        self.keyword = keyword
        self.setup_ui()

    def setup_ui(self):
        """设置标签样式和内容"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        # 创建文本标签
        self.text_label = QLabel(self.keyword)
        
        # 创建关闭按钮，传入关键字
        self.close_button = CloseButton(self.keyword)
        self.close_button.clicked.connect(self.on_close)  # 连接关闭按钮的信号
        
        # 添加到布局
        layout.addWidget(self.text_label)
        layout.addWidget(self.close_button)

        # 设置整体样式
        self.setStyleSheet("""
            KeywordLabel {
                background-color: #e1e1e1;
                border-radius: 10px;
            }
            QLabel {
                background: transparent;
            }
        """)

    def on_close(self, keyword):
        """关闭按钮被点击时，发出信号以移除关键词"""
        self.remove_clicked.emit(keyword)  # 发出信号
        self.deleteLater()  # 删除小标签控件
