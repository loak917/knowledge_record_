import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class DeleteKnowledge:
    def __init__(self, master, return_callback, db):
        self.master = master
        self.return_callback = return_callback
        self.db = db
        self.master.title("删除知识")
        self.master.geometry("800x600")  # 增加窗口大小

        self.create_widgets()
        self.load_categories()
        self.load_items()

    def create_widgets(self):
        # 返回按钮
        self.return_button = tk.Button(self.master, text="返回", command=self.return_callback, font=("Microsoft YaHei", 12))
        self.return_button.pack(anchor='nw', padx=10, pady=10)

        # 分类筛选
        filter_frame = tk.Frame(self.master)
        filter_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(filter_frame, text="筛选分类:", font=("Microsoft YaHei", 12)).pack(side='left')
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly", font=("Microsoft YaHei", 12), width=20)
        self.category_combobox.pack(side='left', padx=5)
        tk.Button(filter_frame, text="筛选", command=self.filter_items, font=("Microsoft YaHei", 12)).pack(side='left', padx=5)

        # 创建一个框架来容纳Treeview和滚动条
        tree_frame = tk.Frame(self.master)
        tree_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # 创建Treeview
        self.item_list = ttk.Treeview(tree_frame, columns=('ID', '分类', '内容'), show='headings', style="Treeview")
        self.item_list.heading('ID', text='ID')
        self.item_list.heading('分类', text='分类')
        self.item_list.heading('内容', text='内容')
        self.item_list.column('ID', width=50)
        self.item_list.column('分类', width=100)
        self.item_list.column('内容', width=400)
        self.item_list.pack(side='left', fill='both', expand=True)

        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.item_list.yview)
        scrollbar.pack(side='right', fill='y')
        self.item_list.configure(yscrollcommand=scrollbar.set)

        # 删除按钮
        self.delete_button = tk.Button(self.master, text="删除选中项", command=self.delete_selected, font=("Microsoft YaHei", 12))
        self.delete_button.pack(pady=10)

        # 设置Treeview的样式
        style = ttk.Style()
        style.configure("Treeview", font=("Microsoft YaHei", 11))
        style.configure("Treeview.Heading", font=("Microsoft YaHei", 12, "bold"))
        
    def load_categories(self):
        categories = self.db.get_categories()
        self.category_combobox['values'] = ["全部"] + [cat[1] for cat in categories]
        self.category_combobox.set("全部")

    def load_items(self, category=None):
        self.item_list.delete(*self.item_list.get_children())
        items = self.db.get_knowledge_items()
        categories = {cat[0]: cat[1] for cat in self.db.get_categories()}
        for item in items:
            item_category = categories.get(item[1], "未分类")
            if category is None or category == "全部" or category == item_category:
                self.item_list.insert('', 'end', values=(item[0], item_category, item[3]))

    def filter_items(self):
        selected_category = self.category_var.get()
        self.load_items(selected_category)

    def delete_selected(self):
        selected_item = self.item_list.selection()
        if selected_item:
            item_id = self.item_list.item(selected_item)['values'][0]
            if messagebox.askyesno("确认删除", "确定要删除此项吗？"):
                self.db.delete_knowledge_item(item_id)
                self.item_list.delete(selected_item)
        else:
            messagebox.showwarning("未选择", "请选择要删除的项。")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeleteKnowledge(root, lambda: root.destroy(), Database())
    root.mainloop()