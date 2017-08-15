"""Figure 3-2: Percent Head Rise [US]"""
from __future__ import print_function
from itertools import chain
import numpy as np
from numpy.polynomial import polynomial
from numpy import polyfit
from matplotlib import pyplot as plt
from misc import memoized, polyfit2d
from units import ureg
from . import _jsondata as _module_jsondata


def _jsondata():
    return _module_jsondata()['head_rise']


@memoized
def get_phr_coeffs():
    """Polynomial coefficients relating number of vanes and specific speed to percent head rise"""
    fitdata = [
        [np.ones(len(x['data'])) * x['vanes'] for x in _jsondata()],
        [np.transpose(x['data'])[0] for x in _jsondata()],
        [np.transpose(x['data'])[1] for x in _jsondata()]
    ]
    fitdata = np.array([list(chain.from_iterable(x)) for x in fitdata])
    return polyfit2d(*fitdata, order=3)


@memoized
def get_vanes(droop=None):
    """Return lowest and highest number of vanes for which there is data"""
    vanes = [x['vanes'] for x in _jsondata() if droop == None or (droop and x['droop']) or (not droop and not x['droop'])]
    return sorted(vanes)


@memoized
def get_Ns_limit_coeffs():
    """Polynomial coefficients relating number of vanes to highest Ns in graph"""
    vanes = [x['vanes'] for x in _jsondata()]
    val = [x['data'][-1][0] for x in _jsondata()]
    coeffs = polyfit(vanes, val, 3)
    test = np.polyval(coeffs, vanes)
    return coeffs


@memoized
def get_discharge_angle_coeffs():
    """Polynomial coefficients relating number of vanes to discharge angle"""
    vanes = [x['vanes'] for x in _jsondata()]
    val = [x['discharge_angle'] for x in _jsondata()]
    coeffs = polyfit(vanes, val, 3)
    test = np.polyval(coeffs, vanes)
    return coeffs


def plot():
    """Plot raw data and polynomial approximation"""

    for datum in _jsondata():
        vanes = datum['vanes']
        N_s, phr = np.transpose(datum["data"]).tolist()
        startpoint = N_s[0]
        endpoint = N_s[-1]
        label = str(datum["vanes"]) + " vanes, " + str(datum["discharge_angle"]) + " deg" + (", droop" if datum["droop"] else "")
        label_xy = (N_s[-1], phr[-1])
        plt.plot(N_s, phr, 'r--')
        plt.annotate(label, xy=label_xy)

    for datum in _jsondata():
        vanes = datum['vanes']
        N_s, phr = np.transpose(datum["data"]).tolist()
        startpoint = N_s[0]
        endpoint = N_s[-1]
        regular_N_s = np.arange(startpoint, endpoint + 1, 50)
        fitted_phr = polynomial.polyval2d(np.ones(len(regular_N_s)) * vanes, regular_N_s, get_phr_coeffs())
        plt.plot(regular_N_s, fitted_phr, 'g-')

    # plot limit of data
    fitted_limit_Ns = np.polyval(get_Ns_limit_coeffs(), get_vanes())
    fitted_limit_phr = polynomial.polyval2d(get_vanes(), fitted_limit_Ns, get_phr_coeffs())
    plt.plot(fitted_limit_Ns, fitted_limit_phr)

    plt.gca().set_xticks(np.arange(0, endpoint + 1, 400))
    plt.gca().set_yticks(np.arange(0, 65, 5))
    plt.grid()
    plt.show()
