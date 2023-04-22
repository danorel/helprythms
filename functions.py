import os

import numpy as np
import matplotlib.pyplot as plt

from chromosome import Chromosome
from constants import DELTA, SIGMA, N
from population import Population
from population_factory import PopulationFactory
from coding import *


def _draw_fitness_histogram(
    population: Population,
    folder_name: str,
    func_name: str,
    run: int,
    iteration: int,
) -> None:
    dir_path = f"Function/{N}/{func_name}/{folder_name}/{run}/genotypes"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    plt.figure()
    plt.hist(population.fitness_list, bins=100, color="green", histtype="bar", rwidth=1)

    # x-axis label
    plt.xlabel("Health")
    # frequency label
    plt.ylabel("Num of individual")
    # plot title

    plt.title("Phenotypes (fitness)")
    plt.savefig(f"{dir_path}/{iteration}.png")
    plt.close()


def _draw_phenotype_histogram(
    a: float,
    b: float,
    population: Population,
    folder_name: str,
    func_name: str,
    run: int,
    iteration: int,
) -> None:
    dir_path = f"Function/{N}/{func_name}/{folder_name}/{run}/phenotypes"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    phenotypes = [
        decode(chromosome.code, a, b, len(chromosome.code))
        for chromosome in population.chromosomes
    ]

    plt.figure()
    plt.hist(phenotypes, bins=100, color="red", histtype="bar", rwidth=None)

    # x-axis label
    plt.xlabel("X")
    # frequency label
    plt.ylabel("Num of individual")
    # plot title

    plt.title("Genotype (x)")

    plt.savefig(f"{dir_path}/{iteration}.png")
    plt.close()


def _draw_count_ones_in_genotype_histogram(
    population: Population,
    folder_name: str,
    func_name: str,
    run: int,
    iteration: int,
) -> None:
    dir_path = f"Function/{N}/{func_name}/{folder_name}/{run}/ones_in_genotypes"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    ones = [
        sum(chromosome.code)
        for chromosome in population.chromosomes
    ]
    bins = 100

    plt.figure()
    plt.hist(
        ones, bins, color="red", histtype="bar", rwidth=1
    )

    # x-axis label
    plt.xlabel("Ones in genotype")
    # frequency label
    plt.ylabel("Num of individual")
    # plot title
    plt.title("Number of ones in chromosome")

    plt.savefig(f"{dir_path}/{iteration}.png")
    plt.close()


class FH:
    def __init__(self):
        self.factory = PopulationFactory(self)

    def estimate(self, chromosome_code):
        l = len(chromosome_code)
        k = np.count_nonzero(chromosome_code)
        return l - k

    def get_genotype_value(self, chromosome_code):
        k = np.count_nonzero(chromosome_code)
        return k

    def generate_optimal(self, length):
        return Chromosome(np.zeros((length,), dtype=int), length)

    def get_optimal(self, n, l, p_m, c_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, c_m, i):
        return self.factory.generate_population_fh(n, l, p_m, c_m, i)

    def draw_histograms(
        self,
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )


class FHD:
    def __init__(self, delta: float = 100.):
        self.delta = delta
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        k = np.count_nonzero(chromosome_code)
        return k

    def estimate(self, chromosome_code):
        l = len(chromosome_code)
        k = np.count_nonzero(chromosome_code)
        return (l - k) + k * self.delta

    def generate_optimal(self, length):
        return Chromosome(np.zeros((length,), dtype=int), length * self.delta)

    def get_optimal(self, n, l, p_m, c_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, c_m, i):
        return self.factory.generate_population_fhd(n, l, p_m, c_m, i)

    def draw_histograms(
        self,
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )


class Fconst:
    def estimate(self, chromosome: Chromosome):
        return len(chromosome.code)

    def generate_optimal(self, length: int):
        return [
            Chromosome(np.zeros((length,), dtype=int), length),
            Chromosome(np.ones((length,), dtype=int), length),
        ]

    def generate_population(self, n, l, p_m, c_m):
        chromosomes = self.generate_optimal(l) * int(n / 2)
        return Population(chromosomes, p_m, c_m)


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
        return Chromosome(coding, self.extremum_y)

    def get_optimal(self, n, l, p_m, c_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, c_m, i):
        return self.factory.generate_population_fx2(n, l, p_m, c_m, i)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        y = self.score(x)
        return abs(self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA

    def draw_histograms(
        self,
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )
        _draw_fitness_histogram(population, folder_name, func_name, run, iteration)
        _draw_phenotype_histogram(
            self.a, self.b, population, folder_name, func_name, run, iteration
        )


class F5122subx2:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self.extremum_x = 0
        self.extremum_y = 0
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.pow(5.12, 2) - math.pow(x, 2)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return math.pow(5.12, 2) - math.pow(x, 2)

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def get_optimal(self, n, l, p_m, c_m, i):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        coding = encode(self.extremum_x, self.a, self.b, length)
        return Chromosome(coding, self.extremum_y)

    def generate_population(self, n, l, p_m, c_m, i):
        return self.factory.generate_population_f5122subx2(n, l, p_m, c_m, i)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        y = self.score(x)
        return abs(self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA

    def draw_histograms(
        self,
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )
        _draw_fitness_histogram(population, folder_name, func_name, run, iteration)
        _draw_phenotype_histogram(
            self.a, self.b, population, folder_name, func_name, run, iteration
        )


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
        return Chromosome(coding, self.extremum_y)

    def get_optimal(self, n, l, p_m, c_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, c_m, i):
        return self.factory.generate_population_fecx(n, l, p_m, c_m, i)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        y = self.score(x)
        return abs(self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA

    def draw_histograms(
        self,
        population: Population,
        folder_name: str,
        func_name: str,
        run: int,
        iteration: int,
    ) -> None:
        _draw_count_ones_in_genotype_histogram(
            population, folder_name, func_name, run, iteration
        )
        _draw_fitness_histogram(population, folder_name, func_name, run, iteration)
        _draw_phenotype_histogram(
            self.a, self.b, population, folder_name, func_name, run, iteration
        )
