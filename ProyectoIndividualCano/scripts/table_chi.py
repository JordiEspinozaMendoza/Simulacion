import numpy as np
import pandas as pd


class Table_Chi:
    alpha = 0.0
    nGroups = 0.0
    dataFrame = None
    data_table = {0.001:
                  {1: 10.8274, 2: 13.815, 3: 16.266, 4: 18.4662, 5: 20.5147, 6: 22.4575, 7: 24.3213, 8: 26.1239, 9: 27.8767, 10: 29.5879, 11: 31.2635, 12: 32.9092, 13: 34.5274, 14: 36.1239, 15: 37.6978, 16: 39.2518, 17: 40.7911, 18: 42.3119, 19: 43.8194, 20: 45.3142, 21: 46.7963, 22: 48.2676, 23: 49.7276, 24: 51.179, 25: 52.6187, 26: 54.0511, 27: 55.4751, 28: 56.8918, 29: 58.3006}, 0.0025: {1: 9.1404, 2: 11.9827, 3: 14.3202, 4: 16.4238, 5: 18.3854, 6: 20.2491, 7: 22.0402, 8: 23.7742, 9: 25.4625, 10: 27.1119, 11: 28.7291, 12: 30.3182, 13: 31.883, 14: 33.4262, 15: 34.9494, 16: 36.4555, 17: 37.9462, 18: 39.422, 19: 40.8847, 20: 42.3358, 21: 43.7749, 22: 45.2041, 23: 46.6231, 24: 48.0336, 25: 49.4351, 26: 50.8291, 27: 52.2152, 28: 53.5939, 29: 54.9662}, 0.005: {1: 7.8794, 2: 10.5965, 3: 12.8381, 4: 14.8602, 5: 16.7496, 6: 18.5475, 7: 20.2777, 8: 21.9549, 9: 23.5893, 10: 25.1881, 11: 26.7569, 12: 28.2997, 13: 29.8193, 14: 31.3194, 15: 32.8015, 16: 34.2671, 17: 35.7184, 18: 37.1564, 19: 38.5821, 20: 39.9969, 21: 41.4009, 22: 42.7957, 23: 44.1814, 24: 45.5584, 25: 46.928, 26: 48.2898, 27: 49.645, 28: 50.9936, 29: 52.3355}, 0.01: {1: 6.6349, 2: 9.2104, 3: 11.3449, 4: 13.2767, 5: 15.0863, 6: 16.8119, 7: 18.4753, 8: 20.0902, 9: 21.666, 10: 23.2093, 11: 24.725, 12: 26.217, 13: 27.6882, 14: 29.1412, 15: 30.578, 16: 31.9999, 17: 33.4087, 18: 34.8052, 19: 36.1908, 20: 37.5663, 21: 38.9322, 22: 40.2894, 23: 41.6383, 24: 42.9798, 25: 44.314, 26: 45.6416, 27: 46.9628, 28: 48.2782, 29: 49.5878}, 0.025: {1: 5.0239,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       2: 7.3778, 3: 9.3484, 4: 11.1433, 5: 12.8325, 6: 14.4494, 7: 16.0128, 8: 17.5345, 9: 19.0228, 10: 20.4832, 11: 21.92, 12: 23.3367, 13: 24.7356, 14: 26.1189, 15: 27.4884, 16: 28.8453, 17: 30.191, 18: 31.5264, 19: 32.8523, 20: 34.1696, 21: 35.4789, 22: 36.7807, 23: 38.0756, 24: 39.3641, 25: 40.6465, 26: 41.9231, 27: 43.1945, 28: 44.4608, 29: 45.7223}, 0.05: {1: 3.8415, 2: 5.9915, 3: 7.8147, 4: 9.4877, 5: 11.0705, 6: 12.5916, 7: 14.0671, 8: 15.5073, 9: 16.919, 10: 18.307, 11: 19.6752, 12: 21.0261, 13: 22.362, 14: 23.6848, 15: 24.9958, 16: 26.2962, 17: 27.5871, 18: 28.8693, 19: 30.1435, 20: 31.4104, 21: 32.6706, 22: 33.9245, 23: 35.1725, 24: 36.415, 25: 37.6525, 26: 38.8851, 27: 40.1133, 28: 41.3372, 29: 42.5569}, 0.1: {1: 2.7055, 2: 4.6052, 3: 6.2514, 4: 7.7794, 5: 9.2363, 6: 10.6446, 7: 12.017, 8: 13.3616, 9: 14.6837, 10: 15.9872, 11: 17.275, 12: 18.5493, 13: 19.8119, 14: 21.0641, 15: 22.3071, 16: 23.5418, 17: 24.769, 18: 25.9894, 19: 27.2036, 20: 28.412, 21: 29.6151, 22: 30.8133, 23: 32.0069, 24: 33.1962, 25: 34.3816, 26: 35.5632, 27: 36.7412, 28: 37.9159, 29: 39.0875}, 0.15: {1: 2.0722, 2: 3.7942, 3: 5.317, 4: 6.7449, 5: 8.1152, 6: 9.4461, 7: 10.7479, 8: 12.0271, 9: 13.288, 10: 14.5339, 11: 15.7671, 12: 16.9893, 13: 18.202, 14: 19.4062, 15: 20.603, 16: 21.7931, 17: 22.977, 18: 24.1555, 19: 25.3289, 20: 26.4976, 21: 27.662, 22: 28.8224, 23: 29.9792, 24: 31.1325, 25: 32.2825, 26: 33.4295, 27: 34.5736, 28: 35.715, 29: 36.8538}, 0.2: {1: 1.6424, 2: 3.2189, 3: 4.6416, 4: 5.9886, 5: 7.2893, 6: 8.5581, 7: 9.8032, 8: 11.0301, 9: 12.2421, 10: 13.442, 11: 14.6314, 12: 15.812, 13: 16.9848, 14: 18.1508, 15: 19.3107, 16: 20.4651, 17: 21.6146, 18: 22.7595, 19: 23.9004, 20: 25.0375, 21: 26.1711, 22: 27.3015, 23: 28.4288, 24: 29.5533, 25: 30.6752, 26: 31.7946, 27: 32.9117, 28: 34.0266, 29: 35.1394}, 0.25: {1: 1.3233, 2: 2.7726, 3: 4.1083, 4: 5.3853, 5: 6.6257, 6: 7.8408, 7: 9.0371, 8: 10.2189, 9: 11.3887, 10: 12.5489, 11: 13.7007, 12: 14.8454, 13: 15.9839, 14: 17.1169, 15: 18.2451, 16: 19.3689, 17: 20.4887, 18: 21.6049, 19: 22.7178, 20: 23.8277, 21: 24.9348, 22: 26.0393, 23: 27.1413, 24: 28.2412, 25: 29.3388, 26: 30.4346, 27: 31.5284, 28: 32.6205, 29: 33.7109}, 0.3: {1: 1.0742, 2: 2.4079, 3: 3.6649, 4: 4.8784, 5: 6.0644, 6: 7.2311, 7: 8.3834, 8: 9.5245, 9: 10.6564, 10: 11.7807, 11: 12.8987, 12: 14.0111, 13: 15.1187, 14: 16.2221, 15: 17.3217, 16: 18.4179, 17: 19.511, 18: 20.6014, 19: 21.6891, 20: 22.7745, 21: 23.8578, 22: 24.939, 23: 26.0184, 24: 27.096, 25: 28.1719, 26: 29.2463, 27: 30.3193, 28: 31.3909, 29: 32.4612}, 0.35: {1: 0.8735, 2: 2.0996, 3: 3.2831, 4: 4.4377, 5: 5.5731, 6: 6.6948, 7: 7.8061, 8: 8.9094, 9: 10.006, 10: 11.0971, 11: 12.1836, 12: 13.2661, 13: 14.3451, 14: 15.4209, 15: 16.494, 16: 17.5646, 17: 18.633, 18: 19.6993, 19: 20.7638, 20: 21.8265, 21: 22.8876,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  22: 23.9473, 23: 25.0055, 24: 26.0625, 25: 27.1183, 26: 28.173, 27: 29.2266, 28: 30.2791, 29: 31.3308}, 0.4: {1: 0.7083, 2: 1.8326, 3: 2.9462, 4: 4.0446, 5: 5.1319, 6: 6.2108, 7: 7.2832, 8: 8.3505, 9: 9.4136, 10: 10.4732, 11: 11.5298, 12: 12.5838, 13: 13.6356, 14: 14.6853, 15: 15.7332, 16: 16.7795, 17: 17.8244, 18: 18.8679, 19: 19.9102, 20: 20.9514, 21: 21.9915, 22: 23.0307, 23: 24.0689, 24: 25.1064, 25: 26.143, 26: 27.1789, 27: 28.2141, 28: 29.2486, 29: 30.2825}, 0.45: {1: 0.5707, 2: 1.597, 3: 2.643, 4: 3.6871, 5: 4.7278, 6: 5.7652, 7: 6.8, 8: 7.8325, 9: 8.8632, 10: 9.8922, 11: 10.9199, 12: 11.9463, 13: 12.9717, 14: 13.9961, 15: 15.0197, 16: 16.0425, 17: 17.0646, 18: 18.086, 19: 19.1069, 20: 20.1272, 21: 21.147, 22: 22.1663, 23: 23.1852, 24: 24.2037, 25: 25.2218, 26: 26.2395, 27: 27.2569, 28: 28.274, 29: 29.2908}, 0.5: {1: 0.4549, 2: 1.3863, 3: 2.366, 4: 3.3567, 5: 4.3515, 6: 5.3481, 7: 6.3458, 8: 7.3441, 9: 8.3428, 10: 9.3418, 11: 10.341, 12: 11.3403, 13: 12.3398, 14: 13.3393, 15: 14.3389, 16: 15.3385, 17: 16.3382, 18: 17.3379, 19: 18.3376, 20: 19.3374, 21: 20.3372, 22: 21.337, 23: 22.3369, 24: 23.3367, 25: 24.3366, 26: 25.3365, 27: 26.3363, 28: 27.3362, 29: 28.3361}}

    def __init__(self, alpha, nGroups):
        self.alpha = alpha
        self.nGroups = nGroups-1

    def getTable(self):
        self.dataFrame = pd.DataFrame(self.data_table)

    def foundChi(self):
        temp = self.dataFrame[self.alpha].tolist()
        if self.nGroups <= 0:
            return temp[0]
        else:
            return temp[self.nGroups-1]


# table = Table_Chi(0.0010, 5)
# table.getTable()
# table.foundChi()
