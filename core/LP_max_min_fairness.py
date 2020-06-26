import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time
import sys

my_filename = sys.argv[1] #npz containing similarity matrix and conflict matrix
is_upper_bound = int(sys.argv[2])

if (is_upper_bound == 0):
    upper_bound = int(sys.argv[3]) 
    #upper bound on all matchings (multiplied by 100)
else:
    M_name = sys.argv[3]
    upper_bound_matrix = np.load(M_name, allow_pickle = True)

is_reviewer_load_fixed = int(sys.argv[4])

if (is_reviewer_load_fixed == 0):
    k = int(sys.argv[5]) #k is the upper bound for papers per reviewer
else:
    reviewer_loads_name = sys.argv[5]
    reviewer_load_list = np.load(reviewer_loads_name, allow_pickle = True)
    
is_paper_load_fixed = int(sys.argv[6])

if (is_paper_load_fixed == 0):
    l = int(sys.argv[7]) #l is the number of reviewers per paper
else:
    paper_loads_name = sys.argv[7]
    paper_load_list = np.load(paper_loads_name, allow_pickle = True)

start_time = time.time()
file = open("output.txt", "w")

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
    
    file.write(f"{n} {d}\n")
    #output has "num_reviewers num_papers" as its first line
    
    A = [([0] * d) for i in range(n)] 
    #creates n x d matrix of 0's to represent assignment
    
    if (is_upper_bound == 0):
        solve_fractional_LP(upper_bound/100, S, M, A, n, d)
    else:
        solve_fractional_LP(upper_bound_matrix, S, M, A, n, d)
    

def solve_fractional_LP(Q, similarity_matrix, mask_matrix, assignment_matrix, n, d):
#takes as input all the information of the assignment problem, constructs an LP, and uses Gurobi to solve the LP.

#this function was created with reference to the Gurobi quickstart guide for mac on their website.
    
    try:
        
        model = gp.Model("my_model") 
        obj = model.addVar(lb = 0, name = "min_similarity")
        
        #adding variables to model, while updating objective
        for j in range(d):
            paper_similarity = 0
            #total similarity for the paper
            
            for i in range(n):
                
                padded_j = j + n
                #padding the papers to be distinct numbers from the reviewers
                
                #check if variable should be masked
                if (mask_matrix[i][j] == 1):
                    v = model.addVar(lb = 0, ub = 0, name = f"{i} {padded_j}")
                else:
                    if (is_upper_bound == 0):
                        v = model.addVar(lb = 0, ub = Q, name = f"{i} {padded_j}") #upper bound for the weight of the matching is Q
                    else: 
                        v = model.addVar(lb = 0, ub = (Q[i][j])/100, name = f"{i} {padded_j}") #upper bound specified in the matrix
                    
                    ##if you want to set an upper bound on a specific matching
                    # you would do so here with
                    # v = model.addVar(lb = 0, ub = [new bound], name = f"{i} {padded_j}")
                    # inside an if statement
                    
                assignment_matrix[i][j] = v
                paper_similarity += v * similarity_matrix[i][j]
            
            model.addConstr(obj <= paper_similarity)
            #objective is <= all paper total similarities
            #this way, when we maximize the objective, it is the minimum of the paper total similarities
        
        model.setObjective(obj, GRB.MAXIMIZE) #telling Gurobi to maximize obj
        
        for i in range(n):
            papers = 0
            for j in range(d):
                papers += assignment_matrix[i][j]
            
            if (is_reviewer_load_fixed == 0):
                model.addConstr(papers <= k) 
                #each reviewer has k or less papers to review
            else:
                model.addConstr(papers <= load_list[i])
            
            ##if you want to set different amounts of papers for a few reviewers
            # you would do so here with
            # model.addConstr(papers <= new_amount)
            # inside an if statement
        
        
        for j in range(d):
            reviewers = 0
            for i in range(n):
                reviewers += assignment_matrix[i][j]
            
            if (is_paper_load_fixed == 0):
                model.addConstr(reviewers == l)
                #each paper gets exactly l reviews
            else:
                model.addConstr(reviewers == paper_load_list[j])
        
        model.optimize()

        for v in range(n):
            file.write("1\n")
            #This file does not account for different institutions
            #so to fit it with our bvn program parsing we have everyone set to institution 1.
            
        for v in model.getVars():
            name = v.varName
            value = v.x
            if (ord(name[0]) != 109): 
            #do not need to write min similarity variable
                file.write(f"{name} {value}\n")
                #writes the matching along with its fractional weight to the output.
        
        print(model.objVal) #the objective value
        
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
        
    except AttributeError:
        print("Attribute error")
        

get_output()
file.close()
time_taken = time.time() - start_time
print("time taken:", time_taken)
