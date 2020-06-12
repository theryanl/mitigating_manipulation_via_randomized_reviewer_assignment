import sys
import os
import numpy as np
import time
from generate_dataset import generate_deterministic_concentrated_expertise_dataset
from std_error import calculate_standard_error

# This file runs an experiment on the community model simulation over a varying group size and varying Q

# fixed parameters for this experiment
k = 3
l = 3
num_trials = 10
group_sizes = [3, 6, 9, 12]
Q_values = np.linspace(0.1, 1, num=10)
numpap = 360

total_results = []
total_stderrs = []

os.system("g++ -lm ../core/bvn.cpp") #compiles the bvn portion

for gs in group_sizes:
    Q_results = []
    Q_stderrs = []
    for Q in Q_values:
        Q = int(Q * 100)
        print(gs, Q)
        # generate the community model
        generate_deterministic_concentrated_expertise_dataset(numpap, gs)
            
        Q_result = os.popen(f"python3 ../core/LP_TPMS.py det_concentrated_expertise_dataset.npz 0 {Q} 0 {k} {l}")
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
            Q_results.append(s)
            print(s, scores)
            Q_stderrs.append(calculate_standard_error(scores, s, num_trials))
        else:
            s = -1 # signal infeasible
            Q_results.append(s)
            Q_stderrs.append(s)
    opt = Q_results[-1]
    total_results.append(np.array(Q_results)/opt)
    total_stderrs.append(np.array(Q_stderrs)/opt) 
     
print("results:", total_results)
print("stderrs:", total_stderrs)
name = "D.npy"
np.save(name, [group_sizes, Q_values, total_results, total_stderrs])
