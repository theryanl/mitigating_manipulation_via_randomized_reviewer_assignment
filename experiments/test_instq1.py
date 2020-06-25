import sys
import os
import numpy as np
import time
from count_num_institution_pairs import count_num_institution_pairs
from institution_generator import *
from std_error import calculate_standard_error 
from get_dataset_name import get_dataset_name

# Tests the number of same-institution pairs with random institutions on a dataset, without any constraints on the institution loads or on Q.

Q = 100

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
k = int(sys.argv[2]) #k is the upper bound for papers per reviewer
l = int(sys.argv[3]) #l is the number of reviewers per paper
reviewers_per_institution = int(sys.argv[4]) #upper bound on the number of reviewers per institution

n = len((np.load(my_dataset))["similarity_matrix"]) #number of reviewers

## The number of trials per value of reviewers_per_institution can be adjusted here:
runs = 10


os.system("g++ -lm ../core/bvn.cpp") #compiling the bvn portion

pairs_list = []

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

    pairs_list.append(opt_pairs)

anp = sum(pairs_list) / runs
stderr_pairs = calculate_standard_error(pairs_list, anp, runs)
print(anp, stderr_pairs)
print(pairs_list)
