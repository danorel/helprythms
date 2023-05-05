import numpy as np

from chromosome import Chromosome
from constants import DELTA, SIGMA, N
from population import Population
from population_factory import PopulationFactory
from coding import *


class FHD:
    def __init__(self, delta: float = 100.0):
        self.delta = delta
        self.extremum_x = 0
        self.extremum_y = self.estimate([0]*100) 
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        k = np.count_nonzero(chromosome_code)
        return k

    def estimate(self, chromosome_code):
        l = len(chromosome_code)
        k = l - np.count_nonzero(chromosome_code)
        return (l - k) + k * self.delta

    def generate_optimal(self, length):
        coding = np.zeros((length, ), dtype=int)
        return Chromosome(coding, self.estimate(coding))

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def __repr__(self):
        return "FHD"


class FConst:
    def __init__(self):
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        k = np.count_nonzero(chromosome_code)
        return k

    def estimate(self, chromosome: Chromosome):
        return len(chromosome.code)

    def generate_optimal(self, length: int):
        return [
            Chromosome(np.zeros((length,), dtype=int), length),
            Chromosome(np.ones((length,), dtype=int), length),
        ]

    def generate_population(self, n, l):
        chromosomes = self.generate_optimal(l) * int(n / 2)
        population = Population(chromosomes)
        population.override_chromosome_keys()
        return population

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def __repr__(self):
        return "FConst"


class Fx2:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self.extremum_x = b
        self.extremum_y = math.pow(b, 2)
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.pow(x, 2)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        y = self.score(x)
        return y

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def generate_optimal(self, length):
        coding = encode(self.extremum_x, self.a, self.b, length)
        return Chromosome(coding, self.estimate(coding))

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        y = self.score(x)
        return abs(self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA

    def __repr__(self):
        return "Fx2"


class F5122subx2:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self.extremum_x = .0
        self.extremum_y = math.pow(5.12, 2)
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.pow(5.12, 2) - math.pow(x, 2)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        y = self.score(x)
        return y

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        coding = encode(self.extremum_x, self.a, self.b, length)
        return Chromosome(coding, self.estimate(coding))

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        y = self.score(x)
        return abs(self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA
    
    def __repr__(self):
        return "F5122subx2"


class Fecx:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c
        self.extremum_x = b
        self.extremum_y = math.exp(c * b)
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.exp(self.c * x)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return self.score(x)

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def generate_optimal(self, length):
        coding = encode(self.extremum_x, self.a, self.b, length)
        return Chromosome(coding, self.estimate(coding))

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        y = self.score(x)
        return abs(self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA

    def __repr__(self):
        return "Fecx"
