import math
import numpy as np

def err_foton_energy(err_theta,theta,E_f):
    m = 9.109*10**-31
    c = 3*10**8
    theta_rad = np.deg2rad(theta)
    err_theta = np.deg2rad(err_theta)
    a = E_f
    b  = (E_f)/(m*(c**2))

    err_foton_energy = -(a*b*math.sin(theta_rad))/((-b*math.cos(theta_rad) + b + 1)**2)*err_theta
    return err_foton_energy

def err_mili_voltage(err_foton_energy):
    return ((err_foton_energy/(1.602*10**-16))/3.97)

test = err_foton_energy(90,35.0,662*(1.602*10**-16))
yes = err_mili_voltage(test)
print(yes)