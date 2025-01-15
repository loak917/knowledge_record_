import tkinter as tk
from tkinter import filedialog
import json
from database import Database

class ImportExport:
    def __init__(self, master, return_callback, db):
        self.master = master
        self.return_callback = return_callback
        self.db = db
        self.master.title("导入/导出知识")

        self.create_widgets()

    def create_widgets(self):
        self.return_button = tk.Button(self.master, text="返回", command=self.return_callback)
        self.return_button.pack(anchor='nw')
        self.export_button = tk.Button(self.master, text="导出知识", command=self.export_knowledge)
        self.export_button.pack(pady=10)
        self.import_button = tk.Button(self.master, text="导入知识", command=self.import_knowledge)
        self.import_button.pack(pady=10)

    def export_knowledge(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON文件", "*.json")])
        if filename:
            categories = self.db.get_categories()
            items = self.db.get_knowledge_items()
            data = {
                "categories": categories,
                "items": items
            }
            with open(filename, 'w') as f:
                json.dump(data, f)

    def import_knowledge(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON文件", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for category in data["categories"]:
                self.db.add_category(category[1])
            for item in data["items"]:
                self.db.add_knowledge_item(item[1], item[2], item[3], item[4])

if __name__ == "__main__":
    root = tk.Tk()
    app = ImportExport(root, lambda: root.destroy(), Database())
    root.mainloop()