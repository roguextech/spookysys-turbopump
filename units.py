from pint import UnitRegistry, set_application_registry

ureg = UnitRegistry()
set_application_registry(ureg)
Q = ureg.Quantity

ureg.define('percent = 0.01*count = pct')
ureg.define('gallons_per_minute = gallons/minute = gpm')
ureg.define('liters_per_second = liter/second = lps')

ureg.define('Ns_loba_metric = rpm * (m**3/s)**0.5 / meter**0.75')
ureg.define('Ns_loba = rpm * gpm**0.5 / feet**0.75')
