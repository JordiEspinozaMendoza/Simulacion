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

menubar = Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='Ayuda')
helpmenu.add_command(label='Acerca del metodo')
helpmenu.add_command(label='Integrantes')

menubar.add_command(label="Inicio")
menubar.add_cascade(label="Ayuda", menu=helpmenu)

# Properties
root.title("Prueba de frecuencia")

app_width = 800
app_height = 700

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

        res, chi_table, chi_calc, df = test.solve()
        trv["column"] = list(res.columns)
    except Exception as e:
        messagebox.showinfo("Error", "Ingresa valores correctos para la simulacion")
    for column in trv["column"]:
        trv.heading(column, text=column)
    df_rows = res.to_numpy().tolist()
    for row in df_rows:
        trv.insert("", "end", values=row)
    if chi_calc > chi_table:
        chi_table_result.configure(
            text=f"Los numeros analizados no estan distribuidos uniformemente de acuerdo a la prueba de la frecuencia \nCHI calculada: {str(chi_calc)}\nCHI de tabla: {str(chi_table)}")  # Mensaje
    else:
        chi_table_result.configure(
            text=f"Los numeros analizados si estan distribuidos uniformemente de acuerdo a \nla prueba de la frecuencia \nCHI calculada: {str(chi_table)}\nCHI de tabla:{str(chi_calc)}")
    
    for column in trv2["column"]:
        trv2.heading(column, text=column)
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        trv2.insert("", "end", values=row)


def delete():
    for i in trv.get_children():
        trv.delete(i)


# Titulo
Label(root, text="Prueba de frecuencia",  font=(
    "Arial", 14)).pack(padx=20, pady=5, fill="both")

# Contenedores
wrapper1 = LabelFrame(root, text="Resultados")
wrapper2 = LabelFrame(root, text="Datos de entrada para la simulacion")
wrapper3 = LabelFrame(root, text="Numeros generados")
wrapper4 = LabelFrame(root, text="Numeros pseudoaleatorios generados")

wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

# Fin de contenedores

# Resultados

trv = ttk.Treeview(wrapper1, columns=("Intervalo", "FE",
                   "FO", "Grupo"), show="headings", height="2")
trv.pack(pady=10, fill='x')
trv.heading('Intervalo', text='Intervalo', anchor="w")
trv.heading('FE', text='FE', anchor="w")
trv.heading('FO', text='FO', anchor="w")
trv.heading('Grupo', text='Grupo', anchor="w")

# Numeros pseudo
trv2 = ttk.Treeview(wrapper3, columns=(
    "n", "Xn", "Xn+1", "Rn"), show='headings', height='2')
trv2.pack(pady=10, fill='x')
trv2.heading('n', text='n', anchor="w")
trv2.heading('Xn', text='Xn', anchor="w")
trv2.heading('Xn+1', text='Xn+1', anchor="w")
trv2.heading('Rn', text='Residuo', anchor="w")

# Mensaje final
chi_table_result = Label(wrapper1, text="")
chi_table_result.pack()

# Fin resultado
# Info para el simulador
lbl2 = Label(wrapper2, text="Cantidad de grupos").grid(
    row=1, column=0, padx=5, pady=3, sticky='w')
nGroups = Entry(wrapper2)
nGroups.grid(row=1, column=1, pady=3, padx=3)

lbl3 = Label(wrapper2, text="Alpha").grid(
    row=2, column=0, padx=5, pady=3, sticky="W")
alpha = Entry(wrapper2)
alpha.grid(row=2, column=1, pady=3, padx=3)

btn = Button(wrapper2, text="Calcular", command=clickedGenerator)
btn.grid(column=0, row=3, pady=5, padx=6, sticky="W")
# Fin info para el simulador


root.mainloop()
