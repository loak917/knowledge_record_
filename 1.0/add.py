import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from database import Database

class AddKnowledge:
    def __init__(self, master, return_callback, db):
        self.master = master
        self.return_callback = return_callback
        self.db = db
        self.master.geometry("800x600")  # Increase window size

        self.category_var = tk.StringVar()
        self.index_var = tk.StringVar()
        self.content_var = tk.StringVar()
        self.image_paths = []
        self.image_labels = []

        self.create_widgets()
        self.load_categories()

    def create_widgets(self):
        # Create a return button fixed at top-left
        self.return_button = tk.Button(self.master, text="返回", command=self.return_callback, font=("Microsoft YaHei", 12))
        self.return_button.place(x=10, y=10)

        # Create a main frame for centered content
        main_frame = tk.Frame(self.master, width=650, height=550)
        main_frame.pack(expand=True)
        main_frame.pack_propagate(False)  # Prevent the frame from shrinking

        # Create a canvas
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the canvas
        self.inner_frame = tk.Frame(self.canvas, width=550)
        self.inner_frame.pack(expand=True)

        # Add that new frame to a window in the canvas
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        tk.Label(self.inner_frame, text="分类:", font=("Microsoft YaHei", 14)).pack(pady=10)
        self.category_combobox = ttk.Combobox(self.inner_frame, textvariable=self.category_var, state="readonly", font=("Microsoft YaHei", 12), width=40)
        self.category_combobox.pack(pady=5)

        tk.Label(self.inner_frame, text="主题索引:", font=("Microsoft YaHei", 14)).pack(pady=10)
        self.index_entry = tk.Entry(self.inner_frame, textvariable=self.index_var, font=("Microsoft YaHei", 12), width=40)
        self.index_entry.pack(pady=5)

        tk.Label(self.inner_frame, text="内容:", font=("Microsoft YaHei", 14)).pack(pady=10)
        self.content_text = tk.Text(self.inner_frame, height=15, width=60, font=("Microsoft YaHei", 12))
        self.content_text.pack(pady=10)

        self.image_canvas = tk.Canvas(self.inner_frame, height=150)
        self.image_canvas.pack(fill=tk.X, expand=True, pady=10)
        
        self.image_frame = tk.Frame(self.image_canvas)
        self.image_canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

        self.image_scrollbar = ttk.Scrollbar(self.inner_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        self.image_scrollbar.pack(fill=tk.X)
        self.image_canvas.configure(xscrollcommand=self.image_scrollbar.set)

        self.add_image_button = tk.Button(self.inner_frame, text="添加图片", command=self.add_image, font=("Microsoft YaHei", 12))
        self.add_image_button.pack(pady=10)

        self.save_button = tk.Button(self.inner_frame, text="保存", command=self.save_knowledge, font=("Microsoft YaHei", 12))
        self.save_button.pack(pady=10)

        # Bind mousewheel to scrollbar
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_categories(self):
        categories = self.db.get_categories()
        self.category_combobox['values'] = [cat[1] for cat in categories]

    def add_image(self):
        image_paths = filedialog.askopenfilenames(filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif")])
        for image_path in image_paths:
            self.image_paths.append(image_path)
            self.display_image(image_path)
        self.update_image_scroll()

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        
        image_frame = tk.Frame(self.image_frame)
        image_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        image_label = tk.Label(image_frame, image=photo)
        image_label.image = photo
        image_label.pack()
        
        delete_button = tk.Button(image_frame, text="删除", command=lambda: self.delete_image(image_frame, image_path))
        delete_button.pack()
        
        self.image_labels.append((image_frame, image_path))

    def delete_image(self, image_frame, image_path):
        image_frame.destroy()
        self.image_paths.remove(image_path)
        self.image_labels = [(frame, path) for frame, path in self.image_labels if path != image_path]
        self.update_image_scroll()

    def update_image_scroll(self):
        self.image_frame.update_idletasks()
        self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))

    def save_knowledge(self):
        category = self.category_var.get()
        index = self.index_var.get()
        content = self.content_text.get("1.0", tk.END).strip()

        if not index:
            self.index_entry.config(bg='red')
            messagebox.showerror("错误", "请输入主题索引")
            return
        else:
            self.index_entry.config(bg='white')

        if category and index:
            categories = self.db.get_categories()
            category_id = next(cat[0] for cat in categories if cat[1] == category)

            self.db.add_knowledge_item(category_id, index, content, self.image_paths)
            
            self.category_var.set("")
            self.index_var.set("")
            self.content_text.delete("1.0", tk.END)
            for frame, _ in self.image_labels:
                frame.destroy()
            self.image_labels.clear()
            self.image_paths.clear()
            self.update_image_scroll()
            messagebox.showinfo("成功", "知识项已成功保存")
        else:
            messagebox.showerror("错误", "请至少填写分类和主题索引")

if __name__ == "__main__":
    root = tk.Tk()
    app = AddKnowledge(root, lambda: root.destroy(), Database("test.db"))
    root.mainloop()