import sys
import os
import numpy as np
import time
from generate_dataset import generate_deterministic_concentrated_expertise_dataset
from std_error import calculate_standard_error

k = 3
l = 3
Q = 50
num_trials = 10
my_dataset = "det_concentrated_expertise_dataset.npz" 

pap_values = np.logspace(0, 7, num=8, base=2) * 10
Q_results = []
AAAI_results = []
Q_stderrs = []
AAAI_stderrs = []
for numpap in pap_values: # for fairness obj
    print("numpap", numpap)
    generate_deterministic_concentrated_expertise_dataset(int(numpap))

    optr = os.popen(f"python3 ./LP_TPMS.py det_concentrated_expertise_dataset.npz 100 {k} {l}")
    opt = (optr.readlines())[-2]
    opt = float(opt)
    print("opt", opt)
        
    Q_result = os.popen(f"python3 ./LP_TPMS.py {my_dataset} {Q} {k} {l}")
    lines = Q_result.readlines()
    try:
        TPMS_score = float(lines[-2]) #the objective value
        print("actual", TPMS_score)
    except ValueError:
        TPMS_score = -1
        #print("infeasible")
 
    if TPMS_score != -1: # if feasible
        scores = []
        for i in range(num_trials):
            os.system("./a.out < output.txt > output_bvn.txt")
            bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
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
 
    #getting results for AAAI
    scores = []
    count_infeasible = 0
    for i in range(num_trials):
        AAAI_result = os.popen(f"python3 ./AAAI_TPMS.py {my_dataset} {Q/100} {k} {l}")
        lines = AAAI_result.readlines()
        try:
            TPMS_score = float(lines[-2]) #the objective value
            print("aaai actual", TPMS_score)
        except ValueError:
            TPMS_score = -1
            count_infeasible += 1
            #print("infeasible")
 
        if TPMS_score != -1: # feasible
            os.system("./a.out < output.txt > output_bvn.txt")
            bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
            x = float(bvn_result.readline())
            scores.append(x)
    if num_trials == count_infeasible: # all infeasible
        s = -1
        AAAI_results.append(s)
        AAAI_stderrs.append(s)
    else:
        s = sum(scores) / (num_trials - count_infeasible)
        AAAI_results.append(s/opt)
        AAAI_stderrs.append(calculate_standard_error(scores, s, num_trials - count_infeasible)/opt)
        print("aaai estimate:", s)
     
print("Q_results:", Q_results)
print("AAAI_results:", AAAI_results)
print("Q_stderrs:", Q_stderrs)
print("AAAI_stderrs:", AAAI_stderrs)
dataset_name = my_dataset.split('.')[0]
name = "D_0_" + dataset_name + ".npy"
np.save(name, [pap_values, Q_results, AAAI_results, Q_stderrs, AAAI_stderrs])

