import math

from numpy import random
from chromosome import Chromosome
from population import Population
from coding import encode


class PopulationFactory:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def generate_population_fh(self, n, l, p_m, c_m, i):
        if i < 5 or p_m == 0:
            chromosomes = [self.fitness_function.generate_optimal(l)]
        else:
            chromosomes = []
        start = len(chromosomes)

        for j in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code)
            chromosomes.append(Chromosome(code, fitness, j + 1))
        return Population(chromosomes, p_m, c_m)

    def generate_population_fhd(self, n, l, p_m, c_m, i):
        if i < 5 or p_m == 0:
            chromosomes = [self.fitness_function.generate_optimal(l)]
        else:
            chromosomes = []
        start = len(chromosomes)

        for j in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code)
            chromosomes.append(Chromosome(code, fitness, j + 1))
        return Population(chromosomes, p_m, c_m)

    def generate_population_fx2(self, n, l, p_m, c_m, i):
        if i < 5 or p_m == 0:
            chromosomes = [self.fitness_function.generate_optimal(l)]
        else:
            chromosomes = []
        start = len(chromosomes)

        fitness_list = random.binomial(
            n=self.fitness_function.b**2, p=0.5, size=n - start
        )

        for y in fitness_list:
            x = round(math.sqrt(y), 2)
            code = encode(x, self.fitness_function.a, self.fitness_function.b, l)
            fitness = math.pow(x, 2)
            chromosomes.append(Chromosome(code, fitness, start + 1))
            start = start + 1

        return Population(chromosomes, p_m, c_m)

    def generate_population_fecx(self, n, l, p_m, c_m, i):
        if i < 5 or p_m == 0:
            chromosomes = [self.fitness_function.generate_optimal(l)]
        else:
            chromosomes = []

        key = len(chromosomes)

        fitness_list = random.binomial(
            n=math.exp(self.fitness_function.b * self.fitness_function.c),
            p=0.5,
            size=n - key,
        )

        for y in fitness_list:
            x = round(math.log(y) / self.fitness_function.c, 2)
            code = encode(x, self.fitness_function.a, self.fitness_function.b, l)
            fitness = math.exp(x * self.fitness_function.c)
            chromosomes.append(Chromosome(code, fitness, key + 1))
            key = key + 1

        return Population(chromosomes, p_m, c_m)

    def generate_population_f5122subx2(self, n, l, p_m, c_m, i):
        if i < 5 or p_m == 0:
            chromosomes = [self.fitness_function.generate_optimal(l)]
        else:
            chromosomes = []

        key = len(chromosomes)

        fitness_list = random.binomial(n=5.12**2, p=0.5, size=n - key)

        for y in fitness_list:
            x = round(math.sqrt(5.12**2 - y), 2)
            code = encode(x, -5.11, 5.12, l)
            fitness = math.pow(5.12, 2) - math.pow(x, 2)
            chromosomes.append(Chromosome(code, fitness, key + 1))
            key = key + 1

        return Population(chromosomes, p_m, c_m)
