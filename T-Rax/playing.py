from T_Rax_Data import black_body_function

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

data = np.loadtxt('15A_lamp.txt')

x=data.T[0]
y=data.T[1]

param, pcov = curve_fit(black_body_function,x,y, p0=[2000,100])
print param

y_fit = black_body_function(x,param[0],param[1])

plt.plot(x,y)
plt.plot(x,y_fit)

plt.show()