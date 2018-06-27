"""Miscellaneous functions"""
import scipy.constants
from units import ureg


# Gravity in the USA
G = (scipy.constants.g * ureg['m/s**2']).to('ft/s**2')


@ureg.check('gpm', 'ft', 'rpm')
def calc_specific_speed(Q, H, n):
    """Calculate Ns, specific speed, or Nss, by supplying npshr for H"""
    Ns = n.to('rpm') * Q.to('gpm')**0.5 / H.to('ft')**0.75
    return Ns.to(ureg.Ns_loba)
