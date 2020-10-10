import numpy as np
import gurobipy as gp
from gurobipy import GRB

# Standard, deterministic assignment
# Return {0, 1} if manipulator was assigned to paper
def standard_assignment(new_S, M, paper, manipulator, k=6, l=3):
    n, d = new_S.shape

    try:
        model = gp.Model("my_model") 
        obj = 0 #objective is the total sum similarity
        A = [([0] * d) for i in range(n)] #A represents assignment
        
        for i in range(n):
            for j in range(d):
                
                if (M[i][j] == 1):
                    v = model.addVar(lb = 0, ub = 0, name = f"{i} {j}")
                else:
                    v = model.addVar(lb = 0, ub = 1, name = f"{i} {j}")
                
                A[i][j] = v
                obj += v * new_S[i][j]
        
        model.setObjective(obj, GRB.MAXIMIZE) #telling Gurobi to maximize obj
        
        for i in range(n):
            papers = 0
            for j in range(d):
                papers += A[i][j]
            model.addConstr(papers <= k) #each reviewer has k or less papers to review
        
        for j in range(d):
            reviewers = 0
            for i in range(n):
                reviewers += A[i][j]
            model.addConstr(reviewers == l) #each paper gets exactly l reviews
        
        model.optimize()
        
        return A[manipulator][paper].x
    
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
    except AttributeError:
        print("Attribute error")

# Randomized assignment
# Return probability of manipulator being assigned to paper
def our_assignment(new_S, M, paper, manipulator, k=6, l=3, upper_bound=0.5):
    n, d = new_S.shape

    try:
        model = gp.Model("my_model") 
        obj = 0 #objective is the total sum similarity
        A = [([0] * d) for i in range(n)] #A represents assignment
        
        for i in range(n):
            for j in range(d):
                
                if (M[i][j] == 1):
                    v = model.addVar(lb = 0, ub = 0, name = f"{i} {j}")
                else:
                    v = model.addVar(lb = 0, ub = upper_bound, name = f"{i} {j}")
                
                A[i][j] = v
                obj += v * new_S[i][j]
        
        model.setObjective(obj, GRB.MAXIMIZE) #telling Gurobi to maximize obj
        
        for i in range(n):
            papers = 0
            for j in range(d):
                papers += A[i][j]
            model.addConstr(papers <= k) #each reviewer has k or less papers to review
        
        for j in range(d):
            reviewers = 0
            for i in range(n):
                reviewers += A[i][j]
            model.addConstr(reviewers == l) #each paper gets exactly l reviews
        
        model.optimize()
        
        return A[manipulator][paper].x
    
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
    except AttributeError:
        print("Attribute error")

# Return, for each paper, a list of non-conflicting reviewers
# ordered by decreasing similarity
def valid_ranked_reviewers_for_all_papers(S, M):
    d = len(S[0])
    result = []
    
    for paper in range(d):
        naive_ranked_reviewers = np.argsort(S[:, paper])
        reversed_reviewers = np.flip(naive_ranked_reviewers)
        
        valid_ranked_reviewers = []
        for reviewer in reversed_reviewers:
            if M[reviewer][paper] == 0:
                valid_ranked_reviewers.append(reviewer)
        result.append(valid_ranked_reviewers)

        for i in range(len(valid_ranked_reviewers) - 1):
            assert(S[valid_ranked_reviewers[i], paper] >= S[valid_ranked_reviewers[i+1], paper])

        
    return np.array(result, dtype=object)

# Return, for each reviewer, a list of non-conflicting papers
# ordered by decreasing similarity
def valid_ranked_papers_for_all_reviewers(S, M):
    n = len(S)
    result = []
   
    for rev in range(n):
        naive_ranked_paps = np.argsort(S[rev, :])
        reversed_paps = np.flip(naive_ranked_paps) # papers in high to low sim order
        
        valid_ranked_paps = []
        for pap in reversed_paps:
            if M[rev][pap] == 0:
                valid_ranked_paps.append(pap)
        result.append(valid_ranked_paps)

        for j in range(len(valid_ranked_paps) - 1):
            assert(S[rev, valid_ranked_paps[j]] >= S[rev, valid_ranked_paps[j+1]])

        
    return np.array(result, dtype=object)


