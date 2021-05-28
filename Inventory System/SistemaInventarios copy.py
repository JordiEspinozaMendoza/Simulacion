import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk

from matplotlib.pyplot import figure
from scripts import *
from scripts.generator import *
from scripts.frequency import TestFrequency
from scripts.smirnov import Test_Smirnov
from simulation import inventory_system
import pandas as pd
from pandastable import Table, TableModel
import tkinter.scrolledtext as scrolledtext
from ttkthemes import ThemedTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

root = ThemedTk(theme='breeze')  # tema
root.title("Sistema de inventarios")  # titulo
# tamaño de anchura de toda la ventana del ordenador
screen_width = root.winfo_screenwidth()
# tamaño de la altura toda la ventana del ordenador
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
# root.iconbitmap('/logo.ico')


def cleanGeneratorTests():
    main.wrapper1.pack_forget()
    main.wrapper2.pack_forget()
    main.wrapper3.pack_forget()
    openSimulation()


def cleanSimulator():
    main.wrapper4.pack_forget()
    main.wrapper5.pack_forget()
    openGeneratorTests()


def openGeneratorTests():
    main.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
    main.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
    main.wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)


def openSimulation():
    main.wrapper4.pack(fill="both", padx=20, pady=10)
    main.wrapper5.pack(fill="both", expand="yes", padx=20, pady=10)


menubar = Menu(root)  # se crea el menu
root.config(menu=menubar)  # ??
helpmenu = Menu(menubar, tearoff=0)

menubar.add_command(label="Generador y pruebas", command=cleanSimulator)
menubar.add_command(label="Sistema de inventarios",
                    command=cleanGeneratorTests)
menubar.add_cascade(label="Mas", menu=helpmenu)
# Menu de ayuda y demas informacion
helpmenu.add_command(label='Ayuda')
helpmenu.add_command(label='Acerca del metodo')
helpmenu.add_command(label='Formulas')
helpmenu.add_command(label='Informacion de las pruebas')
helpmenu.add_command(label='Integrantes')

NavigationToolbar2Tk.toolitems = [
    t for t in NavigationToolbar2Tk.toolitems if t[0] not in ('Subplots', 0)]

# Metodo para generador


