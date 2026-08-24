import tkinter as tk
from tkinter import ttk, messagebox
from models import Product, GroceryManager

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Grocery Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#F4F6F9") # Açıq boz/mavi fon (Modern görünüş)
        
        self.manager = GroceryManager()

        self.create_styles()
        self.create_top_panel()
        self.create_middle_panel()
        self.create_bottom_panel()

    def create_styles(self):
        # Cədvəl üçün qəşəng dizayn tənzimləmələri
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'), background="#2C3E50", foreground="white")
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=30)

    def create_top_panel(self):
        top_frame = tk.Frame(self.root, bg="#FFFFFF", pady=20, padx=20)
        top_frame.pack(fill="x", padx=20, pady=20)

        # Şriftlər
        font_lbl = ('Segoe UI', 12, 'bold')
        font_entry = ('Segoe UI', 12)

        # Name
        tk.Label(top_frame, text="Product Name:", bg="#FFFFFF", font=font_lbl).grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(top_frame, font=font_entry, width=20, bg="#F0F0F0", relief="flat")
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        # Quantity
        tk.Label(top_frame, text="Quantity:", bg="#FFFFFF", font=font_lbl).grid(row=0, column=2, padx=10, pady=5)
        self.entry_qty = tk.Entry(top_frame, font=font_entry, width=15, bg="#F0F0F0", relief="flat")
        self.entry_qty.grid(row=0, column=3, padx=10, pady=5)

        # Price
        tk.Label(top_frame, text="Price ($):", bg="#FFFFFF", font=font_lbl).grid(row=0, column=4, padx=10, pady=5)
        self.entry_price = tk.Entry(top_frame, font=font_entry, width=15, bg="#F0F0F0", relief="flat")
        self.entry_price.grid(row=0, column=5, padx=10, pady=5)

    def create_middle_panel(self):
        mid_frame = tk.Frame(self.root, bg="#F4F6F9")
        mid_frame.pack(fill="x", padx=20, pady=5)

        # Düymə hazırlamaq üçün kiçik funksiya (Kod təkrarı olmasın deyə)
        def make_btn(text, color, fg_color, command):
            return tk.Button(mid_frame, text=text, bg=color, fg=fg_color, font=('Segoe UI', 10, 'bold'),
                             relief="flat", width=12, pady=5, command=command, cursor="hand2")

        # Tapşırıqda istənilən rənglər əsasında müasir tonlar
        btn_add = make_btn("Add Item", "#2ECC71", "white", self.action_add)
        btn_del = make_btn("Delete Item", "#E74C3C", "white", self.action_delete)
        btn_upd = make_btn("Update Item", "#3498DB", "white", self.action_update)
        btn_show = make_btn("Show Items", "#E67E22", "white", self.refresh_table)
        btn_search = make_btn("Search", "#F1C40F", "black", self.action_search)
        btn_save = make_btn("Save", "#1ABC9C", "white", self.action_save)
        btn_load = make_btn("Load", "#2C3E50", "white", self.action_load)

        # Düymələri yan-yana düzmək
        buttons = [btn_add, btn_del, btn_upd, btn_show, btn_search, btn_save, btn_load]
        for i, btn in enumerate(buttons):
            btn.grid(row=0, column=i, padx=5)

    def create_bottom_panel(self):
        bottom_frame = tk.Frame(self.root, padx=20, pady=10, bg="#F4F6F9")
        bottom_frame.pack(fill="both", expand=True)

        columns = ("Name", "Quantity", "Price")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        self.tree.pack(fill="both", expand=True)

    # --- ACTION (ƏMƏLİYYAT) METODLARI ---

    def get_inputs(self):
        # Xanaları oxuyur və validasiya edir (səhv varsa Alert verir)
        name = self.entry_name.get().strip()
        qty = self.entry_qty.get().strip()
        price = self.entry_price.get().strip()

        if not name or not qty or not price:
            messagebox.showwarning("Xəta", "Bütün sahələr doldurulmalıdır!")
            return None, None, None
        
        try:
            qty = int(qty)
            price = float(price)
            return name, qty, price
        except ValueError:
            messagebox.showerror("Xəta", "Quantity və Price yalnız rəqəm olmalıdır!")
            return None, None, None

    def action_add(self):
        name, qty, price = self.get_inputs()
        if name:
            product = Product(name, qty, price)
            result = self.manager.add_item(product)
            if result == "Updated":
                messagebox.showinfo("Uğurlu", f"{name} artıq var idi, sayı artırıldı!")
            
            self.refresh_table()
            self.clear_entries()

    def action_delete(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Xəta", "Silmək üçün Məhsul Adını yazın!")
            return
        
        if self.manager.delete_item(name):
            self.refresh_table()
            messagebox.showinfo("Uğurlu", "Məhsul silindi!")
        else:
            messagebox.showerror("Xəta", "Məhsul tapılmadı!")

    def action_update(self):
        name, qty, price = self.get_inputs()
        if name:
            if self.manager.update_item(name, qty, price):
                self.refresh_table()
                messagebox.showinfo("Uğurlu", "Məhsul yeniləndi!")
            else:
                messagebox.showerror("Xəta", "Məhsul tapılmadı!")

    def action_search(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Xəta", "Axtarmaq üçün Məhsul Adını yazın!")
            return
            
        item = self.manager.search_item(name)
        
        # Cədvəli təmizlə və ancaq tapılanı göstər
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if item:
            self.tree.insert("", "end", values=(item.name, item.quantity, f"${item.price}"))
        else:
            messagebox.showinfo("Nəticə", "Belə məhsul yoxdur.")

    def refresh_table(self):
        # Cədvəldəki köhnə sətirləri silirik
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Bütün məhsulları yenidən cədvələ əlavə edirik
        for item in self.manager.get_all_items():
            self.tree.insert("", "end", values=(item.name, item.quantity, f"${item.price}"))

    def action_save(self):
        self.manager.save_to_file()
        messagebox.showinfo("Uğurlu", "Məlumatlar fayla yadda saxlanıldı! (grocery_data.json)")

    def action_load(self):
        self.manager.load_from_file()
        self.refresh_table()
        messagebox.showinfo("Uğurlu", "Məlumatlar fayldan yükləndi!")

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)