
# Soon Chee Loong
# cheeloong.soon@mail.utoronto.ca 
# CSC384 Winter 2015
# University of Toronto 

'''Classes for variable elimination Routines 
   A) class BN_Variable

      This class allows one to define Bayes Net variables.

      On initialization the variable object can be given a name and a
      domain of values. This list of domain values can be added to or
      deleted from in support of an incremental specification of the
      variable domain.

      The variable also has a set and get value method. These set a
      value for the variable that can be used by the factor class. 

    B) class factor

      This class allows one to define a factor specified by a table
      of values. 

      On initialization the variables the factor is over is
      specified. This must be a list of variables. This list of
      variables cannot be changed once the constraint object is
      created.

      Once created the factor can be incrementally initialized with a
      list of values. To interact with the factor object one first
      sets the value of each variable in its scope (using the
      variable's set_value method), then one can set or get the value
      of the factor (a number) on those fixed values of the variables
      in its scope.

      Initially, one creates a factor object for every conditional
      probability table in the bayes-net. Then one initializes the
      factor by iteratively setting the values of all of the factor's
      variables and then adding the factor's numeric value using the
      add_value method. 

    C) class BN
       This class allows one to put factors and variables together to form a Bayes net.
       It serves as a convient place to store all of the factors and variables associated
       with a Bayes Net in one place. It also has some utility routines to, e.g,., find
       all of the factors a variable is involved in. 

    '''

# This class defines a Bayes Net variable
class Variable:
    '''Class for defining Bayes Net variables. '''
    
    # Constructor
    # It takes in: 
    # name (string) 
    # domain (values this variable can take) 
    def __init__(self, name, domain=[]):
        '''Create a variable object, specifying its name 
        (a string). Optionally specify the initial domain.
        '''
        self.name = name                # name for variable (string) 
        self.dom = list(domain)         # Create a copy of the domain as a list 
        # Evidence index is the index for the value that this variable holds when used as an evidence for some factor's computation
        self.evidence_index = 0         # evidence value (stored as index into self.dom)
        # Set the assignment of this variable to the index for easier storing of values into the proper index of the factor table
        # Refer to add_value_at_current_assignment() method defined in class Factors for more information 
        self.assignment_index = 0       # For use by factors. We can assign variables values
                                        # and these assigned values can be used by factors
                                        # to index into their tables.

    # Add a given value to the domain of values 
    def add_domain_values(self, values):
        '''Add domain values to the domain. values should be a list.'''
        for val in values: self.dom.append(val)

    # Return the index in the domain that contains value 
    def value_index(self, value):
        '''Domain values need not be numbers, so return the index
           in the domain list of a variable value'''
        return self.dom.index(value)

    # Return the size of the domain 
    def domain_size(self):
        '''Return the size of the domain'''
        return(len(self.dom))

    # Return the domain itself as a list  
    def domain(self):
        '''return the variable domain'''
        return(list(self.dom))

    # Set this variable's evidence value to value 
    def set_evidence(self,val):
        '''set this variable's value when it operates as evidence'''
        self.evidence_index = self.value_index(val)

    # Get the value of this variable's evidence 
    def get_evidence(self):
        return(self.dom[self.evidence_index])

    # Set the assignment's index to refer to the value given 
    def set_assignment(self, val):
        '''Set this variable's assignment value for factor lookups'''
        self.assignment_index = self.value_index(val)

    # Get the assignment value 
    def get_assignment(self):
        return(self.dom[self.assignment_index])

    #---------------------------------------------------------------------------
    # These routines are special low-level routines used 
    # directly by the factor objects
    
    # Get the assignment's index, not the value it refers to 
    def set_assignment_index(self, index):
        '''This routine is used by the factor objects'''
        self.assignment_index = index

    # Set the assignment's index, not to a value 
    def get_assignment_index(self):
        '''This routine is used by the factor objects'''
        return(self.assignment_index)

    # Print the name of this variable 
    def __repr__(self):
        '''string to return when evaluating the object'''
        return("{}".format(self.name))
    
    # Print the name of this variable together with its domain. 
    def __str__(self):
        '''more elaborate string for printing'''
        return("{}, Dom = {}".format(self.name, self.dom))