class MainPage:
    # Generator
    df = None
    trv2 = None
    # Frequency
    trvFreq = None
    dfFrequency = None
    foundedChiFreq = None
    chiFreq = None
    dfFreq = None
    resultsFreq = None
    # Smirnov
    resultsSmirnov = None
    # Inventory
    dfSimulation = None
    figure1 = None

    def CallGenerator(self):
        try:
            data_generator = {"n": [], "Xn": [], "Xn+1": [], "Rn": []}
            Recursivo(
                float(self.X.get()), float(self.a.get()), float(self.c.get()), float(self.m.get()), 0, False, [], data_generator)
            # Recursivo(17, 101, 221, 17001, 0, False, [], data_generator)
            self.df = pd.DataFrame(data_generator, columns=[
                                   'n', 'Xn', 'Xn+1', 'Rn'])
            self.trv2["column"] = list(self.df.columns)

            for column in self.trv2["column"]:
                self.trv2.heading(column, text=column)

            df_rows = self.df.to_numpy().tolist()
            for row in df_rows:
                self.trv2.insert("", "end", values=row)
            self.statusSimulation.config(
                text=f"Cantidad de numeros: {len(self.df['Rn'])}")

        except Exception as err:
            messagebox.showerror(
                'Error', str(err))

    def CallFrequency(self):
        try:
            # testFrequency = TestFrequency(
            #     10,0.5, self.df)
            testFrequency = TestFrequency(
                int(self.nGroups.get()), float(self.alpha.get()), self.df)
            self.dfFrequency, self.foundedChiFreq, self.chiFreq, self.dfFreq = testFrequency.solve()
        except Exception as err:
            messagebox.showinfo(
                "Error", "Ingresa valores correctos para la simulacion")

        if self.chiFreq > self.foundedChiFreq:
            self.resultsFreq.configure(
                text=f"Los numeros analizados no \nestan distribuidos uniformemente de \nacuerdo a la prueba de la frecuencia \n\nCHI calculada: {str(self.chiFreq)}\n\nCHI de tabla: {str(self.foundedChiFreq)}")  # Mensaje
        else:
            self.resultsFreq.configure(
                text=f"Los numeros analizados si \nestan distribuidos uniformemente de \nacuerdo a \nla prueba de la frecuencia \n\nCHI calculada: {str(self.foundedChiFreq)}\n\nCHI de tabla:{str(self.chiFreq)}")

        for column in self.trvFreq["column"]:
            self.trvFreq.heading(column, text=column)
        df_rows = self.dfFrequency.to_numpy().tolist()
        for row in df_rows:
            self.trvFreq.insert("", "end", values=row)

    def CallSmirnov(self):
        try:
            smirnov = Test_Smirnov(f"{self.txtN.get()}%",
                                   int(self.alpha2.get()), self.df)
            res = smirnov.solve()
            self.resultsSmirnov.config(
                text=f"{res['message']}\nEl numero Di Maximo es: {str(res['max'])}\nEl valor Di de tablas es: {str(res['aprox'])}")
        except Exception as err:
            messagebox.showinfo(
                "Error", "Ingresa valores correctos para la prueba de Smirnov")

    def CallSimulation(self):
        try:
            simulation = inventory_system(int(self.R.get()), int(self.Q.get()), self.df)
            # simulation = inventory_system(100, 200, self.df)
            simulation.Calc_probability_month()
            simulation.Calc_probability_delivery()
            self.dfSimulation = simulation.Simulation()
            self.trvSimulation["column"]
            for column in self.trvSimulation["column"]:
                self.trvSimulation.heading(column, text=column)
            df_rows = self.dfSimulation.to_numpy().tolist()
            for row in df_rows:
                self.trvSimulation.insert("", "end", values=row)
            # Figure
            self.figure1 = plt.Figure(figsize=(4, 1), dpi=100)
            ax2 = self.figure1.add_subplot(111)

            line2 = FigureCanvasTkAgg(self.figure1, self.wrapper5)

            line2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(line2, self.wrapper5)

            toolbar.update()

            dfFigure = self.dfSimulation[[
                'month', 'dem_sim']].groupby('month').sum()
            dfFigure.plot(kind='line', legend=True, ax=ax2,
                          color='r', marker='o', fontsize=10)

        except Exception as err:
            messagebox.showinfo(
                "Error", str(err))

    def __init__(self, root):
        # region Ventana generador y tests
        # Wrappers o contenedores dentro de la ventana(root)
        self.wrapper1 = LabelFrame(
            root, text="Datos de entrada para el generador")
        self.wrapper2 = LabelFrame(root, text="Prueba de la frecuencia")
        self.wrapper3 = LabelFrame(root, text="Prueba de Smirnov")

        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
        # region Wrappers Generador y tests
        # Contendores para el wrapper1
        self.wrapper11 = Frame(self.wrapper1)
        #self.wrapper11.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.wrapper11.pack(side=LEFT, fill="y")
        #self.wrapper12.grid(row=1,column=1, padx=20, pady=10, sticky="w")
        self.wrapper12 = Frame(self.wrapper1)
        self.wrapper12.pack(side=RIGHT, fill="y")

        # Contendores para el self.wrapper2
        self.wrapper21 = Frame(self.wrapper2)
        #self.wrapper11.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.wrapper21.pack(side=LEFT, fill="y")
        #self.wrapper12.grid(row=1,column=1, padx=20, pady=10, sticky="w")
        self.wrapper22 = Frame(self.wrapper2)
        self.wrapper22.pack(side=RIGHT, fill="y")
        # Contendores para el self.wrapper3
        self.wrapper31 = Frame(self.wrapper3)
        #self.wrapper11.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.wrapper31.pack(side=LEFT, fill="y")
        #self.wrapper12.grid(row=1,column=1, padx=20, pady=10, sticky="w")
        self.wrapper32 = Frame(self.wrapper3)
        self.wrapper32.pack(side=LEFT, fill="y")
        # endregion

        # region inputs generador
        # Inputs para generador
        LabelX = Label(self.wrapper11, text="X: ").grid(
            row=1, column=0, padx=2, pady=2, sticky='w')

        self.X = Entry(self.wrapper11)
        self.X.grid(row=1, column=1, padx=3, pady=2)

        Labela = Label(self.wrapper11, text="a: ").grid(
            row=3, column=0, padx=2, pady=2, sticky='w')

        self.a = Entry(self.wrapper11)
        self.a.grid(row=3, column=1, padx=3, pady=2)

        Labelc = Label(self.wrapper11, text="c: ").grid(
            row=5, column=0, padx=2, pady=2, sticky='w')

        self.c = Entry(self.wrapper11)
        self.c.grid(row=5, column=1, padx=3, pady=2)

        Labelm = Label(self.wrapper11, text="m: ").grid(
            row=6, column=0, padx=2, pady=2, sticky='w')

        self.m = Entry(self.wrapper11)
        self.m.grid(row=6, column=1, padx=3, pady=2)

        # Boton para calcular dependiendo de la insercion de datos
        BtnCalcular = Button(self.wrapper11, text="Calcular",
                             command=self.CallGenerator)
        BtnCalcular.grid(row=7, column=0, padx=3, pady=2)

        self.trv2 = ttk.Treeview(self.wrapper12, columns=(
            "n", "Xn", "Xn+1", "Rn"), show='headings', height='8')
        self.trv2.grid(row=1, column=3, sticky="ne")
        self.trv2.heading('n', text='n', anchor="w")
        self.trv2.heading('Xn', text='Xn', anchor="w")
        self.trv2.heading('Xn+1', text='Xn+1', anchor="w")
        self.trv2.heading('Rn', text='Rn', anchor="w")
        # endregion

        # region frequency

        lbl2 = Label(self.wrapper21, text="Cantidad de grupos").grid(
            row=1, column=0, padx=5, pady=3, sticky='w')
        self.nGroups = Entry(self.wrapper21)
        self.nGroups.grid(row=1, column=1, pady=3, padx=3)

        lbl3 = Label(self.wrapper21, text="Alpha").grid(
            row=2, column=0, padx=5, pady=3, sticky="w")
        self.alpha = Entry(self.wrapper21)
        self.alpha.grid(row=2, column=1, pady=3, padx=3)

        btn = Button(self.wrapper21, text="Calcular",
                     command=self.CallFrequency)
        btn.grid(column=0, row=3, pady=5, padx=6, sticky="w")

        # Resultados Freq

        self.trvFreq = ttk.Treeview(self.wrapper22, columns=("Intervalo", "FE",
                                                             "FO", "Grupo"), show="headings", height="6")
        self.trvFreq.pack(pady=10, fill='x')
        self.trvFreq.heading('Intervalo', text='Intervalo', anchor="w")
        self.trvFreq.heading('FE', text='FE', anchor="w")
        self.trvFreq.heading('FO', text='FO', anchor="w")
        self.trvFreq.heading('Grupo', text='Grupo', anchor="w")
        self.resultsFreq = Label(self.wrapper21, text="")
        self.resultsFreq.grid(column=0, row=4, pady=5, padx=6, sticky="w")
        # endregion

        # region Smirnov
        # Prueba de Smirnov
        Label(self.wrapper31, text="Alpha").grid(
            row=2, column=0, padx=5, pady=3, sticky="w")
        self.alpha2 = Entry(self.wrapper31)
        self.alpha2.grid(row=2, column=1, pady=3, padx=3)
        Label(self.wrapper31, text="Cantidad de numeros").grid(
            row=3, column=0, sticky='w')
        self.txtN = Entry(self.wrapper31)
        self.txtN.grid(row=3, column=1, sticky='w')

        btnSmirnov = Button(self.wrapper31, text="Calcular",
                            command=self.CallSmirnov)
        btnSmirnov.grid(column=0, row=4, pady=5, padx=6, sticky="w")
        # Resultados Smirnov
        self.resultsSmirnov = Label(self.wrapper32, text="")
        self.resultsSmirnov.grid(column=0, row=0, pady=5, padx=6, sticky="w")
        # endregion

        # endregion

        self.wrapper4 = LabelFrame(
            root, text="Datos para la simulacion de inventarios", height="2")
        self.wrapper5 = LabelFrame(root, text="Grafica")

        self.wrapper41 = Frame(self.wrapper4)
        self.wrapper41.pack(side=LEFT, fill="y")
        self.wrapper42 = Frame(self.wrapper4)
        self.wrapper42.pack(side=RIGHT, fill="y", pady=10)

        Label(self.wrapper41, text="Q: ").grid(
            row=1, column=0, padx=2, pady=2, sticky='w')
        self.Q = Entry(self.wrapper41)
        self.Q.grid(row=1, column=1, padx=3, pady=2)
        Label(self.wrapper41, text="R: ").grid(
            row=2, column=0, padx=2, pady=2, sticky='w')
        self.R = Entry(self.wrapper41)
        self.R.grid(row=2, column=1, padx=3, pady=2)
        self.statusSimulation = Label(self.wrapper41, text="")
        self.statusSimulation.grid(
            row=3, column=0, padx=2, pady=2, sticky='w')
        BtnCalcularSimulation = Button(self.wrapper41, text="Calcular",
                                       command=self.CallSimulation)
        BtnCalcularSimulation.grid(row=4, column=0, padx=3, pady=2)

        trvSimulationScrollBar = Scrollbar(self.wrapper42, orient=HORIZONTAL)
        trvSimulationScrollBar.pack(side=BOTTOM, fill="both")
        self.trvSimulation = ttk.Treeview(self.wrapper42,  xscrollcommand=trvSimulationScrollBar.set, columns=(
            "Mes", "Reorden", "Inv_inicial", "Ri", "Dem_sim", "Factores", "Dem_ajust", "Sobrante", "Orden", "Inv_men", "Ri2", "Entrega"), show='headings', height='8')
        self.trvSimulation.pack()
        self.trvSimulation.heading('Mes', text='Mes', anchor="w")
        self.trvSimulation.heading('Reorden', text='Reorden', anchor="w")
        self.trvSimulation.heading(
            'Inv_inicial', text='Inv_inicial', anchor="w")
        self.trvSimulation.heading('Ri', text='Ri', anchor="w")
        self.trvSimulation.heading('Dem_sim', text='Dem_sim', anchor="w")
        self.trvSimulation.heading('Factores', text='Factores', anchor="w")
        self.trvSimulation.heading('Dem_ajust', text='Dem_ajust', anchor="w")
        self.trvSimulation.heading('Sobrante', text='Sobrante', anchor="w")
        self.trvSimulation.heading('Orden', text='Orden', anchor="w")
        self.trvSimulation.heading('Inv_men', text='Inv_men', anchor="w")
        self.trvSimulation.heading('Ri2', text='Ri2', anchor="w")
        self.trvSimulation.heading('Entrega', text='Entrega', anchor="w")
        trvSimulationScrollBar.config(command=self.trvSimulation.xview)


main = MainPage(root)
root.mainloop()
