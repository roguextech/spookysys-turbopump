print(__name__)
from . import DATA as IMPELLER_DATA
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

DATA = IMPELLER_DATA["head_rise"]


def _init():
    for datum in DATA:
        N_s, phr = np.transpose(datum["data"]).tolist()
        extrap = 400
        startpoint = N_s[0] - extrap
        endpoint = N_s[-1] + extrap
        regular_N_s = np.arange(startpoint, endpoint + 1, 200)
        regular_phr = interp1d(N_s, phr, fill_value="extrapolate")(regular_N_s)
        datum["fit"] = np.polyfit(regular_N_s, regular_phr, 7)


def _plot_data():
    for datum in DATA:
        N_s, phr = np.transpose(datum["data"]).tolist()
        startpoint = N_s[0]
        endpoint = N_s[-1]
        regular_N_s = np.arange(startpoint, endpoint + 1, 50)
        fitted_phr = np.polyval(datum["fit"], regular_N_s)
        label = str(datum["vanes"]) + " vanes, " \
            + str(datum["discharge_angle"]) + " deg" \
            + (", droop" if datum["droop"] else "")
        label_xy = (N_s[-1], phr[-1])
        plt.plot(regular_N_s, fitted_phr, 'g--', label=label)
        plt.annotate(label, xy=label_xy)
    plt.gca().set_xticks(np.arange(0, endpoint + 1, 400))
    plt.gca().set_yticks(np.arange(0, 65, 5))
    plt.grid()
    plt.show()


def get_percent_head_rise(vanes, N_s):
    tmp = next(x for x in DATA if x["vanes"] == vanes)
    return np.polyval(tmp["fit"], N_s)


def get_discharge_angle(vanes):
    tmp = next(x for x in DATA if x["vanes"] == vanes)
    return tmp["discharge_angle"]


def get_droop(vanes):
    tmp = next(x for x in DATA if x["vanes"] == vanes)
    return tmp["droop"]


_init()
_plot_data()
