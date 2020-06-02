import random
import math
import numpy as np

def generate_institutions_list(reviewers_per_institution, reviewers):
    
    outfile = "institutions"
    
    num_institutions = math.ceil(reviewers/reviewers_per_institution)
    
    institution_list = []
    for i in range(reviewers):
        institution_list.append(random.randint(1, num_institutions))
    
    np.savez(outfile, num_institutions = num_institutions, \
    institution_list = institution_list)

#reviewers_per_institution = 5
#n = 31 
#generate_institutions_list(reviewers_per_institution, n)
