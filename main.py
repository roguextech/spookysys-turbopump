import passes.empirical.lobanoff.impeller.head_rise
import passes.empirical.lobanoff.impeller.head_constant
import passes.empirical.lobanoff.impeller.capacity_constant
from passes.empirical.lobanoff import impeller
from helpers import *



# specs
n = 90000 # rpm
Q = 25 # l/s
H = bar_to_m(25) # m

# specific speeds
n_q = get_specific_speed(n=n, Q=Q, H=H)
N_s = get_specific_speed(n=n, Q=lps_to_gpm(Q), H=m_to_ft(H))


print("speed: n =", n, "[rpm] aw =", int(rpm_to_aw(n)), "[rad/s]")
print("flow:", Q, "[lps]", int(lps_to_gpm(Q)), "[gpm]")
print("head:", int(H), "[m]", int(m_to_ft(H)), "[ft]")
print("specific speed: n_q =", int(n_q), " N_s =", int(N_s))

