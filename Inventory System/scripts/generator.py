import sys
import os
import pandas as pd

sys.setrecursionlimit(10000)

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
    
        if Detener==True or conta==10000:
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


