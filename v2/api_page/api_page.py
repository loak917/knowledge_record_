from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class APIPage(QWidget):
    def __init__(self, parent=None):
        super(APIPage, self).__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("API 功能即将实现，敬请期待！")
        layout.addWidget(label)
        self.setLayout(layout)
