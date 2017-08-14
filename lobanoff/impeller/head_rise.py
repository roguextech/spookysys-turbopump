"""Head Rise Figure"""
import scipy as sp
import itertools
from numpy.polynomial.polynomial import polyval2d
from scipy.interpolate import interp2d
import numpy as np
from matplotlib import pyplot as plt
from itertools import chain
from pprint import pprint
from misc import mem
from . import JSONDATA as JSONDATA_IMPELLER


def polyfit2d(x, y, z, order=3):
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order + 1), range(order + 1))
    for k, (i, j) in enumerate(ij):
        G[:, k] = x**i * y**j
    m, _, _, _ = np.linalg.lstsq(G, z)
    return m.reshape([order+1,order+1])


#@mem.cache
def _prepare(jsondata):
    fitdata = [
        [np.ones(len(x['data'])) * x['vanes'] for x in jsondata],
        [np.transpose(x['data'])[0] for x in jsondata],
        [np.transpose(x['data'])[1] for x in jsondata]
    ]
    fitdata = np.array([list(chain.from_iterable(x)) for x in fitdata])
    fit = polyfit2d(*fitdata, order=3)
    return {
        'fit': fit
    }


_DATA = _prepare(JSONDATA_IMPELLER['head_rise'])


def plot():
    for datum in JSONDATA_IMPELLER['head_rise']:
        vanes = datum['vanes']
        N_s, phr = np.transpose(datum["data"]).tolist()
        startpoint = N_s[0]
        endpoint = N_s[-1]
        label = str(datum["vanes"]) + " vanes, " \
            + str(datum["discharge_angle"]) + " deg" \
            + (", droop" if datum["droop"] else "")
        label = '.'
        label_xy = (N_s[-1], phr[-1])
        plt.plot(N_s, phr, 'r--')

    for datum in JSONDATA_IMPELLER['head_rise']:
        vanes = datum['vanes']
        N_s, phr = np.transpose(datum["data"]).tolist()
        startpoint = N_s[0]
        endpoint = N_s[-1]
        regular_N_s = np.arange(startpoint, endpoint + 1, 50)
        fitted_phr = polyval2d(np.ones(len(regular_N_s))*vanes, regular_N_s, _DATA['fit'])
        plt.plot(regular_N_s, fitted_phr, 'g-')

#        plt.annotate(label, xy=label_xy)
    plt.gca().set_xticks(np.arange(0, endpoint + 1, 400))
    plt.gca().set_yticks(np.arange(0, 65, 5))
    plt.grid()
    plt.show()


# def get_percent_head_rise(vanes, N_s):
#     tmp = next(x for x in DATA if x["vanes"] == vanes)
#     return np.polyval(tmp["fit"], N_s)


# def get_discharge_angle(vanes):
#     tmp = next(x for x in DATA if x["vanes"] == vanes)
#     return tmp["discharge_angle"]


# def get_droop(vanes):
#     tmp = next(x for x in DATA if x["vanes"] == vanes)
#     return tmp["droop"]


# _init()
# _plot_data()
