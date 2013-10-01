from T_Rax_Data import gauss_curve_function
from T_Rax_RubyData import pseudo_voigt_curve, gauss_curve, lorentz_curve
import matplotlib.pyplot as plt
import numpy as np

x=np.linspace(-5,5,1000)
y=pseudo_voigt_curve(x,5,0.2,0.3,0)
plt.plot(x,y)

y=pseudo_voigt_curve(x,5,0.1,0.3,0)

plt.plot(x,y)

y=pseudo_voigt_curve(x,5,0.2,0.9,0)
plt.plot(x,y)

y=pseudo_voigt_curve(x,5,0.3,0.1,0)
plt.plot(x,y)

y=pseudo_voigt_curve(x,5,0.5,0.2,0)
plt.plot(x,y)
plt.show()