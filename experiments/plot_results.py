import numpy as np
import matplotlib.pyplot as plt
import pylab
import sys

'''
Functions for plotting results. Input on command line the experiment to plot
(and the objective, if applicable).
'''

fontsize = 18
labels=["ICLR", "PrefLib1", "PrefLib2", "PrefLib3"]
sim_labels=["Community, g=3", "Community, g=6", "Community, g=9", "Community, g=12", "Uniform random"]
colors=["red", "blue", "green", "magenta", "black"]
markers=["o", "s", "^", "D", "v"]
markersize=10
lw=3
ls =['solid', 'dotted', 'dashed', 'dashdot', 'solid']

# Plots the legend for the datasets
def legend():
    plt.rcParams.update({'font.size': 10})
    for i in range(4):
        plt.plot(np.arange(10), np.zeros(10), label=labels[i], color=colors[i], marker=markers[i], ms=markersize, linewidth=lw, linestyle=ls[i])
    plt.legend(ncol=4)
    plt.savefig("legend_full.pdf")

# Plots the legend for the simulations
def sim_legend():
    plt.rcParams.update({'font.size': 9})
    for i in range(5):
        plt.plot(np.arange(10), np.zeros(10), label=sim_labels[i], color=colors[i], marker=markers[i], ms=markersize, linewidth=lw, linestyle=ls[i])
    plt.legend(ncol=3)
    plt.savefig("sim_legend_full.pdf")

def plotA(obj): # Q vs objective experiment, datasets
    # plots results from testrunner A
    plt.rcParams.update({'font.size': fontsize})
    if obj == "0": # data = [q_values, our_algo_objectives, stderr]
        ylab = "Sum-similarity (% of optimal)"
        data0 = np.load("A_0_iclr2018.npy")
        data1 = np.load("A_0_preflib1.npy")
        data2 = np.load("A_0_preflib2.npy")
        data3 = np.load("A_0_preflib3.npy")
        for i, data in enumerate([data0, data1,data2, data3]):
            feasible_ours = data[1] >= 0
            plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]*100, yerr=data[2, feasible_ours]*100, color=colors[i], linewidth=lw, marker =markers[i], ms=markersize, linestyle=ls[i])
    elif obj == "1": # data = [q_values, our_algo_objectives, []]
        ylab = "Stochastic fairness (% of optimal)"
        data0 = np.load("A_1_iclr2018.npy", allow_pickle=True)
        data1 = np.load("A_1_preflib1.npy", allow_pickle=True)
        data2 = np.load("A_1_preflib2.npy", allow_pickle=True)
        data3 = np.load("A_1_preflib3.npy", allow_pickle=True)
        for i, data in enumerate([data0, data1,data2, data3]):
            l = []
            for j in range(2):
                l.append(data[j])
            data = np.array(l)
            feasible_ours = data[1] >= 0
            plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]*100, color=colors[i], linewidth=lw, marker = markers[i], ms=markersize, linestyle=ls[i])
    plt.xlabel("Maximum probability of each assignment")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('A_' + obj + '.pdf')
    plt.close()

def plotB(): # runtime experiment, simulations
    # plots results from testrunners: B, H
    # data = [sizes, avg_runtimes, std_err]
    plt.rcParams.update({'font.size': fontsize})
    for i, fn in enumerate(["H_3.npy", "H_6.npy", "H_9.npy", "H_12.npy", "B.npy"]):
        data = np.load(fn)
        plt.errorbar(data[0], data[1], yerr=data[2], color=colors[i], linewidth=lw, marker = markers[i], ms=markersize, linestyle=ls[i])
    plt.xlabel("Problem size")
    plt.ylabel("Runtime (sec)")
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('B.pdf')
    plt.close()

