import numpy as np
import matplotlib.pyplot as plt
import sys

def plotA(obj, dataset): # Q vs objective experiment
    # data = [q_values, our_algo_objectives, avg_baseline_algo_objectives]
    if obj == "sum-similarity":
        data = np.load("A_sum-similarity_" + dataset + ".npy")
        ylab = "Sum-similarity objective (% of optimal)"
    elif obj == "fairness":
        data = np.load("A_fairness_" + dataset + ".npy")
        ylab = "Fairness objective (% of optimal)"
    plt.plot(data[0], data[1], label="Our Algorithm", color='red') # our algo
    plt.plot(data[0], data[2], label="Random Removal Baseline", color='black', linestyle='--') # aaai algo
    plt.xlabel("Maximum probability of each assignment")
    plt.ylabel(ylab)
    plt.legend()
    plt.savefig('A_' + obj + '_' + dataset + '.png')
    plt.close()

def plotB(): # runtime experiment
    # data = [sizes, avg_runtimes]
    data = np.load("B.npy")
    plt.plot(data[0], data[1], color='red')
    plt.xlabel("Problem size")
    plt.ylabel("Runtime (sec)")
    plt.savefig('B.png')
    plt.close()

def plotC(obj, dataset): # institution experiment
    # data = [number_same-institution_pairs, our_algo_objectives]
    if obj == "sum-similarity":
        data = np.load("C_sum-similarity_" + dataset + ".npy")
        ylab = "Sum-similarity objective (% of optimal)"
    elif obj == "fairness":
        data = np.load("C_fairness_" + dataset + ".npy")
        ylab = "Fairness objective (% of optimal)"
    plt.plot(data[0], data[1], label="Our Algorithm", color='red') # our algo
    plt.xlabel("Number of same-institution reviewer pairs")
    plt.ylabel(ylab)
    plt.legend()
    plt.savefig('C_' + obj + '_' + dataset + '.png')
    plt.close()

def main():
    if sys.argv[1] == 'A':
        plotA(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'B':
        plotB()
    elif sys.argv[1] == 'C':
        plotC(sys.argv[2], sys.argv[3])
