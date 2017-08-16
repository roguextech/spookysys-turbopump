import numpy as np
from units import ureg
from lobanoff.misc import calc_specific_speed
from lobanoff.impeller import head_rise, head_constant, capacity_constant, diameter_ratio, npshr, volute_constant


def calc_discharge_angle(vanes):
    """Calculate discharge angle from number of vanes"""
    return np.polyval(head_rise.get_discharge_angle_coeffs(), vanes) * ureg.degrees


@ureg.check(ureg.pump_Ns_us, None)
def calc_head_constant(Ns, vanes):
    offset_coeffs, slope = head_constant.get_coeffs()
    offset = np.polyval(offset_coeffs, vanes)
    return offset + slope * Ns.to(ureg.pump_Ns_us).magnitude


@ureg.check(ureg.gpm, ureg.ft, ureg.rpm)
def do(Q, H, n, vanes=5):
    """Design impeller"""

    # Specific speed
    Ns = calc_specific_speed(Q, H, n)

    # Discharge angle
    discharge_angle = calc_discharge_angle(vanes)

    # Head constant
    Ku = calc_head_constant(Ns, vanes)

    return Ns, discharge_angle, Ku


if __name__ == '__main__':
    pumpe = do(2100 * ureg.gpm, 450 * ureg.ft, 3600 * ureg.rpm, 6)
    print(list(str(x) for x in pumpe))
