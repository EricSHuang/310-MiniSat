#TODO: figure out if i need this line later
import a2_q1	#for rand_graph()
import os
import time

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

#See if it should be incorporated into find_min_teams() instead of being a helper function
def writeToFile(string, fileName):
	"""Writes given string to file."""
	file = open(fileName, "w")
	file.write(string)
	file.close()

#TODO: Check this for correctness
def find_min_teams(graph):
	"""Uses minisat to find the exact min number of colours needed to colour the graph."""
	k = 1
	unsolved = True
	while (unsolved):
		sentence = make_ice_breaker_sat(graph, k)
		writeToFile(sentence, "min_teams.txt")
		os.system("minisat min_teams.txt out2")
		file = open("out2", "r")

		if (file.readline() == "UNSAT"):
			k += 1
		else:
			unsolved = False
			return k

#TODO: Check this for correctness
def experiment():
	"""Prints out average solving time and average number of teams."""
	N = 1000
	probability = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	rounds = 10

	for p in probability:
		averageMinTeams = 0.0
		averageRunningTime = 0.0
		for i in range(0, rounds):
			graph = a2_q1.rand_graph(N, p)
			startTime = time.time()
			minTeams = find_min_teams(graph)
			sol = make_ice_breaker_sat(graph, minTeams)
			elapsedTime = time.time() - startTime

			averageMinTeams += minTeams
			averageRunningTime += elapsedTime
			print("Min Teams for %0.1f: %d" %(p, minTeams))
			print("Running Time: %f seconds" %(elapsedTime))

		print("Average Min Teams for %0.1f: %f" %(p, averageMinTeams/rounds))
		print("Average Running Time for %0.1f: %f" %(p, averageRunningTime/rounds))

"""
graphs = []
for probability in range(0.1, 0.9):
	n = 1000
	graphs.append(rand_graph(n, probability))
"""

g1 = {0: [1, 2], 1: [0], 2: [0], 3: []}
make_ice_breaker_sat(g1, 3)
