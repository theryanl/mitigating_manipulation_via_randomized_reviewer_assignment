# upper-bounding-pairwise-matching-probability-with-BvN-sampling
This repository contains code to generate a integral assignment of papers to reviewers in an academic conference setting. In particular, it allows for the guarantee that the probability that any pair is matched is at most Q. 

We get our desired assignment by following these 2 steps:

The first step creates a fractional solution to the LP and puts it in "output.txt". This portion requires 
	Gurobi's python package "gurobipy" and Python3.

	For this step, please have a file named "[name].npz" in .npz format containing the similarity matrix under keyword name "similarity_matrix" and conflict matrix under keyword name "mask_matrix". Note, the conflict matrix should have entry 1 if there is a conflict, and 0 otherwise.

	To run the first step and maximize sum-similarity, run the command line (from the core/ directory): python3 ./LP_TPMS.py [name].npz X U Y K Z L
	where X is 0 if you want to set the same upper bound for all reviewer-paper matchings and U is the desired upper bound * 100 (U must be an integer),
	X is 1 if you want to specify the reviewer-paper matchings using a matrix, and U is the name of an npy file containing the matrix of upper-bounds (each multiplied by 100).
	Y is 0 if you want to set the same upper bound for all reviewers' paper loads and K is the upper bound,
	Y is 1 if you want to specify the reviewer loads using a list, and in this case K is the name of an npy file containing the list of upper bounds on the reviewer loads.
	Z is 0 if you want to set the same number for all papers' reviewer loads and L is that number,
	Z is 1 if you want to specify the paper loads using a list, and in this case L is the name of an npy file containing the list of values for the paper loads.

	To maximize the fairness objective, run python3 ./LP_max_min_fairness.py [name].npz X U Y K Z L

	To maximize the sum-similarity and constrain the loads on each paper from each institution, run: python3 ./LP_output_institution_t.py [name].npz X U Y K Z L i t
	where i is an .npz file containing the number of institutions under keyword "num_institutions" and list of a positive integer ID for each reviewer's institution in order under keyword "institution_list"
	and t is the maximum load on each paper from each institution (set to 1 to prevent all same-institution reviewer pairs).

	If you would like to change the upper bound probability on a specific pair of (paper, reviewer), or change the paper load for a reviewer, without inputting the entire matrix/list, you could edit the code following the bolded corresponding comment.

	The output, "output.txt", contains "[num_reviewers] [num_papers]" on the first line, followed by a list of institution IDs in order (positive integers), followed by each possible reviewer-paper pair and the weight assigned to that pair. Note that the indices of papers are padded by the number of reviewers for ease of distinction. If no institutions were input, all reviewers are given institution ID 1.

The second step takes the output and converts the fractional solution to a integral assignment. This 
	portion requires C++.

	For this step, please run the first step beforehand, or have a .txt file of the same format available.

	To run this step, compile bvn.cpp using: g++ -lm bvn.cpp
	Then, run the command line: ./a.out < output.txt > output_bvn.txt

	The integral assignment is now in output_bvn.txt, with the first line being the number of total assigned pairs, and all the following lines reviewer-paper matchings in the assignment. You can get the TPMS and max-min fairness scores for the matching by running:
	
	python3 ../experiments/TPMS_score_from_assignment.py [name].npz output_bvn.txt
	python3 ../experiments/max_min_fairness_from_assignment.py [name].npz output_bvn.txt
