from bnetbase import *
# Refer to Assignmnet3.pdf for the graph of how everything relates to each other. 

# Create a variable called Alternator
# with values: [okay, faulty] 
al = Variable("Alternator", ['okay', 'faulty'])
# Create a factor for the alternator variable  
F1 = Factor("P(al)", [al])
# Add probability values for each of the possible values in the domain of the alternator variable 
F1.add_values(
    [['okay', 0.997],
     ['faulty', 0.003]])

# Create another variable called Charging System that can either be okay or faulty 
cs = Variable("Charging system",  ['okay', 'faulty'])
# Create a factor for this Charging system variable given the Alternator variable 
# This factors take in both bn_variable Charging System and Alternator
F2 = Factor("P(cs|al)", [cs, al])
# Add the probability values for Charging System given the Alternator varable 
F2.add_values(
    [['okay', 'okay', 0.5],
     ['faulty', 'okay', 0.5],
     
     ['okay', 'faulty', 0],
     ['faulty', 'faulty', 1]])

#---------------------------------------------------------------------
ba = Variable("Battery age", ['new', 'old', 'very_old'])
F3 = Factor("P(ba)", [ba])
F3.add_values(
    [['new', 0.4], 
     ['old', 0.4], 
     ['very_old', 0.2]])

bv = Variable("Battery voltage", ['strong', 'weak', 'dead'])
F4 = Factor("P(bv|cs,ba)", [bv, cs, ba])
F4.add_values(
    [['strong', 'okay', 'new', 0.95],
     ['weak', 'okay', 'new', 0.04],
     ['dead', 'okay', 'new', 0.01],
     
     ['strong', 'okay', 'old', 0.8],
     ['weak', 'okay', 'old', 0.15],
     ['dead', 'okay', 'old', 0.05],
     
     ['strong', 'okay', 'very_old', 0.6],
     ['weak', 'okay', 'very_old', 0.3],
     ['dead', 'okay', 'very_old', 0.1],
     
     ['strong', 'faulty', 'new', 0.008],
     ['weak', 'faulty', 'new', 0.3],
     ['dead', 'faulty', 'new', 0.692],
    
     ['strong', 'faulty', 'old', 0.004],
     ['weak', 'faulty', 'old', 0.2],
     ['dead', 'faulty', 'old', 0.796],
    
     ['strong', 'faulty', 'very_old', 0.002],
     ['weak', 'faulty', 'very_old', 0.1],
     ['dead', 'faulty', 'very_old', 0.898]])


mf = Variable("Main fuse", ['okay', 'blown'])
F5 = Factor("P(mf)", [mf])
F5.add_values(
    [['okay', 0.99],
    ['blown', 0.01]])

ds = Variable("Distributer", ['okay', 'faulty'])
F6 = Factor("P(ds)", [ds])
F6.add_values(
    [['okay', 0.99],
     ['faulty', 0.00999999]])

