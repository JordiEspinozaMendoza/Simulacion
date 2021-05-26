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
from ttkthemes import ThemedTk


root = ThemedTk(theme="breeze")
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
        trv["column"] = list(res.columns)
    except Exception as e:
        messagebox.showinfo("Error", str(e))
    print(chi_table)
    for column in trv["column"]:
        trv.heading(column, text=column)
    df_rows = res.to_numpy().tolist()
    for row in df_rows:
        trv.insert("", "end", values=row)
    if CHI > chi_table:
        chi_table_result.configure(text=f"{str(CHI)} > {str(chi_table)}")
    else:
        chi_table_result.configure(text=f"{str(chi_table)} > {str(CHI)}")


def delete():
    for i in trv.get_children():
        trv.delete(i)


Label(root, text="Prueba de frecuencia",  font=(
    "Arial", 14)).pack(padx=20, pady=5, fill="both")

wrapper1 = LabelFrame(root, text="Resultados")
wrapper2 = LabelFrame(root, text="Datos de entrada para la simulacion")
wrapper3 = LabelFrame(root, text="C")

wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
# wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

trv = ttk.Treeview(wrapper1, columns=("Intervalo", "FE", "FO", "Grupo"), show="headings", height="6")
trv.pack(pady=10)
trv.heading('Intervalo', text='Intervalo', anchor="w")
trv.heading('FE', text='FE',anchor="w")
trv.heading('FO', text='FO', anchor="w")
trv.heading('Grupo', text='Grupo', anchor="w")


lbl2 = Label(wrapper2, text="Cantidad de grupos").grid(
    row=1, column=0, padx=5, pady=3, sticky='w')
nGroups = Entry(wrapper2).grid(row=1, column=1, pady=3, padx=3)

lbl3 = Label(wrapper2, text="Alpha").grid(row=2, column=0, padx=5, pady=3, sticky="W")
alpha=Entry(wrapper2).grid(row=2, column=1, pady=3, padx=3)

btn = Button(wrapper2, text="Calcular", command=clickedGenerator)
btn.grid(column=0,row=3,pady=5, padx=6, sticky="W")

root.geometry("800x600")
root.mainloop()

# # Frame for treeview
# tree_frame = Frame(root, relief='flat')
# tree_frame.grid(pady=20, padx=10)
# # Treeview scrollbar
# scrollbary = ttk.Scrollbar(tree_frame)
# scrollbary.pack(side=RIGHT, fill=Y)
# scrollbarx = ttk.Scrollbar(tree_frame, orient="horizontal")
# scrollbarx.pack(side=BOTTOM, fill=X)
# # Treeview
# my_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbary.set,
#                        xscrollcommand=scrollbarx.set, selectmode="extended")
# my_tree.pack(expand=False)
# scrollbary.config(command=my_tree.yview)
# scrollbarx.config(command=my_tree.xview)
# chi_table_result.grid(
#     pady=5, sticky="W", padx=6)
# root.mainloop()
