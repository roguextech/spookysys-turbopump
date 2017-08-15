"""Figure 3-5: Impeller eye to outside diameter ratio [US]"""
from __future__ import print_function
from itertools import chain
import numpy as np
from numpy.polynomial import polynomial
from numpy import polyfit
from matplotlib import pyplot as plt
from misc import memoized, polyfit2d
from . import _jsondata as _module_jsondata


def _jsondata():
    return _module_jsondata()['diameter_ratio']


def _points(curve):
    return np.transpose(_jsondata()[curve])


@memoized
def get_coeffs(curve):
    """Polynomial coefficients for lower or upper bound"""
    x, y = _points(curve)
    return np.polyfit(x, y, 3)


@memoized
def get_limits():
    """Get the allowable range for Ns"""
    upper, _ = _points('upper')
    lower, _ = _points('lower')
    min_ = max(min(upper), min(lower))
    max_ = min(max(upper), max(lower))
    return min_, max_


def plot():
    """Plot raw data and polynomial approximation"""

    # Plot data
    for curve in _jsondata():
        x, y = _points(curve)
        plt.plot(x, y, 'r--')

    # Plot fitted curves
    for curve in _jsondata():
        x = np.linspace(*get_limits())
        y = np.polyval(get_coeffs(curve), x)
        plt.plot(x, y, 'g-')
        plt.annotate(curve, xy=(x[-1], y[-1]))

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, 3400 + 400, 400))
    plt.gca().set_yticks(np.arange(0.05, 0.75 + 0.05, 0.05))
    plt.xlabel('Ns - Specific Speed')
    plt.ylabel('D1/D2 - Eye Diameter / Outside Diameter')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    plot()