class Factor: 
    '''Class for defining factors. A factor is a function that is over
    an ORDERED sequence of variables called its scope. It maps every
    assignment of values to these variables to a number. In a Bayes
    Net every Conditional Probability Table (CPT) is represented as a factor. 
    Pr(A|B,C) for example
    will be represented by a factor over the variables (A,B,C). If we
    assign A = a, B = b, and C = c, then the factor will map this
    assignment, A=a, B=b, C=c, to a number that is equal to Pr(A=a|
    B=b, C=c). During variable elimination new factors will be
    generated. However, the factors computed during variable
    elimination do not necessarily correspond to conditional
    probabilities. Nevertheless, they still map assignments of values
    to the variables in their scope to numbers.

    Note that if the factor's scope is empty it is a constaint factor
    that stores only one value. add_values would be passed something
    like [[0.25]] to set the factor's single value. The get_value
    functions will still work.  E.g., get_value([]) will return the
    factor's single value. Constaint factors might be created when a
    factor is restricted.'''

    # Constructor 
    def __init__(self, name, scope):
        '''create a Factor object, specify the Factor name (a string)
        and its scope (an ORDERED list of variable objects).'''
        self.scope = list(scope)
        self.name = name
        size = 1 # Initialize size to 1 
        # Size represents number of rows in the Conditional Probability Table for this factor 
        # It grows exponentially with the number of variables 
        for v in scope:
            size = size * v.domain_size() # since you would have the multiple of all the domain sizes as the maximum number of different values this factor can take. 
        self.values = [0]*size  #initialize values to be long list of zeros.

    # Get the list of variables this factor depends on 
    def get_scope(self):
        '''returns copy of scope...you can modify this copy without affecting 
           the factor object'''
        return list(self.scope)

    # This is used to initialize a factor 
    # by giving it a list representing all the possible row of assignments
    # and their probabability values 
    def add_values(self, values):
        '''This routine can be used to initialize the factor. We pass
        it a list of lists. Each sublist is a ORDERED sequence of
        values, one for each variable in self.scope followed by a
        number that is the factor's value when its variables are
        assigned these values. For example, if self.scope = [A, B, C],
        and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], then we could pass add_values the
        following list of lists
        [[1, 'a', 'heavy', 0.25], [1, 'a', 'light', 1.90],
         [1, 'b', 'heavy', 0.50], [1, 'b', 'light', 0.80],
         [2, 'a', 'heavy', 0.75], [2, 'a', 'light', 0.45],
         [2, 'b', 'heavy', 0.99], [2, 'b', 'light', 2.25],
         [3, 'a', 'heavy', 0.90], [3, 'a', 'light', 0.111],
         [3, 'b', 'heavy', 0.01], [3, 'b', 'light', 0.1]]

         This list initializes the factor so that, e.g., its value on
         (A=2,B=b,C='light) is 2.25'''

        # For each row given 
        for t in values:
            #initialize index to 0 
            index = 0
            # for each variable in this factor  
            # Get the unique mapping from all these variable choices. 
            for v in self.scope:
                # 
                index = index * v.domain_size() + v.value_index(t[0])
                t = t[1:] # Go to next variable of this row. 
            # Get the unique mapping for this combination of variable values 
            # From the unique mapping, index the value of this combination of values to be the probability value given. 
            self.values[index] = t[0]
               
    # Similar to addValue but it allows an easier interface to assign probability values to a list of assignments 
    def add_value_at_current_assignment(self, number): 

        '''This function allows adding values to the factor in a way
        that will often be more convenient. We pass it only a single
        number. It then looks at the assigned values of the variables
        in its scope and initializes the factor to have value equal to
        number on the current assignment of its variables. Hence, to
        use this function one first must set the current values of the
        variables in its scope.

        For example, if self.scope = [A, B, C],
        and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], and we first set an assignment for A, B
        and C:
        A.set_assignment(1)
        B.set_assignment('a')
        C.set_assignment('heavy')
        then we call 
        add_value_at_current_assignment(0.33)
         with the value 0.33, we would have initialized this factor to have
        the value 0.33 on the assigments (A=1, B='1', C='heavy')
        This has the same effect as the call
        add_values([1, 'a', 'heavy', 0.33])

        One advantage of the current_assignment interface to factor values is that
        we don't have to worry about the order of the variables in the factor's
        scope. add_values on the other hand has to be given tuples of values where 
        the values must be given in the same order as the variables in the factor's 
        scope. 

        See recursive_print_values called by print_table to see an example of 
        where the current_assignment interface to the factor values comes in handy.
        '''

        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        self.values[index] = number

    # Get the probability value given a list of assignments 
    def get_value(self, variable_values):

        '''This function is used to retrieve a value from the
        factor. We pass it an ordered list of values, one for every
        variable in self.scope. It then returns the factor's value on
        that set of assignments.  For example, if self.scope = [A, B,
        C], and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], and we invoke this function
        on the list [1, 'b', 'heavy'] we would get a return value
        equal to the value of this factor on the assignment (A=1,
        B='b', C='light')'''

        index = 0
        # First, calculate the proper index
        for v in self.scope:
            index = index * v.domain_size() + v.value_index(variable_values[0])
            variable_values = variable_values[1:]
        # Now, return the probability value at this index 
        return self.values[index] 

    # Get the probability value at the current assignment of indexes. 
    def get_value_at_current_assignments(self):
        '''This function is used to retrieve a value from the
        factor. The value retrieved is the value of the factor when
        evaluated at the current assignment to the variables in its
        scope.

        For example, if self.scope = [A, B, C], and A.domain() =
        [1,2,3], B.domain() = ['a', 'b'], and C.domain() = ['heavy',
        'light'], and we had previously invoked A.set_assignment(1),
        B.set_assignment('a') and C.set_assignment('heavy'), then this
        function would return the value of the factor on the
        assigments (A=1, B='1', C='heavy')'''
        
        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        return self.values[index]

    # Print this factor's table 
    def print_table(self):
        '''print the factor's table'''
        saved_values = []  #save and then restore the variable assigned values.
        # For each variable in this factor 
        for v in self.scope:
            # Save the current assignment values that will be changed by recursive_print_values() 
            saved_values.append(v.get_assignment_index())

        # Print every value for each variable in this factor 
        self.recursive_print_values(self.scope)

        # Restore the assignment values 
        for v in self.scope:
            v.set_assignment_index(saved_values[0])
            saved_values = saved_values[1:]
        
    # Helper method to print_table() 
    # It prints all the probability values from the list of variables for this table. 
    def recursive_print_values(self, vars):
        # Base Condition for this recursive method 
        # When no more variables left by recursion (means all variables have been assigned values
        # Print it! 
        if len(vars) == 0:
            print("[",end=""),
            # For each variable, print it's variable name and assignment value 
            for v in self.scope:
                print("{} = {},".format(v.name, v.get_assignment()), end="")
            # Finish this set of variables with the probability value 
            print("] = {}".format(self.get_value_at_current_assignments()))
        # Recursively call each variable in this table 
        else:
            # For each value possible for the first variable 
            for val in vars[0].domain():
                # Set the first variable's value to the current value
                vars[0].set_assignment(val)
                # Recursively call print values to all the other remaining variables 
                self.recursive_print_values(vars[1:])

    # Return this factor's name as well as the list of variables it contains
    def __repr__(self):
        return("{}({})".format(self.name, list(map(lambda x: x.name, self.scope))))

