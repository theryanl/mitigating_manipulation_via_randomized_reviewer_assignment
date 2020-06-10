import random
import math
import numpy as np

def generate_institutions_list(reviewers_per_institution, reviewers):
# generates a random assignment of reviewers to institutions
# each reviewer has an equal probability of being at any institution
# each reviewer is only at one institution
    
    outfile = "institutions"
    
    num_institutions = math.ceil(reviewers/reviewers_per_institution)
    # each institution has only reviewers_per_institution reviewers,
    # so we round up.
    
    # randomly assign reviewers to institutions of appropriate sizes
    institution_list = []
    reviewers_list = np.arange(reviewers)
    np.random.shuffle(reviewers_list)
    reviewers_list = reviewers_list.tolist()
    for i in range(reviewers):
        idx = reviewers_list.index(i)
        inst = int(idx/reviewers_per_institution) + 1
        institution_list.append(inst)
    
    np.savez(outfile, num_institutions = num_institutions, \
    institution_list = institution_list) #saves in npz format


# Put the first k reviewers in inst 1, next k in 2, etc
def write_sequential_institutions(n, k):
    outfile = "institutions"
    
    num_institutions = math.ceil(n/k)
    
    institution_list = []
    for i in range(0, n, k):
        inst = int(i / k) + 1
        for _ in range(k):
            institution_list.append(inst)
    
    np.savez(outfile, num_institutions = num_institutions, \
    institution_list = institution_list)
