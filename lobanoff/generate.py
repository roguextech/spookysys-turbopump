"""Generate impeller as per Lobanoff's chapter"""
from __future__ import print_function
import numpy as np
from numpy.polynomial import polynomial
from scipy.special import expit
import scipy.constants
from units import ureg
from lobanoff.graphs.capacity_constant import calc as calc_capacity_constant
from lobanoff.graphs.diameter_ratio import calc as calc_diameter_ratio
from lobanoff.graphs.discharge_angle import calc as calc_discharge_angle
from lobanoff.graphs.head_constant import calc as calc_head_constant
#from lobanoff.graphs.head_rise import calc as calc_head_rise
from lobanoff.graphs.npshr import calc as calc_npshr
from lobanoff.graphs.volute_constant import calc as calc_volute_constant
from lobanoff.graphs.volute_misc import calc_volute_width, calc_cutwater_diameter

# Gravity in the USA
_g = (scipy.constants.g * ureg['m/s**2']).to('ft/s**2')


@ureg.check('gpm', 'ft', 'rpm')
def calc_specific_speed(Q, H, n):
    """Calculate Ns, specific speed, or Nss, by supplying npshr for H"""
    Ns = n * Q**0.5 / H**0.75
    return Ns.to(ureg.pump_Ns_us)


@ureg.check('gpm', 'ft', 'rpm', 'count', 'inch', '')
def generate(Q, H, n, vanes, protruding_shaft_diameter, tweak_eye_diameter, tweak_discharge_blade_width, tweak_volute_width, tweak_cutwater_diameter):
    """Design impeller"""

    # Specific speed
    Ns = calc_specific_speed(Q, H, n)

    # from page 36
    assert 400 <= Ns.to('pump_Ns_us').magnitude <= 3600

    # Head constant, reduced U2
    Ku = calc_head_constant(Ns, vanes)
    U2 = Ku * (2 * _g * H)**0.5

    # Capacity constant, reduced Cm2
    Km2 = calc_capacity_constant(Ns, vanes)
    Cm2 = Km2 * (2 * _g * H)**0.5

    # Outer diameter
    D2 = 2 * (U2 / n).to('inch')  # important cast to go from circular to linear"

    # Eye diameter
    dia_r = calc_diameter_ratio(Ns, tweak_eye_diameter)
    D1 = D2 * dia_r

    # Outer vane thickness (rough guess)
    tmp = expit(-1.35 + tweak_discharge_blade_width.magnitude)
    Su = (np.pi * D2 / vanes.magnitude) * tmp

    # Outer width
    b2 = (Q / (Cm2 * (D2 * np.pi - vanes * Su))).to('inch')

    # Eye area
    Ae = (D1**2 - protruding_shaft_diameter**2) * (np.pi / 4)

    # Inlet flow speed
    Cm1 = (Q / Ae).to('ft/s')

    # Inlet peripheral speed
    Ut = (n * D1 / 2).to('ft/s')

    # suction
    npshr = calc_npshr(Cm1, Ut)

    # Discharge angle
    discharge_angle = calc_discharge_angle(vanes)

    # Suction specific speed
    Nss = calc_specific_speed(Q, npshr, n)

    # Volute area
    K3 = calc_volute_constant(Ns)
    K3 = 0.365 * ureg['']
    C3 = K3 * (2 * _g * H)**0.5
    A8 = (Q / C3).to('inch**2')

    # Volute width
    b3 = b2 * calc_volute_width(Ns, tweak_volute_width)

    # Volute cutwater diameter
    D3 = D2 * calc_cutwater_diameter(Ns, tweak_cutwater_diameter)

    return {
        'D1': D1,
        'D2': D2,
        'D3': D3,
        'b2': b2,
        'b3': b3,
        'Su': Su,
        'A8': A8,
        'Ae': Ae,
        'npshr': npshr,
        'Ns': Ns,
        'Nss': Nss,
        'Cm1': Cm1,
        'Cm2': Cm2,
        'C3': C3,
        'Ut': Ut,
        'U2': U2,
        'discharge_angle': discharge_angle
    }


if __name__ == '__main__':
    pumpe = generate(
        2100 * ureg.gpm,
        450 * ureg.ft,
        3600 * ureg.rpm,
        6 * ureg.count,
        2 * ureg.inch,
        0 * ureg[''],
        0 * ureg[''],
        0 * ureg[''],
        0 * ureg['']
    )
    print('\n'.join((str(x) + ': ' + str(pumpe[x]) for x in pumpe)))
