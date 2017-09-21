import numpy as np
from units import ureg
from pump.lobanoff.vane_and_shroud_thickness import calc_vane_thickness


@ureg.check('gpm', 'feet', 'count', 'inch', 'inch', 'inch', 'inch', 'degrees', '')
def generate_impeller(Q, H, n, vanes, Ds, D1, D2, b2, B2, aspect):
    """Generate geometry for impelller"""

    # Eye area
    Su1 = calc_vane_thickness(D2, 2)
    Ae = np.pi * D1**2 / 4 - np.pi * Ds**2 / 4 - vanes * Su1 * (D1 - Ds) / 2

    # Outlet area
    Su2 = calc_vane_thickness(D2, 0)
    A2 = (np.pi * D2 - vanes * Su2) * b2

    C1 = Q / Ae
    I = C1**2 / 2

    h02 = H * G
    Cu2 = (I * h02) / U2

    # Stagnasjonsentalpi øker lineært fra 0 til H*G
    # C(s)**2 øker lineært
    # Konstant rotalpi gir U(s) og dermed D(s)
    # Interpolasjon fra C1 til C2 i henhold til C**2 sammen med D gir bane i 3 dimensjoner
    # Areal gitt av kontinuitetsligningen
    # Kalkuler front/rear shroud gitt middellinje og uttrykk for areal
