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
    
    institution_list = []
    for i in range(reviewers):
        institution_list.append(random.randint(1, num_institutions))
    
    np.savez(outfile, num_institutions = num_institutions, \
    institution_list = institution_list) #saves in npz format
