import numpy as np
import sys

dataset_name = sys.argv[1]
preflib_dataset_index = dataset_name[-5]
dataset = open(dataset_name, "r")
output_file = f"preflib{preflib_dataset_index}"

lines = dataset.readlines()
d = int(lines[0])
n = int(((lines[d + 1]).split(","))[0]) #first entry of the (d+1)th line

similarity_matrix = [([0] * d) for i in range(n)]
mask_matrix = [([1] * d) for i in range(n)] #start by assuming everything conflicts

def edit_S_M(L, val, reviewer):
    for s in (L[:-1]): #looping through everything except last entry
        if (ord(s[-1]) == 125): #does it end with "}"?
            s = s[:-1]
        
        if (len(s) != 0):
            paper = int(s)
            
            similarity_matrix[reviewer][paper] = val
            mask_matrix[reviewer][paper] = 0 #edit mask matrix to remove non-conflicts

for i in range(n): #looping over reviewers
    line = (lines[d + 2 + i]).split("{")
    yes = line[1].split(",")
    
    edit_S_M(yes, 4, i)
    
    maybe = line[2].split(",")
    edit_S_M(maybe, 2, i)
    
    no = line[3].split(",")
    edit_S_M(no, 1, i)

np.savez(output_file, similarity_matrix = similarity_matrix, mask_matrix = mask_matrix)

dataset.close()