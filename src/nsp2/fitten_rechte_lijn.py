from lmfit import Model
import matplotlib.pyplot as plt
import numpy as np
import csv

from nsp2.smoothing import savitzky_golay

class FitLinearData():

    def __init__(self, c, c_err):
        self.pulse_height = [c[2], c[0], c[3], c[1]]
        self.pulse_height_err = [c_err[2], c_err[0], c_err[3], c_err[1]]
        self.theoretical_pulse_height = [180, 511, 662, 1275]

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

    def __init__(self, subtract):
        self.file_NA22 = open('data\calibratie\spectrum_NA22.csv', 'r')
        self.file_CS137 = open('data\calibratie\spectrum_CS137.csv', 'r')
        self.file_background = open('data\calibratie\spectrum_background.csv', 'r')

        self.counts_CS137 = []
        self.counts_NA22 = []
        self.counts_background = []
        self.pulseheight = []

        csvreader = csv.reader(self.file_CS137)
        for row in csvreader:
            self.pulseheight.append(int(float(row[0])))
            self.counts_CS137.append(int(float(row[1])))

        csvreader = csv.reader(self.file_NA22)
        for row in csvreader:
            self.counts_NA22.append(int(float(row[1])))
        
        csvreader = csv.reader(self.file_background)
        for row in csvreader:
            self.counts_background.append(int(float(row[1])))
       
        self.maximum_CS137_1 = []
        self.maximum_CS137_2 = []
        self.maximum_NA22_1 = []
        self.maximum_NA22_2 = []

        self.maximum_CS137_1_pulseheight = []
        self.maximum_CS137_2_pulseheight = []
        self.maximum_NA22_1_pulseheight = []
        self.maximum_NA22_2_pulseheight = [] 
        self.subtracted = subtract
        self.subtract_max = []
        self.subtract_x = []

        self.fit_c = []
        self.fit_c_error = []

    def select_maximum(self):
        i = 0
        for x in self.pulseheight:
            if x >= 90 and x <= 180:
                self.subtract_max.append(float(self.subtracted[i]))
                self.subtract_x.append(float(self.pulseheight[i]))
            i += 1

        i = 0
        for x in self.pulseheight:
            if x >= 120 and x <= 150:
                self.maximum_NA22_1.append(float(self.counts_NA22[i]))
                self.maximum_NA22_1_pulseheight.append(float(self.pulseheight[i]))

            if x >= 305 and x <= 350:
                self.maximum_NA22_2.append(float(self.counts_NA22[i]))
                self.maximum_NA22_2_pulseheight.append(float(self.pulseheight[i]))

            i += 1

        i = 0
        for x in self.pulseheight:
            if x >= 46 and x <= 61:
                self.maximum_CS137_1.append(float(self.counts_CS137[i]))
                self.maximum_CS137_1_pulseheight.append(float(self.pulseheight[i]))

            if x >= 143 and x <= 191:
                self.maximum_CS137_2.append(float(self.counts_CS137[i]))
                self.maximum_CS137_2_pulseheight.append(float(self.pulseheight[i]))

            i += 1

    def gaussian_func(self, x, a, b, c, sigma):
        return a * np.exp(-(x - c) ** 2 / (2 * sigma ** 2)) + b
    
    def gaussian_fit(self):
        model = Model(self.gaussian_func)

        self.result_subtract = model.fit(self.subtract_max, x = self.subtract_x, a = 2, b = 100, c = 136, sigma = 1)
        print(self.result_subtract.fit_report())
        # self.result_NA22_1 = model.fit(self.maximum_NA22_1, x = self.maximum_NA22_1_pulseheight, a = 20 , b = 1150, c = 136, sigma = 1)
        # self.fit_c.append(self.result_NA22_1.params['c'].value)
        # self.fit_c_error.append(self.result_NA22_1.params['c'].stderr/np.sqrt(np.sum(self.maximum_NA22_1)))

        # self.result_NA22_2 = model.fit(self.maximum_NA22_2, x = self.maximum_NA22_2_pulseheight, a = 1 , b = 140, c = 328, sigma = 1)
        # self.fit_c.append(self.result_NA22_2.params['c'].value)
        # self.fit_c_error.append(self.result_NA22_2.params['c'].stderr/np.sqrt(np.sum(self.maximum_NA22_2)))

        # self.result_CS137_1 = model.fit(self.maximum_CS137_1, x = self.maximum_CS137_1_pulseheight, a = 10 , b = 900, c = 55, sigma = 1)
        # self.fit_c.append(self.result_CS137_1.params['c'].value)
        # self.fit_c_error.append(self.result_CS137_1.params['c'].stderr/np.sqrt(np.sum(self.maximum_CS137_1)))

        # self.result_CS137_2 = model.fit(self.maximum_CS137_2, x = self.maximum_CS137_2_pulseheight, a = 10 , b = 2250, c = 170, sigma = 1)
        # self.fit_c.append(self.result_CS137_2.params['c'].value)
        # self.fit_c_error.append(self.result_CS137_2.params['c'].stderr/np.sqrt(np.sum(self.maximum_CS137_2)))

        # print(self.result_NA22_1.fit_report())
        # print(self.result_NA22_2.fit_report())
        # print(self.result_CS137_1.fit_report())
        # print(self.result_CS137_2.fit_report())
    
        # return self.fit_c, self.fit_c_error
    
    def plot_data(self):
        # plt.plot(self.pulseheight, self.counts_NA22)
        # plt.show()
        # plt.plot(self.pulseheight, self.counts_CS137)
        # plt.show()
        # plt.plot(self.pulseheight, self.counts_background)
        # plt.show()
        plt.plot(self.subtract_x, self.subtract_max)
        plt.plot(self.subtract_x, self.result_subtract.best_fit)
        plt.show()

