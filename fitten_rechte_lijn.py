from lmfit import Model
import matplotlib.pyplot as plt
import numpy as np
from reader import ReadData
import csv

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

    def __init__(self):
        self.file_NA22 = open('NSP2\spectrum_NA22.csv', 'r')
        self.file_CS137 = open('NSP2\spectrum_CS137.csv', 'r')
        self.file_background = open('NSP2\spectrum_background.csv', 'r')

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

        self.fit_c = []
        self.fit_c_error = []

    def select_maximum(self):
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
        self.result_NA22_1 = model.fit(self.maximum_NA22_1, x = self.maximum_NA22_1_pulseheight, a = 20 , b = 1150, c = 136, sigma = 1)
        self.fit_c.append(self.result_NA22_1.params['c'].value)
        self.fit_c_error.append(self.result_NA22_1.params['c'].stderr/np.sqrt(np.sum(self.maximum_NA22_1)))

        self.result_NA22_2 = model.fit(self.maximum_NA22_2, x = self.maximum_NA22_2_pulseheight, a = 1 , b = 140, c = 328, sigma = 1)
        self.fit_c.append(self.result_NA22_2.params['c'].value)
        self.fit_c_error.append(self.result_NA22_2.params['c'].stderr/np.sqrt(np.sum(self.maximum_NA22_2)))

        self.result_CS137_1 = model.fit(self.maximum_CS137_1, x = self.maximum_CS137_1_pulseheight, a = 10 , b = 900, c = 55, sigma = 1)
        self.fit_c.append(self.result_CS137_1.params['c'].value)
        self.fit_c_error.append(self.result_CS137_1.params['c'].stderr/np.sqrt(np.sum(self.maximum_CS137_1)))

        self.result_CS137_2 = model.fit(self.maximum_CS137_2, x = self.maximum_CS137_2_pulseheight, a = 10 , b = 2250, c = 170, sigma = 1)
        self.fit_c.append(self.result_CS137_2.params['c'].value)
        self.fit_c_error.append(self.result_CS137_2.params['c'].stderr/np.sqrt(np.sum(self.maximum_CS137_2)))

        print(self.result_NA22_1.fit_report())
        print(self.result_NA22_2.fit_report())
        print(self.result_CS137_1.fit_report())
        print(self.result_CS137_2.fit_report())
    
        return self.fit_c, self.fit_c_error
    
    def plot_data(self):
        plt.plot(self.pulseheight, self.counts_NA22)
        plt.show()
        plt.plot(self.pulseheight, self.counts_CS137)
        plt.show()
        plt.plot(self.pulseheight, self.counts_background)
        plt.show()

class compton():

    def __init__(self):
        self.file_compton3 = open('edge_30_11.csv', 'r')
        self.file_compton2 = open('background_20min_30_11.csv', 'r')
        self.file_compton1 = open('1h_30_11.csv', 'r')
        self.pulseheight_compton1 = []
        self.counts_compton1 = []
        
        self.pulseheight_compton2 = []
        self.counts_compton2 = []

        self.pulseheight_compton3 = []
        self.counts_compton3 = []


        csvreader = csv.reader(self.file_compton1)
        for row in csvreader:
            self.pulseheight_compton1.append(int(float(row[0])))
            self.counts_compton1.append(int(float(row[1])))
        csvreader = csv.reader(self.file_compton2)
        for row in csvreader:
            self.pulseheight_compton2.append(int(float(row[0])))
            self.counts_compton2.append(3 * int(float(row[1])))
        # csvreader = csv.reader(self.file_compton3)
        # for row in csvreader:
        #     self.pulseheight_compton3.append(int(float(row[0])))
        #     self.counts_compton3.append(6 * int(float(row[1])))

        # self.counts_compton1_half = []
        # self.counts_compton2_half = []
        # self.pulseheight_compton1_half = []
        # for i in range(0, 100, 2):
        #     self.counts_compton1_half.append(self.counts_compton1[i] + self.counts_compton1[i+1])
        #     self.counts_compton2_half.append(self.counts_compton2[i] + self.counts_compton2[i+1])
        #     self.pulseheight_compton1_half.append(self.pulseheight_compton1[i])
        self.background = []
        for i in self.pulseheight_compton1:
            self.background.append(np.e**(-0.00810236 * i + 6.96630832))

        subtracted = []
        for i,j in zip(self.background, self.counts_compton1):
            subtracted.append(j - i)
        
        # subtracted2 = []
        # for i,j in zip(self.counts_compton2, self.counts_compton3):
        #     subtracted2.append(j - i)
        
        plt.plot(self.pulseheight_compton1, self.counts_compton1, label = 'met object')
        # plt.plot(self.pulseheight_compton3, self.counts_compton3, label = 'edge')
        plt.plot(self.pulseheight_compton2, self.background, label = 'zonder object')
        plt.plot(self.pulseheight_compton1, subtracted, label = 'subtracted')
        # plt.plot(self.pulseheight_compton1, subtracted2, label = 'subtracted2')
        plt.legend()
        plt.show()

