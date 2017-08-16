"""Miscellaneous tables and figures"""
from scipy.special import expit
import numpy as np
from matplotlib import pyplot as plt
from utils import memoized

#@ureg.wraps('', ('pump_Ns_us'))


def _points_volute_width():
    return [0, 1000, 1000, 3000, 3000, 4000], [2.0, 2.0, 1.75, 1.75, 1.6, 1.6]


def calc_volute_width(Ns, tweak):
    """Estimate b3/b2 - Volute width factor"""
    param = -(Ns - 1500) / 500 + 0.5
    t = expit(param + tweak)
    return 1.6 + t * (2.0 - 1.6)


def _points_cutwater_diameter():
    return [600, 1000, 1000, 1500, 1500, 2500, 2500, 4000], [1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.09, 1.09]


def calc_cutwater_diameter(Ns, tweak):
    """Estimate D3/D2 - Volute diameter factor"""
    param = (Ns - 1750) / 250
    t = expit(param + tweak)
    return 1.05 + t * (1.09 - 1.05)


def plot_volute_width():
    plt.figure()

    startpoint, endpoint = 0, 4000

    # What Lobanoff said
    plt.plot(*_points_volute_width())

    # Plot fitted curve
    x = np.linspace(startpoint, endpoint)

    plt.plot(x, calc_volute_width(x, 0))
    plt.plot(x, calc_volute_width(x, -1), '--')
    plt.plot(x, calc_volute_width(x, +1), '--')
    plt.plot(x, calc_volute_width(x, -2), '.')
    plt.plot(x, calc_volute_width(x, +2), '.')

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, endpoint + 1, 500))
    plt.gca().set_yticks(np.arange(1.6, 2.0 + .1, .1))
    plt.xlabel('Ns - Specific Speed')
    plt.ylabel('b3/b2')
    plt.grid()
    plt.draw()


def plot_cutwater_diameter():
    plt.figure()

    startpoint, endpoint = 0, 4000

    # What Lobanoff said
    plt.plot(*_points_cutwater_diameter())

    # Plot fitted curve
    x = np.linspace(startpoint, endpoint)

    plt.plot(x, calc_cutwater_diameter(x, 0))
    plt.plot(x, calc_cutwater_diameter(x, -1), '--')
    plt.plot(x, calc_cutwater_diameter(x, +1), '--')
    plt.plot(x, calc_cutwater_diameter(x, -2), '.')
    plt.plot(x, calc_cutwater_diameter(x, +2), '.')

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, endpoint + 1, 500))
    plt.gca().set_yticks(np.arange(1.05, 1.09 + .01, .01))
    plt.xlabel('Ns - Specific Speed')
    plt.ylabel('D3/D2')
    plt.grid()
    plt.draw()


if __name__ == '__main__':
    plot_volute_width()
    plot_cutwater_diameter()
    plt.show()
