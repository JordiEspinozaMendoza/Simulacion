from scripts.generator import *
import pandas as pd
from pandas.core.frame import DataFrame
import math
import tkinter


class Test_Smirnov:
    porcent = 0
    n = 0
    approved = False
    def __init__(self, porcent, n, df):
        self.data_generator = {
            "n": [],
            "Xn": [],
            "Xn+1": [],
            "Rn": []
        }

        self.porcent = porcent
        self.n = n
        self.df = df

    def solve(self):
        Di = []
        nums2 = []
        excel = {'n': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20, 20: 25, 21: 30, 22: 35, 23: 40, 24: 50, 25: 60, 26: 70, 27: 80, 28: 90, 29: 100, 30: 325}, '0.10': {0: 0.95, 1: 0.776, 2: 0.642, 3: 0.564, 4: 0.51, 5: 0.47, 6: 0.438, 7: 0.411, 8: 0.388, 9: 0.368, 10: 0.352, 11: 0.338, 12: 0.352, 13: 0.314, 14: 0.304, 15: 0.295, 16: 0.286, 17: 0.278, 18: 0.272, 19: 0.264, 20: 0.24, 21: 0.22, 22: 0.21, 23: 0.1928989373, 24: 0.1725340546, 25: 0.1575013227, 26: 0.1458178903, 27: 0.1364001466, 28: 0.1285992915, 29: 0.122, 30: 0.06767342394}, '0.05': {0: 0.975, 1: 0.842,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         2: 0.708, 3: 0.624, 4: 0.563, 5: 0.521, 6: 0.486, 7: 0.457, 8: 0.432, 9: 0.409, 10: 0.391, 11: 0.375, 12: 0.361, 13: 0.349, 14: 0.338, 15: 0.328, 16: 0.318, 17: 0.309, 18: 0.301, 19: 0.294, 20: 0.264, 21: 0.242, 22: 0.23, 23: 0.21, 24: 0.188, 25: 0.172, 26: 0.16, 27: 0.15, 28: 0.141, 29: 0.134, 30: 0.07543922669}, '0.01': {0: 0.995, 1: 0.929, 2: 0.829, 3: 0.734, 4: 0.669, 5: 0.618, 6: 0.577, 7: 0.543, 8: 0.514, 9: 0.486, 10: 0.468, 11: 0.45, 12: 0.433, 13: 0.418, 14: 0.404, 15: 0.392, 16: 0.381, 17: 0.371, 18: 0.363, 19: 0.352, 20: 0.317, 21: 0.29, 22: 0.27, 23: 0.252, 24: 0.226, 25: 0.207, 26: 0.192, 27: 0.18, 28: 0.1718170862, 29: 0.163, 30: 0.09041613198}}
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
            self.approved = True
        else:
            message = "Los numeros No estan distribuidos uniformemente de acuerdo a la prueba de kolmogorov-smirnov"
            self.approved = False

        # retornacion de valoraciones infravaloradas
        return {'message': message, 'max': max(Di), 'aprox': aprox}
