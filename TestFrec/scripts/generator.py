import sys
import os
import pandas as pd

sys.setrecursionlimit(5000)

# X = Semilla
# a = Multiplicador
# c = Constante aditiva
# m = Modulo

def Operacion(X, a, c, m):
     Resi = ((a*X)+c) % m
     return Resi
     
def createDataFrame(data):
    df = pd.DataFrame(data, columns=["n","Xn","Xn+1","Rn"])
    cols = list(df.columns)
    return df.to_string(), df, cols

def Recursivo(X0, a, c, m, conta,Detener, ArraySemilla, data):
    try:
        for Semilla in ArraySemilla:
            if X0==Semilla:
                Detener = True
    
        if Detener==True or conta==325:
            pass
        else:         
            data["n"].append(conta+1)
            data["Xn"].append(X0)  
            data["Xn+1"].append(Operacion(X0,a,c,m))  
            data["Rn"].append(Operacion(X0,a,c,m)/m)  
            conta = conta + 1
            ArraySemilla.append(X0)
            Recursivo(Operacion(X0,a,c,m),a,c,m,conta,Detener, ArraySemilla, data)
    except Exception as e: 
        print(str(e))    






        
#Info para el generador
# LabelX = Label(wrapper3,text="X").grid(row=1,column=0,padx=5,pady=3,sticky='w')
# EntradaX = Entry(wrapper3)
# EntradaX.grid(row=1,column=1,padx=3,pady=3)  

# Labela=Label(wrapper3,text="a").grid(row=2,column=0,padx=5,pady=3,sticky='w')
# Entradaa = Entry(wrapper3)
# Entradaa.grid(row=2,column=1,padx=3,pady=3)

# Labelc=Label(wrapper3,text="c").grid(row=3,column=0,padx=5,pady=3,sticky='w')
# Entradac = Entry(wrapper3)
# Entradac.grid(row=3,column=1,padx=3,pady=3)

# Labelm=Label(wrapper3,text="m").grid(row=4,column=0,padx=5,pady=3,sticky='w')
# Entradam = Entry(wrapper3)
# Entradam.grid(row=4,column=1,padx=3,pady=3)
#Fin info para el generador


