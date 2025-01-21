import os
import sqlite3
import logging
from PySide6.QtWidgets import QFileDialog, QMessageBox
from src.core.database_manager import DatabaseManager  # 确保正确导入 DatabaseManager

"""
创建新的数据库
"""

class CreateNewDatabase:
    def __init__(self, parent, init_db_callback):
        self.parent = parent
        self.init_db = init_db_callback

    def execute(self):
        # 设置默认数据库文件夹路径
        default_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'db')
        # 确保文件夹存在
        os.makedirs(default_db_path, exist_ok=True)

        db_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "选择数据库保存位置",
            default_db_path,  # 使用默认路径
            "SQLite数据库 (*.db);;所有文件 (*.*)"
        )
        
        if db_path:
            try:
                # 检查路径有效性
                if not os.path.isdir(os.path.dirname(db_path)):
                    QMessageBox.critical(self.parent, "错误", "选择的路径无效。")
                    logging.error(f"无效的数据库路径：{db_path}")
                    return

                # 创建新的数据库文件
                if not os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    conn.close()
                    logging.info(f"新建数据库成功，路径：{db_path}")
                    QMessageBox.information(self.parent, "成功", f"新建数据库成功，路径：{db_path}")
                    
                    # 使用 DatabaseManager 初始化数据库
                    new_db_manager = DatabaseManager(db_path)
                    new_db_manager.connect()
                    new_db_manager.create_tables()
                    new_db_manager.migrate_tables()                

                    # 自动切换到新创建的数据库
                    self.parent.set_database(db_path)
                   
                else:
                    QMessageBox.warning(self.parent, "警告", f"数据库文件已存在：{db_path}")
            except sqlite3.Error as e:
                logging.error(f"新建数据库失败：{e}")
                QMessageBox.critical(self.parent, "数据库错误", f"新建数据库失败：{str(e)}")
