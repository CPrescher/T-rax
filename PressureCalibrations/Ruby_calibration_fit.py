import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


Mao_data = np.loadtxt('Model/Ruby/Mao_et_al_1986_Cu.txt', delimiter='\t')
Zou_data = np.loadtxt('Model/Ruby/Zou_et_al_1982_Ag.txt', delimiter='\t')

Mao_P = Mao_data.T[0]
Mao_delta_wavelength = Mao_data.T[1]

Zou_P = Zou_data.T[0]
Zou_delta_wavelenth = Zou_data.T[1]

all_data_P = np.array(list(Mao_P) + list(Zou_P)) / 10
all_data_delta_wavelength = np.array(list(Mao_delta_wavelength) + list(Zou_delta_wavelenth)) / 10

plt.scatter(all_data_delta_wavelength, all_data_P, s=20)


##fitting both parameters

lambda0 = 694


def fit_function_both(x, A, B):
    return float(A) / B * ((1 + (x / lambda0)) ** B - 1)


par, cov = curve_fit(fit_function_both, all_data_delta_wavelength, all_data_P, p0=[1904, 7.665])
print par
print np.sqrt(cov.diagonal())

own_fit_both_x = np.linspace(0, max(all_data_delta_wavelength) * 1.05, 100)
own_fit_both_y = fit_function_both(own_fit_both_x, par[0], par[1])

##fitting one parameter

def fit_function_one(x, B):
    A = 1904
    return float(A) / B * ((1 + (x / lambda0)) ** B - 1)


par, cov = curve_fit(fit_function_one, all_data_delta_wavelength, all_data_P, p0=[7.665])
print par
print np.sqrt(cov[0, 0])

own_fit_one_x = np.linspace(0, max(all_data_delta_wavelength) * 1.05, 100)
own_fit_one_y = fit_function_one(own_fit_one_x, par[0])

mao_fit_x = np.linspace(0, max(all_data_delta_wavelength) * 1.05, 100)
mao_fit_y = fit_function_both(mao_fit_x, 1904, 7.665)
plt.plot(own_fit_both_x, own_fit_both_y, 'g-', lw=3)
plt.plot(own_fit_one_x, own_fit_one_y, 'b-', lw=3)
plt.plot(mao_fit_x, mao_fit_y, 'r-', lw=3)
plt.show()




