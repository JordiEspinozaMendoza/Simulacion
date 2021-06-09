
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk

##from matplotlib.pyplot import figure, fill
from scripts import *
from scripts.generator import *
from scripts.frequency import TestFrequency
from scripts.smirnov import Test_Smirnov
from Ruleta import *

from exception import *
import pandas as pd
from pandastable import Table, TableModel
import tkinter.scrolledtext as scrolledtext
from ttkthemes import ThemedTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

root = ThemedTk(theme='breeze')  # tema
root.title("Proyecto en equipo")  # titulo
# tamaño de anchura de toda la ventana del ordenador
screen_width = root.winfo_screenwidth()
# tamaño de la altura toda la ventana del ordenador
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(1200, 700)


def cleanAll():
    main.wrapperGeneratorTests.pack_forget()
    main.wrapperSimulatorInv.pack_forget()
    # main.wrapperVolados.pack_forget()
    main.wrapperHelp.pack_forget()


def openHelp():
    cleanAll()
    main.wrapperHelp.pack(expand="yes", fill="both")


def openGenerator():
    cleanAll()
    main.wrapperGeneratorTests.pack(fill="both")


def openInv():
    cleanAll()
    main.wrapperSimulatorInv.pack(fill="both", expand="yes")


menubar = Menu(root)  # se crea el menu
root.config(menu=menubar)  #
helpmenu = Menu(menubar, tearoff=0)

menubar.add_command(label="Generador y pruebas", command=openGenerator)
menubar.add_command(label="Apuestas",
                    command=openInv)
menubar.add_cascade(label="Mas", menu=helpmenu)
# Menu de ayuda y demas informacion
helpmenu.add_command(label='Ayuda', command=openHelp)
helpmenu.add_command(label='Acerca del metodo')
helpmenu.add_command(label='Formulas')
helpmenu.add_command(label='Informacion de las pruebas')
helpmenu.add_command(label='Integrantes')

NavigationToolbar2Tk.toolitems = [
    t for t in NavigationToolbar2Tk.toolitems if t[0] not in ('Subplots', 0)]


