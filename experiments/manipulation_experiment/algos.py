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


