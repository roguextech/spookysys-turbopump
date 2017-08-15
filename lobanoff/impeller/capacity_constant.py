"""Figure 3-4: Capacity Constant Km2 [US]"""
from __future__ import print_function
from itertools import chain
import numpy as np
from numpy.polynomial import polynomial
from numpy import polyfit
from matplotlib import pyplot as plt
from misc import memoized, polyfit2d
from . import _jsondata as _module_jsondata


def _jsondata():
    return _module_jsondata()['capacity_constant']


@memoized
def get_Km2_coeffs():
    """Polynomial coefficients relating vane-count and specific speed to capacity constant"""
    fitdata = np.ndarray(shape=(3, 0), dtype=float)
    for curve in _jsondata():
        y, z = np.transpose(curve['points'])
        for vanes in curve['vanes']:
            x = np.ones(len(curve['points'])) * vanes
            fitdata = np.append(fitdata, [x, y, z], axis=1)
    return polyfit2d(*fitdata, order=2)


@memoized
def get_vane_limits():
    """Return the vane-counts for which there is data"""
    vanes = list(chain.from_iterable(
        x['vanes'] for x in _jsondata()
    ))
    return min(vanes), max(vanes) + 1


@memoized
def get_Ns_limit_coeffs():
    """Polynomial coefficients relating vane-count to highest Km2 in graph"""
    x, y = [], []
    for curve in _jsondata():
        vanes = curve['vanes']
        point = curve['points'][-1][0]
        x.extend(vanes)
        y.extend([point] * len(vanes))
    return polyfit(x, y, deg=1)


def plot():
    """Plot raw data and polynomial approximation"""

    # Plot data
    for curve in _jsondata():
        vanes = curve['vanes']
        Ns, Km2 = np.transpose(curve['points']).tolist()
        plt.plot(Ns, Km2, 'r-')

    # Plot fitted curves
    for vanes in np.arange(get_vane_limits()[0], get_vane_limits()[1] - 0.5, step=0.5):
        startpoint = 400
        endpoint = np.polyval(get_Ns_limit_coeffs(), vanes)
        x = np.arange(startpoint, endpoint + 1, 50)
        y = polynomial.polyval2d(np.ones(len(x)) * vanes, x, get_Km2_coeffs())
        plt.plot(x, y, 'g--')
        label = str(vanes)
        label_xy = (endpoint, y[-1])
        plt.annotate(label, xy=label_xy)

    # plot limit of data
    vanespace = range(*get_vane_limits())
    limit_x = np.polyval(get_Ns_limit_coeffs(), vanespace)
    limit_y = polynomial.polyval2d(vanespace, limit_x, get_Km2_coeffs())
    plt.plot(limit_x, limit_y)

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, 3600 + 1, 400))
    plt.gca().set_yticks(np.arange(0, 0.28, 0.02))
    plt.xlabel('Ns - Specific Speed')
    plt.ylabel('Km2 - Capacity Constant')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    plot()
