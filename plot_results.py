import numpy as np
import matplotlib.pyplot as plt
import sys

fontsize = 18

def plotA(obj, dataset): # Q vs objective experiment
    plt.rcParams.update({'font.size': fontsize})
    if obj == "0": # data = [q_values, our_algo_objectives, avg_baseline_algo_objectives, our_stderr, their_stderr]
        data = np.load("A_0_" + dataset + ".npy")
        ylab = "Sum-similarity (% of optimal)"
        opt_obj = max(np.max(data[1]), np.max(data[2]))
        feasible_baseline = data[2] >= 0
        feasible_ours = data[1] >= 0
        plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]/opt_obj, yerr=data[3, feasible_ours]/opt_obj, label="Our Algorithm", color='red', linewidth=3) # our algo
    elif obj == "1": # data = [q_values, our_algo_objectives, [], [], []]
        data = np.load("A_1_" + dataset + ".npy", allow_pickle=True)
        ylab = "Fairness (% of optimal)"
        opt_obj = np.max(data[1])
        l = []
        for i in range(2):
            l.append(data[i])
        data = np.array(l)
        feasible_ours = data[1] >= 0
        plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]/opt_obj, label="Our Algorithm", color='red', linewidth=3) # our algo
    #plt.errorbar(data[0, feasible_baseline], data[2, feasible_baseline]/opt_obj, yerr=data[4, feasible_baseline]/opt_obj, label="Random Removal Baseline", color='black', linestyle='--') # aaai algo
    plt.xlabel("Maximum probability of each assignment")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    #plt.legend()
    plt.tight_layout()
    plt.savefig('A_' + obj + '_' + dataset + '.png')
    plt.show()
    plt.close()

def plotB(): # runtime experiment
    # data = [sizes, avg_runtimes, std_err]
    data = np.load("B.npy")
    plt.rcParams.update({'font.size': fontsize})
    plt.errorbar(data[0], data[1], yerr=data[2], color='red', linewidth=3)
    plt.xlabel("Problem size")
    plt.ylabel("Runtime (sec)")
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('B.png')
    plt.show()
    plt.close()

def plotC(obj, dataset): # institution experiment
    # data = [number_same-institution_pairs, our_algo_objectives, std_err_pairs, std_err_obj, opt_obj]
    if obj == "0":
        data = np.load("C_0_" + dataset + ".npy", allow_pickle=True)
        ylab = "Sum-similarity (% of optimal)"
    elif obj == "1":
        data = np.load("C_1_" + dataset + ".npy", allow_pickle=True)
        ylab = "Fairness (% of optimal)"
    opt_obj = data[-1]
    l = []
    for i in range(4):
        l.append(data[i])
    data = np.array(l)

    feasible_ours = data[1] >= 0 
    plt.rcParams.update({'font.size': fontsize})
    plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]/opt_obj, xerr=data[2, feasible_ours],  yerr=data[3, feasible_ours]/opt_obj, label="Our Algorithm", color='red', linewidth=3) # our algo
    plt.xlabel("Number of same-institution reviewer pairs")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    plt.savefig('C_' + obj + '_' + dataset + '.png')
    plt.show()
    plt.close()

def plotD(obj, dataset): # community model experiment
    if obj == "0":
        data = np.load("D_0_" + dataset + ".npy")
        ylab = "Sum-similarity (% of optimal)"
    elif obj == "1":
        data = np.load("D_1_" + dataset + ".npy")
        ylab = "Fairness (% of optimal)"
    feasible_ours = data[1] >= 0
    feasible_baseline = data[2] >= 0
    plt.rcParams.update({'font.size': fontsize})
    plt.errorbar(data[0, feasible_ours], data[1, feasible_ours], yerr=data[3, feasible_ours], label="Our Algorithm", color='red', linewidth=3) # our algo
    #plt.errorbar(data[0, feasible_baseline], data[2, feasible_baseline], yerr=data[4, feasible_baseline], label="Random Removal Baseline", color='black', linestyle='--') # baseline algo
    plt.xlabel("Number of papers")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    #plt.legend()
    plt.tight_layout()
    plt.savefig('D_' + obj + '_' + dataset + '.png')
    plt.show()
    plt.close()

def main():
    if sys.argv[1] == 'A':
        plotA(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'B':
        plotB()
    elif sys.argv[1] == 'C':
        plotC(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'D':
        plotD(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
