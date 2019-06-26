#TODO: figure out if i need this line later
#import a2_q1	#for rand_graph()

def make_ice_breaker_sat(graph, k):
	"""Returns a SAT sentence for the k-Graph Colouring problem that can be inputted into minisat.
	Graph is the friendship graph, and k is the number of possible teams."""
	clauses = []

	#one literal for each (node, colour) pair
	#k literals per node for a total of len(graph)*k literals
	literals = range(1, k*len(graph)+1)
	print(literals)

	#-----CONSTRAINTS-----#
	#Each node must be assigned a colour
	for node in graph:
		clause = ""
		for i in range(0, k):
			clause += "%d "%(literals[node*k + i])
		clause += "0\n"
		clauses.append(clause)


	#Each node can only be ONE colour
	for i in range(0, len(literals), k):
		for j in range(0, k):
			# a -> (~b ∧ ~c ∧ ...) = (~a V ~b) ∧ (~a V ~c) ∧ ...
			colouredLit = literals[i+j]
			for l in range(j+1, k):
				# b -> ~a = ~b V ~a = ~a V ~b = a -> ~b (ie duplicates)
				clause = "%d %d 0\n" %(-colouredLit, -literals[i+l])
				#print(clause)
				clauses.append(clause)


	#Connected nodes cannot have the same colour
	for node in graph:
		connections = graph[node]
		#print (connections)
		for edge in connections:
			#print(edge)
			if (edge > node):
				for colour in range(0, k):
					c1 = literals[node*k + colour]
					c2 = literals[edge*k + colour]
					clause = "%d %d 0\n" %(-c1, -c2)
					clauses.append(clause)



	#-----WRITING THE SENTENCE-----#
	#Comment stating the problem description
	sentence = "c k=%d Graph Colouring Problem\n" %(k)
	#Problem Description
	sentence += "p cnf %d %d\n" %(len(literals), len(clauses))
	#Constraints
	for i in range(0, len(clauses)):
		sentence += clauses[i]

	print(sentence)
	return sentence

"""
graphs = []
for probability in range(0.1, 0.9):
	n = 1000
	graphs.append(rand_graph(n, probability))
"""

g1 = {0: [1, 2], 1: [0], 2: [0], 3: []}
make_ice_breaker_sat(g1, 3)
