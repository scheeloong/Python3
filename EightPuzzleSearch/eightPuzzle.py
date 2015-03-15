#Look for #IMPLEMENT tags in this file. These tags indicate changes in the 
#file to implement the required routines. 


'''8-Puzzle STATESPACE 
'''
from search import *

class eightPuzzle(StateSpace):
    StateSpace.n = 0
    
    def __init__(self, action, gval, state, parent = None):
        '''Create an 8-puzzle state object.
        The parameter state represents the puzzle configuration as a list of 9 numbers in the range [0-8] 
        The 9 numbers specify the position of the tiles in the puzzle from the
        top left corner, row by row, to the bottom right corner. E.g.:

        [2, 4, 5, 0, 6, 7, 8, 1, 3] represents the puzzle configuration

        |-----------|
        | 2 | 4 | 5 |
        |-----------|
        |   | 6 | 7 |
        |-----------|
        | 8 | 1 | 3 |
        |-----------|
        '''
        #Note we represent the puzzle configuration in the state member.
        #the list of tile positions.
        StateSpace.__init__(self, action, gval, parent)
        self.state = state

    def successors(self) :
#IMPLEMENT
        '''Implement the actions of the 8-puzzle search space.'''
        #   IMPORTANT. The list of successor states returned must be in the ORDER
        #   Move blank down move, move blank up, move blank right, move blank left
        #   (with some successors perhaps missing if they are not available
        #   moves from the current state, but the remaining ones in this  
        #   order!)
        
        # state is a list of 9 numbers 
        States = list()
        
        # 1. Move Blank Down 
        for i in range(0,6): 
            if self.state[i] == 0: 
                #stateNew = self.state # this creates a reference not a new variable  
                stateNew = self.state[:]  # this creates a copy of state 
                stateNew[i] = self.state[i+3]
                stateNew[i+3] = self.state[i]
                States.append( eightPuzzle('Blank-Down', self.gval+1, stateNew, self))        
        
        # 2. Move Blank Up 
        for i in range(3,9): 
            if self.state[i] == 0: 
               # stateNew = self.state      
                stateNew = self.state[:]  # this creates a copy of state 
                stateNew[i] = self.state[i-3]
                stateNew[i-3] = self.state[i]
                States.append( eightPuzzle('Blank-Up', self.gval+1, stateNew, self))          
    
        # 3. Move Blank Right 
        for i in range(0,9):
            if self.state[i] == 0: 
                col = i % 3 
                if col != 2:
                  #  stateNew = self.state     
                    stateNew = self.state[:]  # this creates a copy of state 
                    stateNew[i] = self.state[i+1]
                    stateNew[i+1] = self.state[i]
                    States.append( eightPuzzle('Blank-Right', self.gval+1, stateNew, self))            
        
        # 4. Move Blank Left 
        for i in range(0,9):
            if self.state[i] == 0: 
                col = i % 3 
                if col != 0:
                    #stateNew = self.state 
                    stateNew = self.state[:]  # this creates a copy of state 
                    stateNew[i] = self.state[i-1]
                    stateNew[i-1] = self.state[i]
                    States.append( eightPuzzle('Blank-Left', self.gval+1, stateNew, self))  
        return States 
    def hashable_state(self) :
        # This would just be the list of 9 numbers configuration 
        # as each of them would be unique 
#IMPLEMENT
        #Attempt 1
        return (self.state[0], self.state[1], self.state[2], self.state[3], self.state[4], self.state[5], self.state[6], self.state[7], self.state[8])
        
        # Attempt 2
        specialSum = 0 
        for i in range(0,9): 
            specialSum = specialSum + ((9 ** i) * self.state[i])
        #return (0, specialSum)
        return str(specialSum) 

        # Attempt 3 
        #return self.state
        #return "Superman"
    
    def print_state(self):
#DO NOT CHANGE THIS METHOD
        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[0],self.state[1],self.state[2]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[3],self.state[4],self.state[5]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[6],self.state[7],self.state[8]))
        print("|-----------|")

#Set up the goal.
#We allow any full configuration of the puzzle to be a goal state. 
#We use the class variable "eightPuzzle.goal_state" to store the goal configuration. 
#The goal test function compares a state's configuration with the goal configuration

eightPuzzle.goal_state = False # A class variable not defined inside the class 

def eightPuzzle_set_goal(state):
    '''set the goal state to be state. Here state is a list of 9
       numbers in the same format as eightPuzzle.___init___'''
    eightPuzzle.goal_state = state

def eightPuzzle_goal_fn(state):
    return (eightPuzzle.goal_state == state.state)

def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

#return the number of tiles (NOT INCLUDING THE BLANK) in state that are not in their goal 
#position. (will need to access the class variable eigthPuzzle.goal_state)
def h_misplacedTiles(state):
#IMPLEMENT
    numMisplaced = 0 # initialize numMisplaced to 0 
    for i in range(0,9):
        if eightPuzzle.goal_state[i] != 0:
            if state.state[i] != eightPuzzle.goal_state[i]: 
                numMisplaced = numMisplaced + 1
    return numMisplaced 

# for case statement below
def h_MHDistCaseGetXPos(x):
    return {
         0 : 0, 
         1 : 0,
         2 : 0, 
         3 : 1, 
         4 : 1, 
         5 : 1, 
         6 : 2, 
         7 : 2, 
         8 : 2, 
    }[x]

def h_MHDistCaseGetyPos(y):
    return y % 3 
    
def h_MHDist(state):
    #return the sum of the manhattan distances each tile (NOT INCLUDING
    #THE BLANK) is from its goal configuration. 
    #The manhattan distance of a tile that is currently in row i column j
    #and that has to be in row x column y in the goal is defined to be
    #  abs(i - x) + abs(j - y)
    sumManhattan = 0 # intialize sumManhatten to 0 
    for i in range(0,9):
        for j in range(0,9):
            if eightPuzzle.goal_state[j] != 0:
                if eightPuzzle.goal_state[j] == state.state[i]:
                    # set the x and y values based on value of i 
                        x = h_MHDistCaseGetXPos(i)
                        y = h_MHDistCaseGetyPos(i) 
                    
                    # set the a and b value based on value of j 
                        a = h_MHDistCaseGetXPos(j)
                        b = h_MHDistCaseGetyPos(j) 
                    
                        currDistance = abs(a - x) + abs(b - y)
                        sumManhattan = sumManhattan + currDistance
    return sumManhattan 