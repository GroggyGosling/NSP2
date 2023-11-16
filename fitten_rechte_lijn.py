from lmfit import Model
import matplotlib.pyplot as plt
import numpy as np
from reader import ReadData

class FitLinearData():

    def __init__(self, c, c_err):
        self.pulse_height = [c[2], c[0], c[3], c[1]]
        self.pulse_height_err = [c_err[2], c_err[0], c_err[3], c_err[1]]
        self.theoretical_pulse_height = [135, 330, 511, 1275]

    def linear_func(self, x,a, b):
        return a*x + b

    def linear_fit(self):
        model = Model(self.linear_func)
        self.result = model.fit(self.theoretical_pulse_height, x = self.pulse_height, weights = self.pulse_height_err, a = 3.86, b = -90)
        print(self.result.fit_report()) 

        return self.result.params['a'].value, self.result.params['a'].stderr, self.result.params['b'].value, self.result.params['b'].stderr

    def plot_linear_fit(self):
        plt.scatter(self.pulse_height, self.theoretical_pulse_height)
        plt.plot(self.pulse_height, self.result.best_fit)
        plt.show()

class FitGaussianData():

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
        self.fit_c = []
        self.fit_c_error = []

    def gaussian_func(self, x, a, b, c, sigma):
        return a * np.exp(-(x - c) ** 2 / (2 * sigma ** 2)) + b
    
    def gaussian_fit(self):
        model = Model(self.gaussian_func)
        self.result_NA22_1 = model.fit(self.maximum_NA22_1, x = self.maximum_NA22_1_pulseheight, a = 20 , b = 1150, c = 136, sigma = 1)
        self.fit_c.append(self.result_NA22_1.params['c'].value)
        self.fit_c_error.append(self.result_NA22_1.params['c'].stderr/np.sqrt(np.sum(self.maximum_NA22_1)))
        print(self.result_NA22_1.fit_report())

        self.result_NA22_2 = model.fit(self.maximum_NA22_2, x = self.maximum_NA22_2_pulseheight, a = 1 , b = 140, c = 328, sigma = 1)
        self.fit_c.append(self.result_NA22_2.params['c'].value)
        self.fit_c_error.append(self.result_NA22_2.params['c'].stderr/np.sqrt(np.sum(self.maximum_NA22_2)))
        print(self.result_NA22_2.fit_report())

        self.result_CS137_1 = model.fit(self.maximum_CS137_1, x = self.maximum_CS137_1_pulseheight, a = 10 , b = 900, c = 55, sigma = 1)
        self.fit_c.append(self.result_CS137_1.params['c'].value)
        self.fit_c_error.append(self.result_CS137_1.params['c'].stderr/np.sqrt(np.sum(self.maximum_CS137_1)))
        print(self.result_CS137_1.fit_report())

        self.result_CS137_2 = model.fit(self.maximum_CS137_2, x = self.maximum_CS137_2_pulseheight, a = 10 , b = 2250, c = 170, sigma = 1)
        self.fit_c.append(self.result_CS137_2.params['c'].value)
        self.fit_c_error.append(self.result_CS137_2.params['c'].stderr/np.sqrt(np.sum(self.maximum_CS137_2)))
        print(self.result_CS137_2.fit_report())
    
        return self.fit_c, self.fit_c_error
    
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
gaussian = FitGaussianData(a,b,c,d,e,f)

gaussian.select_maximum()
c, c_err = gaussian.gaussian_fit()

linear = FitLinearData(c, c_err)
print(linear.linear_fit())
linear.plot_linear_fit()


