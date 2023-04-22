from numpy import random
from chromosome import Chromosome
from population import Population


class PopulationFactory:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def generate_population_fh(self, n, l, p_m, c_m, i):
        chromosomes = [self.fitness_function.generate_optimal(l)]

        start = len(chromosomes)

        for key in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code) 
            chromosomes.append(Chromosome(code, fitness, key + 1))

        return Population(chromosomes, p_m, c_m)

    def generate_population_fhd(self, n, l, p_m, c_m, i):
        chromosomes = [self.fitness_function.generate_optimal(l)]

        start = len(chromosomes)

        for key in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code) 
            chromosomes.append(Chromosome(code, fitness, key + 1))

        return Population(chromosomes, p_m, c_m)

    def generate_population_fx2(self, n, l, p_m, c_m, i):
        chromosomes = [self.fitness_function.generate_optimal(l)]
        
        start = len(chromosomes)

        for key in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code) 
            chromosomes.append(Chromosome(code, fitness, key + 1))

        return Population(chromosomes, p_m, c_m)

    def generate_population_fecx(self, n, l, p_m, c_m, i):
        chromosomes = [self.fitness_function.generate_optimal(l)]
        
        start = len(chromosomes)

        for key in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code) 
            chromosomes.append(Chromosome(code, fitness, key + 1))

        return Population(chromosomes, p_m, c_m)

    def generate_population_f5122subx2(self, n, l, p_m, c_m, i):
        chromosomes = [self.fitness_function.generate_optimal(l)]
        
        start = len(chromosomes)

        for key in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code) 
            chromosomes.append(Chromosome(code, fitness, key + 1))

        return Population(chromosomes, p_m, c_m)