# This is the Bayes Net class which contains the Factors, Variables and Variable Elimination algorithm. 
class BN:
    '''Class for defining a Bayes Net.
       This class is simple, it just is a wrapper for a list of factors. And it also
       keeps track of all variables in the scopes of these factors'''

    # Constructor 
    # Initialize this Bayes Net with a name, a list of Variables, and all the Factors that contains these variables 
    def __init__(self, name, Vars, Factors):
        self.name = name
        self.Variables = list(Vars)
        self.Factors = list(Factors)
        # Check for any factors that contain variables that are not in the list of Variables 
        for f in self.Factors:
            for v in f.get_scope(): 
                # If a factor contains a variable that was not included in the list of Variables, 
                # Output error 
                if not v in self.Variables:
                    print("Bayes net initialization error")
                    print("Factor scope {} has variable {} that", end='')
                    print(" does not appear in list of variables {}.".format(list(map(lambda x: x.name, f.get_scope()), v.name, map(lambda x: x.name, Vars))))

    # Return list of factors for this Bayes Net
    def factors(self):
        return list(self.Factors)

    # Return list of variables for this Bayes Net 
    def variables(self):
        return list(self.Variables)

#-------------------------------------------------------------------------------------------------------------------------------------
# Multiply==Join Factor methods 
#-------------------------------------------------------------------------------------------------------------------------------------

