from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QInputDialog, QHBoxLayout
import logging
import sqlite3
from src.core.database_manager import DatabaseManager

"""
分类管理
"""

class CategoryManagement(QDialog):
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super(CategoryManagement, self).__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("分类管理")
        self.setModal(True)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("分类列表：")
        self.layout.addWidget(self.label)
        
        self.listWidget = QListWidget()
        self.layout.addWidget(self.listWidget)
        
        self.button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("添加分类")
        self.delete_button = QPushButton("删除分类")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        
        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)
        
        self.add_button.clicked.connect(self.add_category)
        self.delete_button.clicked.connect(self.delete_category)
        
        self.load_categories()
    
    def load_categories(self):
        """加载分类到列表中"""
        self.listWidget.clear()
        categories = self.db_manager.get_categories()
        self.listWidget.addItems(categories)
    
    def add_category(self):
        """添加新的分类"""
        text, ok = QInputDialog.getText(self, "添加分类", "分类名称：")
        if ok and text:
            # 首先检查该分类是否已存在
            categories = self.db_manager.get_categories()
            if text in categories:
                QMessageBox.warning(self, "警告", f"分类 '{text}' 已存在。")
                logging.warning(f"尝试添加已存在的分类：{text}")
                return
            # 插入新分类到 categories 表
            success = self.db_manager.add_category(text)
            if success:
                logging.info(f"添加分类：{text}")
                self.load_categories()
                QMessageBox.information(self, "成功", f"添加分类 '{text}' 成功。")
            else:
                QMessageBox.warning(self, "警告", f"分类 '{text}' 添加失败或已存在。")
        else:
            QMessageBox.warning(self, "警告", "分类名称不能为空！")
            logging.warning("尝试添加空分类名称。")
    
    def delete_category(self):
        """删除选中的分类"""
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要删除的分类。")
            return
        
        categories_to_delete = [item.text() for item in selected_items]
        confirm = QMessageBox.question(
            self, "确认删除",
            f"确定要删除选中的分类：{', '.join(categories_to_delete)} 吗？\n这将删除所有相关的知识点记录。",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        for category_name in categories_to_delete:
            success = self.db_manager.remove_category(category_name, delete_related=True)
            if success:
                logging.info(f"删除分类及相关记录：{category_name}")
                QMessageBox.information(self, "成功", f"删除分类 '{category_name}' 及相关记录成功。")
            else:
                QMessageBox.critical(self, "错误", f"删除分类 '{category_name}' 失败。")
        
        self.load_categories()
