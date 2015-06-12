from bnetbase import *
'''
#Two sample bayes nets are defined in this file. 
VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
F1 = Factor("F1", [VisitAsia])
F1.add_values([['visit', 0.01], ['no-visit', 0.99]])

Smoking = Variable('Smoking', ['smoker', 'non-smoker'])
F2 = Factor("F2", [Smoking])
F2.add_values([['smoker', 0.5], ['non-smoker', 0.5]])


Tuberculosis = Variable('Tuberculosis', ['present', 'absent'])
F3 = Factor("F3", [Tuberculosis, VisitAsia])
F3.add_values([['present', 'visit', 0.05],
               ['present', 'no-visit', 0.01],
               ['absent', 'visit', 0.95],
               ['absent', 'no-visit', 0.99]])

Cancer = Variable('Lung Cancer', ['present', 'absent'])
F4 = Factor("F4", [Cancer, Smoking])
F4.add_values([['present', 'smoker', 0.10],
               ['present', 'non-smoker', 0.01],
               ['absent', 'smoker', 0.90],
               ['absent', 'non-smoker', 0.99]])

Bronchitis = Variable('Bronchitis', ['present', 'absent'])
F5 = Factor("F5", [Bronchitis, Smoking])
F5.add_values([['present', 'smoker', 0.60],
               ['present', 'non-smoker', 0.30],
               ['absent', 'smoker', 0.40],
               ['absent', 'non-smoker', 0.70]])

TBorCA = Variable('Tuberculosis or Lung Cancer', ['true', 'false'])
F6 = Factor("F6", [TBorCA, Tuberculosis, Cancer])
F6.add_values([['true', 'present', 'present', 1.0],
               ['true', 'present', 'absent', 1.0],
               ['true', 'absent', 'present', 1.0],
               ['true', 'absent', 'absent', 0],
               ['false', 'present', 'present', 0],
               ['false', 'present', 'absent', 0],
               ['false', 'absent', 'present', 0],
               ['false', 'absent', 'absent', 1]])


Dyspnea = Variable('Dyspnea', ['present', 'absent'])
F7 = Factor("F7", [Dyspnea, TBorCA, Bronchitis])
F7.add_values([['present', 'true', 'present', 0.9],
               ['present', 'true', 'absent', 0.7],
               ['present', 'false', 'present', 0.8],
               ['present', 'false', 'absent', 0.1],
               ['absent', 'true', 'present', 0.1],
               ['absent', 'true', 'absent', 0.3],
               ['absent', 'false', 'present', 0.2],
               ['absent', 'false', 'absent', 0.9]])


Xray = Variable('XRay Result', ['abnormal', 'normal'])
F8 = Factor("F8", [Xray, TBorCA])
F8.add_values([['abnormal', 'true', 0.98],
               ['abnormal', 'false', 0.05],
               ['normal', 'true', 0.02],
               ['normal', 'false', 0.95]])

Asia = BN("Asia", [VisitAsia, Smoking, Tuberculosis, Cancer,
                   Bronchitis, TBorCA, Dyspnea, Xray],
          [F1, F2, F3, F4, F5, F6, F7, F8])

## E,B,S,w,G example from sample questions
E = Variable('E', ['e', '-e'])
B = Variable('B', ['b', '-b'])
S = Variable('S', ['s', '-s'])
G = Variable('G', ['g', '-g'])
W = Variable('W', ['w', '-w'])
FE = Factor('P(E)', [E])
FB = Factor('P(B)', [B])
FS = Factor('P(S|E,B)', [S, E, B])
FG = Factor('P(G|S)', [G,S])
FW = Factor('P(W|S)', [W,S])

FE.add_values([['e',0.1], ['-e', 0.9]])
FB.add_values([['b', 0.1], ['-b', 0.9]])
FS.add_values([['s', 'e', 'b', .9], ['s', 'e', '-b', .2], ['s', '-e', 'b', .8],['s', '-e', '-b', 0],
               ['-s', 'e', 'b', .1], ['-s', 'e', '-b', .8], ['-s', '-e', 'b', .2],['-s', '-e', '-b', 1]])
FG.add_values([['g', 's', 0.5], ['g', '-s', 0], ['-g', 's', 0.5], ['-g', '-s', 1]])
FW.add_values([['w', 's', 0.8], ['w', '-s', .2], ['-w', 's', 0.2], ['-w', '-s', 0.8]])

testQ4 = BN('SampleQ4', [E,B,S,G,W], [FE,FB,FS,FG,FW])

#Using Bayes net ``testQ4'' (see example_bn.py)

###(a) What is the probablity of S given G='g'?
B.set_evidence('b')
print(VE(testQ4, E, [B]))
#>>>[1.0, 0.0]
##That is, P(s|g) = 1.0, P(-s|g) = 0.0

G.set_evidence('g')
print(VE(testQ4,S,[G])) 

###(b) What is the probability of G given S='s'?
S.set_evidence('s')
print(VE(testQ4, G, [S]))
#>>[0.5, 0.5]

###(c) What is the probability of G given S='-s'?
S.set_evidence('-s')
print(VE(testQ4, G, [S]))
#>>[0.0, 1.0]

#For (b) and (c) P(g|s) = 0.5, P(-g|s) = 0.5 
#                P(g|-s) = 0.0, P(-g|-s) = 1.0

###(d) Now we try two items in evidence, S='s' /\ W='w'
###    and we want to compute the probability of G (given S='s' /\ W='w')
S.set_evidence('s')
W.set_evidence('w')
print(VE(testQ4, G, [S,W]))
#>>[0.5, 0.5]

###(e) Similar to (d) but now W='-w'

S.set_evidence('s')
W.set_evidence('-w')
print(VE(testQ4, G, [S,W]))
#>>[0.5, 0.5]
##i.e., P(g|s,-w) = 0.5, P(-g|s,-w) = 0.5

###(f)
S.set_evidence('-s')
W.set_evidence('w')
print (VE(testQ4, G, [S,W]))
#>>[0.0, 1.0]
##i.e., P(g|-s,w) = 0.0, P(-g|-s,w) = 1.0

###(g)
S.set_evidence('-s')
W.set_evidence('-w')
print (VE(testQ4, G, [S,W]))
#>>[0.0, 1.0]
##i.e., P(g|-s,-w) = 0.0, P(-g|-s,-w) = 1.0

###(h)
W.set_evidence('w')
print (VE(testQ4, G, [W]))
#>>[0.15265998457979954, 0.8473400154202004]

##P(g|w) = 0.15, P(-g|w) = 0.84 (Note that numerical rounding issues occur)

###(i)
W.set_evidence('-w')
print (VE(testQ4, G, [W]))
#>>[0.01336753983256819, 0.9866324601674318]

##P(g|-w) = 0.01, P(-g|w) = 0.99
'''
print("CSC384 Winter 2015 Assignment 3 Question 1") 

