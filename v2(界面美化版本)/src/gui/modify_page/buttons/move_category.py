from PySide6.QtWidgets import QInputDialog, QMessageBox
from PySide6.QtCore import Qt
import logging

"""
移动选中的知识点到指定的分类下
"""
class MoveTo:
    def __init__(self, parent, db_manager, table_widget, db_name):
        self.parent = parent
        self.db_manager = db_manager
        self.table_widget = table_widget
        self.db_name = db_name

    def execute(self):
        # 获取所有选中的行
        selected_rows = []
        for row in range(self.table_widget.rowCount()):
            checkbox_item = self.table_widget.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.warning(self.parent, "警告", "请先选择要移动的项。")
            return

        # 获取所有可用的分类
        categories = self.db_manager.get_categories()
        if not categories:
            QMessageBox.warning(self.parent, "警告", "没有可用的分类。")
            return

        # 弹出对话框让用户选择目标分类
        target_category, ok = QInputDialog.getItem(
            self.parent,
            "选择目标分类",
            "请选择要移动到的分类：",
            categories,
            0,  # 默认选择第一项
            False  # 不可编辑
        )

        if not ok or not target_category:
            return

        try:
            # 更新选中项的分类
            for row in selected_rows:
                # 获取记录ID（在第二列）
                record_id = int(self.table_widget.item(row, 1).text())
                
                # 获取当前记录的其他信息
                title = self.table_widget.item(row, 2).text()
                description = self.table_widget.item(row, 4).text()
                
                # 从数据库获取完整记录信息
                record = self.db_manager.get_record_by_id(record_id)
                if record:
                    # 更新记录，保持其他字段不变，只更新分类
                    self.db_manager.update_record(
                        record_id=record_id,
                        title=record[1],  # 保持原标题
                        category=target_category,  # 新分类
                        description=record[3],  # 保持原描述
                        images=record[4],  # 保持原图片
                        soft_modify=record[5]  # 保持原soft_modify状态
                    )
                    
                    # 更新表格显示
                    self.table_widget.item(row, 3).setText(target_category)

            QMessageBox.information(
                self.parent,
                "成功",
                f"已将选中的 {len(selected_rows)} 项移动到分类 '{target_category}'。"
            )
            logging.info(f"已将 {len(selected_rows)} 项移动到分类 '{target_category}'")

            # 刷新表格显示
            self.parent.load_existing_records()
            
        except Exception as e:
            logging.error(f"移动分类失败：{e}")
            QMessageBox.critical(self.parent, "错误", f"移动分类失败：{str(e)}")
