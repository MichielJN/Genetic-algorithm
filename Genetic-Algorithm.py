import pandas as pd
import random


def GeneticAlgorithm(fileName:str, sheetName:str, populationAmount:int, amountOfJobsPerCombination:int, amountOfIterations:int, amountOfMutations:int, onlyEliteSelection:bool, onlyRandomSelection:bool, eliteAndRandomSelection:bool):
    """
    This is the part where everything comes together and that runs the algorithm. 
    One of the last three parameters should be True and the other two should be False.
    fileName = The directory of the file with the jobs.
    sheetName = The sheet that has to be used.
    populationAmount = How many sequences of jobs each generation should have.
    amountOfJobsPerCombination = How many jobs each sequence of jobs should have.
    amountOfIterations = How many times should crossovers happen.
    amountOfMutations = Per how many iterations should a mutation happen?
    onlyEliteSelection = Selection for crossovers happens like this: best is pared with second best, third best with fourth best...
    onlyRandomSelection = Two random parents out of the population will be selected for the crossovers.
    eliteAndRandomSelection = First the best will be paired with second best, then two random parents will be selected. And so on...
    """

    fileContent = pd.read_excel(fileName, sheet_name=sheetName, usecols=["id", "deadline", "profit"])
    jobs = fileContent.values.tolist()
    population = CreatePopulation(jobs, populationAmount, amountOfJobsPerCombination)
    population = list(population)
    population.sort(key=lambda x : x[-1], reverse=True)
    print(population[0])
    x = 0 #This is to decide wheter to use elite selection or random selection if eliteAndRandomSelection is True
    amount = 1
    newPopulation = []
    bestOverall = population[0]

    for i in range(0, amountOfIterations+1):
        if len(population)< 2:
            population += newPopulation.copy()
            newPopulation = []
            population.sort(key=lambda x : x[-1], reverse=True)
            if population[0][-1] > bestOverall[-1]:
                bestOverall = population[0]

        if onlyEliteSelection or (eliteAndRandomSelection and (x == 0)):#Random selection.
            parent1 = population.pop(0)
            parent2 = population.pop(0)
            children = ApplyCrossoverAndMutation(parent1, parent2, amountOfMutations, amountOfJobsPerCombination, amount)
            newPopulation.append(children[0])
            newPopulation.append(children[1])
            x = 1
            amount += 1
        elif onlyRandomSelection or (eliteAndRandomSelection and x == 1):#Elite selection.
            parent1 = population.pop(random.randint(0, len(population)-1))
            parent2 = population.pop(random.randint(0, len(population)-1))
            children = ApplyCrossoverAndMutation(parent1, parent2, amountOfMutations, amountOfJobsPerCombination, amount)
            newPopulation.append(children[0])
            newPopulation.append(children[1])
            x = 0
            amount +=1

    newPopulation.sort(key=lambda x : x[-1], reverse=True) 
    print(newPopulation[0])#Print the best of the last iteration.

    if newPopulation[0][-1] > bestOverall[-1]:
        bestOverall = newPopulation[0]

    return bestOverall

def ApplyCrossoverAndMutation(parent1, parent2, amountOfMutations, amountOfJobsPerCombination, iteration):
    """
    Does the crossover and the mutation if it is the right iteration to do so.
    """

    child1 = Crossover(parent1, parent2, amountOfJobsPerCombination )
    child2 = Crossover(parent2, parent1, amountOfJobsPerCombination)

    if amountOfMutations > 0 and iteration % amountOfMutations == 0:
        child1 = Mutate(child1, amountOfJobsPerCombination)
        child2 = Mutate(child2, amountOfJobsPerCombination)

    return [child1, child2]

def CreatePopulation(jobs, populationAmount, amountOfJobsPerCombination):
    """
    Creates a population without duplicates.
    """

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
    """
    This crossover takes the middle part of parent1 and then wraps unused parts of
    parent 2 in order around it (So if every part of parent 2 can be used it means that
    if index 2-6 is used of parent 1 it will put index 7, 8 and 9 of parent 2 at  the end and 1 at the beginning).
    if parent2 doesn't have enough unused elements it will add unused elements of parent1 to the end of unused elements.
    """

    parent1 = list(parent1)
    parent2 = list(parent2)
    parent1.pop(), parent2.pop()
    child = [None]*amountOfJobsPerComnbination

    crossoverPoint1 = random.randint(0, len(parent1) -2)
    crossoverPoint2 = random.randint(crossoverPoint1, len(parent1)-1)
    middle = parent1[crossoverPoint1:crossoverPoint2]

    child[crossoverPoint1:crossoverPoint2] = middle
    parent2 = Rotate(True, parent2.copy(), crossoverPoint2)
    unusedElements = [item for item in parent2 if item not in middle]

    if len(unusedElements + middle) < amountOfJobsPerComnbination:
        unusedElements += [item for item in parent1 if item not in child]

    pieceAfterMiddle = unusedElements[0:amountOfJobsPerComnbination-crossoverPoint2]     
    pieceBeforeMiddle = unusedElements[ len(pieceAfterMiddle): len(pieceAfterMiddle)+crossoverPoint1]    
    child[crossoverPoint2:amountOfJobsPerComnbination] = pieceAfterMiddle 
    child[0:crossoverPoint1] = pieceBeforeMiddle

    profit = CalculateProfit(child, amountOfJobsPerComnbination)
    child.append(profit)

    return child