A = Variable('A', ['a', '-a'])
B = Variable('B', ['b', '-b'])
C = Variable('C', ['c', '-c'])
D = Variable('D', ['d', '-d'])
E = Variable('E', ['e', '-e'])
F = Variable('F', ['f', '-f'])
G = Variable('G', ['g', '-g'])
H = Variable('H', ['h', '-h'])
I = Variable('I', ['i', '-i'])

FA = Factor('P(A)', [A])
FH = Factor('P(H)', [H])
FG = Factor('P(G)', [G])
FF = Factor('P(F)', [F])

FB = Factor('P(B|A,H)', [B,A,H])
FI = Factor('P(I|B)', [I,B])
FC = Factor('P(C|B,G)', [C,B,G])
FE = Factor('P(E|C)', [E,C])
FD = Factor('P(D|C,F)', [D,C,F])

FA.add_values([['a',0.9], ['-a', 0.1]])
FH.add_values([['h',0.5], ['-h', 0.5]])
FG.add_values([['g',1.0], ['-g', 0.0]])
FF.add_values([['f',0.1], ['-f', 0.9]])

FI.add_values([['i', 'b', 0.3], ['-i', 'b', 0.7], ['i', '-b', 0.9], ['-i', '-b', 0.1]])
FE.add_values([['e', 'c', 0.2], ['-e', 'c', 0.8], ['e', '-c', 0.4], ['-e', '-c', 0.6]])

FB.add_values([['b', 'a', 'h', 1.0], ['-b', 'a', 'h', 0.0], ['b', 'a', '-h', 0.0],['-b', 'a', '-h', 1.0],
               ['b', '-a', 'h', 0.5], ['-b', '-a', 'h', 0.5], ['b', '-a', '-h', 0.6],['-b', '-a', '-h', 0.4]])

FC.add_values([['c', 'b', 'g', 0.9], ['-c', 'b', 'g', 0.1], ['c', 'b', '-g', 0.9],['-c', 'b', '-g', 0.1],
               ['c', '-b', 'g', 0.1], ['-c', '-b', 'g', 0.9], ['c', '-b', '-g', 1.0],['-c', '-b', '-g', 0.0]])

FD.add_values([['d', 'c', 'f', 0.0], ['-d', 'c', 'f', 1.0], ['d', 'c', '-f', 1.0],['-d', 'c', '-f', 0.0],
               ['d', '-c', 'f', 0.7], ['-d', '-c', 'f', 0.3], ['d', '-c', '-f', 0.2],['-d', '-c', '-f', 0.8]])


testQ1 = BN('Q1', [A,B,C,D,E,F,G,H,I], [FA,FB,FC,FD,FE,FF,FG,FH,FI])

print('a) Pr(b|a)') 
A.set_evidence('a')
Q1a = VE(testQ1, B, [A])
print(Q1a[0]) # Want b = true 

#temp = VE(testQ1, A, [])
#print(temp[0]) 

print('b) Pr(c|a)') 
A.set_evidence('a')
Q1b = VE(testQ1, C, [A])
print(Q1b[0]) # Want c = true

print('c) Pr(c|a,-e)') 
A.set_evidence('a')
E.set_evidence('-e')
Q1c = VE(testQ1, C, [A, E])
print(Q1c[0])

print('d) Pr(c|a,-f)') 
A.set_evidence('a')
F.set_evidence('-f')
Q1d = VE(testQ1, C, [A, F])
print(Q1d[0])

#print('P(g|-s,w) = {} P(-g|-s,w) = {} P(g|-s,-w) = {} P(-g|-s,-w) = {}'.format(probs3[0],probs3[1],probs4[0],probs4[1]))

