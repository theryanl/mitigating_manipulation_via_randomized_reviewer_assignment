import numpy as np

def get_paper_totals(filename, my_dataset):
    # reads a fractional assignment matrix in from filename and calculates
    # the total expected similarity weight on each paper
    scores = np.load(my_dataset, allow_pickle=True)
    S = scores["similarity_matrix"]

    f = open(filename, "r")
    rp = f.readline().split(' ')
    numrev, numpap = int(rp[0]), int(rp[1])
    paper_totals = np.zeros(numpap)
    for line in f:
        rp = line.split(' ')
        w = float(rp[2])
        r = int(rp[0])
        p = int(rp[1]) - numrev
        paper_totals[p] += (w * S[r, p])
    f.close()
    return paper_totals

