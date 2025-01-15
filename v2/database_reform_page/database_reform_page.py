from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog
from PySide6.QtCore import Qt
from .database_reform_ui import Ui_database_reform
from .database_versions import DatabaseVersion, DatabaseVersionManager
import os
import logging

class DatabaseReformPage(QWidget):
    def __init__(self, parent=None):
        super(DatabaseReformPage, self).__init__(parent)
        self.ui = Ui_database_reform()
        self.ui.setupUi(self)
        
        # 初始化版本选项
        self.ui.comboBox_current_version.clear()
        self.ui.comboBox_target_version.clear()
        self.ui.comboBox_current_version.addItems([v.value for v in DatabaseVersion])
        self.ui.comboBox_target_version.addItems([v.value for v in DatabaseVersion])
        
        # 禁用当前版本选择（因为会自动检测）
        self.ui.comboBox_current_version.setEnabled(False)
        
        # 连接信号
        self.ui.pushButton_select_db.clicked.connect(self.select_database)
        self.ui.pushButton_select_save_path.clicked.connect(self.select_save_path)
        self.ui.pushButton_start.clicked.connect(self.start_conversion)
        
        # 设置默认目标版本为V2
        default_target_index = self.ui.comboBox_target_version.findText(DatabaseVersion.V2.value)
        if default_target_index >= 0:
            self.ui.comboBox_target_version.setCurrentIndex(default_target_index)
        
    def select_database(self):
        """选择数据库文件并自动检测版本"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择数据库文件",
            "",
            "SQLite数据库 (*.db);;所有文件 (*.*)"
        )
        if file_path:
            self.ui.lineEdit_db_path.setText(file_path)
            self.ui.label_db_name.setText(os.path.basename(file_path))
            
            try:
                # 自动检测版本
                version = DatabaseVersionManager.detect_version(file_path)
                index = self.ui.comboBox_current_version.findText(version.value)
                if index >= 0:
                    self.ui.comboBox_current_version.setCurrentIndex(index)
                    self.log_message(f"检测到数据库版本：{version.value}")
                    
                    # 自动设置目标版本为另一个版本
                    target_version = DatabaseVersion.V2 if version == DatabaseVersion.V1 else DatabaseVersion.V1
                    target_index = self.ui.comboBox_target_version.findText(target_version.value)
                    if target_index >= 0:
                        self.ui.comboBox_target_version.setCurrentIndex(target_index)
                        
                    # 自动生成默认保存路径
                    default_save_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{target_version.value}.db"
                    default_save_path = os.path.join(os.path.dirname(file_path), default_save_name)
                    self.ui.lineEdit_save_path.setText(default_save_path)
                    
            except Exception as e:
                self.log_message(f"检测数据库版本失败：{str(e)}", "error")
                QMessageBox.warning(self, "警告", f"无法识别数据库版本：{str(e)}")
                
    def select_save_path(self):
        """选择保存路径"""
        # 获取当前文件名（如果有）
        current_path = self.ui.lineEdit_save_path.text()
        initial_path = current_path if current_path else ""
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "选择保存位置",
            initial_path,
            "SQLite数据库 (*.db);;所有文件 (*.*)"
        )
        if file_path:
            # 确保文件扩展名为.db
            if not file_path.lower().endswith('.db'):
                file_path += '.db'
            self.ui.lineEdit_save_path.setText(file_path)
            
    def start_conversion(self):
        """开始转换"""
        source_path = self.ui.lineEdit_db_path.text()
        target_path = self.ui.lineEdit_save_path.text()
        
        if not source_path or not target_path:
            QMessageBox.warning(self, "警告", "请选择源数据库和保存路径")
            return
            
        if os.path.exists(target_path):
            reply = QMessageBox.question(
                self,
                "确认覆盖",
                "目标文件已存在，是否覆盖？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
            
        try:
            from_version = DatabaseVersion(self.ui.comboBox_current_version.currentText())
            to_version = DatabaseVersion(self.ui.comboBox_target_version.currentText())
            
            if from_version == to_version:
                self.log_message("源版本和目标版本相同，将直接复制数据库文件")
            
            self.log_message(f"开始转换：{from_version.value} -> {to_version.value}")
            success = DatabaseVersionManager.convert_database(
                source_path, target_path, from_version, to_version
            )
            
            if success:
                self.log_message("数据库转换成功！")
                QMessageBox.information(self, "成功", "数据库转换完成！")
            else:
                self.log_message("数据库转换失败", "error")
                QMessageBox.critical(self, "错误", "数据库转换失败，请查看日志")
                
        except Exception as e:
            self.log_message(f"转换过程出错：{str(e)}", "error")
            QMessageBox.critical(self, "错误", f"转换过程出错：{str(e)}")
            
    def log_message(self, message, level="info"):
        """添加日志消息到文本框"""
        if level == "error":
            message = f"错误：{message}"
            color = "red"
        else:
            color = "black"
            
        self.ui.textEdit_log.append(f'<p style="color: {color};">{message}</p>')   