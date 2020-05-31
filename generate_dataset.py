import numpy as np

def generate_concentrated_expertise_dataset():
    numrev = 100
    numpap = 100
    S = np.zeros((numrev, numpap))
    for i in range(numpap):
        good_revs = np.random.choice(numrev, 6) # only 6 good per pap
        for x in good_revs:
            S[x, i] = 1
    M = np.zeros((numrev, numpap))
    np.savez("concentrated_expertise_dataset.npz", similarity_matrix=S.tolist(), mask_matrix=M.tolist())

generate_concentrated_expertise_dataset()
