print(__name__)
from . import DATA as IMPELLER_DATA
import scipy as sp
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

DATA = IMPELLER_DATA["head_rise"]


def _init():
    for iter in DATA:
        n_s, percent_head_rise = np.transpose(iter["data"]).tolist()
        iter["fit"] = np.polyfit(n_s, percent_head_rise, 4)


def _plot_data():
    for data in DATA:
        n_s, percent_head_rise = np.transpose(data["data"]).tolist()
        fitted_n_s = np.arange(0, n_s[-1]+1000, 100)
        fitted_vals = np.polyval(data["fit"], fitted_n_s)
        label = str(data["vanes"]) + " vanes, " \
            + str(data["discharge_angle"]) + " deg" \
            + (", droop" if data["droop"] else "")
        label_xy = (n_s[-1], percent_head_rise[-1])
        plt.plot(fitted_n_s, fitted_vals, 'g--', 
                 n_s, percent_head_rise, 'r',
                 label=label)
        plt.annotate(label, xy=label_xy)
    plt.grid()
    plt.show()


def get(vanes, n_s):
    tmp = next(x for x in DATA if x["vanes"] == vanes)
    return np.polyval(tmp["fit"], n_s)


_init()
_plot_data()
