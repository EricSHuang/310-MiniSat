"""
CMPT310: a2_q1.py
Eric Huang
"""
from csp import *


def rand_graph(n, p):
    """Returns a new random graph with n nodes numbered 0 to n-1 where every pair of
    nodes is connected with a probability p."""
    
    graph = {}
    #Add one-way friend connections randomly
    for i in range (0, n):
        friends = []
        for j in range (i, n):
            randNum = random.random()
            if (i != j and randNum < p):
                friends.append(j)
        graph[i] = friends

    #Add other side of the friend connections
    for i in range (n, 0, -1):
        for j in range (0, i):
            if (contains(graph[j], i)):
                friendList = graph[i]
                friendList.append(j)
                graph[i] = friendList

    #Sort the friends lists for readability
    for i in range(0, n):
        friendList = graph[i]
        friendList.sort()
        graph[i] = friendList
    return graph

#Returns true if array 'arr' contains element 'x'
def contains(arr, x):
    for element in arr:
        if (element == x):
            return True
    return False


"""
#testing
graph = rand_graph(5, 0.5)
print(graph)
"""
