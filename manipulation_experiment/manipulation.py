import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import time
import copy
import algos
import sys

def valid_ranked_reviewers_for_all_papers():
    result = []
    
    for paper in range(d):
        naive_ranked_reviewers = np.argsort(S[:, paper])
        reversed_reviewers = np.flip(naive_ranked_reviewers)
        
        valid_ranked_reviewers = []
        for reviewer in reversed_reviewers:
            if M[reviewer][paper] == 0:
                valid_ranked_reviewers.append(reviewer)
        result.append(valid_ranked_reviewers)

        for i in range(len(valid_ranked_reviewers) - 1):
            assert(S[valid_ranked_reviewers[i], paper] >= S[valid_ranked_reviewers[i+1], paper])

        
    return np.array(result, dtype=object)


def valid_ranked_papers_for_all_reviewers():
    result = []
    
    for rev in range(n):
        naive_ranked_paps = np.argsort(S[rev, :])
        reversed_paps = np.flip(naive_ranked_paps) # papers in high to low sim order
        
        valid_ranked_paps = []
        for pap in reversed_paps:
            if M[rev][pap] == 0:
                valid_ranked_paps.append(pap)
        result.append(valid_ranked_paps)

        for j in range(len(valid_ranked_paps) - 1):
            assert(S[rev, valid_ranked_paps[j]] >= S[rev, valid_ranked_paps[j+1]])

        
    return np.array(result, dtype=object)



def random_honest_bids(S_new, manipulator):
    def do_rev_bids(rev, p, pap_frac):
        for pap in ranked_papers[rev][0:int(pap_frac * d)]:
            z = np.random.rand()
            if z < p/pap_frac:
                if np.random.rand() < 0.5:
                    S_new[rev][pap] *= bidding_scale
                else:
                    S_new[rev][pap] /= bidding_scale

    p_high = 0.024
    p_low = 0.0016
    n_high = int(0.3 * n)
    n_low = int(0.5 * n)
    pap_frac = 0.1
    shuffled_revs = np.arange(n)
    np.random.shuffle(shuffled_revs)
    for rev in shuffled_revs[0:n_high]:
        if rev != manipulator:
            do_rev_bids(rev, p_high, pap_frac)
    for rev in shuffled_revs[n_high:(n_high + n_low)]:
        if rev != manipulator:
            do_rev_bids(rev, p_low, pap_frac)

'''
def run_TPMS_assignment_with_test(new_S, paper, manipulator):
    try:
        model = gp.Model("my_model") 
        obj = 0 #objective is the total sum similarity
        A = [([0] * d) for i in range(n)] #A represents assignment
        
        for i in range(n):
            for j in range(d):
                
                if (M[i][j] == 1):
                    v = model.addVar(lb = 0, ub = 0, name = f"{i} {j}")
                else:
                    v = model.addVar(lb = 0, ub = 1, name = f"{i} {j}")
                
                A[i][j] = v
                obj += v * new_S[i][j]
        
        model.setObjective(obj, GRB.MAXIMIZE) #telling Gurobi to maximize obj
        
        for i in range(n):
            papers = 0
            for j in range(d):
                papers += A[i][j]
            model.addConstr(papers <= k) #each reviewer has k or less papers to review
        
        for j in range(d):
            reviewers = 0
            for i in range(n):
                reviewers += A[i][j]
            model.addConstr(reviewers == l) #each paper gets exactly l reviews
        
        model.optimize()
        
        return A[manipulator][paper].x
    
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
    except AttributeError:
        print("Attribute error")
'''


def main():
    y_of_xs = []
    values = []
    num_trials = len(mani_values * num_selections)
    paper_selectionss = []
    count = 0
    for x in (mani_values):
        successful_assignments = []
        
        paper_selections = np.random.choice(d, num_selections, replace = False)
        paper_selectionss.append(paper_selections)
        for paper in paper_selections:
            count += 1
            print(f"{count}/{num_trials}")
            manipulator = ranked_reviewers[paper][x]
            
            new_S = np.array(S)
            '''
            for i in range(n):
                if i == manipulator:
                    new_S[i][paper] *= bidding_scale
                else:
                    new_S[i][paper] /= bidding_scale
            '''
            for j in range(d):
                if j == paper:
                    new_S[manipulator][j] *= bidding_scale
                else:
                    new_S[manipulator][j] /= bidding_scale

            if honest_bids:
                random_honest_bids(new_S, manipulator)
            
            if baseline:
                successful_assignments.append(algos.standard_assignment(new_S, M, paper, manipulator, k, l))
            else:
                successful_assignments.append(algos.our_assignment(new_S, M, paper, manipulator, k, l))
        y_of_x = sum(successful_assignments)/num_selections
        print("x", x, "rate", y_of_x)
        y_of_xs.append(y_of_x)
        values.append(successful_assignments)
    
    
##PLOTTING
    plt.plot(mani_values, y_of_xs)
    plt.xlabel("xth best reviewer")
    plt.ylabel("fraction of asssignments assigned")
    plt.savefig(f"{mani_values[0]}-{mani_values[-1]}_manipulation_baseline{baseline}_honestbids{honest_bids}_scale{bidding_scale}")
    plt.clf()
    
    time_taken = time.time() - start_time
    print(f"Total time: {time_taken}")
    
##SAVING
    title = f"{mani_values[0]}-{mani_values[-1]}_manipulation_baseline{baseline}_honestbids{honest_bids}_scale{bidding_scale}_" + str(time.time())
    
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

k = 6
l = 3
dataset = "iclr2018.npz"

mani_values = [0, 2, 4, 8, 16, 32, 50, 100, 150, 200, 300, 400]
num_selections = 20
bidding_scale = 2
#the following block is referenced from github.com/xycforgithub/StrategyProof_Conference_Review
scores = np.load(dataset)
S = scores["similarity_matrix"]
M = scores["mask_matrix"] #each entry is 0 or 1, with 1 representing a conflict.

n = len(S) #number of reviewers
d = len(S[0]) #number of papers


baseline = (sys.argv[1] == 'standard')
honest_bids = (sys.argv[2] == 'bids')
print("baseline", baseline, "honest_bids", honest_bids)

ranked_reviewers = valid_ranked_reviewers_for_all_papers()
ranked_papers = valid_ranked_papers_for_all_reviewers()

main()
