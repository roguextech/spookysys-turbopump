"""Figure 3-2 and ___ redundantly, Discharge angle by vane-count [US]"""
from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
from utils import memoized
from units import ureg
from lobanoff.graphs._data import _data as _lobanoff_data


def _data():
    return _lobanoff_data()['impeller']['head_rise']


@memoized
def get_limits(droop=None):
    """Return the minimum and maximum vane-count"""
    vanes = [
        x['vanes']
        for x in _data()
        if droop is None
        or (droop and x['droop'])
        or (not droop and not x['droop'])
    ]
    return min(vanes), max(vanes)


@memoized
def get_coeffs():
    """Polynomial coefficients relating vane-count to discharge angle"""
    vanes = [x['vanes'] for x in _data()]
    val = [x['discharge_angle'] for x in _data()]
    coeffs = np.polyfit(vanes, val, 3)
    test = np.polyval(coeffs, vanes)
    return coeffs


def plot():
    """Plot raw data and polynomial approximation"""
    plt.figure()
    startpoint, endpoint = get_limits()

    print('TODO TODO TODO TODO')

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(startpoint, endpoint + 1, 1))
    plt.gca().set_yticks(np.arange(0, 65, 5))
    plt.xlabel('Z - Vane count')
    plt.ylabel('Discharge angle')
    plt.grid()
    plt.draw()


if __name__ == '__main__':
    plot()
    plt.show()


@ureg.wraps('degrees', ('count'))
def calc(vanes):
    """Calculate discharge angle"""
    return np.polyval(get_coeffs(), vanes)
