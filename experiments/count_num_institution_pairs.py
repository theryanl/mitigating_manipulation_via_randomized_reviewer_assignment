import numpy as np
import sys

# Counts the number of same-institution reviewers assigned to the same paper
# in the given assignment
def count_num_institution_pairs(assignment, inst_file):
    inst_data = np.load(inst_file)
    insts = inst_data['institution_list'] # drop number of institutions entry
    
    reviewers = len(insts)

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
            if (p, i) in count_insts:
                count_insts[(p, i)] += 1
            else:
                count_insts[(p, i)] = 1
    
    count = 0
    for val in count_insts.values():
        count += 0.5 * (val) * (val - 1)
    
    pairs_file.close()
    return count
