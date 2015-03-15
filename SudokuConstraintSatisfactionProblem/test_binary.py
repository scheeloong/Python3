from cspbase import *
from sudoku_csp2 import *

def create_variables(board):
    i = 1
    variable_matrix = []
    for row in board:
        j = 1
        variable_row = []
        for cell in row:
            if cell == 0:
                variable_row.append(Variable("V{}{}".format(i, j), range(1,10)))
            else:
                variable_row.append(Variable("V{}{}".format(i, j), [cell]))
            j += 1
        variable_matrix.append(variable_row)
        i += 1
    return variable_matrix

def create_tuples(dom1, dom2):
    tuples = []
    for v1 in dom1:
        for v2 in dom2:
            if v1 != v2:
                tuples.append([v1,v2])
    return tuples

def extract_column(i, j, matrix):
    col = [matrix[i][j]]
    i += 1
    while i < 9:
        col.append(matrix[i][j])
        i += 1
    return col

def extract_sub_square(i,j,matrix):
    sub_square = [matrix[i][j]]
    i += 1
    while i%3 != 0:
        col = j - j%3
        while (col%3 != 0) or (col <= j):
            if col != j:
                sub_square.append(matrix[i][col])
            col += 1
        i += 1
    return sub_square

def add_binary_constraints(variables):
    constraints = []
    var1 = variables[0]
    i = 1
    while i < len(variables):
        var2 = variables[i]
        c = Constraint("C_{}{}".format(var1.name, var2.name), [var1, var2])
        c.add_satisfying_tuples(create_tuples(c.scope[0].domain(), c.scope[1].domain()))
        constraints.append(c)
        i += 1
    return constraints

def create_binary_constraints(variables):
    constraints = []
    for row in variables:
        for cell in row:
            # create the row constraints
            constraints += add_binary_constraints(row[row.index(cell):])
            # create the column constraints
            column = extract_column(variables.index(row), row.index(cell), variables)
            constraints += add_binary_constraints(column)
            # create the sub-square constraints
            sub_square = extract_sub_square(variables.index(row), row.index(cell), variables)
            constraints += add_binary_constraints(sub_square)
    return constraints

def print_solution(solution):
    for row in solution:
        print(row)

b1 = [[0,0,2,0,9,0,0,6,0], [0,4,0,0,0,1,0,0,8], [0,7,0,4,2,0,0,0,3], [5,0,0,0,0,0,3,0,0], [0,0,1,0,6,0,5,0,0],  [0,0,3,0,0,0,0,0,6], [1,0,0,0,5,7,0,4,0], [6,0,0,9,0,0,0,2,0], [0,2,0,0,8,0,1,0,0]]

b3 = [[0,4,0,0,0,0,0,0,0],[0,0,2,0,5,0,7,0,0],[0,8,6,0,0,2,0,0,0],[0,1,0,9,0,3,0,0,6],[0,2,0,0,4,0,0,7,0],[3,0,0,2,0,5,0,4,0],[0,0,0,8,0,0,4,1,0],[0,0,9,0,1,0,6,0,0],[0,0,0,0,0,0,0,5,0]]

var = sudoku_enforce_gac_model_1(b3)

print_solution(var)

