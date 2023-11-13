from lmfit import model
import numpy
import matplotlib.pyplot as plt
import csv
class Radiatonfit():
    
    def __init__(self):
        self.pulseheight_NA22 = []
        self.counts_NA22 = []
        self.pulseheight_CS137 = []
        self.counts_CS137 = []

        self.file_NA22 = open('NSP2\spectrum_NA22.csv', 'r')
        self.file_CS137 = open('NSP2\spectrum_CS137.csv', 'r')

    def plot_data(self):
        csvreader = csv.reader(self.file_CS137)

        for row in csvreader:
            self.pulseheight_CS137.append(int(float(row[0])))
            self.counts_CS137.append(int(float(row[1])))

        plt.plot(self.pulseheight_CS137, self.counts_CS137)
        plt.show()

        csvreader = csv.reader(self.file_NA22)

        for row in csvreader:
            self.pulseheight_NA22.append(int(float(row[0])))
            self.counts_NA22.append(int(float(row[1])))

        plt.plot(self.pulseheight_NA22, self.counts_NA22)
        plt.show()

fit = Radiatonfit()
fit.plot_data()