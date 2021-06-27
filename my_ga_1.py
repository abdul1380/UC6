import numpy as np

def cal_pop_fitness(tariffs, i_ga,grid_limits): 
    # Calculating the fitness value of each solution in the current population.
    cost_b = np.zeros((i_ga.shape[0],i_ga.shape[1]))    # same shape as i_ga  (100,24)
    E = np.zeros((i_ga.shape[0],i_ga.shape[1]))   # same shape as i_ga  (100,24)
    cost = np.zeros((i_ga.shape[0],i_ga.shape[1]))   # same shape as i_ga  (100,24)
    soft_cost = np.zeros((i_ga.shape[0],i_ga.shape[1]))   # same shape as i_ga  (100,24)
    soft_cost_b = np.zeros((i_ga.shape[0],i_ga.shape[1]))   # same shape as i_ga  (100,24)
    for i in range(i_ga.shape[0]):
        for j in range(i_ga.shape[1]):
            if i_ga[i][j] > grid_limits[j]: 
                cost_b[i][j] = 1000000  
            if i_ga[i][j] < 60: 
                soft_cost[i][j] = 10*(60-i_ga[i][j])
                
            if i>0 and j>0 :
                if i_ga[i][j] > i_ga[i-1][j-1]: 
                    soft_cost_b[i][j] = i_ga[i][j] - i_ga[i-1][j-1]
            
            E[i][j] = i_ga[i][j]*400/12000
            cost[i][j] = E[i][j]*tariffs[j]
            
    cost_energy = np.sum(cost, axis=1)     
    E1 = np.sum(E, axis=1)   # doing sum of each row to make (100,1)  like E below
    cost_b1 = np.sum(cost_b, axis=1)   # doing sum of each row to make (100,1)  like E below
    soft_cost = np.sum(soft_cost , axis=1)   # doing sum of each row to make (100,1)  like E below
    soft_cost_b = np.sum(soft_cost_b , axis=1)   # doing sum of each row to make (100,1)  like E below        
    #E = np.sum(i_ga*400/12000, axis=1)
    #cost =  np.sum(tariffs*i_ga*400/12000, axis=1)
    cost_a = [0 for i in range(len(E1)) ] 
    for i in range(len(E1)):
        if E1[i] < 40 or E1[i] > 40.1:
            cost_a[i] = 1000000   
    fitness_cost =  cost_energy + cost_b1 + cost_a + soft_cost + soft_cost_b

    return fitness_cost

def select_mating_pool(i_ga, fitness_cost, num_parents_mating):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents_mating, i_ga.shape[1]))
    for i in range(num_parents_mating):
        min_fitness_cost_idx = np.where(fitness_cost == np.min(fitness_cost))
        min_fitness_cost_idx = min_fitness_cost_idx[0][0]
        parents[i,:] = i_ga[min_fitness_cost_idx, :]
        fitness_cost[min_fitness_cost_idx] = 999999999999
    return parents

def crossover(best_parents, offspring_size):
    offspring = np.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = np.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%best_parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%best_parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = best_parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = best_parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        random_value = np.random.uniform(0, 120, 4)
        offspring_crossover[idx,20:] =  random_value  # 
    return offspring_crossover