import numpy as np
import pandas as pd

def GenerateProblems(NumberOfProblems = 10, MinTransCost = 30, MaxTransCost = 80, MinFixedCost = 70, MaxFixedCost = 120\
                     , NumberOFDistCenter = 10, NumberOfPlants = 5, MinDemand = 20,  MaxDemand = 50, MinCapacity = 50\
                        , MaxCapacity = 100):
    for i in range(NumberOfProblems):
        ProblemName = 'Problem ' + str(i+1)+ '.xlsx'
        pd.DataFrame(np.random.randint(MinTransCost, MaxTransCost,(NumberOFDistCenter, NumberOfPlants)),\
                        columns=['Plant ' + str(j+1) for j in range(NumberOfPlants)],\
                        index=['Center ' + str(j+1) for j in range(NumberOFDistCenter)]).to_excel\
                            (ProblemName, sheet_name='Transportation Costs')
        with pd.ExcelWriter(ProblemName, engine='openpyxl', mode='a') as writer:
            pd.DataFrame(np.random.randint(MinFixedCost, MaxFixedCost, NumberOFDistCenter), columns=['Fixed Costs']\
                            , index=['Center '+ str(j+1) for j in range(NumberOFDistCenter)]).to_excel(writer, sheet_name='Fixd Costs')
            randDemand = np.random.randint(MinDemand, MaxDemand, (NumberOfPlants, 3))
            randDemand.sort()
            pd.DataFrame(randDemand, columns=['min', 'Most likely', 'max'], index=['Plant ' + str(j+1) for j in range(NumberOfPlants)])\
                .to_excel(writer, sheet_name='Demands')
            pd.DataFrame(np.random.randint(MinCapacity, MaxCapacity, NumberOFDistCenter), columns=['Capacity'], index=['Center '+str(j+1) \
                for j in range(NumberOFDistCenter)]).to_excel(writer, sheet_name='Capacities')

##########################################################################
def BubbleSortProcedure(x, y):
    y_length = len(y)
    j = 0
    test = 1
    while(test == 1):
        test = 0
        for i in range(y_length - j - 1):
            if y[i] < y[i+1]:
                temp = y[i]
                temp2 = x[i]
                y[i] = y[i+1]
                x[i] = x[i+1]
                y[i+1] = temp
                x[i+1] = temp2
                test = 1
        j += 1

##########################################################################
def GenerateDemands(Demands, membershipvalue):
    DeterministicDemand = np.array([], dtype=int)
    for i in Demands:
        D1 = membershipvalue * (i[1] - i[0]) + i[0]
        D2 = i[2] - membershipvalue * (i[2] - i[1])        
        DeterministicDemand = np.append(DeterministicDemand,int(D1 + np.random.uniform() * (D2 - D1)))
    return DeterministicDemand

##########################################################################
def ReadProblem(fileName):
    Capacities = np.array(pd.read_excel(fileName + ".xlsx", sheet_name='Capacities').iloc[:,1])
    Demands = np.array(pd.read_excel(fileName + ".xlsx", sheet_name='Demands').iloc[:,1:])
    FixedCosts = np.array(pd.read_excel(fileName + ".xlsx", sheet_name='Fixd Costs').iloc[:,1])
    TransPortationCosts = np.array(pd.read_excel(fileName + ".xlsx", sheet_name='Transportation Costs').iloc[:,1:])
    return Capacities, Demands, FixedCosts, TransPortationCosts

##########################################################################
class solStucture:
    def __init__(self, Demands, Capacities):
        self.NumberOFDistCenter = len(Capacities)
        self.NumberOfPlants = len(Demands)
        self.DistCenterArray = np.random.uniform(0, 1, self.NumberOFDistCenter)
        self.PlantArray = np.random.uniform(0, 1, self.NumberOfPlants)
        self.membershipvalue = np.round(np.random.uniform(), 2)

        self.Demands = Demands
        self.Capacities = Capacities
        self.solution = np.zeros((self.NumberOFDistCenter, self.NumberOfPlants), dtype=int)
    
    def GenerateSolution(self):
        self.solution = np.zeros((self.NumberOFDistCenter, self.NumberOfPlants), dtype=int)
        D = GenerateDemands(self.Demands, self.membershipvalue)
        C = self.Capacities.copy()
        self.D, self.C = D.copy(), C.copy()
        Centers = list(range(self.NumberOFDistCenter))
        plants = list(range(self.NumberOfPlants))
        BubbleSortProcedure(Centers,  self.DistCenterArray.copy())
        # print(Centers)
        BubbleSortProcedure(plants,  self.PlantArray.copy())
        # print(plants)
        while(len(plants) != 0):
            plant = plants[0]
            while(plant in plants):
                if D[plant] < C[Centers[0]]:
                    C[Centers[0]] = C[Centers[0]] - D[plant]
                    self.solution[Centers[0], plant] = D[plant]
                    np.delete(D, plant)
                    del plants[0]
                elif D[plant] > C[Centers[0]]:
                    D[plant] = D[plant] - C[Centers[0]]
                    self.solution[Centers[0], plant] = C[Centers[0]]
                    np.delete(C, Centers[0])
                    del Centers[0]
                else:
                    self.solution[Centers[0], plant] = D[plant]
                    np.delete(C, Centers[0])
                    del Centers[0]
                    np.delete(D, plant)
                    del plants[0]
                    
    def Evaluate(self, TransCosts, FixedCosts):
        self.GenerateSolution()
        self.Eval = (self.solution * TransCosts).sum() + sum(np.clip(self.solution.sum(axis=1), 0, 1) *FixedCosts)
        return self.Eval        
