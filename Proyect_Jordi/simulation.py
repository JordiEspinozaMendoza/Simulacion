import pandas as pd


class SimulationApples:

    distribution = {
        "duration": [3, 5, 8, 10, 14, 16],
        "prob": [0.15, 0.08, 0.12, 0.20, 0.25, 0.20]
    }
    distribution_cumulative = {
        "duration": [], "L_inf": [], "L_sup": []}
    test = [0.11399, 0.52632, 0.17152, 0.33645, 0.99453]
    dataFinal = {
        "year": [],
        "days": []
    }
    finalDuration = None
    years = 0
    normalPrice = 0.0
    politicTwoCounter = 0
    politicTwo = False

    finalPorcent = 0.0
    finalMessage = ""
    # Constructor

    def __init__(self, df, years, normalPrice):
        self.df = df
        self.years = years
        self.normalPrice = normalPrice
        self.dataFinal = {
            "year": [],
            "days": []
        }

    # Methods for limits

    def Calc_probability_delivery(self):
        self.distribution_cumulative = {
            "duration": [], "L_inf": [], "L_sup": []}

        for i in range(0, len(self.distribution["duration"])):
            self.distribution_cumulative["duration"].append(
                self.distribution["duration"][i]
            )
            if i == 0:
                self.distribution_cumulative["L_sup"].append(
                    self.distribution["prob"][i]
                )
                self.distribution_cumulative["L_inf"].append(0)
            else:
                self.distribution_cumulative["L_sup"].append(
                    self.distribution_cumulative["L_sup"][i - 1]
                    + self.distribution["prob"][i]
                )
                self.distribution_cumulative["L_inf"].append(
                    self.distribution_cumulative["L_sup"][i - 1]
                )

    def checkIntervals(self, number, actualYear):
        try:
            for i in range(0, 6):
                # Limits
                L_inf = self.distribution_cumulative["L_inf"][i]
                L_sup = self.distribution_cumulative["L_sup"][i]

                if number >= L_inf and number <= L_sup:
                    self.dataFinal["year"].append(actualYear)
                    self.dataFinal["days"].append(
                        self.distribution_cumulative["duration"][i])
                    if self.distribution_cumulative["duration"][i] < 14:
                        self.politicTwoCounter += 1
        except Exception as e:
            print(str(e))

    def PoliticOne(self):
        try:
            earned = ((self.normalPrice*100)*30)/100.0
            self.finalMessage+=f"Ganado: ${earned}"
        except Exception as e:
            print(str(e))

    def PoliticTwo(self):
        try:
            self.checkIntervals(self.df[self.years+1], self.years+1)
            if self.dataFinal["days"][-1] >= 14:
                print(self.dataFinal["days"][-1])
                earned = (self.normalPrice*100)*70/100.0
                self.finalMessage+=f"El clima no mejoro este año\nGanado: ${earned}"
                
            else:
                print(self.dataFinal["days"][-1])
                earned = (self.normalPrice*100)*10/100.0
                self.finalMessage+=f"El clima mejoro este año\nPerdido: ${earned}"

        except Exception as e:
            print(str(e))

    def Solve(self):
        try:
            for i in range(0, self.years):
                self.checkIntervals(self.df[i], i+1)

            self.finalPorcent = (self.politicTwoCounter*100)/self.years
            self.finalMessage = f"\nAños simulados: {self.years}\nPorcentaje final de clima frio: {self.finalPorcent}%\n"

            if ((self.years * 25)/100.0) >= self.politicTwoCounter:
                self.finalMessage += "Politica 1 implementada\n"
                self.PoliticOne()
            else:
                self.finalMessage += "Politica 2 implementada\n"
                self.PoliticTwo()

            return self.dataFinal
        except Exception as e:
            print(str(e))
