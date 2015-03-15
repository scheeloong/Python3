# Soon Chee Loong
# 999295793
# c4soonch 
# University of Toronto 
from cspbase import *
import itertools # for itertools.permutations()
import sys
#-------------------------------------------------------------------------------
# Helper Functions  
#-------------------------------------------------------------------------------
# This function gets the initial board configuration 
# and returns a list of variables, where it should be 81 of them 
def makeVariables(initialSudokuBoard):
    # Initialize the variables to return 
    VariablesCreated = [] 
    indexRow = 1
    # For each row 
    for row in initialSudokuBoard: 
        indexCol = 1 
        # Initialize the columns of variables for this row 
        variableRow  = []
        # Get each list of values for that position 
        for cell in row: 
            # If that cell is empty, which means it's equal to 0 
            if not cell: 
                variableRow.append(Variable("V{}{}".format(indexRow, indexCol), range(1,10)))
            # Else, create the domain as only that value 
            else: 
                variableRow.append(Variable("V{}{}".format(indexRow, indexCol), [cell]))
            indexCol += 1 
        VariablesCreated.append(variableRow)
        indexRow += 1 
    return VariablesCreated

def makeVariablesEmpty(initialSudokuBoard):
    # Initialize the variables to return 
    VariablesCreated = [] 
    indexRow = 1
    # For each row 
    for row in initialSudokuBoard: 
        indexCol = 1 
        # Initialize the columns of variables for this row 
        variableRow  = []
        # Get each list of values for that position 
        for cell in row: 
            variableRow.append(Variable("V{}{}".format(indexRow, indexCol), []))
            indexCol += 1 
        VariablesCreated.append(variableRow)
        indexRow += 1 
    return VariablesCreated

#-------------------------------------------------------------------------------
# These are helper functions for createBinaryNotEqualConstraints() 
#-------------------------------------------------------------------------------

def createBinarySatisfyingTuples(domainVariableOne, domainVariableTwo):
    satisfyingTuples = []
    for valueOne in domainVariableOne:
        for valueTwo in domainVariableTwo:
            if valueOne != valueTwo:
                satisfyingTuples.append([valueOne,valueTwo])
    return satisfyingTuples

def makeBinaryConstraintHelper(varOne, varTwo):
    listOfConstraints = [] 
    newConstraint = Constraint("BinaryCons{}{}".format(varOne.name, varTwo.name), [varOne, varTwo])
    newConstraint.add_satisfying_tuples(createBinarySatisfyingTuples(newConstraint.scope[0].domain(), newConstraint.scope[1].domain()))
    listOfConstraints.append(newConstraint) 
    return listOfConstraints
    

def makeBinaryRowConstraints(rowList):
    rowConstraint = [] # initialize the rowOfConstraints 
    for variableOne in rowList: 
        for variableTwo in rowList: 
            if rowList.index(variableOne) < rowList.index(variableTwo):
                rowConstraint += makeBinaryConstraintHelper(variableOne, variableTwo)
    return rowConstraint 
            
def makeBinaryColConstraints(listOfVariables, rowIndex, colIndex): 
    colConstraint = [] # initialize the colOfConstraints
    colList = [] # Initialize the colList to create 
    # Get the column from the current cell's index from the listOfVariables 
    index = rowIndex 
    while rowIndex < len(listOfVariables):
        colList.append(listOfVariables[rowIndex][colIndex])
        rowIndex += 1 
    # Now, create and add the colConstraint similar to rowConstraints since arranged similarly 
    colConstraint += makeBinaryRowConstraints(colList) 
    # return the created column Constraint 
    return colConstraint 
    
def makeBinarySubSquareConstraints(listOfVariables, rowIndex, colIndex): 
    subSquareConstraint = [] # Initialize the subSquareConstraints 
    # First, generate the subSquareList
    subSquareList = [listOfVariables[rowIndex][colIndex]] # initialize with the element at listOfVariables[rowIndex][colIndex] itself 
    rowIndex += 1 # Skip the current column itself 
    # Continue looping till past the rows below current row but doesn't extend to next sub-square 
    while rowIndex%3 != 0: # Don't go into next bottom sub-square 
        leftMostCol = colIndex - colIndex%3 # Get the leftmost columns in the current sub-square 
        # Make sure it does not go to current column number 
        # note: take into account it has to be less than colIndex to be able to handle 
        # while loop ends when you enter next subcell or the next subcell is greater than the current subcell!
        # This means, it will go through all appropriate columns to compare with before nextSubCell 
        while (leftMostCol%3 != 0) or (leftMostCol <= colIndex): 
            #                             # But, it handles the case where you can view the others in the same cell!!!!! 
            if leftMostCol != colIndex: # Don't add with the same column itself 
                subSquareList.append(listOfVariables[rowIndex][leftMostCol])
            leftMostCol += 1
        rowIndex += 1    
    # Now, create the constraints similar to rowConstraints 
    subSquareConstraint += makeBinaryRowConstraints(subSquareList) 
    return subSquareConstraint

