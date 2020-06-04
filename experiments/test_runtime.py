import sys
import os
import numpy as np
import time
from institution_generator import *

# Quickly tests the runtime of the algorithms on the ICLR dataset

my_dataset = "data/iclr2018.npz"
k = 6
l = 3
Q = 50
t = 1

os.system("g++ -lm ../core/bvn.cpp") #compiles the bvn portion

num_trials = 10
runtimes = []
for i in range(num_trials):
    print(i)
    start_time = time.time()
    Q_result = os.popen(f"python3 ../core/LP_TPMS.py {my_dataset} {Q} {k} {l}")
    lines = Q_result.readlines()
    os.system("./a.out < output.txt > output_bvn.txt")
    end_time = time.time()      
    runtimes.append(end_time - start_time)
mean = sum(runtimes) / num_trials
print("normal mean:", mean, runtimes)

num_trials = 10
runtimes = []
for i in range(num_trials):
    print(i)
    generate_institutions_list(15, 2435)
    start_time = time.time()
    result = os.popen(f"python3 ../core/LP_output_institution_t.py {my_dataset} {Q} {k} {l} institutions.npz {t}")
    test = result.readlines()
    os.system("./a.out < output.txt > output_bvn.txt")
    end_time = time.time()
    runtimes.append(end_time - start_time)
mean = sum(runtimes) / num_trials
print("institution mean:", mean, runtimes)

