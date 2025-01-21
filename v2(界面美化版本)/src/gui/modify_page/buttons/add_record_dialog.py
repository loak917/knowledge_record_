from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QTextEdit, QListWidget, QFileDialog, QMessageBox, QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt
import os
import shutil
import logging
import time

"""
打开新的知识点添加对话框
"""

class AddRecordDialog(QDialog):
    def __init__(self, parent=None, categories=None,db_name=None):
        super(AddRecordDialog, self).__init__(parent)
        self.setWindowTitle("添加新知识点")
        self.setMinimumSize(700, 500)
        self.db_name = db_name

        self.images = []  # 存储选中的图片路径

        layout = QVBoxLayout()

        # 标题
        layout.addWidget(QLabel("标题:"))
        self.title_edit = QLineEdit()
        self.title_edit.setMaxLength(100)  # 设置标题最大长度
        layout.addWidget(self.title_edit)

        # 分类
        layout.addWidget(QLabel("分类:"))
        self.category_combo = QComboBox()
        if categories:
            self.category_combo.addItems(categories)
        layout.addWidget(self.category_combo)

        # 内容
        layout.addWidget(QLabel("内容:"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(150)  # 限制描述框高度
        layout.addWidget(self.description_edit)

        # 图片选择
        img_layout = QHBoxLayout()
        self.add_image_button = QPushButton("添加图片")
        self.add_image_button.clicked.connect(self.add_images)
        self.remove_image_button = QPushButton("移除选中图片")
        self.remove_image_button.clicked.connect(self.remove_selected_image)
        img_layout.addWidget(self.add_image_button)
        img_layout.addWidget(self.remove_image_button)
        layout.addLayout(img_layout)

        # 图片列表
        self.image_list = QListWidget()
        layout.addWidget(QLabel("已添加的图片:"))
        layout.addWidget(self.image_list)

        # 确认和取消按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_images(self):
        """选择并添加图片"""
        image_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if image_paths:
            for path in image_paths:
                if path not in self.images:
                    self.images.append(path)
                    item = QListWidgetItem(os.path.basename(path))
                    self.image_list.addItem(item)
                else:
                    QMessageBox.warning(self, "警告", f"图片 {os.path.basename(path)} 已经添加过了。")

    def remove_selected_image(self):
        """移除选中的图片"""
        selected_items = self.image_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要移除的图片。")
            return
        for item in selected_items:
            index = self.image_list.row(item)
            removed_path = self.images.pop(index)
            self.image_list.takeItem(index)
            logging.info(f"移除图片：{removed_path}")

    def get_data(self):
        """获取用户输入的数据并处理图片保存"""
        title = self.title_edit.text().strip()
        category = self.category_combo.currentText().strip()
        description = self.description_edit.toPlainText().strip()
        image_paths = self.images  # 直接使用完整路径
        images_str = ",".join(image_paths)

        return title, category, description, images_str

    def accept(self):
        data = self.get_data()
        if data:
            title, category, description, images_str = data
            try:
                # 插入新记录到数据库
                self.parent().db_manager.add_record(title, category, description, images_str,soft_modify=0)
                image_target_path = "resources/image/" + self.db_name + "/" 
                if not os.path.exists(image_target_path):
                    os.makedirs(image_target_path)
                if images_str:
                    image_paths = images_str.split(",")
                    for image_path in image_paths:
                        if not self.image_name_exist(image_path,self.get_all_image_name(image_target_path)):
                            continue
                        shutil.copy(image_path, image_target_path)#将图片复制到目标路径
                QMessageBox.information(self, "成功", "新知识点已添加。")
                logging.info(f"添加新知识点：标题={title}, 分类={category}")
                super().accept()
            except Exception as e:
                logging.error(f"添加知识点失败：{e}")
                QMessageBox.critical(self, "错误", f"添加知识点失败：{str(e)}")
        else:
            logging.warning("获取知识点数据失败，未保存。")

    def image_name_exist(self,image_name,image_names):
        """检查图片名称是否已存在"""
        for image_name in image_names:
            if os.path.exists(image_name):
                return True
        logging.warning("图片名称已存在")
        return False
    
    def get_all_image_name(self,path_folder):
        """获取所有图片名称"""
        image_names = []
        for root, dirs, files in os.walk(path_folder):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_names.append(file)
        return image_names

    