class lineair_achtergond():
    def __init__(self):
        
        self.file_compton4 = open('background_20min_30_11.csv', 'r')
        self.file_compton5 = open('1h_30_11.csv', 'r')

        self.achtergrond_counts = []
        self.achtergrond_pulseheight = []

        self.pulseheight_compton4 = []
        self.counts_compton4 = []

        self.pulseheight_compton5 = []
        self.counts_compton5 = []

        self.counts = []
        self.pulseheight = []

        csvreader = csv.reader(self.file_compton4)
        for row in csvreader:
            self.pulseheight_compton4.append(int(float(row[0])))
            self.counts_compton4.append(3 * int(float(row[1])))

        csvreader = csv.reader(self.file_compton5)
        for row in csvreader:
            self.pulseheight_compton5.append(int(float(row[0])))
            self.counts_compton5.append(int(float(row[1])))

    def select_maximum(self):
        i = 0
        
        for x in self.pulseheight_compton4:

            if x >= 100 and x <= 160:
                self.achtergrond_pulseheight.append(float(self.pulseheight_compton4[i]))
                self.achtergrond_counts.append(float(self.counts_compton4[i]))
            i += 1

        i = 0
        for x in self.pulseheight_compton4:
            if x >= 100 and x <= 160:
                self.pulseheight.append(float(self.pulseheight_compton4[i]))
                self.counts.append(float(self.counts_compton4[i]))
            i += 1

    def linear_func(self, x, a, b):
        return np.e**(-a*x + b)

    def linear_fit(self):
        model = Model(self.linear_func)
        self.result = model.fit(self.achtergrond_counts, x = self.achtergrond_pulseheight, a = -0.33, b =100)

    def plotten(self):
        print(self.result.fit_report())
        plt.plot(self.achtergrond_pulseheight, self.result.best_fit,)
        plt.plot(self.pulseheight, self.counts)
        plt.show()

test = lineair_achtergond()
test.select_maximum()
test.linear_fit()
test.plotten()
# test.plotten()



    # def plot_data(self):
    #     plt.plot(self.pulseheight_compton1, self.counts_compton1)
    #     plt.show()
    
    # def gaussian_func(self, x, a, b, c, sigma):
    #     return a * np.exp(-(x - c) ** 2 / (2 * sigma ** 2)) + b
    
    # def select_maximum(self):
    #     i = 0
    #     self.maximum_compton1 = []
    #     self.maximum_compton1_pulseheight = []
    #     for x in self.pulseheight_compton1:
    #         if x >= 158 and x <= 193:
    #             self.maximum_compton1.append(float(self.counts_compton1[i]))
    #             self.maximum_compton1_pulseheight.append(float(self.pulseheight_compton1[i]))
    #         i += 1

    # def gaussian_fit(self):
    #     model = Model(self.gaussian_func)
    #     self.result_compton1 = model.fit(self.maximum_compton1, x = self.maximum_compton1_pulseheight, a = 10 , b = 400, c = 175, sigma = 1)
    #     print(self.result_compton1.fit_report())
    #     plt.plot(self.maximum_compton1_pulseheight, self.result_compton1.best_fit)
    #     plt.show()
    


        
test = compton()
# test.plot_data()
# test.select_maximum()
# test.gaussian_fit()


    

# reader = ReadData()
# a,b,c,d,e,f = reader.read_data()
# gaussian = FitGaussianData(a,b,c,d,e,f)

# gaussian.select_maximum()
# c, c_err = gaussian.gaussian_fit()
# gaussian.plot_data()

# linear = FitLinearData(c, c_err)
# print(linear.linear_fit())
# linear.plot_linear_fit()




