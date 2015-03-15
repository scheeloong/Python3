'''Constraint Satisfaction Routines
   A) class Variable

      This class allows one to define CSP variables.

      Currently no support for backtracking--i.e., can not remember
      and undo changes, so if one wants to implement backtracking
      search an extension is needed.

      On initialization the variable object can be given a name, and
      an original domain of values. This list of domain values can be
      added but NOT deleted from.
      
      To support GAC propagation, the class also maintains a
      current domain for the variable. Values pruned from the variable
      domain are removed from the current domain but not from the
      original domain.

      The current domain can be re-initialized at any point to be
      equal to the original domain.

    B) class constraint

      This class allows one to define constraints specified by tables
      of satisfying assignments.

      On initialization the variables the constraint is over is
      specified (i.e. the scope of the constraint). This must be an
      ORDERED list of variables. This list of variables cannot be
      changed once the constraint object is created.

      Once initialized the constraint can be incrementally initialized
      with a list of satisfying tuples. Each tuple specifies a value
      for each variable in the constraint (in the same ORDER as the
      variables of the constraint were specified).

'''

# Note: Don't have to change this file for this assignment. 
# Just need to use it. 

class Variable:
    # Constructor 
    # Each variable has a 
    # string: name
    # list of values originally for this domain 
    # list of values after pruning for current domain 
    '''Class for defining CSP variables'''
    def __init__(self, name, domain=[]):
        '''Create a variable object, specifying its name (a
        string). Optionally specify the initial domain.
        '''
        self.name = name                # text name for variable
        self.dom = list(domain)         # Make a copy of passed domain
        self.curdom = list(domain)      # using list

    # This method adds additional possible values for the domain of this variable 
    def add_domain_values(self, values):
        '''Add additional domain values to the domain'''
        for val in values: self.dom.append(val)
        for val in values: self.curdom.append(val)

    # Returns the index position of the given value of this Variable's domain 
    # Note: It assumes all values in the current domain are unique 
    # You need to do this, so that you can figure out where it is when checking for supports later 
    # The position relies on the original domain of values given for this Variable. 
    def value_index(self, value):
        '''Domain values need not be numbers, so return the index
           in the domain list of a variable value'''
        return self.dom.index(value)

    # Remove a value from this domain of values 
    def prune_value(self, value):
        '''Remove value from current domain'''
        self.curdom.remove(value)

    # Get the size of the original domain 
    # size => number of possible values originally 
    def domain_size(self):
        '''Return the size of the domain'''
        return(len(self.dom))

    # Get the original domain 
    def domain(self):
        '''return the variable domain'''
        return(self.dom)

    # Get the current domain 
    def cur_domain(self):
        '''return the variable current domain'''
        return(self.curdom)

    # Get the size of the current domain 
    # size => Number of possible values left 
    def cur_domain_size(self):
        '''Return the size of the current domain'''
        return(len(self.curdom))

    # Check if a given value is still in the current domain for this variable 
    def in_cur_domain(self, value):
        '''check if value is in current domain'''
        return(value in self.curdom)


    # It only prints out the the name of this variable 
    def __repr__(self):
        return("Variable \"{}\"".format(self.name))
        # Define a printable representation of this variable
        # For example, if you do this on the commandline; 
        # >> v  # print out this variable using the __repr__ function 
    
    # Print the variable's name, original domain and it's current domain 
    def print_var(self):
        '''Also print the variable domain and current domain'''
        print("Variable\"{}\": Dom = {}, CurDom = {}".format(self.name, self.dom, self.curdom))

