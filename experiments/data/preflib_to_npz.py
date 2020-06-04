import numpy as np
import sys

""" This file converts a {}{}{}-form toi file to the standard npz file that is then used for our main assignment calculations"""

## if you want to change the similarity weights of bids, adjust these
#  constants:
yes_similarity = 4
maybe_similarity = 2
no_similarity = 1

###########################################################################

dataset_name = sys.argv[1] #name of the npz file
preflib_dataset_index = dataset_name[-5] #names of the toi files include an index
dataset = open(dataset_name, "r")
output_file = f"preflib{preflib_dataset_index}"

lines = dataset.readlines()
d = int(lines[0]) #num_papers
n = int(((lines[d + 1]).split(","))[0]) #first entry of the (d+1)th line
#n is num_reviewers

similarity_matrix = [([0] * d) for i in range(n)] #empty similarity matrix
mask_matrix = [([1] * d) for i in range(n)] #start by assuming everything conflicts
#conflicts are not within any of the {} {} {}, so we can set non-conflicts to 0 as we iterate through the sets.


def edit_S_M(L, val, reviewer):
# edits the similarity and mask (conflict) matrix
# entries in L correspond to paper indices
# S[reviewer][paper] is set to val

    for s in (L[:-1]): #looping through everything except last entry
        if (ord(s[-1]) == 125): #does it end with "}"?
            s = s[:-1] #get rid of the "}"
        
        if (len(s) != 0): #sometimes there are empty sets "{}"
            paper = int(s)
            
            similarity_matrix[reviewer][paper] = val
            mask_matrix[reviewer][paper] = 0 #edit mask matrix to remove non-conflicts


for i in range(n): #looping over reviewers
    line = (lines[d + 2 + i]).split("{")
    
    yes = line[1].split(",") #the first {} corresponds to "yes" bids
    edit_S_M(yes, yes_similarity, i)
    
    maybe = line[2].split(",") #the second {} corresponds to "maybe" bids
    edit_S_M(maybe, maybe_similarity, i)
    
    no = line[3].split(",") #the third {} corresponds to "no" bids
    edit_S_M(no, no_similarity, i)

np.savez(output_file, similarity_matrix = similarity_matrix, mask_matrix = mask_matrix) #saves as npz file

dataset.close()