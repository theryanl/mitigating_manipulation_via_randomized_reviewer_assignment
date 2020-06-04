import sys
import os
import numpy as np
import time
from generate_dataset import generate_deterministic_concentrated_expertise_dataset
from std_error import calculate_standard_error

# This file runs an experiment on the community model dataset over a varying number of papers

k = 3
l = 3
Q = 50
num_trials = 10

pap_values = np.logspace(0, 7, num=8, base=2) * 10
Q_results = []
Q_stderrs = []

os.system("g++ -lm ../core/bvn.cpp") #compiles the bvn portion

for numpap in pap_values:
    print("numpap", numpap)
    # generate the community model
    generate_deterministic_concentrated_expertise_dataset(int(numpap))

    optr = os.popen(f"python3 ../core/LP_TPMS.py det_concentrated_expertise_dataset.npz 100 {k} {l}")
    opt = (optr.readlines())[-2]
    opt = float(opt)
    print("opt", opt)
        
    Q_result = os.popen(f"python3 ../core/LP_TPMS.py det_concentrated_expertise_dataset.npz {Q} {k} {l}")
    lines = Q_result.readlines()
    try:
        TPMS_score = float(lines[-2]) #the objective value
        print("actual", TPMS_score)
    except ValueError:
        TPMS_score = -1
 
    if TPMS_score != -1: # if feasible
        scores = []
        for i in range(num_trials):
            os.system("./a.out < output.txt > output_bvn.txt")
            bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py det_concentrated_expertise_dataset.npz output_bvn.txt")
            x = float(bvn_result.readline())
            scores.append(x)
        s = sum(scores) / num_trials
        Q_results.append(s/opt)
        print(s, scores)
        Q_stderrs.append(calculate_standard_error(scores, s, num_trials)/opt)
        print("estimate:", s)
    else:
        s = -1 # signal infeasible
        Q_results.append(s)
        Q_stderrs.append(s)
 
     
print("Q_results:", Q_results)
print("Q_stderrs:", Q_stderrs)
name = "D.npy"
np.save(name, [pap_values, Q_results, Q_stderrs])

