import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from database import Database
import io
import os
import shutil
from datetime import datetime
import uuid

class ShowKnowledge:
    def __init__(self, master, return_callback, db):
        self.master = master
        self.return_callback = return_callback
        self.db = db
        self.master.title("显示知识")
        self.master.geometry("800x600")
        self.temp_images = []  # 用于存储临时添加的图片路径

        self.create_widgets()
        self.load_categories()
        self.load_items()

    def create_widgets(self):
        # 返回按钮固定在左上角
        self.return_button = tk.Button(self.master, text="返回", command=self.return_callback, font=("Microsoft YaHei", 12))
        self.return_button.place(x=10, y=10)

        # 创建主框架
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=50)

        # 分类选择（居中显示）
        category_frame = tk.Frame(main_frame)
        category_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(category_frame, text="分类:", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT, padx=(200, 5))
        self.category_list = ttk.Combobox(category_frame, state="readonly", font=("Microsoft YaHei", 12), width=30)
        self.category_list.pack(side=tk.LEFT)

        # 搜索框架
        search_frame = tk.Frame(main_frame)
        search_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # 搜索方式选择
        self.search_mode = tk.StringVar(value="主题索引")
        tk.Radiobutton(search_frame, text="主题索引", variable=self.search_mode, value="主题索引", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT)
        tk.Radiobutton(search_frame, text="内容", variable=self.search_mode, value="内容", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT)

        # 搜索输入和按钮
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Microsoft YaHei", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(search_frame, text="查找", command=self.search_knowledge, font=("Microsoft YaHei", 12))
        self.search_button.pack(side=tk.LEFT)

        # 创建Treeview和滚动条的框架
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=10)

        # Treeview
        self.item_list = ttk.Treeview(tree_frame, columns=('ID', '最新日期', '分类', '主题索引', '内容'), show='headings', height=15)
        self.item_list.heading('ID', text='ID')
        self.item_list.heading('最新日期', text='最新日期')
        self.item_list.heading('分类', text='分类')
        self.item_list.heading('主题索引', text='主题索引')
        self.item_list.heading('内容', text='内容')
        self.item_list.column('ID', width=50)
        self.item_list.column('最新日期', width=100)
        self.item_list.column('分类', width=100)
        self.item_list.column('主题索引', width=150)
        self.item_list.column('内容', width=300)
        self.item_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.item_list.bind('<<TreeviewSelect>>', self.on_item_select)

        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.item_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.item_list.configure(yscrollcommand=scrollbar.set)

        # 添加导出按钮
        self.export_button = tk.Button(main_frame, text="导出为TXT", command=self.export_to_txt, font=("Microsoft YaHei", 12))
        self.export_button.pack(side=tk.TOP, pady=10)

    def load_categories(self):
        categories = self.db.get_categories()
        self.category_list['values'] = ['全部'] + [cat[1] for cat in categories]
        self.category_list.current(0)
        self.category_list.bind('<<ComboboxSelected>>', self.on_category_select)

    def on_category_select(self, event):
        self.load_items()

    def load_items(self):
        selected_category = self.category_list.get()
        if selected_category == '全部':
            items = self.db.get_knowledge_items()
        else:
            category_id = next(cat[0] for cat in self.db.get_categories() if cat[1] == selected_category)
            items = self.db.get_knowledge_items(category_id)

        self.item_list.delete(*self.item_list.get_children())
        for item in items:
            category = next(cat[1] for cat in self.db.get_categories() if cat[0] == item[1])
            date = datetime.strptime(item[6], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            self.item_list.insert('', 'end', values=(item[0], date, category, item[2], item[3]))

    def search_knowledge(self):
        search_text = self.search_var.get().lower()
        search_mode = self.search_mode.get()
        items = self.db.search_knowledge_items(search_text)
        self.item_list.delete(*self.item_list.get_children())
        for item in items:
            category = next(cat[1] for cat in self.db.get_categories() if cat[0] == item[1])
            if (search_mode == "主题索引" and search_text in item[2].lower()) or \
               (search_mode == "内容" and search_text in item[3].lower()):
                self.item_list.insert('', 'end', values=(item[0], item[6], category, item[2], item[3]))

    def on_item_select(self, event):
        selected_items = self.item_list.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        item_id = self.item_list.item(selected_item)['values'][0]
        item = next(item for item in self.db.get_knowledge_items() if item[0] == item_id)
        
        detail_window = tk.Toplevel(self.master)
        detail_window.title("详细内容")
        detail_window.geometry("800x600")

        tk.Label(detail_window, text="主题索引:", font=("Microsoft YaHei", 12)).pack(anchor='w', padx=10, pady=5)
        index_entry = tk.Entry(detail_window, width=50, font=("Microsoft YaHei", 12))
        index_entry.insert(0, item[2])
        index_entry.pack(padx=10, pady=5)

        tk.Label(detail_window, text="内容:", font=("Microsoft YaHei", 12)).pack(anchor='w', padx=10, pady=5)
        
        # 创建一个框架来容纳文本框和滚动条
        content_frame = tk.Frame(detail_window)
        content_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # 添加滚动条
        content_scrollbar = tk.Scrollbar(content_frame)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文本框并关联滚动条
        content_text = tk.Text(content_frame, height=10, width=50, font=("Microsoft YaHei", 12), yscrollcommand=content_scrollbar.set)
        content_text.insert(tk.END, item[3])
        content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        content_scrollbar.config(command=content_text.yview)

        image_frame = tk.Frame(detail_window)
        image_frame.pack(padx=10, pady=10)

        self.image_labels = []
        self.deleted_images = []
        if item[4]:  # If there's image data
            image_paths = self.db.deserialize_images(item[4])
            for relative_path in image_paths:
                try:
                    full_path = self.db.get_full_image_path(relative_path)
                    self.display_image(image_frame, full_path, relative_path)
                except Exception as e:
                    print(f"Error loading image: {e}")
                    messagebox.showerror("错误", f"加载图片时出错: {e}")

        add_image_button = tk.Button(detail_window, text="添加图片", command=lambda: self.add_image(image_frame), font=("Microsoft YaHei", 12))
        add_image_button.pack(pady=5)

        save_button = tk.Button(detail_window, text="保存修改", command=lambda: self.save_changes(item[0], index_entry, content_text, detail_window), font=("Microsoft YaHei", 12))
        save_button.pack(pady=10)

    def display_image(self, frame, image_path, relative_path):
        image = Image.open(image_path)
        image.thumbnail((200, 200))  # Increase thumbnail size
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo)
        image_label.image = photo  # Keep a reference
        image_label.pack(side=tk.LEFT, padx=5)
        
        # 添加点击事件以放大查看图片
        image_label.bind("<Button-1>", lambda e, img=image_path: self.show_full_image(img))
        
        delete_button = tk.Button(frame, text="删除", command=lambda: self.delete_image(image_label, relative_path))
        delete_button.pack(side=tk.LEFT)
        
        self.image_labels.append((image_label, delete_button, relative_path))

    def show_full_image(self, image_path):
        full_image_window = tk.Toplevel(self.master)
        full_image_window.title("图片查看")
        full_image_window.geometry("800x600")

        # 创建一个框架来容纳画布和滚动条
        frame = tk.Frame(full_image_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # 创建画布
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(full_image_window, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # 配置画布
        canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # 打开并显示图片
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        
        # 在画布上创建图片
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo  # 保持对图片的引用

        # 设置滚动区域
        canvas.configure(scrollregion=canvas.bbox("all"))

        # 添加缩放功能
        def zoom(event):
            if event.delta > 0:
                canvas.scale("all", event.x, event.y, 1.1, 1.1)
            elif event.delta < 0:
                canvas.scale("all", event.x, event.y, 0.9, 0.9)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<MouseWheel>", zoom)

        # 添加拖动功能
        def move_start(event):
            canvas.scan_mark(event.x, event.y)

        def move_move(event):
            canvas.scan_dragto(event.x, event.y, gain=1)

        canvas.bind("<ButtonPress-1>", move_start)
        canvas.bind("<B1-Motion>", move_move)

    def delete_image(self, image_label, relative_path):
        for label, button, path in self.image_labels:
            if path == relative_path:
                label.destroy()
                button.destroy()
                self.image_labels.remove((label, button, path))
                break
        self.deleted_images.append(relative_path)

    def add_image(self, frame):
        image_paths = filedialog.askopenfilenames(filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif")])
        for path in image_paths:
            # 生成一个新的唯一文件名
            new_filename = f"{uuid.uuid4()}{os.path.splitext(path)[1]}"
            # 使用新文件名作为相对路径
            relative_path = os.path.join("temp", new_filename)
            # 复制图片到临时文件夹
            temp_dir = os.path.join(self.db.image_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, new_filename)
            shutil.copy(path, temp_path)
            self.display_image(frame, temp_path, relative_path)
            self.temp_images.append(relative_path)

    def save_changes(self, item_id, index_entry, content_text, detail_window):
        new_index = index_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        
        # 获取当前项的类别
        current_item = next(item for item in self.db.get_knowledge_items() if item[0] == item_id)
        category_id = current_item[1]
        category_name = next(cat[1] for cat in self.db.get_categories() if cat[0] == category_id)
        
        # 处理新添加的图片和已存在的图片
        new_images = []
        for _, _, path in self.image_labels:
            if path in self.temp_images:
                # 这是一个新添加的图片
                new_images.append(path)
            else:
                # 这是一个已存在的图片
                new_images.append(path)

        self.db.update_knowledge_item(item_id, category_name, new_index, new_content, new_images, self.deleted_images)
        detail_window.destroy()
        self.load_items()
        self.temp_images = []  # 清空临时图片列表

    def export_to_txt(self):
        selected_category = self.category_list.get()
        if selected_category == '全部':
            items = self.db.get_knowledge_items()
            filename = "全部类别"
        else:
            category_id = next(cat[0] for cat in self.db.get_categories() if cat[1] == selected_category)
            items = self.db.get_knowledge_items(category_id)
            filename = selected_category

        if not items:
            messagebox.showinfo("提示", "没有可导出的内容")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text files", "*.txt")],
                                                 initialfile=f"{filename}.txt")
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for index, item in enumerate(items, start=1):
                    category = next(cat[1] for cat in self.db.get_categories() if cat[0] == item[1])
                    f.write(f"{index}. {item[2]}\n{item[3]}\n\n")

            messagebox.showinfo("成功", f"已成功导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShowKnowledge(root, lambda: root.destroy(), Database("test.db"))
    root.mainloop()