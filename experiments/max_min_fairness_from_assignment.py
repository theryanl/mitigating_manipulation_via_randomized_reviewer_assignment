import numpy as np
import sys

# Reads in an assignment file and outputs the fairness of this assignment

# part of this are referenced from https://github.com/xycforgithub/StrategyProof_Conference_Review
my_dataset = sys.argv[1] #dataset
assignment = sys.argv[2] #integral assignment

scores = np.load(my_dataset, allow_pickle=True)
S = scores["similarity_matrix"]

reviewers = len(S)
papers = len(S[0])

pairs_file = open(assignment, "r")

paper_similarities = [0] * papers

for pair in pairs_file.readlines():
    tmp = pair.split() #split into paper and reviewer
    if (len(tmp) == 1):
        pass
        # first line
    else:
        r = int(tmp[0])
        p = int(tmp[1]) - reviewers
        paper_similarities[p] += S[r][p] #add similarity to paper's total similarity

lowest = paper_similarities[0]

for item in paper_similarities:
    if (item < lowest):
        lowest = item

pairs_file.close()
print(f'{lowest}')