class compton():

    def __init__(self):
        # self.file_background_20 = open('data\\04_12\\background_20m_45d_4_12.csv', 'r')
        # self.file_1h = open('data\\04_12\\1h_45d_4_12.csv', 'r')
        self.file_background_20 = open('data\\30_11\\background_20min_30_11.csv', 'r')
        self.file_1h = open('data\\30_11\\1h_30_11.csv', 'r')

        self.pulseheight = []

        self.counts_1h = []
        self.counts_background_20 = []

        csvreader = csv.reader(self.file_1h)
        for row in csvreader:
            self.pulseheight.append(int(float(row[0])))
            self.counts_1h.append(int(float(row[1])))

        csvreader = csv.reader(self.file_background_20)
        for row in csvreader:
            self.counts_background_20.append(3 * int(float(row[1])))

    def smoothing(self):
        self.x = np.array(self.pulseheight)
        self.y = savitzky_golay(np.array(self.counts_background_20),window_size= 51, order=10) 
        

    def approx_background(self):
        self.background = []
        for i in self.pulseheight:
            self.background.append(np.e**(-0.00810236 * i + 6.96630832))

    def subtract(self): 
        self.subtracted = []
        for i,j in zip(self.counts_1h, self.y):
            self.subtracted.append(i - j)
        return self.subtracted
        
    def plot(self):
        plt.plot(self.x, self.y)
        plt.plot(self.pulseheight, self.counts_1h, label = 'met object')
        plt.plot(self.pulseheight, self.counts_background_20, label = 'zonder object')
        plt.plot(self.pulseheight, self.subtracted, label = 'subtracted')
        plt.legend()
        plt.show()

class lineair_achtergond():
    def __init__(self):
    
        self.file_background_20 = open('data\\30_11\\background_20min_30_11.csv', 'r')
        self.file_1h = open('data\\30_11\\1h_30_11.csv', 'r')

        self.pulseheight = []
        self.counts_background_20 = []
        self.counts_1h = []

        self.achtergrond_counts = []
        self.achtergrond_pulseheight = []
        self.counts = []
        self.pulseheight = []

        csvreader = csv.reader(self.file_background_20)
        for row in csvreader:
            self.pulseheight.append(int(float(row[0])))
            self.counts_background_20.append(3 * int(float(row[1])))

        csvreader = csv.reader(self.file_1h)
        for row in csvreader:
            self.counts_1h.append(int(float(row[1])))

    def select_maximum(self):
        i = 0
        for x in self.pulseheight:
            if x >= 100 and x <= 160:
                self.achtergrond_pulseheight.append(float(self.pulseheight[i]))
                self.achtergrond_counts.append(float(self.counts_background_20[i]))
            i += 1

        i = 0
        for x in self.pulseheight:
            if x >= 100 and x <= 160:
                self.pulseheight.append(float(self.pulseheight[i]))
                self.counts.append(float(self.counts_background_20[i]))
            i += 1

    def linear_func(self, x, a, b):
        return np.e**(-a*x + b)

    def linear_fit(self):
        model = Model(self.linear_func)
        self.result = model.fit(self.achtergrond_counts, x = self.achtergrond_pulseheight, a = -0.33, b =100)
        print(self.result.fit_report())

    def plotten(self):
        plt.plot(self.achtergrond_pulseheight, self.result.best_fit,)
        plt.plot(self.pulseheight, self.counts)
        plt.show()

    

comptontest = compton()
comptontest.smoothing()
subtract = comptontest.subtract()
comptontest.plot()

fit = FitGaussianData(subtract)
fit.select_maximum()
fit.gaussian_fit()
fit.plot_data()




