from pint import UnitRegistry, set_application_registry

ureg = UnitRegistry()
set_application_registry(ureg)
Q = ureg.Quantity

ureg.define('gallons_per_minute = gallons/minute = gpm')
ureg.define('liters_per_second = liter/second = lps')
ureg.define('pump_Ns_metric = rpm * lps**0.5 / meter**0.75')
ureg.define('pump_Ns_us = rpm * gpm**0.5 / feet**0.75')
ureg.define('percent = 0.01*count = pct')
