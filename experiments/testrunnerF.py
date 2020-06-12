import sys
import os
import numpy as np
import time
from get_paper_totals import get_paper_totals
from std_error import calculate_standard_error 
from get_dataset_name import get_dataset_name
from generate_dataset import *

# Runs the test that varies Q and checks the sum-sim objective, on random 100x100 similarities

# fixed parameters
num_trials = 10
my_dataset = "rand.npz"
k = 3
l = 3
size = 100

os.system("g++ -lm ../core/bvn.cpp") #compiles the bvn portion

Q_values = []
Q_results = []
Q_stderrs = []

for Q in range(10, 110, 10): #loops through Q values (multiplied by 100)
    Q_values.append(Q/100)
    print(f"running Q = {Q/100}...")
    
    scores = []
    feas = True
    for i in range(num_trials):
        generate_random(size)

        Q_result = os.popen(f"python3 ../core/LP_TPMS.py {my_dataset} 0 {Q} 0 {k} {l}")
        lines = Q_result.readlines()
        try:
            TPMS_score = float(lines[-2]) #the objective value in the string output
            print("actual", TPMS_score)
        except ValueError:
            TPMS_score = -1
    
        if TPMS_score != -1: # if feasible
                os.system("./a.out < output.txt > output_bvn.txt")
                bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
                x = float(bvn_result.readline())
                scores.append(x)
        else: # infeas, skip to next
            feas = False
            break 
 
    if feas:
        #getting the avg and stderr
        s = sum(scores) / num_trials
        Q_results.append(s)
        Q_stderrs.append(calculate_standard_error(scores, s, num_trials))
        print("estimate:", s)
    else:
        s = -1 # signal infeasible
        Q_results.append(s)
        Q_stderrs.append(s)
  
print("Q_values:", Q_values)
print("Q_results:", Q_results)
print("Q_stderrs:", Q_stderrs)

name = "F.npy"
opt = Q_results[-1]
np.save(name, [Q_values, np.array(Q_results)/opt, np.array(Q_stderrs)/opt]) #saves as npy file