# This method accepts Factors, and newFactor which is a join all of the factor in Factors
# and newScope which contains all the unique variables joint. 
# It then update the probability values in newFactor based on the multiplication of all the probability values in Factors 
# Note: Similar to recursive_print_values() starter code that was given 
# Helper method for multiply_factors() 
def recursiveMultiplyFactors(newFactor, Factors, newScope):
    # Base Case: When completely reach one assignment, set the probability value 
    if len(newScope) == 0:
        # Compute the multiplication of all related assignments from Factors
        product = 1
        for factor in Factors:
            product *= factor.get_value_at_current_assignments()
        # Add the resulting product to the newFactor's current assignment 
        newFactor.add_value_at_current_assignment(product)
    # Try out all possible value assignments   
    else:
        for value in newScope[0].domain():
            newScope[0].set_assignment(value)
            recursiveMultiplyFactors(newFactor, Factors, newScope[1:])    

# Join Factors == Multiply out the factors to join any similarities
# Note: It returns a new factor but does not modify the original Factors given 
def multiply_factors(Factors):
    '''return a new factor that is the product of the factors in Factors'''
    # Create a new factor with a scope that contains all variables
    name = "" 
    newScope = [] 
    for factor in Factors:
        name += factor.name # add this factor name to the resulting name for newFactor 
        for variable in factor.get_scope():
            if variable not in newScope:
                newScope.append(variable)
    # Create the new factor 
    newFactor = Factor(name, newScope) 
    # Now, recursively add the assignments 
    # note: Similar to recursive_print_values() 
    recursiveMultiplyFactors(newFactor, Factors, newScope)
    return newFactor 
  
#-------------------------------------------------------------------------------------------------------------------------------------
# RestrictFactor methods 
#-------------------------------------------------------------------------------------------------------------------------------------
# Helper method for restrict_factor()
def recursiveRestrictFactors(newFactor, factor, newScope):
    # Base case: When no more variables, which means all variables has been assigned values at this iteration 
    if len(newScope) == 0:
        # Add to the new factor the new values based on the restricted assignment from previous factor
        newFactor.add_value_at_current_assignment(factor.get_value_at_current_assignments())
    else:
        # Continue going through every possible value in the variable's domain 
        for value in newScope[0].domain():
            # And set the assignment to that value for this variable 
            newScope[0].set_assignment(value)
            # Now continue setting the remaining variable values 
            recursiveRestrictFactors(newFactor, factor, newScope[1:])    

# Restrict the factor for a variable to contain a given value 
def restrict_factor(f, var, value):
    '''f is a factor, var is a Variable, and value is a value from var.domain.
    Return a new factor that is the restriction of f by this var = value.
    Don't change f! If f has only one variable its restriction yields a
    constant factor'''
    # Note: Don't change f! 
    # Create a copy of f!
    #factor = f[:] 
    name = f.name + "restrict" + var.name 
    newScope = f.get_scope() 
    # Set the assignment of this evidence variable to is evidence value 
    var.set_assignment(value) 
    # Remove the evidence variable for var
    newScope.remove(var) 
    # If this factor becomes empty after removing 1 variable, return an empty list 
    if (len(newScope) == 0):
        # Return a constant factor  
        return [f.get_value([value])] # return the constant probability value 
    # If there are still factors left after removing the evidence variables 
    # Create a new factor with the new name and the remaining scope 
    newFactor = Factor(name, newScope)
    # Only pass in the scope of the newFactor so that you only loop through the assignment values of the new factor
    # whereas the originalFactor already contains the evidence values for the evidence variables for its assignment 
    # Note: Similar to recursive_print_values() 
    recursiveRestrictFactors(newFactor, f, newScope)
    # Finally, return the newFactor 
    return newFactor    