class MainPage:
    # region properties
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
    test1Approved = False
    test2Approved = False
    # endregion

    # Diccionario para la info.
    helpInfo = {
        'SistemaInventario': '\nLas variables de decisión para este modelo son la cantidad a ordenar (Q) y el nivel de reorden (R), las cuales minimizan los costos totales\ndel inventario (costo de ordene, costo de llevar inventario y costos de faltante). Por consiguiente, para evaluar el funcionamiento del sistema de \nacuerdo a los valores de las variables de decisión utilizados, costos totales anuales son acumulables.',
        'AyudaInventario': '\nEl nivel de inventarios promedio mensual es utilizado para evaluar el costo de llevar inventario. Al final de cada mes se determina el número\nde unidades faltantes y el costo que este representa. La suma de los costos anteriores, proporciona el costo total anual.',
        'Volados1': '\nEste método es una manera de jugar volados, consiste en doblar la apuesta cada vez que se pierda esto con la finalidad de recuperar lo perdido.\nEn caso de ganar, la apuesta seguira siendo de $ X. ',
        'Volados2': '\nPor ejemplo, si se apuesta $ X y se pierde, entonces, se apuesta $2X; si de nuevo se vuelve a perder, entonces se apuesta $4X y así sucesivamente.\nSin embargo, si deseas continuar y la apuesta es mayor a la cantidad que dispones se apostara lo que esté disponible.'
    }
    # Constructor

    def __init__(self, root):
        self.initGeneratorTests()
        self.initSimulation()
        self.initHelp()
        self.wrapperGeneratorTests.pack(fill="both")

    def CallGenerator(self):
        self.trv2.tag_configure('oddrow', background="white")
        self.trv2.tag_configure('evenrow', background="lightblue")
        data_generator = {"n": [], "Xn": [], "Xn+1": [], "Rn": []}
        if self.X.get() == '':
            raise InputEmpty('X')

        if self.a.get() == '':
            raise InputEmpty('a')

        if self.c.get() == '':
            raise InputEmpty('c')

        if self.m.get() == '':
            raise InputEmpty('m')
        try:
            Recursivo(
                float(self.X.get()), float(self.a.get()), float(self.c.get()), float(self.m.get()), 0, False, [], data_generator)
            # Recursivo(17, 101, 221, 17001, 0, False, [], data_generator)
        except Exception as err:
            messagebox.showerror(
                "Error", "Ingresa valores con un formato correcto")
        except ZeroDivisionError as err:
            messagebox.showerror("Error", "Intentaste dividir entre cero")

        for i in self.trv2.get_children():
            self.trv2.delete(i)

        self.df = None
        self.df = pd.DataFrame(data_generator, columns=[
            'n', 'Xn', 'Xn+1', 'Rn'])

        self.trv2["column"] = list(self.df.columns)

        for column in self.trv2["column"]:
            self.trv2.heading(column, text=column)

        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
            if row[0] % 2 == 0:
                self.trv2.insert("", "end", values=row, tags=('evenrow',))
            else:
                self.trv2.insert("", "end", values=row, tags=('oddrow',))

        self.statusSimulation.config(
            text=f"Cantidad de numeros: {len(self.df['Rn'])}")

    def CallFrequency(self):
        self.trvFreq.tag_configure('oddrow', background="white")
        self.trvFreq.tag_configure('evenrow', background="lightblue")
        if self.nGroups.get() == '':
            raise InputEmpty('numero de grupos')

        if self.alpha.get() == '':
            raise InputEmpty('Nivel de significancia')

        try:

            for i in self.trvFreq.get_children():  # FRECUENCIA
                self.trvFreq.delete(i)

            self.dfFrequency = None

            # testFrequency = TestFrequency(
            #     10, 0.5, self.df)
            testFrequency = TestFrequency(
                int(self.nGroups.get()), float(self.alpha.get()), self.df)
            self.dfFrequency, self.foundedChiFreq, self.chiFreq, self.dfFreq = testFrequency.solve()
        except Exception as err:
            messagebox.showinfo(
                "Error", "Ingresa valores correctos para la simulacion")
        except ZeroDivisionError as err:
            messagebox.showerror("Error", "Intentaste dividir entre cero")

        if self.chiFreq > self.foundedChiFreq:
            self.resultsFreq.configure(
                text=f"Los numeros analizados no \nestan distribuidos uniformemente de \nacuerdo a la prueba de la frecuencia \n\nCHI calculada: {str(self.chiFreq)}\n\nCHI de tabla: {str(self.foundedChiFreq)}")  # Mensaje
            self.test1Approved = False
        else:
            self.resultsFreq.configure(
                text=f"Los numeros analizados si \nestan distribuidos uniformemente de \nacuerdo a \nla prueba de la frecuencia \n\nCHI calculada: {str(self.foundedChiFreq)}\n\nCHI de tabla:{str(self.chiFreq)}")
            self.test1Approved = True

        for column in self.trvFreq["column"]:
            self.trvFreq.heading(column, text=column)
        df_rows = self.dfFrequency.to_numpy().tolist()
        for row in df_rows:
            if row[0] == "Sumatoria":
                print(row[0])
                self.trvFreq.insert("", "end", values=row, tags=('evenrow',))
            else:
                if row[0] % 2 == 0:
                    print(row[0])
                    self.trvFreq.insert(
                        "", "end", values=row, tags=('evenrow',))
                else:
                    print(row[0])
                    self.trvFreq.insert(
                        "", "end", values=row, tags=('oddrow',))

        # if self.test1Approved==True:
        #     self.statusVolados.config(text=f"{self.statusVolados.get()}\nPrueba Frecuencia aprobada")
        # else:
        #     self.statusVolados.config(text=f"{self.statusVolados.get()}\nPrueba Frecuencia no aprobada")

    def CallSmirnov(self):

        if self.txtN == '':
            raise InputEmpty('Numero de grupos')

        if self.alpha2.get() == '':
            raise InputEmpty('Nivel de significancia')

        try:
            smirnov = Test_Smirnov(f"{self.alpha2.get()}%",
                                   int(self.txtN.get()), self.df)
            res = smirnov.solve()
            self.resultsSmirnov.config(
                text=f"{res['message']}\nEl numero Di Maximo es: {str(res['max'])}\nEl valor Di de tablas es: {str(res['aprox'])}")

            self.test2Approved = smirnov.approved
        except Exception as err:
            messagebox.showinfo(
                "Error", "Ingresa valores correctos para la prueba de Smirnov")
            print(str(err))
        except ZeroDivisionError as err:
            messagebox.showerror("Error", "Intentaste dividir entre cero")

    def CallSimulation(self):
        if self.R.get() == '':
            raise InputEmpty('Punto de reorden')

        if self.Q.get() == '':
            raise InputEmpty('Cantidad inicial')

        if self.test1Approved == False:
            raise TestNotApproved("Frecuencia")

        if self.test2Approved == False:
            raise TestNotApproved("Smirnov")

        self.trvSimulation.tag_configure('oddrow', background="white")
        self.trvSimulation.tag_configure('evenrow', background="lightblue")

        try:
            for i in self.trvSimulation.get_children():
                print("Borrando")
                self.trvSimulation.delete(i)

            self.simulation = ApuestaRuleta(
                self.df['Rn'].to_list(), int(self.R.get()), float(self.Q.get()))

            if(self.Color.get() == 'Apuesta rojo'):
                print("Llamando Rojo")
                self.simulation.ApuestaRojo()
            else:
                print("Llamando Negro")
                self.simulation.ApuestaNegro()

            self.dfSimulation = None

            data_simulation = self.simulation.data_simulation
            self.dfSimulation = pd.DataFrame(data_simulation)

            for column in self.trvSimulation["column"]:
                self.trvSimulation.heading(column, text=column)
            self.df_rows = self.dfSimulation.to_numpy().tolist()

            for row in self.df_rows:
                if row[0] % 2 == 0:
                    self.trvSimulation.insert(
                        "", "end", values=row, tags=('evenrow',))
                else:
                    self.trvSimulation.insert(
                        "", "end", values=row, tags=('oddrow',))

            # configurando el texto
            self.textResultados.config(text=self.simulation.Resultado)
            dataResults = [self.simulation.Vganadas1,
                           self.simulation.Vperdidas1, self.simulation.empate]
            dataLabels = [f"Ganó {self.simulation.Vganadas1} veces",
                          f"Perdió {self.simulation.Vperdidas1} veces", f"Empato {self.simulation.empate} veces"]
            explode = (0.1, 0,0.2)
            figure2 = plt.Figure(figsize=(4, 3), dpi=100)
            subplot2 = figure2.add_subplot(111)
            subplot2.pie(dataResults, labels=dataLabels,
                     autopct='%1.1f%%', shadow=True, startangle=90, explode=explode)
            try:
                self.pieFigure.get_tk_widget().pack_forget()
            except:
                pass
            self.pieFigure = FigureCanvasTkAgg(figure2, self.wrapper5)
            self.pieFigure.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   

        except Exception as err:
            messagebox.showinfo(
                "Error", str(err))

    def initGeneratorTests(self):
        # region Ventana generador y tests
        # Wrappers o contenedores dentro de la ventana(root)
        self.wrapperGeneratorTests = Frame(root)

        self.wrapper1 = LabelFrame(
            self.wrapperGeneratorTests, text="Datos de entrada para el generador")
        self.wrapper2 = LabelFrame(
            self.wrapperGeneratorTests, text="Prueba de la frecuencia")
        self.wrapper3 = LabelFrame(
            self.wrapperGeneratorTests, text="Prueba de kolmogorov-smirnov")

        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
        # region Wrappers Generador y tests

        # Contendores para el wrapper1
        self.wrapper11 = Frame(self.wrapper1)
        self.wrapper11.pack(side=LEFT, fill="y")
        self.wrapper12 = Frame(self.wrapper1)
        self.wrapper12.pack(side=RIGHT, fill="y")

        # Contendores para el self.wrapper2
        self.wrapper21 = Frame(self.wrapper2)
        self.wrapper21.pack(side=LEFT, fill="y")
        self.wrapper22 = Frame(self.wrapper2)
        self.wrapper22.pack(side=RIGHT, fill="y")

        # Contendores para el self.wrapper3
        self.wrapper31 = Frame(self.wrapper3)
        self.wrapper31.pack(side=LEFT, fill="y")
        self.wrapper32 = Frame(self.wrapper3)
        self.wrapper32.pack(side=LEFT, fill="y")

        # endregion

        # region inputs generador
        # Inputs para generador
        Label(self.wrapper11, text="X: ").grid(
            row=1, column=0, padx=2, pady=2, sticky='w')
        self.X = Entry(self.wrapper11)
        self.X.grid(row=1, column=1, padx=3, pady=2)
        Label(self.wrapper11, text="a: ").grid(
            row=3, column=0, padx=2, pady=2, sticky='w')
        self.a = Entry(self.wrapper11)
        self.a.grid(row=3, column=1, padx=3, pady=2)
        Label(self.wrapper11, text="c: ").grid(
            row=5, column=0, padx=2, pady=2, sticky='w')
        self.c = Entry(self.wrapper11)
        self.c.grid(row=5, column=1, padx=3, pady=2)
        Label(self.wrapper11, text="m: ").grid(
            row=6, column=0, padx=2, pady=2, sticky='w')
        self.m = Entry(self.wrapper11)
        self.m.grid(row=6, column=1, padx=3, pady=2)

        # Boton para calcular dependiendo de la insercion de datos
        BtnCalcular = Button(self.wrapper11, text="Calcular",
                             command=self.CallGenerator)
        BtnCalcular.grid(row=7, column=0, padx=3, pady=2)
        scrollGenerator = Scrollbar(self.wrapper12)
        self.trv2 = ttk.Treeview(self.wrapper12, columns=(
            "n", "Xn", "Xn+1", "Rn"), show='headings', height='8',  yscrollcommand=scrollGenerator.set)
        self.trv2.grid(row=1, column=3, sticky="ne")
        self.trv2.heading('n', text='n', anchor="w")
        self.trv2.heading('Xn', text='Xn', anchor="w")
        self.trv2.heading('Xn+1', text='Xn+1', anchor="w")
        self.trv2.heading('Rn', text='Rn', anchor="w")

        scrollGenerator.grid(row=1, column=4, sticky=N+S+W)
        scrollGenerator.config(command=self.trv2.yview)

        # endregion

        # region frequency
        lbl2 = Label(self.wrapper21, text="Cantidad de grupos").grid(
            row=1, column=0, padx=5, pady=3, sticky='w')
        self.nGroups = Entry(self.wrapper21)
        self.nGroups.grid(row=1, column=1, pady=3, padx=3)

        lbl3 = Label(self.wrapper21, text="Alpha").grid(
            row=2, column=0, padx=5, pady=3, sticky="w")
        self.alpha = Combobox(self.wrapper21, state="readonly")
        self.alpha["values"] = ["0.001", "0.0025", "0.005", "0.01", "0.025",
                                "0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5"]
        self.alpha.grid(row=2, column=1, pady=3, padx=3)

        btn = Button(self.wrapper21, text="Calcular",
                     command=self.CallFrequency)
        btn.grid(column=0, row=3, pady=5, padx=6, sticky="w")

        # Resultados Freq
        scrollbarFreq = Scrollbar(self.wrapper22)
        scrollbarFreq.pack(side=RIGHT, fill=Y)

        self.trvFreq = ttk.Treeview(self.wrapper22, columns=("Intervalo", "FE",
                                                             "FO", "Grupo"), show="headings", height="6", yscrollcommand=scrollbarFreq.set)
        self.trvFreq.pack(pady=10, fill='x')
        self.trvFreq.heading('Intervalo', text='Intervalo', anchor="w")
        self.trvFreq.heading('FE', text='FE', anchor="w")
        self.trvFreq.heading('FO', text='FO', anchor="w")
        self.trvFreq.heading('Grupo', text='Grupo', anchor="w")
        self.resultsFreq = Label(self.wrapper21, text="")
        self.resultsFreq.grid(column=0, row=4, pady=5, padx=6, sticky="w")
        scrollbarFreq.config(command=self.trvFreq.yview)
        # endregion

        # region Smirnov
        # Prueba de Smirnov
        Label(self.wrapper31, text="Alpha (%)").grid(
            row=2, column=0, padx=5, pady=3, sticky="w")
        self.alpha2 = Combobox(self.wrapper31, state="readonly")
        self.alpha2["values"] = ["1", "5", "10"]
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

    def initSimulation(self):
        # region simulador
        self.wrapperSimulatorInv = Frame(root)

        self.wrapper4 = LabelFrame(
            self.wrapperSimulatorInv, text="Datos para el juego de la ruleta", height="2")
        self.wrapper5 = LabelFrame(
            self.wrapperSimulatorInv, text="Grafica", height="2")

        self.wrapper4.pack(fill="both", padx=20, pady=10)
        self.wrapper5.pack(fill="both", expand="yes", padx=20, pady=10)

        self.wrapper41 = Frame(self.wrapper4)
        self.wrapper41.pack(side=LEFT, fill="y")
        self.wrapper42 = Frame(self.wrapper4)
        self.wrapper42.pack(side=RIGHT, fill="y", pady=10)

        Label(self.wrapper41, text="Cantidad de dinero inicial: ").grid(
            row=1, column=0, padx=2, pady=2, sticky='w')
        self.Q = Entry(self.wrapper41)
        self.Q.grid(row=1, column=1, padx=3, pady=2)
        Label(self.wrapper41, text="Número de juegos que desea simular: ").grid(
            row=2, column=0, padx=2, pady=2, sticky='w')
        self.R = Entry(self.wrapper41)
        self.R.grid(row=2, column=1, padx=3, pady=2)
        self.statusSimulation = Label(self.wrapper41, text="")
        self.statusSimulation.grid(
            row=3, column=0, padx=2, pady=2, sticky='w')

        Label(self.wrapper41, text="Color que se apostará: ").grid(
            row=4, column=0, padx=2, pady=2, sticky='w')
        self.Color = Combobox(self.wrapper41, state="readonly")
        self.Color["values"] = ["Apuesta rojo", "Apuesta negro"]
        self.Color.grid(row=4, column=1, padx=2, pady=2, sticky='w')

        BtnCalcularSimulation = Button(self.wrapper41, text="Calcular",
                                       command=self.CallSimulation)
        BtnCalcularSimulation.grid(row=5, column=0, padx=3, pady=2)
        self.textResultados = Label(self.wrapper41, text="")
        self.textResultados.grid(row=6, column=0, padx=2, pady=2)
        trvSimulationScrollBar = Scrollbar(self.wrapper42, orient=HORIZONTAL)
        trvSimulationScrollBar.pack(side=BOTTOM, fill="both")
        self.trvSimulation = ttk.Treeview(self.wrapper42,  xscrollcommand=trvSimulationScrollBar.set, columns=(
            "Número de juego", "Resultado", "Jugador 1", "Jugador 2"), show='headings', height='8')
        self.trvSimulation.pack()
        self.trvSimulation.heading(
            'Número de juego', text='Número de juego', anchor="w")
        self.trvSimulation.heading('Resultado', text='Resultado', anchor="w")
        self.trvSimulation.heading(
            'Jugador 1', text='Jugador 1', anchor="w")
        self.trvSimulation.heading('Jugador 2', text='Jugador 2', anchor="w")

        self.trvSimulation.column('Número de juego', stretch=NO, width=130)
        self.trvSimulation.column('Resultado', stretch=NO, width=130)
        self.trvSimulation.column('Jugador 1', stretch=NO, width=130)
        self.trvSimulation.column('Jugador 2', stretch=NO, width=130)

        trvSimulationScrollBar.config(command=self.trvSimulation.xview)

    def initHelp(self):
        self.wrapperHelp = Frame(root)

        self.HelpInventario = LabelFrame(
            self.wrapperHelp, text="Ayuda Sistema inventarios")
        self.HelpInventario.pack(fill="both", expand="yes", padx=20, pady=10)
        Label(
            self.HelpInventario, text="Sistema de inventario.", font=("Arial", 16)).grid(row=0, column=0, sticky="W")
        Label(
            self.HelpInventario, text=self.helpInfo['SistemaInventario'], font=("Arial", 10)).grid(row=1, column=0, sticky="W")
        Label(self.HelpInventario, text=self.helpInfo['AyudaInventario'],
              font=("Arial", 10)).grid(row=2, column=0, sticky="W")

        self.HelpVolado = LabelFrame(
            self.wrapperHelp, text="Ayuda Juego de volados")
        self.HelpVolado.pack(fill="both", expand="yes", padx=20, pady=10)
        Label(
            self.HelpVolado, text="Juego de volados.", font=("Arial", 16)).grid(row=0, column=0, sticky="W")

        Label(self.HelpVolado, text=self.helpInfo['Volados1'], font=(
            "Arial", 10)).grid(row=1, column=0, sticky="W")
        Label(self.HelpVolado, text=self.helpInfo['Volados2'], font=(
            "Arial", 10)).grid(row=2, column=0, sticky="W")

    def initVolados(self):
        # region PRUEBA DE VOLADOS
        self.wrapperVolados = Frame(root)
        self.wrapperVoladosEntry = LabelFrame(
            self.wrapperVolados, text="Prueba de Volados")
        self.wrapperVoladosGraph = LabelFrame(
            self.wrapperVolados, text="Grafica")

        self.wrapperVoladosEntry.pack(fill="both", padx=20, pady=10)
        self.wrapperVoladosGraph.pack(
            fill="both", expand="yes", padx=20, pady=10)

        self.wrapperVoladosInput = Frame(self.wrapperVoladosEntry)
        self.wrapperVoladosInput.pack(side=LEFT, fill="y")

        self.wrapperVoladosMessage = Frame(self.wrapperVoladosEntry)
        self.wrapperVoladosMessage.pack(side=RIGHT, fill="y")

        Label(self.wrapperVoladosInput, text="Inserte el dinero con el que quiere empezar: ").grid(
            row=1, column=0, padx=3, pady=2)

        self.txtDinero = Entry(self.wrapperVoladosInput)
        self.txtDinero.grid(
            row=1, column=1, padx=3, pady=2)

        Label(self.wrapperVoladosInput, text="Inserte la apuesta: ").grid(
            row=2, column=0, padx=3, pady=2)

        self.txtApuesta = Entry(self.wrapperVoladosInput)
        self.txtApuesta.grid(
            row=2, column=1, padx=3, pady=2)
        self.statusVolados = Label(self.wrapperVoladosInput, text="")
        self.statusVolados.grid(
            row=3, column=0, padx=2, pady=2, sticky='w')
        Button(self.wrapperVoladosInput, text='Calcular', command=self.CallVolados).grid(
            row=4, column=0, padx=3, pady=2)  # falta el comando

        self.resultsVolado = scrolledtext.ScrolledText(
            self.wrapperVoladosMessage)
        self.resultsVolado.pack()
        # endregion FIN DE LA PRUEBA DEVOLADA


main = MainPage(root)
root.mainloop()
