import sys
import os
import pandas as pad
from pandas.core.frame import DataFrame
from scripts.generator import *
from scripts.table_chi import *


class TestFrequency:
    # Properties

    Resi = 0.000

    numTest = 0
    numsTestList = None
    FO = None
    FE = None
    intervals = [0]
    alpha = 0.0
    CHI = 0.00
    founded_chi = 0.00
    dfFinal = None
    # Data for test
    date = {
        "Intervalo": [],
        "FE": [],
        "FO": [],
        "Grupo": []
    }
    df = None

    def __init__(self, numTest, alpha, df):
        print("Simulation init")
        self.data = {
            "n": [],
            "Xn": [],
            "Xn+1": [],
            "Rn": []
        }
        self.CHI = 0.00
        self.founded_chi = 0.00
        self.Resi = 0.000

        self.alpha = alpha
        self.intervals = [0]
        self.date = {
            "Intervalo": [],
            "FE": [],
            "FO": [],
            "Grupo": []
        }
        self.dfFinal = None
        self.numTest = numTest
        self.numsTestList = [x for x in range(1, self.numTest+1)]
        self.FO = [0]*self.numTest
        self.FE = [0]*self.numTest
        self.df = df

    # Methdos
    def checkIntervals(self, number):
        for i in range(0, len(self.FO)):
            if number >= self.intervals[i] and number < self.intervals[i+1]:
                self.FO[i] = self.FO[i]+1

    def solve(self):
        print("Solving")
        numerosprueba = self.df["Rn"]
        for i in range(0, self.numTest):
            self.date["Intervalo"].append(i+1)
        for i in range(0, len(self.FE)):
            self.FE[i] = len(numerosprueba) / self.numTest
        myInterval = 1.0/float(self.numTest)
        for i in range(1, self.numTest):
            try:
                self.intervals.append(self.intervals[i-1]+myInterval)
            except Exception as e:
                print(str(e))

        self.intervals.append(1)
        self.intervals.sort()

        for i in range(0, len(numerosprueba)):
            self.checkIntervals(numerosprueba[i])

        for i in range(0, len(self.FE)):
            self.date["FE"].append(self.FE[i])
            self.date["FO"].append(self.FO[i])
        self.CHI = 0.00
        SumaFe = 0.00
        SumaFo = 0.00

        for j in range(0, len(self.FO)):
            self.CHI += ((self.FO[j] - self.FE[j]) *
                         (self.FO[j] - self.FE[j])) / self.FE[j]
            SumaFe += self.FE[j]
            SumaFo += self.FO[j]
            self.date["Grupo"].append(
                f"{str('{:.2f}'.format(self.intervals[j]))} - {str('{:.2f}'.format(self.intervals[j+1]))}")

        self.date["Intervalo"].append("Sumatoria")
        self.date["FE"].append(SumaFe)
        self.date["FO"].append(SumaFo)
        self.date["Grupo"].append("---")
        # Table chi method
        table_chi = Table_Chi(self.alpha, self.numTest)
        table_chi.getTable()
        self.founded_chi = table_chi.foundChi()
        self.dfFinal = pad.DataFrame(
            self.date, columns=["Intervalo", "FE", "FO", "Grupo"])
        print(self.dfFinal)
        return self.dfFinal, self.founded_chi, self.CHI, self.df

# Calling generator
# test = TestFrequency(20)
# test.solve()
