from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = Tk()

wrapper1 = LabelFrame(root, text="A")
wrapper2 = LabelFrame(root, text="B")
wrapper3 = LabelFrame(root, text="C")

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

trv = ttk.Treeview(wrapper1, columns=(1,2,3,4), show="headings", height="6")
trv.pack()

root.geometry("800x600")
root.mainloop()