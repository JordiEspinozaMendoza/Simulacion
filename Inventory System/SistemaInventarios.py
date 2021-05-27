import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk
from scripts import *
from scripts.generator import *
from scripts.frequency import TestFrequency
import pandas as pd
from pandastable import Table, TableModel
import tkinter.scrolledtext as scrolledtext
from ttkthemes import ThemedTk

root = ThemedTk(theme='breeze')  # tema
root.title("Sistema de inventarios")  # titulo
# tamaño de anchura de toda la ventana del ordenador
screen_width = root.winfo_screenwidth()
# tamaño de la altura toda la ventana del ordenador
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")


menubar = Menu(root)  # se crea el menu
root.config(menu=menubar)  # ??
helpmenu = Menu(menubar, tearoff=0)

menubar.add_command(label="Generador y pruebas")
menubar.add_command(label="Sistema de inventarios")
menubar.add_cascade(label="Mas", menu=helpmenu)
# Menu de ayuda y demas informacion
helpmenu.add_command(label='Ayuda')
helpmenu.add_command(label='Acerca del metodo')
helpmenu.add_command(label='Formulas')
helpmenu.add_command(label='Informacion de las pruebas')
helpmenu.add_command(label='Integrantes')

# Metodo para generador

df = None


def CallGenerator():
    try:
        data_generator = {"n": [], "Xn": [], "Xn+1": [], "Rn": []}
        # Recursivo(
        #     float(X.get()), float(a.get()), float(c.get()), float(m.get()), 0, False, [], data_generator)
        Recursivo(17, 101, 221, 17001, 0, False, [], data_generator)
        df = pd.DataFrame(data_generator, columns=['n', 'Xn', 'Xn+1', 'Rn'])
        trv2["column"] = list(df.columns)

        for column in trv2["column"]:
            trv2.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            trv2.insert("", "end", values=row)
        print(df)

    except Exception as err:
        messagebox.showerror(
            'Error', str(err))


def CallFrequency():
        print(df)
        # testFrequency = TestFrequency(
        #     10,0.5, df)
        # # testFrequency = TestFrequency(
        # #     int(nGroups.get()), float(alpha.get()), df)
        # dfFrequency, foundedChiFreq, chiFreq, dfFreq = testFrequency.solve()
        # print(dfFrequency)
    # try:
    # except Exception as err:
    #     messagebox.showinfo("Error", "Ingresa valores correctos para la simulacion")

    # if chi_calc > chi_table:
    #     chi_table_result.configure(
    #         text=f"Los numeros analizados no estan distribuidos uniformemente de acuerdo a la prueba de la frecuencia \nCHI calculada: {str(chi_calc)}\nCHI de tabla: {str(chi_table)}")  # Mensaje
    # else:
    #     chi_table_result.configure(
    #         text=f"Los numeros analizados si estan distribuidos uniformemente de acuerdo a \nla prueba de la frecuencia \nCHI calculada: {str(chi_table)}\nCHI de tabla:{str(chi_calc)}")
    
    # for column in trvFreq["column"]:
    #     trvFreq.heading(column, text=column)
    # df_rows = dfFrequency.to_numpy().tolist()
    # for row in df_rows:
    #     trvFreq.insert("", "end", values=row)


# Titulo para el generador
Label(root, text="Generador y pruebas",  font=(
    "Arial", 14)).pack(padx=20, pady=5, fill="both")

# Wrappers o contenedores dentro de la ventana(root)
wrapper1 = LabelFrame(root, text="Datos de entrada para el generador")
wrapper2 = LabelFrame(root, text="Prueba de la frecuencia")
wrapper3 = LabelFrame(root, text="Prueba de Smirnov")


wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)


# Contendores para el wrapper1
wrapper11 = Frame(wrapper1)
#wrapper11.grid(row=1, column=0, padx=20, pady=10, sticky="w")
wrapper11.pack(side=LEFT, fill="y")
#wrapper12.grid(row=1,column=1, padx=20, pady=10, sticky="w")
wrapper12 = Frame(wrapper1)
wrapper12.pack(side=RIGHT, fill="y")

