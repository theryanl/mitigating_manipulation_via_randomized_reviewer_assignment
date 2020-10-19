This directory contains files to run the bidding-manipulation experiments in the paper.

manipulation.py runs the manipulation experiment on the iclr dataset. Run with the following command line arguments.
	- argument 1: "standard" or "randomized", selects the assignment algorithm
	- argument 2: "bids" or "nobids", selects whether the honest reviewers should bid
	- argument 3: scale for bidding (integer)
	- argument 4 (optional): "manip" (default) or "nomanip", selects whether the malicious reviewer should bid

The results can be plotted using the functions in plotter.py.

The results in the paper can be recreated with the calls:
	- python manipulation.py standard bids 2
	- python manipulation.py randomized bids 2
	- python manipulation.py standard bids 4
	- python manipulation.py randomized bids 4
	- python manipulation.py standard bids 2 nomanip
	- python manipulation.py standard bids 4 nomanip
along with appropriate calls to the plotting functions.
