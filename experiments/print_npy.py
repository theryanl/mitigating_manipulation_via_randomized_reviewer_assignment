import numpy as np
import sys

fname = sys.argv[1]
x = np.load(fname, allow_pickle=True)
print(x)
