import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import time
import copy
import algos
import sys

# Modify S_new by adding bids from all honest reviewers
def random_honest_bids(S_new, manipulator):
    def do_rev_bids(rev, p, pap_frac): # add bids for rev
        for pap in ranked_papers[rev][0:int(pap_frac * d)]:
            z = np.random.rand()
            if z < p/pap_frac: # probability of bidding
                if np.random.rand() < 0.5:
                    S_new[rev][pap] *= bidding_scale
                else:
                    S_new[rev][pap] /= bidding_scale

    # overall probability of bidding on each paper by group
    p_high = 0.024
    p_low = 0.0016
    # number of revs in each group
    n_high = int(0.3 * n)
    n_low = int(0.5 * n)
    # frac of papers each rev considers
    pap_frac = 0.1
    shuffled_revs = np.arange(n)
    np.random.shuffle(shuffled_revs)
    for rev in shuffled_revs[0:n_high]:
        if rev != manipulator:
            do_rev_bids(rev, p_high, pap_frac)
    for rev in shuffled_revs[n_high:(n_high + n_low)]:
        if rev != manipulator:
            do_rev_bids(rev, p_low, pap_frac)

def main():
    y_of_xs = []
    values = []
    num_trials = len(mani_values * num_selections)
    paper_selectionss = []
    count = 0
    for x in (mani_values):
        successful_assignments = []
        
        # Choose papers for manipulator to target
        paper_selections = np.random.choice(d, num_selections, replace = False)
        paper_selectionss.append(paper_selections)
        for paper in paper_selections:
            count += 1
            print(f"{count}/{num_trials}")
            # Get xth ranked reviewer to be the manipulator
            manipulator = ranked_reviewers[paper][x]
            
            new_S = np.array(S)

            # Manipulator bids
            if manip_bids:
                for j in range(d):
                    if j == paper:
                        new_S[manipulator][j] *= bidding_scale
                    else:
                        new_S[manipulator][j] /= bidding_scale

            if honest_bids:
                random_honest_bids(new_S, manipulator)
            
            # Run assignment
            if baseline:
                successful_assignments.append(algos.standard_assignment(new_S, M, paper, manipulator, k, l))
            else:
                successful_assignments.append(algos.our_assignment(new_S, M, paper, manipulator, k, l))
        y_of_x = sum(successful_assignments)/num_selections
        print("x", x, "rate", y_of_x)
        y_of_xs.append(y_of_x)
        values.append(successful_assignments)

        # save in case of crash
        np.savez("temp_save", \
        mani_values = mani_values, \
        num_selections = num_selections, \
        paper_selectionss = paper_selectionss, \
        k = k, \
        l = l, \
        y_of_xs = y_of_xs, \
        values = values, \
        bidding_scale = bidding_scale)
 
    
    t = int(time.time())
    time_taken = time.time() - start_time
    print(f"Total time: {time_taken}")
    
    # Save data
    title = f"{mani_values[0]}-{mani_values[-1]}_manipulation_baseline{baseline}_honestbids{honest_bids}_scale{bidding_scale}_trials{num_selections}_manip{manip_bids}_" + str(t)
    
    np.savez(title, \
    mani_values = mani_values, \
    num_selections = num_selections, \
    paper_selectionss = paper_selectionss, \
    k = k, \
    l = l, \
    dataset = dataset, \
    y_of_xs = y_of_xs, \
    time_taken = time_taken, \
    values = values, \
    bidding_scale = bidding_scale)
    
    print("Saving complete!")


start_time = time.time()

# rev+pap loads
k = 6
l = 3

dataset = "../data/iclr2018.npz"

# Ranks of the reviewers' similarities wrt the target paper,
# roughly logspaced
# 2**i - 1: [0, 1, 3, 7, 15, 31, 63, 127, 255, 511]
# int(2**(i.5)) - 1: [0, 1, 4, 10, 21, 44, 89, 180, 361] 
mani_values = [0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 2, 4, 10, 21, 44, 89, 180, 361]

num_selections =50 # number of trials per mani_value

# The following block is referenced from github.com/xycforgithub/StrategyProof_Conference_Review
scores = np.load(dataset)
S = scores["similarity_matrix"]
M = scores["mask_matrix"] #each entry is 0 or 1, with 1 representing a conflict.

n = len(S) #number of reviewers
d = len(S[0]) #number of papers

# Parse command line args
baseline = (sys.argv[1] == 'standard')
honest_bids = (sys.argv[2] == 'bids')
bidding_scale = int(sys.argv[3])
manip_bids = True
if len(sys.argv) == 5 and sys.argv[4] == "nomanip":
    manip_bids = False
print("baseline", baseline, "honest_bids", honest_bids, "scale", bidding_scale, "manip", manip_bids)

# Sort revs and paps
ranked_reviewers = algos.valid_ranked_reviewers_for_all_papers(S, M)
ranked_papers = algos.valid_ranked_papers_for_all_reviewers(S, M)

main()
