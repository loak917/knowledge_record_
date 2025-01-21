import sys
import os
import sqlite3
import logging
import shutil
from PySide6.QtWidgets import (
    QWidget, QMessageBox, QFileDialog, QInputDialog, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QComboBox, QDialog, 
    QAbstractItemView, QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QRect, Signal
from ui.modify_ui import Ui_dataloader  # 导入自动生成的UI类
from src.tools.flowlayout import FlowLayout, KeywordLabel  # 导入小标签功能
from .buttons.add_record_dialog import AddRecordDialog  # 导入添加对话界面
from .buttons.import_database import ImportDatabase#导入选择数据库功能
from .buttons.create_new_database import CreateNewDatabase#导入创建新数据库功能
from .buttons.delete_selected import DeleteSelected#导入删除选中功能
from .buttons.add_keyword import AddKeyword #导入小标签（关键字）功能
from .buttons.add_category import AddCategory#导入添加分类功能
from .buttons.move_category import MoveTo#导入移动归类的功能
from .buttons.category_management import CategoryManagement#导入归类管理功能
from .buttons.save import SaveOperation#导入保存操作功能
from src.core.database_manager import DatabaseManager  # 导入数据库管理功能
from src.gui.show_modify_page.show_modify_page import ShowModifyPage  # 导入修改页面
from .buttons.undo_operation import UndoOperation#导入撤销操作功能
from src.tools.logger import logger

class ModifyPage(QWidget):
    switch_window = Signal(str)  # 添加信号用于切换窗口或其他用途

    def __init__(self, db_manager=None, parent=None):
        super(ModifyPage, self).__init__(parent)
        self.ui = Ui_dataloader()
        self.ui.setupUi(self)

        self.db_manager = db_manager
        self.db_path = None

        # 创建关键字显示区域
        self.keywords_widget = QWidget()
        self.keywords_layout = FlowLayout()
        self.keywords_widget.setLayout(self.keywords_layout)
        self.keywords_widget.setMinimumHeight(40)
        self.keywords_widget.setMaximumHeight(80)
        self.setup_keyword_container()  # 设置关键字容器的样式

        self.ui.verticalLayout.insertWidget(1, self.keywords_widget)

        # 存储当前的关键字集合
        self.keywords = set()

        # 加载现有记录
        self.load_existing_records()

        # 添加当前数据库显示标签
        self.ui.label.setText("当前数据库: 未选择")
        self.ui.label.setFont(QFont("Arial", 9, QFont.Bold))
        self.ui.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 设置日志记录
        log_dir = os.path.join('resources', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, 'app.log'),
            level=logging.DEBUG,  # 设置为 DEBUG 级别以捕获更多日志信息
            format='%(asctime)s:%(levelname)s:%(message)s'
        )

        # 初始化按钮状态
        self.update_ui_state()

        # 设置表格结构
        self.setup_table()

        # 初始化文件后缀下拉框
        self.ui.comboBox.addItem("全部")

        # 动态添加显示已选择数量的标签
        self.selection_label = QLabel("目前已选择数量：0", self)
        self.selection_label.setFont(QFont("Microsoft YaHei", 12))
        # 将selection_label添加到bottomWidget的布局中
        self.ui.horizontalLayout_4.insertWidget(1, self.selection_label)

        # 连接按钮信号
        self.setup_buttons()

        # 连接其他信号
        self.ui.tableWidget.itemClicked.connect(self.handle_row_click)
        self.ui.tableWidget.itemChanged.connect(self.update_selection_count)
        self.ui.comboBox.currentTextChanged.connect(self.filter_by_category)
        self.ui.lineEdit.returnPressed.connect(self.handle_add_keyword)

        # 清空上一次的打开信息
        self.reset_state()

        # 连接表格双击信号
        self.ui.tableWidget.cellDoubleClicked.connect(self.handle_table_double_click)

        # 设置表格列数和表头
        headers = ["选择", "ID", "标题", "分类", "内容"]
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        
        # 隐藏ID列
        self.ui.tableWidget.setColumnHidden(1, True)  # 隐藏第二列（ID列）

    def update_ui_state(self):
        """根据是否选择数据库，更新UI状态"""
        db_selected = self.db_path is not None

        # 更新当前数据库标签
        if db_selected:
            self.ui.label.setText(f"当前数据库: {self.db_path}")

            # 启用相关按钮
            self.ui.pushButton_5.setEnabled(db_selected)    # 查询按钮
            self.ui.pushButton_6.setEnabled(db_selected)    # 添加归类按钮
            self.ui.pushButton_9.setEnabled(db_selected)    # 移动至按钮
            self.ui.pushButton_10.setEnabled(db_selected)   # 归类管理按钮
            self.ui.pushButton_3.setEnabled(db_selected)   # 确认修改按钮
            self.ui.pushButton_4.setEnabled(db_selected)   # 撤销按钮
            self.ui.pushButton_7.setEnabled(db_selected)   # 删除选中按钮
            self.ui.pushButton_8.setEnabled(db_selected)   # 添加记录按钮
            self.ui.radioButton.setEnabled(db_selected)   # 全选按钮

        else:
            self.ui.label.setText("当前数据库: 未选择")

            # 禁用相关按钮
            self.ui.pushButton_5.setEnabled(db_selected)    # 查询按钮
            self.ui.pushButton_6.setEnabled(db_selected)    # 添加归类按钮
            self.ui.pushButton_9.setEnabled(db_selected)    # 移动至按钮
            self.ui.pushButton_10.setEnabled(db_selected)   # 归类管理按钮
            self.ui.pushButton_3.setEnabled(db_selected)   # 确认修改按钮
            self.ui.pushButton_4.setEnabled(db_selected)   # 撤销按钮
            self.ui.pushButton_7.setEnabled(db_selected)   # 删除选中按钮
            self.ui.pushButton_8.setEnabled(db_selected)   # 添加记录按钮
            self.ui.radioButton.setEnabled(db_selected)   # 全选按钮

    def setup_buttons(self):
        """连接按钮到对应的功能模块"""
        self.ui.radioButton.clicked.connect(self.handle_select_all)                   #全部选中
        self.ui.pushButton.clicked.connect(self.handle_import_database)               # 导入数据库 -> handle_import_database
        self.ui.pushButton_2.clicked.connect(self.handle_create_new_database)         # 新建数据库 -> handle_create_new_database
        self.ui.pushButton_3.clicked.connect(self.handle_save_operation)              # 确认修改保存 -> handle_save_operation
        self.ui.pushButton_4.clicked.connect(self.handle_undo_operation)              # 撤销操作 -> handle_undo_operation
        self.ui.pushButton_5.clicked.connect(self.handle_query)                       # 查询 -> handle_query
        self.ui.pushButton_6.clicked.connect(self.handle_add_category)                # 添加归类 -> handle_add_category
        self.ui.pushButton_7.clicked.connect(self.handle_delete_selected)             # 删除选中 -> handle_delete_selected
        self.ui.pushButton_8.clicked.connect(self.handle_add_record)                  # 添加记录 -> handle_add_record
        self.ui.pushButton_9.clicked.connect(self.handle_move_to)                     # 移动至 -> handle_move_to
        self.ui.pushButton_10.clicked.connect(self.handle_category_management)        # 归类管理 -> handle_category_management

    def set_database(self, db_path):
        """
        设置新的数据库路径，并加载数据。
        """
        self.db_path = db_path
        self.db_manager = DatabaseManager(self.db_path)
        self.db_name = self.db_manager.get_db_name()
        self.init_db(insert_sample=False)
        self.load_existing_files()
        QMessageBox.information(self, "成功", f"已选择数据库：{db_path}")
        logging.info(f"已选择数据库：{db_path}")
        self.update_ui_state()

    def init_db_callback(self, db_path):
        """数据库初始化回调函数"""
        self.set_database(db_path)

    def init_db(self, insert_sample=True):
        """初始化数据库"""
        if self.db_manager:
            self.db_manager.connect()
            if insert_sample:
                self.db_manager.insert_sample_data()
            logging.info("数据库初始化完成")
            self.update_ui_state()

    def handle_import_database(self):
        """处理导入数据库按钮点击"""
        selector = ImportDatabase(self, self.set_database)
        selector.execute()
        self.load_existing_records()
        self.load_categories_into_combobox()

    def handle_category_management(self):
        """处理归类管理按钮点击"""
        if not self.db_manager:
            QMessageBox.warning(self, "警告", "尚未选择数据库。")
            return
        manager = CategoryManagement(self.db_manager, self)
        result = manager.exec()
        if result == QDialog.Accepted:
            logging.info("归类管理对话框已通过.")
        else:
            logging.info("归类管理对话框已取消.")
        # 重新加载分类到下拉框
        self.load_categories_into_combobox()

    def reset_state(self):
        """重置页面状态，清空之前的信息"""
        if self.db_manager:
            # 清空表格
            self.ui.tableWidget.setRowCount(0)
            
            # 清空关键字集合和标签
            self.keywords.clear()
            for i in reversed(range(self.keywords_layout.count())):
                widget_to_remove = self.keywords_layout.itemAt(i).widget()
                self.keywords_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)
            
            # 重置选择计数
            self.selection_label.setText("目前已选择数量：0")
            
            # 重置下拉框和搜索框
            self.ui.comboBox.setCurrentIndex(0)
            self.ui.lineEdit.clear()

    def setup_keyword_container(self):
        """设置关键字标签区域"""
        # 设置关键字区域的样式
        self.keywords_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        # 设置大小策略
        self.keywords_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def handle_query(self):
        """处理查询按钮点击"""
        keyword = self.ui.lineEdit.text().strip()
        if not keyword:
            QMessageBox.warning(self, "警告", "请输入查询关键字！")
            return
        
        # 添加关键字标签
        self.add_keyword_label(keyword)
        # 清空输入框
        self.ui.lineEdit.clear()
        logging.info(f"执行查询，关键字：{keyword}")
        
    def handle_undo_operation(self):
        """处理撤销操作按钮点击"""
        QMessageBox.information(self, "信息", "撤销操作尚未实现。")
        logging.info("执行撤销操作（尚未实现）。")

    def add_keyword_label(self, keyword):
        """添加关键字标签到布局"""
        if keyword and keyword not in self.keywords:
            self.keywords.add(keyword)
            # 创建关键字标签
            keyword_label = KeywordLabel(keyword)
            keyword_label.remove_clicked.connect(lambda k=keyword: self.keywords_filters(k))
            # 添加到FlowLayout
            self.keywords_layout.addWidget(keyword_label)
            
            # 应用筛选
            self.keywords_filters()
            
            # 更新布局
            self.keywords_widget.adjustSize()
            self.keywords_layout.update()

    def keywords_filters(self, removed_keyword=None):
        """关键字过滤"""
        if removed_keyword:
            # 如果是移除关键字的操作
            if removed_keyword in self.keywords:
                self.keywords.remove(removed_keyword)
                # 查找并移除对应的标签
                for i in range(self.keywords_layout.count()):
                    widget = self.keywords_layout.itemAt(i).widget()
                    if isinstance(widget, KeywordLabel) and widget.keyword == removed_keyword:
                        widget.hide()
                        widget.deleteLater()
                        break
        
        # 执行筛选操作
        self.filter_by_keywords()
        # 强制刷新表格视图
        self.ui.tableWidget.viewport().update()

    def setup_table(self):
        """设置表格结构"""
        self.ui.tableWidget.setColumnCount(5)
        headers = ["选择", "ID", "标题", "分类", "内容"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        
        # 设置列宽
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 200)
        self.ui.tableWidget.setColumnWidth(3, 150)
        self.ui.tableWidget.setColumnWidth(4, 600)
        
        # 设置选择行为和编辑触发
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # 连接双击信号
        self.ui.tableWidget.cellDoubleClicked.connect(self.handle_table_double_click)
        

    def add_table_row(self, title, category, description):
        """添加新行到表格"""
        try:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)

            # 添加复选框
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)

            self.ui.tableWidget.setItem(row, 0, checkbox)
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(row + 1)))  # 假设ID为行号
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(title))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(category))
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(description))

            logging.info(f"添加表格行：标题={title}, 分类={category}, 内容={description}")
        except Exception as e:
            logging.error(f"添加表格行时出错：{e}")
            QMessageBox.critical(self, "错误", f"添加表格行失败：{str(e)}")

    def handle_row_click(self, item):
        """处理表格行点击事件"""
        # 可以根据需求添加处理逻辑
        pass

    def update_selection_count(self, item):
        """更新选择计数"""
        try:
            count = 0
            for row in range(self.ui.tableWidget.rowCount()):
                checkbox_item = self.ui.tableWidget.item(row, 0)
                if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                    count += 1
            self.selection_label.setText(f"目前已选择数量：{count}")
            logging.info(f"更新选择计数：{count}")
        except Exception as e:
            logging.error(f"更新选择计数时出错：{e}")
            QMessageBox.critical(self, "错误", f"更新选择计数时出错：{str(e)}")

    def filter_by_category(self, category):
        """根据分类筛选表格内容"""
        try:
            for row in range(self.ui.tableWidget.rowCount()):
                if category == "全部":
                    self.ui.tableWidget.setRowHidden(row, False)
                else:
                    category_item = self.ui.tableWidget.item(row, 3)  # 分类在第4列
                    if category_item:
                        self.ui.tableWidget.setRowHidden(
                            row, 
                            category_item.text() != category
                        )
            
            # 更新选择计数
            self.update_selection_count(None)
            
        except Exception as e:
            logging.error(f"分类筛选失败：{e}")
            QMessageBox.critical(self, "错误", f"分类筛选失败：{str(e)}")

    def filter_by_keywords(self):
        """依据关键字对内容查找"""
        try:
            # 获取当前分类筛选条件
            current_category = self.ui.comboBox.currentText()
            
            # 遍历表格中的每一行
            for row in range(self.ui.tableWidget.rowCount()):
                should_show = True
                
                # 获取该行的标题和内容
                title_item = self.ui.tableWidget.item(row, 2)  # 标题在第3列
                category_item = self.ui.tableWidget.item(row, 3)  # 分类在第4列
                content_item = self.ui.tableWidget.item(row, 4)  # 内容在第5列
                
                if title_item and category_item and content_item:
                    title = title_item.text().lower()
                    category = category_item.text()
                    content = content_item.text().lower()
                    
                    # 检查是否匹配所有关键字
                    for keyword in self.keywords:
                        keyword = keyword.lower()
                        # 如果关键字不在标题或内容中，则隐藏该行
                        if keyword not in title and keyword not in content:
                            should_show = False
                            break
                    
                    # 如果选择了特定分类，还需要检查分类是否匹配
                    if current_category != "全部" and category != current_category:
                        should_show = False
                    
                # 设置行的显示状态
                self.ui.tableWidget.setRowHidden(row, not should_show)
            
            # 强制刷新表格显示
            self.ui.tableWidget.viewport().update()
            
            # 更新已选择的数量显示
            self.update_selection_count(None)           
            
            logging.info(f"根据关键字 {self.keywords} 和分类 '{current_category}' 筛选完成")
            
        except Exception as e:
            logging.error(f"关键字筛选失败：{e}")
            QMessageBox.critical(self, "错误", f"筛选失败：{str(e)}")

    def apply_filters(self):
        """应用所有筛选条件（关键字和分类）"""
        try:
            # 获取当前分类筛选条件
            current_category = self.ui.comboBox.currentText()
            
            # 遍历表格中的每一行
            for row in range(self.ui.tableWidget.rowCount()):
                should_show = True
                
                # 获取该行的标题、分类和内容
                title_item = self.ui.tableWidget.item(row, 2)
                category_item = self.ui.tableWidget.item(row, 3)
                content_item = self.ui.tableWidget.item(row, 4)
                
                if title_item and category_item and content_item:
                    title = title_item.text().lower()
                    category = category_item.text()
                    content = content_item.text().lower()
                    
                    # 检查分类筛选
                    if current_category != "全部" and category != current_category:
                        should_show = False
                    
                    # 检查关键字筛选
                    if should_show and self.keywords:  # 只有在分类匹配时才检查关键字
                        for keyword in self.keywords:
                            keyword = keyword.lower()
                            if keyword not in title and keyword not in content:
                                should_show = False
                                break
                
                # 设置行的显示状态
                self.ui.tableWidget.setRowHidden(row, not should_show)
            
            # 更新选择计数
            self.update_selection_count(None)
            
            logging.info(f"应用筛选：关键字={self.keywords}, 分类='{current_category}'")
            
        except Exception as e:
            logging.error(f"应用筛选失败：{e}")
            QMessageBox.critical(self, "错误", f"筛选失败：{str(e)}")

    def load_existing_files(self):
        """加载已有的文件到表格中"""
        records = self.db_manager.get_all_records()
        for record in records:
            title = record[1]
            category = record[2]
            description = record[3]
            self.add_table_row(title, category, description)
        logging.info("加载已有记录完成")

    def handle_add_record(self):
        """处理添加新记录按钮点击"""
        if not self.db_manager:
            QMessageBox.warning(self, "警告", "数据库尚未连接。")
            return

        categories = self.db_manager.get_categories()
        dialog = AddRecordDialog(self, categories, self.db_name)
        if dialog.exec_() == QDialog.Accepted:
            title, category, description, image_names = dialog.get_data()
            self.add_table_row(title, category, description)
            logging.info(f"更新显示：标题={title}, 分类={category}")

    def handle_table_double_click(self, row, column):
        """处理表格行双击事件，打开修改界面"""
        if not self.db_manager:
            QMessageBox.warning(self, "警告", "数据库尚未连接。")
            return

        try:
            # 获取记录ID（从第二列）
            record_id_item = self.ui.tableWidget.item(row, 1)
            if record_id_item:
                record_id = int(record_id_item.text())
                
                # 检查是否已经打开了修改窗口
                if hasattr(self, 'modify_page') and self.modify_page.isVisible():
                    self.modify_page.close()
                
                # 创建并显示新的修改窗口
                self.modify_page = ShowModifyPage(self.db_manager, record_id, self)
                self.modify_page.show()
                logging.info(f"打开记录ID={record_id}的修改界面")
                
        except ValueError as e:
            logging.error(f"无效的记录ID：{e}")
            QMessageBox.critical(self, "错误", f"无效的记录ID")
        except Exception as e:
            logging.error(f"打开修改界面失败：{e}")
            QMessageBox.critical(self, "错误", f"打开修改界面失败：{str(e)}")

    def open_modify_page(self, record_id):
        """打开修改界面并传递记录ID"""
        self.modify_page = ShowModifyPage(self.db_manager, record_id, self)
        self.modify_page.show()

    def load_existing_records(self):
        """加载数据库中的现有记录到表格"""
        try:
            # 清空表格
            self.ui.tableWidget.setRowCount(0)
            
            if not self.db_manager:
                return
            
            # 获取所有记录
            records = self.db_manager.get_all_records()
            
            # 设置表格行数
            self.ui.tableWidget.setRowCount(len(records))
            
            # 填充表格
            for row, record in enumerate(records):
                # 添加复选框
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.ui.tableWidget.setItem(row, 0, checkbox_item)
                
                # 填充其他列
                for col, value in enumerate(record, start=1):
                    item = QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(row, col, item)
            
            # 更新选择计数
            self.update_selection_count(None)
            
            logging.info("成功加载现有记录")
            
        except Exception as e:
            logging.error(f"加载记录失败：{e}")
            QMessageBox.critical(self, "错误", f"加载记录失败：{str(e)}")

    def handle_add_keyword(self):
        """处理回车添加关键词"""
        keyword = self.ui.lineEdit.text().strip()
        if keyword:
            self.add_keyword_label(keyword)
            self.ui.lineEdit.clear()  # 清空输入框

    def handle_delete_selected(self):
        """处理删除选中按钮点击"""
        deleter = DeleteSelected(self, self.db_manager, self.ui.tableWidget)
        deleter.execute()

    def handle_add_category(self):
        """处理添加归类按钮点击"""
        adder = AddCategory(self)
        adder.execute()

    def handle_save_operation(self):
        """处理保存操作按钮点击"""
        saver = SaveOperation(self, self.db_manager, self.ui.tableWidget, self.db_name)
        saver.execute()

    def handle_create_new_database(self):
        """处理创建新数据库按钮点击"""
        creator = CreateNewDatabase(self, self.init_db_callback)
        creator.execute()

    def handle_move_to(self):
        """处理移动至按钮点击"""
        mover = MoveTo(self, self.db_manager, self.ui.tableWidget, self.db_name)
        mover.execute() 
    
    def handle_select_all(self):
        """处理全选按钮点击"""
        try:
            # 获取当前按钮状态
            is_checked = self.ui.radioButton.isChecked()
            
            # 遍历所有行
            for row in range(self.ui.tableWidget.rowCount()):
                # 只处理未被隐藏的行
                if not self.ui.tableWidget.isRowHidden(row):
                    checkbox_item = self.ui.tableWidget.item(row, 0)
                    if checkbox_item:
                        checkbox_item.setCheckState(
                            Qt.Checked if is_checked else Qt.Unchecked
                        )
            
            # 更新选择计数
            self.update_selection_count(None)
            
            logging.info(f"{'全选' if is_checked else '取消全选'}操作完成")
            
        except Exception as e:
            logging.error(f"全选操作出错：{e}")
            QMessageBox.critical(self, "错误", f"全选操作失败：{str(e)}")

    def load_categories_into_combobox(self):
        """加载分类到下拉框"""
        try:
            if not self.db_manager:
                return
            
            # 保存当前选中的分类
            current_category = self.ui.comboBox.currentText()
            
            # 清空下拉框
            self.ui.comboBox.clear()
            
            # 添加"全部"选项
            self.ui.comboBox.addItem("全部")
            
            # 从数据库获取所有分类并添加到下拉框
            categories = self.db_manager.get_categories()
            self.ui.comboBox.addItems(categories)
            
            # 恢复之前选中的分类
            index = self.ui.comboBox.findText(current_category)
            if index >= 0:
                self.ui.comboBox.setCurrentIndex(index)
            
            logging.info("成功加载分类到下拉框")
            
        except Exception as e:
            logging.error(f"加载分类到下拉框失败：{e}")
            QMessageBox.critical(self, "错误", f"加载分类失败：{str(e)}")


