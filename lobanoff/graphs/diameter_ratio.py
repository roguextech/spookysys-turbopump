"""Figure 3-5: D2/D1 - Impeller eye to outside diameter ratio"""
from __future__ import print_function
import numpy as np
from scipy.special import expit
from matplotlib import pyplot as plt
from utils import memoized
from units import ureg
from lobanoff.graphs._data import _data as _lobanoff_data


def _data():
    return _lobanoff_data()['diameter_ratio']


def _points(curve):
    return np.transpose(_data()[curve])


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
    startpoint = max(min(upper), min(lower))
    endpoint = min(max(upper), max(lower))
    return startpoint, endpoint


def plot():
    """Plot raw data and polynomial approximation"""
    plt.figure()

    # Plot data
    for curve in _data():
        x, y = _points(curve)
        plt.plot(x, y, 'r--')

    # Plot fitted curves
    for curve in _data():
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
    plt.draw()


if __name__ == '__main__':
    plot()
    plt.show()


@ureg.wraps('', ('pump_Ns_us', ''))
def calc(Ns, tweak_eye_diameter):
    """Calculate D2/D1"""
    startpoint, endpoint = get_limits()
    assert startpoint <= Ns <= endpoint
    lower = np.polyval(get_coeffs('lower'), Ns)
    upper = np.polyval(get_coeffs('upper'), Ns)
    return lower + (upper - lower) * expit(tweak_eye_diameter)
