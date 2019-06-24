import a2_q1	#for rand_graph()

def make_ice_breaker_sat(graph, k):
	"""Returns a SAT sentence for the chromatic-number problem that can be inputted into minisat.
	Graph is the friendship graph, and k is the number of possible teams."""
	clauses = []

	numVars = 1
	for node in range(0, len(graph)):
		#one literal for each (node, colour) pair
		literals = []
		for i in range(0, k):
			literals.append(numVars + i)

		#each node must be assigned a colour
		clause = ""
		for i in range(0, k):
			clause += "%d "%(literals[i])




graphs = []
for probability in range(0.1, 0.9):
	n = 1000
	graphs.append(rand_graph(n, probability))

