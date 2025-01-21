from enum import Enum
import sqlite3
import logging
import json
import os

class DatabaseVersion(Enum):
    V1 = "V1"
    V2 = "V2"

class DatabaseVersionManager:
    VERSION_SCHEMAS = {
        DatabaseVersion.V1: {
            "tables": {
                "分类": """
                    CREATE TABLE IF NOT EXISTS 分类 (
                        id INTEGER PRIMARY KEY,
                        名称 TEXT NOT NULL
                    )
                """,
                "知识项": """
                    CREATE TABLE IF NOT EXISTS 知识项 (
                        id INTEGER PRIMARY KEY,
                        分类_id INTEGER,
                        主题索引 TEXT,
                        内容 TEXT,
                        图片 TEXT,
                        创建日期 TEXT,
                        最新日期 TEXT,
                        FOREIGN KEY (分类_id) REFERENCES 分类(id)
                    )
                """
            }
        },
        DatabaseVersion.V2: {
            "tables": {
                "knowledge": """
                    CREATE TABLE IF NOT EXISTS knowledge (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        category TEXT,
                        images TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        soft_modify INTEGER DEFAULT 0
                    )
                """,
                "categories": """
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )
                """
            }
        }
    }

    @staticmethod
    def detect_version(db_path):
        """检测数据库版本"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 检查表结构
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            
            # V1版本特有的表名是中文的
            if "分类" in tables and "知识项" in tables:
                return DatabaseVersion.V1
            # V2版本使用英文表名
            elif "knowledge" in tables and "categories" in tables:
                return DatabaseVersion.V2
            else:
                raise ValueError("无法识别的数据库版本")
                
        except sqlite3.Error as e:
            logging.error(f"检测数据库版本失败：{e}")
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def convert_database(source_path, target_path, from_version, to_version):
        """转换数据库版本
        
        Args:
            source_path (str): 源数据库路径
            target_path (str): 目标数据库路径
            from_version (DatabaseVersion): 源版本
            to_version (DatabaseVersion): 目标版本
            
        Returns:
            bool: 转换是否成功
        """
        if from_version == to_version:
            return True
            
        try:
            # 复制源数据库到目标路径
            import shutil
            shutil.copy2(source_path, target_path)
            
            # 连接新数据库
            conn = sqlite3.connect(target_path)
            cursor = conn.cursor()
            
            if from_version == DatabaseVersion.V1 and to_version == DatabaseVersion.V2:
                # V1 到 V2 的转换逻辑
                # 1. 创建新表
                for table_sql in DatabaseVersionManager.VERSION_SCHEMAS[DatabaseVersion.V2]["tables"].values():
                    cursor.execute(table_sql)
                
                # 2. 转换分类数据
                cursor.execute("SELECT id, 名称 FROM 分类")
                categories = cursor.fetchall()
                for _, name in categories:
                    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
                
                # 3. 转换知识项数据
                cursor.execute("""
                    SELECT 知识项.id, 知识项.主题索引, 知识项.内容, 分类.名称, 知识项.图片, 知识项.创建日期
                    FROM 知识项 
                    LEFT JOIN 分类 ON 知识项.分类_id = 分类.id
                """)
                items = cursor.fetchall()
                for _, title, description, category, images, created_at in items:
                    # 处理图片路径
                    image_paths = json.loads(images) if images else []
                    new_images = json.dumps(image_paths) if image_paths else None
                    
                    cursor.execute("""
                        INSERT INTO knowledge (title, description, category, images, created_at, soft_modify)
                        VALUES (?, ?, ?, ?, ?, 0)
                    """, (title, description, category, new_images, created_at))
                
                # 4. 删除旧表
                cursor.execute("DROP TABLE IF EXISTS 知识项")
                cursor.execute("DROP TABLE IF EXISTS 分类")
                
            elif from_version == DatabaseVersion.V2 and to_version == DatabaseVersion.V1:
                # V2 到 V1 的转换逻辑
                # 1. 创建新表
                for table_sql in DatabaseVersionManager.VERSION_SCHEMAS[DatabaseVersion.V1]["tables"].values():
                    cursor.execute(table_sql)
                
                # 2. 转换分类数据
                cursor.execute("SELECT name FROM categories")
                categories = cursor.fetchall()
                category_map = {}  # 用于存储新旧ID的映射
                for name, in categories:
                    cursor.execute("INSERT INTO 分类 (名称) VALUES (?)", (name,))
                    category_map[name] = cursor.lastrowid
                
                # 3. 转换知识项数据
                cursor.execute("SELECT title, description, category, images, created_at FROM knowledge")
                items = cursor.fetchall()
                for title, description, category, images, created_at in items:
                    category_id = category_map.get(category) if category else None
                    current_time = created_at or "2024-01-01 00:00:00"  # 默认时间
                    
                    cursor.execute("""
                        INSERT INTO 知识项 (分类_id, 主题索引, 内容, 图片, 创建日期, 最新日期)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (category_id, title, description, images, current_time, current_time))
                
                # 4. 删除旧表
                cursor.execute("DROP TABLE IF EXISTS knowledge")
                cursor.execute("DROP TABLE IF EXISTS categories")
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            logging.error(f"转换数据库失败：{e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
