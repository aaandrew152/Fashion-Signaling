"""
Wright Fisher Model for Fashion trends, modeled by costly signaling
"""

#import from __future__ division
import random
import math

"""
We consider 4 separate populations - one of low type senders, 
one of high type senders, one of low type receivers, and one of high type receivers.
Each of the sender populations interacts with the receiver populations in a signalling 
game, in which each sender chooses to either send no signal, send a normal signal, or send 
a hidden signal, and the receivers choose whether or not
to accept the sender.

This script initializes random populations of senders and receivers and then
updates the populations over many time steps. In each time step, the populations
play the above signalling game, receive payoffs, and then reproduce to create
a new population via Wright-Fisher updating. The ouput of the program is a
plot of the average signals of high and low types over time.

First we define several parameters we will need later.
"""
r = random.Random()

low_costs = [0, 0.9, 0.9]
high_costs = [0, 0.9, 0.9]
#Cost to send [no signal, signal, hidden signal]

low_accepted_payoff = [1, 2]
high_accepted_payoff = [1, 10]
#Payoffs of sender = [accepted by low receiver, high]

low_receiver_payoff = [-1, 2]
high_receiver_payoff = [-1, 4]
#Payoffs of receiver = [accept low sender, medium, high]

low_receiver_cost = 10
high_receiver_cost = 1/2
#Costs of investment

high_sender_fraction = 1/5 #Fraction of high senders
low_sender_fraction = 4/5
assert high_sender_fraction+low_sender_fraction == 1

high_receiver_fraction = 1/5
low_receiver_fraction = 4/5
assert high_receiver_fraction + low_receiver_fraction == 1

selection_strength = 1
mu = 0.02 #Mutation probability

size = 100 #Total number of senders (equal to number of receivers)
#Disadvised to use sizes greater than 150

time = 500 #Total number of generations

sender_strategies=[0, 1, 2]#0 = no signal, 1 = a normal signal, 2 = send but hide signal
receiver_strategies = [ [0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], 
                        [0,1,0,0], [0,1,0,1], [0,1,1,0], [0,1,1,1],
                        [1,0,0,0], [1,0,0,1], [1,0,1,0], [1,0,1,1], 
                        [1,1,0,0], [1,1,0,1], [1,1,1,0], [1,1,1,1]
                      ]


"""
A receiver strategy is of the following sort:
[accept no signal(if 1), accept common signal(if 1), 
accept hidden (if 1 and invested), invest (if 1)]
"""

## Next we define functions to get the payoffs for each type of player

def get_low_payoff(low_strategy, low_receiver_population, high_receiver_population):
    """
    Returns the payoff to a low type playing the given strategy
    Input: low type's strategy, population of receivers(low and high)
    Output: low type's average payoff across population of receivers
    """
    cost = low_costs[low_strategy]
    
    low_acceptances, high_acceptances = 0, 0
    
    for low_receiver in low_receiver_population:
        if low_strategy == 2:
            temp_strat = 2 if low_receiver[3] else 0#If they invested they recognize my hidden signal
        else:
            temp_strat = low_strategy#Otherwise my strategy is my normal strategy
            
        if low_receiver[temp_strat] == 1:
            low_acceptances += 1
    
    for high_receiver in high_receiver_population:
        if low_strategy == 2:
            temp_strat = 2 if high_receiver[3] else 0
        else:
            temp_strat = low_strategy
            
        if high_receiver[temp_strat] == 1:
            high_acceptances += 1
            
    payoff = low_accepted_payoff[0]*low_acceptances
    payoff += low_accepted_payoff[1]*high_acceptances
    payoff /= size
    payoff -= cost
    
    return payoff

