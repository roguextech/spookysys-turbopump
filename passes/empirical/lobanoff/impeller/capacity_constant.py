print(__name__)
from . import DATA as IMPELLER_DATA
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

DATA = IMPELLER_DATA["capacity_constant"]


def _init():
    for datum in DATA:
        N_s, K_m2 = np.transpose(datum["data"]).tolist()
        datum["fit"] = np.polyfit(N_s, K_m2, 2)


def _plot_data():
    for datum in DATA:
        N_s, K_m2 = np.transpose(datum["data"]).tolist()
        fitted_N_s = np.arange(400, N_s[-1]+400, 100)
        fitted_K_m2 = np.polyval(datum["fit"], fitted_N_s)
        label = str(datum["vanes"]) + " vanes"
        label_xy = (N_s[-1], K_m2[-1])
        plt.plot(fitted_N_s, fitted_K_m2, 'g--',
                 N_s, K_m2, 'r',
                 label=label)
        plt.annotate(label, xy=label_xy)
    plt.gca().set_xticks(np.arange(0, 3601, 400))
    plt.gca().set_yticks(np.arange(0, .26, .02))
    plt.grid()
    plt.show()


def get_K_m2(vanes, N_s):
    tmp = next(x for x in DATA if vanes in x["vanes"])
    return np.polyval(tmp["fit"], N_s)


_init()
#_plot_data()
