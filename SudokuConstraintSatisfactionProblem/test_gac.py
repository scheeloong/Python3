#part 1 test on other problems 

from sudoku_csp import *


x = Variable("X", [1,2,3,4])
y = Variable("Y", [1,2,3,4])
z = Variable("Z", [1,2,3,4])
w = Variable("W", [1,2,3,4,5])
 
c1 = Constraint("c1", [x,y,z])
 
for x_0 in x.domain():
    for y_0 in y.domain():
        for z_0 in z.domain():
            if x_0 == y_0 + z_0:
                c1.add_satisfying_tuples([[x_0, y_0, z_0]])
               
 
c2 = Constraint("c2", [x,w])
 
for w_0 in w.domain():
    for x_0 in x.domain():
        if w_0 > x_0:
            c2.add_satisfying_tuples([[x_0, w_0]])
 
 
c3 = Constraint("c3", [x,y,z,w])
 
for w_0 in w.domain():
    for x_0 in x.domain():
        for y_0 in y.domain():
            for z_0 in z.domain():
                if w_0 == x_0 + y_0 + z_0:
                    c3.add_satisfying_tuples([[x_0, y_0, z_0, w_0]])
 
 
conslist = [c1,c2,c3]
varslist = [x,y,z,w]
 
 
varslist2 = []
for i in range(5):
    varslist2.append(Variable("V" + str(i + 1), ["A", "B", "C"]))
v1 = varslist2[0]
v2 = varslist2[1]
v3 = varslist2[2]
v4 = varslist2[3]
v5 = varslist2[4]
 
cv1 = Constraint("C1", [v1,v2,v3])
cv1.add_satisfying_tuples([["A","B","C"],
                           ["B","A","C"],
                           ["A","A","B"]])
cv2 = Constraint("C2", [v1,v3,v4,v5])
cv2.add_satisfying_tuples([["A","A","A","A"],
                           ["A","B","C","B"],
                           ["B","C","B","B"],
                           ["C","A","B","C"],
                           ["C","B","A","B"]])
cv3 = Constraint("C3", [v2,v3,v5])
cv3.add_satisfying_tuples([["A","A","A"],
                           ["A","B","C"],
                           ["B","C","B"],
                           ["C","A","B"],
                           ["C","B","A"]])
 
conslist2 = [cv1, cv2, cv3]
 
def print_all(lst):
    for var in lst:
        var.print_var()
 
               
if not enforce_gac(conslist):
    print("1st problem had DWO") 

print_all(varslist)
 
if not enforce_gac(conslist2): 
    print("2nd problem had DWO") 
 
 
print_all(varslist2)