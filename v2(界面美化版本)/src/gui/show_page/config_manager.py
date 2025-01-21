import json
import os
import logging
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # 确保配置目录存在
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'config')
        os.makedirs(self.config_dir, exist_ok=True)
        
        # 配置文件路径
        self.config_file = os.path.join(self.config_dir, 'settings.json')
        
        # 默认配置
        self.default_config = {
            'font_size': 12,  # 默认字体大小
        }
        
        # 加载配置
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self.default_config.copy()
        except Exception as e:
            logging.error(f"加载配置文件失败：{e}")
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"保存配置文件失败：{e}")
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
        self.save_config()
