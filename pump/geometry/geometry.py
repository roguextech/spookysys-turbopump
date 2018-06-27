import numpy as np
import scipy.constants
from units import ureg


# Metric gravity
G = scipy.constants.g * ureg['m/s**2']


# def _vane_width_function_generator(Su1, Su12, Su2, tx):
#     """Generate function for vane width
#     f(0) = Su1, f(1) = Su2, f(tx) = Su12, f'(tx) = 0
#     """
#     f = lambda x:
#         if x < tx:
#             return (1 - x / tx)**2 * (Su12 - Su1) + Su1
#         else:
#             return (x / (1 - tx))**2 * (Su2 - Su12) + Su12
#     return f


# def generate_impeller(Ds, D1, D2, b2, aspect, B1, B2, z, Su1, Su12, Su2, steps_axial=256, steps_tangential=256):
#     """Generate geometry for impelller
#     Ds - protruding shaft diameter
#     D1 - diameter at entry
#     D2 - diameter at exit
#     b2 - height at exit
#     aspect - length over radius (midline is an ellipse)
#     B1 - blade angle at inlet (periphery)
#     B2 - blade angle at discharge
#     z - number of vanes
#     Su1 - Vane thickness leading edge
#     Su12 - Vane thickness middle
#     Su2 - Vane thickness at discharge
#     """

#     # kurve for energimengde over reiselengde
#     # kurve for fraksjon av energi som er trykk vs kinetisk
#     # discharge angle

#     # Eye area
#     Ae = np.pi * D1**2 / 4 - np.pi * Ds**2 / 4 - z * Su1 * (D1 - Ds) / 2

#     # Outlet area
#     A2 = (np.pi * D2 - z * Su2) * b2

# #    for axial_s in xrange(0, 1, 1.0 / steps_axial):
# #        pass

#     # Stagnasjonsentalpi øker lineært fra 0 til H*G
#     # C(s)**2 øker lineært
#     # Konstant rotalpi gir U(s) og dermed D(s)
#     # Interpolasjon fra C1 til C2 i henhold til C**2 sammen med D gir bane i 3 dimensjoner
#     # Areal gitt av kontinuitetsligningen
#     # Kalkuler front/rear shroud gitt middellinje og uttrykk for areal


def generate_vaneless_impeller(Q, density, kinetic_head_curve, pressure_head_curve, Ds, D2, b2, discharge_angle):
    Cm1 = np.sqrt(2 * kinetic_head_curve(0) * G)  # kinetic_energy_per_kg = kinetic_head_curve(0) * G = 0.5 * Cm1**2
    Ae = Q / Cm1
    D1 = 2 * np.sqrt(Ae / np.pi + Ds**2 / 4)  # Ae = pi * r1**2 - pi * Ds**2/4

    # find radial midpoint D1_mid at entry
    # Ae_hi = Ae_lo
    # pi/4 * D1**2 - pi/4 * D1_mid**2 = pi/4 * D1_mid**2 - pi/4 * Ds**2
    # D1**2 - D1_mid**2 = D1_mid**2 - Ds**2
    # 2 * D1_mid**2 = D1**2 + Ds**2
    D1_mid = np.sqrt(D1**2 / 2.0 + Ds**2 / 2.0)


def main():
    pass


if __name__ == '__main__':
    main()