# Contendores para el wrapper2
wrapper21 = Frame(wrapper2)
#wrapper11.grid(row=1, column=0, padx=20, pady=10, sticky="w")
wrapper21.pack(side=LEFT, fill="y")
#wrapper12.grid(row=1,column=1, padx=20, pady=10, sticky="w")
wrapper22 = Frame(wrapper2)
wrapper22.pack(side=RIGHT, fill="y")

# Inicio y acomodo de etiquitas y textbox para la entrada de datos
# X=4
# a=5
# c=11
# m=100
LabelX = Label(wrapper11, text="X: ").grid(
    row=1, column=0, padx=2, pady=2, sticky='w')

X = Entry(wrapper11)
X.grid(row=1, column=1, padx=3, pady=2)

Labela = Label(wrapper11, text="a: ").grid(
    row=3, column=0, padx=2, pady=2, sticky='w')

a = Entry(wrapper11)
a.grid(row=3, column=1, padx=3, pady=2)

Labelc = Label(wrapper11, text="c: ").grid(
    row=5, column=0, padx=2, pady=2, sticky='w')

c = Entry(wrapper11)
c.grid(row=5, column=1, padx=3, pady=2)

Labelm = Label(wrapper11, text="m: ").grid(
    row=6, column=0, padx=2, pady=2, sticky='w')

m = Entry(wrapper11)
m.grid(row=6, column=1, padx=3, pady=2)

# Fin de etiquitas y textbox para la entrada de datos

# Boton para calcular dependiendo de la insercion de datos
BtnCalcular = Button(wrapper11, text="Calcular", command=CallGenerator)
BtnCalcular.grid(row=7, column=0, padx=3, pady=2)

trv2 = ttk.Treeview(wrapper12, columns=(
    "n", "Xn", "Xn+1", "Rn"), show='headings', height='8')
trv2.grid(row=1, column=3, sticky="ne")
trv2.heading('n', text='n', anchor="w")
trv2.heading('Xn', text='Xn', anchor="w")
trv2.heading('Xn+1', text='Xn+1', anchor="w")
trv2.heading('Rn', text='Rn', anchor="w")

# Prueba de la frecuencia Maquetado

lbl2 = Label(wrapper21, text="Cantidad de grupos").grid(
    row=1, column=0, padx=5, pady=3, sticky='w')
nGroups = Entry(wrapper21)
nGroups.grid(row=1, column=1, pady=3, padx=3)

lbl3 = Label(wrapper21, text="Alpha").grid(
    row=2, column=0, padx=5, pady=3, sticky="w")
alpha = Entry(wrapper21)
alpha.grid(row=2, column=1, pady=3, padx=3)

btn = Button(wrapper21, text="Calcular", command=CallFrequency)
btn.grid(column=0, row=3, pady=5, padx=6, sticky="w")

# Resultados Freq

trvFreq = ttk.Treeview(wrapper22, columns=("Intervalo", "FE",
                   "FO", "Grupo"), show="headings", height="2")
trvFreq.pack(pady=10, fill='x')
trvFreq.heading('Intervalo', text='Intervalo', anchor="w")
trvFreq.heading('FE', text='FE', anchor="w")
trvFreq.heading('FO', text='FO', anchor="w")
trvFreq.heading('Grupo', text='Grupo', anchor="w")


# Prueba de Smirnov
Label(wrapper3, text="Cantidad de grupos").grid(
    row=1, column=0, padx=5, pady=3, sticky='w')
TxtAlpha = Entry(wrapper3)
TxtAlpha.grid(row=1, column=1, pady=3, padx=3)
Label(wrapper3, text="Alpha").grid(
    row=2, column=0, padx=5, pady=3, sticky="w")
alpha2 = Entry(wrapper3)
alpha2.grid(row=2, column=1, pady=3, padx=3)
Label(wrapper3, text="Cantidad de numeros").grid(
    row=3, column=0, sticky='w')
txtN = Entry(wrapper3)
txtN.grid(row=3, column=1, sticky='w')

btnSmirnov = Button(wrapper3, text="Calcular")
btnSmirnov.grid(column=0, row=4, pady=5, padx=6, sticky="w")


root.mainloop()
