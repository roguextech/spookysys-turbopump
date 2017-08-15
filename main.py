from __future__ import print_function
from matplotlib import pyplot as plt
import lobanoff
import lobanoff.impeller
import lobanoff.impeller.head_rise
import lobanoff.impeller.head_constant
import lobanoff.impeller.capacity_constant
import lobanoff.impeller.diameter_ratio
import lobanoff.impeller.npshr
import lobanoff.impeller.volute_constant
from units import ureg

print(ureg.pump_Ns)
print(ureg.pump_Ns_us)
print(ureg.meter)
print(1 * ureg.meter)
print(1 * ureg.pump_Ns)
print((1 * ureg.pump_Ns).to_base_units())
print((1 * ureg.pump_Ns).to(ureg.pump_Ns_us))
print((1 * ureg.pump_Ns).to(ureg.pump_Ns_us).to_base_units())

# lobanoff.impeller.head_rise.plot()
# lobanoff.impeller.head_constant.plot()
# lobanoff.impeller.capacity_constant.plot()
# lobanoff.impeller.diameter_ratio.plot()
lobanoff.impeller.npshr.plot()
# lobanoff.impeller.volute_constant.plot()
plt.show()
