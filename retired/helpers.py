import numpy as np

# n is rounds per minute
# Q is volume_flow (US: GPM, metric: l/s)
# H is head (US: ft, metric: m)


def get_specific_speed(n, Q, H, double_entry=False, stages=1):
    f_q = 2 if double_entry else 1
    H_st = H / stages
    return n * np.sqrt(Q / f_q) / np.power(H_st, 0.75)


GRAVITY = 9.81


def lps_to_gpm(Q):
    return Q * 15.8503231


def gpm_to_lps(Q):
    return Q / 15.8503231


def m3ps_to_gpm(Q):
    return lps_to_gpm(m3_to_l(Q))


def gpm_to_m3ps(Q):
    return l_to_m3(gpm_to_lps(Q))


def bar_to_m(pressure, density=1000):
    force_per_m2 = pressure * 100000
    mass_per_m2 = force_per_m2 / GRAVITY
    return mass_per_m2 / density


def m_to_bar(head, density=1000):
    mass_per_m2 = head * density
    force_per_m2 = mass_per_m2 * GRAVITY
    return force_per_m2 / 100000


def m_to_ft(s):
    return s * 3.2808399


def ft_to_m(s):
    return s / 3.2808399


def rpm_to_aw(n):
    return n * np.pi * 2 / 60


def lb_to_kg(mass):
    return mass / 2.20462262


def psi_to_bar(pressure):
    return pressure / 14.5037738


def l_to_m3(volume):
    return volume / 1000


def m3_to_l(volume):
    return volume * 1000

# HOT FACT:
# g is acceleration: m/s^2
# g is also force per kilo: N/kg


# HOT FACT:
# pressure is force per area: N/m^2
# pressure is also energy per volume: J/m^3