#-------------------------------------------------------------------------------------------------------------------------------------
# SumOutVariable == Eliminate methods 
#-------------------------------------------------------------------------------------------------------------------------------------

# Helper method for sum_out_variable() 
# Similar to recursive_print_values() 
def recursiveSumOutVariables(newFactor, factor, newScope, variable): 
    # Base Case: When completely reach one assignment, set the probability value 
    if len(newScope) == 0:
        # Compute the multiplication of all related assignments from Factors
        summation = 0
        # Get the summation of all possible assignments of value for this variable 
        for value in variable.domain():
            variable.set_assignment(value)
            summation += factor.get_value_at_current_assignments()
        # Add the resulting sum to the newFactor's current assignment 
        newFactor.add_value_at_current_assignment(summation)
        
    # Try out all possible value assignments   
    else:
        for value in newScope[0].domain():
            newScope[0].set_assignment(value)
            recursiveSumOutVariables(newFactor, factor, newScope[1:], variable)  

# Eliminate = Sum Out => Eliminate the variable from a list of factors by summing out that variable from the list of factors 
def sum_out_variable(f, var):
    '''return a new factor that is the result of summing var out of the input factor f'''
    name = f.name + "sumOut" + var.name 
    newScope = f.get_scope()
    newScope.remove(var)
    # If removing that variable results in an empty scope, 
    # Return an empty variable since it represents probability of 1 
    if not (newScope):
        return []       
    newFactor = Factor(name, newScope)
    # Now, compute the sum of all the possible assignments fromt he original factor into the new factor 
    # note: Similar to recursive_print_values() 
    recursiveSumOutVariables(newFactor, f, newScope, var)
    # Return the newly created factor 
    return newFactor   
#-------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------
# Ordering
#------------------------------------------

# Find out the the best ordering to do variable elimination by 
# Checking which which variable results in the least variable when its factors are combined 
def min_fill_ordering(Factors, QueryVar):
    '''Compute a min fill ordering given a list of factors. Return a list
    of variables from the scopes of the factors in Factors. The QueryVar is 
    NOT part of the returned ordering'''
    scopes = [] # Initialize scopes to be an empty list, which will be a list that contains lists of variable scopes 
    # For each factor in the list of factors 
    for f in Factors:
        # Append the variables this factor relies as a list to the scopes
        scopes.append(list(f.get_scope()))
    # Initialize an empty list of variables 
    Vars = []
    # For each list of variables in scopes, 
    for s in scopes:
        # For each variable in the list of variables 
        for v in s:
            # If the variable is not in the list of Variables already, and it is also not the query variable 
            if not v in Vars and v != QueryVar:
                # Append this variable to the list of variables 
                Vars.append(v)
    # Basically, here, we're done determining all the hidden variables 
    # Initialize ordering of variables to be no variables 
    ordering = []
    # While there are still variables left in Vars that have not to ordering 
    while Vars:
        # Get the variable and the new scope 
        # Get the minimum variable as well as the union scope from removing this variable 
        (var,new_scope) = min_fill_var(scopes,Vars)
        # Append this variable to ordering, the earlier you append it, the earlier this variable should be eliminated first. 
        ordering.append(var)
        # if this variable is in list of variables to check, remove it as already checked that it should be removed first 
        if var in Vars:
            # Remove it 
            Vars.remove(var)
        # Remove all scopes containing this variable from scopes 
        # as well as add the new union scope to scopes 
        # which will be used in min_fill_var() for finding the next variable to insert into ordering 
        scopes = remove_var(var, new_scope, scopes)
    return ordering

