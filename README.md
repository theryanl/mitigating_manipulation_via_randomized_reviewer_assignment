# upper-bounding-pairwise-matching-probability-with-BvN-sampling
This repository contains code to generate a integral assignment of papers to reviewers in an academic conference setting. In particular, it allows for the guarantee that the probability that any pair is matched is at most Q. 

We get our desired assignment by following these 2 steps:

The first step creates a fractional solution to the LP and puts it in "output.txt". This portion requires 
	Gurobi's python package "gurobipy" and Python3.

	For this step, please have a file named "[name].npz" in .npz format containing the similarity matrix under keyword name "similarity_matrix" and conflict matrix under keyword name "mask_matrix". Note, the conflict matrix should have entry 1 if there is a conflict, and 0 otherwise.

	To run the first step, run the command line: python3 ./LP_output.py [name].npz U K L
	where U is the desired upper bound * 100 (U must be an integer)
    	  K is the upper bound for papers per reviewer
    	  L is the number of reviewers per paper

	If you would like to change the upper bound probability on a specific pair of (paper, reviewer), or change the paper load for a reviewer, you could edit the code following the bolded corresponding comment.

	The output, "output.txt", contains "[num_reviewers] [num_papers]" on the first line, followed by each possible pair and the weight assigned to that pair. Note that the indices of papers are padded by the number of reviewers for ease of distinction.

The second step takes the output and converts the fractional solution to a integral assignment. This 
	portion requires C++.

	For this step, please run the first step beforehand, or have a .txt file of the same format available.

	To run this step, compile bvn.cpp using: g++ -lm bvn.cpp
				 Then, run the command line: ./a.out < output.txt > output_bvn.txt

	The integral assignment is now in output_bvn.txt, with the first line being the number of total assigned pairs, and all the following lines reviewer-paper matchings in the assignment.

	Note: this step has random elements, so running it a few times and using the assignment with the highest sum similarity may yield minor increases in total sum similarity.

(Optional) Finding the total sum similarity of a matching
	
	To find the total sum similarity of an outputted matching, run the command line: python3 ./TPMS_score_from_assignment.py [name].npz output_bvn.txt

	To find the total sum similarity if there were no constraints on the matchings, run ONLY the first step with U = 100. The second-to-last line of the console output will report the optimal objective, which is what is desired.
