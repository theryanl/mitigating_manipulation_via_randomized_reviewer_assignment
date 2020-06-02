import numpy as np
import sys

# part of this are referenced from https://github.com/xycforgithub/StrategyProof_Conference_Review
my_dataset = sys.argv[1] #dataset
assignment = sys.argv[2] #integral assignment

scores = np.load(my_dataset, allow_pickle=True)
S = scores["similarity_matrix"]

reviewers = len(S)
papers = len(S[0])

pairs_file = open(assignment, "r")

score = 0

for pair in pairs_file.readlines():
    tmp = pair.split() #split into paper and reviewer
    if (len(tmp) == 1):
        pass
        # first line
    else:
        r = int(tmp[0])
        p = int(tmp[1]) - reviewers
        score += S[r][p] #summing up similarities

pairs_file.close()
print(f'{score}')
