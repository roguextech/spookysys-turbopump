import passes.empirical.lobanoff.impeller.head_rise
import passes.empirical.lobanoff.impeller.head_constant
import passes.empirical.lobanoff.impeller.capacity_constant
from helpers import *

from passes.empirical.lobanoff import impeller


#impeller.generate()

#exit

vanes = 5
n = 90000 # rpm
Q = 25 # l/s
H = bar_to_head_m(25) # m

impeller.generate(vanes=vanes, n=n, Q=lps_to_gpm(Q), H=m_to_ft(H))

# impeller.generate(vanes=5, n=3600, Q=2100, H=450)

