import numpy as np
import sys

# part of this are referenced from https://github.com/xycforgithub/StrategyProof_Conference_Review
inst_file = sys.argv[1] # file containing institution list
assignment = sys.argv[2] #integral assignment

inst_data = np.load(inst_file, allow_pickle=True)
insts = inst_data[1:] # drop number of institutions entry

reviewers = len(insts)
#papers = len(S[0])

pairs_file = open(assignment, "r")
count_insts = {}

for pair in pairs_file.readlines():
    tmp = pair.split() #split into paper and reviewer
    if (len(tmp) == 1):
        pass
        # first line
    else:
        r = int(tmp[0])
        p = int(tmp[1]) - reviewers
        i = int(insts[r])
        count_insts[(p, i)] += 1

count = 0
for val in count_insts.values():
    count += 0.5 * (val) * (val - 1)

pairs_file.close()
print(count)
