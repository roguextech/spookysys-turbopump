"""Conversions w Lobanoff"""
from units import ureg
import scipy.constants
import numpy as np
from pump.lobanoff.misc import G as G_loba, calc_specific_speed as calc_specific_speed_loba
from numpy import pi as PI

G = scipy.constants.g * ureg['m/s**2']


@ureg.check('Ns_loba')
def from_Ns_loba(Ns_loba):
    """Convert Lobanoff's specific speed to Dixan's omega specific speed (do .to('rads') to get omega)"""
    Ns_dixan = Ns_loba / G_loba**0.75
    return Ns_dixan.to('turns')


@ureg.check('', '')
def from_coeffs_loba(Km2, Ku):
    """Convert Lobanoff's head and capacity constants to Dixan's head and flow coefficients"""
    # Cm2 / U2
    flow_coefficient = Km2 / Ku
    # w = U/r = 2U/D
    # N = w * 60/2PI = 2U/D * 60/2PI = U/D * 60/PI
    # ND = U * 60/PI
    head_coefficient = .5 / (Ku * 60 / PI)**2
    return flow_coefficient.to(''), head_coefficient.to('')


def Ns_from_coeffs(flow_coeff, head_coeff):
    return flow_coeff**0.5 / head_coeff**0.75


from pump.lobanoff.head_constant import calc as calc_head_constant
from pump.lobanoff.capacity_constant import calc as calc_capacity_constant

if __name__ == '__main__':
    vanes = 6 * ureg['']
    D = 4.31 * ureg['m']
    H = 543 * ureg['m']
    Q = 71.5 * ureg['m**3/s']
    n = (333 * ureg['rpm']).to('rad/s')
    print(str(n))
    Ns_loba = calc_specific_speed_loba(Q, H, n)
    capacity_constant = calc_capacity_constant(Ns_loba, vanes)
    head_constant = calc_head_constant(Ns_loba, vanes)
    Ns_dixon_from_loba = from_Ns_loba(Ns_loba)
    flow_coeff, head_coeff = from_coeffs_loba(capacity_constant, head_constant)
    Ns_dixon_from_coeffs = Ns_from_coeffs(flow_coeff, head_coeff)
    #print(str(Ns_dixon), str(Ns_dixon2))
    # plot()
    # plt.show()
