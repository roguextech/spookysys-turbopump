"""Figure 3-6: NPSHR prediction chart [US]"""
from __future__ import print_function
from itertools import chain
import numpy as np
from numpy.polynomial import polynomial
from numpy import polyfit
from matplotlib import pyplot as plt
from misc import memoized, polyfit2d
from . import _jsondata as _module_jsondata


def _points():
    return np.transpose(_module_jsondata()['npshr'])


@memoized
def get_coeffs():
    """Polynomial coefficients relating Cm1 and Ut to NPSHR"""
    return polyfit2d(*_points(), order=2)


@memoized
def get_limits():
    """Return limits"""
    Cm1, Ut, npshr = _points()
    # return min(Cm1), max(npshr), min(Ut), max(Ut)
    return (5), (80), (30, 120)


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
