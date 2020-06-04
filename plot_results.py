import numpy as np
import matplotlib.pyplot as plt
import pylab
import sys

fontsize = 18
labels=["ICLR", "PrefLib1", "PrefLib2", "PrefLib3"]
colors=["red", "blue", "green", "magenta"]
markers=["o", "s", "^", "D"]
markersize=10
lw=3
ls =['solid', 'dotted', 'dashed', 'dashdot']

def legend():
    plt.rcParams.update({'font.size': 10})
    for i in range(4):
        plt.plot(np.arange(10), np.zeros(10), label=labels[i], color=colors[i], marker=markers[i], ms=markersize, linewidth=lw, linestyle=ls[i])
    plt.legend(ncol=4)
    plt.savefig("legend_full.png")
    #figLegend = pylab.figure(figsize = (1.5,1.3))
    #pylab.figlegend(*ax.get_legend_handles_labels(), loc = 'upper left', ncol=4)
    #figLegend.savefig("legend.png")

def plotA(obj): # Q vs objective experiment
    plt.rcParams.update({'font.size': fontsize})
    if obj == "0": # data = [q_values, our_algo_objectives, avg_baseline_algo_objectives, our_stderr, their_stderr]
        ylab = "Sum-similarity (% of optimal)"
        data0 = np.load("A_0_iclr2018.npy")
        data1 = np.load("A_0_preflib1.npy")
        data2 = np.load("A_0_preflib2.npy")
        data3 = np.load("A_0_preflib3.npy")
        for i, data in enumerate([data0, data1,data2, data3]):
            opt_obj = max(np.max(data[1]), np.max(data[2]))/100
            feasible_baseline = data[2] >= 0
            feasible_ours = data[1] >= 0
            plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]/opt_obj, yerr=data[3, feasible_ours]/opt_obj, color=colors[i], linewidth=lw, marker =markers[i], ms=markersize, linestyle=ls[i])
    elif obj == "1": # data = [q_values, our_algo_objectives, [], [], []]
        ylab = "Fairness (% of optimal)"
        data0 = np.load("A_1_iclr2018.npy", allow_pickle=True)
        data1 = np.load("A_1_preflib1.npy", allow_pickle=True)
        data2 = np.load("A_1_preflib2.npy", allow_pickle=True)
        data3 = np.load("A_1_preflib3.npy", allow_pickle=True)
        for i, data in enumerate([data0, data1,data2, data3]):
            l = []
            for j in range(2):
                l.append(data[j])
            data = np.array(l)
            opt_obj = np.max(data[1])/100
            feasible_ours = data[1] >= 0
            plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]/opt_obj, color=colors[i], linewidth=lw, marker = markers[i], ms=markersize, linestyle=ls[i])
    plt.xlabel("Maximum probability of each assignment")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    #plt.legend()
    plt.tight_layout()
    plt.savefig('A_' + obj + '.png')
    #plt.show()
    plt.close()

def plotB(): # runtime experiment
    # data = [sizes, avg_runtimes, std_err]
    data = np.load("B.npy")
    plt.rcParams.update({'font.size': fontsize})
    plt.errorbar(data[0], data[1], yerr=data[2], color='black', linewidth=lw, marker = 'o', ms=markersize)
    plt.xlabel("Problem size")
    plt.ylabel("Runtime (sec)")
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('B.png')
    #plt.show()
    plt.close()

def plotC(): # institution experiment
    # data = [number_same-institution_pairs, our_algo_objectives, std_err_pairs, std_err_obj, opt_obj]
    data0 = np.load("C_0_iclr2018.npy", allow_pickle=True)
    data1 = np.load("C_0_preflib1.npy", allow_pickle=True)
    data2 = np.load("C_0_preflib2.npy", allow_pickle=True)
    data3 = np.load("C_0_preflib3.npy", allow_pickle=True)
    #numrevs = [2435, 31, 24, 146]
    #instsize = [811, 11, 8, 48]
    #extra_pairs = [1, 0, 0, 1]
    ylab = "Sum-similarity (%)"

    plt.rcParams.update({'font.size': fontsize})
    for i, data in enumerate([data0, data1, data2, data3]):
        opt_obj = data[-1]/100
        l = []
        for j in range(4):
            l.append(data[j])
        data = np.array(l)
        feasible_ours = data[1] >= 0 
        numpairs = [691.2, 51.8, 50.2, 133.2][i]/100 # gotten through separate experiment and manually transfered here
        plt.errorbar(data[0, feasible_ours]/numpairs, data[1, feasible_ours]/opt_obj, xerr=data[2, feasible_ours]/numpairs,  yerr=data[3, feasible_ours]/opt_obj, color=colors[i], linewidth=lw, marker=markers[i], ms=markersize, linestyle=ls[i]) # our algo
    plt.xlabel("Same-institution reviewer pairs (%)")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    #plt.legend()
    plt.tight_layout()
    plt.savefig('C.png')
    #plt.show()
    plt.close()

def plotD(): # community model experiment
    data = np.load("D_0_det_concentrated_expertise_dataset.npy")
    ylab = "Sum-similarity (% of optimal)"
    feasible_ours = data[1] >= 0
    feasible_baseline = data[2] >= 0
    plt.rcParams.update({'font.size': fontsize})
    plt.errorbar(data[0, feasible_ours], data[1, feasible_ours]*100, yerr=data[3, feasible_ours], color='black', linewidth=lw, marker = 'o', ms=markersize)
    plt.xlabel("Number of papers")
    plt.ylabel(ylab)
    plt.ylim(bottom=0)
    #plt.legend()
    plt.tight_layout()
    plt.savefig('D.png')
    #plt.show()
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


if __name__ == "__main__":
    main()
