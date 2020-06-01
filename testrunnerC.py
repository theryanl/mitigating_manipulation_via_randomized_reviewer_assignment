import sys
import os
import numpy as np
import time
from count_num_institution_pairs import count_num_institution_pairs
from institution_generator import *

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
obj_type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper
reviewers_per_institution = int(sys.argv[5])

avg_num_pairs = []
results = []

n = len((np.load(my_dataset))["similarity_matrix"])

runs = 2
os.system("g++ -lm bvn.cpp")

if (obj_type == 0):
    for t in np.linspace(1, 2, 11):
        print(f"running t = {t}...")
        total = 0
        total_pairs = 0
        
        for i in range(runs):
            print(f"{i} iterations completed")
            generate_institutions_list(reviewers_per_institution, n)
            
            result = os.popen(f"python3 LP_output_institution_t.py {my_dataset} 100 {k} {l} institutions.npz {t}")
            
            test = (result.readlines())[-2]
            
            if (ord(test[0]) == ord("a")):
                print("infeasible")
                TPMS_score = 0
            else:
                TPMS_score = float(test) #the objective value
            total += TPMS_score
            
            print("doing bvn")
            
            os.system("./a.out < output.txt > output_bvn.txt")
            # (make sure to wait for the process to finish)
            total_pairs += count_num_institution_pairs("output_bvn.txt", insts)
        avg = total / runs
        results.append(avg)
        avg_pairs = total_pairs / runs
        avg_num_pairs.append(avg_pairs)
        print(avg, avg_pairs)

elif (obj_type == 1):
    pass
    # do later
        
print("avg num inst pairs:", avg_num_pairs)
print("results:", results)
dataset_name = my_dataset.split('.')[0]
name = "C_" + str(obj_type) + "_" + dataset_name + ".npy"
np.save(name, [avg_num_pairs, results])

print("time taken", time.time() - start_time)
