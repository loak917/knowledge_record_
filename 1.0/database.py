# version1.0版本数据库
import sqlite3
from datetime import datetime
import io
import os
import shutil
import uuid
import json

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.image_dir = os.path.join(os.path.dirname(db_path), "images")
        os.makedirs(self.image_dir, exist_ok=True)
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS 分类 (
            id INTEGER PRIMARY KEY,
            名称 TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
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
        ''')
        
        # Check and add new columns
        self.cursor.execute("PRAGMA table_info(知识项)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "创建日期" not in columns:
            self.cursor.execute("ALTER TABLE 知识项 ADD COLUMN 创建日期 TEXT")
        if "最新日期" not in columns:
            self.cursor.execute("ALTER TABLE 知识项 ADD COLUMN 最新日期 TEXT")
        
        self.conn.commit()

    def add_category(self, name):
        self.cursor.execute('INSERT INTO 分类 (名称) VALUES (?)', (name,))
        self.conn.commit()

    def get_categories(self):
        self.cursor.execute('SELECT * FROM 分类')
        return self.cursor.fetchall()

    def add_knowledge_item(self, category_id, index, content, image_paths):
        category = self.get_category_by_id(category_id)
        new_relative_paths = self.save_images(category[1], image_paths)
        image_data = json.dumps(new_relative_paths)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO 知识项 (分类_id, 主题索引, 内容, 图片, 创建日期, 最新日期)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category_id, index, content, image_data, current_time, current_time))
        self.conn.commit()

    def get_category_by_id(self, category_id):
        self.cursor.execute('SELECT * FROM 分类 WHERE id = ?', (category_id,))
        return self.cursor.fetchone()

    def save_images(self, category_name, image_paths):
        category_dir = os.path.join(self.image_dir, category_name)
        os.makedirs(category_dir, exist_ok=True)
        relative_paths = []
        for path in image_paths:
            if path:
                file_extension = os.path.splitext(path)[1]
                new_filename = f"{uuid.uuid4()}{file_extension}"
                new_path = os.path.join(category_dir, new_filename)
                shutil.copy(path, new_path)
                relative_paths.append(os.path.relpath(new_path, self.image_dir))
        return relative_paths

    def serialize_images(self, image_paths):
        return json.dumps(image_paths)

    def deserialize_images(self, serialized_images):
        if not serialized_images:
            return []
        return json.loads(serialized_images)

    def get_full_image_path(self, relative_path):
        return os.path.join(self.image_dir, relative_path)

    def get_knowledge_items(self, category_id=None):
        if category_id:
            self.cursor.execute('SELECT * FROM 知识项 WHERE 分类_id = ?', (category_id,))
        else:
            self.cursor.execute('SELECT * FROM 知识项')
        return self.cursor.fetchall()

    def search_knowledge_items(self, search_text):
        self.cursor.execute('SELECT * FROM 知识项 WHERE 主题索引 LIKE ? OR 内容 LIKE ?', ('%' + search_text + '%', '%' + search_text + '%'))
        return self.cursor.fetchall()

    def delete_knowledge_item(self, item_id):
        self.cursor.execute('DELETE FROM 知识项 WHERE id = ?', (item_id,))
        self.conn.commit()

    def update_knowledge_item(self, item_id, category_name, new_index, new_content, new_images, deleted_images):
        # 处理删除的图片
        for image_path in deleted_images:
            full_path = os.path.join(self.image_dir, image_path)
            if os.path.exists(full_path):
                os.remove(full_path)

        # 处理新图片和已存在的图片
        new_relative_paths = []
        for image_path in new_images:
            if image_path.startswith("temp"):
                # 这是一个新添加的图片，需要移动到正确的位置
                new_filename = os.path.basename(image_path)
                new_relative_path = os.path.join(category_name, new_filename)
                new_full_path = os.path.join(self.image_dir, new_relative_path)
                os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
                temp_path = os.path.join(self.image_dir, image_path)
                if os.path.exists(temp_path):
                    shutil.move(temp_path, new_full_path)
                    new_relative_paths.append(new_relative_path)
            else:
                # 这是一个已存在的图片
                new_relative_paths.append(image_path)

        # 更新数据库
        image_data = json.dumps(new_relative_paths)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute("PRAGMA table_info(知识项)")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        if "最新日期" in columns:
            self.cursor.execute('''
                UPDATE 知识项
                SET 主题索引 = ?, 内容 = ?, 图片 = ?, 最新日期 = ?
                WHERE id = ?
            ''', (new_index, new_content, image_data, current_time, item_id))
        else:
            self.cursor.execute('''
                UPDATE 知识项
                SET 主题索引 = ?, 内容 = ?, 图片 = ?
                WHERE id = ?
            ''', (new_index, new_content, image_data, item_id))
        
        self.conn.commit()

    def rename_category(self, old_name, new_name):
        self.cursor.execute('UPDATE 分类 SET 名称 = ? WHERE 名称 = ?', (new_name, old_name))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_category(self, category_id):
        self.cursor.execute('UPDATE 分类 SET deleted = 1 WHERE id = ?', (category_id,))
        self.conn.commit()

    def restore_category(self, category_id, category_name):
        self.cursor.execute('INSERT OR REPLACE INTO 分类 (id, 名称) VALUES (?, ?)', (category_id, category_name))
        self.cursor.execute('UPDATE 知识项 SET 分类_id = ? WHERE 分类_id IS NULL', (category_id,))
        self.conn.commit()

    def confirm_delete_category(self, category_id):
        self.cursor.execute('DELETE FROM 知识项 WHERE 分类_id = ?', (category_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()