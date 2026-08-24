import tkinter as tk
from gui import GroceryApp

if __name__ == "__main__":
    root = tk.Tk()
    
    # Proqramın Windows/Mac-da kənarları kəskin olmasın deyə dizayn hiyləsi
    try:
        root.tk.call('tk', 'scaling', 1.5)
    except:
        pass
        
    app = GroceryApp(root)
    root.mainloop()