pv = Variable("Voltage at plug", ['strong', 'weak', 'none'])
# Choices domain are (3, 2, 2, 3) => 3 * 2 * 2 * 3 = 36 => 36 possible values 
F7 = Factor("P(pv|mf,ds,bv)", [pv, mf, ds, bv])
F7.add_values([
     # Note: Each value of it's own domain given any configuration(evidence) must sum to 1! 
     ['strong', 'okay', 'okay', 'strong', 0.9],
     ['weak', 'okay', 'okay', 'strong', 0.05],
     ['none', 'okay', 'okay', 'strong', 0.05],

     ['strong', 'okay', 'okay', 'weak', 0.0],
     ['weak', 'okay', 'okay', 'weak', 0.9],
     ['none', 'okay', 'okay', 'weak', 0.1], 

     ['strong', 'okay', 'okay', 'dead', 0],
     ['weak', 'okay', 'okay', 'dead', 0],
     ['none', 'okay', 'okay', 'dead', 1], 

     ['strong', 'okay', 'faulty', 'strong', 0.1],
     ['weak', 'okay', 'faulty', 'strong', 0.1],
     ['none', 'okay', 'faulty', 'strong', 0.8],

     ['strong', 'okay', 'faulty', 'weak', 0],
     ['weak', 'okay', 'faulty', 'weak', 0.1],
     ['none', 'okay', 'faulty', 'weak', 0.9], 

     ['strong', 'okay', 'faulty', 'dead', 0],
     ['weak', 'okay', 'faulty', 'dead', 0],
     ['none', 'okay', 'faulty', 'dead', 1], 

     ['strong', 'blown', 'okay', 'strong', 0],
     ['weak', 'blown', 'okay', 'strong', 0],
     ['none', 'blown', 'okay', 'strong', 1],

     ['strong', 'blown', 'okay', 'weak', 0],
     ['weak', 'blown', 'okay', 'weak', 0],
     ['none', 'blown', 'okay', 'weak', 1],

     ['strong', 'blown', 'okay', 'dead', 0],
     ['weak', 'blown', 'okay', 'dead', 0],
     ['none', 'blown', 'okay', 'dead', 1],

     ['strong', 'blown', 'faulty', 'strong', 0],
     ['weak', 'blown', 'faulty', 'strong', 0],
     ['none', 'blown', 'faulty', 'strong', 1],

     ['strong', 'blown', 'faulty', 'weak', 0],
     ['weak', 'blown', 'faulty', 'weak', 0],
     ['none', 'blown', 'faulty', 'weak', 1],

     ['strong', 'blown', 'faulty', 'dead', 0],
     ['weak', 'blown', 'faulty', 'dead', 0],
     ['none', 'blown', 'faulty', 'dead', 1]])

sm = Variable("Starter Motor", ['okay', 'faulty'])
F8 = Factor("P(sm)", [sm])
F8.add_values([
    ['okay', 0.995],
    ['faulty', 0.004999995]]) # why not just 0.005?

ss = Variable("Starter system", ['okay', 'faulty'])
F9 = Factor("P(ss)", [ss, mf, sm, bv])
F9.add_values([
    ['okay', 'okay', 'okay', 'strong', 0.98], 
    ['faulty', 'okay', 'okay', 'strong', 0.02], 
    
    ['okay', 'okay', 'okay', 'weak', 0.9], 
    ['faulty', 'okay', 'okay', 'weak', 0.1], 
    
    ['okay', 'okay', 'okay', 'dead', 0.1], 
    ['faulty', 'okay', 'okay', 'dead', 0.9], 

    ['okay', 'okay', 'faulty', 'strong', 0.02], 
    ['faulty', 'okay', 'faulty', 'strong', 0.98], 

    ['okay', 'okay', 'faulty', 'weak', 0.01], 
    ['faulty', 'okay', 'faulty', 'weak', 0.99], 

    ['okay', 'okay', 'faulty', 'dead', 0.005], 
    ['faulty', 'okay', 'faulty', 'dead', 0.995], 

    ['okay', 'blown', 'okay', 'strong', 0], 
    ['faulty', 'blown', 'okay', 'strong', 1], 

    ['okay', 'blown', 'okay', 'weak', 0], 
    ['faulty', 'blown', 'okay', 'weak', 1], 

    ['okay', 'blown', 'okay', 'dead', 0], 
    ['faulty', 'blown', 'okay', 'dead', 1], 

    ['okay', 'blown', 'faulty', 'strong', 0], 
    ['faulty', 'blown', 'faulty', 'strong', 1], 

    ['okay', 'blown', 'faulty', 'weak', 0], 
    ['faulty', 'blown', 'faulty', 'weak', 1], 

    ['okay', 'blown', 'faulty', 'dead', 0], 
    ['faulty', 'blown', 'faulty', 'dead', 1]])

