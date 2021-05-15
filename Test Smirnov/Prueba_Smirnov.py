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


Label(main, text="Prueba de kolmogorov-smirnov", font=("Arial", 14)).pack()
Label(main, text="Inserte el numero de alpha: ").pack()

TxtAlpha = tk.Entry(main)
TxtAlpha.pack()

Label(main, text="Inserte el numero de numeros que desea utilizar: ").pack()

txtN = tk.Entry(main)
txtN.pack()

btnSolve = tk.Button(main, text="Calcular", command=clickSolve).pack()
# ///*btnSolve.pack()*/

Label1.pack()

Label2.pack()

Label3.pack()

main.mainloop()
