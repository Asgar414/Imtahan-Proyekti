import tkinter as tk
from gui import GroceryApp

root = tk.Tk()
root.tk.call('tk', 'scaling', 1.5)

app = GroceryApp(root)
root.mainloop()