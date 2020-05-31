import sys
import os
import numpy as np
import time
from get_paper_totals import get_paper_totals

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
obj_type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper

Q_values = []
Q_results = []
AAAI_results = []

if (obj_type == 0):
    for Q in range(10, 110, 10):
        Q_values.append(Q/100)
        print(f"running Q = {Q/100}...")
        
        #getting result for Q
        Q_result = os.popen(f"python3 ./LP_TPMS.py {my_dataset} {Q} {k} {l}")
        TPMS_score = float((Q_result.readlines())[-2]) #the objective value
        Q_results.append(TPMS_score)
        print(TPMS_score)
        
        #getting results for AAAI
        summ = 0
        
        for i in range(10):
            AAAI_result = os.popen(f"python3 ./AAAI_TPMS.py {my_dataset} {Q/100} {k} {l}")
            AAAI_score = float((AAAI_result.readlines())[-2]) 
            #the objective value
            summ += AAAI_score
            
        avg = summ/10
        AAAI_results.append(avg)
        print(avg)
    
    
elif (obj_type == 1):
    for Q in range(10, 110, 10):
        Q_values.append(Q/100)
        print(f"running Q = {Q/100}...")
        
        #getting result for Q
        Q_result = os.popen(f"python3 ./LP_max_min_fairness.py {my_dataset} {Q} {k} {l}")
        max_min_fairness = float((Q_result.readlines())[-2]) #the objective value
        Q_results.append(max_min_fairness)
        print(max_min_fairness)
        
        #getting results for AAAI
        #summ = 0
        paper_totals_list = [] 
        for i in range(10):
            AAAI_result = os.popen(f"python3 ./AAAI_max_min_fairness.py {my_dataset} {Q/100} {k} {l}")
            AAAI_score = float((AAAI_result.readlines())[-2]) 
            #the objective value
            #summ += AAAI_score
            #file.write(f"{name} {value}\n")

            # calculate expected total similarity for each paper
            paper_totals_list.append(get_paper_totals("output.txt", my_dataset))
        # average together and take min
        avg_paper_totals = sum(paper_totals_list) / 10
        avg = np.min(avg_paper_totals)
            
        #avg = summ/10
        AAAI_results.append(avg)
        print(avg)
        
        
print("Q_values:", Q_values)
print("Q_results:", Q_results)
print("AAAI_results:", AAAI_results)
dataset_name = my_dataset.split('.')[0]
name = "A_" + str(obj_type) + "_" + dataset_name + ".npy"
np.save(name, [Q_values, Q_results, AAAI_results])

print("time taken", time.time() - start_time)
