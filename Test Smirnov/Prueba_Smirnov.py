import tkinter as tk
from tkinter import *
from scripts.smirnov import Test_Smirnov

main = tk.Tk()
main.geometry("600x500")
main.title("Prueba de kolmogorov-smirnov.")
main.resizable(False, False)

Label1 = Label(main)
Label2 = Label(main)
Label3 = Label(main)

def clickSolve():
    smirnov = Test_Smirnov(TxtAlpha.get(), int(txtN.get()))
    result = smirnov.solve()

    Label1.configure(text=result['message'])
    Label2.configure(text=f"El numero Di Maximo es: {str(result['max'])}")
    Label3.configure(text=f"El valor Di de tablas es: {str(result['aprox'])}")


Label(main, text="Prueba de kolmogorov-smirnov",
      font=("Arial", 14)).grid(row=0, column=0, sticky='NW')
Label(main, text="Inserte el numero de alpha: ").grid(row=1, column=0, sticky='NW')

TxtAlpha = tk.Entry(main)
TxtAlpha.grid(row=2, column=0,sticky='NW')

Label(main, text="Inserte el numero de numeros que desea utilizar: ").grid(
    row=3, column=0,sticky='NW')

txtN = tk.Entry(main)
txtN.grid(row=4, column=0,sticky='NW')

btnSolve = tk.Button(main, text="Calcular",
                     command=clickSolve).grid(row=5, column=0,sticky='NW')
# ///*btnSolve.pack()*/

Label1.grid(sticky='NW')

Label2.grid(sticky='NW')

Label3.grid(sticky='NW')

main.mainloop()
