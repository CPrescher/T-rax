import numpy as np
import matplotlib.pyplot as plt
from T_Rax_Data import CalibParam

test_param=CalibParam()
test_param.load_etalon_spec("Temperature Calibration\\15A Lamp.txt")
test_param.set_temp(2500)
x=np.linspace(600,900)

plt.plot(x, test_param.get_calibrated_spec(x))
plt.figure()
test_param.set_modus(1)
plt.plot(x, test_param.get_calibrated_spec(x))
plt.figure()
test_param.set_modus(2)
test_param.set_polynom([1,2,0,4])
plt.plot(x, test_param.get_calibrated_spec(x))
plt.show()


