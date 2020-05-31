import sys
import os
import numpy as np
import time

overall_start_time = time.time()

Q = float(sys.argv[1]) #upper bound probability of matching
type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper
start_size = int(sys.argv[5])
end_size = int(sys.argv[6]) #end size is also run (inclusive upper bound)
step_size = int(sys.argv[7])

os.system("g++ -lm bvn.cpp") #compiles the bvn portion

size_list = []
avg_runtimes = []

if (type == 0):
    for size in range(start_size, end_size + step_size, step_size):
        size_list.append(size)
        print(f"running size = {size}...")
        
        summ = 0
        
        for i in range(10):
            start_time = time.time()
            result = os.popen(f"python3 ./rand_LP_output.py {Q} {size} {k} {l}")
            lines = result.readlines()
            if (ord((lines[-4])[0]) == 73):
                #infeasible model
                print(f"infeasible model for size = {size} in run {i}")
            
            os.system("./a.out < rand_output.txt > rand_output_bvn.txt")
            
            runtime = time.time() - start_time
            summ += runtime
        
        avg = summ/10
        avg_runtimes.append(avg)
        print(avg)
          
elif (type == 1):
    print("not yet implemented")
    
print("sizes:", size_list)
print("avg_runtimes:", avg_runtimes)
np.save("testrunner_rand_results", [size_list, avg_runtimes])

print("time taken", time.time() - overall_start_time)