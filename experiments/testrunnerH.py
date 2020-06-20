import sys
import os
import numpy as np
import time
from std_error import calculate_standard_error
from generate_dataset import *

# Runs the experiment to test the runtime of the community model simulations

num_trials = 10

###########################################################################

overall_start_time = time.time()

Q = 50 #upper bound probability of matching * 100
k = 3 #k is the upper bound for papers per reviewer
l = 3 #l is the number of reviewers per paper

#for loop arguments:
start_size = int(sys.argv[1])
end_size = int(sys.argv[2]) #end size is also run (inclusive upper bound)
step_size = int(sys.argv[3])

g = int(sys.argv[4]) # group size

os.system("g++ -lm ../core/bvn.cpp") #compiles the bvn portion

size_list = [] #list of sizes
avg_runtimes = [] #list of average runtimes
stderrs = [] #list of stderrs

for size in range(start_size, end_size + step_size, step_size):
#looping over the sizes to test

    size_list.append(size)
    print(f"running size = {size}...")
    
    times = [] #list of individual runtimes for this particular size
    
    for i in range(num_trials):
        generate_deterministic_concentrated_expertise_dataset(size, g) # generate the similarities
        start_time = time.time()
        result = os.popen(f"python3 ../core/LP_TPMS.py det_concentrated_expertise_dataset.npz 0 {Q} 0 {k} {l}")
        lines = result.readlines()
        try:
            TPMS_score = float(lines[-2]) #the objective value
            print("actual", TPMS_score)
        except ValueError:
            TPMS_score = -1
        if TPMS_score != -1: # if feasible
            os.system("./a.out < output.txt > output_bvn.txt") #run the bvn part
        runtime = time.time() - start_time
        times.append(runtime)
    
    #getting the average and stderr
    avg = sum(times)/num_trials
    avg_runtimes.append(avg)
    stderrs.append(calculate_standard_error(times, avg, num_trials))
    print(times, avg, stderrs[-1])
    np.save("H_" + str(g) + ".npy", [size_list, avg_runtimes, stderrs]) #saves in npy format. In case the program stops in this middle, it will still save what was most recently completed.

    
print("sizes:", size_list)
print("avg_runtimes:", avg_runtimes)
print("stderrs:", stderrs)
np.save("H_" + str(g) + ".npy", [size_list, avg_runtimes, stderrs]) #saves in npy format

print("time taken", time.time() - overall_start_time)
