from pint import UnitRegistry, set_application_registry

ureg = UnitRegistry()
set_application_registry(ureg)
Q = ureg.Quantity

ureg.define('gpm = gallons/minute')
ureg.define('lps = liter/second')
ureg.define('pump_Ns_mt = rpm * lps**0.5 / meter**0.75')
ureg.define('pump_Ns_us = rpm * gpm**0.5 / feet**0.75')
