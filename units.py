"""Global ureg and some derived units"""
from __future__ import unicode_literals
from pint import UnitRegistry, set_application_registry
ureg = UnitRegistry()
set_application_registry(ureg)
Q_ = ureg.Quantity

ureg.pump_Ns = ureg.rpm * (ureg.liter / ureg.second)**0.5 / ureg.meter**0.75
ureg.pump_Ns_us = ureg.rpm * (ureg.gallons / ureg.minute)**0.5 / ureg.feet**0.75
