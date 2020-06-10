import numpy as np
import random
from institution_generator import *

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

# Generates a community model simulation, where there are k
# good reviewers (chosen deterministically)
def generate_deterministic_concentrated_expertise_dataset(n, k):
    S = np.zeros((n, n))
    for i in range(0, n, k):
        stop = min(i+k, n)
        S[i:stop, i:stop] = 1
    M = np.zeros((n, n))
    np.savez("det_concentrated_expertise_dataset.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

# As above, but each group has an institution
def generate_dced_with_inst(n, k):
    generate_deterministic_concentrated_expertise_dataset(n, k)
    write_sequential_institutions(n, k)

# 50 reviewers are good for all papers, rest are okay for 5 papers
def generate_good_reviewers_sim():
    numrev = 100
    numpap = 100
    S = np.zeros((numrev, numpap))
    S[:50, :] = 1
    for i in range(50):
        start = (i*2)
        if start + 5 > 100: # loops around
            end = start+5-100
            good_paps = list(range(start, 100)) + list(range(0, end))
        else:
            good_paps = range(start, start+5)
        for x in good_paps:
            S[50+i, x] = 0.5
    M = np.zeros((numrev, numpap))
    np.savez("good_revs.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

# 50 papers are good for all revs, rest are okay for half revs
def generate_good_papers_sim():
    numrev = 100
    numpap = 100
    S = np.zeros((numrev, numpap))
    S[:, :50] = 1
    for i in range(50):
        start = (i*2)
        if start + 5 > 100: # loops around
            end = start-5
            good_revs = list(range(start, 100)) + list(range(0, end))
        else:
            good_revs = range(start, start+5)
        for x in good_revs:
            S[x, 50+i] = 0.5
    M = np.zeros((numrev, numpap))
    np.savez("good_paps.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

# Square similarity matrix uniformly in [0, 1)
def generate_random(n):
    S = np.random.rand(n, n)
    M = np.zeros((n, n))
    np.savez("rand.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

