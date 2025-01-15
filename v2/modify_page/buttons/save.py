import logging
from PySide6.QtWidgets import QMessageBox

class SaveOperation:
    def __init__(self, parent,db_manager,table_widget,db_name):
        self.parent = parent
        self.db_manager = db_manager
        self.table_widget = table_widget
        self.db_name = db_name

    def execute(self):
        try:
            # 获取 soft_modify=1 的记录
            records_to_delete = self.db_manager.get_records_with_soft_modify(1)
            if not records_to_delete:
                QMessageBox.information(self.parent, "信息", "没有需要删除的记录。")
                return

            # 删除数据库中的记录
            for record in records_to_delete:
                record_id = record[0]  # 假设 record_id 在第一列
                success = self.db_manager.remove_file(record_id)
                if success:
                    logging.info(f"删除记录 ID={record_id}")
                    # 在 table_widget 中找到并删除对应的行
                    for row in range(self.table_widget.rowCount()):
                        if int(self.table_widget.item(row, 1).text()) == record_id:
                            self.table_widget.removeRow(row)
                            break
                else:
                    logging.error(f"删除记录失败 ID={record_id}")
                    QMessageBox.warning(self.parent, "警告", f"删除记录 ID={record_id} 失败。")
        except Exception as e:
            logging.error(f"保存操作失败: {e}")
            QMessageBox.critical(self.parent, "错误", f"保存操作失败: {e}")
        QMessageBox.information(self.parent, "成功", "保存成功")
