import sys
import os
import numpy as np
import time
from count_num_institution_pairs import count_num_institution_pairs
from institution_generator import *
from std_error import calculate_standard_error 

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
obj_type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper
reviewers_per_institution = int(sys.argv[5])
Q = 50

avg_num_pairs = []
results = []
stderr_pairs = []
stderr_results = []

n = len((np.load(my_dataset))["similarity_matrix"])

runs = 10
os.system("g++ -lm bvn.cpp")

if (obj_type == 0):
    result = os.popen(f"python3 LP_TPMS.py {my_dataset} {Q} {k} {l}")
    test = (result.readlines())[-2]
    opt = float(test)
    print("opt", opt)
 
    #max_inst_load = reviewers_per_institution * Q
    for t in np.linspace(1, 2, 11):
        print(f"running t = {t}...")
        scores_list = []
        pairs_list = []
        count_infeasible = 0

        for i in range(runs):
            #print(f"{i} iterations completed")
            generate_institutions_list(reviewers_per_institution, n)
           
            result = os.popen(f"python3 LP_output_institution_t.py {my_dataset} {Q} {k} {l} institutions.npz {t}")
            test = (result.readlines())[-2]
            try:
                TPMS_score = float(test)
                print("actual:", TPMS_score)
            except ValueError:
                TPMS_score = -1
                count_infeasible += 1

            if TPMS_score != -1:
                r = os.system("./a.out < output.txt > output_bvn.txt")
                if r != 0:
                    exit()
                bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
                x = float(bvn_result.readline())
                scores_list.append(x)
                pairs = count_num_institution_pairs("output_bvn.txt", "institutions.npz")
                pairs_list.append(pairs)

        if runs == count_infeasible:
            avg_num_pairs.append(-1)
            results.append(-1)
            stderr_pairs.append(-1)
            stderr_results.append(-1)
        else:
            feas_runs = runs-count_infeasible
            anp = sum(pairs_list) / feas_runs
            avg_num_pairs.append(anp)
            avg = sum(scores_list) / feas_runs
            print(avg, anp)
            results.append(avg)
            stderr_pairs.append(calculate_standard_error(pairs_list, anp, feas_runs))
            stderr_results.append(calculate_standard_error(scores_list, avg, feas_runs))

elif (obj_type == 1):
    pass #unimplemented for now

print("avg num inst pairs:", avg_num_pairs)
print("results:", results)
dataset_name = my_dataset.split('.')[0]
name = "C_" + str(obj_type) + "_" + dataset_name + ".npy"
np.save(name, [avg_num_pairs, results, stderr_pairs, stderr_results, opt])

print("time taken", time.time() - start_time)
