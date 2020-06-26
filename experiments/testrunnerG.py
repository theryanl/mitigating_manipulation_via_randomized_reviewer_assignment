import sys
import os
import numpy as np
import time
from count_num_institution_pairs import count_num_institution_pairs
from institution_generator import *
from std_error import calculate_standard_error 
from get_dataset_name import get_dataset_name
from generate_dataset import *

# Runs the test that varies the institution loads on the uniform random simulation

# fixed parameters for this experiment
Q = 50
k = 3
l = 3
n = 1000
runs = 10
my_dataset = "rand.npz"
instsize = 100

avg_num_pairs = []
results = []
stderr_pairs = []
stderr_results = []

os.system("g++ -lm ../core/bvn.cpp") #compiling the bvn portion


for t in np.linspace(1, 3, 11):
    print(f"running t = {t}...")
    scores_list = []
    pairs_list = []
    for i in range(runs):
        generate_random_with_inst(n, instsize) # generate 
        
        #running the LP portion without institution constraints for comparison to the optimal:
        result = os.popen(f"python3 ../core/LP_output_institution_t.py {my_dataset} 0 {Q} 0 {k} 0 {l} institutions.npz {n}") # institution load cannot be >n
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
            print("infeasible")
            exit()
 
        r = os.system("./a.out < output.txt > output_bvn.txt")
        #running bvn portion
        if r != 0:
            print("bvn error")
            exit()

        bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
        x = float(bvn_result.readline())
        scores_list.append(x/opt)
        pairs = count_num_institution_pairs("output_bvn.txt", "institutions.npz") #counting the pairs of reviewers that belong to the same institution
        pairs_list.append(pairs/opt_pairs) #normalize based on current institutions

    anp = sum(pairs_list) / runs #average number of pairs
    avg_num_pairs.append(anp)
    avg = sum(scores_list) / runs
    results.append(avg)
    stderr_pairs.append(calculate_standard_error(pairs_list, anp, runs))
    stderr_results.append(calculate_standard_error(scores_list, avg, runs))

print("avg num inst pairs:", avg_num_pairs)
print("results:", results)
name = "G.npy"
np.save(name, [avg_num_pairs, results, stderr_pairs, stderr_results])
