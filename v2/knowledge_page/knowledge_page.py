# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QFileDialog, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, Signal, QRect
from .knowledge_ui import Ui_dataloader
from tools.database_manager import DatabaseManager
import os
import logging

class KeywordLabel(QLabel):
    """关键字标签"""
    remove_clicked = Signal(str)  # 删除信号

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(f" {text} ×")
        self.setStyleSheet("""
            QLabel {
                background-color: #e1e1e1;
                border-radius: 10px;
                padding: 5px;
                margin: 2px;
            }
            QLabel:hover {
                background-color: #d1d1d1;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.keyword = text

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.remove_clicked.emit(self.keyword)

class KnowledgePage(QWidget):
    def __init__(self, parent=None):
        super(KnowledgePage, self).__init__(parent)
        self.ui = Ui_dataloader()
        self.ui.setupUi(self)
        
        # 初始化变量
        self.db_manager = None
        self.db_path = None
        self.keywords = set()
        self.detail_windows = []  # 保存详情窗口的引用
        
        # 创建关键字显示区域
        self.setup_keywords_area()
        
        # 设置表格属性
        self.setup_table()
        
        # 连接信号槽
        self.connect_signals()
        
        # 初始化日志
        self.setup_logging()
        
        # 初始禁用按钮
        self.set_buttons_enabled(False)

    def setup_keywords_area(self):
        """设置关键字显示区域"""
        # 创建水平布局
        self.keywords_layout = QHBoxLayout()
        self.keywords_layout.setContentsMargins(0, 0, 0, 0)
        self.keywords_layout.setSpacing(5)
        self.keywords_layout.setAlignment(Qt.AlignLeft)
        
        # 创建一个容器widget
        self.keywords_widget = QWidget()
        self.keywords_widget.setLayout(self.keywords_layout)
        
        # 将keywords_widget添加到UI中适当的位置
        # 注意：这里的具体位置需要根据你的UI布局调整
        keywords_container = QWidget(self.ui.scrollAreaWidgetContents)
        keywords_container.setGeometry(QRect(100, 50, 500, 35))
        container_layout = QHBoxLayout(keywords_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.keywords_widget)

    def add_keyword(self):
        """添加关键字"""
        if not self.db_manager:
            QMessageBox.warning(self, "警告", "请先导入数据库！")
            return
            
        keyword = self.ui.lineEdit.text().strip()
        if keyword and keyword not in self.keywords:
            # 创建新的关键字标签
            label = KeywordLabel(keyword, self.keywords_widget)
            
            # 添加到布局
            self.keywords_layout.addWidget(label)
            self.keywords.add(keyword)
            
            # 清空搜索框
            self.ui.lineEdit.clear()
            
            # 连接删除信号
            label.remove_clicked.connect(self.remove_keyword)
            
            # 更新搜索结果
            self.apply_filters()
            
            logging.info(f"添加了关键字：{keyword}")
        else:
            QMessageBox.warning(self, "警告", "关键字为空或已存在！")

    def remove_keyword(self, keyword):
        """移除关键字"""
        try:
            self.keywords.remove(keyword)
            # 移除对应的标签
            for i in range(self.keywords_layout.count()):
                widget = self.keywords_layout.itemAt(i).widget()
                if isinstance(widget, KeywordLabel) and widget.keyword == keyword:
                    widget.deleteLater()
                    break
            
            # 更新搜索结果
            self.apply_filters()
            
            logging.info(f"移除了关键字：{keyword}")
            
        except KeyError:
            logging.warning(f"尝试移除不存在的关键字：{keyword}")

    def apply_filters(self):
        """应用所有筛选条件（关键字和分类）"""
        try:
            current_category = self.ui.comboBox.currentText()
            
            for row in range(self.ui.tableWidget.rowCount()):
                should_show = True
                
                # 检查分类
                if current_category != "全部":
                    category_item = self.ui.tableWidget.item(row, 1)
                    if category_item and category_item.text() != current_category:
                        should_show = False
                
                # 检查关键字
                if should_show and self.keywords:
                    title = self.ui.tableWidget.item(row, 0).text().lower()
                    description = self.ui.tableWidget.item(row, 2).text().lower()
                    
                    # 所有关键字都必须匹配
                    for keyword in self.keywords:
                        if keyword.lower() not in title and keyword.lower() not in description:
                            should_show = False
                            break
                
                self.ui.tableWidget.setRowHidden(row, not should_show)
                
        except Exception as e:
            logging.error(f"应用筛选失败：{e}")
            QMessageBox.critical(self, "错误", f"筛选失败：{str(e)}")

    def setup_table(self):
        """设置表格属性"""
        # 设置表格列数和列标题
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(["标题", "分类", "描述"])
        
        # 设置列宽
        self.ui.tableWidget.setColumnWidth(0, 200)  # 标题列宽
        self.ui.tableWidget.setColumnWidth(1, 100)  # 分类列宽
        self.ui.tableWidget.setColumnWidth(2, 500)  # 描述列宽
        
        # 设置表格可以选择整行
        self.ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        # 设置表格不可编辑
        self.ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # 双击打开详情
        self.ui.tableWidget.doubleClicked.connect(self.show_detail)

    def connect_signals(self):
        """连接信号槽"""
        # 导入数据库按钮
        self.ui.pushButton_import.clicked.connect(self.import_database)
        # 导出按钮
        self.ui.pushButton_export.clicked.connect(self.export_data)
        # 分类筛选
        self.ui.comboBox.currentTextChanged.connect(self.apply_filters)
        # 关键字搜索
        self.ui.pushButton_search.clicked.connect(self.add_keyword)
        # 回车添加关键字
        self.ui.lineEdit.returnPressed.connect(self.add_keyword)

    def setup_logging(self):
        """设置日志"""
        log_dir = os.path.join('resources', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, 'knowledge.log'),
            level=logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s'
        )

    def import_database(self):
        """导入数据库"""
        try:
            # 设置默认数据库文件夹路径
            default_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'db')
            os.makedirs(default_db_path, exist_ok=True)

            db_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择数据库",
                default_db_path,
                "SQLite数据库 (*.db);;所有文件 (*.*)"
            )
            
            if db_path:
                # 关闭现有连接
                if self.db_manager:
                    self.db_manager.close()
                
                # 创建新连接
                self.db_manager = DatabaseManager(db_path)
                self.db_manager.connect()
                self.db_path = db_path
                
                # 更新界面
                self.load_data()
                self.load_categories()
                
                # 启用按钮
                self.set_buttons_enabled(True)
                
                logging.info(f"成功导入数据库：{db_path}")
                
        except Exception as e:
            logging.error(f"导入数据库失败：{e}")
            QMessageBox.critical(self, "错误", f"导入数据库失败：{str(e)}")
            # 导入失败时禁用按钮
            self.set_buttons_enabled(False)

    def export_data(self):
        """导出数据到txt文件"""
        if not self.db_manager:
            QMessageBox.warning(self, "警告", "请先导入数据库！")
            return
        
        try:
            # 获取保存文件路径，确保默认文件名带有.txt扩展名
            default_name = f"{self.db_manager.get_db_name()}_export.txt"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "导出数据",
                os.path.join(os.getcwd(), default_name),  # 使用完整路径
                "文本文件 (*.txt)"  # 只显示txt选项
            )
            
            if not file_path:  # 用户取消选择
                return
            
            # 确保文件有.txt扩展名
            if not file_path.lower().endswith('.txt'):
                file_path += '.txt'
            
            # 其余导出逻辑保持不变
            visible_records = []
            for row in range(self.ui.tableWidget.rowCount()):
                if not self.ui.tableWidget.isRowHidden(row):
                    title = self.ui.tableWidget.item(row, 0).text()
                    category = self.ui.tableWidget.item(row, 1).text()
                    description = self.ui.tableWidget.item(row, 2).text()
                    visible_records.append((title, category, description))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                for index, (title, category, description) in enumerate(visible_records):
                    f.write(f"序号：{index}\n")
                    f.write(f"标题：{title}\n")
                    f.write(f"分类：{category}\n")
                    f.write(f"描述：{description}\n")
                    f.write("-" * 50 + "\n")
            
            QMessageBox.information(self, "成功", "数据导出成功！")
            logging.info(f"成功导出数据到：{file_path}")
            
        except Exception as e:
            logging.error(f"导出数据失败：{e}")
            QMessageBox.critical(self, "错误", f"导出数据失败：{str(e)}")

    def load_data(self):
        """加载数据到表格"""
        try:
            if not self.db_manager:
                return
                
            records = self.db_manager.get_all_records()
            self.ui.tableWidget.setRowCount(len(records))
            
            for row, record in enumerate(records):
                # 只显示标题、分类、描述
                title = QTableWidgetItem(str(record[1]))  # 标题
                category = QTableWidgetItem(str(record[2]))  # 分类
                description = QTableWidgetItem(str(record[3]))  # 描述
                
                self.ui.tableWidget.setItem(row, 0, title)
                self.ui.tableWidget.setItem(row, 1, category)
                self.ui.tableWidget.setItem(row, 2, description)
                
            logging.info("成功加载数据")
            
        except Exception as e:
            logging.error(f"加载数据失败：{e}")
            QMessageBox.critical(self, "错误", f"加载数据失败：{str(e)}")

    def load_categories(self):
        """加载分类到下拉框"""
        try:
            if not self.db_manager:
                return
                
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("全部")
            categories = self.db_manager.get_categories()
            self.ui.comboBox.addItems(categories)
            
        except Exception as e:
            logging.error(f"加载分类失败：{e}")
            QMessageBox.critical(self, "错误", f"加载分类失败：{str(e)}")

    def filter_by_category(self, category):
        """按分类筛选"""
        try:
            for row in range(self.ui.tableWidget.rowCount()):
                if category == "全部":
                    self.ui.tableWidget.setRowHidden(row, False)
                else:
                    category_item = self.ui.tableWidget.item(row, 1)  # 分类在第2列
                    if category_item:
                        self.ui.tableWidget.setRowHidden(
                            row, 
                            category_item.text() != category
                        )
                        
        except Exception as e:
            logging.error(f"分类筛选失败：{e}")
            QMessageBox.critical(self, "错误", f"分类筛选失败：{str(e)}")

    def search_by_keyword(self):
        """关键字搜索"""
        keyword = self.ui.lineEdit.text().strip()
        if not keyword:
            QMessageBox.warning(self, "警告", "请输入搜索关键字！")
            return
            
        try:
            for row in range(self.ui.tableWidget.rowCount()):
                title = self.ui.tableWidget.item(row, 0).text()  # 标题在第1列
                description = self.ui.tableWidget.item(row, 2).text()  # 描述在第3列
                
                # 如果关键字在标题或描述中，显示该行
                if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                    self.ui.tableWidget.setRowHidden(row, False)
                else:
                    self.ui.tableWidget.setRowHidden(row, True)
                    
        except Exception as e:
            logging.error(f"关键字搜索失败：{e}")
            QMessageBox.critical(self, "错误", f"关键字搜索失败：{str(e)}")

    def show_detail(self, index):
        """显示详细信息"""
        try:
            row = index.row()
            records = self.db_manager.get_all_records()
            record_id = records[row][0]  # 从完整记录中获取ID
            
            from show_page.show_page import ShowPage
            # 创建展示页面实例
            detail_page = ShowPage()  # 不设置父窗口，使其成为独立窗口
            # 设置数据库管理器
            detail_page.db_manager = self.db_manager
            detail_page.db_path = self.db_path
            # 加载当前记录的详细信息
            detail_page.display_knowledge_details_by_id(record_id)
            # 设置窗口属性
            detail_page.setWindowModality(Qt.ApplicationModal)  # 设置为模态窗口
            detail_page.resize(800, 600)  # 设置默认大小
            
            # 保存窗口引用
            self.detail_windows.append(detail_page)
            # 连接窗口关闭信号
            detail_page.destroyed.connect(lambda: self.detail_windows.remove(detail_page))
            
            # 显示窗口
            detail_page.show()
            
            logging.info(f"打开记录ID={record_id}的详细信息")
            
        except Exception as e:
            logging.error(f"显示详情失败：{e}")
            QMessageBox.critical(self, "错误", f"显示详情失败：{str(e)}")

    def set_buttons_enabled(self, enabled=True):
        """设置按钮的启用状态"""
        # 设置按钮状态
        self.ui.pushButton_export.setEnabled(enabled)
        self.ui.pushButton_search.setEnabled(enabled)
        self.ui.lineEdit.setEnabled(enabled)
        self.ui.comboBox.setEnabled(enabled)
        
        # 如果是禁用状态，清空并禁用表格
        if not enabled:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setEnabled(False)
            # 清空关键字
            self.keywords.clear()
            while self.keywords_layout.count():
                item = self.keywords_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            self.ui.tableWidget.setEnabled(True)
    

