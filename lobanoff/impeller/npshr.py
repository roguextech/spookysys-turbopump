"""Figure 3-6: NPSHR prediction chart [US]"""
from __future__ import print_function
import numpy as np
from numpy.polynomial import polynomial
from matplotlib import pyplot as plt
from utils import memoized, polyfit2d
from units import ureg
from lobanoff.data import _data as _lobanoff_data


def _data():
    return _lobanoff_data()['impeller']['npshr']


def _points():
    return np.transpose(_data())


@memoized
def get_coeffs():
    """Polynomial coefficients relating Cm1 and Ut to NPSHR"""
    return polyfit2d(*_points(), order=3)


@memoized
def get_limits():
    """Return limits"""
    Cm1, Ut, npshr = _points()
    # max npshr is 80
    return min(Cm1), 80, (min(Ut), max(Ut))


def plot():
    """Plot raw data and polynomial approximation"""
    plt.figure()
    Cm1s, Uts, npshrs = _points()

    # Plot fit
    for Ut in sorted(list(set(Uts))):
        fitted_Cm1 = np.linspace(5, 50)
        fitted_Ut = [Ut] * len(fitted_Cm1)
        fitted_npshr = polynomial.polyval2d(fitted_Cm1, fitted_Ut, get_coeffs())
        plt.plot(fitted_Cm1, fitted_npshr, 'g-')
        annotate_x = 34
        annotate_y = polynomial.polyval2d(annotate_x, Ut, get_coeffs())
        plt.annotate(str(Ut), xy=(annotate_x, annotate_y))

    # Plot data
    plt.plot(Cm1s, npshrs, 'r.')

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, 50 + 5, 5))
    plt.gca().set_yticks(np.arange(0, 80 + 5, 5))
    plt.gca().set_xlim(0, 50)
    plt.gca().set_ylim(0, 80)
    plt.xlabel('Cm1 - Suction Eye Velocity [ft/s]')
    plt.ylabel('Required NPSH water [ft]')
    plt.minorticks_on()
    plt.grid()
    plt.draw()


if __name__ == '__main__':
    plot()
    plt.show()


@ureg.wraps('ft', ('ft/s', 'ft/s'))
def calc(Cm1, Ut):
    """Calculate NPSHR"""
    startpoint_Cm1, endpoint_npshr, (startpoint_Ut, endpoint_Ut) = get_limits()
    assert startpoint_Ut <= Ut <= endpoint_Ut
    assert startpoint_Cm1 <= Cm1
    npshr = polynomial.polyval2d(Cm1, Ut, get_coeffs())
    assert npshr <= endpoint_npshr
    return npshr
