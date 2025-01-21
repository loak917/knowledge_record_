from PySide6.QtWidgets import QInputDialog, QMessageBox
import logging

"""
添加归类（分类）
"""

class AddCategory:
    def __init__(self, parent):
        self.parent = parent

    def execute(self):
        category, ok = QInputDialog.getText(self.parent, "添加归类", "输入新归类名称：")
        if ok and category.strip():
            category = category.strip()
            if category not in self.parent.db_manager.get_categories():
                self.parent.db_manager.add_category(category)
                self.parent.ui.comboBox.addItem(category)
                QMessageBox.information(self.parent, "成功", f"添加归类成功：{category}")
                logging.info(f"添加了新分类：{category}")
            else:
                QMessageBox.warning(self.parent, "警告", "分类已存在！")
                logging.warning("尝试添加已存在的分类。")
        else:
            QMessageBox.warning(self.parent, "警告", "分类名称不能为空！")
            logging.warning("尝试添加空分类名称。")
