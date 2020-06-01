import sys
import os
import numpy as np
import time
from generate_dataset import generate_deterministic_concentrated_expertise_dataset
#import subprocess

k = 3
l = 3
Q = 50
num_trials = 10
my_dataset = "det_concentrated_expertise_dataset.npz" 

pap_values = np.logspace(0, 7, num=8, base=2) * 10
Q_results = []
AAAI_results = []
for numpap in pap_values:
    print("numpap", numpap)
    generate_deterministic_concentrated_expertise_dataset(int(numpap))
    #subprocess.run(f"python3 ./LP_TPMS.py det_concentrated_expertise_dataset.npz {Q} {k} {l}")

    optr = os.popen(f"python3 ./LP_TPMS.py det_concentrated_expertise_dataset.npz 100 {k} {l}")
    opt = (optr.readlines())[-2]
    opt = float(opt)
    print("opt", opt)
        
    Q_result = os.popen(f"python3 ./LP_TPMS.py det_concentrated_expertise_dataset.npz {Q} {k} {l}")
   
    x = (Q_result.readlines())[-2]
    try:
        TPMS_score = float(x) #the objective value
    except ValueError:
        TPMS_score = 0
        print("infeasible assignment")
    Q_results.append(TPMS_score/opt)
    print("tpms", TPMS_score)
        
    #getting results for AAAI
    summ = 0
    count_infeas = 0
    
    for i in range(num_trials):
        AAAI_result = os.popen(f"python3 ./AAAI_TPMS.py det_concentrated_expertise_dataset.npz {Q/100} {k} {l}")
        x = (AAAI_result.readlines())[-2]
        try:
            AAAI_score = float(x)#float((AAAI_result.readlines())[-2]) 
        except ValueError:
            AAAI_score = 0
            count_infeas += 1
            #print("infeasible assignment")
        #the objective value
        summ += AAAI_score
        
    if num_trials == count_infeas:
        print("all infeasible assignments")
        avg = 0
    else:
        avg = summ/(num_trials - count_infeas)
    AAAI_results.append(avg/ opt)
    print("aaai", avg)
     
print("Q_results:", Q_results)
print("AAAI_results:", AAAI_results)
dataset_name = my_dataset.split('.')[0]
name = "D_0_" + dataset_name + ".npy"
np.save(name, [pap_values, Q_results, AAAI_results])

