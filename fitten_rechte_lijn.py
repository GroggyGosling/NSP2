from lmfit import Model
import matplotlib.pyplot as plt
import numpy as np
from reader import ReadData

class FitLinearData():

    def __init__(self):
        self.pulse_height = np.array([0,3,8]) #mV
        self.theoretical_pulse_height = np.array([0,1,2]) #mV

    def linear_func(self, x,a,b):
        self.y = a*x + b

    def linear_fit(self):
        model = Model(self.y)
        self.result = model.fit(self.pulse_height,x = self.theoretical_pulse_height, a = 3.86, b = 0)
        print(self.result.fit_report())

    def plot_linear_fit(self):
        plt.plot(self.theoretical_pulse_height, self.result.best_fit)
        plt.show()

class FitQuadraticData():

    def __init__(self, pulseheight_CS, counts_CS, pulseheight_NA, counts_NA, pulseheight_background, counts_background):
        self.pulseheight_CS137 = pulseheight_CS
        self.counts_CS137 = counts_CS
        self.pulseheight_NA22 = pulseheight_NA
        self.counts_NA22 = counts_NA
        self.pulseheight_background = pulseheight_background
        self.counts_background = counts_background
        self.maximum_CS137_1 = []
        self.maximum_CS137_2 = []
        self.maximum_NA22_1 = []
        self.maximum_NA22_2 = []
        self.maximum_CS137_1_pulseheight = []
        self.maximum_CS137_2_pulseheight = []
        self.maximum_NA22_1_pulseheight = []
        self.maximum_NA22_2_pulseheight = []

    def quadratic_func(self, x, a, b, c, sigma):
        return a * np.exp(-(x - c) ** 2 / (2 * sigma ** 2)) + b
    
    def quadratic_fit(self):
        model = Model(self.quadratic_func)
        self.result_NA22_1 = model.fit(self.maximum_NA22_1, x = self.maximum_NA22_1_pulseheight, a = 20 , b = 1150, c = 136, sigma = 1)
        print(self.result_NA22_1.fit_report())
        plt.plot(self.maximum_NA22_1_pulseheight, self.result_NA22_1.best_fit)
        plt.show()

        self.result_NA22_2 = model.fit(self.maximum_NA22_2, x = self.maximum_NA22_2_pulseheight, a = 1 , b = 140, c = 328, sigma = 1)
        print(self.result_NA22_2.fit_report())
        plt.plot(self.maximum_NA22_2_pulseheight, self.result_NA22_2.best_fit)
        plt.show()

        self.result_CS137_1 = model.fit(self.maximum_CS137_1, x = self.maximum_CS137_1_pulseheight, a = 10 , b = 900, c = 55, sigma = 1)
        print(self.result_CS137_1.fit_report())
        plt.plot(self.maximum_CS137_1_pulseheight, self.result_CS137_1.best_fit)
        plt.show()

        self.result_CS137_2 = model.fit(self.maximum_CS137_2, x = self.maximum_CS137_2_pulseheight, a = 10 , b = 2250, c = 170, sigma = 1)
        print(self.result_CS137_2.fit_report())
        plt.plot(self.maximum_CS137_2_pulseheight, self.result_CS137_2.best_fit)
        plt.show()
    
    def select_maximum(self):
        i = 0
        for x in self.pulseheight_NA22:
            if x >= 120 and x <= 150:
                self.maximum_NA22_1.append(float(self.counts_NA22[i]))
                self.maximum_NA22_1_pulseheight.append(float(self.pulseheight_NA22[i]))
            if x >= 305 and x <= 350:
                self.maximum_NA22_2.append(float(self.counts_NA22[i]))
                self.maximum_NA22_2_pulseheight.append(float(self.pulseheight_NA22[i]))
            i += 1
        i = 0
        for x in self.pulseheight_CS137:
            if x >= 46 and x <= 61:
                self.maximum_CS137_1.append(float(self.counts_CS137[i]))
                self.maximum_CS137_1_pulseheight.append(float(self.pulseheight_CS137[i]))
            if x >= 143 and x <= 191:
                self.maximum_CS137_2.append(float(self.counts_CS137[i]))
                self.maximum_CS137_2_pulseheight.append(float(self.pulseheight_CS137[i]))
            i += 1
    
    def plot_data(self):
        plt.plot(self.pulseheight_NA22, self.counts_NA22)
        plt.show()
        plt.plot(self.pulseheight_CS137, self.counts_CS137)
        plt.show()
        plt.plot(self.pulseheight_background, self.counts_background)
        plt.show()
        


        
    
    

reader = ReadData()
a,b,c,d,e,f = reader.read_data()
finder = FitQuadraticData(a,b,c,d,e,f)

finder.select_maximum()
finder.quadratic_fit()

