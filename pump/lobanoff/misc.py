"""Miscellaneous functions"""
import scipy.constants
from units import ureg


# Gravity in the USA
G = (scipy.constants.g * ureg['m/s**2']).to('ft/s**2')


@ureg.check('gpm', 'ft', 'rpm')
def calc_specific_speed(Q, H, n):
    """Calculate Ns, specific speed, or Nss, by supplying npshr for H"""
    Ns = n * Q**0.5 / H**0.75
    return Ns.to(ureg.pump_Ns_us)
