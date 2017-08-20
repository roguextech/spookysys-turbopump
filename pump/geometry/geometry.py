import numpy as np
from units import ureg
from pump.lobanoff.vane_and_shroud_thickness import calc_vane_thickness


@ureg.check('count', 'inch', 'inch', 'inch', 'inch', 'gpm', 'degrees', 'degrees')
def generate_impeller(vanes, Ds, D1, D2, b2, Q, B1, B2):
    """Generate geometry for impelller"""

    # Eye area
    Su1 = calc_vane_thickness(D2, 2)
    Ae = np.pi * D1**2 / 4 - np.pi * Ds**2 / 4 - vanes * Su1 * (D1 - Ds) / 2

    # Outlet area
    Su2 = calc_vane_thickness(D2, 0)
    A2 = (np.pi * D2 - vanes * Su2) * b2

    # Smooth area interpolation
    # Smooth meridional angle interpolation
    # Smooth radial angle interpolation
