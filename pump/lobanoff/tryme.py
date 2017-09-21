"""Generate impeller as per Lobanoff's chapter"""
from __future__ import print_function
import numpy as np
from numpy import pi as PI
from numpy.polynomial import polynomial
from scipy.special import expit
from units import ureg
from pump.lobanoff.capacity_constant import calc as calc_capacity_constant
from pump.lobanoff.diameter_ratio import calc as calc_diameter_ratio
from pump.lobanoff.discharge_angle import calc as calc_discharge_angle
from pump.lobanoff.head_constant import calc as calc_head_constant
from pump.lobanoff.head_rise_shutoff import calc as calc_head_rise_shutoff
from pump.lobanoff.npshr import calc as calc_npshr
from pump.lobanoff.volute_constant import calc as calc_volute_constant
from pump.lobanoff.volute_misc import calc_volute_width, calc_cutwater_diameter
from pump.lobanoff.vane_and_shroud_thickness import calc_vane_thickness
from pump.lobanoff.misc import calc_specific_speed, G


@ureg.check('gpm', 'ft', 'rpm', 'count', 'inch')
def generate(Q, H, n, vanes, Ds, tweak_eye_diameter, tweak_discharge_blade_width, tweak_volute_width, tweak_cutwater_diameter, tweak_Ps1):
    """Design impeller"""

    # Specific speed
    Ns = calc_specific_speed(Q, H, n)

    # from page 36
    assert 400 <= Ns.to('Ns_loba').magnitude <= 3600

    # Head constant, reduced U2
    Ku = calc_head_constant(Ns, vanes)
    U2 = Ku * (2 * G * H)**0.5

    # Capacity constant, reduced Cm2
    Km2 = calc_capacity_constant(Ns, vanes)
    Cm2 = Km2 * (2 * G * H)**0.5

    # Outer diameter
    D2 = 2 * U2.to('inches/s') / n.to('1/s')

    # Eye diameter
    dia_r = calc_diameter_ratio(Ns, tweak_eye_diameter)
    D1 = D2 * dia_r

    # Outer vane thickness
    Su2 = calc_vane_thickness(D2, 0)

    # Outer width
    b2 = (Q / (Cm2 * (D2 * PI - vanes * Su2))).to('inch')

    # Impeller discharge area
    A2 = (D2 * PI - vanes * Su2) * b2

    # Impeller eye area at blade entry
    Ae = (D1**2 - Ds**2) * (PI / 4)

    # Outer vane thickness
    Su1 = calc_vane_thickness(D2, 2)

    # Average meridianal velocity at blade inlet
    Cm1 = (Q / Ae).to('ft/s')

    # Inlet peripheral speed
    Ut = (n * D1 / 2).to('ft/s')

    # Discharge angle
    discharge_angle = calc_discharge_angle(vanes)

    # suction
    npshr = calc_npshr(Cm1, Ut)

    # Suction specific speed
    Nss = calc_specific_speed(Q, npshr, n)

    # Volute throat area
    K3 = calc_volute_constant(Ns)
    K3 = 0.365 * ureg['']
    C3 = K3 * (2 * G * H)**0.5
    A8 = (Q / C3).to('inch**2')

    # Volute width
    b3 = b2 * calc_volute_width(Ns, tweak_volute_width)

    # Volute cutwater diameter
    D3 = D2 * calc_cutwater_diameter(Ns, tweak_cutwater_diameter)

    # Head rise at shutoff
    head_rise_shutoff = calc_head_rise_shutoff(Ns, vanes)

    # Inlet angle, Ps1
    theta = np.arctan2(Cm1, Ut).to('deg')
    R1_inv = 1.05 + (1.2 - 1.05) * expit(tweak_Ps1)
    Ps1 = Cm1 * R1_inv
    B1 = np.arctan2(Ps1, Ut).to('deg')  # tan(B1) = Ps1 / Ut
    Wu1 = Cm1 / np.tan(B1)  # tan(B1) = Cm1 / Wu1
    prerot_angle = np.arctan2((Ut - Wu1), Cm1).to('deg')  # tan(prerot) = (Ut-Wu1) / Cm1
    if prerot_angle > 30:
        print('Warning: Prerotation angle shouldn\'t be higher than 30 degrees.')

    return {
        'D1': D1,
        'D2': D2,
        'D3': D3,
        'b2': b2,
        'b3': b3,
        'Su1': Su1,
        'Su2': Su2,
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
        'B1': B1,
        'prerot_angle': prerot_angle,
        'discharge_angle': discharge_angle,
        'head_rise_shutoff': head_rise_shutoff,
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
        0 * ureg[''],
        0 * ureg['']
    )
    print('\n'.join((str(x) + ': ' + str(pumpe[x]) for x in pumpe)))