def get_high_payoff(high_strategy, low_receiver_population, high_receiver_population):
    """
    Returns the payoff to a high type playing the given strategy
    Input: high type's strategy, population of receivers(low and high)
    Output: high type's average payoff across population of receivers
    """
    cost = high_costs[high_strategy]
    
    low_acceptances, high_acceptances = 0, 0
    
    for low_receiver in low_receiver_population:
        if high_strategy == 2:
            temp_strat = 2 if low_receiver[3] else 0
        else:
            temp_strat = high_strategy
            
        if low_receiver[temp_strat] == 1:
            low_acceptances += 1
    
    for high_receiver in high_receiver_population:
        if high_strategy == 2:
            temp_strat = 2 if high_receiver[3] else 0
        else:
            temp_strat = high_strategy
            
        if high_receiver[temp_strat] == 1:
            high_acceptances += 1
            
    payoff = high_accepted_payoff[0]*low_acceptances
    payoff += high_accepted_payoff[1]*high_acceptances
    payoff /= size
    payoff -= cost
    
    return payoff

def get_low_receiver_payoff(low_receiver_strategy, low_population, high_population):
    """
    Returns the payoff to a low receiver playing the given strategy
    Input: low receiver's strategy, populations of senders
    Output: low receiver's payoff
    """
    low_acceptances, high_acceptances = 0, 0
    invest = True if low_receiver_strategy[3] else False
    
    for low in low_population:
        if low == 2:#Test whether or not signal revealed
            temp_strat = 2 if invest else 0
        else:
            temp_strat = low
            
        if low_receiver_strategy[temp_strat] == 1:
            low_acceptances += 1
                  
    for high in high_population:
        if high == 2:#Test whether or not signal revealed
            temp_strat = 2 if low_receiver_strategy[3] else 0
        else:
            temp_strat = high
            
        if low_receiver_strategy[temp_strat] == 1:
            high_acceptances += 1
            
    payoff =  low_acceptances * low_receiver_payoff[0]
    payoff += high_acceptances * low_receiver_payoff[1]
    payoff -= low_receiver_cost if invest else 0
    
    return payoff

def get_high_receiver_payoff(high_receiver_strategy, low_population, high_population):
    """
    Returns the payoff to a high receiver playing the given strategy
    Input: high receiver's strategy, populations of senders
    Output: high receiver's payoff
    """
    low_acceptances, high_acceptances = 0, 0 
    
    invest = True if high_receiver_strategy[3] else False
    
    for low in low_population:
        if low == 2:#Test whether or not signal revealed
            temp_strat = 2 if invest else 0
        else:
            temp_strat = low
            
        if high_receiver_strategy[temp_strat] == 1:
            low_acceptances += 1
                  
    for high in high_population:
        if high == 2:#Test whether or not signal revealed
            temp_strat = 2 if invest else 0
        else:
            temp_strat = high
            
        if high_receiver_strategy[temp_strat] == 1:
            high_acceptances += 1
            
    payoff =  low_acceptances * high_receiver_payoff[0]
    payoff += high_acceptances * high_receiver_payoff[1]
    payoff -= high_receiver_cost if invest else 0
    
    return payoff

## Now we get fitnesses from payoffs and selection strength

def get_fitness(populations):
    """
    This function determines the fitness of each member of the population.
    Input: five lists of the populations with their strategies
    Output: five lists of fitnesses corresponding to the input populations
    """
    low_senders = populations[0]
    high_senders = populations[1]
    low_receivers = populations[2]
    high_receivers = populations[3]
    
    low_sender_fitnesses = []
    high_sender_fitnesses = []
    low_receiver_fitnesses = []
    high_receiver_fitnesses = []
        
    for low in low_senders:
        payoff = get_low_payoff(low, low_receivers, high_receivers)
        low_sender_fitnesses.append(math.exp(selection_strength*payoff))
        
    for high in high_senders:
        payoff = get_high_payoff(high, low_receivers, high_receivers)
        high_sender_fitnesses.append(math.exp(selection_strength*payoff))
        
    for low_rec in low_receivers:
        payoff = get_low_receiver_payoff(low_rec, low_senders, high_senders)
        low_receiver_fitnesses.append(math.exp(selection_strength*payoff))
    
    for high_rec in high_receivers:
        payoff = get_high_receiver_payoff(high_rec, low_senders, high_senders)
        high_receiver_fitnesses.append(math.exp(selection_strength*payoff))
            
    return [low_sender_fitnesses, high_sender_fitnesses, low_receiver_fitnesses, high_receiver_fitnesses]
                 
