"""
CMPT310: a3_q1.py
Eric Huang
"""


def make_queen_sat(N):
	"""Generates a SAT sentence for the N-Queens problem that can be inputted into miniSAT."""

	#GENERATING THE 'BOARD'
	board = []
	for i in range(0, N):
		row = []
		for j in range(0, N):
			currNum = i*N + j + 1
			row.append(currNum)
		board.append(row)
	#print(board)

	#GENERATING THE CONSTRAINTS
	clauses = []
	
	#Horizontal Constraints
	for row in range(0, N):
		lastNumOnRow = (row+1)*N
		#print("lastNumRow: %d" %(lastNumOnRow))

		for col in range(0, N):
			currNum = row*N + col + 1
			#print(currNum)
			for num in range(currNum+1, lastNumOnRow+1):
				clauses.append("%d %d 0\n" %(currNum, num))
				clauses.append("%d %d 0\n" %(-currNum, -num))

	#Vertical Constraints
	for col in range(0, N):
		lastNumInCol = N*(N-1) + col + 1
		print("lastNumCol: %d" %(lastNumInCol))

		for row in range(0, N):
			currNum = row*N + col +1
			print(currNum)

			for num in range(currNum, lastNumInCol+1, N):
				#print("%d %d 0\n" %(currNum, num))
				if (num != currNum):
					clauses.append("%d %d 0\n" %(currNum, num))
					clauses.append("%d %d 0\n" %(-currNum, -num))

	#Upward Diagonal Constraints
	for num in range(0, N*N):


	#WRITING THE SENTENCE
	#Comment at start stating the problem description
	sentence = "c N=%d queens\n" %(N)

	#Problem Description Line
	numVars = N * N
	sentence += "p cnf %d %d\n" %(numVars, len(clauses))

	#Constraints
	for i in range(0, len(clauses)):
		sentence = sentence + clauses[i]

	print(sentence)


make_queen_sat(4)