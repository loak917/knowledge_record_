import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import logging

"""
导入已有的数据库
""" 
class ImportDatabase:
    def __init__(self, parent, set_database_callback):
        self.parent = parent
        self.set_database = set_database_callback
        # 设置默认数据库文件夹路径
        self.default_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'db')
        # 确保文件夹存在
        os.makedirs(self.default_db_path, exist_ok=True)

    def execute(self):
        # 如果当前已有打开的数据库，提示用户
        if self.parent.db_path:
            reply = QMessageBox.question(
                self.parent,
                "确认切换数据库",
                "切换数据库将关闭当前数据库，是否继续？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        db_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "选择数据库",
            self.default_db_path,  # 使用默认路径
            "SQLite数据库 (*.db);;所有文件 (*.*)"
        )
        
        if db_path:
            try:
                # 关闭当前数据库连接（如果有）
                if self.parent.db_manager:
                    self.parent.db_manager.close()
                
                # 清空当前表格
                self.parent.ui.tableWidget.setRowCount(0)
                
                # 清空关键字
                self.parent.keywords.clear()
                
                # 清空关键字标签
                while self.parent.keywords_layout.count():
                    item = self.parent.keywords_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                
                # 重置分类下拉框
                self.parent.ui.comboBox.clear()
                self.parent.ui.comboBox.addItem("全部")
                
                # 重置选择计数
                self.parent.selection_label.setText("目前已选择数量：0")
                
                # 设置新数据库
                db_path = os.path.normpath(db_path)
                self.set_database(db_path)
                
                # 加载分类到下拉框
                categories = self.parent.db_manager.get_categories()
                self.parent.ui.comboBox.addItems(categories)
                
                # 重新加载数据
                self.parent.load_existing_records()
                
                # 更新数据库路径显示
                self.parent.ui.label.setText(f"当前数据库：{db_path}")
                
                logging.info(f"成功切换到新数据库：{db_path}")
                
            except Exception as e:
                logging.error(f"切换数据库失败：{e}")
                QMessageBox.critical(self.parent, "错误", f"切换数据库失败：{str(e)}")

