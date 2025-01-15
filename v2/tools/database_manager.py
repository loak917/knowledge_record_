# version2.0版本数据库
import sqlite3
import os
import shutil
import logging

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """连接到SQLite数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            logging.info("成功连接到数据库。")
            self.create_tables()
            self.migrate_tables()
        except sqlite3.Error as e:
            logging.error(f"数据库连接失败：{e}")
            raise e

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
            logging.info("数据库连接已关闭。")

    def create_tables(self):
        """创建必要的表格"""
        try:
            cursor = self.conn.cursor()
            # 创建知识点表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT,
                    images TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    soft_modify INTEGER DEFAULT 0
                )
            ''')
            # 创建分类表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            self.conn.commit()
            logging.info("表格创建或已存在。")
        except sqlite3.Error as e:
            logging.error(f"创建表格失败：{e}")
            raise e

    def migrate_tables(self):
        """迁移表结构，添加缺失的列"""
        try:
            cursor = self.conn.cursor()
            # 检查 knowledge 表是否存在 images 列
            cursor.execute("PRAGMA table_info(knowledge)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'images' not in columns:
                cursor.execute("ALTER TABLE knowledge ADD COLUMN images TEXT")
                self.conn.commit()
                logging.info("已向 'knowledge' 表添加 'images' 列。")
            else:
                logging.info("'knowledge' 表已包含 'images' 列。")
        except sqlite3.Error as e:
            logging.error(f"迁移表结构失败：{e}")
            raise e

    def add_category(self, category):
        """添加新分类"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
            self.conn.commit()
            logging.info(f"添加分类：{category}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"分类 '{category}' 已存在。")
            return False
        except sqlite3.Error as e:
            logging.error(f"添加分类失败：{e}")
            raise e

    def remove_category(self, category, delete_related=False):
        """删除分类
        Args:
            category (str): 要删除的分类名称
            delete_related (bool): 是否删除相关的知识点记录
        """
        try:
            cursor = self.conn.cursor()
            self.conn.execute('BEGIN')
            if delete_related:
                cursor.execute("DELETE FROM knowledge WHERE category = ?", (category,))
                logging.info(f"删除分类 '{category}' 及其相关知识点记录。")
            else:
                # 将相关知识点的分类设置为默认分类
                default_category = '未归类'
                if default_category not in self.get_categories():
                    self.add_category(default_category)
                cursor.execute("UPDATE knowledge SET category = ? WHERE category = ?", (default_category, category))
                logging.info(f"将分类 '{category}' 的知识点重新分配到 '{default_category}'。")
            cursor.execute("DELETE FROM categories WHERE name = ?", (category,))
            self.conn.commit()
            logging.info(f"删除分类：{category}")
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"删除分类失败：{e}")
            return False

    def get_categories(self):
        """获取所有分类"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM categories")
            categories = [row[0] for row in cursor.fetchall()]
            return categories
        except sqlite3.Error as e:
            logging.error(f"获取分类失败：{e}")
            return []

    def reassign_category(self, old_category, new_category='未归类'):
        """重新分配知识点的分类"""
        try:
            self.conn.execute('BEGIN')
            # 确保新分类存在
            if new_category not in self.get_categories():
                self.add_category(new_category)
                logging.info(f"自动添加默认分类：{new_category}")
            cursor = self.conn.cursor()
            cursor.execute("UPDATE knowledge SET category = ? WHERE category = ?", (new_category, old_category))
            self.conn.commit()
            logging.info(f"将分类 '{old_category}' 的知识点重新分配到 '{new_category}'。")
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"重新分配分类失败：{e}")
            raise e

    def add_record(self, title, category, description, images,soft_modify=0):
        """添加知识点记录"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO knowledge (title, category, description, images,soft_modify)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, category, description, images,soft_modify))
            self.conn.commit()
            logging.info(f"添加记录：标题={title}, 分类={category}, 图片路径={images}")
        except sqlite3.Error as e:
            logging.error(f"添加记录失败：{e}")
            raise e

    def update_record(self, record_id, title, category, description, images,soft_modify=0):
        """更新知识点记录"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE knowledge
                SET title = ?, category = ?, description = ?, images = ?,soft_modify = ?
                WHERE id = ?
            ''', (title, category, description, images, soft_modify, record_id))
            self.conn.commit()
            logging.info(f"更新记录ID={record_id}: 标题={title}, 分类={category}")
        except sqlite3.Error as e:
            logging.error(f"更新记录失败：{e}")
            raise e

    def get_all_records(self):
        """获取所有记录"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, title, category, description, images,soft_modify FROM knowledge")
            records = cursor.fetchall()
            logging.info("成功获取所有记录。")
            return records
        except sqlite3.Error as e:
            logging.error(f"获取记录失败：{e}", exc_info=True)
            return []

    def get_record_by_id(self, record_id):
        """通过ID获取单条知识点记录"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, title, category, description, images,soft_modify FROM knowledge WHERE id = ?', (record_id,))
            record = cursor.fetchone()
            return record
        except sqlite3.Error as e:
            logging.error(f"获取记录失败：{e}")
            return None

    def remove_file(self, record_id):
        """根据记录ID删除记录"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM knowledge WHERE id = ?", (record_id,))
            self.conn.commit()
            logging.info(f"删除记录 ID={record_id}")
            return True
        except sqlite3.Error as e:
            logging.error(f"删除记录 ID={record_id} 失败：{e}")
            return False

    def update_file_path(self, old_path, new_path):
        """更新文件路径"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE knowledge SET images = ? WHERE images = ?", (new_path, old_path))
            self.conn.commit()
            logging.info(f"更新文件路径从 {old_path} 到 {new_path}")
            return True
        except sqlite3.Error as e:
            logging.error(f"更新文件路径失败：{e}")
            return False

    def copy_database(self, target_path):
        """复制数据库到目标路径"""
        try:
            if self.conn:
                self.close()
            shutil.copy2(self.db_path, target_path)
            self.connect()
            logging.info(f"数据库已复制到 {target_path}")
            return True
        except Exception as e:
            logging.error(f"复制数据库失败：{e}")
            return False

    def get_db_name(self):
        return os.path.basename(self.db_path).split('.')[0]

    def get_image_name(self):
        """返回该数据库所有的图片名称"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT images FROM knowledge")
        image_names = [row[0] for row in cursor.fetchall()]
        return image_names

    def update_soft_modify(self, record_id, soft_modify=1):
        """仅更新记录的 soft_modify 状态"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE knowledge
                SET soft_modify = ?
                WHERE id = ?
            ''', (soft_modify, record_id))
            self.conn.commit()
            logging.info(f"更新记录ID={record_id}的soft_modify为{soft_modify}")
        except sqlite3.Error as e:
            logging.error(f"更新soft_modify失败：{e}")
            raise e
    
    def get_records_with_soft_modify(self, soft_modify=1):
        """获取soft_modify=1的记录"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, category, description, images,soft_modify FROM knowledge WHERE soft_modify = ?", (soft_modify,))
        records = cursor.fetchall()
        return records  
    

