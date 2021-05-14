from generator import *
import pandas as pd
from pandas.core.frame import DataFrame


class Test_Smirnov:
    data_generator = {
        "n": [],
        "Xn": [],
        "Xn+1": [],
        "Rn": []
    }
    arraySeed = []
    counter = 0
    X0 = 17.00
    a = 101.00
    c = 221.00
    m = 17001.00
    stop = False
    df = None

    def __init__(self):
        self.data_generator = {
            "n": [],
            "Xn": [],
            "Xn+1": [],
            "Rn": []
        }
        self.arraySeed = []
        self.counter = 0
        self.X0 = 17.00
        self.a = 101.00
        self.c = 221.00
        self.m = 17001.00
        self.stop = False

        Recursivo(self.X0, self.a, self.c, self.m, self.counter,
                  self.stop, self.arraySeed, self.data_generator)
        res, self.df, cols = createDataFrame(self.data_generator)

    def solve(self):
        Di = []
        A = []

        for i in self.df["Rn"]:
            A.append(i)
        A.sort()
        frequency = [0]*len(A)
        for i in range(0, len(A)):
            frequency[i] = (i+2)/(len(A))

        for i in range(0, len(A)):
            if A[i]-frequency[i] < 0:
                Di.append((A[i]-frequency[i])*(-1))
        print(Di)
        print("El valor maximo de Di es: " + str(max(Di)))


A = Test_Smirnov()
A.solve()
