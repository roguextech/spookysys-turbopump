import empirical.lobanoff.impeller.head_rise
import empirical.lobanoff.impeller.head_constant
import empirical.lobanoff.impeller.capacity_constant
from empirical.lobanoff import impeller
from helpers import *

# Note: Potassium permanganate activated alumina balls are cheap
# -> just run the h2o2 thru a long tube of these and screw poison


# Note Q in lps
def evaluate_pump(n, Q, P):
    H = bar_to_m(P) # m

    # specific speeds
    n_q = get_specific_speed(n=n, Q=l_to_m3(Q), H=H, double_entry=False)
    N_s = get_specific_speed(n=n, Q=lps_to_gpm(Q), H=m_to_ft(H), double_entry=False)

    print("speed: n =", n, "[rpm] aw =", int(rpm_to_aw(n)), "[rad/s]")
    print("flow:", round(Q, 2), "[lps]", int(lps_to_gpm(Q)), "[gpm]")
    print("head:", int(H), "[m]", int(m_to_ft(H)), "[ft]")
    print("specific speed: n_q =", round(n_q, 2), " N_s =", int(N_s))


print()
print("Purdue fuel pump")
evaluate_pump(n=90000, Q=m3_to_l(lb_to_kg(3.3)/800), P=psi_to_bar(4496))

print()
print("Purdue oxidizer pump")
evaluate_pump(n=90000, Q=m3_to_l(lb_to_kg(17.6)/1400), P=psi_to_bar(5946))

print()
print("Spica proposal:")
evaluate_pump(n=30000, Q=25, P=25)

# turbine 
# omega_s should be 0.6 for best efficiency of n_ts=87%
# omega_s high limit is 1.0 which leaves velocity in flow
