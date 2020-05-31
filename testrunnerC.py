import sys
import os
import numpy as np
import time
from count_num_institution_pairs import count_num_institution_pairs

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
obj_type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper

avg_num_pairs = []
results = []

# TODO generate 10 random institution files
# inst_list

if (obj_type == 0):
    for t in np.linspace(1, 2, 0.1):
        print(f"running t = {t}...")
        total = 0
        total_pairs = 0
        for insts in inst_list:
            result = os.popen # TODO run LP with loads limited to t and Q = 1 and insts
            TPMS_score = float((result.readlines())[-2]) #the objective value
            total += TPMS_score
            # TODO run bvn on output.txt and get output_bvn.txt
            # (make sure to wait for the process to finish)
            total_pairs += count_num_institution_pairs("output_bvn.txt", insts)
        avg = total / len(inst_list)
        results.append(avg)
        avg_pairs = total_pairs / len(inst_list)
        avg_num_pairs.append(avg_pairs)
        print(avg, avg_pairs)

elif (obj_type == 1):
    # do later
        
print("avg num inst pairs:", avg_num_pairs)
print("results:", results)
dataset_name = my_dataset.split('.')[0]
name = "C_" + str(obj_type) + "_" + dataset_name + ".npy"
np.save(name, [avg_num_pairs, results])

print("time taken", time.time() - start_time)
