import sys
import os
import numpy as np
import time
from std_error import calculate_standard_error

overall_start_time = time.time()

Q = float(sys.argv[1]) #upper bound probability of matching
type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper
start_size = int(sys.argv[5])
end_size = int(sys.argv[6]) #end size is also run (inclusive upper bound)
step_size = int(sys.argv[7])

num_trials = 10

os.system("g++ -lm bvn.cpp") #compiles the bvn portion

size_list = []
avg_runtimes = []
stderrs = []

if (type == 0):
    for size in range(start_size, end_size + step_size, step_size):
        size_list.append(size)
        print(f"running size = {size}...")
        
        times = []
        
        for i in range(num_trials):
            start_time = time.time()
            result = os.popen(f"python3 ./rand_LP_output.py {Q} {size} {k} {l}")
            lines = result.readlines()
            try:
                TPMS_score = float(lines[-2]) #the objective value
                print("actual", TPMS_score)
            except ValueError:
                TPMS_score = -1
            if TPMS_score != -1: # if feasible
                os.system("./a.out < rand_output.txt > rand_output_bvn.txt")
            runtime = time.time() - start_time
            times.append(runtime)
        
        avg = sum(times)/num_trials
        avg_runtimes.append(avg)
        stderrs.append(calculate_standard_error(times, avg, num_trials))
        print(avg)
          
elif (type == 1):
    print("not yet implemented")
    
print("sizes:", size_list)
print("avg_runtimes:", avg_runtimes)
print("stderrs:", stderrs)
np.save("B.npy", [size_list, avg_runtimes, stderrs])

print("time taken", time.time() - overall_start_time)
