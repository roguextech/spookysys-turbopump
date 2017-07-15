import numpy as np

# n is rounds per minute
# Q is volume_flow (US: GPM, metric: l/s)
# H is head (US: ft, metric: m)


def get_specific_speed(n, Q, H):
    return n * np.sqrt(Q) / np.power(H, 0.75)


GRAVITY = 9.81


def lps_to_gpm(Q):
    return Q * 15.8503231


def gpm_to_lps(Q):
    return Q / 15.8503231


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


# HOT FACT:
# g is acceleration: m/s^2
# g is also force per kilo: N/kg


# HOT FACT:
# pressure is force per area: N/m^2
# pressure is also energy per volume: J/m^3
