from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import logging

"""
撤销操作,利用数据库的soft_modify字段
默认为0,表示正常
如果是准备删除,则将soft_modify设置为1
在保存时,将所有的soft_modify设置为0
"""
class UndoOperation:
    def __init__(self, parent, db_manager, table_widget, db_name):
        self.parent = parent
        self.db_manager = db_manager
        self.table_widget = table_widget
        self.db_name = db_name

    def execute(self):
        # 获取所有标记为删除的记录
        records_to_undo = self.db_manager.get_records_with_soft_modify(soft_modify=1)
        
        if not records_to_undo:
            QMessageBox.information(self.parent, "信息", "没有需要撤销的操作。")
            return
            
        try:
            # 将所有标记为删除的记录恢复
            for record in records_to_undo:
                record_id = record[0]  # 获取记录ID
                self.db_manager.update_soft_modify(record_id, soft_modify=0)
            
            QMessageBox.information(self.parent, "成功", f"已撤销 {len(records_to_undo)} 项的删除标记。")
            logging.info(f"已撤销 {len(records_to_undo)} 项的删除标记")
            
            # 刷新表格显示
            self.parent.load_existing_records()
            
        except Exception as e:
            logging.error(f"撤销操作失败：{e}")
            QMessageBox.critical(self.parent, "错误", f"撤销操作失败：{str(e)}")
        

