import random;
import numpy as npm
import math;
from deap import creator, base, tools, algorithms

# Training functions
def getAndValue(item):
    if (sum(item) == 2):
        return 1;
    return 0;


def getOrValue(item):
    if (sum(item) >= 1):
        return 1;
    return 0;


def getXOR(item):
    if (sum(item) == 1):
        return 1;
    return 0;


items = [[0, 1], [1, 0], [1, 1], [0, 0]];

truthFunction = getAndValue;

def squareFitness(individual):
    fitness = 0;
    for item in items:
        realValue = truthFunction(item);
        fitness += (realValue - getNeuralOutput(individual, item)) ** 2;
    return fitness,


def tweak(individual, prob, radius):
    mutant = toolbox.clone(individual)
    for i in range(len(individual)):
        if (random.random() <= prob):
            mutant[i] = mutant[i] + npm.random.uniform(-1, 1) * radius;
    return mutant,


bias = [1];  # hidden nodes


# Return the neural output given the weights and inputs
def getNeuralOutput(individual, item):
    index = 0;
    item = toolbox.clone(item)
    for i in bias:  # adding bias(es)
        item.append(i)
    oldLayer = item;
    for i in range(0, len(individual) / len(item) - 1):  # iterate through layers
        nextLayer = [];
        for l in range(0, len(item)):  # iterate through each node
            nextLayer.append(getZ(oldLayer, individual[index:(index + len(item))]));
            index += 1;
        oldLayer = nextLayer;
    return getSigmoidZ(oldLayer, individual[index:]);


# return sigmoid of (z)
def getSigmoidZ(inputs, weights):
    sumi = 0;
    for i in range(0, len(inputs)):
        sumi += inputs[i] * weights[i];
    return 1 / (1 + math.exp(-sumi));


toolbox = base.Toolbox();
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # minimising the fitness
creator.create("Individual", list, fitness=creator.FitnessMin);

toolbox.register("floatNum", random.random)
numLayers = 2;  # 2 layers for better complexity (XOR only return satisfied result when layers >= 2)
numBiases = len(bias);  # hidden nodes
numWeights = (len(items[0]) + numBiases) ** numLayers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.floatNum, n=numWeights)
toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=100)

toolbox.register("evaluate", squareFitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tweak, prob=1, radius=0.5);
toolbox.register("select", tools.selTournament, tournsize=3)

truthFuncs = [getAndValue, getOrValue, getXOR];
funcNames = ["AND logic weights: ", "OR logic weights: ", "(Prob 3)XOR logic weights: "]
weights = []

NGEN = 1000
for i in range(len(truthFuncs)):
    truthFunction = truthFuncs[i];
    population = toolbox.population();
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):  # match fitness
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

    print str(funcNames[i]) + " " + str(population[0]);
    print "";
    weights.append(population[0]);

# a smart/greedy approach for XOR could be:
# if(!(AND && OR) && (AND || OR)) -> true

print "\n---Testing weights---"
for i in range(len(truthFuncs)):
    print str(funcNames[i]);
    print "Truth Values:"
    for item in items:
        print str(item) + " : " + str(getNeuralOutput(weights[i], item))

    print "\n";
