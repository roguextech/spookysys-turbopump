print(__name__)
from . import DATA as IMPELLER_DATA
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

DATA = IMPELLER_DATA["head_rise"]


def _init():
    for datum in DATA:
        N_s, percent_head_rise = np.transpose(datum["data"]).tolist()
        datum["fit"] = np.polyfit(N_s, percent_head_rise, 4)


def _plot_data():
    for datum in DATA:
        N_s, percent_head_rise = np.transpose(datum["data"]).tolist()
        fitted_N_s = np.arange(0, N_s[-1]+1000, 100)
        fitted_vals = np.polyval(datum["fit"], fitted_N_s)
        label = str(datum["vanes"]) + " vanes, " \
            + str(datum["discharge_angle"]) + " deg" \
            + (", droop" if datum["droop"] else "")
        label_xy = (N_s[-1], percent_head_rise[-1])
        plt.plot(fitted_N_s, fitted_vals, 'g--',
                 N_s, percent_head_rise, 'r',
                 label=label)
        plt.annotate(label, xy=label_xy)
    plt.gca().set_xticks(np.arange(0, 3601, 400))
    plt.gca().set_yticks(np.arange(0, 65, 5))
    plt.grid()
    plt.show()


def get(vanes, N_s):
    tmp = next(x for x in DATA if x["vanes"] == vanes)
    return np.polyval(tmp["fit"], N_s)


_init()
_plot_data()