# Helper method for min_fill_ordering() 
# Given a list of variables in scopes and a list of variables to be eliminated in Vars
# It computes the best variable to remove next 
# and returns the best variable to remove next, as well as the new scope (individual factor) 
# that consists of the union of all the factors containing the minimum variable that was removed. 
# Note: You would add this new union to your scopes but also use remove_var() to remove all the existing scope that contains this variable 
def min_fill_var(scopes, Vars):
    '''Given a set of scopes (lists of lists of variables) compute and
    return the variable with minimum fill in. That the variable that
    generates a factor of smallest scope when eliminated from the set
    of scopes. Also return the new scope generated from eliminating
    that variable.'''
    minv = Vars[0] # Initialize the minimum variable to remove to the first variable 
    # Get the length and new scope that results in eliminating this variable 
    (minfill,min_new_scope) = compute_fill(scopes,Vars[0])
    # Do the same for all the other variables 
    # but keep track of the minimumVariable to remove
    for v in Vars[1:]:
        (fill, new_scope) = compute_fill(scopes, v)
        # If it results in a smaller scope, 
        if fill < minfill:
            # Update the best variable to remove to be this variable
            minv = v
            # Also, update the length of the minimum variable as well as the updated scope 
            minfill = fill
            min_new_scope = new_scope
    return (minv, min_new_scope)

# A helper method for min_fill_var() which is a helper method for min_fill_ordering() 
# This method computes the new scope that results from eliminating variable a from the list of scope in scopes
# Also, returns the length of this new scope 
def compute_fill(scopes, var):
    '''Return the fill in scope generated by eliminating var from
    scopes along with the size of this new scope'''
    union = []
    # For each list of variables in scopes
    for s in scopes:
        # If this list of variables contains the variable to be removed
        if var in s:
            # Then add all the other variables to union 
            for v in s:
                if not v in union:
                    union.append(v)
    # Also, remove the original variable as it was added to union 
    if var in union: union.remove(var)
    # Return the length of the union and the union of all the factors that contains this variable 
    return (len(union), union)

# Return the new set of factors that results from eliminating a variable from factors
# This is used for the step right after (joining and eliminating a variable to create a new factor) 
# Then, this step cleans up the list of Factors in this Bayes Net by removing all Factors that contains the previous variable 
# Also, it adds the union of all the factors that contain the previous variable, where this union is passed in as the parameter called new_scope 
# Also, used in min_fill_ordering() method. 
def remove_var(var, new_scope, scopes):
    '''Return the new set of scopes that arise from eliminating var
    from scopes'''
    new_scopes = []
    for s in scopes:
        if not var in s:
            new_scopes.append(s)
    # Also, add the new_scope which is the union from all the factors remove by removing this variable 
    new_scopes.append(new_scope)
    return new_scopes
            
#-------------------------------------------------------------------------------------------------------------------------------------
# This is a helper method for Variable Elimination that uses
# restrict_factor(). However, it gets passed a list of factors and a list of evidenceVariables instead
def restrictFactorsWithEvidenceVariables(listOfFactors, listOfEvidenceVariables):   
    for factor in listOfFactors:
        # determine whether factor has any evidence variable. If yes, then get the 
        # evidence variable(s) present in factor
        # Get all the evidence variables that are in factor 
        # and make it into a list of variables 
        evidences = []
        for evidence in listOfEvidenceVariables:
            for variable in factor.get_scope():
                if evidence == variable:
                    evidences.append(evidence)
        # If this factor has evidence variables 
        if (evidences):
            for evidence in evidences: 
                newFactor = restrict_factor(factor, evidence, evidence.get_evidence())            
                # Note: newFactor may be a constant factor 
                if (newFactor):
                    listOfFactors[listOfFactors.index(factor)] = newFactor # replace the old factor with the new factor that was created 
                else: # If new factor is empty after restricting, remove that factor from the list of factors 
                    listOfFactors.remove(factor)
                factor = newFactor # Replace factor with newFactor                 
        # Upon return, listOfFactors may contain factors that are constant values 

