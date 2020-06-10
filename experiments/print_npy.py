import numpy as np
import sys

# Convenience file to print the contents of a .npy

fname = sys.argv[1]
x = np.load(fname, allow_pickle=True)
print(x)