hl = Variable("Headlights", ['bright', 'dim', 'off'])
F10 = Factor("P(hl|bv", [hl, bv])
F10.add_values([
		 ['bright', 'strong', 0.94],
		 ['dim',    'strong', 0.01],
		 ['off',    'strong', 0.05],

		 ['bright', 'weak', 0],
		 ['dim',    'weak', 0.95],
		 ['off',    'weak',  0.05],

		 ['bright',  'dead', 0],
		 ['dim',     'dead', 0],
		 ['off',     'dead', 1]])

sp = Variable("Spark plugs", ['okay', 'too_wide', 'fouled'])
F11 = Factor("P(sp)", [sp])
F11.add_values([
    ['okay', 0.7],
    ['too_wide', 0.1],
    ['fouled', 0.2]])

sq = Variable("Spark quality", ['good', 'bad', 'very_bad'])
F12 = Factor("P(sq|sp,pv)", [sq, sp, pv])
F12.add_values([
        ['good',     'okay', 'strong', 1],
        ['bad' ,     'okay', 'strong', 0],
        ['very_bad', 'okay', 'strong', 0], 
    	
    	['good',     'okay', 'weak', 0],
        ['bad' ,     'okay', 'weak', 1],
        ['very_bad', 'okay', 'weak', 0],             

    	['good',     'okay', 'none', 0],
        ['bad' ,     'okay', 'none', 0],
        ['very_bad', 'okay', 'none', 1],

        ['good',     'too_wide', 'strong', 0],
        ['bad' ,     'too_wide', 'strong', 1],
        ['very_bad', 'too_wide', 'strong', 0], 
    	
    	['good',     'too_wide', 'weak', 0],
        ['bad' ,     'too_wide', 'weak', 0],
        ['very_bad', 'too_wide', 'weak', 1],             

    	['good',     'too_wide', 'none', 0],
        ['bad' ,     'too_wide', 'none', 0],
        ['very_bad', 'too_wide', 'none', 1],

        ['good',     'fouled', 'strong', 0],
        ['bad' ,     'fouled', 'strong', 1],
        ['very_bad', 'fouled', 'strong', 0], 
    	
    	['good',     'fouled', 'weak', 0],
        ['bad' ,     'fouled', 'weak', 0],
        ['very_bad', 'fouled', 'weak', 1],             

    	['good',     'fouled', 'none', 0],
        ['bad' ,     'fouled', 'none', 0],
        ['very_bad', 'fouled', 'none', 1]])

cc = Variable("Car cranks", ['true', 'false'])
F13 = Factor("P(cc|ss)", [cc, ss])
F13.add_values([
    ['true',  'okay', 0.8],
    ['false', 'okay', 0.2],

    ['true',  'faulty', 0.05], 
    ['false', 'faulty', 0.95]])

tm = Variable("Spark timing", ['good', 'bad', 'very_bad'])
F14 = Factor("P(tm|ds)", [tm, ds])
F14.add_values([
    ['good',     'okay',  0.9],
    ['bad',      'okay', 0.09],
    ['very_bad', 'okay', 0.01],

    ['good',     'faulty', 0.2],
    ['bad',      'faulty', 0.3],
    ['very_bad', 'faulty', 0.5]])

fs = Variable("Fuel system", ['okay', 'faulty'])
F15 = Factor("P(fs)", [fs])
F15.add_values([
    ['okay',   0.9],
    ['faulty', 0.1]])

af = Variable("Air filter", ['clean', 'dirty'])
F16 = Factor("P(af)", [af])
F16.add_values([
    ['clean', 0.9],
    ['dirty', 0.1]])

asys = Variable("Air system", ['okay', 'faulty'])
F17 = Factor("P(asys|af)", [asys, af])
F17.add_values([
    ['okay',   'clean', 0.9],
    ['faulty', 'clean', 0.1],

    ['okay',   'dirty', 0.3],
    ['faulty', 'dirty', 0.7]])