class Constraint: 
    '''Class for defining constraints specified as lists of satisfying
       tuples. Note that the initial scope passed as a list of
       variable objects specifes an ordering over the tuples. That is, each
       tuple must be an ordered list of values, one for each variable
       in scope. For example, if the constaint scope is specified to be
       [v1, v2, v3], where each vi is a variable object then a
       satisfying tuple will have to be a list of three values. For
       example, the tuple [1, 2, 1] would specify the assignments
       v1=1, v2=2, v3=1---the ordering has to agree with the scope.'''

    # Constructor for Constraint
    # It initializes the scope to be number of variable for this constraint
    # gives this constraint a name 
    # and initialize satisfying tuples list to be nothing 
    # The supporting tuples is where, 
    # for every variable, 
    # and for every possible value for each variable 
    # you store the list of supporting tuples for this constraint 
    # that supports that value at that variable 
    # It's a 2D Indexing matrix, [VariableNumber][ValueOfVariable], note: the index limit may be different for each VariableNumber 
    
    def __init__(self, name, scope): 
        '''create a constraint object, specify the constraint name (a
        string) and its scope (an ORDERED list of variable
        objects). The list of satisfying tuples is specified later
        using add_satisfying_tuples'''

        self.scope = list(scope)
        self.name = name
        self.sat_tuples = []
        #The next object data item 'sup_tuples' will be used to help
        #support GAC propagation. It is a list of lists (like a matrix)
        #indexed by two integers [variable position in scope][value
        #position in variable domain] At this position of the matrix
        #will be stored a list of all supporting tuples for that variable
        #value pair. Initially, these lists are set to be empty by the
        #following code. NOTE that support tuple data structure is
        #space expensive, and for solving real CSP problems better
        #data structures would be required.
        self.sup_tuples = []
        # Go through each variable 
        for i in range(len(self.scope)): #i-th variable
            # Initialize space to store the list of supported values 
            # for each variable, and for every possible value in the domain of each variable 
            self.sup_tuples.append([]) # A list of variables for this tuple 
            for j in range(self.scope[i].domain_size()): # Go through each possible value in the domain of that variable 
                self.sup_tuples[i].append([]) # A list of values for this variable for this tuple 
                # Note: They are all initialize to empty now, but will be added a list of corresponding tuples that supports the current value 

    # This method adds a list of (tuple of variables)
    # that satisfy this Constraint 
    # Note: tuples[0] => [list of values], 
    # where value[0] => value for 0th (first) variable 
    def add_satisfying_tuples(self, tuples):
        '''Add list of satisfying tuple to the constraint.'''
        # For each satisfying tuples in this list of tuples 
        for t in tuples:
            # Add this tuple to the list of satisfying tuples 
            self.sat_tuples.append(t)
            
            #--------------------------------------------------------------------------------------------------
            # Update the supports for all variables in this constraint, 
            # to allow the list of values for this tuple 
            #--------------------------------------------------------------------------------------------------
            i = 0 # to be able to increment i using python's 'for each' loop 
            # For each value given in the tuple 
            for val in t:  # note: value i represents the value assigned to the ith variable in this constraint 
                # get the index for the assigned value for variable i in its domain 
                j = self.scope[i].value_index(val) #find value's index for this variable's domain 
                # Add supporting tuples for variable i at index j for value t as there is a tuple that supports it 
                self.sup_tuples[i][j].append(t)    # add tuple on Vi=j support list
                i = i+1

    # This method tests if a tuple of variable values is valid for this constraint 
    def tuple_is_valid(self, t):
        '''internal routine to test if a tuple contains values that are
           in the current domain of the variables. The constraint scope
           determines what variable each value in the tuple corresponds to'''
        i = 0
        for val in t:
             var = self.scope[i] # get the corresponding Variable Object 
             # If there is no variable in the domain with the current value
             # return false. 
             if not var.in_cur_domain(val): # Check if the value is in the current domain for this variable to know if it's valid 
                return False
             i = i + 1
        return True

    # This method checks if a value for a given variable 
    # has tuples supporting it 
    def has_support(self, var, val):
        '''Test if a variable value pair has a supporting tuple (set 
           of assignments satisfying the constraint where each assignment
           is a value that is still in the corresponding variable's current
           domain'''
           
        i = self.scope.index(var)
        j = var.value_index(val)
        #it would be more efficient to work through the list of supporting tuples
        #from the end, popping tuples as they are found to be invalid. 
        #this way we would avoid processing the same invalid tuple twice.
        #However, if eventually we add support for backtracking (i.e., restoring
        #tuples to validity) this would make it more complex. So for now 
        #just do it the more time consuming but easier way.
        
        # Brilliant: Just go through each other tuple and see if the current value 
        # has corresponding supportedTuples that are in the list of tupleIsValid
        for t in self.sup_tuples[i][j]:
            # Check if tuple is still valid 
            if self.tuple_is_valid(t):
                return True
        # Return false if no currently valid tuples at all,
        return False

    # Print out the constraint's name as well as the all the variable names in this constraint
    def __repr__(self):
        return("Constraint \"{}{}\"".format(self.name,[var.name for var in self.scope]))

    # Pirnt out the The constraint name and all the variable names in this constraint 
    def print_constraint(self):
        '''print basic information about the constraint'''
        print("Constraint {}: scope = {}".format(self.name,
                                                 [var.name for var in self.scope]))

    # Print this constaint name, as well as all the variables 
    # Also, print all the satisfying tuples of variable values that are valid for this constraint 
    def print_constraint_all(self):
        '''print all of the information about the constraint (can be voluminous)'''
        self.print_constraint()
        # Print all tuples and if it is still valid 
        print("Satisfying Tuples:")
        for t in self.sat_tuples:
            print("{}: {}".format(t, self.tuple_is_valid(t)))

        # For every variable, and every of its possible value, 
        # Print the supporting tuples that were added and if there were still valid. 
        print("Supporting Tuples")
        for var in self.scope:
            for val in var.domain():
                print("  {} = {}: {}".format(var.name, val, self.sup_tuples[self.scope.index(var)][var.value_index(val)]))