#-------------------------------------------------------------------------------
# These are helper functions for createAllDifferentConstraints() 
#-------------------------------------------------------------------------------

# Get the domain values from the listOfVariables given 
def getDomFromVar(listOfVariables):
    dom = []
    for variable in listOfVariables:
        values = variable.domain()
        if len(values) == 1:
            dom.append(values[0])
        else:
            dom.append(0)
    return dom

def getColumns(listOfVariables):
    colList = []
    i = 0
    while i < 9:
        j = 0
        newColumn = [listOfVariables[j][i]]
        j += 1
        while j < 9:
            newColumn.append(listOfVariables[j][i])
            j += 1
        colList.append(newColumn)
        i += 1
    return colList

def getSubSquares(listOfVariables):
    subSquareList = []
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            sub = [] 
            indexRow = i
            while indexRow%3 != 0 or indexRow <= i:
                indexCol = j
                while indexCol%3 != 0 or indexCol <= j:
                    sub.append(listOfVariables[indexRow][indexCol])
                    indexCol += 1
                indexRow += 1
            subSquareList.append(sub)
            j += 3
        i += 3    
    return subSquareList

def createAllDiffSatisfyingTuples(rowList):
    forPermute = []
    for num in range(1,10):
        if num not in rowList:
            forPermute.append(num)
    permutations = itertools.permutations(forPermute) # find all possible permutations 
    tupleList = []
    # For each possible permutation 
    for eachPerm in permutations:
        # Make a copy of the rowList 
        newTuple = rowList[:]
        # For each value of the permutation 
        for value in eachPerm:
            # Put it in the next slot of value 0 
            newTuple[newTuple.index(0)] = value
        # Add the tuple to the list of satisfying tuples 
        tupleList.append(newTuple)
    return tupleList    

#-------------------------------------------------------------------------------
# This function returns the list of all possible BinaryNotEqual Constraints 
# from the listOfVariables for the sudoku problem 
# Note: It is problem specific for the Sudoku problem as it only creates 810 binary constraints 
def createBinaryNotEqualConstraints(listOfVariables):
    listOfConstraints = []
    for row in listOfVariables:
        for cell in row:
            # create the binary constraints from rows and add it to the list of constraints 
            listOfConstraints += makeBinaryRowConstraints(row[row.index(cell):])
            # create the binary constraints from cols and add it to the list of constraints 
            listOfConstraints += makeBinaryColConstraints(listOfVariables, listOfVariables.index(row), row.index(cell))
            # create the binary constraints from sub-squares and add it to the list of constraints 
            listOfConstraints += makeBinarySubSquareConstraints(listOfVariables, listOfVariables.index(row), row.index(cell))
    return listOfConstraints

# This function returns the list of all possible All-Different Constraints 
# from the listOfVariables for the sudoku problem 
# Note: It is problem specific for the Sudoku problem as it only creates 27 All-Different constraints 
def createAllDifferentConstraints(initial_sudoku_board, listOfVariables):
    listOfConstraints = []
    # First, create the row constraints 
    i = 0 # A counter for naming 
    for row in listOfVariables:
        newConstraint = Constraint("AllDiffConsR{}".format(i+1), row)
        newConstraint.add_satisfying_tuples(createAllDiffSatisfyingTuples(initial_sudoku_board[i]))
        listOfConstraints.append(newConstraint)
        i += 1        
    # Now, handle the column constraints 
    # create the column constraints
    columns = getColumns(listOfVariables)
    i = 0
    for col in columns:
        newConstraint = Constraint("AllDiffConsC{}".format(i+1), col)
        newConstraint.add_satisfying_tuples(createAllDiffSatisfyingTuples(getDomFromVar(col)))
        listOfConstraints.append(newConstraint)
        i += 1    
    # Finally, handle the subsquare constraints 
    # create the subSquares
    i = 0
    subSquares = getSubSquares(listOfVariables)
    for sub in subSquares:
        newConstraint = Constraint("AllDiffConsS{}".format(i+1), sub)
        newConstraint.add_satisfying_tuples(createAllDiffSatisfyingTuples(getDomFromVar(sub)))
        listOfConstraints.append(newConstraint)
        i += 1    
    return listOfConstraints

#-------------------------------------------------------------------------------
# This function returns the variables formatted in the proper way for output 
def formatVariables(listOfVariables):
    formattedOutput = []
    for row in listOfVariables:
        rowSolution = []
        for cell in row:
            rowSolution.append(cell.cur_domain())
        formattedOutput.append(rowSolution)
    return formattedOutput
