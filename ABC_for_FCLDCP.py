import numpy as np
import HeuristicApproach as ha
import copy


#  Initialization Phase
def Initialize(popSize , Demands, Capacities):
    population = [ha.solStucture(Demands, Capacities) for _ in range(popSize)]
    return population

def sphere(x):
    return sum(x**2)

def evaluationFunc(population, TransCosts, FixedCosts):
    # Evals = [i.Evaluate(TransCosts, FixedCosts) for i in population]
    Evals = []
    for i in population:
        i.GenerateSolution()
        Evals.append(i.Evaluate(TransCosts, FixedCosts))

    bestBee = population[np.argmin(Evals)]
    return np.min(Evals), bestBee, Evals


#  Employed Bees Phase
def EmployedBeesFun(population, a, popSize, abandonmentVector, abandonmentLimit, Evals, BestEval, bestBee\
    , Demands, Capacities, TransCosts, FixedCosts):
    k = 0
    for i in population:
        randchoice = np.random.choice([j for j in range(popSize) if j != k], 1)[0]
        rndBee = population[randchoice]
        Employed = copy.deepcopy(i)
        Employed.DistCenterArray = Employed.DistCenterArray + np.random.uniform(-a, a, Employed.NumberOFDistCenter)*(Employed.DistCenterArray - rndBee.DistCenterArray)
        Employed.PlantArray = Employed.PlantArray + np.random.uniform(-a, a, Employed.NumberOfPlants)*(Employed.PlantArray - rndBee.PlantArray)  
        EmployedEval = Employed.Evaluate(TransCosts, FixedCosts)
        if EmployedEval <= Evals[k]:
            population[k] = copy.deepcopy(Employed)
            Evals[k] = EmployedEval
        if EmployedEval <= BestEval:
            BestEval = EmployedEval
            bestBee = copy.deepcopy(Employed)

        # Scout Bees Phase
        else:
            abandonmentVector[k] += 1
            if abandonmentVector[k] == abandonmentLimit:
                population[k] = ha.solStucture(Demands, Capacities)
                Evals[k] = population[k].Evaluate(TransCosts, FixedCosts)
                abandonmentVector[k] = 0
        k += 1
    return population, Evals, BestEval, bestBee

def CalculateFitness(Evals):
    fitness = []
    for i in Evals:
        if i >= 0:
            fitness.append(1/(1+i))
        else:
            fitness.append(1+abs(i))
    return fitness

# Onlooker Bees Phase
def OnlookerBees(population, a, popSize, abandonmentVector, abandonmentLimit, Evals, BestEval, bestBee\
    , Demands, Capacities, TransCosts, FixedCosts):
    k = 0
    for i in population:
        Onlooker = copy.deepcopy(i)
        Onlooker.DistCenterArray = bestBee.DistCenterArray + np.random.uniform(-a, a, Onlooker.NumberOFDistCenter)\
            *(Onlooker.DistCenterArray - bestBee.DistCenterArray)
        Onlooker.PlantArray = bestBee.PlantArray + np.random.uniform(-a, a, Onlooker.NumberOfPlants)*(Onlooker.PlantArray - bestBee.PlantArray)  
        OnlookerEval = Onlooker.Evaluate(TransCosts, FixedCosts)
        if OnlookerEval <= Evals[k]:
            population[k] = copy.deepcopy(Onlooker)
            Evals[k] = OnlookerEval
        if OnlookerEval <= BestEval:
            BestEval = OnlookerEval
            bestBee = copy.deepcopy(Onlooker)
        # Scout Bees Phase
        else:
            abandonmentVector[k] += 1
            if abandonmentVector[k] == abandonmentLimit:
                population[k] = ha.solStucture(Demands, Capacities)
                Evals[k] = population[k].Evaluate(TransCosts, FixedCosts)
                abandonmentVector[k] = 0
        k += 1
    return population, Evals, BestEval, bestBee

def ABC_Algorithm_FCLDCP(popSize, MaxItr, a, abandonmentLimit, Demands, Capacities, TransCosts, FixedCosts):
    abandonmentVector = np.zeros(popSize)
    population = Initialize(popSize , Demands, Capacities)
    # global BestEval, bestBee    
    BestEval, bestBee, Evals = evaluationFunc(population, TransCosts, FixedCosts)
    # Evals = [sphere(i) for i in population]
    # BestEvalCopy = copy.deepcopy(BestEval)
    ConvergenceVector = [BestEval]
    for _ in range(MaxItr):
        # print(BestEval)
        # Employed Bees Phase
        # population, Evals = EmployedBeesFun(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals)
        population, Evals, BestEval, bestBee = EmployedBeesFun(population, a, popSize, abandonmentVector, abandonmentLimit, Evals, BestEval, bestBee\
                , Demands, Capacities, TransCosts, FixedCosts)
        # Onlooker Bees Phase 
        # population, Evals = OnlookerBees(population, a, popSize, abandonmentVector, abandonmentLimit, dim, Evals)
        population, Evals, BestEval, bestBee = OnlookerBees(population, a, popSize, abandonmentVector, abandonmentLimit, Evals, BestEval, bestBee\
                , Demands, Capacities, TransCosts, FixedCosts)
        # BestEvalCopy = copy.deepcopy(BestEval)
        ConvergenceVector.append(BestEval)
    
    return bestBee, ConvergenceVector