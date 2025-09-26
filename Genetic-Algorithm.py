import pandas as pd
import random
#import unittest


def GeneticAlgorithm(fileName, sheetName, populationAmount, amountOfJobsPerCombination, amountOfIterations, amountOfMutations, onlyEliteSelection, onlyRandomSelection, eliteAndRandomSelection):
    fileContent = pd.read_excel(fileName, sheet_name=sheetName, usecols=["id", "deadline", "profit"])
    jobs = fileContent.values.tolist()
    population = CreatePopulation(jobs, populationAmount, amountOfJobsPerCombination)
    population = list(population)
    population.sort(key=lambda x : x[-1], reverse=True)
    x = 0
    amount = 1
    newPopulation = []
    for i in range(0, amountOfIterations+1):
        if len(population)< 2:
            population
            population += newPopulation.copy()
            newPopulation = []
            population.sort(key=lambda x : x[-1], reverse=True)
        if onlyEliteSelection or (eliteAndRandomSelection and (x == 0)):
            parent1 = population.pop(0)
            parent2 = population.pop(0)
            child = Crossover(parent1, parent2, amountOfJobsPerCombination )
            newPopulation.append(child)
            child = Crossover(parent2, parent1, amountOfJobsPerCombination)
            newPopulation.append(child)
            x = 1
            amount += 1
            if amountOfMutations > 0 and amount % amountOfMutations == 0:
                child = Mutate(child, amountOfJobsPerCombination)
        elif onlyRandomSelection or (eliteAndRandomSelection and x == 1):
            parent1 = population.pop(random.randint(0, len(population)-1))
            parent2 = population.pop(random.randint(0, len(population)-1))
            child = Crossover(parent1, parent2, amountOfJobsPerCombination)
            newPopulation.append(child)
            child = Crossover(parent2, parent1, amountOfJobsPerCombination)
            newPopulation.append(child)
            x = 0
            amount +=1
            if amountOfMutations > 0 and amount % amountOfMutations == 0:
                child = Mutate(child, amountOfJobsPerCombination)
        newPopulation.sort(key=lambda x : x[-1], reverse=True)
        print(newPopulation[0])
    newPopulation.sort(key=lambda x : x[-1], reverse=True)
    return newPopulation[0]

def CreatePopulation(jobs, populationAmount, amountOfJobsPerCombination):
    jobs = [tuple(job) for job in jobs]
    allCombinations = set()
    jobsToUse = jobs.copy()
    while len(allCombinations) < populationAmount:
        jobCombination = []
        if len(jobsToUse) < amountOfJobsPerCombination:
            random.shuffle(jobs)
            jobsToUse = jobs.copy()
        for i in range(0, amountOfJobsPerCombination):
                jobCombination.append(tuple(jobsToUse.pop(random.randint(0, len(jobsToUse)-1))))
        profit = CalculateProfit(jobCombination, amountOfJobsPerCombination)        
        jobCombination.append(profit)
        allCombinations.add(tuple(jobCombination))
    return allCombinations

def Crossover(parent1, parent2, amountOfJobsPerComnbination):
    parent1 = list(parent1)
    parent2 = list(parent2)
    parent1.pop(), parent2.pop()
    child = []
    crossoverPoint1 = random.randint(0, len(parent1) -2)
    crossoverPoint2 = random.randint(crossoverPoint1, len(parent1)-1)
    middle = parent1[crossoverPoint1:crossoverPoint2]
    unusedElements = [item for item in parent2 if item not in middle]
    for i in range(0, crossoverPoint1):
        if len(unusedElements) == 0:
            unusedElements = [item for item in parent1 if item not in child]
        child.append(unusedElements.pop(0))
    child += middle
    for i in range(len(child), amountOfJobsPerComnbination):
        if len(unusedElements) == 0:
            unusedElements = [item for item in parent1 if item not in child]
        child.append(unusedElements.pop(0))
    profit = CalculateProfit(child, amountOfJobsPerComnbination)
    child.append(profit)
    return child

def Mutate(child, amountOfJobsPerCombination):
    if len(child) > amountOfJobsPerCombination: #The profit can be at the end of the list
        child.pop()
    position1 = random.randint(0, len(child)-1)
    if position1 == len(child) -1:
        position2 = random.randint(0, len(child) - 2)
    else:    
        position2 = random.randint(position1+1, len(child) - 1)
    child[position1], child[position2] = child[position2], child[position1]
    child.append(CalculateProfit(child, amountOfJobsPerCombination))
    return child

def CalculateProfit(jobSequence, amountOfJobsPerCombination):
    profit = 0
    for jobIndex in range(0, amountOfJobsPerCombination):
        if jobIndex < jobSequence[jobIndex][1]:
            profit+= jobSequence[jobIndex][2]
    return profit

        

# print(CalculateProfit([(149, 8, 64), (82, 3, 77), (43, 2, 56), (15, 10, 1), (47, 4, 23), (169, 1, 70), (104, 8, 38), (60, 10, 52), (172, 1, 56), (19, 4, 12)], 10))
# assert(CalculateProfit([(149, 8, 64), (82, 3, 77), (43, 2, 56), (15, 10, 1), (47, 4, 23), (169, 1, 70), (104, 8, 38), (60, 10, 52), (172, 1, 56), (19, 4, 12)], 10)) == 232
# print(CalculateProfit([(13, 9, 74), (115, 8, 22), (100, 10, 20), (184, 10, 63), (56, 7, 8), (90, 10, 5), (195, 4, 62), (25, 10, 31), (57, 2, 97), (185, 9, 19)],10))
# assert(CalculateProfit([(13, 9, 74), (115, 8, 22), (100, 10, 20), (184, 10, 63), (56, 7, 8), (90, 10, 5), (195, 4, 62), (25, 10, 31), (57, 2, 97), (185, 9, 19)],10)) == 223
# print(CalculateProfit([(165, 3, 58), (12, 2, 81), (163, 7, 31), (45, 8, 40), (42, 3, 94), (129, 1, 9),(146, 7, 39), (81, 2, 60), (199, 9, 85), (193, 8, 59)], 10))
# assert(CalculateProfit([(165, 3, 58), (12, 2, 81), (163, 7, 31), (45, 8, 40), (42, 3, 94), (129, 1, 9), (146, 7, 39), (81, 2, 60), (199, 9, 85), (193, 8, 59)], 10)) == 334



print(GeneticAlgorithm("example_problems.xlsx", "p4", 1000, 10, 1000, 0, True, False, False))

        

