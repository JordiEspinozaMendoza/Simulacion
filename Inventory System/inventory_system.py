import pandas as pd


class inventory_system:
    month_demand = {
        "qty": [35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
        "prob": [0.010, 0.015, 0.020, 0.020, 0.022, 0.023, 0.025, 0.027, 0.028, 0.029, 0.035,  0.045, 0.060, 0.065, 0.070, 0.080, 0.075, 0.070, 0.065, 0.060, 0.050, 0.040, 0.030, 0.016, 0.015, 0.005],
    }
    prob_delivery_months = {
        "months": [1, 2, 3],
        "prob": [0.30, 0.40, 0.30]
    }
    seasonal_factors = {
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "factor": [1.90, 1.00, 0.90, 0.80, 0.80, 0.70, 0.80, 0.90, 1.00, 1.20, 1.30, 1.40]
    }
    initial_values = {
        "inventory_initial": 150,
        "order_cost": 50,
        "inventory_cost": 26,
        "cost_absences": 25,
        "days_year": 260,
        "month_demand": month_demand,
        "prob_delivery_months": prob_delivery_months,
        "seasonal_factors": seasonal_factors
    }

    def calc_probability_delivery(self):
        cumulative_probability_delivery = {
            "months": [],
            "L_inf": [],
            "L_sup": []
        }
        for i in range(0, len(self.initial_values["prob_delivery_months"]["months"])):
            cumulative_probability_delivery["months"].append(
                self.initial_values["prob_delivery_months"]["months"][i])
            if i == 0:
                cumulative_probability_delivery["L_sup"].append(
                    self.initial_values["prob_delivery_months"]["prob"][i]
                )
                cumulative_probability_delivery["L_inf"].append(0)
            else:
                cumulative_probability_delivery["L_sup"].append(
                    cumulative_probability_delivery["L_sup"][i-1] +
                    self.initial_values["prob_delivery_months"]["prob"][i]
                )
                cumulative_probability_delivery["L_inf"].append(
                    cumulative_probability_delivery["L_sup"][i-1]
                )
        df = pd.DataFrame(cumulative_probability_delivery)
        print(df)

    def calc_probability_month(self):
        cumulative_probability = {
            "qty": [],
            "L_inf": [],
            "L_sup": []
        }
        for i in range(0, len(self.initial_values["month_demand"]["qty"])):
            cumulative_probability["qty"].append(
                self.initial_values["month_demand"]["qty"][i])
            if i == 0:
                cumulative_probability["L_sup"].append(
                    self.initial_values["month_demand"]["prob"][i])
                cumulative_probability["L_inf"].append(0)
            else:
                cumulative_probability["L_sup"].append(
                    cumulative_probability["L_sup"][i-1] +
                    self.initial_values["month_demand"]["prob"][i])
                cumulative_probability["L_inf"].append(
                    cumulative_probability["L_sup"][i-1])
        # df = pd.DataFrame(cumulative_probability)
        # print(df)


A = inventory_system()
A.calc_probability_delivery()