st = Variable("Car starts", ['true', 'false'])
F18 = Factor("P(st|cc, fs, sq, asys, tm)", [st, cc, fs, sq, asys, tm])
F18.add_values([
    ['true', 'true', 'okay', 'good', 'okay', 'good', 0.99], 
    ['false','true', 'okay', 'good', 'okay', 'good', 0.01],

    ['true', 'true', 'okay', 'good', 'okay', 'bad', 0.98],
    ['false','true', 'okay', 'good', 'okay', 'bad', 0.02],

    ['true', 'true', 'okay', 'good', 'okay', 'very_bad', 0.7], 
    ['false','true', 'okay', 'good', 'okay', 'very_bad', 0.3], 

    ['true', 'true', 'okay', 'good', 'faulty', 'good', 0.8], 
    ['false','true', 'okay', 'good', 'faulty', 'good', 0.2], 

    ['true', 'true', 'okay', 'good', 'faulty', 'bad', 0.75],
    ['false','true', 'okay', 'good', 'faulty', 'bad', 0.25],

    ['true', 'true', 'okay', 'good', 'faulty', 'very_bad', 0.6], 
    ['false','true', 'okay', 'good', 'faulty', 'very_bad', 0.4], 

    ['true', 'true', 'okay', 'bad', 'okay', 'good', 0.7], 
    ['false','true', 'okay', 'bad', 'okay', 'good', 0.3], 

    ['true', 'true', 'okay', 'bad', 'okay', 'bad', 0.65],
    ['false','true', 'okay', 'bad', 'okay', 'bad', 0.35],

    ['true', 'true', 'okay', 'bad', 'okay', 'very_bad', 0.5], 
    ['false','true', 'okay', 'bad', 'okay', 'very_bad', 0.5], 

    ['true', 'true', 'okay', 'bad', 'faulty', 'good', 0.6], 
    ['false','true', 'okay', 'bad', 'faulty', 'good', 0.4], 

    ['true', 'true', 'okay', 'bad', 'faulty', 'bad', 0.5], 
    ['false','true', 'okay', 'bad', 'faulty', 'bad', 0.5], 

    ['true', 'true', 'okay', 'bad', 'faulty', 'very_bad', 0.4], 
    ['false','true', 'okay', 'bad', 'faulty', 'very_bad', 0.6], 

    ['true', 'true', 'okay', 'very_bad', 'okay', 'good', 0], 
    ['false','true', 'okay', 'very_bad', 'okay', 'good', 1], 

    ['true', 'true', 'okay', 'very_bad', 'okay', 'bad', 0], 
    ['false','true', 'okay', 'very_bad', 'okay', 'bad', 1], 

    ['true', 'true', 'okay', 'very_bad', 'okay', 'very_bad', 0], 
    ['false','true', 'okay', 'very_bad', 'okay', 'very_bad', 1], 

    ['true', 'true', 'okay', 'very_bad', 'faulty', 'good', 0], 
    ['false','true', 'okay', 'very_bad', 'faulty', 'good', 1], 

    ['true', 'true', 'okay', 'very_bad', 'faulty', 'bad', 0], 
    ['false','true', 'okay', 'very_bad', 'faulty', 'bad', 1], 

    ['true', 'true', 'okay', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false','true', 'okay', 'very_bad', 'faulty', 'very_bad', 1], 

    ['true', 'true', 'faulty', 'good', 'okay', 'good', 0.1], 
    ['false','true', 'faulty', 'good', 'okay', 'good', 0.9], 

    ['true', 'true', 'faulty', 'good', 'okay', 'bad', 0.05],
    ['false','true', 'faulty', 'good', 'okay', 'bad', 0.95],

    ['true', 'true', 'faulty', 'good', 'okay', 'very_bad', 0.02],
    ['false','true', 'faulty', 'good', 'okay', 'very_bad', 0.98],

    ['true', 'true', 'faulty', 'good', 'faulty', 'good', 0.05],
    ['false','true', 'faulty', 'good', 'faulty', 'good', 0.95],

    ['true', 'true', 'faulty', 'good', 'faulty', 'bad', 0.02],
    ['false','true', 'faulty', 'good', 'faulty', 'bad', 0.98],

    ['true', 'true', 'faulty', 'good', 'faulty', 'very_bad', 0.01],
    ['false','true', 'faulty', 'good', 'faulty', 'very_bad', 0.99],

    ['true', 'true', 'faulty', 'bad', 'okay', 'good', 0.05],
    ['false','true', 'faulty', 'bad', 'okay', 'good', 0.95],

    ['true', 'true', 'faulty', 'bad', 'okay', 'bad', 0.02],
    ['false','true', 'faulty', 'bad', 'okay', 'bad', 0.98],

    ['true', 'true', 'faulty', 'bad', 'okay', 'very_bad', 0.01],
    ['false','true', 'faulty', 'bad', 'okay', 'very_bad', 0.99],

    ['true', 'true', 'faulty', 'bad', 'faulty', 'good', 0.02],
    ['false','true', 'faulty', 'bad', 'faulty', 'good', 0.98],

    ['true', 'true', 'faulty', 'bad', 'faulty', 'bad', 0.01],
    ['false','true', 'faulty', 'bad', 'faulty', 'bad', 0.99],

    ['true', 'true', 'faulty', 'bad', 'faulty', 'very_bad', 0], 
    ['false','true', 'faulty', 'bad', 'faulty', 'very_bad', 1], 

    ['true', 'true', 'faulty', 'very_bad', 'okay', 'good', 0], 
    ['false','true', 'faulty', 'very_bad', 'okay', 'good', 1], 

    ['true', 'true', 'faulty', 'very_bad', 'okay', 'bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'okay', 'bad', 1], 

    ['true', 'true', 'faulty', 'very_bad', 'okay', 'very_bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'okay', 'very_bad', 1], 

    ['true', 'true', 'faulty', 'very_bad', 'faulty', 'good', 0], 
    ['false','true', 'faulty', 'very_bad', 'faulty', 'good', 1], 

    ['true', 'true', 'faulty', 'very_bad', 'faulty', 'bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'faulty', 'bad', 1], 

    ['true', 'true', 'faulty', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false','true', 'faulty', 'very_bad', 'faulty', 'very_bad', 1], 

    ['true', 'false', 'okay', 'good', 'okay', 'good', 0], 
    ['false', 'false', 'okay', 'good', 'okay', 'good', 1], 

    ['true', 'false', 'okay', 'good', 'okay', 'bad', 0], 
    ['false', 'false', 'okay', 'good', 'okay', 'bad', 1], 

    ['true', 'false', 'okay', 'good', 'okay', 'very_bad', 0], 
    ['false', 'false', 'okay', 'good', 'okay', 'very_bad', 1], 

    ['true', 'false', 'okay', 'good', 'faulty', 'good', 0], 
    ['false', 'false', 'okay', 'good', 'faulty', 'good', 1], 

    ['true', 'false', 'okay', 'good', 'faulty', 'bad', 0], 
    ['false', 'false', 'okay', 'good', 'faulty', 'bad', 1], 

    ['true', 'false', 'okay', 'good', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'okay', 'good', 'faulty', 'very_bad', 1], 

    ['true', 'false', 'okay', 'bad', 'okay', 'good', 0], 
    ['false', 'false', 'okay', 'bad', 'okay', 'good', 1], 

    ['true', 'false', 'okay', 'bad', 'okay', 'bad', 0], 
    ['false', 'false', 'okay', 'bad', 'okay', 'bad', 1], 

    ['true', 'false', 'okay', 'bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'okay', 'bad', 'okay', 'very_bad', 1], 

    ['true', 'false', 'okay', 'bad', 'faulty', 'good', 0], 
    ['false', 'false', 'okay', 'bad', 'faulty', 'good', 1], 

    ['true', 'false', 'okay', 'bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'okay', 'bad', 'faulty', 'bad', 1], 

    ['true', 'false', 'okay', 'bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'okay', 'bad', 'faulty', 'very_bad', 1], 

    ['true', 'false', 'okay', 'very_bad', 'okay', 'good', 0], 
    ['false', 'false', 'okay', 'very_bad', 'okay', 'good', 1], 

    ['true', 'false', 'okay', 'very_bad', 'okay', 'bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'okay', 'bad', 1], 

    ['true', 'false', 'okay', 'very_bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'okay', 'very_bad', 1], 

    ['true', 'false', 'okay', 'very_bad', 'faulty', 'good', 0], 
    ['false', 'false', 'okay', 'very_bad', 'faulty', 'good', 1], 

    ['true', 'false', 'okay', 'very_bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'faulty', 'bad', 1], 

    ['true', 'false', 'okay', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'okay', 'very_bad', 'faulty', 'very_bad', 1], 

    ['true', 'false', 'faulty', 'good', 'okay', 'good', 0], 
    ['false', 'false', 'faulty', 'good', 'okay', 'good', 1], 

    ['true', 'false', 'faulty', 'good', 'okay', 'bad', 0], 
    ['false', 'false', 'faulty', 'good', 'okay', 'bad', 1], 

    ['true', 'false', 'faulty', 'good', 'okay', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'good', 'okay', 'very_bad', 1], 

    ['true', 'false', 'faulty', 'good', 'faulty', 'good', 0], 
    ['false', 'false', 'faulty', 'good', 'faulty', 'good', 1], 

    ['true', 'false', 'faulty', 'good', 'faulty', 'bad', 0], 
    ['false', 'false', 'faulty', 'good', 'faulty', 'bad', 1], 

    ['true', 'false', 'faulty', 'good', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'good', 'faulty', 'very_bad', 1], 

    ['true', 'false', 'faulty', 'bad', 'okay', 'good', 0], 
    ['false', 'false', 'faulty', 'bad', 'okay', 'good', 1], 

    ['true', 'false', 'faulty', 'bad', 'okay', 'bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'okay', 'bad', 1], 

    ['true', 'false', 'faulty', 'bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'okay', 'very_bad', 1], 

    ['true', 'false', 'faulty', 'bad', 'faulty', 'good', 0], 
    ['false', 'false', 'faulty', 'bad', 'faulty', 'good', 1], 

    ['true', 'false', 'faulty', 'bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'faulty', 'bad', 1], 

    ['true', 'false', 'faulty', 'bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'bad', 'faulty', 'very_bad', 1], 

    ['true', 'false', 'faulty', 'very_bad', 'okay', 'good', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'okay', 'good', 1], 

    ['true', 'false', 'faulty', 'very_bad', 'okay', 'bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'okay', 'bad', 1], 

    ['true', 'false', 'faulty', 'very_bad', 'okay', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'okay', 'very_bad', 1], 

    ['true', 'false', 'faulty', 'very_bad', 'faulty', 'good', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'faulty', 'good', 1], 

    ['true', 'false', 'faulty', 'very_bad', 'faulty', 'bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'faulty', 'bad', 1], 

    ['true', 'false', 'faulty', 'very_bad', 'faulty', 'very_bad', 0], 
    ['false', 'false', 'faulty', 'very_bad', 'faulty', 'very_bad', 1]])

# Create a Bayes Net with all the variables and factors created 
car = BN('Car Diagnosis', 
         [al, cs, ba, bv, mf, ds, pv, sm, ss, hl,   sp,  sq,  cc,  tm,  fs,  af, asys, st], 
         [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18])

if __name__ == '__main__':
    # Loop through all variables 
    for v in [al, cs, ba, bv, mf, ds, pv, sm, ss, hl,   sp,  sq,  cc,  tm,  fs,  af, asys, st]:        
        # Print the variable name 
        print("Variable:", v.name)
        # Perform variable elimination for each variable in the bayes net car 
        probs = VE(car, v, [])
        # Check the new domains of the variable 
        doms = v.domain()
        # Print all the probabilities for each value for the latest domain of the variables 
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(v.name, doms[i], 100*probs[i]))
        # Print a new line after completing this variable 
        print()
        
        
    print("CSC384 Winter 2015 Assignment 3 Question 2") 
    print()
    print("1.")
    print("V1 = ss , V2 = sm , V3 = cc")
    print('P(cc|ss) = P(cc|ss,sm)')
    ss.set_evidence('okay')
    sm.set_evidence('okay')
    Q1a = VE(car, cc, [ss])
    Q1b = VE(car, cc, [ss,sm])
    ss.set_evidence('okay')
    sm.set_evidence('faulty')
    Q1c = VE(car, cc, [ss])
    Q1d = VE(car, cc, [ss,sm])   
    
    ss.set_evidence('faulty')
    sm.set_evidence('okay')
    Q1e = VE(car, cc, [ss])
    Q1f = VE(car, cc, [ss,sm])
    ss.set_evidence('faulty')
    sm.set_evidence('faulty')
    Q1g = VE(car, cc, [ss])
    Q1h = VE(car, cc, [ss,sm])   
    
    print('P(cc = true|ss = okay) = {0:.2f} = P(cc = true|ss = okay, sm = okay) = {0:.2f}'.format(Q1a[0],Q1b[0]))
    print('P(cc = false|ss = okay) = {0:.2f} = P(cc = false|ss = okay, sm = okay) = {0:.2f}'.format(Q1a[1],Q1b[1])) 
    print('P(cc = true|ss = okay) = {0:.2f} = P(cc = true|ss = okay, sm = faulty) = {0:.2f}'.format(Q1c[0],Q1d[0]))
    print('P(cc = false|ss = okay) = {0:.2f} = P(cc = false|ss = okay, sm = faulty) = {0:.2f}'.format(Q1c[1],Q1d[1]))     
    print('P(cc = true|ss = faulty) = {0:.2f} = P(cc = true|ss = faulty, sm = okay) = {0:.2f}'.format(Q1e[0],Q1f[0]))
    print('P(cc = false|ss = faulty) = {0:.2f} = P(cc = false|ss = faulty, sm = okay) = {0:.2f}'.format(Q1e[1],Q1f[1])) 
    print('P(cc = true|ss = faulty) = {0:.2f} = P(cc = true|ss = faulty, sm = faulty) = {0:.2f}'.format(Q1g[0],Q1h[0]))
    print('P(cc = false|ss = faulty) = {0:.2f} = P(cc = false|ss = faulty, sm = faulty) = {0:.2f}'.format(Q1g[1],Q1h[1]))        
    print('These statements illustrate that probability of cc is conditionally independent on sm given ss.') 
    print() 
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------
    print("2.")
    print("V = sq , d = bad")
    print("V1 = pv , d1 = weak")    
    print("V2 = sp , d2 = fouled")
    sq.set_evidence('bad')
    pv.set_evidence('weak')        
    sp.set_evidence('fouled')
    
    Q2a = VE(car, pv, [])
    Q2b = VE(car, sp, [])
    Q2c = VE(car, pv, [sq])
    Q2d = VE(car, sp, [sq])
    Q2e = VE(car, pv, [sq, sp]) 
    Q2f = VE(car, sp, [sq, pv])  
    print('P(pv = weak) = {0:.3f}'.format(Q2a[1]))
    print('P(sp = fouled) = {0:.3f}'.format(Q2b[2]))    
    print('P(pv = weak | sq = bad) = {0:.3f}'.format(Q2c[1]))
    print('P(sp = fouled | sq = bad) = {0:.3f}'.format(Q2d[2]))    
    print('P(pv = weak | sq = bad , sp = fouled) = {0:.3f}'.format(Q2e[1]))
    print('P(sp = fouled | sq = bad, pv = weak) = {0:.3f}'.format(Q2f[2]))
    
    print('These statements illustrate that sq = bad increases the probability of pv = weak and sp = fouled.')
    print('However, once it is known that sp = fouled, which explains away the reason sq = bad, probability of pv = weak decreases and vice-versa.')     
    print() 
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------    
    print("3.")
    print("V = ss , d = okay")
    print("V1 = sm , d1 = okay")
    print("V2 = mf , d2 = okay")
    print("V3 = bv , d3 = strong")
    sm.set_evidence('okay')
    mf.set_evidence('okay')
    bv.set_evidence('strong')
    
    print('P(ss = okay|sm = okay) < P(ss = okay|sm = okay, mf = okay)  < P(ss = okay|sm = okay, mf = okay, bv = strong) ')
    Q3a = VE(car, ss, [sm])
    Q3b = VE(car, ss, [mf, sm])
    Q3c = VE(car, ss, [mf, sm, bv])
    
    print('P(ss = okay|sm = okay) = {0:.3f}'.format(Q3a[0]))
    print('P(ss = okay|sm = okay, mf = okay) = {0:.3f}'.format(Q3b[0]))
    print('P(ss = okay|sm = okay, mf = okay, bv = strong) = {0:.3f}'.format(Q3c[0]))
    print('These statements illustrate that probability of ss = okay increases monotonically as we add the evidence items of sm = okay, mf = okay, and bv = strong.') 
    print() 
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------
    print("4.")
    print("V = st , d = true") # true, false
    print("V1 = sq , d1 = bad") # good, bad, very_bad
    print("V2 = fs , d2 = faulty") # okay, faulty 
    print("V3 = tm , d3 = good") # good, bad , very_bad
    print("V4 = asys , d4 = faulty") # okay, faulty     
    print("V5 = cc , d5 = true") # true, false
    sq.set_evidence('bad')
    fs.set_evidence('faulty')
    tm.set_evidence('good')
    asys.set_evidence('faulty')
    cc.set_evidence('true')
    
    print('P(st = true|sq = bad) > P(st = true|sq = bad, fs = faulty) < P(st = true|sq = bad, fs = faulty, tm = good) >' 
          + ' P(st = true|sq = bad, fs = faulty, tm = good, asys = faulty) < '+ 'P(st = true|sq = bad, fs = faulty, tm = good, asys = faulty, cc = true)')
    print(VE(car,st, []))
    Q4a = VE(car, st, [sq])
    Q4b = VE(car, st, [sq, fs])
    Q4c = VE(car, st, [sq, fs, tm])
    Q4d = VE(car, st, [sq, fs, tm, asys])
    Q4e = VE(car, st, [sq, fs, tm, asys, cc])
    
    print('P(st = true|sq = bad) = {0:.3f}'.format(Q4a[0]))
    print('P(st = true|sq = bad, fs = faulty) = {0:.3f}'.format(Q4b[0]))
    print('P(st = true|sq = bad, fs = faulty, tm = good) = {0:.3f}'.format(Q4c[0]))
    print('P(st = true|sq = bad, fs = faulty, tm = good, asys = faulty) = {0:.3f}'.format(Q4d[0]))
    print('P(st = true|sq = bad, fs = faulty, tm = good, asys = faulty, cc = true) = {0:.3f}'.format(Q4e[0]))
    
    print('These statements illustrate that probability of st = true both increases and decreases as we add the evidence items of' +
    ' sq = bad, fs = faulty, tm = good, asys = faulty, and cc = true.') 
    print()     
    