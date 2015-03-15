##8-puzzle test cases. 

# This is sort of like the main function to test every function 
# implemented in eightPuzzle. Run this file once fully implemented eightPuzzle 
# Import everything from eight puzzle

"""
# Temporary begin 

from eightPuzzle import *

se = SearchEngine('astar', 'full')

# Test Group 1
eightPuzzle_set_goal([1, 2, 3, 8, 0, 4, 7, 6, 5])
# Easy
# Let s2 be an eightPuzzle object 
s2 = eightPuzzle("START", 0, [1, 2, 3, 8, 4, 0, 7, 6, 5])
                             # h value of Manhattan Distance 
# Make sure default strategy is ASTAR 
print("===========Test 1, EASY, ASTAR, h_MHDist==============")
se.search(s2, eightPuzzle_goal_fn, h_MHDist) 

print("======================================================")

print("===========Test 1, EASY, ASTAR, h_misplacedTiles======")
se.search(s2, eightPuzzle_goal_fn, h_misplacedTiles)

print("======================================================")
# Temporary End 
"""


# Import everything from eight puzzle
from eightPuzzle import *

se = SearchEngine('astar', 'full')

# Test Group 1
eightPuzzle_set_goal([1, 2, 3, 8, 0, 4, 7, 6, 5])
# Easy
s2 = eightPuzzle("START", 0, [1, 3, 4, 8, 6, 2, 7, 0, 5])
                             # h value of Manhattan Distance 
# Make sure default strategy is ASTAR 
print("===========Test 1, EASY, ASTAR, h_MHDist==============")
se.search(s2, eightPuzzle_goal_fn, h_MHDist) 

print("======================================================")

print("===========Test 1, EASY, ASTAR, h_misplacedTiles======")
se.search(s2, eightPuzzle_goal_fn, h_misplacedTiles)

print("======================================================")


# Medium 1
s3 = eightPuzzle("START", 0, [2, 8, 1, 0, 4, 3, 7, 6, 5])

print("===========Test 1, MEDIUM 1, ASTAR, h_MHDist==============")
se.search(s3, eightPuzzle_goal_fn, h_MHDist)
print("======================================================")

print("===========Test 1, MEDIUM 1, ASTAR, h_misplacedTiles======")
se.search(s3, eightPuzzle_goal_fn, h_misplacedTiles)
print("======================================================")

# Medium 2
s4 = eightPuzzle("START", 0, [2, 8, 1, 4, 6, 3, 0, 7, 5])
print("===========Test 1, MEDIUM 2, ASTAR, h_MHDist==============")
se.search(s4, eightPuzzle_goal_fn, h_MHDist)
print("======================================================")

print("===========Test 1, MEDIUM 2, ASTAR, h_misplacedTiles======")
se.search(s4, eightPuzzle_goal_fn, h_misplacedTiles)
print("======================================================")

# Hard
s5 = eightPuzzle("START", 0, [5, 6, 7, 4, 0, 8, 3, 2, 1])
print("===========Test 1, HARD, ASTAR, h_MHDist==============")
se.search(s5, eightPuzzle_goal_fn, h_MHDist)
print("======================================================")

print("===========Test 1, HARD, ASTAR, h_misplacedTiles======")
se.search(s5, eightPuzzle_goal_fn, h_misplacedTiles)
print("======================================================")

# Test Group 2
eightPuzzle_set_goal([1, 2, 3, 4, 5, 6, 7, 8, 0])
se.set_strategy('astar')

# Hard
s9 = eightPuzzle("START", 0, [3, 6, 0, 5, 7, 8, 2, 1, 4])
print("===========Test 2, HARD, ASTAR, h_MHDist======")
se.search(s9, eightPuzzle_goal_fn, h_MHDist)
print("======================================================")

print("===========Test 2, HARD, ASTAR, h_misplacedTiles======")
se.search(s9, eightPuzzle_goal_fn, h_misplacedTiles)
print("======================================================")
