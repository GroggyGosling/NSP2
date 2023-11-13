from lmfit import Model
import matplotlib.pyplot as plt
import numpy as np

pulse_height = np.array([0,3,8]) #mV
theoretical__pulse_height = np.array([0,1,2]) #mV


def func(x,a,b):
    y = np.exp(a*x) + b
    return y 
model = Model(func)



result = model.fit(pulse_height,x = theoretical__pulse_height, a = 3.86, b = 0)

plt.plot(theoretical__pulse_height, result.best_fit)

plt.show()

print(result.fit_report())