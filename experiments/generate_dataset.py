import numpy as np
import random

# Generates a simulation where there are 6 good reviewers per paper, chosen
# at random
def generate_concentrated_expertise_dataset():
    numrev = 100
    numpap = 100
    S = np.zeros((numrev, numpap))
    for i in range(numpap):
        good_revs = random.sample(range(numrev), 6) # only 6 good per pap
        for x in good_revs:
            S[x, i] = 1
    print(S)
    M = np.zeros((numrev, numpap))
    np.savez("concentrated_expertise_dataset.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

# Generates a community model simulation, where there are 6
# good reviewers (chosen deterministically)
def generate_deterministic_concentrated_expertise_dataset(n):
    S = np.zeros((n, n))
    for i in range(0, n, 6):
        stop = min(i+6, n)
        S[i:stop, i:stop] = 1
    M = np.zeros((n, n))
    np.savez("det_concentrated_expertise_dataset.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

