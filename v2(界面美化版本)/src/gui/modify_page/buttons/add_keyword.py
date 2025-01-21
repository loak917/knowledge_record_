from PySide6.QtWidgets import QMessageBox
import logging
from src.tools.flowlayout import KeywordLabel

"""
添加关键字（标签）
"""

class AddKeyword:
    def __init__(self, parent, line_edit, keywords_set, layout):
        self.parent = parent
        self.line_edit = line_edit
        self.keywords = keywords_set
        self.layout = layout

    def execute(self):
        keyword = self.line_edit.text().strip()
        if keyword and keyword not in self.keywords:
            # 创建新的关键字标签
            label = KeywordLabel(keyword, self.parent.keywords_widget)
            
            # 添加到布局
            self.layout.addWidget(label)
            self.keywords.add(keyword)
            
            # 清空搜索框
            self.line_edit.clear()
            
            # 连接删除信号
            label.remove_clicked.connect(self.parent.remove_keyword)
            
            # 更新搜索结果
            self.parent.apply_filters()
            
            logging.info(f"添加了关键字：{keyword}")
        else:
            QMessageBox.warning(self.parent, "警告", "关键字为空或已存在！")
            logging.warning("尝试添加空或已存在的关键字。")
    
    def remove_keyword(self, keyword):
        """移除关键字并更新相关数据"""
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.parent.apply_filters()
            logging.info(f"移除关键字：{keyword}")
            # 手动刷新布局
            self.parent.keywords_layout.update()
        else:
            logging.warning(f"尝试移除不存在的关键字：{keyword}")
