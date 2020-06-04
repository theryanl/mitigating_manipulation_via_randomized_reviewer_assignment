import sys
import os
import numpy as np
import time
from get_paper_totals import get_paper_totals
from std_error import calculate_standard_error 
from get_dataset_name import get_dataset_name

""" This file runs multiple tests of the similarity matrix LP + bvn process on a user-specified file. Then, it outputs data that allows the user to compare the two. """

## adjust this constant if you want more or less trials per size to take the average over.
num_trials = 10

##########################################################################

start_time = time.time()

my_dataset = sys.argv[1] #npz containing similarity matrix and conflict matrix
obj_type = int(sys.argv[2]) #type is 0 if TPMS, 1 if max min
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper

os.system("g++ -lm ../core/bvn.cpp") #compiles the bvn portion

Q_values = []
Q_results = []
Q_stderrs = []

if (obj_type == 0): #TPMS objective
    for Q in range(10, 110, 10): #loops through Q values (multiplied by 100)
        Q_values.append(Q/100)
        print(f"running Q = {Q/100}...")
        
        #getting our TPMS result for Q
        Q_result = os.popen(f"python3 ../core/LP_TPMS.py {my_dataset} {Q} {k} {l}")
        lines = Q_result.readlines()
        try:
            TPMS_score = float(lines[-2]) #the objective value in the string output
            print("actual", TPMS_score)
        except ValueError:
            TPMS_score = -1

        if TPMS_score != -1: # if feasible
            scores = []
            for i in range(num_trials):
                os.system("./a.out < output.txt > output_bvn.txt")
                #running the bvn portion
                
                bvn_result = os.popen(f"python3 ./TPMS_score_from_assignment.py {my_dataset} output_bvn.txt")
                #gets the TPMS score from the output
                
                x = float(bvn_result.readline())
                scores.append(x)
            
            #getting the avg and stderr
            s = sum(scores) / num_trials
            Q_results.append(s)
            Q_stderrs.append(calculate_standard_error(scores, s, num_trials))
            print("estimate:", s)
        
        else:
            s = -1 # signal infeasible
            Q_results.append(s)
            Q_stderrs.append(s)
    
elif (obj_type == 1): #max-min fairness objective
    for Q in range(10, 110, 10): #looping through values for Q (multiplied by 100)
        Q_values.append(Q/100)
        print(f"running Q = {Q/100}...")
        
        #getting result for Q
        Q_result = os.popen(f"python3 ../core/LP_max_min_fairness.py {my_dataset} {Q} {k} {l}") #running the LP portion
        lines = Q_result.readlines()
        
        try:
            max_min_fairness = float(lines[-2]) #the objective value
            print("actual", max_min_fairness)
        except ValueError:
            max_min_fairness = -1

        if max_min_fairness != -1: # if feasible
            Q_results.append(max_min_fairness)
        else:
            s = -1 # signal infeasible
            Q_results.append(s)
            #no stderr, since randomness is only in bvn portion

print("Q_values:", Q_values)
print("Q_results:", Q_results)
print("Q_stderrs:", Q_stderrs)

dataset_name = get_dataset_name(my_dataset)
name = "A_" + str(obj_type) + "_" + dataset_name + ".npy"
opt = Q_results[-1]
np.save(name, [Q_values, np.array(Q_results)/opt, np.array(Q_stderrs)/opt]) #saves as npy file

print("time taken", time.time() - start_time)
