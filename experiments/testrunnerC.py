import sys
import os
import numpy as np
import time
from count_num_institution_pairs import count_num_institution_pairs
from institution_generator import *
from std_error import calculate_standard_error 
from get_dataset_name import get_dataset_name

# Varies the institution loads and observes objective and number of same institution pairs, on a dataset

## The tests are run on a fixed Q value (upper bound on any matching). This can be changed here:
Q = 50 

###########################################################################

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
k = int(sys.argv[2]) #k is the upper bound for papers per reviewer
l = int(sys.argv[3]) #l is the number of reviewers per paper
reviewers_per_institution = int(sys.argv[4]) #upper bound on the number of reviewers per institution

avg_num_pairs = []
results = []
stderr_pairs = []
stderr_results = []

n = len((np.load(my_dataset))["similarity_matrix"]) #number of reviewers

## The number of trials per value of reviewers_per_institution can be adjusted here:
runs = 10


os.system("g++ -lm ../core/bvn.cpp") #compiling the bvn portion

for t in np.linspace(1, 2, 11): #1.0, 1.1, 1.2, ..., 1.9, 2.0
    print(f"running t = {t}...")
    scores_list = []
    pairs_list = []
    count_infeasible = 0

    for i in range(runs):
        print("trial", i)
        generate_institutions_list(reviewers_per_institution, n)
        #generates random institution list based on reviewers per institution
        #for more details see the comments in institution_generator.py

        #running the LP portion without institution constraints for comparison to the optimal:
        result = os.popen(f"python3 ../core/LP_output_institution_t.py {my_dataset} 0 {Q} 0 {k} 0 {l} institutions.npz {n}") #load cannot be >n
        test = (result.readlines())[-2]
        opt = float(test)
        r = os.system("./a.out < output.txt > output_bvn.txt")
        opt_pairs = count_num_institution_pairs("output_bvn.txt", "institutions.npz") #counting the pairs of reviewers that belong to the same institution

        #run actual test
        result = os.popen(f"python3 ../core/LP_output_institution_t.py {my_dataset} 0 {Q} 0 {k} 0 {l} institutions.npz {t}") #running LP portion
        test = (result.readlines())[-2]
               
        try:
            TPMS_score = float(test)
        except ValueError:
            TPMS_score = -1
            count_infeasible += 1

        if TPMS_score != -1:
            r = os.system("./a.out < output.txt > output_bvn.txt")
            #running bvn portion
            if r != 0:
                exit()
            
            bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
            #calculating TPMS score from the bvn output
            
            x = float(bvn_result.readline())
            scores_list.append(x/opt)
            pairs = count_num_institution_pairs("output_bvn.txt", "institutions.npz") #counting the pairs of reviewers that belong to the same institution
            if pairs == 0 and opt_pairs == 0:
                pairs_list.append(1) #normalize based on current institutions
            else:
                pairs_list.append(pairs/opt_pairs)

    if runs == count_infeasible:
        avg_num_pairs.append(-1)
        results.append(-1)
        stderr_pairs.append(-1)
        stderr_results.append(-1)
    else:
        #finding the avg and stderr of both #pairs and score
        feas_runs = runs-count_infeasible
        anp = sum(pairs_list) / feas_runs #average number of pairs
        avg_num_pairs.append(anp)
        avg = sum(scores_list) / feas_runs
        print(avg, anp)
        results.append(avg)
        stderr_pairs.append(calculate_standard_error(pairs_list, anp, feas_runs))
        stderr_results.append(calculate_standard_error(scores_list, avg, feas_runs))
        

print("avg num inst pairs:", avg_num_pairs)
print("results:", results)
dataset_name = get_dataset_name(my_dataset)

name = "C_" + dataset_name + ".npy"
np.save(name, [avg_num_pairs, results, stderr_pairs, stderr_results])
#saves as npy file containing the above ^

print("time taken", time.time() - start_time)
