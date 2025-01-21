from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import logging

"""
软删除，将选中的知识点的 soft_modify 标记为 1
"""
class DeleteSelected:
    def __init__(self, parent, db_manager, table_widget):
        self.parent = parent
        self.db_manager = db_manager
        self.table_widget = table_widget

    def execute(self):
        # 获取所有选中的行（通过复选框）
        ids_to_delete = []
        for row in range(self.table_widget.rowCount()):
            checkbox_item = self.table_widget.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                # 获取ID（在第二列）
                id_item = self.table_widget.item(row, 1)
                if id_item:
                    record_id = id_item.text()
                    ids_to_delete.append(record_id)

        if not ids_to_delete:
            QMessageBox.warning(self.parent, "警告", "请先选择要删除的项。")
            return

        try:
            for record_id in ids_to_delete:
                self.db_manager.update_soft_modify(record_id, soft_modify=1)  # 默认设置为1
            
            QMessageBox.information(self.parent, "成功", "选中的项已标记为删除状态。")
            logging.info(f"已标记 {len(ids_to_delete)} 项为删除状态。")
            
            # 刷新表格显示
            self.parent.load_existing_records()
        
        except Exception as e:
            logging.error(f"标记删除失败：{e}")
            QMessageBox.critical(self.parent, "错误", f"标记删除失败：{str(e)}")
        
