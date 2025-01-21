from PySide6.QtWidgets import (
    QDialog, QMessageBox, QFileDialog, QAbstractItemView, 
    QLabel, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from ui.show_modify_ui import Ui_show_modify
from src.core.database_manager import DatabaseManager
import os
import shutil
import logging

class ImagePreviewLabel(QLabel):
    """可点击的图片预览标签"""
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setScaledContents(True)
        self.setMinimumSize(100, 100)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.show_full_image()

    def show_full_image(self):
        """显示完整图片"""
        dialog = QDialog(self.parent())
        dialog.setWindowTitle("图片查看")
        layout = QVBoxLayout()
        
        label = QLabel()
        pixmap = QPixmap(self.image_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.resize(pixmap.width(), pixmap.height())
        dialog.exec()

class ShowModifyPage(QDialog):
    def __init__(self, db_manager: DatabaseManager, record_id: int, parent=None):
        super(ShowModifyPage, self).__init__(parent)
        self.ui = Ui_show_modify()
        self.ui.setupUi(self)
        
        # 设置窗口标题和模态
        self.setWindowTitle("修改记录")
        self.setWindowModality(Qt.ApplicationModal)
        
        self.db_manager = db_manager
        self.record_id = record_id
        self.current_record = None
        self.images = []
        self.db_name = self.db_manager.get_db_name()
        
        # 创建图片预览区域的布局
        self.preview_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.ui.scrollAreaWidgetContents.setLayout(self.preview_layout)

        # 加载记录数据
        self.load_record()

        # 连接按钮信号
        self.ui.pushButton.clicked.connect(self.save_changes)          # 保存
        self.ui.pushButton_3.clicked.connect(self.add_image)          # 添加图片
        self.ui.pushButton_4.clicked.connect(self.delete_image)       # 删除图片
        self.ui.pushButton_2.clicked.connect(self.model_API)          # 大模型

    def load_record(self):
        """加载选中的记录数据到界面"""
        try:
            record = self.db_manager.get_record_by_id(self.record_id)
            if not record:
                QMessageBox.critical(self, "错误", "未找到该记录。")
                self.reject()
                return

            self.current_record = record
            record_id, title, category, description, images, soft_modify = record

            # 设置界面数据
            self.ui.title_edit.setText(title)
            
            # 加载分类到下拉框
            categories = self.db_manager.get_categories()
            self.ui.category_combo.clear()
            self.ui.category_combo.addItems(categories)
            self.ui.category_combo.setCurrentText(category)
            
            self.ui.description_edit.setPlainText(description)

            # 处理图片
            self.images = images.split(',') if images and images.strip() else []
            self.update_image_previews()

        except Exception as e:
            logging.error(f"加载记录失败：{e}")
            QMessageBox.critical(self, "错误", f"加载记录失败：{str(e)}")
            self.reject()

    def update_image_previews(self):
        """更新图片预览"""
        try:
            # 清除现有预览
            while self.preview_layout.count():
                child = self.preview_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # 添加新的预览
            for img_name in self.images:
                if img_name and img_name.strip():
                    img_path = os.path.join('resources', 'image', self.db_name, img_name)
                    if os.path.exists(img_path):
                        preview = ImagePreviewLabel(img_path)
                        pixmap = QPixmap(img_path)
                        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        preview.setPixmap(scaled_pixmap)
                        self.preview_layout.addWidget(preview)

            # 添加弹簧项
            self.preview_layout.addStretch()
            logging.info("图片预览更新成功")
        except Exception as e:
            logging.error(f"更新图片预览失败：{e}")
            QMessageBox.critical(self, "错误", f"更新图片预览失败：{str(e)}")

    def save_changes(self):
        """保存修改内容"""
        try:
            new_title = self.ui.title_edit.text().strip()
            new_category = self.ui.category_combo.currentText().strip()
            new_description = self.ui.description_edit.toPlainText().strip()
            images_str = ",".join(filter(None, self.images))

            if not new_title or not new_category or not new_description:
                QMessageBox.warning(self, "警告", "标题、分类和内容不能为空！")
                return

            self.db_manager.update_record(
                self.record_id, new_title, new_category, 
                new_description, images_str, soft_modify=0
            )
            QMessageBox.information(self, "成功", "记录已成功更新。")
            logging.info(f"记录ID={self.record_id} 已更新。")
            
            # 更新父窗口的表格显示
            if self.parent():
                self.parent().load_existing_records()
                # 如果有分类筛选，重新应用筛选
                current_category = self.parent().ui.comboBox.currentText()
                if current_category != "全部":
                    self.parent().filter_by_category(current_category)
                # 如果有关键字筛选，重新应用筛选
                if self.parent().keywords:
                    self.parent().apply_filters()
            
            # 关闭修改窗口
            self.accept()
            
        except Exception as e:
            logging.error(f"更新记录失败：{e}")
            QMessageBox.critical(self, "错误", f"更新记录失败：{str(e)}")

    def add_image(self):
        """添加图片到记录"""
        try:
            image_paths, _ = QFileDialog.getOpenFileNames(
                self,
                "选择图片",
                "",
                "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            
            if image_paths:
                image_dir = os.path.join('resources', 'image', self.db_name)
                os.makedirs(image_dir, exist_ok=True)
                
                for img_path in image_paths:
                    img_name = os.path.basename(img_path)
                    target_path = os.path.join(image_dir, img_name)

                    # 处理重名文件
                    base, ext = os.path.splitext(img_name)
                    counter = 1
                    while os.path.exists(target_path):
                        img_name = f"{base}_{counter}{ext}"
                        target_path = os.path.join(image_dir, img_name)
                        counter += 1

                    shutil.copy2(img_path, target_path)
                    self.images.append(img_name)
                    logging.info(f"复制图片 {img_path} 到 {target_path}")
                
                self.update_image_previews()

        except Exception as e:
            logging.error(f"添加图片失败：{e}")
            QMessageBox.critical(self, "错误", f"添加图片失败：{str(e)}")

    def delete_image(self):
        """删除选中的图片"""
        try:
            # 获取当前选中的预览图片
            selected_widget = self.ui.scrollArea.widget().childAt(
                self.ui.scrollArea.widget().mapFromGlobal(self.cursor().pos())
            )
            
            if isinstance(selected_widget, ImagePreviewLabel):
                img_name = os.path.basename(selected_widget.image_path)
                confirm = QMessageBox.question(
                    self, "确认删除", 
                    f"确定要删除图片 '{img_name}' 吗？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if confirm == QMessageBox.Yes:
                    # 删除文件
                    if os.path.exists(selected_widget.image_path):
                        os.remove(selected_widget.image_path)
                        logging.info(f"删除图片文件：{selected_widget.image_path}")
                    
                    # 从列表中移除
                    self.images.remove(img_name)
                    
                    # 更新预览
                    self.update_image_previews()
                    logging.info(f"从记录中移除图片：{img_name}")
            else:
                QMessageBox.warning(self, "警告", "请选择要删除的图片。")

        except Exception as e:
            logging.error(f"删除图片失败：{e}")
            QMessageBox.critical(self, "错误", f"删除图片失败：{str(e)}")
    
    def model_API(self):
        """大模型API功能"""
        QMessageBox.information(self, "提示", "大模型API功能暂未实现")