#-------------------------------------------------------------------------------
# This function returns: 
# True if all the variables had their values pruned properly by GAC 
# False if any of the variables had all their values pruned => Domain Wipe Out 
def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then 
       enforce GAC on them pruning values from the variables in the scope of
       these constraints. Return False if a DWO is detected. Otherwise, return True. 
       The pruned values will be removed from the variable object's cur_domain.
       enforce_gac modifies the variable objects that are in the scope of
       the constraints passed to it.'''
    changed = True # initialize with variables being pruned 
    while changed: 
        changed = False # set to false so that while loop ends if nothing happens 
        # For every constraint in the constraint list 
        for constraint in constraint_list:
            # for each variable in each constraint's list of variables 
            for variable in constraint.scope: 
                # Check if each value in the current domain has a support
                for value in variable.cur_domain(): 
                    # If it does not, prune that value away 
                    if not constraint.has_support(variable, value):
                        variable.prune_value(value)
                        changed = True # updated change so have to run GAC on every variable again 
                        # Check if pruning this variable result in a Domain Wipe Out 
                        # If the current domain size is 0 
                        if not variable.cur_domain_size(): 
                            return False 
    return True # return true if no values are pruned (changed)  

#-------------------------------------------------------------------------                

# Solve the sudoku problem using: 
# A list of binary constraints of NOT_EQUAL => V1 != V2, etc. 
# Note: For 9 x 9 sudoku board:
# i) Generating constraints repeatedly results in : 1944 constraints
# ii) Generating constraints repeatedly only for the subcells part: 972 constraints
# iii) Generating constraints without duplicates: 810 (means no such thing as (V1,V2) & (V2,V1) duplicated pair in the total amount 
# Basically, first generate all the binary constraints
# Then, prune all the variable values with enforce_gac() above applied on a list of all binary constraints 
# It accepts the board position: 
# means need to initialize domain to (1,2,...,9) if that cell is empty (has value 0) 
# and initialize domain to (i) if that cell has value i 
def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1 to 9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       In model_1 you should create a variable for each cell of the
       board, with domain equal to {1-9} if the board has a 0 at that
       position, and domain equal {i} if the board has a fixed number i
       at that cell. 
       
       Model_1 should create BINARY CONSTRAINTS OF NOT-EQUAL between all
       relevant variables (e.g., all pairs of variables in the same
       row, etc.), then invoke enforce_gac on those constraints. All of the
       constraints of Model_1 MUST BE binary constraints (i.e.,
       constraints whose scope includes two and only two variables).

       After creating all variables and constraints you can invoke
       your enforce_gac routine to obtain the GAC reduced current domains
       of the variables.
       
       The output should have the same layout as the input: a list of
       nine lists each representing a row of the board. However, now the
       numbers in the positions of the input list are to be replaced by
       LISTS which are the corresponding cell's pruned domain (current
       domain) AFTER gac has been performed.
       
       For example, if GAC failed to prune any values the output from
       the above input would result in an output would be: NOTE I HAVE
       PADDED OUT ALL OF THE LISTS WITH BLANKS SO THAT THEY LINE UP IN
       TO COLUMNS. Python would not output this list of lists in this
       format.
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8]],
       [[1,2,3,4,5,6,7,8,9],[                7],[1,2,3,4,5,6,7,8,9],[                4],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3]],
       [[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9],[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6]],
       [[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                5],[                7],[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9]],
       [[                6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains SO THIS WOULD
       NOT BE the outputted list.
       
       '''
    # Create the variables given the board 
    # There should be 81 variables on the 9x9 boards
    # First, create the binary constraints
    # Go through each row and create the constraint for that row 
    listOfVariables = makeVariables(initial_sudoku_board)
    emptyList = makeVariablesEmpty(initial_sudoku_board) # Return an empty list as all variables will be pruned 

    # Now, use the list of variables to create all 810 binary Constraints
    listOfConstraints = createBinaryNotEqualConstraints(listOfVariables)
    # Now, use enforce_gac() on the variables and constraints created 
    if not enforce_gac(listOfConstraints): # If Domain Wipe Out occurs, don't prune and give original bounds variables 
        return formatVariables(emptyList) # note: This means there is no solution in the variables 
    # Otherwise, if successful, return variables itself formatted to show the domains of each variable 
    else: 
        return formatVariables(listOfVariables)
##############################

# This function solves the Sudoku board using the 27 all-different constraint 
def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists
    specifying the board, and generates the same format output as
    sudoku_enforce_gac_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''
    
    # Create the variables given the board 
    # There should be 81 variables on the 9x9 boards
    # First, create the binary constraints
    # Go through each row and create the constraint for that row 
    listOfVariables = makeVariables(initial_sudoku_board)
    emptyList = makeVariablesEmpty(initial_sudoku_board) # Return an empty list as all variables will be pruned 
    # Now, use the list of variables to create all 27 All-Different Constraints
    listOfConstraints = createAllDifferentConstraints(initial_sudoku_board, listOfVariables)    
    # Now, use enforce_gac() on the variables and constraints created 
    if not enforce_gac(listOfConstraints): # If Domain Wipe Out occurs, give all bounds as fully pruned, (empty list) 
        return formatVariables(emptyList) # note: This means there is no solution in the variables 
    # Otherwise, if successful, return variables itself formatted to show the domains of each variable 
    else: 
        return formatVariables(listOfVariables)
