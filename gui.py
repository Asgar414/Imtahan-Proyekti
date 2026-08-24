import tkinter as tk
from tkinter import ttk, messagebox
from models import Product, GroceryManager

# --- XÜSUSİ RƏNG PALİTRASI (DARK THEME) ---
BG_COLOR = "#1E1E1E"       # Əsas arxa fon (Tünd qara)
PANEL_COLOR = "#252526"    # Panellərin rəngi (VS Code tərzi)
TEXT_COLOR = "#D4D4D4"     # Əsas yazı rəngi (Açıq boz)
ENTRY_BG = "#3C3C3C"       # Giriş xanalarının rəngi
ACCENT_BLUE = "#007ACC"    # Seçilmiş sətir rəngi

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PRO Grocery Manager - Dark Edition")
        self.root.geometry("850x650")
        self.root.configure(bg=BG_COLOR)
        
        self.manager = GroceryManager()

        self.create_styles()
        self.create_top_panel()
        self.create_middle_panel()
        self.create_bottom_panel()

        # Başlanğıcda datanı avtomatik yükləmək (Opsional)
        self.manager.load_from_file()
        self.refresh_table()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Cədvəl Dizaynı
        style.configure("Treeview", 
                        background=PANEL_COLOR, 
                        foreground=TEXT_COLOR, 
                        fieldbackground=PANEL_COLOR,
                        borderwidth=0, 
                        font=('Segoe UI', 10), 
                        rowheight=35)
        
        # Sütun Başlıqları
        style.configure("Treeview.Heading", 
                        background="#333333", 
                        foreground="white", 
                        borderwidth=0, 
                        font=('Segoe UI', 11, 'bold'))
        
        # Seçilən sətrin rəngi
        style.map('Treeview', background=[('selected', ACCENT_BLUE)])

    def create_top_panel(self):
        top_frame = tk.Frame(self.root, bg=PANEL_COLOR, pady=25, padx=20)
        top_frame.pack(fill="x", padx=20, pady=20)

        font_lbl = ('Segoe UI', 12, 'bold')
        font_entry = ('Segoe UI', 12)

        tk.Label(top_frame, text="Product Name:", bg=PANEL_COLOR, fg=TEXT_COLOR, font=font_lbl).grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(top_frame, font=font_entry, width=18, bg=ENTRY_BG, fg="white", insertbackground="white", relief="flat")
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_frame, text="Quantity:", bg=PANEL_COLOR, fg=TEXT_COLOR, font=font_lbl).grid(row=0, column=2, padx=10, pady=5)
        self.entry_qty = tk.Entry(top_frame, font=font_entry, width=12, bg=ENTRY_BG, fg="white", insertbackground="white", relief="flat")
        self.entry_qty.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(top_frame, text="Price ($):", bg=PANEL_COLOR, fg=TEXT_COLOR, font=font_lbl).grid(row=0, column=4, padx=10, pady=5)
        self.entry_price = tk.Entry(top_frame, font=font_entry, width=12, bg=ENTRY_BG, fg="white", insertbackground="white", relief="flat")
        self.entry_price.grid(row=0, column=5, padx=10, pady=5)

    def create_middle_panel(self):
        mid_frame = tk.Frame(self.root, bg=BG_COLOR)
        mid_frame.pack(fill="x", padx=20, pady=5)

        def make_btn(text, color, command):
            return tk.Button(mid_frame, text=text, bg=color, fg="white", font=('Segoe UI', 10, 'bold'),
                             relief="flat", width=12, pady=8, activebackground=color, activeforeground="white",
                             command=command, cursor="hand2")

        # Neon Rənglər
        buttons = [
            make_btn("Add Item", "#2EA043", self.action_add),     # GitHub Green
            make_btn("Delete", "#DA3633", self.action_delete),    # Coral Red
            make_btn("Update", "#D29922", self.action_update),    # Gold/Orange
            make_btn("Refresh", "#007ACC", self.refresh_table),   # VS Blue
            make_btn("Search", "#8957E5", self.action_search),    # Purple
            make_btn("Save File", "#238636", self.action_save),   # Deep Green
        ]

        for i, btn in enumerate(buttons):
            btn.grid(row=0, column=i, padx=7)

    def create_bottom_panel(self):
        bottom_frame = tk.Frame(self.root, padx=20, pady=10, bg=BG_COLOR)
        bottom_frame.pack(fill="both", expand=True)

        columns = ("Name", "Quantity", "Price")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        self.tree.pack(fill="both", expand=True)

    # --- ƏMƏLİYYATLAR ---

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
            res = self.manager.add_item(Product(name, qty, price))
            if res == "updated":
                messagebox.showinfo("Info", f"'{name}' artıq var idi. Sayı artırıldı!")
            self.refresh_table()
            self.clear_entries()

    def action_delete(self):
        name = self.entry_name.get().strip()
        if name and self.manager.delete_item(name):
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Məhsul tapılmadı!")

    def action_update(self):
        name, qty, price = self.get_inputs()
        if name and self.manager.update_item(name, qty, price):
            self.refresh_table()
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