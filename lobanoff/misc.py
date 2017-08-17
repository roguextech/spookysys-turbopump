"""Miscellaneous functions for Lobanoff method"""
from units import ureg


@ureg.check('gpm', 'ft', 'rpm')
def calc_specific_speed(Q, H, n):
    """Calculate Ns, specific speed, as per Lobanoff"""
    Ns = n * Q**0.5 / H**0.75
    return Ns.to(ureg.pump_Ns_us)
