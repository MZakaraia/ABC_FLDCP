import numpy as np


#  Initialization Phase
def Initialize(popSize = 10, dim = 10, lb = -1, ub = 1):
    population = np.random.uniform(lb, ub, (popSize,dim))
    return population

def sphere(x):
    return sum(x**2)

def evaluationFunc(population):
    Evals = [sphere(i) for i in population]
    bestBee = population[np.argmin(Evals),:]
    return np.min(Evals), bestBee, Evals


#  Employed Bees Phase
def EmployedBeesFun(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals, BestEval, bestBee):
    k = 0
    for i in population:
        # fitness = CalculateFitness(Evals)
        # Probabilities = np.array([i/sum(fitness) for i in fitness])
        # Selected = np.random.choice(popSize, p = Probabilities)
        randchoice = np.random.choice([j for j in range(popSize) if j != k], 1)[0]
        rndBee = population[randchoice, :]
        Employed = bestBee + np.random.uniform(-a, a, dim)*(i - rndBee)
        # Employed = i + np.random.uniform(-a, a, dim)*(i - Selected)        
        EmployedEval = sphere(Employed)
        if EmployedEval <= Evals[k]:
            population[k] = Employed
            Evals[k] = EmployedEval
        if EmployedEval <= BestEval:
            BestEval = EmployedEval
            bestBee = Employed

        # Scout Bees Phase
        else:
            abandonmentVector[k] += 1
            if abandonmentVector[k] == abandonmentLimit:
                population[k] = np.random.uniform(0, 1, dim)
                Evals[k] = sphere(population[k])
                abandonmentVector[k] = 0
        k += 1
    # return population, Evals

def CalculateFitness(Evals):
    fitness = []
    for i in Evals:
        if i >= 0:
            fitness.append(1/(1+i))
        else:
            fitness.append(1+abs(i))
    return fitness

# Onlooker Bees Phase
def OnlookerBees(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals, BestEval, bestBee):
    k = 0
    for i in population:
        # fitness = CalculateFitness(Evals)
        # Probabilities = np.array([i/sum(fitness) for i in fitness])
        # Selected = np.random.choice(popSize, p = Probabilities)
        # Selected = population[np.argmin(Evals)]
        Onlooker = bestBee + np.random.uniform(-a, a, dim)*(i - bestBee)
        OnlookerEval = sphere(Onlooker)
        if OnlookerEval <= Evals[k]:
            population[k] = Onlooker
            Evals[k] = OnlookerEval
        if OnlookerEval <= BestEval:
            BestEval = OnlookerEval
            bestBee = Onlooker
        # Scout Bees Phase
        else:
            abandonmentVector[k] += 1
            if abandonmentVector[k] == abandonmentLimit:
                population[k] = np.random.uniform(0, 1, dim)
                Evals[k] = sphere(population[k])
                abandonmentVector[k] = 0
        k += 1
    # return population, Evals

def ABC_Algorithm(popSize, MaxItr, a, dim, abandonmentLimit, lb, ub):
    abandonmentVector = np.zeros(popSize)
    population = Initialize(popSize, dim, lb, ub)
    global BestEval, bestBee    
    BestEval, bestBee, Evals = evaluationFunc(population)
    # Evals = [sphere(i) for i in population]
    for _ in range(MaxItr):
        # Employed Bees Phase
        # population, Evals = EmployedBeesFun(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals)
        EmployedBeesFun(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals, BestEval, bestBee)
        # Onlooker Bees Phase 
        # population, Evals = OnlookerBees(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals)
        OnlookerBees(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals, BestEval, bestBee)
    
    return min(Evals), population[np.argmin(Evals)]