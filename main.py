import tkinter as tk
from gui import GroceryApp


root = tk.Tk()
    
try:
    root.tk.call('tk', 'scaling', 1.5)
except:
    pass
        
app = GroceryApp(root)
root.mainloop()