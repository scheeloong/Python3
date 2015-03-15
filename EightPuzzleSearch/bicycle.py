#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the bicycle domain.  

'''
bicycle STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from math import sqrt

class bicycle(StateSpace):
 
    '''Initialize a bicycle search state object.''' 
    def __init__(self, action, gval, jobsToVisit, location, time, weight, earned, jobsCarried, jobsFinished, parent = None):#, ... 
#IMPLEMENT
    # note: action = 'START' is treated as starting the search space
        if action == 'START':   
            StateSpace.n = 0 # The recursive level in tree is 0 
        # Call the parent constructor
        StateSpace.__init__(self, action, gval, parent) # incrementing StateSpace.n is handled here 
        # Current list of jobs being carried by bicycle 
        self.jobsCarried = jobsCarried # Note: This is a reference not a copy 
        # Current list of jobs to visit by bicycle 
        self.jobsToVisit = jobsToVisit # 
        self.currentLocation = location # The current location of the bicycle
        self.currentTime = time   # The current time of the bicycle 
        self.currentWeight = weight # Current amount of weight on the bicycle 
        self.currentEarned = earned # The current amount of money earned by the bicycle
        self.jobsFinished = jobsFinished # The list of finished jobs done by the bicycle 

    '''Return list of bicycle objects that are the successors of the current object'''
    def successors(self): 
#IMPLEMENT
        # Initialize a list of states 
        States = []

        #--------------------------------------------
        # first_pickup(jobName) 
        #--------------------------------------------
        if self.currentLocation == "home":
            # loop through each job Name available and 
            # append it as a state
            for job in self.jobList:
                # Initialize all copies
                updatedJobLists = self.jobList[:] # Create a JobLists variable to hold all job information 
                jobsCarried = self.jobsCarried[:] 
                jobsToVisit = self.jobsToVisit[:]
                # Execute 
                jobName = job[0] 
                firstJobLocation = job[1] # get the job location to do first  
                startTime = job[2] # First time to pickup at the jobs pickup time  which is >= 420 
                jobsCarried.append(jobName) # add the jobName to jobsCarried
                jobsToVisit.remove(jobName) # Remove this jobName from jobsToVist 
                weightCarried = job[4] + self.currentWeight
#    def __init__(self, action, gval, jobsToVisit, location, time, weight, earned, jobsCarried, finishedJobs, parent = None):#, ... 

                States.append(bicycle("first_pickup({})".format(jobName), self.gval, jobsToVisit, firstJobLocation, startTime,
                                      weightCarried, self.currentEarned, jobsCarried ,self.jobsFinished, self))
                

        # If not at first location , try doing both pickUp and deliver 
        else:  
        #--------------------------------------------
        # deliver(jobName) 
        #--------------------------------------------
            # For each job name available 
            for jobDeliverName in self.jobsCarried:
                # Look for corresponding jobName in the list of jobs 
                for jobFound in self.jobList:
                    # only execute if found the right job 
                    if jobDeliverName == jobFound[0]:
                        # Initialize
                        updatedJobLists = self.jobList[:] 
                        jobsCarried = self.jobsCarried[:]
                        jobsFinished = self.jobsFinished[:]
                        currentEarned = self.currentEarned
                        # Execute 
                        jobName = jobFound[0] 
                        deliverJobLocation = jobFound[3] 
                        timeAtDeliver =  self.currentTime + distanceTime(self.currentLocation, deliverJobLocation)
                        # If arrive after latest time 
                        if timeAtDeliver > 1140: 
                            continue 
                        # Get the amount earned from arriving at destination location at time timeAtDeliver
                        amountEarneds = amountEarned(jobFound[5], timeAtDeliver)
                        # Take the cost as the maximum amountEarned available - actual amountEarned
                        # as want to minimize cost 
                        gval = jobFound[5][0][1] - amountEarneds +self.gval
                        
                        # Append to jobsFinished
                        jobsFinished.append(jobFound[0]) 
                        # Remove from current list of jobs carried 
                        jobsCarried.remove(jobFound[0])
                        # Remove job's weight from weight 
                        weightCarried =  self.currentWeight - jobFound[4]
                        # Add profit to amount earned so far 
                        currentEarned = currentEarned + amountEarneds
                        # Finally, append this as a new state 
                        
                        States.append(bicycle("deliver({})".format(jobName), gval, self.jobsToVisit, deliverJobLocation, 
                                              timeAtDeliver, weightCarried, currentEarned, jobsCarried, self.jobsFinished, self))   
        #--------------------------------------------
        # pickup(jobName)
        #-------------------------------------------- 
            # For each job name available 
            for jobPickUpName in self.jobsToVisit:
                # Look for corresponding jobName in the list of jobs 
                for jobFound in self.jobList:
                    # only execute if found the right job 
                    if jobPickUpName == jobFound[0]:
                        # Initialize
                        updatedJobLists = self.jobList[:] 
                        jobsCarried = self.jobsCarried[:]
                        jobsToVisit = self.jobsToVisit[:] 
                        # Execute 
                        jobName = jobFound[0] 
                        pickUpJobLocation = jobFound[1] # get the job location to pick up 
                        # Add job to carrying 
                        timeAtPickUp = self.currentTime + distanceTime(self.currentLocation, pickUpJobLocation) # Add the time taken from current location
                                                                                                          # of bicycle to the pickUplocation 
                        # Handle waiting if arrive earlier 
                        if jobFound[2] > timeAtPickUp:
                            timeAtPickUp = jobFound[2] 
                        weightCarried = jobFound[4] + self.currentWeight
                        # Check satisfies condition for picking up 
                        # Condition 1: Pick Up Time is after constaint time given 
                        if timeAtPickUp > 1140: 
                            continue
                        # Condition 2: Current weight more than maximum weight allowed  
                        if weightCarried > 10000:
                            continue 
                        # To check if condition3 is true 
                        condition3Boolean = 0
                        # Condition 3: The pick up location is not the same as a delivery location for any jobs currently being carried 
                        for jobDeliverName in self.jobsCarried:
                            for jobFoundDelivery in self.jobList:
                                # only execute if found the right job 
                                if jobDeliverName == jobFoundDelivery[0]:
                                    if jobFoundDelivery[3]==pickUpJobLocation:
                                        condition3Boolean = 1 # Found a jobDelivery that is the same as pickUp, don't pick up 
                        if condition3Boolean == 1:
                            continue 
                        
                        # Only append to jobsCarried after checking Condition 3 
                        jobsCarried.append(jobName)
                        jobsToVisit.remove(jobName) 
                        States.append(bicycle("pickup({})".format(jobName), self.gval, jobsToVisit, pickUpJobLocation, 
                                              timeAtPickUp, weightCarried, self.currentEarned, jobsCarried, self.jobsFinished, self))  
        return States

    '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
    def hashable_state(self) : # Maybe you're returning more state than there is, if same states exists 
    #IMPLEMENT
        if not self:
            return ()    
        return (self.currentLocation,  "{},{}".format(self.jobsToVisit, self.jobsCarried), "gval={}".format(self.gval), self.currentTime)        
               # include time cause time influence how much earn next 
    
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output. 
    #Note that if you implement the "get" routines below properly, 
    #This function should work irrespective of how you represent
    #your state.     
    def print_state(self):
        # If this state has a parent
        if self.parent:
                   # ActionName, StateNumber, currentCosts, previousStateNumber
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        # Otherwise, this state has no parent 
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        # Carrying weight ['Job0', 'Job1']  # a list of job names
        # load is weight in grams (an integer) 
        print("    Carrying: {} (load {} grams)".format(
                      self.get_carrying(), self.get_load()))
        # Start time is time in minutes 
        # Location is current location 
        # Earned is amount of money earned so far 
        print("    State time = {} loc = {} earned so far = {}".format(
                      self.get_time(), self.get_loc(), self.get_earned()))
        # Output list of unstarted jobs 
        print("    Unstarted Jobs.{}".format(self.get_unstarted()))


    '''Return location of courier in this state'''
    def get_loc(self):
#IMPLEMENT
        return self.currentLocation 


    '''Return list of NAMES of jobs being carried in this state'''
    def get_carrying(self):
#IMPLEMENT
        return self.jobsCarried

    '''Return list of NAMES of jobs not yet stated in this state''' 
    def get_unstarted(self):
    #IMPLEMENT   
        return self.jobsToVisit 
        
    
    '''Return total weight being carried in this state'''
    def get_load(self):
#IMPLEMENT
        return self.currentWeight 

    '''Return current time in this state'''
    def get_time(self):
#IMPLEMENT
        return self.currentTime

    '''Return amount earned so far in this state'''
    def get_earned(self):
#IMPLEMENT
        return self.currentEarned 

# List of maps and jobs from input 
bicycle.mapList = [] # the map given from input 
bicycle.jobList = [] # list of jobs that needs to be done from input 
#bicycle.maxProfit = 0
# bicycle 

# End of class bicycle     
    
'''Null Heuristic use to make A* search perform uniform cost search'''
def heur_null(state):
    return 0

'''Bicycle Heuristic sum of delivery costs.'''

#Sum over every job J being carried: Lost revenue if we
#immediately travel to J's dropoff point and deliver J.
#Plus 
#Sum over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
#point then to J's dropoff poing and then deliver J.
def heur_sum_delivery_costs(state):
#IMPLEMENT
    totalSumLostRevenue = 0 # initialize totalSum 
    
    # First, handle all job carried 
    #------------------------------------------------
    # Job Carried
    #------------------------------------------------
    for jobDeliverName in state.jobsCarried:
        # Look for corresponding jobName in the list of jobs 
        for jobFound in state.jobList:
            # only execute if found the right job 
            if jobDeliverName == jobFound[0]:
                deliverJobLocation = jobFound[3]                 
                timeAtDeliver =  state.currentTime + distanceTime(state.currentLocation, deliverJobLocation)
                # Get the amount earned from arriving at destination location at time timeAtDeliver
                amountEarneds = amountEarned(jobFound[5], timeAtDeliver)
                lostRevenue = jobFound[5][0][1] - amountEarneds
                totalSumLostRevenue = totalSumLostRevenue + lostRevenue
    #------------------------------------------------
    # Unstarted Job 
    #------------------------------------------------
    # For each job name available 
    for jobPickUpName in state.jobsToVisit:
        # Look for corresponding jobName in the list of jobs 
        for jobFound in state.jobList:
            # only execute if found the right job 
            if jobPickUpName == jobFound[0]:   
                jobName = jobFound[0] 
                pickUpJobLocation = jobFound[1] # get the job location to pick up 
                deliverJobLocation = jobFound[3]                                 
                # Add job to carrying 
                timeAtPickUp = state.currentTime + distanceTime(state.currentLocation, pickUpJobLocation) # Add the time taken from current location
                                                                                                  # of bicycle to the pickUplocation 
                # Handle waiting if arrive earlier 
                if jobFound[2] > timeAtPickUp:
                    timeAtPickUp = jobFound[2]     
                # Now find time to deliver 
                timeAtDeliver =  timeAtPickUp + distanceTime(pickUpJobLocation, deliverJobLocation)
                # Get the amount earned from arriving at destination location at time timeAtDeliver
                amountEarneds = amountEarned(jobFound[5], timeAtDeliver)
                lostRevenue = jobFound[5][0][1] - amountEarneds
                totalSumLostRevenue = totalSumLostRevenue + lostRevenue    
    return totalSumLostRevenue
    
    

'''Bicycle Heuristic sum of delivery costs.'''
#m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff
#point and deliver J.
#m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
#point then to J's dropoff poing and then deliver J.
#heur_max_delivery_costs(state) = max(m1, m2)
def heur_max_delivery_costs(state):
#IMPLEMENT
    totalMaxLostRevenue = 0 #initialize max that can be achieved 
    # First, handle all job carried 
    #------------------------------------------------
    # Job Carried
    #------------------------------------------------
    for jobDeliverName in state.jobsCarried:
        # Look for corresponding jobName in the list of jobs 
        for jobFound in state.jobList:
            # only execute if found the right job 
            if jobDeliverName == jobFound[0]:
                deliverJobLocation = jobFound[3]                 
                timeAtDeliver =  state.currentTime + distanceTime(state.currentLocation, deliverJobLocation)
                # Get the amount earned from arriving at destination location at time timeAtDeliver
                amountEarneds = amountEarned(jobFound[5], timeAtDeliver)
                lostRevenue = jobFound[5][0][1] - amountEarneds
                if lostRevenue > totalMaxLostRevenue:
                    totalMaxLostRevenue = lostRevenue
    #------------------------------------------------
    # Unstarted Job 
    #------------------------------------------------
    # For each job name available 
    for jobPickUpName in state.jobsToVisit:
        # Look for corresponding jobName in the list of jobs 
        for jobFound in state.jobList:
            # only execute if found the right job 
            if jobPickUpName == jobFound[0]:   
                jobName = jobFound[0] 
                pickUpJobLocation = jobFound[1] # get the job location to pick up 
                deliverJobLocation = jobFound[3]                                 
                # Add job to carrying 
                timeAtPickUp = state.currentTime + distanceTime(state.currentLocation, pickUpJobLocation) # Add the time taken from current location
                                                                                                  # of bicycle to the pickUplocation 
                # Handle waiting if arrive earlier 
                if jobFound[2] > timeAtPickUp:
                    timeAtPickUp = jobFound[2]     
                # Now find time to deliver 
                timeAtDeliver =  timeAtPickUp + distanceTime(pickUpJobLocation, deliverJobLocation)
                # Get the amount earned from arriving at destination location at time timeAtDeliver
                amountEarneds = amountEarned(jobFound[5], timeAtDeliver)
                lostRevenue = jobFound[5][0][1] - amountEarneds
                if lostRevenue > totalMaxLostRevenue:
                    totalMaxLostRevenue = lostRevenue
    return totalMaxLostRevenue

'''Have we reached the goal (where all jobs have been delivered)?'''
def bicycle_goal_fn(state):
#IMPLEMENT
    return state.jobsToVisit == [] and state.jobsCarried == []     

'''Input a map list and a job_list. Return a bicycle StateSpace object
with action "START", gval = 0, and initial location "home" that represents the 
starting configuration for the scheduling problem specified'''
def make_start_state(map, job_list):
#IMPLEMENT
    bicycle.mapList = map
    bicycle.jobList = job_list 
    jobsCarried = []  # Initialize jobsCarried to nothing 
    jobsFinished = [] # Initialize finishedJobs to nothing 
    jobsToVisit = []  # Initialize jobsToVisit
    # for all jobs in jobList, append their names to jobsToVisit 
    for eachJob in bicycle.jobList:
        jobName = eachJob[0] # Get the jobName 
        jobsToVisit.append(jobName) 
    # Initial state is START 
    # current cost is 0 before anything 
    # The list of jobs to visit 
    # Current Location is called home 
    # Current time is 420 minutes 
    # Current weight is 0 grams 
    # Current earned is 0 dollars 
    # The jobs carried are none 
    # The jobs done are none 
    # Do not give a parent so it defaults to None in __init__ 
    return bicycle("START", 0, jobsToVisit, "home", 420, 0, 0, jobsCarried, jobsFinished )    


#-------------------------------------------------------
# Helper Functions for class functions               
#-------------------------------------------------------

#---------------------------------------------
# To calculate distance between 2 locations 
#---------------------------------------------
# Given two locations, returns their distance from each other from the map 
def dist(l1, l2, map):
    '''Return distance from l1 to l2 in map (as output by make_rand_map)'''
    # Get the subset of the lists where it is the locations and their distances
    ldist = map[1]
    # If same location, return 0 as no distnace to travel 
    if l1 == l2:
        return 0
    # For each 3 pairs of values in the ldist list
    for [n1, n2, d] in ldist:
        # If the location is found, return the distance
        if (n1 == l1 and n2 == l2) or (n1 == l2 and n2 == l1):
            return d
    # Otherwise, location was not found, therefore return 0 
    return 0

# Given 2 locations A and B, find the journey time between A and B 
def distanceTime(l1, l2):
    return dist(l1, l2, bicycle.mapList)

#---------------------------------------------
# To calculate profit gained
#---------------------------------------------

def amountEarned(timeProfitList, timeAfterDone):
    for timeProfitPair in timeProfitList: 
        if (timeAfterDone <= timeProfitPair[0]): 
            return timeProfitPair[1]
    return 0

#-------------------------------------------------------
# Helper Functions to test implementation              
#-------------------------------------------------------

def make_rand_map(nlocs):
    '''Generate a random collection of locations and distances 
    in input format'''
    lpairs = [(randint(0,50), randint(0,50)) for i in range(nlocs)]
    lpairs = list(set(lpairs))  #remove duplicates
    nlocs = len(lpairs)
    lnames = ["loc{}".format(i) for i in range(nlocs)]
    ldists = list()

    for i in range(nlocs):
        for j in range(i+1, nlocs):
            ldists.append([lnames[i], lnames[j],
                           int(round(euclideandist(lpairs[i], lpairs[j])))])
    return [lnames, ldists]

    
def euclideandist(p1, p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def make_rand_jobs(map, njobs):
    '''input a map (as output by make_rand_map) object and output n jobs in input format'''
    jobs = list()
    for i in range(njobs):
        name = 'Job{}'.format(i)
        ploc = map[0][randint(0,len(map[0])-1)]
        ptime = randint(7*60, 16*60 + 30) #no pickups after 16:30
        dloci = randint(0, len(map[0])-1)
        if map[0][dloci] == ploc:
            dloci = (dloci + 1) % len(map[0])
        dloc = map[0][dloci]
        weight = randint(10, 5000)
        job = [name, ploc, ptime, dloc, weight]
        payoffs = list()
        amount = 50
        #earliest delivery time
        time = ptime + dist(ploc, dloc, map)
        for j in range(randint(1,5)): #max of 5 payoffs
            time = time + randint(5, 120) #max of 120mins between payoffs
            amount = amount - randint(5, 25)
            if amount <= 0 or time >= 19*60:
                break
            payoffs.append([time, amount])
        job.append(payoffs)
        jobs.append(job)
    return jobs

def test(nloc, njobs):
    map = make_rand_map(nloc)
    jobs = make_rand_jobs(map, njobs)
    print("Map = ", map)
    print("jobs = ", jobs)
    s0 = make_start_state(map, jobs)
    print("heur Sum = ", heur_sum_delivery_costs(s0))
    print("heur max = ", heur_max_delivery_costs(s0))
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, bicycle_goal_fn, heur_max_delivery_costs)