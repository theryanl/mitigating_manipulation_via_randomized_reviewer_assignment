import numpy as np
import matplotlib.pyplot as plt
import sys

def plotA(obj, dataset): # Q vs objective experiment
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
    data = np.load("B.npy")
    plt.plot(data[0], data[1], color='red')
    plt.xlabel("Problem size")
    plt.ylabel("Runtime (sec)")
    plt.savefig('B.png')
    plt.close()

def plotC(obj, dataset): # institution experiment
    if obj == "sum-similarity":
        data = np.load("C_sum-similarity_" + dataset + ".npy")
        ylab = "Sum-similarity objective (% of optimal)"
    elif obj == "fairness":
        data = np.load("C_fairness_" + dataset + ".npy")
        ylab = "Fairness objective (% of optimal)"
    plt.plot(data[0], data[1], label="Our Algorithm", color='red') # our algo
    plt.plot(data[0], data[2], label="Random Removal Baseline", color='black', linestyle='--') # aaai algo
    plt.xlabel("Average number of same-institution reviewer pairs")
    plt.ylabel(ylab)
    plt.legend()
    plt.savefig('C_' + obj + '_' + dataset + '.png')
    plt.close()

def main():
    if sys.argv[0] == 'A':
        plotA(sys.argv[1], sys.argv[2])
    elif sys.argv[0] == 'B':
        plotB()
    elif sys.argv[0] == 'C':
        plotC(sys.argv[1], sys.argv[2])
