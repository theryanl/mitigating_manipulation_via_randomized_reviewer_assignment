import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time
import random
import sys

""" Runs the normal TPMS objective LP with a randomly generated nxn similarity matrix, with the same upper bound for all reviewer-paper probabilities and the same load constraint across all reviewers. """

Q = float(sys.argv[1]) #upper bound probability of matching
size = int(sys.argv[2]) #side length of similarity matrix
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper

start_time = time.time()
file1 = open("rand_output_no_zeros.txt", "w")
file2 = open("rand_output.txt", "w")

def generate_similarity_matrix(n):
#generate a nxn similarity matrix with entries as uniform(0, 1)
    S = [([0] * n) for i in range(n)]
    for i in range(n):
        for j in range(n):
            S[i][j] = np.random.uniform()
    return S

def generate_mask_matrix(n):
#generate a nxn identity matrix that we use as the mask matrix
    M = [([0] * n) for i in range(n)]
    for i in range(n):
        M[i][i] = 1
    return M

def get_rand_output(Q, n):
    S = generate_similarity_matrix(n)
    M = generate_mask_matrix(n)
    # mask matrix is the conflicts
    
    # the above code is referenced from https://github.com/xycforgithub/StrategyProof_Conference_Review
    
    n = len(S) #num_reviewers
    d = len(S[0]) #num_papers
    for i in range(n):
        file1.write("0\n") #fits the institution template
        file2.write("0\n")
    
    file1.write(f"{n} {d}\n")
    file2.write(f"{n} {d}\n")
    
    A = [([0] * d) for i in range(n)] #creates nxd matrix of 0's
    
    TPMS_score(Q, S, M, A, n, d)
    

def TPMS_score(Q, similarity_matrix, mask_matrix, assignment_matrix, n, d):
#takes as input the max probability for any matching, Q, and outputs the maximized objective value under TPMS.
#k is the upper bound for papers per reviewer
#l is the lower bound for reviewers per paper

#this function was created with reference to the Gurobi quickstart guide for mac on their website.
    
    try:
        
        model = gp.Model("BvN") 
        #ICLR under LP from section 4
        
        gp.setParam("NodefileStart", 0.5)
        ## runs it with less memory usage on higher sized matrices. You can remove this line if you want.
        
        obj = 0
        
        #adding variables to model, while updating objective
        for i in range(n):
            for j in range(d):
                
                #check if variable should be masked
                padded_j = j + n
                if (mask_matrix[i][j] == 1):
                    v = model.addVar(lb = 0, ub = 0, name = f"{i} {padded_j}")
                    
                else:
                    v = model.addVar(lb = 0, ub = Q, name = f"{i} {padded_j}")
                    #upper bound for the weight of the matching is Q
                    
                assignment_matrix[i][j] = v
                
                obj += v * similarity_matrix[i][j]
        
    
        model.setObjective(obj, GRB.MAXIMIZE) #telling Gurobi to maximize obj
        
        for i in range(n):
            papers = 0
            for j in range(d):
                papers += assignment_matrix[i][j]
                
            model.addConstr(papers <= k)
            #each reviewer has k or less papers to review
        
        for j in range(d):
            reviewers = 0
            for i in range(n):
                reviewers += assignment_matrix[i][j]
            
            model.addConstr(reviewers == l)
            #each paper gets exactly l reviews
        
        model.optimize()
        
        for v in model.getVars(): 
            #fitting to the institution template was done earlier in the code
            name = v.varName
            value = v.x
            file2.write(f"{name} {value}\n")
            if (value != 0):
                file1.write(f"{name} {value}\n")
                #writes the matching along with its fractional weight to the output.
    
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
        
    except AttributeError:
        print("Attribute error")
        
        
get_rand_output(Q, size)
file1.close()
file2.close()

time_taken = time.time() - start_time
print("time taken:")
print(time_taken)
