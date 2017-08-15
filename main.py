from __future__ import print_function
import lobanoff
import lobanoff.impeller
import lobanoff.impeller.head_rise
from units import ureg

print(ureg.pump_Ns)
print(ureg.pump_Ns_us)
print(ureg.meter)
print(1 * ureg.meter)
print(1 * ureg.pump_Ns)
print((1 * ureg.pump_Ns).to_base_units())
print((1 * ureg.pump_Ns).to(ureg.pump_Ns_us))
print((1 * ureg.pump_Ns).to(ureg.pump_Ns_us).to_base_units())

lobanoff.impeller.head_rise.plot()
print('done')
