import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from generator import *
import pandas as pd
from pandastable import Table, TableModel
import tkinter.scrolledtext as scrolledtext

data = {
    "n": [],
    "Xn": [],
    "Xn+1": [],
    "Rn": []
}
Resi = 0.000
ArraySemilla = []
conta = 0
X0 = 17.00
a = 101.00
c = 221.00
m = 17001.00
Detener = False

window = tk.Tk()
# Properties
window.title("Generador de numeros pseudoaleatorios")
window.geometry("700x400")
window.resizable(False, False)

lbl = Label(window, text="Generador de numeros",  font=("Arial", 14))
lbl.grid(column=0, row=0, columnspan=2)
# Scrollbar
def clickedGenerator():
    Recursivo(X0, a, c, m, conta, Detener, ArraySemilla, data)
    res, df, cols = createDataFrame(data)
    table.insert(tk.INSERT, res)
    table.config(state=DISABLED)


btn = Button(window, text="Generar numeros", command=clickedGenerator)
btn.grid(column=0, row=1)

table = scrolledtext.ScrolledText(window, height="20", width="55", undo=True)
table.grid(column=2, row=5)

window.mainloop()
