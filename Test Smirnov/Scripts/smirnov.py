from scripts.generator import *
import pandas as pd
from pandas.core.frame import DataFrame
import math
import tkinter


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
    porcent = "0%"
    n = 0

    def __init__(self, porcent, n):
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
        self.porcent = porcent
        self.n = n
        Recursivo(self.X0, self.a, self.c, self.m, self.counter,
                  self.stop, self.arraySeed, self.data_generator)
        res, self.df, cols = createDataFrame(self.data_generator)

    def solve(self):
        Di = []
        nums2 = []

        excel = pd.read_excel('./scripts/table.xlsx')
        data_excel = pd.DataFrame(excel)

        for i in self.df["Rn"]:
            nums2.append(i)
        nums2.sort()
        nums = []
        for i in range(0, self.n):
            nums.append(nums2[i])
        # print(nums)
        Fn = [0]*len(nums)
        for i in range(0, len(nums)):
            Fn[i] = (i+1)/(len(nums))
        for i in range(0, len(nums)):
            # rest = Fn[i] - nums[i] detalle
            rest = nums[i]-Fn[i]
            if rest < 0:
                Di.append((rest)*(-1))
            else:
                Di.append(rest)
        aprox = 0.0
        nValues = []
        for i in data_excel['n']:
            nValues.append(i)
        if self.porcent == "10%":
            if len(nums) in (y for y in nValues if y == self.n):
                aprox = data_excel.loc[data_excel['n']
                                       == self.n, '0.10'].item()
                print(f"El valor de tablas es {aprox}")
                # print(aprox['0.10'])
            else:
                aprox = (1.22/(math.sqrt(self.n)))
                print(aprox)
        elif self.porcent == "5%":
            if self.n in (y for y in nValues if y == self.n):
                aprox = data_excel.loc[data_excel['n']
                                       == self.n, '0.05'].item()
                print(f"El valor de tablas es {aprox}")
            else:
                aprox = (1.36/math.sqrt(self.n))
                print(aprox)

        elif self.porcent == "1%":
            if self.n in (y for y in nValues if y == self.n):
                aprox = data_excel.loc[data_excel['n']
                                       == self.n, '0.01'].item()
                print(f"El valor de tablas es {aprox}")
            else:
                aprox = (1.63/math.sqrt(self.n))
                print(aprox)
        print("El valor maximo de Di es: " + str(max(Di)))
        if aprox < max(Di):
            message = "Los numeros Si estan distribuidos uniformemente de acuerdo a la prueba de kolmogorov-smirnov"
        else:
            message = "Los numeros No estan distribuidos uniformemente de acuerdo a la prueba de kolmogorov-smirnov"

        # retornacion de valoraciones infravaloradas
        return {'message': message, 'max': max(Di), 'aprox': aprox}
