import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, h, hbar, alpha, c, m_e

class CrossSection():

    def __init__(self): 
        self.f = (hbar * alpha / m_e / c)**2 / 2
        self.l_in = np.array([])
        self.l_out = np.array([])
        self.theta_list = np.array(np.array[])
        
    def compute_cross_section(self):
         self.l_out = self.l_in + h / m_e / c * (1 - np.cos(self.theta))
         
         self.P = self.l_out/self.l_in
         self.dsigma_dOmega = self.f * self.P**2 * (self.P + 1/self.P - np.sin(self.theta)**2)


    def plot_cross_section(self):

        plt.plot(self.theta_list,self.dsigma_dOmega)
        plt.show()