# Evidence = A set of values given for some of the conditional variables (parents) 
# Variable Elimination 
# Order them so they are eliminated in a good order 
# Min fill ordering gives good ordering 
###
def VE(Net, QueryVar, EvidenceVars):
    '''
    Input: Net---a BN object (a Bayes Net)
           QueryVar---a Variable object (the variable whose distribution
                      we want to compute)
           EvidenceVars---a LIST of Variable objects. Each of these
                          variables has had its evidence set to a particular
                          value from its domain using set_evidence. 

   VE returns a distribution over the values of QueryVar, i.e., a list
   of numbers one for every value in QueryVar's domain. These numbers
   sum to one, and the i'th number is the probability that QueryVar is
   equal to its i'th value given the setting of the evidence
   variables. For example if QueryVar = A with Dom[A] = ['a', 'b',
   'c'], EvidenceVars = [B, C], and we have previously called
   B.set_evidence(1) and C.set_evidence('c'), then VE would return a
   list of three numbers. E.g. [0.5, 0.24, 0.26]. These numbers would
   mean that Pr(A='a'|B=1, C='c') = 0.5 Pr(A='a'|B=1, C='c') = 0.24
   Pr(A='a'|B=1, C='c') = 0.26
 
    '''
    # First, get the list of factors from the Bayes Net object so to not modify any original factors from input Net 
    factors = Net.factors()
    # First, restrict all the factors given by the evidence variables 
    
    #print(factors)
    #print("TEMP1")
    #for factoree in factors: 
    #    factoree.print_table() 
    restrictFactorsWithEvidenceVariables(factors, EvidenceVars)
    # Note: This may generate constant factors 
    constantFactorsRestrict = 1 # To keep track of all the multiplication of constant factors due to restriction 
    # Get rid of constant factors 
    factorsToRemove = [] 
    for factor in factors: 
        try: 
            factor.get_scope() 
        except: # If can't get scope, it means it is a constant factor
            constantFactorsRestrict *= factor[0]
            factorsToRemove.append(factor) 
    for factor in factorsToRemove:
        factors.remove(factor)
    #print(factors)
    #print("TEMP2")
    
    # Now, get the elimination order after restricting the factor in factors
    variablesInOrder = min_fill_ordering(factors, QueryVar) #note: This is an NP-Hard Algorithm! 
    # Note: The variablesInOrder will not include the QueryVariables 
    # Loop through each variable in order 
    #print(variablesInOrder)
    for variable in variablesInOrder: 
        # Get all factors that contains current variables 
        listOfFactors = [] #Initialize listOfFactors that contains current variable 
        # Get all factors related to this variable into listOfFactors        
        for factor in factors:
            if variable in factor.get_scope():                
                listOfFactors.append(factor)
                #print("TEMP3") 
                #print(factor)
                #factor.print_table() 
        #print(listOfFactors) 
        # If this variable has >1 associated factors with it 
        if len(listOfFactors) >= 1:
            # Multiply out the common factors 
            combinedFactor = multiply_factors(listOfFactors)
            # Note: combinedFactor may contain constant factors             
            # Sum out the variable from that factor 
            combinedFactor = sum_out_variable(combinedFactor, variable)        
            # If the combined factor is not just a constant probability 
        # Remove all the factors 
        # Remove the factors that were changed from the original factors in this BayesNet
        for factorToRemove in listOfFactors:
            factors.remove(factorToRemove)
        # Add the new combinedFactor only if it is not empty 
        if(combinedFactor): # If did not wipe out the entire factor, if you did wipe out, its probability is 1, so there is no need to add it to the combination 
            factors.append(combinedFactor) # Append the combined factor to factors 
    # Multiply out the remaining factors 
    finalCombinedFactor =  multiply_factors(factors)
    # Multiply all the values with the constantFactor's multiplcations before normalization 
    size = 1
    for v in finalCombinedFactor.get_scope():
        size = size * v.domain_size() 
    for i in range(0, size):
        finalCombinedFactor.values[i] *= constantFactorsRestrict
    #finalCombinedFactor.print_table()     
    # Normalize the final probability values     
    divisor = float(sum(finalCombinedFactor.values)) # Sum all the values in the finalCombinedFactor and convert to float 
    # Only divide if not equal to 0 
    if (divisor != 0):
        # Return the normalize probability values for each row in the final finalCombinedFactor's table 
        return [value/divisor for value in finalCombinedFactor.values]    
    # Return a probability of 0.0 for each value in the finalCombinedFactor's table 
    return [value for value in finalCombinedFactor.values] # Return the original probability which are all zeros in the original factor values to result in divisor = 0 
    
if __name__ == '__main__':
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
    
