print(__name__)
from .. import DATA as BOOK_DATA
import helpers

DATA = BOOK_DATA["impeller"]



def generate(vanes, n, Q, H):
    print("gpm: ", Q)
    print("head: ", H, "ft")
    N_s = helpers.get_specific_speed(n=n, Q=Q, H=H)
    print("N_s: ", N_s)

