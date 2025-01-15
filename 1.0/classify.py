import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
import time

class ClassifyKnowledge:
    def __init__(self, master, return_callback, db):
        self.master = master
        self.return_callback = return_callback
        self.db = db
        self.master.title("分类知识")
        self.master.geometry("800x600")  # 增加窗口大小

        self.category_var = tk.StringVar()
        self.create_widgets()
        self.load_categories()
        self.last_deleted_category = None

    def create_widgets(self):
        # 返回按钮
        self.return_button = tk.Button(self.master, text="返回", command=self.return_callback, font=("Microsoft YaHei", 12))
        self.return_button.pack(anchor='nw', padx=10, pady=10)

        # 分类标签
        tk.Label(self.master, text="分类:", font=("Microsoft YaHei", 14)).pack(pady=5)

        # 创建一个框架来容纳Treeview和滚动条
        tree_frame = tk.Frame(self.master)
        tree_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # 创建Treeview
        self.category_list = ttk.Treeview(tree_frame, columns=('ID', '名称'), show='headings', style="Treeview")
        self.category_list.heading('ID', text='ID')
        self.category_list.heading('名称', text='名称')
        self.category_list.column('ID', width=100)
        self.category_list.column('名称', width=300)
        self.category_list.pack(side='left', fill='both', expand=True)

        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.category_list.yview)
        scrollbar.pack(side='right', fill='y')
        self.category_list.configure(yscrollcommand=scrollbar.set)

        # 新分类输入框
        tk.Label(self.master, text="新分类:", font=("Microsoft YaHei", 12)).pack(pady=5)
        self.category_entry = tk.Entry(self.master, textvariable=self.category_var, font=("Microsoft YaHei", 12), width=30)
        self.category_entry.pack(pady=5)

        # 添加分类按钮
        self.add_button = tk.Button(self.master, text="添加分类", command=self.add_category, font=("Microsoft YaHei", 12))
        self.add_button.pack(pady=10)

        # 添加更改类别名称按钮
        self.rename_button = tk.Button(self.master, text="更改类别名称", command=self.rename_category, font=("Microsoft YaHei", 12))
        self.rename_button.pack(pady=5)

        # 添加删除类别按钮
        self.delete_button = tk.Button(self.master, text="删除类别", command=self.delete_category, font=("Microsoft YaHei", 12))
        self.delete_button.pack(pady=5)

        # 添加撤销删除按钮（初始状态为禁用）
        self.undo_button = tk.Button(self.master, text="撤销删除", command=self.undo_delete, font=("Microsoft YaHei", 12), state=tk.DISABLED)
        self.undo_button.pack(pady=5)

        # 设置Treeview的样式
        style = ttk.Style()
        style.configure("Treeview", font=("Microsoft YaHei", 11))
        style.configure("Treeview.Heading", font=("Microsoft YaHei", 12, "bold"))

    def load_categories(self):
        self.category_list.delete(*self.category_list.get_children())
        categories = self.db.get_categories()
        for category in categories:
            self.category_list.insert('', 'end', values=category)

    def add_category(self):
        new_category = self.category_var.get().strip()
        if new_category:
            existing_categories = [self.category_list.item(item)['values'][1] for item in self.category_list.get_children()]
            if new_category in existing_categories:
                messagebox.showwarning("分类已存在", f"分类 '{new_category}' 已经存在，请输入新的分类名称。")
            else:
                self.db.add_category(new_category)
                self.load_categories()
                self.category_var.set("")
                messagebox.showinfo("成功", f"分类 '{new_category}' 已成功添加。")
        else:
            messagebox.showwarning("输入错误", "请输入分类名称。")

    def rename_category(self):
        selected_items = self.category_list.selection()
        if not selected_items:
            messagebox.showwarning("未选择", "请选择要更改名称的类别。")
            return

        old_name = self.category_list.item(selected_items[0])['values'][1]
        new_name = simpledialog.askstring("更改类别名称", f"请输入新的类别名称（原名称：{old_name}）：", parent=self.master)

        if new_name and new_name != old_name:
            if self.db.rename_category(old_name, new_name):
                self.load_categories()
                messagebox.showinfo("成功", f"类别名称已更改为：{new_name}")
            else:
                messagebox.showerror("错误", "更改类别名称失败。")

    def delete_category(self):
        selected_items = self.category_list.selection()
        if not selected_items:
            messagebox.showwarning("未选择", "请选择要删除的类别。")
            return

        values = self.category_list.item(selected_items[0])['values']
        category_id, category_name = values[0], values[1]  # 只取前两个值
        if messagebox.askyesno("确认删除", f"确定要删除类别 '{category_name}' 吗？\n此操作将导致该类别下所有知识项无法查找。"):
            password = simpledialog.askstring("输入密码", "请输入管理员密码：", show='*')
            if password == "admin123":  # 这里使用了一个示例密码，您可以根据需要修改
                self.last_deleted_category = (category_id, category_name)
                self.db.delete_category(category_id)
                self.load_categories()
                self.undo_button.config(state=tk.NORMAL)
                self.master.after(5000, self.disable_undo_button)
                messagebox.showinfo("删除成功", f"类别 '{category_name}' 已删除。")
            else:
                messagebox.showerror("密码错误", "密码不正确，删除操作已取消。")

    def undo_delete(self):
        if self.last_deleted_category:
            category_id, category_name = self.last_deleted_category
            self.db.restore_category(category_id, category_name)
            self.load_categories()
            self.last_deleted_category = None
            self.undo_button.config(state=tk.DISABLED)
            messagebox.showinfo("撤销成功", f"已恢复类别：{category_name}")

    def disable_undo_button(self):
        self.undo_button.config(state=tk.DISABLED)
        if self.last_deleted_category:
            category_id, category_name = self.last_deleted_category
            if messagebox.askyesno("确认删除", f"是否确定永久删除类别 '{category_name}'？\n此操作不可撤销。"):
                self.db.confirm_delete_category(category_id)
                messagebox.showinfo("删除成功", f"类别 '{category_name}' 已永久删除。")
            else:
                self.db.restore_category(category_id, category_name)
                self.load_categories()
            self.last_deleted_category = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ClassifyKnowledge(root, lambda: root.destroy(), Database("test.db"))
    root.mainloop()