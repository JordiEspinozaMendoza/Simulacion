import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk
from scripts import *
from scripts.frequency import TestFrequency
import pandas as pd
from pandastable import Table, TableModel
import tkinter.scrolledtext as scrolledtext

root = tk.Tk()
# Properties
root.title("Prueba de frecuencia")
root.resizable(False, False)

app_width = 900
app_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)

root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

chi_table_result = Label(root)
# Methods


def clickedGenerator():
    delete()
    test = None
    res = None
    chi_table = None
    CHI = None
    try:
        test = TestFrequency(int(nGroups.get()), float(alpha.get()))
        res, chi_table, CHI = test.solve()
        my_tree["column"] = list(res.columns)
        my_tree["show"] = "headings"
    except Exception as e:
        messagebox.showinfo("Error", str(e))

    for column in my_tree["column"]:
        my_tree.heading(column, text=column)
    df_rows = res.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("", "end", values=row)
    if CHI > chi_table:
        chi_table_result.configure(text=f"{str(CHI)} > {str(chi_table)}")
    else:
        chi_table_result.configure(text=f"{str(chi_table)} > {str(CHI)}")


def delete():
    for i in my_tree.get_children():
        my_tree.delete(i)


# Labels
Label(root, text="Prueba de frecuencia",  font=("Arial", 14)).grid(
    column=0, padx=6, pady=5, row=0, columnspan=2, sticky="W")
# Entriess
Label(root, text="Ingresa la cantidad de grupos").grid(
    pady=5, column=0, row=1, sticky="W", padx=6)
nGroups = Entry(root)
nGroups.grid(column=0, padx=6, sticky="W")
Label(root, text="Ingresa alpha").grid(
    pady=6, column=0, row=4, sticky="W", padx=6)
alpha = Entry(root)
alpha.grid(column=0, padx=6, sticky="W")

# Buttons
btn = Button(root, text="Calcular", command=clickedGenerator)
btn.grid(column=0, pady=5, padx=6, sticky="W")
# Frame for treeview
tree_frame = Frame(root, relief='flat')
tree_frame.grid(pady=20, padx=10)
# Treeview scrollbar
scrollbary = ttk.Scrollbar(tree_frame)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx = ttk.Scrollbar(tree_frame, orient="horizontal")
scrollbarx.pack(side=BOTTOM, fill=X)
# Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbary.set,
                       xscrollcommand=scrollbarx.set, selectmode="extended")
my_tree.pack(expand=False)
scrollbary.config(command=my_tree.yview)
scrollbarx.config(command=my_tree.xview)
chi_table_result.grid(
    pady=5, sticky="W", padx=6)
root.mainloop()
