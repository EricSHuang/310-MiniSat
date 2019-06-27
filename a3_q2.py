"""
CMPT310: a3_q2.py
Eric Huang
"""
import os
import time
import a2_q1	#for rand_graph()

def make_ice_breaker_sat(graph, k):
	"""Returns a SAT sentence for the k-Graph Colouring problem that can be inputted into minisat.
	Graph is the friendship graph, and k is the number of possible teams."""
	clauses = []

	#one literal for each (node, colour) pair
	#k literals per node for a total of len(graph)*k literals
	literals = range(1, k*len(graph)+1)
	#print(literals)

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

	#print(sentence)
	return sentence


def writeToFile(string, fileName):
	"""Writes given string to file."""
	file = open(fileName, "w")
	file.write(string)
	file.close()


def find_min_teams(graph):
	"""Uses minisat to find the exact min number of colours needed to colour the graph."""
	k = 1
	unsolved = True
	while (unsolved):
		sentence = make_ice_breaker_sat(graph, k)
		writeToFile(sentence, "min_teams.txt")
		os.system("minisat min_teams.txt out2")
		file = open("out2", "r")

		if (file.readline() == "UNSAT\n"):
			k += 1
		else:
			unsolved = False
			return k


def experiment():
	"""Prints out average solving time and average number of teams."""
	N = 20
	probability = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	#probability = [0.1]
	rounds = 1		#set to 10 for best results

	for p in probability:
		averageMinTeams = 0.0
		averageRunningTime = 0.0
		for i in range(0, rounds):
			graph = a2_q1.rand_graph(N, p)
			startTime = time.time()
			minTeams = find_min_teams(graph)
			#sol = make_ice_breaker_sat(graph, minTeams)
			elapsedTime = time.time() - startTime

			averageMinTeams += minTeams
			averageRunningTime += elapsedTime
			print("Min Teams for %0.1f: %d" %(p, minTeams))
			print("Running Time: %f seconds" %(elapsedTime))

		print("Average Min Teams for %0.1f: %f" %(p, averageMinTeams/rounds))
		print("Average Running Time for %0.1f: %f" %(p, averageRunningTime/rounds))

experiment()

"""
#---Testing make_ice_breaker_sat()---#
#g1 = {0: [1, 2], 1: [0], 2: [0], 3: []}
#make_ice_breaker_sat(g1, 3)

k3 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
k4 = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}

#k3unsat = make_ice_breaker_sat(k3, 2)
#writeToFile(k3unsat, "k3unsat.txt")
#os.system("minisat k3unsat.txt k3unsatOUT")

#k3sat = make_ice_breaker_sat(k3, 3)
#writeToFile(k3sat, "k3sat.txt")
#os.system("minisat k3sat.txt k3satOUT")

#---Testing find_min_teams()---#
#print("min teams for k3: %d" %(find_min_teams(k3)))
#print("min teams for k4: %d" %(find_min_teams(k4)))
"""
