import sys
import os
import numpy as np
import time
from get_paper_totals import get_paper_totals
from std_error import calculate_standard_error 
from check_det import check_det 

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
obj_type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper

os.system("g++ -lm bvn.cpp") #compiles the bvn portion

Q_values = []
Q_results = []
Q_stderrs = []
AAAI_results = []
AAAI_stderrs = []

num_trials = 10

if (obj_type == 0):
    for Q in range(10, 110, 10):
        Q_values.append(Q/100)
        print(f"running Q = {Q/100}...")
        
        #getting result for Q
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
            Q_results.append(s)
            Q_stderrs.append(calculate_standard_error(scores, s, num_trials))
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
            AAAI_stderrs.append(-1)
        else:
            s = sum(scores) / (num_trials - count_infeasible)
            AAAI_results.append(s)
            AAAI_stderrs.append(calculate_standard_error(scores, s, num_trials - count_infeasible))
            print("aaai estimate:", s)

    
    
elif (obj_type == 1):
    for Q in range(10, 110, 10):
        Q_values.append(Q/100)
        print(f"running Q = {Q/100}...")
        
        #getting result for Q
        Q_result = os.popen(f"python3 ./LP_max_min_fairness.py {my_dataset} {Q} {k} {l}")
        lines = Q_result.readlines()
        try:
            max_min_fairness = float(lines[-2]) #the objective value
            print("actual", max_min_fairness)
        except ValueError:
            max_min_fairness = -1
            print("infeasible")

        if max_min_fairness != -1: # if feasible
            scores = []
            for i in range(num_trials):
                os.system("./a.out < output.txt > output_bvn.txt")
                bvn_result = os.popen(f"python3 ./max_min_fairness_from_assignment.py {my_dataset} output_bvn.txt")
                fair = float(bvn_result.readline())
                scores.append(fair)
            s = sum(scores) / num_trials
            Q_results.append(s)
            Q_stderrs.append(calculate_standard_error(scores, s, num_trials))
            print("estimate:", s)
        else:
            s = -1 # signal infeasible
            Q_results.append(s)
            Q_stderrs.append(s)

        
        #getting results for AAAI
        scores = []
        count_infeasible = 0
        for i in range(num_trials):
            AAAI_result = os.popen(f"python3 ./AAAI_max_min_fairness.py {my_dataset} {Q/100} {k} {l}")
            lines = AAAI_result.readlines()
            try:
                max_min_fairness = float(lines[-2]) #the objective value
                print("actual", max_min_fairness)
            except ValueError:
                max_min_fairness = -1
                count_infeasible += 1
                print("infeasible")

            if max_min_fairness != -1: # feasible
                os.system("./a.out < output.txt > output_bvn.txt")
                bvn_result = os.popen(f"python3 ./max_min_fairness_from_assignment.py {my_dataset} output_bvn.txt")
                fair = float(bvn_result.readline())
                scores.append(fair)
        if num_trials == count_infeasible: # all infeasible
            s = -1
            AAAI_results.append(s)
            AAAI_stderrs.append(-1)
        else:
            s = sum(scores) / (num_trials - count_infeasible)
            AAAI_results.append(s)
            AAAI_stderrs.append(calculate_standard_error(scores, s, num_trials - count_infeasible))
            print("aaai estimate:", s)

print("Q_values:", Q_values)
print("Q_results:", Q_results)
print("AAAI_results:", AAAI_results)
print("Q_stderrs:", Q_stderrs)
print("AAAI_stderrs:", AAAI_stderrs)
dataset_name = my_dataset.split('.')[0]
name = "A_" + str(obj_type) + "_" + dataset_name + ".npy"
np.save(name, [Q_values, Q_results, AAAI_results, Q_stderrs, AAAI_stderrs])

print("time taken", time.time() - start_time)