def reproduce(fitness):
    """
    Chooses a member of the population proportional to fitness
    Input: a list of fitness values
    Output: an index in range(0, len(fitness)) for the selected member
    """
    total_fitness = sum(fitness)
    scaled_fitness_intervals = [(sum(fitness[0:i+1]))/total_fitness for i in
                               range(len(fitness))]
    raw = r.uniform(0, 1)
    for i in range(len(scaled_fitness_intervals)):
        if raw < scaled_fitness_intervals[i]:
            return i

def update(populations):
    """
    This updates the population over 1 time step via Wright-Fisher
    Input: a list of members of the population with their strategies
    Output: a new population list, one time step later using Wright-Fisher
    """
    fitnesses = get_fitness(populations)
    new_population=[ [], [], [], [], ]

    for low in range(len(populations[0])):
        mutation = r.uniform(0, 1)
        if mutation < mu:
            new_population[0].append(random.choice(sender_strategies))
        else:
            new_population[0].append(populations[0][reproduce(fitnesses[0])])
            
    for high in range(len(populations[1])):
        mutation = r.uniform(0, 1)
        if mutation < mu:
            new_population[1].append(random.choice(sender_strategies))
        else:
            new_population[1].append(populations[1][reproduce(fitnesses[1])])
            
    for low_rec in range(len(populations[2])):
        mutation = r.uniform(0, 1)
        if mutation < mu:
            new_population[2].append(r.choice(receiver_strategies))
        else:
            new_population[2].append(populations[2][reproduce(fitnesses[2])]) 
            
    for high_rec in range(len(populations[3])):
        mutation = r.uniform(0, 1)
        if mutation < mu:
            new_population[3].append(r.choice(receiver_strategies))
        else:
            new_population[3].append(populations[3][reproduce(fitnesses[3])]) 
                   
    return new_population

def get_sender_portion(population, strategy):
    num_senders = 0
    for sender in population:
        if sender == strategy:
            num_senders += 1
    portion = num_senders / len(population)
    return portion

def get_receiver_portion(population, strategy):
    num_receivers = 0
    for receiver in population:
        if receiver[strategy] == 1:
            num_receivers += 1
    portion = num_receivers / len(population)
    return portion

def simulate(size, time):
    """
    Starts with a random initial population and updates for many time steps
    Input: population time, size, and mutation rate
    Output: pylab plots of population changes over time
    """
    populations=[ [], [], [], [], [] ]
        
    for i in range(size):
        if i < low_sender_fraction * size:
            populations[0].append(r.choice(sender_strategies))
        else:
            populations[1].append(r.choice(sender_strategies))
            
        if i < low_receiver_fraction * size:
            populations[2].append(r.choice(receiver_strategies))
        else:
            populations[3].append(r.choice(receiver_strategies))
                
    for i in range(time):#Runs the simulation
        populations = update(populations)
    
    print ("These are the proportions of senders who send each strategy")    
    for sender in range(2):#Outputs sender strategy proportions
        for signal in range(3):
            print ("Type: " + str(sender) + " Signal: " + str(signal) + " " + str(get_sender_portion(populations[sender], signal)))
    
    print ("These are the proportions of receivers who accept a strategy") 
    #NOTE THESE VALUES DO NOT NEED TO SUM TO 1, a receiver may accept more than one strategy       
    for receiver in range(2):#Outputs receiver strategy's
        for signal in range(3):
            print ("Type: " + str(receiver) + " Signal: " + str(signal) + " "+ str(get_receiver_portion(populations[receiver+2], signal)))
        print ("Type: " + str(receiver) + " Invests: " + " "+ str(get_receiver_portion(populations[receiver+2], 3)))
    
simulate(size, time)