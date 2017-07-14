print(__name__)
import numpy as np

# n is rounds per minute
# Q is volume_flow (US: GPM, metric: l/s)
# H is head (US: ft, metric: m)
def get_specific_speed(n, Q, H):
    return n * np.sqrt(Q) / np.power(H, 0.75)