def Mutate(child, amountOfJobsPerCombination):
    """
    Tries to find a job with a deadline that isnt valid for its position.
    Then searches for a job that is valid for the position of the first job but 
    the deadline of the first job should also be valid for the position of that job.
    If it cant find that it will use the invalid job that has the most profit and rotate
    the child left unil that job is in a place that it is valid.
    """

    bestProfit = [(0, 0, 0), 0]

    if len(child) > amountOfJobsPerCombination: #The profit can be at the end of the list
        child.pop()

    for i in range(-1, -amountOfJobsPerCombination-1, -1):
        if child[i][2] > bestProfit[0][2]:
            bestProfit = [child[i], amountOfJobsPerCombination+ i]

        if amountOfJobsPerCombination+i >= child[i][1]:
            for j in range(0, amountOfJobsPerCombination):
                if j < child[i][1] and amountOfJobsPerCombination + i < child[j][1]:
                    child[i], child[j] = child[j], child[i]
                    child.append(CalculateProfit(child, amountOfJobsPerCombination))

                    return child
                
    child = Rotate(True, child, bestProfit[1]-bestProfit[0][1]-1 )
    child.append(CalculateProfit(child, amountOfJobsPerCombination))

    return child

def CalculateProfit(jobSequence, amountOfJobsPerCombination):
    """
    Calculates how much profit a collection of jobs has.
    for example a job with deadline 1 counts in index 0 but not in index 1.
    """

    profit = 0

    for jobIndex in range(0, amountOfJobsPerCombination):
        if jobIndex < jobSequence[jobIndex][1]:
            profit+= jobSequence[jobIndex][2]

    return profit

def Rotate(left, collection, steps):
    """
    Rotates a list right or left,
    this is used as fallback in the mutation and
    to wrap parent2 in order around the middle part that
    is taken from parent 1 in the crossover.
    """

    newList = []
    steps = steps %len(collection)

    if left:
        for i in range(steps, len(collection)+steps):
            if i > len(collection)-1:
                newList.append(collection[i-len(collection)])
            else:
                newList.append(collection[i])
    else:
        for i in range(-steps, len(collection)-steps):
            newList.append(collection[i])

    return newList



# print(CalculateProfit([(149, 8, 64), (82, 3, 77), (43, 2, 56), (15, 10, 1), (47, 4, 23), (169, 1, 70), (104, 8, 38), (60, 10, 52), (172, 1, 56), (19, 4, 12)], 10))
# assert(CalculateProfit([(149, 8, 64), (82, 3, 77), (43, 2, 56), (15, 10, 1), (47, 4, 23), (169, 1, 70), (104, 8, 38), (60, 10, 52), (172, 1, 56), (19, 4, 12)], 10)) == 232
# print(CalculateProfit([(13, 9, 74), (115, 8, 22), (100, 10, 20), (184, 10, 63), (56, 7, 8), (90, 10, 5), (195, 4, 62), (25, 10, 31), (57, 2, 97), (185, 9, 19)],10))
# assert(CalculateProfit([(13, 9, 74), (115, 8, 22), (100, 10, 20), (184, 10, 63), (56, 7, 8), (90, 10, 5), (195, 4, 62), (25, 10, 31), (57, 2, 97), (185, 9, 19)],10)) == 223
# print(CalculateProfit([(165, 3, 58), (12, 2, 81), (163, 7, 31), (45, 8, 40), (42, 3, 94), (129, 1, 9),(146, 7, 39), (81, 2, 60), (199, 9, 85), (193, 8, 59)], 10))
assert(CalculateProfit([(165, 3, 58), (12, 2, 81), (163, 7, 31), (45, 8, 40), (42, 3, 94), (129, 1, 9), (146, 7, 39), (81, 2, 60), (199, 9, 85), (193, 8, 59)], 10)) == 334
print(GeneticAlgorithm("example_problems.xlsx", "p4", 1000, 10, 49999, 6, False, False, True))

        

