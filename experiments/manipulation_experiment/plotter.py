import numpy as np
from scipy.stats import sem
import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import ScalarFormatter

fontsize = 18
lw = 3
ms = 10

# Loads relevant data from .npz file with given name
def load_file(name):
    f = np.load(name)
    mvs = f["mani_values"]
    vs = []
    for v in f["values"]:
        vs.append(v)
    mvs, vs = zip(*sorted(zip(mvs, vs)))
    return np.array(mvs), list(vs)

# Combines the loaded data for two files with same manipulation_values
def combine_data(data1, data2):
    mvs1, vs1 = data1
    mvs2, vs2 = data2
    assert(all(mvs1 == mvs2))
    vs = []
    for i in range(len(mvs1)):
        v = np.append(vs1[i], vs2[i])
        vs.append(v)
    return mvs1, vs

# Combines the loaded data for two files with different manipulation_values
def append_data(data1, data2):
    mvs1, vs1 = data1
    mvs2, vs2 = data2
    assert(mvs1 != mvs2)

    mv = np.append(mvs1, mvs2)
    v = vs1 + vs2
    mv, v = zip(*sorted(zip(mv, v)))
    return np.array(mv), v


# Compute mean and standard error of mean
def compute_stats(vs):
    means = []
    ses = []
    for v in vs:
        means.append(np.mean(v))
        ses.append(sem(v))
    return means, ses

# Plots results for manipulation experiment
#   b: (manipulation_values, values) for standard assignment, 
#       where values is a list of lists containing, for each manipulation_value, the results of all trials
#   o: (manipulation_values, values) for randomized assignment
#   nm: (manipulation_values, values) for non-manipulated assignment
#   name: name of plot file
def plot_res(b, o, nm, name):
    mvs, bvs = b
    mvs2, ovs = o
    mvs0, nmvs = nm
    assert(all(mvs == mvs2))
    assert(all(mvs == mvs0))

    bmeans, bses = compute_stats(bvs)
    omeans, oses = compute_stats(ovs)
    nmmeans, nmses = compute_stats(nmvs)
    mvs = mvs + 1 # adjust to 1-indexing

    plt.rcParams.update({'font.size': fontsize})
    print(mvs, omeans)
    plt.errorbar(mvs, nmmeans, yerr=nmses, fmt="gX-.", linewidth=lw, markersize=ms)
    plt.errorbar(mvs, bmeans, yerr=bses, fmt="bo-", linewidth=lw, markersize=ms)
    plt.errorbar(mvs, omeans, yerr=oses, fmt="rs--", linewidth=lw, markersize=ms)
    plt.plot(mvs, [0.5]*len(mvs), 'k:', linewidth=lw)
    plt.ylim([-0.05, 1.05])
    plt.xlabel("Reviewer rank")
    plt.ylabel("Assignment probability")
    plt.xscale('log', basex=2)
    ax = plt.gca()
    plt.xticks([2**i for i in range(10)])
    #ax.xaxis.set_major_formatter(ScalarFormatter())
    #ax.annotate('Desired limit', xy=(100, 0.51))
    plt.tight_layout()
    plt.savefig(str(name) + ".pdf")
    plt.show()
    plt.close()

# Plots legend for manipulation experiment
def leg():
    plt.rcParams.update({'font.size': 10})
    plt.plot(np.arange(10), np.zeros(10), 'rs--', label='Our randomized assignment algorithm (Q=0.5)', linewidth=lw, markersize=ms)
    plt.plot(np.arange(10), np.zeros(10), 'bo-', label='Standard assignment algorithm', linewidth=lw, markersize=ms)
    plt.plot(np.arange(10), np.zeros(10), 'gX-.', label='Standard assignment algorithm, no manipulation', linewidth=lw, markersize=ms)
    plt.legend(ncol=1)
    plt.savefig("legend.pdf")
    plt.show()
    plt.close()
