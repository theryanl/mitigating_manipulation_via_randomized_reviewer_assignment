import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time
import sys
import random

my_filename = sys.argv[1] #npz containing similarity matrix and conflict matrix
p = float(sys.argv[2]) #probability that a paper has no conflict
k = int(sys.argv[3]) #k is the upper bound for papers per reviewer
l = int(sys.argv[4]) #l is the number of reviewers per paper

start_time = time.time()
file = open("output.txt", "w")

def add_random_conflicts(M, num_conflicts, n, d):
    for reviewer in range(n):
        L = random.sample(range(d), num_conflicts)
        for conflict in L:
            M[reviewer][conflict] = 1
    return M

def get_output():
# get_output disassembles the npz, finds number of reviewers & papers, and 
# calls solve_fractional_LP to finish the job.

# parts of this function are referenced from https://github.com/xycforgithub/StrategyProof_Conference_Review

    scores = np.load(my_filename, allow_pickle=True)
    S = scores["similarity_matrix"]
    M = scores["mask_matrix"]
    # mask matrix is the conflict matrix. 
    # each entry is 0 or 1, with 1 meaning there is a conflict.
    
    n = len(S) #number of reviewers
    d = len(S[0]) #number of papers
    
    papers_available = int((d * p)//1)
    updated_M = add_random_conflicts(M, d - papers_available, n, d)
    
    file.write(f"{n} {d}\n")
    #output has "num_reviewers num_papers" as its first line
    
    A = [([0] * d) for i in range(n)] 
    #creates n x d matrix of 0's to represent assignment
    
    solve_fractional_LP(S, updated_M, A, n, d)
    

def solve_fractional_LP(similarity_matrix, mask_matrix, assignment_matrix, n, d):
#takes as input all the information of the assignment problem, constructs an LP,
#and uses Gurobi to solve the LP.

#this function was created with reference to the Gurobi quickstart guide for mac
#on their website.
    
    try:
        
        model = gp.Model("my_model") 
        obj = 0 #objective is the total sum similarity
        
        #adding variables to model, while updating objective
        for i in range(n):
            for j in range(d):
                
                padded_j = j + n
                #padding the papers to be distinct numbers from the reviewers
                
                #check if variable should be masked
                if (mask_matrix[i][j] == 1):
                    v = model.addVar(lb = 0, ub = 0, name = f"{i} {padded_j}")
                else:
                    v = model.addVar(lb = 0, ub = 1, name = f"{i} {padded_j}")
                    
                    ##if you want to set an upper bound on a specific matching
                    # you would do so here with
                    # v = model.addVar(lb = 0, ub = [new bound], name = f"{i} {padded_j}")
                    # inside an if statement
                    
                assignment_matrix[i][j] = v
                obj += v * similarity_matrix[i][j]
        
    
        model.setObjective(obj, GRB.MAXIMIZE) #telling Gurobi to maximize obj
        
        for i in range(n):
            papers = 0
            for j in range(d):
                papers += assignment_matrix[i][j]
                
            model.addConstr(papers <= k) 
            #each reviewer has k or less papers to review
            
            ##if you want to set different amounts of papers for a few reviewers
            # you would do so here with
            # model.addConstr(papers <= new_amount)
            # inside an if statement
        
        
        for j in range(d):
            reviewers = 0
            for i in range(n):
                reviewers += assignment_matrix[i][j]
            
            model.addConstr(reviewers == l)
            #each paper gets exactly l reviews
        
        model.optimize()
        
        for v in model.getVars():
            name = v.varName
            value = v.x
            file.write(f"{name} {value}\n")
            #writes the matching along with its fractional weight to the output.
        
        print(model.objVal)
    
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
        
    except AttributeError:
        print("Attribute error")
        

get_output()
file.close()
time_taken = time.time() - start_time
print("time taken:", time_taken)