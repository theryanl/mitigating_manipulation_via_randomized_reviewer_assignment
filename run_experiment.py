import numpy as np
import LP_output as LP
import sys

def runA(obj, dataset): # Q vs objective experiment
    l = 3
    if dataset == "preflib2":
        k = 7
    else:
        k = 6
    optimal_obj = # get optimal objective
    Q_values = np.linspace(0.125, 1, num=20)
    our_obj = []
    baseline_obj = []
    for p in Q_values:
        # set Q to p and call appropriate function with both algos
        if obj == "sum-similarity":
        elif obj == "fairness":
    data = [Q_values, our_obj, baseline_obj]
    np.save("A_" + obj + "_" + dataset + ".npy", data)

def plotB(): # runtime experiment
    sizes = np.linspace(0, 8000, num=20)
    k = 6
    l = 3
    Q = 0.5
    times = []
    for size in sizes:
        for i in range(10):
            # run algo
            # run bvn with exec()
            # get time
        # average times and store
    data = [sizes, times]
    np.save("B.npy", data)

def plotC(obj, dataset): # institution experiment
    l = 3
    if dataset == "preflib2":
        k = 7
    else:
        k = 6
    # set institutions somehow here
    optimal_obj = # get optimal objective in base problem
    t_values = np.linspace(1, 2, num=10)
    our_obj = []
    num_pairs = []
    for t in t_values:
        # set t and call institution-limit problem
        if obj == "sum-similarity":
        elif obj == "fairness":
        
        # call bvn version
        # load bvn output and count # of same-institution pairs
    data = [num_pairs, our_obj]
    np.save("C_" + obj + "_" + dataset + ".npy", data)

def main():
    if sys.argv[0] == 'A':
        runA(sys.argv[1], sys.argv[2])
    elif sys.argv[0] == 'B':
        runB()
    elif sys.argv[0] == 'C':
        runC(sys.argv[1], sys.argv[2])
