print(__name__)
from . import DATA as IMPELLER_DATA
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

DATA = IMPELLER_DATA["head_constant"]


def _init():
    for datum in DATA:
        N_s, K_u = np.transpose(datum["data"]).tolist()
        datum["fit"] = np.polyfit(N_s, K_u, 1)


def _plot_data():
    for datum in DATA:
        N_s, K_u = np.transpose(datum["data"]).tolist()
        fitted_N_s = np.linspace(0, 3600)
        fitted_K_u = np.polyval(datum["fit"], fitted_N_s)
        label = str(datum["vanes"]) + " vanes"
        label_xy = (2000, np.polyval(datum["fit"], 2000))
        plt.plot(fitted_N_s, fitted_K_u, 'g--', 
                 N_s, K_u, 'ro',
                 label=label)
        plt.annotate(label, xy=label_xy)
    plt.gca().set_xticks(np.arange(0, 3601, 400))
    plt.grid()
    plt.show()


def get_K_u(vanes, N_s):
    tmp = next(x for x in DATA if vanes in x["vanes"])
    return np.polyval(tmp["fit"], N_s)


_init()
#_plot_data()

