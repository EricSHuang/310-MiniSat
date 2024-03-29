"""
CMPT310: a3_q1.py
Eric Huang
"""
import math
import os
import time

def make_queen_sat(N):
	"""Generates a SAT sentence for the N-Queens problem that can be inputted into miniSAT."""

	#-----GENERATING THE BOARD-----#
	board = []
	for i in range(0, N):
		row = []
		for j in range(0, N):
			currNum = i*N + j + 1
			row.append(currNum)
		board.append(row)
	#print(board)

	#-----GENERATING CONSTRAINTS-----#
	clauses = []

	#Horizontal Constraints
	for row in range(0, N):
		lastNumOnRow = board[row][N-1]
		#print("lastNumRow: %d" %(lastNumOnRow))

		for col in range(0, N):
			currNum = board[row][col]
			#print(currNum)

			for num in board[row]:
				#print(board[row])
				if (currNum < num):
					clauses.append("%d %d 0\n" %(-currNum, -num))

		#At least one var per row must be true
		oneTrue = ""
		for num in board[row]:
			oneTrue += "%d " %(num)
		oneTrue += "0\n"
		clauses.append(oneTrue)

	#Vertical Constraints
	for col in range(0, N):
		firstNumInCol = board[0][col]
		lastNumInCol = board[N-1][col]
		#print("lastNumCol: %d" %(lastNumInCol))

		for row in range(0, N):
			currNum = board[row][col]
			#print(currNum)

			for num in range(currNum, lastNumInCol+1, N):
				if (num != currNum):
					clauses.append("%d %d 0\n" %(-currNum, -num))

		#At least one var per column must be true
		oneTrue = ""
		for num in range(firstNumInCol, lastNumInCol+1, N):
			oneTrue += "%d " %(num)
		oneTrue += "0\n"
		clauses.append(oneTrue)

	#Upward Sloping Diagonal Constraints
	for i in range(0, N*2):
		diagonal = []
		#Extracting the diagonal numbers line by lune
		for j in range(0, i+1):
			k = i - j
			if (k < N and j < N):
				diagonal.append(board[k][j])

		#print(diagonal)
		if (len(diagonal) > 1):
			for i in range(0, len(diagonal)):
				currNum = diagonal[i]
				for j in range(i+1, len(diagonal)):
					clauses.append("%d %d 0\n" %(-currNum, -diagonal[j]))

	#Downward Sloping Diagonal Constraints
	for i in range(-N, N):
		diagonal = []
		for j in range(0, N):
			if ((j-i >= 0) and (j-i < N)):
				diagonal.append(board[j][j-i])

		#print(diagonal)
		if (len(diagonal) > 1):
			for i in range(0, len(diagonal)):
				currNum = diagonal[i]
				for j in range(i+1, len(diagonal)):
					clauses.append("%d %d 0\n" %(-currNum, -diagonal[j]))



	#-----WRITING THE SENTENCE-----#
	#Comment stating the problem description
	sentence = "c N=%d Queens\n" %(N)

	#Problem Description
	numVars = N * N
	sentence += "p cnf %d %d\n" %(numVars, len(clauses))

	#Constraints
	for i in range(0, len(clauses)):
		sentence = sentence + clauses[i]

	#print(sentence)
	return sentence


def draw_queen_sat_sol(sol):
	sentence = sol.split()

	if (sentence[0] == "UNSAT"):
		print("No solution.")
		return
	else:
		sentence.remove("SAT")
		sentence.remove("0")	#Removes the terminating 0 at the end of sol
		N = int(math.sqrt(len(sentence)))
		print("N : %d" %(N))

	if (len(sentence) > 41):
		#"SAT" + N = 41 elements
		print("Too Big: N must be less than 40")
		return

	else:
		line = ""
		for i in range(0, N):
			line += "----"
		print(line)	#Top of Board

		#Board Contents
		for row in range(0, N):
			currRow = ""
			for col in range(0, N):
				num = row*N + col
				if (int(sentence[num]) < 0):
					currRow += "|   "
				else: currRow += "| Q "
			currRow += "|"
			print(currRow)
			print(line)
		return


def writeToFile(string, fileName):
	"""Writes given string to file."""
	file = open(fileName, "w")
	file.write(string)
	file.close()


def experiment():
	"""Determines the max value for N that minisat can solve in 10seconds or less"""
	solvableInTime = True
	N = 0
	runningTimes = []
	while(solvableInTime):
		queenSAT = make_queen_sat(N)
		writeToFile(queenSAT, "queenSAT.txt")
		startTime = time.time()
		os.system('minisat queenSAT.txt out')
		elapsedTime = time.time() - startTime

		if (elapsedTime > 10):
			solvableInTime = False
			"""
			#Print out the running time for each n
			for i in range(1, N+1):
				print("N = %d running time: %0.6f" %(i, runningTimes[i]))
			print("MAX N: %d" %(N))
			"""
			return N
		else:
			runningTimes.append(elapsedTime)
			N += 1


maxN = experiment()

"""
#Testing
#make_queen_sat(4)
testSol = "SAT -1 -2 3 -4 5 -6 -7 -8 -9 -10 -11 12 -13 14 -15 -16 0"
draw_queen_sat_sol(testSol)
"""
