"""Figure 3-11: Recommended minimum impeller vane and shroud thickness for castability (standard cast materials) from D2"""
from __future__ import print_function
from itertools import chain
import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial import polynomial
from utils import memoized, polyfit2d
from units import ureg
from pump.lobanoff._data import _data as _lobanoff_data


def _data():
    return _lobanoff_data()['vane_and_shroud_thickness']


@memoized
def get_limits():
    """Return the limits for D2"""
    vanes = list(chain.from_iterable(
        x['D2'] for x in _data()
    ))
    return min(vanes), max(vanes)


def _points(part):
    diameters, values = [], []
    for iter in _data():
        p = iter['D2']
        dias = [p[0], np.average(p), p[-1]]
        diameters.extend(dias)
        values.extend([iter[part]] * len(dias))
    return diameters, values


@memoized
def get_coeffs(part, point):
    """Polynomial coefficients relating D2 to vane/shroud thickness at different points"""
    diameters, values = _points(part)
    values = [x[point] for x in values]
    return np.polyfit(diameters, values, 2)


def plot(part):
    plt.figure()

    # Plot data
    x, y = _points(part)
    plt.plot(x, y, 'r.')

    # Plot fitted curve
    x = np.linspace(*get_limits())
    for point in range(0, len(y[0])):
        y = np.polyval(get_coeffs(part, point), x)
        plt.plot(x, y, 'g-')

    plt.gca().set_title(part)
    plt.gca().set_xticks(np.arange(0, get_limits()[1] + get_limits()[0] + 1, 10))
    plt.gca().set_yticks(np.arange(0, 1, 1. / 16))
    plt.gca().set_xlim(0, get_limits()[1] + get_limits()[0])
    plt.gca().set_ylim(0, 1)
    plt.minorticks_on()
    plt.grid()
    plt.xlabel('D2 - Impeller diameter [inch]')
    plt.ylabel(part + 'thickness [inch]')
    plt.draw()


if __name__ == '__main__':
    plot('vane')
    plot('shroud')
    plt.show()


@ureg.wraps('inch', ('inch'))
def calc_vane_thickness(D2, point):
    """Minimum vane thickness, 0: outlet, 1:middle, 2:inlet"""
    startpoint, endpoint = get_limits()
    assert startpoint < D2 < endpoint
    return np.polyval(get_coeffs('vane', point), D2)


@ureg.wraps('inch', ('inch'))
def calc_shroud_thickness(D2, point):
    """Minimum back shroud thickness, 0:t1 at outlet, 1:t2 at 3/4*D2"""
    startpoint, endpoint = get_limits()
    assert startpoint < D2 < endpoint
    return np.polyval(get_coeffs('shroud', point), D2)
