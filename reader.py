from lmfit import model
import numpy
import matplotlib.pyplot as plt
import csv

class ReadData():
    
    def __init__(self):
        self.pulseheight_NA22 = []
        self.counts_NA22 = []
        self.pulseheight_CS137 = []
        self.counts_CS137 = []
        self.pulseheight_background = []
        self.counts_background = []

        self.file_NA22 = open('NSP2\spectrum_NA22.csv', 'r')
        self.file_CS137 = open('NSP2\spectrum_CS137.csv', 'r')
        self.file_background = open('NSP2\spectrum_background.csv', 'r')

    def read_data(self):
        csvreader = csv.reader(self.file_CS137)

        for row in csvreader:
            self.pulseheight_CS137.append(int(float(row[0])))
            self.counts_CS137.append(int(float(row[1])))

        csvreader = csv.reader(self.file_NA22)

        for row in csvreader:
            self.pulseheight_NA22.append(int(float(row[0])))
            self.counts_NA22.append(int(float(row[1])))
        
        csvreader = csv.reader(self.file_background)

        for row in csvreader:
            self.pulseheight_background.append(int(float(row[0])))
            self.counts_background.append(int(float(row[1])))

        
        return self.pulseheight_CS137, self.counts_CS137, self.pulseheight_NA22, self.counts_NA22, self.pulseheight_background, self.counts_background
