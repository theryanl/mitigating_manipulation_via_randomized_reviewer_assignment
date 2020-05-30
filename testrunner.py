import sys
import os
import numpy as np

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper


results_file = open("results.txt", "w")

if (type == 0):
    for Q in range(10, 110, 10):
        print(f"running Q = {Q/100}...\n")
        
        results_file.write(f"Q = {Q/100}\n")
        result = os.popen(f"python3 ./LP_TPMS.py {my_dataset} {Q} {k} {l}")
        TPMS_score = (result.readlines())[-2] #the objective value
        results_file.write(f"{TPMS_score}")
        print(TPMS_score)
    
    
elif (type == 1):
    for Q in range(10, 110, 10):
        print(f"running Q = {Q/100}...\n")
        
        results_file.write(f"Q = {Q/100}\n")
        result = os.popen(f"python3 ./LP_max_min_fairness.py {my_dataset} {Q} {k} {l}")
        max_min_fairness = (result.readlines())[-2] #the objective value
        results_file.write(f"{max_min_fairness}")
        print(max_min_fairness)
        
        
results_file.close()