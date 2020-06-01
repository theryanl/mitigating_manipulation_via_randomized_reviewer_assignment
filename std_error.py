import numpy as np

def calculate_standard_error(samples, mean, n):
    samples = np.array(samples)
    if n > 1:
        x = np.sqrt(np.sum(np.square(samples - mean)) / (n * (n - 1)))
    elif n == 1:
        x = np.sqrt(np.sum(np.square(samples - mean))) # biased
    else:
        x = -1 # invalid
    return x
