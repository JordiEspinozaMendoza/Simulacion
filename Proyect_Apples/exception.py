from tkinter import messagebox

class InputEmpty(Exception):
    def __init__(self, input):
        messagebox.showinfo("Error",f"Apartado {input} vacio")
class TestNotApproved(Exception):
    def __init__(self, testName):
        messagebox.showinfo("Error", f"En la prueba de {testName} los números no son adecuados para seguir")
class MonthsSimulation(Exception):
    def __init__(self):
        messagebox.showinfo("Error", f"Esa cantidad de numeros no esta disponible")