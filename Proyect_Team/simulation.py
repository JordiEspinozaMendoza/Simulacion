import pandas as pd
from scripts.generator import *
import random
import matplotlib.pyplot as plt


class inventory_system:
    # Data for initial values
    month_demand = {
        "qty": [
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
        ],
        "prob": [
            0.010,
            0.015,
            0.020,
            0.020,
            0.022,
            0.023,
            0.025,
            0.027,
            0.028,
            0.029,
            0.035,
            0.045,
            0.060,
            0.065,
            0.070,
            0.080,
            0.075,
            0.070,
            0.065,
            0.060,
            0.050,
            0.040,
            0.030,
            0.016,
            0.015,
            0.005,
        ],
    }
    prob_delivery_months = {"months": [1, 2, 3], "prob": [0.30, 0.40, 0.30]}
    seasonal_factors = {
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "factor": [
            1.20,
            1.00,
            0.90,
            0.80,
            0.80,
            0.70,
            0.80,
            0.90,
            1.00,
            1.20,
            1.30,
            1.40,
        ],
    }
    initial_values = {
        "inv_initial": 150,
        "order_cost": 50,
        "inventory_cost": 26,
        "cost_absences": 25,
        "days_year": 260,
        "month_demand": month_demand,
        "prob_delivery_months": prob_delivery_months,
        "seasonal_factors": seasonal_factors,
    }
    # Data for simulation
    cumulative_probability_delivery = {"months": [], "L_inf": [], "L_sup": []}
    cumulative_probability = {"qty": [], "L_inf": [], "L_sup": []}
    Q = 0
    R = 0
    # Data for generator
    data_generator = {"n": [], "Xn": [], "Xn+1": [], "Rn": []}
    arraySeed = []
    counter = 0
    X0 = 17.00
    a = 101.00
    c = 221.00
    m = 17001.00
    stop = False
    # End data for generator

    # Data for simulat------------------------ion awaiting
    data_simulation = {
        "month": [],
        "reorder": [],
        "inv_initial": [],
        "Ri": [],
        "dem_sim": [],
        "seasonal_factors": [],
        "dem_adjust": [],
        "inv_final": [],
        "missing": [],
        "order": [],
        "inv_monthly": [],
        "Ri2": [],
        "month_delivered": [],
    }
    dfFinal = None
    # Constructor

    def __init__(self, R, Q, df):
        self.R = R
        self.Q = Q
        self.data_generator = df
        self.data_simulation = {
            "month": [],
            "reorder": [],
            "inv_initial": [],
            "Ri": [],
            "dem_sim": [],
            "seasonal_factors": [],
            "dem_adjust": [],
            "inv_final": [],
            "missing": [],
            "order": [],
            "inv_monthly": [],
            "Ri2": [],
            "month_delivered": [],
        }                

    # Methods for limits
    def Calc_probability_delivery(self):
        self.cumulative_probability_delivery = {
            "months": [], "L_inf": [], "L_sup": []}

        for i in range(0, len(self.initial_values["prob_delivery_months"]["months"])):
            self.cumulative_probability_delivery["months"].append(
                self.initial_values["prob_delivery_months"]["months"][i]
            )
            if i == 0:
                self.cumulative_probability_delivery["L_sup"].append(
                    self.initial_values["prob_delivery_months"]["prob"][i]
                )
                self.cumulative_probability_delivery["L_inf"].append(0)
            else:
                self.cumulative_probability_delivery["L_sup"].append(
                    self.cumulative_probability_delivery["L_sup"][i - 1]
                    + self.initial_values["prob_delivery_months"]["prob"][i]
                )
                self.cumulative_probability_delivery["L_inf"].append(
                    self.cumulative_probability_delivery["L_sup"][i - 1]
                )

    def Calc_probability_month(self):
        self.cumulative_probability = {"qty": [], "L_inf": [], "L_sup": []}
        for i in range(0, len(self.initial_values["month_demand"]["qty"])):
            self.cumulative_probability["qty"].append(
                self.initial_values["month_demand"]["qty"][i]
            )
            if i == 0:
                self.cumulative_probability["L_sup"].append(
                    self.initial_values["month_demand"]["prob"][i]
                )
                self.cumulative_probability["L_inf"].append(0)
            else:
                self.cumulative_probability["L_sup"].append(
                    self.cumulative_probability["L_sup"][i - 1]
                    + self.initial_values["month_demand"]["prob"][i]
                )
                self.cumulative_probability["L_inf"].append(
                    self.cumulative_probability["L_sup"][i - 1]
                )
        # df = pd.DataFrame(self.cumulative_probability)
        # print(df)

    orderActive = False
    limitMonth = None
    counterMonth = None
    missingQty = 0
    counterRn = 0
    counterOrder = 0
    def CreatePlot(self):
        data = {'Month': self.dfFinal['month'],
                'data': self.dfFinal['dem_sim']}
        df = pd.DataFrame(data, columns=['Month', 'data'])
        df.plot(x='Month', y='data', kind='line')
        plt.show()
    # Main simulation
    def Simulation(self):
        try:
            # We simulate 12 months (1 year)
            for y in range(0, 12):
                # We take 1 num pseudo from the generator
                num_pseudo = self.data_generator["Rn"][self.counterRn]
                self.counterRn += 1
                if y == 0:
                    self.data_simulation["inv_initial"].append(
                        self.initial_values["inv_initial"]
                    )
                else:
                    self.data_simulation["inv_initial"].append(new_inv)

                self.data_simulation["month"].append(y + 1)
                self.data_simulation["seasonal_factors"].append(
                    self.initial_values["seasonal_factors"]["factor"][y]
                )
                self.data_simulation["reorder"].append(self.R)
                self.data_simulation["Ri"].append(num_pseudo)

                for i in range(0, len(self.cumulative_probability["qty"])):
                    l_inf = self.cumulative_probability["L_inf"][i]
                    l_sup = self.cumulative_probability["L_sup"][i]
                    qty = self.cumulative_probability["qty"][i]
                    if num_pseudo >= l_inf and num_pseudo <= l_sup:
                        self.data_simulation["dem_sim"].append(qty)
                    else:
                        pass
                self.data_simulation["dem_adjust"].append(
                    int(
                        self.data_simulation["dem_sim"][y]
                        * self.data_simulation["seasonal_factors"][y]
                    )
                )
                if (
                    self.data_simulation["inv_initial"][y]
                    - self.data_simulation["dem_adjust"][y]
                    > 0
                ):
                    self.data_simulation["inv_final"].append(
                        self.data_simulation["inv_initial"][y]
                        - self.data_simulation["dem_adjust"][y]
                    )
                    self.data_simulation["missing"].append(0)
                else:
                    self.data_simulation["inv_final"].append(0)
                    self.data_simulation["missing"].append(
                        (
                            self.data_simulation["inv_initial"][y]
                            - self.data_simulation["dem_adjust"][y]
                        )
                        * (-1)
                    )
                    self.missingQty += self.data_simulation["missing"][y]
                new_inv = self.data_simulation["inv_final"][y]
                # If R > Inv final
                if self.data_simulation["inv_final"][y] < self.R:
                    # If we have a order
                    if self.orderActive == True:
                        if self.limitMonth == self.counterMonth:
                            self.orderActive = False
                            self.limitMonth = 0
                            self.counterMonth = 1
                            new_inv = self.data_simulation["inv_final"][y] + self.Q
                            new_inv = new_inv - self.missingQty
                            self.missingQty = 0
                            self.data_simulation["month_delivered"].append(
                                "---")
                            self.data_simulation["Ri2"].append("---")
                            self.data_simulation["order"].append(0)
                        else:
                            self.counterMonth += 1
                            self.data_simulation["month_delivered"].append(
                                "---")
                            self.data_simulation["Ri2"].append("---")
                            self.data_simulation["order"].append(0)
                    # If we not have a order
                    else:
                        randomRn = self.data_generator["Rn"][self.counterRn]
                        self.counterRn += 1
                        self.data_simulation["Ri2"].append(randomRn)
                        for i in range(
                            0, len(
                                self.cumulative_probability_delivery["months"])
                        ):
                            l_inf = self.cumulative_probability_delivery["L_inf"][i]
                            l_sup = self.cumulative_probability_delivery["L_sup"][i]
                            if randomRn >= l_inf and randomRn <= l_sup:
                                self.data_simulation["month_delivered"].append(
                                    self.cumulative_probability_delivery["months"][i]
                                )
                                self.counterMonth = 1
                                self.limitMonth = self.cumulative_probability_delivery[
                                    "months"
                                ][i]
                                self.orderActive = True
                                self.counterOrder+=1
                                self.data_simulation["order"].append(self.counterOrder)
                else:
                    # If we have a order
                    if self.orderActive == True:
                        if self.limitMonth == self.counterMonth:
                            self.orderActive = False
                            self.limitMonth = 0
                            self.counterMonth = 0
                            new_inv = self.data_simulation["inv_final"][y] + self.Q
                            new_inv = new_inv - self.missingQty
                            self.missingQty = 0
                            self.data_simulation["month_delivered"].append(
                                "---")
                            self.data_simulation["Ri2"].append("---")
                            self.data_simulation["order"].append(0)
                        else:
                            self.counterMonth += 1
                            self.data_simulation["month_delivered"].append(
                                "---")
                            self.data_simulation["Ri2"].append("---")
                            self.data_simulation["order"].append(0)
                    # If we not have a order
                    else:
                        self.data_simulation["Ri2"].append("---")
                        self.data_simulation["month_delivered"].append("---")
                        self.data_simulation["order"].append(0)

                if self.data_simulation["inv_initial"][y] == 0:
                    if self.data_simulation["inv_initial"][y] == 0:
                        self.data_simulation["inv_monthly"].append(
                            ((self.data_simulation["inv_final"][y]) / 2)
                            * (
                                self.data_simulation["inv_final"][y]
                                / self.data_simulation["dem_adjust"][y]
                            )
                        )
                elif self.data_simulation["inv_final"][y] == 0:
                    if self.data_simulation["inv_final"][y] == 0:
                        self.data_simulation["inv_monthly"].append(
                            ((self.data_simulation["inv_initial"][y]) / 2)
                            * (
                                self.data_simulation["inv_initial"][y]
                                / self.data_simulation["dem_adjust"][y]
                            )
                        )
                elif (
                    self.data_simulation["inv_final"][y] == 0
                    and self.data_simulation["inv_initial"][y] == 0
                ):
                    self.data_simulation["inv_monthly"].append(0)
                else:
                    self.data_simulation["inv_monthly"].append(
                        (
                            self.data_simulation["inv_initial"][y]
                            + self.data_simulation["inv_final"][y]
                        )
                        / 2
                    )
            # self.dfFinal = pd.DataFrame(self.data_simulation)
            # self.CreatePlot()
            print(self.data_simulation)
            return self.data_simulation
            # print(self.data_simulation)
        except Exception as err:
            print(self.data_simulation)
            print(str(err))


# A = inventory_system(100,200)
# A.Calc_probability_month()
# A.Calc_probability_delivery()
# A.Simulation()
