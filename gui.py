import tkinter as tk
from tkinter import ttk, messagebox
from models import Product, GroceryManager

BG = "#1E1E1E"
PANEL = "#252526"
TEXT = "#D4D4D4"
ENTRY_BG = "#3C3C3C"

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Manager")
        self.root.geometry("850x650")
        self.root.configure(bg=BG)
        
        self.manager = GroceryManager()

        self.setup_styles()
        self.create_widgets()
        
        self.manager.load_from_file()
        self.refresh_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=PANEL, foreground=TEXT, fieldbackground=PANEL, borderwidth=0, font=('Segoe UI', 10), rowheight=35)
        style.configure("Treeview.Heading", background="#333333", foreground="white", borderwidth=0, font=('Segoe UI', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#007ACC')])

    def create_widgets(self):
        top_frame = tk.Frame(self.root, bg=PANEL, pady=20, padx=20)
        top_frame.pack(fill="x", padx=20, pady=15)

        fields = [("Product Name:", 18), ("Quantity:", 12), ("Price ($):", 12)]
        self.entries = {}

        for i, (label_text, width) in enumerate(fields):
            tk.Label(top_frame, text=label_text, bg=PANEL, fg=TEXT, font=('Segoe UI', 11, 'bold')).grid(row=0, column=i*2, padx=5, pady=5)
            entry = tk.Entry(top_frame, font=('Segoe UI', 11), width=width, bg=ENTRY_BG, fg="white", insertbackground="white", relief="flat")
            entry.grid(row=0, column=i*2+1, padx=8, pady=5)
            self.entries[label_text] = entry

        self.entry_name, self.entry_qty, self.entry_price = self.entries.values()

        mid_frame = tk.Frame(self.root, bg=BG)
        mid_frame.pack(fill="x", padx=20, pady=5)

        buttons = [
            ("Add Item", "#2EA043", self.action_add),
            ("Delete", "#DA3633", self.action_delete),
            ("Update", "#D29922", self.action_update),
            ("Refresh", "#007ACC", self.refresh_table),
            ("Search", "#8957E5", self.action_search),
            ("Save File", "#238636", self.action_save),
        ]

        for i, (text, color, cmd) in enumerate(buttons):
            btn = tk.Button(mid_frame, text=text, bg=color, fg="white", font=('Segoe UI', 10, 'bold'),
                            relief="flat", width=11, pady=6, activebackground=color, activeforeground="white",
                            command=cmd, cursor="hand2")
            btn.grid(row=0, column=i, padx=5)

        bottom_frame = tk.Frame(self.root, padx=20, pady=10, bg=BG)
        bottom_frame.pack(fill="both", expand=True)

        columns = ("Name", "Quantity", "Price")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def get_inputs(self):
        name = self.entry_name.get().strip()
        qty = self.entry_qty.get().strip()
        price = self.entry_price.get().strip()

        if not name or not qty or not price:
            messagebox.showwarning("Warning", "Sahələri boş buraxmayın!")
            return None, None, None
        try:
            return name, int(qty), float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity və Price rəqəm olmalıdır!")
            return None, None, None

    def action_add(self):
        name, qty, price = self.get_inputs()
        if name:
            if self.manager.add_item(Product(name, qty, price)) == "updated":
                messagebox.showinfo("Info", f"'{name}' artıq var idi. Sayı artırıldı!")
            self.refresh_table()
            self.clear_entries()

    def action_delete(self):
        name = self.entry_name.get().strip()
        if name and self.manager.delete_item(name):
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Məhsul tapılmadı!")

    def action_update(self):
        name, qty, price = self.get_inputs()
        if name and self.manager.update_item(name, qty, price):
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Yeniləmək üçün məhsul tapılmadı!")

    def action_search(self):
        name = self.entry_name.get().strip()
        item = self.manager.search_item(name)
        self.tree.delete(*self.tree.get_children())
        if item:
            self.tree.insert("", "end", values=(item.name, item.quantity, f"${item.price:.2f}"))
        else:
            messagebox.showinfo("Result", "Belə məhsul tapılmadı.")

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.manager.get_all_items():
            self.tree.insert("", "end", values=(item.name, item.quantity, f"${item.price:.2f}"))

    def action_save(self):
        self.manager.save_to_file()
        messagebox.showinfo("Success", "Bütün məlumatlar JSON faylına yazıldı!")

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)