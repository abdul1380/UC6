'''
Created on 28 Jun 2020 from page 159 of Amita kapoor Honds on AI

@author: AbdulMannanRauf
'''
import string
import random
from  deap  import base,  creator, tools
import numpy as np


"""First Create a Fitness base class. weights is a tuple -1 for minimize, +1 for maximize.
then create an individual class which inherits the class list and tell deap module
to assign FitnessMax class in its Fitness attribute."""


    
    

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # FitnessMax is now name of base class
creator.create("Individual", list, fitness=creator.FitnessMax)

# Define how the gene pool will be created 
# Next  create an individual  and population by repeatedly using Individual class 

toolbox = base.Toolbox()
toolbox.register("attr_string", random.choice, string.digits )

word = list('54231')   
print(word)
N = len(word)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_string, N )
toolbox.register("population",tools.initRepeat, list, toolbox.individual)

# fitness function

def evalWord(individual, word):
    return sum(individual[i] == word[i] for i in range(len(individual))),

# add fitness function, crossover operator, mutation and parent selection operator to container

toolbox.register("evaluate", evalWord, word)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

'''    main code    of    the    GA, which will  perform    the  
steps we mentioned earlier    in    a    repetitive    manner: '''

if __name__ == '__main__':
    #random.seed(64)

# create initial population of 300 individuals 
    pop = toolbox.population(n=300) # pop is a list of 300 like 
    # [['E', 'h', 'O', 'N', 'z'], ['I', '6', 'R', 'b', 'n'], ['r', 'T', '6', 'Z', 'O'],....]
    CXPB, MUTPB = 0.5, 0.2  # crossover and mutation probability of an individual
    print("Start of evolution")
    fitnesses = list(map(toolbox.evaluate, pop)) #eval the entire population
    print(fitnesses)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print("  Evaluated %i individuals" % len(pop))
    
    fits = [ind.fitness.values[0] for ind in pop]  # Extracting all the fitnesses
    print(fits)
    # Variable keeping track of the number of generations
    g = 0
    
    # Begin the evolution
    while max(fits) < 5 and g < 200:
        g = g + 1    # A new generation
        print("-- Generation %i --" % g)
        offspring = toolbox.select(pop, len(pop))   # Select the next generation individuals
        print(np.shape(offspring))

        offspring = list(map(toolbox.clone, offspring))    # Clone the selected individuals
        print(offspring[::2])
        print(np.shape(offspring))

        
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]): # x[startAt:endBefore:skip]
            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                # fitness values of the children  must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print("  Evaluated %i individuals" % len(invalid_ind))
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
    print("-- End of (successful) evolution --")
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (''.join(best_ind), best_ind.fitness.values))
    
    best_ind = tools.selBest(pop, 1)[0]
     

        
        
        
        
            
                
            
                
                
                
                 
                  
                
                
        
        
        
        
        
        
        
        
        
        
     
    
    
    
    

