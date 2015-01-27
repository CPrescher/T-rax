import sys
# for backwards compatibility of pickle:
import TemperatureData

sys.modules['T_Rax_TemperatureData'] = TemperatureData
sys.modules['data.T_Rax_TemperatureData'] = TemperatureData
