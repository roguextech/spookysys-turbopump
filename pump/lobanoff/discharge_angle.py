"""Figure 3-2 (and redundantly in 3-13), discharge angle by vane-count"""
# Note: Figures 3-2 and 3-13 differ by 1 degree for Z=8. I took the one from 3-2 to avoid inconsistencies.
from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
from utils import memoized
from units import ureg
from pump.lobanoff._data import _data as _lobanoff_data


def _data():
    return _lobanoff_data()['head_rise']


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
    return coeffs


def plot():
    """Plot raw data and polynomial approximation"""
    plt.figure()
    startpoint, endpoint = get_limits()

    # Plot data
    x = [x_['vanes'] for x_ in _data()]
    y = [x_['discharge_angle'] for x_ in _data()]
    plt.plot(x, y, 'r-')

    # Plot fitted curves
    x = np.linspace(*get_limits())
    y = np.polyval(get_coeffs(), x)
    plt.plot(x, y, 'g--')

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, 10 + 2, 2))
    plt.gca().set_yticks(np.arange(12, 32 + 2, 2))
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
