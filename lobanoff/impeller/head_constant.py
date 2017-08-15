"""Figure 3-3: Head Constant Ku [US]"""
from __future__ import print_function
from itertools import chain
import numpy as np
from matplotlib import pyplot as plt
from misc import memoized
from . import _jsondata as _module_jsondata


def _jsondata():
    return _module_jsondata()['head_constant']


@memoized
def get_vanes():
    """Return the number of vanes for which there is data"""
    vanes = chain.from_iterable([x['vanes'] for x in _jsondata()])
    return sorted(vanes)


@memoized
def get_coeffs():
    points = [x['points'] for x in _jsondata()]
    slope = np.average([(x[1][1] - x[0][1]) / (x[1][0] - x[0][0]) for x in points])
    offsets = [x[0][1] - slope * x[0][0] for x in points]

    vanes = [x['vanes'] for x in _jsondata()]
    offsets_expanded = [[x] * len(y) for x, y in zip(offsets, vanes)]
    offsets_expanded = list(chain.from_iterable(offsets_expanded))
    vanes_expanded = list(chain.from_iterable(vanes))
    coeffs = np.polyfit(vanes_expanded, offsets_expanded, 2)

    return (coeffs, slope)


def plot():
    offset_coeffs, slope = get_coeffs()

    for vanes in get_vanes():
        offset = np.polyval(offset_coeffs, vanes)
        space_Ns = np.arange(0, 3600 + 1, 400)
        fitted_Ku = offset + slope * space_Ns
        plt.plot(space_Ns, fitted_Ku)
        label = str(vanes)
        label_xy = (space_Ns[-1], fitted_Ku[-1])
        plt.annotate(label, xy=label_xy)

    plt.gca().set_title(__doc__)
    plt.gca().set_xticks(np.arange(0, 3600 + 1, 400))
    plt.gca().set_yticks(np.arange(0.7, 1.3, 0.05))
    plt.xlabel('Ns - Specific Speed')
    plt.ylabel('Ku - Head Constant')
    plt.grid()
    plt.show()
