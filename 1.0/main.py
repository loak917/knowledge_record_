import tkinter as tk
from tkinter import filedialog, messagebox
from add import AddKnowledge
from show import ShowKnowledge
from classify import ClassifyKnowledge
from delete import DeleteKnowledge
from database import Database

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("知识管理系统")
        self.master.geometry("800x600")
        self.db = None
        self.create_widgets()

    def create_widgets(self):
        self.clear_widgets()
        self.select_db_button = tk.Button(self.master, text="选择数据库", command=self.select_database, font=("Microsoft YaHei", 20))
        self.select_db_button.pack(fill=tk.BOTH, expand=True)
        self.new_db_button = tk.Button(self.master, text="新建数据库", command=self.create_new_database, font=("Microsoft YaHei", 20))
        self.new_db_button.pack(fill=tk.BOTH, expand=True)

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def select_database(self):
        db_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
        if db_path:
            self.db = Database(db_path)
            self.create_main_buttons()

    def create_new_database(self):
        db_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if db_path:
            self.db = Database(db_path)
            self.create_main_buttons()

    def create_main_buttons(self):
        self.clear_widgets()
        self.buttons = [
            tk.Button(self.master, text="添加知识", command=self.open_add, font=("Microsoft YaHei", 20)),
            tk.Button(self.master, text="显示知识", command=self.open_show, font=("Microsoft YaHei", 20)),
            tk.Button(self.master, text="分类知识", command=self.open_classify, font=("Microsoft YaHei", 20)),
            tk.Button(self.master, text="删除知识", command=self.open_delete, font=("Microsoft YaHei", 20))
        ]
        for button in self.buttons:
            button.pack(fill=tk.BOTH, expand=True, pady=5)

    def open_add(self):
        self.clear_widgets()
        AddKnowledge(self.master, self.create_main_buttons, self.db)

    def open_show(self):
        self.clear_widgets()
        ShowKnowledge(self.master, self.create_main_buttons, self.db)

    def open_classify(self):
        self.clear_widgets()
        ClassifyKnowledge(self.master, self.create_main_buttons, self.db)

    def open_delete(self):
        self.clear_widgets()
        DeleteKnowledge(self.master, self.create_main_buttons, self.db)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()