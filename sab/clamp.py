
import numpy as np

def clamp(x, lim):
    return np.clip(x, -lim, lim)