def plotC(): # institution experiment, datasets
    # plots results from testrunner C
    # data = [number_same-institution_pairs, our_algo_objectives, std_err_pairs, std_err_obj]
    data0 = np.load("C_iclr2018.npy", allow_pickle=True)
    data1 = np.load("C_preflib1.npy", allow_pickle=True)
    data2 = np.load("C_preflib2.npy", allow_pickle=True)
    data3 = np.load("C_preflib3.npy", allow_pickle=True)
    ylab = "Sum-similarity (% of optimal)"

    x = np.linspace(1, 2, 11)
    plt.rcParams.update({'font.size': fontsize})
    for i, data in enumerate([data0, data1, data2, data3]):
        feasible_ours = data[1] >= 0 
        #plt.errorbar(data[0, feasible_ours]*100, data[1, feasible_ours]*100, xerr=data[2, feasible_ours]*100,  yerr=data[3, feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i]) # our algo
        plt.errorbar(x[feasible_ours], data[1, feasible_ours]*100, yerr=data[3, feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i]) # our algo

    #plt.xlabel("Same-institution reviewer pairs (%)")
    plt.xlabel("Max. expected same-subset reviewers/paper")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('C.pdf')
    plt.close()

def plotD(): # Q vs objective, simulations
    # plots results from testrunners: D, F
    # data = [group_sizes, q_values, objs, stderrs]
    data_full = np.load("D.npy", allow_pickle=True)
    qs = data_full[1]
    ylab = "Sum-similarity (% of optimal)"
    for i in range(4):
        data = data_full[2][i]
        stderrs = data_full[3][i]
        feasible_ours = data >= 0
        plt.rcParams.update({'font.size': fontsize})
        plt.errorbar(qs[feasible_ours], data[feasible_ours]*100, yerr=stderrs[feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i])
    data = np.load("F.npy")
    feasible_ours = data[1] >= 0
    plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]*100, yerr=data[2, feasible_ours]*100, color=colors[4], linewidth=lw, marker=markers[4], ms=markersize, linestyle=ls[4])
    plt.xlabel("Maximum probability of each assignment")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('D.pdf')
    plt.close()

def plotE(): # institution experiment, simulations
    # plots results from testrunners: E, G
    # data = [number_same-institution_pairs, our_algo_objectives, std_err_pairs, std_err_obj]
    plt.rcParams.update({'font.size': fontsize})
    x = np.linspace(1, 3, 11)
    for i, g in enumerate([3, 6, 9, 12]):
        data = np.load("E_" + str(g) + ".npy", allow_pickle=True)
        feasible_ours = data[1] >= 0 
        #plt.errorbar(data[0, feasible_ours]*100, data[1, feasible_ours]*100, xerr=data[2, feasible_ours]*100,  yerr=data[3, feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i])
        plt.errorbar(x[feasible_ours], data[1, feasible_ours]*100, yerr=data[3, feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i])


    data = np.load("G.npy", allow_pickle=True)
    feasible_ours = data[1] >= 0 
    i = 4
    #plt.errorbar(data[0, feasible_ours]*100, data[1, feasible_ours]*100, xerr=data[2, feasible_ours]*100,  yerr=data[3, feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i])
    plt.errorbar(x[feasible_ours], data[1, feasible_ours]*100, yerr=data[3, feasible_ours]*100, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i])

    ylab = "Sum-similarity (% of optimal)"
    #plt.xlabel("Same-institution reviewer pairs (%)")
    plt.xlabel("Max. expected same-subset reviewers/paper")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('E.pdf')
    plt.close()

def main():
    if sys.argv[1] == 'A':
        plotA(sys.argv[2])
    elif sys.argv[1] == 'B':
        plotB()
    elif sys.argv[1] == 'C':
        plotC()
    elif sys.argv[1] == 'D':
        plotD()
    elif sys.argv[1] == 'L':
        legend()
    elif sys.argv[1] == 'E':
        plotE()
    elif sys.argv[1] == 'SL':
        sim_legend()


if __name__ == "__main__":
    main()
