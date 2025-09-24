import pandas as pd
import random


def GeneticAlgorithm(fileName, sheetName, populationAmount, amountOfJobsPerCombination, amountOfIterations, amountOfMutations):
    fileContent = pd.read_excel(fileName, sheet_name=sheetName, usecols=["id", "deadline", "profit"])
    jobs = fileContent.values.tolist()
    population = CreatePopulation(jobs, populationAmount, amountOfJobsPerCombination)
    population = list(population)
    print(population)
    population.sort(key=lambda x : x[2], reverse=True)
    x = 0
    amount = 1
    newPopulation = []
    for i in range(0, amountOfIterations+1):
        if len(population)< 2:
            population += newPopulation.copy()
            newPopulation = []
            population.sort(key=lambda x : x[2], reverse=True)
        if(x == 0):
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
        else:
            parent1 = population.pop(0)
            parent2 = population.pop()
            child = Crossover(parent1, parent2, amountOfJobsPerCombination)
            newPopulation.append(child)
            child = Crossover(parent2, parent1, amountOfJobsPerCombination)
            newPopulation.append(child)
            x = 0
            amount +=1
            if amountOfMutations > 0 and amount % amountOfMutations == 0:
                child = Mutate(child, amountOfJobsPerCombination)
        print(newPopulation[0])
    return newPopulation[0]

def CreatePopulation(jobs, populationAmount, amountOfJobsPerCombination):
    jobs = [tuple(job) for job in jobs]
    allCombinations = set()
    jobsToUse = jobs
    while len(allCombinations) < populationAmount:
        jobCombination = []
        for i in range(0, amountOfJobsPerCombination):
            if len(jobsToUse) > 0:
                jobCombination.append(tuple(jobsToUse.pop(random.randint(0, len(jobsToUse)-1))))
            else:
                jobsToUse = [jobs]
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
    crossoverPoint1 = random.randint(0, len(parent1) -1)
    crossoverPoint2 = random.randint(crossoverPoint1, len(parent1)-1)
    child = parent1[0:crossoverPoint1] + parent1[crossoverPoint2:]
    unusedElements = [item for item in parent2 if item not in child]
    while len(child) < amountOfJobsPerComnbination:
        child.append(unusedElements.pop())
    profit = sum(job[2] for job in child)
    child.append(profit)

    return child

def Mutate(child, amountOfJobsPerCombination):
    if len(child) > amountOfJobsPerCombination: #The profit can be at the end of the list
        child.pop()
    position1 = random.randint(0, len(child)-1)
    position2 = random.randint(position1+1, len(child)-1)
    child[position1], child[position2] = child[position2], child[position1]
    return child

def CalculateProfit(jobSequence, amountOfJobsPerCombination):
    profit = 0
    for jobIndex in range(0, amountOfJobsPerCombination):
        if jobIndex + 2 > jobSequence[jobIndex][1]:
            profit+= jobSequence[jobIndex][2]
    return profit

        


    



print(GeneticAlgorithm("example_problems.xlsx", "p4", 10, 10, 100, 10))

        

